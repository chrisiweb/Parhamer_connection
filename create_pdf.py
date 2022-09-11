from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QMessageBox
import sys
import os
import re
import json
import subprocess


from config_start import path_programm, path_localappdata_lama, lama_settings_file
from config import (
    config_file,
    config_loader,
    logo_path,
    is_empty,
    shorten_gk,
)
import json
import shutil
from datetime import date, timedelta 
from time import sleep
from refresh_ddb import refresh_ddb, modification_date
from sort_items import order_gesammeltedateien
from standard_dialog_windows import critical_window,question_window, warning_window
from processing_window import working_window_latex_output
import webbrowser
from tinydb import Query
from database_commands import _database, _database_addon, _local_database, get_aufgabentyp
from tex_minimal import tex_preamble, tex_end, begin_beispiel, end_beispiel, begin_beispiel_lang, end_beispiel_lang
from distutils.spawn import find_executable



ag_beschreibung = config_loader(config_file, "ag_beschreibung")
an_beschreibung = config_loader(config_file, "an_beschreibung")
fa_beschreibung = config_loader(config_file, "fa_beschreibung")
ws_beschreibung = config_loader(config_file, "ws_beschreibung")

k5_beschreibung = config_loader(config_file, "k5_beschreibung")
k6_beschreibung = config_loader(config_file, "k6_beschreibung")
k7_beschreibung = config_loader(config_file, "k7_beschreibung")
k8_beschreibung = config_loader(config_file, "k8_beschreibung")

dict_gk = config_loader(config_file, "dict_gk")
Klassen = config_loader(config_file, "Klassen")
list_klassen = config_loader(config_file, "list_klassen")

dict_aufgabenformate = config_loader(config_file, "dict_aufgabenformate")


class Worker_CreatePDF(QObject):
    finished = pyqtSignal()
    signalUpdateOutput = pyqtSignal(object, str)
    @pyqtSlot()
    def task(self, ui, folder_name, file_name, latex_output_file):
        process = build_pdf_file(ui, folder_name, file_name, latex_output_file)

        ui.latex_error_occured = False
        logfile = ""

        while process.poll() is None:
            output = process.stdout.readline().strip()
            if output:
                msg = output.decode("utf-8", 'ignore')
                logfile += msg
                if ui.latex_error_occured != False:
                    ui.latex_error_occured += msg    
                possible_errors = [
                    "! Emergency stop.",
                    "! LaTeX Error:",
                    "Unrecoverable error",
                    "! Undefined control sequence",
                    "! Missing $ inserted",
                    "! Missing } inserted",
                ]

                for all in possible_errors:
                    if all in msg: 
                        ui.latex_error_occured = logfile
                        break
                # if ("! Emergency stop." in msg or 
                # "! LaTeX Error:" in msg or 
                # "Unrecoverable error" in msg or
                # "! Missing $ inserted" in msg or
                # "! Missing } inserted" in msg
                # ):
                #     ui.latex_error_occured = logfile

                self.signalUpdateOutput.emit(ui, msg)

        process.wait()

        self.finished.emit()



def get_number_of_variations(file_name, gesammeltedateien):
    counter = 0

    for all in gesammeltedateien:
        if re.search("{}\[.+\]".format(file_name), all['name']) != None:
            counter +=1

    return counter




def check_gks_not_included(gk_liste, suchbegriffe):
    list_ = []
    for all in gk_liste:
        if all not in suchbegriffe:
            list_.append(all)
    if list_ != []:
        return list_
    else:
        return

def refresh_ddb_according_to_intervall(self, log_file):
    try:
        self.lama_settings['database']
    except KeyError:
        self.lama_settings['database']=2

    if self.lama_settings['database']==1:
        today = date.today()
        week_ago = today - timedelta(days=7)
        week_ago = week_ago.strftime("%y%m%d")
        date_logfile = modification_date(log_file).strftime("%y%m%d")
        if int(date_logfile)<int(week_ago):
            refresh_ddb(self)

    elif self.lama_settings['database'] == 2:
        month_today = date.today().strftime("%m")
        month_update_log_file = modification_date(log_file).strftime("%m")
        if month_today != month_update_log_file:
            refresh_ddb(self)  # self.label_aufgabentyp.text()[-1]
    
    elif self.lama_settings['database'] == 3:
        return

    self.label_update.setText(
        "Letztes Update: "
        + modification_date(log_file).strftime("%d.%m.%y - %H:%M")
    )
    

