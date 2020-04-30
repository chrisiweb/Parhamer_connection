from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
import os
import subprocess
from functools import partial
from config import colors_ui, config_file, config_loader, logo_path, path_programm
import json
import shutil
import datetime
import time
from datetime import date
from refresh_ddb import refresh_ddb, modification_date
from sort_items import natural_keys
from standard_dialog_windows import question_window


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

def get_color(color):
    color= "rgb({0}, {1}, {2})".format(color.red(), color.green(), color.blue())
    return color

blue_7=colors_ui['blue_7']


class Ui_Dialog_loading(object):
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        Dialog.setWindowFlags(QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint)
        Dialog.setWindowTitle('Lade...')
        Dialog.setStyleSheet("background-color: {}; color: white".format(get_color(blue_7)))
        pixmap = QtGui.QPixmap(logo_path)
        Dialog.setWindowIcon(QtGui.QIcon(logo_path))
        Dialog.setFixedSize(200,50)
        verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        verticalLayout.setObjectName("verticalLayout")

        label=QtWidgets.QLabel(Dialog)
        label.setObjectName("label")  
        label.setText("Die PDF Datei wird erstellt...")
        # label.setFixedSize(200,50)
        # label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        label.setAlignment(QtCore.Qt.AlignCenter)
        verticalLayout.addWidget(label)
             