def collect_suchbegriffe(self):
    chosen_aufgabenformat = "Typ{}Aufgaben".format(self.combobox_aufgabentyp.currentIndex()+1) #self.label_aufgabentyp.text()[-1]

    suchbegriffe = {
        'themen':[],
        'af' : [],
        'klasse' : [],
        'erweiterte_suche' : '',
        'info' : []
        }

    if self.chosen_program == "lama":
        for widget in self.dict_widget_variables:
            if widget.startswith("checkbox_search_"):
                if self.dict_widget_variables[widget].isChecked() == True:
                    if "gk" in widget:
                        gk = widget.split("_")[-1]
                        suchbegriffe['themen'].append(dict_gk[gk])

                    if "themen" in widget:
                        # klasse = widget.split("_")[-2]
                        thema = widget.split("_")[-1]
                        suchbegriffe['themen'].append(thema.upper())


    if self.chosen_program == "cria":
        suchbegriffe['klasse'].append(None)
        for all in self.dict_chosen_topics.values():
            thema_string  = all[1] + "." + all[2]
            suchbegriffe['themen'].append(thema_string)
            if all[0] not in suchbegriffe['klasse']:
                suchbegriffe['klasse'].append(all[0])

            


    if chosen_aufgabenformat == "Typ1Aufgaben" or self.chosen_program == "cria":
        if (
            self.cb_af_mc.isChecked()
            or self.cb_af_lt.isChecked()
            or self.cb_af_zo.isChecked()
            or self.cb_af_rf.isChecked()
            or self.cb_af_ta.isChecked()
            or self.cb_af_oa.isChecked()
            or self.cb_af_ko.isChecked()
        ):
            for all_formats in list(dict_aufgabenformate.keys()):
                x = eval("self.cb_af_" + all_formats)

                if x.isChecked():
                    suchbegriffe['af'].append(all_formats)



    if not len(self.entry_suchbegriffe.text()) == 0:
        suchbegriffe['erweiterte_suche'] = self.entry_suchbegriffe.text()



    if self.chosen_program == "lama":
        if (
            self.cb_k5.isChecked()
            or self.cb_k6.isChecked()
            or self.cb_k7.isChecked()
            or self.cb_k8.isChecked()
            or self.cb_mat.isChecked()
            or self.cb_univie.isChecked()
        ):
            for all_formats in list(Klassen.keys()):
                x = eval("self.cb_" + all_formats)
                if x.isChecked() == True:
                    if all_formats == 'mat' or all_formats == 'univie':
                        suchbegriffe['info'].append(all_formats)
                    else:
                        suchbegriffe['klasse'].append(all_formats)

        # if self.cb_mat.isChecked():
        #     suchbegriffe['info'].append('mat')
        # if self.cb_univie.isChecked():
        #     suchbegriffe['info'].append('univie')

    
    return suchbegriffe

def get_program(self):
    if self.chosen_program == 'cria':
        return 'cria'
    elif self.combobox_aufgabentyp.currentIndex()==0:
    # elif int(self.label_aufgabentyp.text()[-1])==1:
        return 'lama_1'
    else:
        return 'lama_2'



def search_in_database(self,current_program, database,suchbegriffe):
    table = 'table_' + current_program
    table_lama = database.table(table)
    _file_ = Query()    

    string_in_list_af = lambda s: True if (s in suchbegriffe['af'] or is_empty(suchbegriffe['af'])) else False
    string_in_list_klasse = lambda s: True if (s in suchbegriffe['klasse'] or is_empty(suchbegriffe['klasse'])) else False
    string_in_list_info = lambda s: True if (s in suchbegriffe['info'] or is_empty(suchbegriffe['info'])) else False
    lineedit_in_erweitert = lambda s: True if (r"{}".format(suchbegriffe['erweiterte_suche'].lower()) in s.lower() or is_empty(suchbegriffe['erweiterte_suche'])) else False
 
    search_True = lambda s: True


    def include_drafts(value):
        if value == False:
            return True
        else:
            if self.cb_drafts.isChecked():
                return True
            else:
                return False
    
    def lineedit_in_bilder(value):
        for bilder in value:
            if suchbegriffe['erweiterte_suche'].lower() in bilder:
                return True
        return False

    def lineedit_in_name(value):
        simplified_search = shorten_gk(suchbegriffe['erweiterte_suche'].lower())
        simplified_value = shorten_gk(value)
        # print(short_gk)#

        _list= simplified_search.split("-")
        gk_search = _list[0]
        num_search = _list[-1]

        _list= simplified_value.split("-")
        gk_value = _list[0]
        num_value = _list[-1]


        if "*" in gk_search:
            gk_search = gk_search.replace("*", ".*")
            x= re.fullmatch("{}".format(gk_search), gk_value)
            if x == None:
                return False
        elif gk_search != gk_value:
            return False

        if "*" in num_search:
            num_search = num_search.replace("*", ".*")
            x= re.fullmatch("{}".format(num_search), num_value)
            if x == None:
                return False
        elif num_search != num_value:
            return False     

        return True


    if suchbegriffe['erweiterte_suche'] == "":
        suche_complete = eval("_file_.titel.test(search_True)")
    else:
        string_suche = ""
        for filter in self.set_filters:
            if filter == "Titel":
                erweiterte_suche = "_file_.titel.test(lineedit_in_erweitert)"
            elif filter == "Inhalt":
                erweiterte_suche = "_file_.content.test(lineedit_in_erweitert)"
            elif filter == "Quelle":
                erweiterte_suche = "_file_.quelle.test(lineedit_in_erweitert)"
            elif filter == "Bilder":
                erweiterte_suche = "_file_.bilder.test(lineedit_in_bilder)"
            elif filter == "Aufgaben-ID":
                erweiterte_suche = "_file_.name.test(lineedit_in_name)"
            
            if string_suche == "":
                string_suche = erweiterte_suche
            else:
                string_suche = f"{string_suche} | {erweiterte_suche}"
        
        suche_complete = eval(string_suche)


    gesammeltedateien = []
    if current_program == 'lama_1' or (current_program == 'cria' and self.combobox_searchtype.currentIndex()==0):
        if suchbegriffe['themen'] != []:
            gesammeltedateien = table_lama.search(
                (_file_.themen.any(suchbegriffe['themen'])) &
                (_file_.af.test(string_in_list_af)) &
                (_file_.klasse.test(string_in_list_klasse)) &
                (_file_.info.test(string_in_list_info)) &
                (suche_complete) &
                (_file_.draft.test(include_drafts))
            )
        else:
            gesammeltedateien = table_lama.search(
                (_file_.af.test(string_in_list_af)) &
                # (_file_.klasse.test(string_in_list_klasse)) &
                (_file_.info.test(string_in_list_info)) &
                (suche_complete) &
                (_file_.draft.test(include_drafts))
            )

    elif current_program == 'cria' and self.combobox_searchtype.currentIndex()==1:
        def themen_included(value):
            for all in suchbegriffe['themen']:
                if all not in value:
                    return False
            return True
        # 
        if suchbegriffe['themen'] != []:
            gesammeltedateien = table_lama.search(
                (_file_.themen.test(themen_included)) &
                (_file_.af.test(string_in_list_af)) &
                (_file_.klasse.test(string_in_list_klasse)) &
                (_file_.info.test(string_in_list_info)) &
                (suche_complete) &
                (_file_.draft.test(include_drafts))
            )
        else:
            gesammeltedateien = table_lama.search(
                (_file_.af.test(string_in_list_af)) &
                # (_file_.klasse.test(string_in_list_klasse)) &
                (_file_.info.test(string_in_list_info)) &
                (suche_complete) &
                (_file_.draft.test(include_drafts))
            )        
  
    elif current_program == 'lama_2':
        def gk_in_list(value):
            for all in value:
                if all not in suchbegriffe['themen']:
                    return False
            return True

        if suchbegriffe['themen'] == []:
            gesammeltedateien = table_lama.search(
                (_file_.klasse.test(string_in_list_klasse)) &
                (_file_.info.test(string_in_list_info)) &
                (suche_complete) &
                (_file_.draft.test(include_drafts))
            )
        elif self.combobox_searchtype.currentIndex()==0:
            gesammeltedateien = table_lama.search(
                (_file_.themen.any(suchbegriffe['themen'])) &
                (_file_.klasse.test(string_in_list_klasse)) &
                (_file_.info.test(string_in_list_info)) &
                (suche_complete) &
                (_file_.draft.test(include_drafts))
            )

        elif self.combobox_searchtype.currentIndex()==1:
            gesammeltedateien = table_lama.search(
                (_file_.themen.test(gk_in_list)) &
                (_file_.klasse.test(string_in_list_klasse)) &
                (_file_.info.test(string_in_list_info)) &
                (suche_complete) &
                (_file_.draft.test(include_drafts))
            )      
        

    return gesammeltedateien