class Worker(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    @QtCore.pyqtSlot()
    def task(self, folder_name, file_name, latex_output_file):
        process = build_pdf_file(folder_name, file_name, latex_output_file)
        process.poll()
        latex_output_file.close()

        loading_animation(process)

        process.wait()

        # for i in range(10000):
        #     print(i)
        self.finished.emit()


def prepare_tex_for_pdf(self):
    QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

    chosen_aufgabenformat = "Typ%sAufgaben" % self.label_aufgabentyp.text()[-1]

    if self.chosen_program == "lama":
        log_file = os.path.join(
            path_programm,
            "Teildokument",
            "log_file_%s" % self.label_aufgabentyp.text()[-1],
        )
    if self.chosen_program == "cria":
        log_file = os.path.join(path_programm, "Teildokument", "log_file_cria")

    if not os.path.isfile(log_file):
        refresh_ddb(self)  # self.label_aufgabentyp.text()[-1]
    else:  ##  Automatic update once per month
        month_update_log_file = modification_date(log_file).strftime("%m")
        month_today = datetime.date.today().strftime("%m")
        if month_today != month_update_log_file:
            refresh_ddb(self)  # self.label_aufgabentyp.text()[-1]

    suchbegriffe = []

    if self.chosen_program == "lama":
        for widget in self.dict_widget_variables:
            if widget.startswith("checkbox_search_"):
                if self.dict_widget_variables[widget].isChecked() == True:
                    if "gk" in widget:
                        gk = widget.split("_")[-1]
                        suchbegriffe.append(dict_gk[gk])

                    if "themen" in widget:
                        klasse = widget.split("_")[-2]
                        thema = widget.split("_")[-1]
                        suchbegriffe.append(thema.upper())

        # #### ALGEBRA UND GEOMETRIE
        # for all in ag_beschreibung:
        #     x = eval("self.cb_" + all)
        #     if x.isChecked() == True:
        #         suchbegriffe.append(all)

        # #### ANALYSIS
        # for all in an_beschreibung:
        #     x = eval("self.cb_" + all)
        #     if x.isChecked() == True:
        #         suchbegriffe.append(all)

        # #### FUNKTIONALE ABHÄNGIGKEITEN
        # for all in fa_beschreibung:
        #     x = eval("self.cb_" + all)
        #     if x.isChecked() == True:
        #         suchbegriffe.append(all)
        # #### WAHRSCHEINLICHKEIT UND STATISTIK
        # for all in ws_beschreibung:
        #     x = eval("self.cb_" + all)
        #     if x.isChecked() == True:
        #         suchbegriffe.append(all)

        # temp_suchbegriffe = []
        # for all in suchbegriffe:
        #     temp_suchbegriffe.append(dict_gk[all])
        # suchbegriffe = temp_suchbegriffe
        # print(suchbegriffe)
        # return
        #### Suche der Schulstufe

        # for y in range(5, 9):
        #     themen_klasse = eval("k%s_beschreibung" % y)
        #     for all in themen_klasse:
        #         x = eval("self.cb_k%s_" % y + all)
        #         grade = "K" + str(y)
        #         if x.isChecked() == True:
        #             # if grade not in suchbegriffe:
        #             # suchbegriffe.append('K'+str(y))
        #             suchbegriffe.append(all.upper())

    #### typ1 ###
    # log_file=os.path.join(path_programm,'Typ 2 Aufgaben','Teildokument','log_file')
    ######

    # log_file = os.path.join(
    #     path_programm,
    #     "Teildokument",
    #     "log_file_%s" % self.label_aufgabentyp.text()[-1],
    # )

    with open(log_file, encoding="utf8") as f:
        beispieldaten_dateipfad = json.load(f)
        # beispieldaten_dateipfad=eval(beispieldaten_dateipfad)
        beispieldaten = list(beispieldaten_dateipfad.keys())

    if self.cb_drafts.isChecked():
        # print(beispieldaten_dateipfad)
        QtWidgets.QApplication.restoreOverrideCursor()
        drafts_path = os.path.join(path_programm, "Beispieleinreichung")

        if self.chosen_program == "lama":
            for all in os.listdir(drafts_path):
                if all.endswith(".tex") or all.endswith(".ltx"):
                    pattern = re.compile("[A-Z][A-Z]")
                    if int(self.label_aufgabentyp.text()[-1]) == 1:
                        if pattern.match(all):
                            file = open(os.path.join(drafts_path, all), encoding="utf8")
                            for i, line in enumerate(file):
                                if not line == "\n":
                                    # line=line.replace('\section{', 'section{ENTWURF ')
                                    beispieldaten_dateipfad[
                                        "ENTWURF " + line
                                    ] = os.path.join(drafts_path, all)
                                    beispieldaten.append(line)
                                    break
                            file.close()
                    if int(self.label_aufgabentyp.text()[-1]) == 2:
                        if not pattern.match(all):
                            file = open(os.path.join(drafts_path, all), encoding="utf8")
                            for i, line in enumerate(file):
                                if not line == "\n":
                                    # line=line.replace('\section{', 'section{ENTWURF ')
                                    beispieldaten_dateipfad[
                                        "ENTWURF " + line
                                    ] = os.path.join(drafts_path, all)
                                    beispieldaten.append(line)
                                    break
                            file.close()

        elif self.chosen_program == "cria":

            if self.cb_drafts.isChecked():
                # print(beispieldaten_dateipfad)
                QtWidgets.QApplication.restoreOverrideCursor()
                drafts_path = os.path.join(path_programm, "Beispieleinreichung")
                for klasse in list_klassen:
                    try:
                        drafts_path = os.path.join(
                            path_programm, "Beispieleinreichung", klasse
                        )
                        for all in os.listdir(drafts_path):
                            file = open(os.path.join(drafts_path, all), encoding="utf8")
                            for i, line in enumerate(file):
                                if not line == "\n":
                                    # line=line.replace('\section{', 'section{ENTWURF ')
                                    beispieldaten_dateipfad[
                                        "ENTWURF " + line
                                    ] = os.path.join(drafts_path, all)
                                    beispieldaten.append(line)
                                    break
                            file.close()
                    except FileNotFoundError:
                        pass

        # print(beispieldaten_dateipfad)
        # return

        # for root, dirs, files in os.walk(os.path.join(path_programm,'_database', chosen_aufgabenformat)):
        # 	for all in files:
        # 		if all.endswith('.tex') or all.endswith('.ltx'):
        # 			if not ('Gesamtdokument' in all) and not ('Teildokument' in all):
        # 				file=open(os.path.join(root,all), encoding='utf8')
        # 				for i, line in enumerate(file):
        # 					if not line == "\n":
        # 						beispieldaten_dateipfad[line]=os.path.join(root,all)
        # 						beispieldaten.append(line)
        # 						break
        # 				file.close()

    ######### new tabu.sty not working ###
    ######################################################
    ########### work around ####################
    #########################################

    path_tabu_pkg = os.path.join(path_programm, "_database", "_config", "tabu.sty")
    copy_path_tabu_pkg = os.path.join(path_programm, "Teildokument", "tabu.sty")
    if os.path.isfile(copy_path_tabu_pkg):
        pass
    else:
        shutil.copy(path_tabu_pkg, copy_path_tabu_pkg)

    ###################################################
    path_srdp_pkg = os.path.join(
        path_programm, "_database", "_config", "srdp-mathematik.sty"
    )
    copy_path_srdp_pkg = os.path.join(
        path_programm, "Teildokument", "srdp-mathematik.sty"
    )
    if os.path.isfile(copy_path_srdp_pkg):
        pass
    else:
        shutil.copy(path_srdp_pkg, copy_path_srdp_pkg)

    ########################################################

    if self.chosen_program == "lama":

        filename_teildokument = os.path.join(
            path_programm,
            "Teildokument",
            "Teildokument_%s.tex" % self.label_aufgabentyp.text()[-1],
        )

    elif self.chosen_program == "cria":
        for all in self.dict_chosen_topics.values():
            suchbegriffe.append(all)

        filename_teildokument = os.path.join(
            path_programm, "Teildokument", "Teildokument_cria.tex"
        )

    try:
        file = open(filename_teildokument, "w", encoding="utf8")
    except FileNotFoundError:
        os.makedirs(filename_teildokument)  # If dir is not found make it recursivly
    file.write(
        "\documentclass[a4paper,12pt]{report}\n\n"
        "\\usepackage{geometry}\n"
        "\geometry{a4paper,left=18mm,right=18mm, top=2cm, bottom=2cm}\n\n"
        "\\usepackage{lmodern}\n"
        "\\usepackage[T1]{fontenc}\n"
        "\\usepackage{eurosym}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\usepackage[ngerman]{babel}\n"
    )
    if self.cb_solution.isChecked() == True:
        file.write("\\usepackage[solution_on]{srdp-mathematik} % solution_on/off\n")
    else:
        file.write("\\usepackage[solution_off]{srdp-mathematik} % solution_on/off\n")
    file.write(
        "\setcounter{Zufall}{0}\n\n\n"
        "\pagestyle{empty} %PAGESTYLE: empty, plain, fancy\n"
        "\onehalfspacing %Zeilenabstand\n"
        "\setcounter{secnumdepth}{-1} % keine Nummerierung der Ueberschriften\n\n\n\n"
        "%\n"
        "%\n"
        "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% DOKUMENT - ANFANG %%%%%%%%%%%%%%%%%%%"
        "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
        "%\n"
        "%\n"
        "\\begin{document}\n"
        '\shorthandoff{"}\n'
    )
    file.close()

    #### Typ1 ####
    # 	if self.combobox_searchtype.currentText()=='Alle Dateien ausgeben, die alle Suchkriterien enthalten':
    #######

    gesammeltedateien = []
    if self.chosen_program == "lama":
        if (
            self.combobox_searchtype.currentText()
            == "Alle Dateien ausgeben, die ausschließlich diese Suchkriterien enthalten"
            and chosen_aufgabenformat == "Typ2Aufgaben"
        ):
            liste_kompetenzbereiche = {}
            gkliste = []
            r = 1
            for all in list(beispieldaten_dateipfad.keys()):
                gkliste = []
                for gkbereich in dict_gk:
                    if dict_gk[gkbereich] in all:
                        gkliste.append(dict_gk[gkbereich])
                liste_kompetenzbereiche.update({r: gkliste})
                r += 1
            for r in range(1, len(liste_kompetenzbereiche) + 1):
                if liste_kompetenzbereiche[r] == []:
                    liste_kompetenzbereiche[r].append("-")
                for all in suchbegriffe:
                    if all in liste_kompetenzbereiche[r]:
                        liste_kompetenzbereiche[r].remove(all)

            gesammeltedateien_temporary = []
            for r in range(1, len(liste_kompetenzbereiche) + 1):
                if liste_kompetenzbereiche[r] == []:
                    gesammeltedateien.append(
                        list(beispieldaten_dateipfad.keys())[r - 1]
                    )
            gesammeltedateien = sorted(gesammeltedateien)

        if (
            self.combobox_searchtype.currentText()
            == "Alle Dateien ausgeben, die zumindest ein Suchkriterium enthalten"
            or chosen_aufgabenformat == "Typ1Aufgaben"
        ):
            gesammeltedateien = []
            for all in suchbegriffe:
                for element in list(beispieldaten_dateipfad.keys())[:]:
                    if all in element:
                        gesammeltedateien.append(element)

        if not len(self.entry_suchbegriffe.text()) == 0:
            suchbegriffe.append(self.entry_suchbegriffe.text())
            if (
                self.combobox_searchtype.currentText()
                == "Alle Dateien ausgeben, die zumindest ein Suchkriterium enthalten"
                or chosen_aufgabenformat == "Typ1Aufgaben"
            ):
                if len(gesammeltedateien) == 0 and len(suchbegriffe) != 0:
                    gesammeltedateien = list(beispieldaten_dateipfad.keys())
            for all in gesammeltedateien[:]:
                if self.entry_suchbegriffe.text().lower() not in all.lower():
                    gesammeltedateien.remove(all)

    if self.chosen_program == "cria":
        if (
            self.combobox_searchtype.currentText()
            == "Alle Dateien ausgeben, die zumindest ein Suchkriterium enthalten"
        ):
            for item in suchbegriffe:
                klasse = item[0].upper()
                thema = item[1] + "." + item[2]
                for all in list(beispieldaten_dateipfad.keys()):
                    if klasse in all:

                        if thema in all:
                            gesammeltedateien.append(all)

        if (
            self.combobox_searchtype.currentText()
            == "Alle Dateien ausgeben, die ausschließlich diese Suchkriterien enthalten"
        ):
            beispieldaten_temporary = list(beispieldaten_dateipfad.keys())
            for item in suchbegriffe:

                klasse = "K" + item[0]
                thema = item[1] + "." + item[2]
                for all in beispieldaten_temporary[:]:
                    if thema not in all:
                        beispieldaten_temporary.remove(all)
                    else:

                        if klasse not in all:
                            beispieldaten_temporary.remove(all)

            gesammeltedateien = beispieldaten_temporary

        if not len(self.entry_suchbegriffe.text()) == 0:
            suchbegriffe.append(self.entry_suchbegriffe.text())
            for all in gesammeltedateien[:]:
                if not len(self.entry_suchbegriffe.text()) == 0:

                    if self.entry_suchbegriffe.text().lower() not in all.lower():
                        gesammeltedateien.remove(all)
    # if not len(self.entry_suchbegriffe.text())==0:
    # 	suchbegriffe.append(self.entry_suchbegriffe.text())

    gesammeltedateien.sort(key=natural_keys)

    dict_gesammeltedateien = {}

    for all in gesammeltedateien:
        dict_gesammeltedateien[all] = beispieldaten_dateipfad[all]

    #### typ1 ###
    # ###############################################
    # #### Auswahl der gesuchten Antwortformate ####
    # ###############################################
    if chosen_aufgabenformat == "Typ1Aufgaben" or self.chosen_program == "cria":
        if (
            self.cb_af_mc.isChecked()
            or self.cb_af_lt.isChecked()
            or self.cb_af_zo.isChecked()
            or self.cb_af_rf.isChecked()
            or self.cb_af_ta.isChecked()
            or self.cb_af_oa.isChecked() == True
        ):
            if suchbegriffe == []:
                dict_gesammeltedateien = beispieldaten_dateipfad
            for all_formats in list(dict_aufgabenformate.keys()):
                x = eval("self.cb_af_" + all_formats)
                if x.isChecked() == False:
                    for all in list(dict_gesammeltedateien):
                        if all_formats.upper() in all:
                            del dict_gesammeltedateien[all]

                        # if all_formats in all:
                        # del dict_gesammeltedateien[all]

                if x.isChecked() == True:
                    suchbegriffe.append(all_formats)
    ########################################################

    ###############################################
    #### Auswahl der gesuchten Klassen #########
    ###############################################

    if self.chosen_program == "lama":
        selected_klassen = []
        if (
            self.cb_k5.isChecked()
            or self.cb_k6.isChecked()
            or self.cb_k7.isChecked()
            or self.cb_k8.isChecked() == True
            or self.cb_matura.isChecked() == True
            or self.cb_univie.isChecked()
        ):
            if suchbegriffe == []:
                dict_gesammeltedateien = beispieldaten_dateipfad
            for all_formats in list(Klassen.keys()):
                # print(all_formats)
                x = eval("self.cb_" + all_formats)
                if x.isChecked() == True:
                    selected_klassen.append(all_formats.upper())
                    suchbegriffe.append(all_formats.upper())
            # print(selected_klassen)
            # print(suchbegriffe)
            for all in list(dict_gesammeltedateien):
                if not any(
                    all_formats.upper() in all for all_formats in selected_klassen
                ):
                    del dict_gesammeltedateien[all]

    # print(dict_gesammeltedateien)

    ##############################
    if not dict_gesammeltedateien:
        QtWidgets.QApplication.restoreOverrideCursor()
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowIcon(QtGui.QIcon(logo_path))
        msg.setText("Es wurden keine passenden Aufgaben gefunden!")
        msg.setInformativeText("Es wird keine Datei ausgegeben.")
        msg.setWindowTitle("Warnung")
        # msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()
        return

    beispieldaten.sort(key=natural_keys)
    file = open(filename_teildokument, "a", encoding="utf8")
    file.write("\n \\scriptsize Suchbegriffe: ")
    if self.chosen_program == "lama":
        for all in suchbegriffe:
            if all == suchbegriffe[-1]:
                file.write(all)
            else:
                file.write(all + ", ")
        file.write("\\normalsize \n \n")

        for key, value in dict_gesammeltedateien.items():
            value = value.replace("\\", "/")
            file = open(filename_teildokument, "a", encoding="utf8")


            if chosen_aufgabenformat == "Typ1Aufgaben":
                if key.startswith("ENTWURF"):
                    file.write('ENTWURF \input{"' + value + '"}%\n' "\hrule	 \leer\n\n")
                else:
                    file.write('\input{"' + value + '"}%\n' "\hrule	 \leer\n\n")
            elif chosen_aufgabenformat == "Typ2Aufgaben":
                if key.startswith("ENTWURF"):
                    file.write('ENTWURF \input{"' + value + '"}%\n' "\\newpage \n")
                else:
                    file.write('\input{"' + value + '"}%\n' "\\newpage \n")

    if self.chosen_program == "cria":
        for all in suchbegriffe:
            if isinstance(all, list):
                item = all[1] + "." + all[2] + " (" + all[0] + ")"
            else:
                item = all.upper()
            if all == suchbegriffe[-1]:
                file.write(item)
            else:
                file.write(item + ", ")
        file.write("\\normalsize \n \n")

        for key, value in dict_gesammeltedateien.items():
            value = value.replace("\\", "/")
            file = open(filename_teildokument, "a", encoding="utf8")
            if key.startswith("ENTWURF"):
                file.write('ENTWURF \input{"' + value + '"}%\n' "\hrule	 \leer\n\n")
            else:
                file.write('\input{"' + value + '"}%\n' "\hrule	 \leer\n\n")

    file.write('\shorthandoff{"}\n' "\end{document}")

    file.close()


    QtWidgets.QApplication.restoreOverrideCursor()
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Question)
    msg.setWindowIcon(QtGui.QIcon(logo_path))
    msg.setText(
        "Insgesamt wurden "
        + str(len(dict_gesammeltedateien))
        + " Aufgaben gefunden.\n "
    )
    msg.setInformativeText("Soll die PDF Datei erstellt werden?")
    msg.setWindowTitle("Datei ausgeben?")
    msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    buttonY = msg.button(QtWidgets.QMessageBox.Yes)
    buttonY.setText("Ja")
    buttonN = msg.button(QtWidgets.QMessageBox.No)
    buttonN.setText("Nein")
    msg.setDefaultButton(QtWidgets.QMessageBox.Yes)
    ret = msg.exec_()

    if ret == QtWidgets.QMessageBox.Yes:
        if self.chosen_program == "lama":
            typ = self.label_aufgabentyp.text()[-1]
        elif self.chosen_program == "cria":
            typ = "cria"

        create_pdf("Teildokument", 0, 0, typ)