def check_if_suchbegriffe_is_empty(suchbegriffe, language_index):
    _list = ['themen', 'af', 'klasse', 'erweiterte_suche' ,'info']
    for all in _list:
        if not is_empty(suchbegriffe[all]) and suchbegriffe[all] != [None]:
            return False
    if language_index ==2:
        return False
    return True

def prepare_tex_for_pdf(self):
    QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
    suchbegriffe = collect_suchbegriffe(self)

    response = check_if_suchbegriffe_is_empty(suchbegriffe, self.combobox_translation.currentIndex())
    if response == True:
        QApplication.restoreOverrideCursor()
        warning_window("Bitte wählen Sie zumindest ein Suchkriterium aus.")
        return

    current_program = get_program(self)



    list_1 = search_in_database(self, current_program,_local_database ,suchbegriffe)
    list_1.sort(key=order_gesammeltedateien)
    
    list_2 = search_in_database(self, current_program,_database ,suchbegriffe)
    # for all in _list:
    #     gesammeltedateien.append(all)

    if _database_addon != None:
        list_3 = search_in_database(self, current_program,_database_addon ,suchbegriffe)
        for all in list_3:
            list_2.append(all)
   

    list_2.sort(key=order_gesammeltedateien)
    
    gesammeltedateien = list_1 + list_2

    # print(suchbegriffe)
    # print(gesammeltedateien)
    # return
    ######################################################
    ########### work around ####################
    #########################################

    # path_tabu_pkg = os.path.join(path_programm, "_database", "_config", "tabu.sty")
    # copy_path_tabu_pkg = os.path.join(path_localappdata_lama,"Teildokument","tabu.sty")
    # if os.path.isfile(copy_path_tabu_pkg):
    #     pass
    # else:
    #     shutil.copy2(path_tabu_pkg, copy_path_tabu_pkg)
    ###################################################################

    path_srdptables_pkg = os.path.join(path_programm, "_database", "_config", "srdp-tables.sty")
    copy_path_srdptables_pkg = os.path.join(path_localappdata_lama,"Teildokument","srdp-tables.sty")
    if os.path.isfile(copy_path_srdptables_pkg):
        pass
    else:
        try:
            shutil.copy2(path_srdptables_pkg, copy_path_srdptables_pkg)
        except FileNotFoundError:
            refresh_ddb(self)
            shutil.copy2(path_srdptables_pkg, copy_path_srdptables_pkg)

    ###################################################
    path_srdp_pkg = os.path.join(
        path_programm, "_database", "_config", "srdp-mathematik.sty"
    )
    copy_path_srdp_pkg = os.path.join(
        path_localappdata_lama,"Teildokument","srdp-mathematik.sty"
    )
    if os.path.isfile(copy_path_srdp_pkg):
        pass
    else:
        shutil.copy2(path_srdp_pkg, copy_path_srdp_pkg)

    ########################################################

    if self.chosen_program == "lama":

        filename_teildokument = os.path.join(
            path_programm,
            "Teildokument",
            "Teildokument_{}.tex".format(self.combobox_aufgabentyp.currentIndex()+1) ,
        )

    if self.chosen_program == "cria":
        # for all in self.dict_chosen_topics.values():
        #     suchbegriffe.append(all)

        filename_teildokument = os.path.join(
            path_programm, "Teildokument", "Teildokument_cria.tex"
        )

    if self.cb_solution.isChecked():
        solutions = "solution_on"
    else:
        solutions = "solution_off"

    if self.cb_show_variation.isChecked():
        variation = True
    else:
        variation = False


    if self.cb_infos.isChecked():
        infos = "info_on"
    else:
        infos = "info_off"

    # print(suchbegriffe)
    # print(self.chosen_program)
    if self.chosen_program == "lama" and (suchbegriffe['klasse'] == [] and suchbegriffe['info'] == [] and suchbegriffe['erweiterte_suche'] == ""):
        spezielle_suche = False
    elif self.chosen_program == "cria" and suchbegriffe['erweiterte_suche'] == "":
        spezielle_suche = False
    else:
        spezielle_suche = True

    language_index = self.combobox_translation.currentIndex()

    construct_tex_file(filename_teildokument, gesammeltedateien, current_program, solutions, variation, infos, spezielle_suche, language_index)


    number_of_files = get_output_size(gesammeltedateien, variation, spezielle_suche, language_index)

    QApplication.restoreOverrideCursor()
    if number_of_files == 0:
        warning_window("Es konnten keine Aufgaben mit angegebenen Suchkriterien gefunden werden!")
        return


    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)
    msg.setWindowIcon(QIcon(logo_path))
    msg.setText(
        "Insgesamt wurden "
        + str(number_of_files)
        + " Aufgaben gefunden.\n "
    )
    msg.setInformativeText("Soll die PDF Datei erstellt werden?")
    msg.setWindowTitle("Datei ausgeben?")
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    buttonY = msg.button(QMessageBox.Yes)
    buttonY.setText("Ja")
    buttonN = msg.button(QMessageBox.No)
    buttonN.setText("Nein")
    msg.setDefaultButton(QMessageBox.Yes)
    ret = msg.exec_()

    if ret == QMessageBox.Yes:
        if current_program == 'cria':
            try:
                self.last_search_history_cria
            except AttributeError:
                self.comboBox_klassen.addItem("")
                self.comboBox_klassen.setItemText(5, "Letzte Suche")

            self.last_search_history_cria = {'typ': current_program, 'files': gesammeltedateien}    
        else:
            try:
                self.last_search_history
            except AttributeError:
                self.comboBox_at_sage.addItem("")
                self.comboBox_at_sage.setItemText(2, "Letzte Suche")

            self.last_search_history = {'typ': current_program, 'files': gesammeltedateien}


        if self.chosen_program == "lama":
            typ = str(self.combobox_aufgabentyp.currentIndex()+1)#self.label_aufgabentyp.text()[-1]
        elif self.chosen_program == "cria":
            typ = "cria"

        create_pdf("Teildokument", 0, 0, typ)

def get_output_size(gesammeltedateien, variation, spezielle_suche, language_index):
    if language_index == 2:
        number = 0
        for all in gesammeltedateien:
            try:
                if all['content_translation'] != None:
                    if variation == True or check_if_variation(all['name']) == False:
                        number +=1
            except KeyError:
                pass
        return number

    if variation == True or spezielle_suche == True:
        return len(gesammeltedateien)
    number = 0
    for all in gesammeltedateien:
        if check_if_variation(all['name']) == False:
            number += 1
    return number

def check_if_variation(name):
    if re.match(".*\[.+\]", name):
        return True
    else:
        return False

def create_tex(
    file_path,
    content,
    punkte = 0,
    pagebreak = True,
    ):
    try:
        with open(file_path, "w", encoding="utf8") as file:
            file.write(tex_preamble())
            if pagebreak == True:
                file.write(begin_beispiel_lang(punkte=punkte) + "\n")
            else:
                file.write(begin_beispiel(punkte=punkte))
            file.write(content)
            if pagebreak == True:
                file.write(end_beispiel_lang)
            else:
                file.write(end_beispiel)
            
            file.write(tex_end)
        return True
    except Exception as e:
        return e


def construct_tex_file(file_name, gesammeltedateien, current_program, solutions, variation, infos, spezielle_suche, language_index):
    with open(file_name, "w", encoding="utf8") as file:
        if current_program == "lama_2":
            bookmark_value = 1
        else:
            bookmark_value = 2

        file.write(tex_preamble(solution=solutions, bookmark=bookmark_value, info=infos))

        for all in gesammeltedateien:
            if variation == False and check_if_variation(all['name']) == True and spezielle_suche == False:
                continue
            
            if language_index == 2:
                try:
                    if all['content_translation'] == None:
                        continue
                except KeyError:
                    continue

            if all['info'] == 'mat':
                add_on = ' ({})'.format(all['quelle'])
            else:
                add_on = ''

            if all['draft']==True:
                draft = '\\textsc{Entwurf:} '
            else:
                draft = ''


            try: 
                if all['content_translation'] != None and language_index==0:
                    language = " \\flagUK\ "
                else:
                    language = ""
            except KeyError:
                    language = ""

            # print(f"{all['name']} : {language}")

            file.write("\smallskip\\begin{minipage}{1\\textwidth}\n")
            green = "green!40!black!60!"

            if variation == True:
                if check_if_variation(all['name']) == True and not is_empty(language):
                    file.write("{0}\color{{{1}}}\\vspace{{-0.5cm}}\n\n".format(language, green))
                elif check_if_variation(all['name']) == True:
                    file.write("{0}\color{{{1}}}\n".format(language, green))
                elif not is_empty(language):
                    file.write(f"{language}\\vspace{{-0.5cm}}\n\n")
            elif spezielle_suche == False:
                number_of_variations = get_number_of_variations(all['name'], gesammeltedateien)

                if number_of_variations != 0:
                    file.write("{2}{{\color{{{0}}}{{\\fbox{{Anzahl weiterer Variationen dieser Aufgabe: {1}}}}}}}\\vspace{{-0.5cm}}\n\n".format(green, number_of_variations, language))
                elif not is_empty(language):
                    file.write(f"{language}\\vspace{{-0.5cm}}\n\n")
            elif not is_empty(language):
                file.write(f"{language}\\vspace{{-0.5cm}}\n\n")

            if current_program == 'lama_2':
                section = "section"
            else:
                section = "subsection"

            file.write('\{0}{{{1}{2} - {3}{4}}}\smallskip\n\n'.format(section, draft, all['name'], all['titel'], add_on))
            file.write('\end{minipage}\n\n')

            if language_index == 0:
                content = all['content']
            else:
                try:
                    if all['content_translation']!= None:
                        content = all['content_translation']
                    else:
                        content = all['content']
                except KeyError:
                    content = all['content']

            if all['pagebreak']==False:
                file.write(begin_beispiel(all['themen'], all['punkte']) + "\n") 
                file.write(content)
                file.write(end_beispiel)
            elif all['pagebreak']==True:
                file.write(begin_beispiel_lang(all['punkte']) + "\n")
                file.write(content)
                file.write(end_beispiel_lang)
            # if variation == True and check_if_variation(all['name']) == True:
            #     file.write("}")               
               
                            
            file.write("\n")
            info_box = create_info_box(all)
            file.write(info_box)
            file.write("\n")
            file.write("\hrulefill")
            file.write("\n\n")
        file.write(tex_end)