def extract_error_from_output(latex_output):
    start=None
    for all in latex_output:
        if all.startswith("! LaTeX Error:"):
            start = latex_output.index(all)
            break    
    if start ==None:
        for all in latex_output:
            if all.startswith("! "):
                start = latex_output.index(all)
                break     

    if start != None:
        list_error = latex_output[start:]

        for all in list_error:
            if all == "":
                end = list_error.index(all)
                break
        error = "".join(list_error[:end])#.replace("\n", "")

        if path_programm in error:
            error_location=None
        else:
            error_location = "".join(latex_output[:start+end])
            index_start=error_location.rfind(path_programm)
            index_end = error_location[index_start:].find('.tex')+4

            error_location = error_location[index_start:index_start+index_end]


        if error_location==None:
            detailed_text= error
        else:
            detailed_text= error + "\n\nFehlerhafte Datei:\n" + error_location     
        QtWidgets.QApplication.restoreOverrideCursor()
        response = question_window(
            "Fehler beim Erstellen der PDF-Datei",
            "Es ist ein Fehler beim Erstellen der PDF-Datei aufgetreten. Dadurch konnte die PDF-Datei nicht vollständig erzeugt werden.\n\n"+
            'Dies kann viele unterschiedliche Ursachen haben (siehe Details).\n'+
            'Durch das Aktualisieren der Datenbank ("Refresh Datsbase") können jedoch die meisten dieser Fehler behoben werden.\n'+
            'Sollte der Fehler weiterhin bestehen, bitte kontaktieren Sie uns unter lama.helpme@gmail.com',
            "Wollen Sie die fehlerhafte PDF-Datei dennoch anzeigen?",
            "Fehlermeldung:\n" + detailed_text,
        )

        return response