def create_info_box(_file):
    titel = _file['titel']
    gk = ', '.join(_file['themen'])
    if _file['af']!=None:
        try:
            af = dict_aufgabenformate[_file['af']]
        except KeyError:
            print('Fehler in der Datenbank - Aufgabe {0} (AF = {1})'.format(_file['name'],_file['af']))
            af = "Fehler"
        af = "Aufgabenformat: {}\\\\".format(af)
    else:
        af = ""
    if _file['klasse'] == None:
        klasse = "-"
    else:
        klasse = _file['klasse'][-1]
    quelle = _file['quelle']
    if not is_empty(_file['bilder']):
        bilder = "\\\\\nBilder: {}".format(_file['bilder'])
    else:
        bilder = ""

    info_box = """
\info{{\\fbox{{\\begin{{minipage}}{{0.98\\textwidth}}
Titel: {0}\\\\
Grundkompetenz(en): {1}\\\\
{2}
Klasse: {3}\\\\
Quelle: {4}{5}
\end{{minipage}}}}}}
""".format(titel, gk, af, klasse, quelle, bilder)

    return info_box


def extract_error_from_output(latex_output):
    if "! Emergency stop." in latex_output or "! LaTeX Error:" in latex_output:
        QApplication.restoreOverrideCursor()
        response = question_window(
            "Es ist ein Fehler beim Erstellen der PDF-Datei aufgetreten. Dadurch konnte die PDF-Datei nicht vollständig erzeugt werden.\n\n"
            + "Dies kann viele unterschiedliche Ursachen haben (siehe Details).\n"
            + "Durch das Aktualisieren der Datenbank (F5) können jedoch die meisten dieser Fehler behoben werden.\n"
            + "Sollte der Fehler weiterhin bestehen, bitte kontaktieren Sie uns unter lama.helpme@gmail.com",
            "Wollen Sie die fehlerhafte PDF-Datei dennoch anzeigen?",
            "Fehler beim Erstellen der PDF-Datei",
            "Fehlermeldung:\n" + latex_output,
        )

        return response