def build_pdf_file(folder_name, file_name, latex_output_file):
    if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        process=subprocess.Popen(
            'cd "{0}" ; latex -interaction=nonstopmode --synctex=-1 "{1}.tex" ; dvips "{1}.dvi" ; ps2pdf -dNOSAFER "{1}.ps"'.format(
                folder_name, file_name
            ),
            stdout=latex_output_file,
            shell=True,
        )

    else:
        process=subprocess.Popen(
            'cd "{0}" & latex -interaction=nonstopmode --synctex=-1 "{1}.tex"& dvips "{1}.dvi" & ps2pdf -dNOSAFER "{1}.ps"'.format(
                folder_name, file_name
            ),
            cwd=os.path.splitdrive(path_programm)[0],
            stdout=latex_output_file,
            shell=True,
        )
    return process

def open_pdf_file(folder_name, file_name):
    file_path = os.path.join(folder_name, file_name)
    if sys.platform.startswith("linux"):
        subprocess.run(
            [
                "sudo",
                "xdg-open",
                "{0}.pdf".format(file_path),
            ]
        )
    elif sys.platform.startswith("darwin"):
        subprocess.run(
            ["open", "{0}.pdf".format(file_path),]
            )
    else:
        if os.path.isfile(
            os.path.join("C:\\", "Program Files", "SumatraPDF", "SumatraPDF.exe")
        ):
            sumatrapdf = os.path.join(
                "C:\\", "Program Files", "SumatraPDF", "SumatraPDF.exe"
            )
        elif os.path.isfile(
            os.path.join(
                "C:\\", "Program Files (x86)", "SumatraPDF", "SumatraPDF.exe"
            )
        ):
            sumatrapdf = os.path.join(
                "C:\\", "Program Files (x86)", "SumatraPDF", "SumatraPDF.exe"
            )
        else:
            sumatrapdf = ""


        subprocess.Popen(
            'cd "{0}" &"{1}" "{2}.pdf"'.format(
                folder_name, sumatrapdf, file_name
            ),
            cwd=os.path.splitdrive(path_programm)[0],
            shell=True,
        ).poll()