def build_pdf_file(ui, folder_name, file_name, latex_output_file):
    if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        if "Teildokument" in file_name:
            terminal_command = 'cd "{0}" ; latex -interaction=nonstopmode --synctex=-1 "{1}.tex" ; dvips "{1}.dvi" ; ps2pdf -dNOSAFER -dALLOWPSTRANSPARENCY "{1}.ps"'.format(
                folder_name, file_name
            )        
        else:
            terminal_command = 'cd "{0}" ; latex -interaction=nonstopmode --synctex=-1 "{1}.tex" ; dvips "{1}.dvi" ; ps2pdf -dNOSAFER -dALLOWPSTRANSPARENCY "{1}.ps"'.format(
                folder_name, file_name
            )
         
        process = subprocess.Popen(
            'cd "{0}" ; latex -interaction=nonstopmode --synctex=-1 "{1}.tex" ; dvips "{1}.dvi" ; ps2pdf -dNOSAFER -dALLOWPSTRANSPARENCY "{1}.ps"'.format(
                folder_name, file_name
            ),
            stdout=subprocess.PIPE,
            shell=True,
        )

    else:
        drive_programm = os.path.splitdrive(path_programm)[0]
        drive_save = os.path.splitdrive(folder_name)[0]

        if drive_programm.upper() != drive_save.upper():
            drive = drive_save.upper()
        else:
            drive = ""

        if is_empty(drive):
            terminal_command = 'cd "{0}" & latex -interaction=nonstopmode --synctex=-1 "{1}.tex" & latex -interaction=nonstopmode --synctex=-1 "{1}.tex" & dvips "{1}.dvi" & ps2pdf -dNOSAFER -dALLOWPSTRANSPARENCY "{1}.ps"'.format(
                folder_name, file_name
            )
        else:
            terminal_command = '{0} & cd "{1}" & latex -interaction=nonstopmode --synctex=-1 "{2}.tex" & latex -interaction=nonstopmode --synctex=-1 "{2}.tex" & dvips "{2}.dvi" & ps2pdf -dNOSAFER -dALLOWPSTRANSPARENCY "{2}.ps"'.format(
                drive, folder_name, file_name
            )


        process = subprocess.Popen(
            terminal_command,
            cwd=os.path.splitdrive(path_programm)[0],
            stdout=subprocess.PIPE,
            shell=True
        )


    return process


def open_pdf_file(folder_name, file_name):
    drive_database = os.path.splitdrive(path_localappdata_lama)[0]

    drive_location = os.path.splitdrive(sys.argv[-1])[0]

    if drive_location.upper() != drive_database.upper():
        drive = drive_database.upper()
    else:
        drive = ""


    try:
        with open(lama_settings_file, "r", encoding="utf8") as f:
            lama_settings = json.load(f)
        path_pdf_reader = '{}'.format(lama_settings['pdf_reader'])
    except (FileNotFoundError, KeyError):
        path_pdf_reader = ""

    file_path = os.path.join(folder_name, file_name)

    

    if sys.platform.startswith("linux"):
        file_path = file_path + ".pdf"
        webbrowser.open(file_path, new=2, autoraise=True)
        # os.system("xdg-open {0}.pdf".format(file_path))
        # subprocess.run(
        #     [
        #         # "sudo",
        #         "xdg-open",
        #         "{0}.pdf".format(file_path),
        #     ]
        # )
    elif sys.platform.startswith("darwin"):
        if os.path.exists(path_pdf_reader) == False:
            if is_empty(path_pdf_reader)== False:
                warning_window("Der ausgewählte Pfad des Pdf-Readers zum Öffnen der Dateien ist fehlerhaft. Bitte korrigieren oder löschen Sie diesen.")
            
            subprocess.run(
                ["open", "{0}.pdf".format(file_path)]
            )
        else:
            subprocess.run(
                ["open","-a","{}".format(path_pdf_reader), "{0}.pdf".format(file_path)]
            )
         
    else:
        if os.path.isfile(path_pdf_reader) == False:
            if is_empty(path_pdf_reader)== False:
                warning_window("Der ausgewählte Pfad des Pdf-Readers zum Öffnen der Dateien ist fehlerhaft. Bitte korrigieren oder löschen Sie diesen.")
            path_pdf_reader = ""
        else:
            path_pdf_reader = '"{}"'.format(path_pdf_reader) 

        if is_empty(drive):
            subprocess.Popen(
                'cd "{0}" & {1} {2}.pdf'.format(folder_name,path_pdf_reader, file_name),
                shell = True).poll()
        else:
            drive = "{} &".format(drive)
            subprocess.Popen(
                '{0} cd "{1}" & {2} {3}.pdf'.format(drive, folder_name,path_pdf_reader, file_name),
                shell = True).poll()            

def loading_animation(process):
    animation = "|/-\\"
    idx = 0
    while True:
        if process.poll() != None:
            print("Done")
            break
        print(animation[idx % len(animation)], end="\r")
        idx += 1
        sleep(0.1)


def try_to_delete_file(file):
    try:
        os.unlink(file)
    except FileNotFoundError:
        pass


def delete_unneeded_files(folder_name, file_name):
    file_path = os.path.join(folder_name, file_name)

    try_to_delete_file("{0}.aux".format(file_path))
    try_to_delete_file("{0}.log".format(file_path))
    try_to_delete_file("{0}.dvi".format(file_path))
    try_to_delete_file("{0}.ps".format(file_path))


def create_pdf(path_file, index=0, maximum=0, typ=0):
    # QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
    if path_file == "Teildokument":
        folder_name = "{0}/Teildokument".format(path_programm)
        file_name = path_file + "_" + typ
    else:
        head, tail = os.path.split(path_file)
        file_name = tail
        if path_file == "Schularbeit_Vorschau" or path_file == "preview" or path_file == 'worksheet':
            folder_name = "{0}/Teildokument".format(path_programm)
        else:
            folder_name = head

    # print("Pdf-Datei wird erstellt. Bitte warten...")

    latex_output_file = open(
        "{0}/Teildokument/temp.txt".format(path_localappdata_lama),
        "w",
        encoding="utf8",
        errors="ignore",
    )

    if path_file == "Teildokument" or path_file == "Schularbeit_Vorschau" or path_file == "preview" or path_file == "worksheet":
        text = "Die PDF Datei wird erstellt..."
    else:
        text = "Die PDF Dateien werden erstellt... ({0}|{1})".format(index + 1, maximum)

    # text = "Die PDF Datei wird erstellt..." + rest


    if not find_executable('latex'):
        QApplication.restoreOverrideCursor()

        link = "https://mylama.github.io/lama/downloads.html"
        critical_window("""<h4>Die PDF-Datei konnte nicht erstellt werden, da keine LaTeX-Distribution auf dem Computer gefunden wurde.</h4>

Bitte öffnen Sie <a href='{0}'>lama.schule/downloads</a> und folgen Sie allen Schritten des Installationsguides.<br><br>

Sollte das Problem weiterhin bestehen, melden Sie sich bitte unter lama.helpme@gmail.com""".format(link),
        titel="Keine LaTeX-Distribution gefunden")
        return


    
    errors_latex_output = working_window_latex_output(Worker_CreatePDF(), text, folder_name, file_name, latex_output_file)
    



    if errors_latex_output != False:
        QApplication.restoreOverrideCursor()
        response = question_window(
            "Es ist ein Fehler beim Erstellen der PDF-Datei aufgetreten. Dadurch konnte die PDF-Datei nicht vollständig erzeugt werden.\n\n"
            + "Dies kann viele unterschiedliche Ursachen haben (siehe Details).\n"
            + "Durch das Aktualisieren der Datenbank (F5) können jedoch die meisten dieser Fehler behoben werden.\n"
            + "Sollte der Fehler weiterhin bestehen, bitte kontaktieren Sie uns unter lama.helpme@gmail.com",
            "Wollen Sie die fehlerhafte PDF-Datei dennoch anzeigen?",
            "Fehler beim Erstellen der PDF-Datei",
            "Log-Datei:\n" + "".join(errors_latex_output),
        )
        if response == False:
            return


    if file_name == "Schularbeit_Vorschau" or file_name.startswith("Teildokument") or file_name == "preview"  or file_name == "worksheet":

        # response = extract_error_from_output(latex_output)

        # if response == False:
        #     return

        open_pdf_file(folder_name, file_name)

    try:
        delete_unneeded_files(folder_name, file_name)
    except Exception as e:
        print("Error: " + str(e))
        return
        
    QApplication.restoreOverrideCursor()