def loading_animation(process):
    animation = "|/-\\"
    idx = 0
    while True:
        if process.poll()!=None:
            print('Done')
            break
        print(animation[idx % len(animation)], end="\r")
        idx += 1
        time.sleep(0.1)  

def delete_unneeded_files(folder_name, file_name):
    file_path = os.path.join(folder_name, file_name)
    os.unlink("{0}.aux".format(file_path))
    os.unlink("{0}.log".format(file_path))
    os.unlink("{0}.dvi".format(file_path))
    os.unlink("{0}.ps".format(file_path))

def create_pdf(path_file, index, maximum, typ=0):

    # Dialog = QtWidgets.QDialog(
    #     None,
    #     QtCore.Qt.WindowSystemMenuHint
    #     | QtCore.Qt.WindowTitleHint
    #     | QtCore.Qt.WindowCloseButtonHint,
    # )
    # ui = ModalInfoDialog()
    # ui.setupUi(Dialog, "Test")
    # Dialog.show()

    # msg = QtWidgets.QMessageBox()
    # msg.setText("Die PDF Datei wird erstellt...")
    # msg.setStandardButtons(QtWidgets.QMessageBox.Abort)
    # buttonAbort = msg.button(QtWidgets.QMessageBox.Abort)
    # buttonAbort.setText("Abbrechen")

    # msg.show()
    # thread = QtCore.QThread(msg)
    # worker = Worker()
    # worker.finished.connect(msg.close)
    # worker.moveToThread(thread)
    # thread.started.connect(worker.task)
    # thread.start()
    # thread.exit()
    # response = msg.exec()

    # if response == QtWidgets.QMessageBox.Abort:
    #     print('test')
        # thread.wait()
        # return
        # sys.exit() 



    # d = 
    # d.show()
    # thread = QtCore.QThread(d)

    # worker = Worker()
    # worker.finished.connect(d.close)
    # worker.moveToThread(thread)
    # thread.started.connect(worker.task)
    # thread.start()

    # return

    # if sys.platform.startswith("linux"):
    #     pass
    # else:
    #     msg = QtWidgets.QMessageBox()
    #     msg.setWindowIcon(QtGui.QIcon(logo_path))
    #     msg.setWindowTitle("Lade...")
    #     msg.setStandardButtons(QtWidgets.QMessageBox.NoButton)
    #     if path_file == "Teildokument" or path_file == "Schularbeit_Vorschau":
    #         rest = ""
    #     else:
    #         rest = " ({0}|{1})".format(index + 1, maximum)
    #     msg.setText("Die PDF Datei wird erstellt..." + rest)

    #     msg.show()
    #     QApplication.processEvents()
    QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
    if path_file == "Teildokument":
        folder_name = '{0}/Teildokument'.format(path_programm)
        file_name = path_file + "_" + typ
    else:
        head, tail = os.path.split(path_file)
        file_name = tail
        if path_file == 'Schularbeit_Vorschau':
            folder_name = '{0}/Teildokument'.format(path_programm)
        else:
            folder_name = head
    
    print('Pdf-Datei wird erstellt. Bitte warten...')

    latex_output_file = open(
        "{0}/Teildokument/temp.txt".format(path_programm), "w", encoding="utf8", errors='ignore'
    )


    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog_loading()
    ui.setupUi(Dialog)
    # print(QMainWindow().pos().x())
    # print(QMainWindow().pos().y())

    # msg = QtWidgets.QMessageBox()
    # msg.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    # height =  QMainWindow().geometry().height()
    # width =  QMainWindow().geometry().width()
    # x= QMainWindow().pos().x()
    # y=QMainWindow().pos().y()

    # msg.setStyleSheet("QLabel{min-width:200 px; min-height:100px}")
    # msg.move(x+0.5*height, y+0.6*width)

    # msg.setWindowIcon(QtGui.QIcon(logo_path))
    # QtGui.QPixmap.pixmap = ExportS
    # pixmap = QtGui.QPixmap(logo_path)
    # msg.setWindowIcon(QtGui.QIcon(logo_path))
    # msg.setIconPixmap(logo_path)
    # # msg.setIcon(QtGui.QIcon(logo_path))
    # # msg.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
    # # msg.setDetailedText("These details disable the close button for some reason.")
    # msg.setWindowFlags(msg.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
    # # msg.move(QMainWindow().pos().x()+200, QMainWindow().pos().y()+200)
    # # msg.setWindowFlags(QtCore.Qt.WindowTitleHint)
    # #QtCore.Qt.FramelessWindowHint
    # # msg.setWindowFlags(QtCore.Qt.WindowTitleHint)
    #     # QtCore.Qt.WindowSystemMenuHint
    #     #     # | QtCore.Qt.WindowTitleHint
    #         # | QtCore.Qt.WindowCloseButtonHint)
    # # msg.setWindowTitle("Lade...")
    # msg.setText("Die PDF Datei wird erstellt...")
    # msg.setStandardButtons(QtWidgets.QMessageBox.Abort)
    # buttonAbort = msg.button(QtWidgets.QMessageBox.Abort)
    # buttonAbort.hide()
    # buttonAbort.setText('Abbrechen')
    # msg.show()
    thread = QtCore.QThread(Dialog)
    worker = Worker()
    worker.finished.connect(Dialog.close)
    worker.moveToThread(thread)
    thread.started.connect(partial(worker.task, folder_name, file_name, latex_output_file))
    thread.start()
    thread.exit()
    Dialog.exec()

    # if response == QtWidgets.QMessageBox.Abort:
    #     thread.exit()
    #     return

    # process = build_pdf_file(folder_name, file_name, latex_output_file)
    # process.poll()
    # latex_output_file.close()

    # loading_animation(process)

    # process.wait()

    # if sys.platform.startswith("linux"):
    #     pass
    # else:
    #     msg.close()

    latex_output_file = open(
        "{0}/Teildokument/temp.txt".format(path_programm), "r", encoding="utf8", errors='ignore'
    )
    latex_output = latex_output_file.read().splitlines()
    latex_output_file.close()


    response = extract_error_from_output(latex_output)

    if response==False:
        return 

    if file_name == "Schularbeit_Vorschau" or file_name.startswith("Teildokument"):
        open_pdf_file(folder_name, file_name)

    try:
        delete_unneeded_files(folder_name, file_name)
    except Exception as e:
        print('error')
        return
    QtWidgets.QApplication.restoreOverrideCursor()

