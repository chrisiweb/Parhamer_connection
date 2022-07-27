#!/usr/bin/python3
# -*- coding: utf-8 -*-

__lastupdate__ = "04/22"


##################

show_popup = False

from lama_gui import setup_stackWizard
from start_window import check_if_database_exists
# from worksheet_wizard import get_all_solution_pixels
check_if_database_exists()


from git_sync import git_reset_repo_to_origin
from config import *
from lama_colors import *
import json

from config_start import (
    __version__,
    path_programm,
    path_home,
    path_localappdata_lama,
    lama_settings_file,
    database,
    lama_developer_credentials,
)
# from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication

import sys

# from tinydb import Query


from handle_exceptions import report_exceptions

class Worker_UpdateDatabase(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    @QtCore.pyqtSlot()
    def task(self):
        Ui_MainWindow.reset_successfull = git_reset_repo_to_origin()
        self.finished.emit()


class Worker_LoadLamaFile(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    @QtCore.pyqtSlot()
    def task(self, MainWindow):
        for index in [0,1]:
            for aufgabe in MainWindow.list_alle_aufgaben_sage[index]:
                MainWindow.sage_load_files(aufgabe)

        self.finished.emit()

class Worker_UpdateLaMA(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    @QtCore.pyqtSlot()
    def task(self, path_installer):
        download_link = (
            "https://github.com/mylama/lama/releases/latest/download/LaMA_setup.exe"
        )
        path_installer = os.path.join(path_home, "Downloads", "LaMA_setup.exe")
        # urlretrieve(download_link, path_installer)

        # timeout_start = time.time()

        try:
            r = requests.get(download_link, allow_redirects=True, timeout=(5, 10))
            open(path_installer, "wb").write(r.content)
            self.response = True

        except requests.exceptions.ConnectionError:
            self.response = False

        self.finished.emit()




class Ui_MainWindow(object):
    # global dict_picture_path  # , set_chosen_gk #, list_sage_examples#, dict_alle_aufgaben_sage
    def __init__(self):
        super().__init__()
        # self.dict_alle_aufgaben_sage = {}
        self.list_alle_aufgaben_sage = [[],[]]
        self.dict_widget_variables = {}
        self.list_selected_topics_creator = []
        self.dict_variablen_punkte = {}
        self.dict_variablen_punkte_halb = {}
        self.dict_variablen_translation = {}
        self.dict_variablen_AB = {}
        self.dict_variablen_abstand = {}
        # self.dict_variablen_label = {}
        # self.dict_sage_ausgleichspunkte_chosen = {}
        self.dict_sage_hide_show_items_chosen = {}
        self.dict_sage_individual_change = {}
        self.dict_chosen_topics = {}
        self.list_copy_images = []
        self.dict_picture_path = {}
        self.dict_aufgaben_wizard = {}

        hashed_pw = read_credentials()
        self.developer_mode_active = False
        self.no_saved_changes_sage = True
        # self.worksheet_wizard_changed = True
        # if sys.platform.startswith("win"):
        # path_lama_developer_credentials = os.path.join(os.getenv('LOCALAPPDATA'), "LaMA", "credentials")
        # lama_developer_credentials = os.path.join(path_lama_developer_credentials, "developer_credentials.txt")

        if os.path.isfile(lama_developer_credentials):
            with open(lama_developer_credentials, "rb") as file:
                password = file.read()
            if bcrypt.checkpw(password, hashed_pw):
                self.developer_mode_active = True

        # elif sys.platform.startswith("darwin"):

        # self.developer_mode_active = False

        try:
            with open(lama_settings_file, "r", encoding="utf8") as f:
                self.lama_settings = json.load(f)
        except FileNotFoundError:
            self.lama_settings = {}

        try:
            self.display_mode = self.lama_settings["display"]
        except KeyError:
            self.lama_settings["display"] = 0
            self.display_mode = 0

        self.dict_titlepage = check_format_titlepage_save("titlepage_save")

        self.dict_titlepage_cria = check_format_titlepage_save("titlepage_save_cria")

        path_teildokument = os.path.join(path_programm, "Teildokument")
        if not os.path.isdir(path_teildokument):
            os.mkdir(path_teildokument)
        app.aboutToQuit.connect(self.close_app)

        

    # def resizeEvent(self, event: QtGui.QResizeEvent):
    #     self.resized.emit()
    #     return self.resizeEvent(event)
    #     # self.resized.emit()
    #     # return 

    # @report_exceptions
    def setupUi(self, MainWindow):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.check_for_update()
        QtWidgets.QApplication.restoreOverrideCursor()
        try:
            self.lama_settings["start_program"]
        except KeyError:
            self.lama_settings["start_program"] = 0
        if loaded_lama_file_path == "" and self.lama_settings["start_program"] == 0:
            ########## Dialog: Choose program ####

            self.Dialog = QtWidgets.QDialog(
                None,
                QtCore.Qt.WindowSystemMenuHint
                | QtCore.Qt.WindowTitleHint
                | QtCore.Qt.WindowCloseButtonHint,
            )
            self.ui = Ui_Dialog_choose_type()
            self.ui.setupUi(self.Dialog)

            bring_to_front(self.Dialog)

            self.Dialog.setFixedSize(self.Dialog.size())
            rsp = self.Dialog.exec_()

            if rsp == QtWidgets.QDialog.Accepted:
                self.chosen_program = self.ui.chosen_program
            if rsp == QtWidgets.QDialog.Rejected:
                sys.exit(0)
        elif loaded_lama_file_path != "":
            loaded_file = self.load_file(loaded_lama_file_path)
            try:
                self.chosen_program = loaded_file["data_gesamt"]["program"]

            except KeyError:
                warning_window(
                    "Die geöffnete *.lama-Datei ist veraltet und kann nur mit der Version LaMA 1.x geöffnet werden.",
                    "Bitte laden Sie eine aktuelle *.lama-Datei oder kontaktieren Sie lama.helpme@gmail.com, wenn Sie Hilfe benötigen.",
                )
                return
        elif self.lama_settings["start_program"] == 1:
            self.chosen_program = "cria"
        elif self.lama_settings["start_program"] == 2:
            self.chosen_program = "lama"
        elif self.lama_settings["start_program"] == 3:
            self.chosen_program = "wizard"

        try:
            self.lama_settings["database"]
        except KeyError:
            self.lama_settings["database"] = 2

        if self.lama_settings["database"] == 0:
            refresh_ddb(self, True)

        else:
            database_file = os.path.join(database, ".git", "index")
            refresh_date_ddb= modification_date(database_file).strftime("%Y%m%d")
            refresh_date_ddb_month = modification_date(database_file).strftime("%m")
            today = datetime.datetime.today().strftime("%Y%m%d")
            today_month = datetime.datetime.today().strftime("%m")

            difference = int(today) - int(refresh_date_ddb)

            if (self.lama_settings["database"] == 1 and difference != 0) or (self.lama_settings["database"] == 2 and difference > 6) or (self.lama_settings["database"] == 3 and refresh_date_ddb_month != today_month):
                refresh_ddb(self, auto_update=True)

        try:
            self.lama_settings["popup_off"]
        except KeyError:
            self.lama_settings["popup_off"] = False


        if self.lama_settings["popup_off"] == False and show_popup==True:
            rsp = self.show_popup_window()
            if rsp == True:
                self.lama_settings["popup_off"] = True

                with open(lama_settings_file, "w+", encoding="utf8") as f:
                    json.dump(self.lama_settings, f, ensure_ascii=False)


        if self.chosen_program == 'wizard':
           self.chosen_gui = "widgets_wizard" 
        else:
            self.chosen_gui = "widgets_search"
        try:
            self.chosen_program
        except AttributeError:
            self.chosen_program = "lama"

        if self.chosen_program == "cria":
            self.chosen_gui = self.chosen_gui + "_cria"


        ########################
        self.MainWindow = MainWindow
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)

        if self.chosen_program == "lama":
            MainWindow.setWindowTitle("LaMA - LaTeX Mathematik Assistent (Oberstufe)")
            MainWindow.setWindowIcon(QtGui.QIcon(logo_path))

        elif self.chosen_program == "cria":
            MainWindow.setWindowTitle("LaMA Cria - LaTeX Mathematik Assistent (Unterstufe)")
            MainWindow.setWindowIcon(QtGui.QIcon(logo_cria_path))

        elif self.chosen_program == "wizard":
            MainWindow.setWindowTitle("LaMA Worksheet Wizard")
            MainWindow.setWindowIcon(QtGui.QIcon(logo_path))



        self.stackMainWindow =  QtWidgets.QStackedWidget(MainWindow)
        self.stackMainWindow.setMinimumSize(1,1)
        self.stackSearch = QtWidgets.QWidget(MainWindow)
        self.stackSage = QtWidgets.QWidget(MainWindow)
        self.stackCreator = QtWidgets.QWidget(MainWindow)
        self.stackFeedback  = QtWidgets.QWidget(MainWindow)
        self.stackWizard = QtWidgets.QWidget(MainWindow)



        self.stackMainWindow.addWidget(self.stackSearch)
        self.stackMainWindow.addWidget(self.stackSage)
        self.stackMainWindow.addWidget(self.stackCreator)
        self.stackMainWindow.addWidget(self.stackFeedback)
        self.stackMainWindow.addWidget(self.stackWizard)

        # self.centralwidget = QtWidgets.QWidget(MainWindow)
        # self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        # self.centralwidget.hide()
        # self.gridLayout = create_new_gridlayout(self.centralwidget)


        self.MainWindow.resize(900,700)
        #######################################################
        ############ Menu Bar ###################
        #######################################################

        setup_MenuBar(self)


        if self.chosen_program == "cria":
            self.action_cria.setVisible(False)
        elif self.chosen_program == "lama":
            self.action_lama.setVisible(False)
        elif self.chosen_program == "wizard":
            self.action_wizard.setVisible(False)

        self.update_label_restore_action()

        if show_popup == False:
            self.actionShowPopupWindow.setEnabled(False)


        ###########################################################################
        ##########################################################################

        #######################################################
        ############ Stack Search ###################
        #######################################################

        setup_stackSearch(self)
        


        #### Warnung ### Hinweis ####
        # self.label_warnung = QtWidgets.QLabel(self.centralwidget)
        # self.label_warnung.setWordWrap(True)
        # self.label_warnung.setObjectName(_fromUtf8("label_warnung"))
        # color = get_color(red)
        # self.label_warnung.setStyleSheet(
        #     _fromUtf8("border: 2px solid {};".format(color))
        # )  # background-color: rgb(195, 58, 63)
        # # self.label_warnung.setMaximumSize(QtCore.QSize(375, 16777215))
        # self.label_warnung.setText(
        #     _translate(
        #         "MainWindow",
        #         "Achtung: Aufgrund neuer hilfreicher Befehle ist es notwendig, ein Update des srdp-mathematik-Pakets so bald wie möglich durchzuführen! Nähere Infos unter: lama.schule/update",
        #         None,
        #     )
        # )
        # self.gridLayout.addWidget(self.label_warnung, 6, 0, 1, 1)
        # self.label_warnung.hide()
        #########################

        #######################################################
        ############ Stack Sage ###################
        #######################################################

        setup_stackSage(self)

       
        #######################################################
        ############ Stack Creator & Stack Editor ###################
        #######################################################

        setup_stackCreator(self)


        #######################################################
        ############ Stack Feedback ###################
        #######################################################

        setup_stackFeedback(self)


        ####################################################
        ######################################################
        ################## WORKSHEET WIZARD ####################
        ######################################################
        ######################################################

        setup_stackWizard(self)


        ####################################################################
        #####################################################################
        ######################################################################
        #####################################################################



        MainWindow.setCentralWidget(self.stackMainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        if self.chosen_program == "wizard":
            self.update_gui("widgets_wizard")
        else:
            self.update_gui("widgets_search")
        

        if loaded_lama_file_path != "":
            self.sage_load(external_file_loaded=True)


    def show_popup_window(self, show_checkbox = True):
        rsp = custom_window("""
<b>Die neue Version von LaMA ({}) verwendet Befehle des aktuellsten "srdp-mathematik"-Pakets. Um die volle Funktionsfähigkeit von LaMA zu gewährleisten, sollte das LaTeX-Paket auf Ihrem Gerät manuell aktualisiert werden.</b><br><br><br>

Eine direkte Aktualisierung des "srdp-mathematik"-Pakets über LaMA kann via<br>

<i>"Optionen -> Update ... -> srdp-mathematik.sty aktualisieren"</i><br>

durchgeführt werden.<br><br>

Sollte dies nicht möglich sein, melden Sie sich bitte unter: lama.helpme@gmail.com<br>
""".format(__version__),
        titel="Update Information",
        show_checkbox=show_checkbox,
        set_width=600,
        )
        return rsp
#         msg = QtWidgets.QMessageBox()
#         msg.setWindowTitle("Update")
#         pixmap = QtGui.QPixmap(logo_path)
#         msg.setIconPixmap(pixmap)
#         msg.setWindowIcon(QtGui.QIcon(logo_path))
#         msg.setText("""Die neue Version von LaMA ({}) verwendet Befehle des aktuellsten "srdp-mathematik"-Pakets. Um die volle Funktionsfähigkeit von LaMA zu gewährleisten, sollte das LaTeX-Paket auf Ihrem Gerät manuell aktualisiert werden.""".format(__version__))
#         msg.setInformativeText("""Eine direkte Aktualisierung des "srdp-mathematik"-Pakets über LaMA kann via

# "Optionen -> Update ... -> srdp-mathematik.sty aktualisieren"

# durchgeführt werden. 

# Sollte dies nicht möglich sein, melden Sie sich bitte unter:
# lama.helpme@gmail.com""")
        
#         cb = QtWidgets.QCheckBox()
#         if show_checkbox==True:
#             msg.setCheckBox(cb)
#             cb.setText("Diese Meldung nicht mehr anzeigen")
#         msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

#         msg.exec_()
#         return cb.isChecked()

    def get_saving_path(self):
        dict_umlaute = {
            "Ä": "AE",
            "ä": "ae",
            "Ö": "OE",
            "ö": "oe",
            "Ü": "ue",
            "ü": "ue",
            "ß": "ss",
        }
        self.chosen_path_schularbeit_erstellen = (
            QtWidgets.QFileDialog.getSaveFileName(
                None,
                "Speicherort wählen",
                os.path.dirname(self.saved_file_path),
                "TeX Dateien (*.tex);; Alle Dateien (*.*)",
            )
        )

        if self.chosen_path_schularbeit_erstellen[0] == "":
            QtWidgets.QApplication.restoreOverrideCursor()
            return
        self.saved_file_path = self.chosen_path_schularbeit_erstellen[0]

        dirname = os.path.dirname(self.chosen_path_schularbeit_erstellen[0])
        filename = os.path.basename(self.chosen_path_schularbeit_erstellen[0])
        if sys.platform.startswith("linux"):
            filename = filename + ".tex"

        for character in dict_umlaute.keys():
            if character in filename:
                filename = filename.replace(character, dict_umlaute[character])
        filename_vorschau = os.path.join(dirname, filename)


        
        return filename_vorschau

    @report_exceptions
    def open_dialogwindow_erstellen(
        self,
        dict_titlepage,
    ):
        self.Dialog = QtWidgets.QDialog(
            None,
            QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint,
        )

        self.ui_erstellen = Ui_Dialog_erstellen()
        self.ui_erstellen.setupUi(
            self.Dialog,
            self,
            self.dict_all_infos_for_file,
            dict_titlepage,
            self.saved_file_path,
            self.comboBox_pruefungstyp.currentText(),
        )
        rsp = self.Dialog.exec_()

        if rsp == QtWidgets.QDialog.Accepted:
            single_file_index = self.ui_erstellen.single_file_index

            if self.ui_erstellen.pdf == False:
                range_limit = 1
            elif single_file_index != None:
                range_limit = 2
            else:
                range_limit = (
                    self.ui_erstellen.spinBox_sw_gruppen.value() * 2
                )  # +1 to reset tex-file to random=0


            filename_vorschau = self.get_saving_path()
            if filename_vorschau == None:
                return

           
            self.collect_all_infos_for_creating_file()

            if self.ui_erstellen.lama == True:
                self.sage_save(path_create_tex_file=filename_vorschau)


            if (
                is_empty(self.list_copy_images) #self.dict_all_infos_for_file["data_gesamt"]["copy_images"]
                == False
            ):
                for image in self.list_copy_images:
                    copy_included_images(self, image)

            for index in range(range_limit):
                single_file_index = self.pushButton_vorschau_pressed(
                    "schularbeit",
                    index,
                    self.ui_erstellen.spinBox_sw_gruppen.value() * 2,
                    self.ui_erstellen.pdf,
                    self.ui_erstellen.show_pagenumber,
                    single_file_index,
                    filename_vorschau = filename_vorschau,
                )

            if not is_empty(self.chosen_path_schularbeit_erstellen[0]):
                if sys.platform.startswith("linux"):
                    file_path = os.path.dirname(self.saved_file_path)
                    subprocess.Popen('xdg-open "{}"'.format(file_path), shell=True)
                elif sys.platform.startswith("darwin"):
                    file_path = os.path.dirname(self.saved_file_path)
                    subprocess.Popen('open "{}"'.format(file_path), shell=True)
                else:
                    file_path = os.path.dirname(self.saved_file_path).replace("/", "\\")
                    subprocess.Popen('explorer "{}"'.format(file_path))

    @report_exceptions
    def check_admin_entry(self):
        if (self.chosen_gui == "widgets_edit" or self.chosen_gui == "widgets_create") and self.developer_mode_active == True:
            self.cb_matura_tag.show()
            self.cb_no_grade_tag.hide()
            self.cb_no_grade_tag.setChecked(False)
        elif (self.chosen_gui == "widgets_edit_cria" or self.chosen_gui == "widgets_create_cria") and self.developer_mode_active == True:
            self.cb_matura_tag.hide()
            self.cb_matura_tag.setChecked(False)
            self.cb_no_grade_tag.show()
        else:
            self.cb_matura_tag.hide()
            self.cb_matura_tag.setChecked(False)
            self.cb_no_grade_tag.hide()
            # self.cb_no_grade_tag.setChecked(False)


    def click_label_to_check(self, new_checkbox):
        if new_checkbox.isChecked() == False:
            new_checkbox.setChecked(True)
        else:
            new_checkbox.setChecked(False)

    def create_checkboxes_themen(self, parent, layout, mode):
        if mode == "creator":
            name_start = "checkbox_creator_themen_"
            # name_start = "checkbox_creator_themen_{}_".format(klasse)
        if mode == "search":
            name_start = "checkbox_search_themen_"
            # name_start = "checkbox_search_themen_{}_".format(klasse)

        # dict_klasse = eval("{}_beschreibung".format(klasse))
        dict_klasse = zusatzthemen_beschreibung
        row = 0

        for thema in dict_klasse:
            new_checkbox = create_new_checkbox(parent, dict_klasse[thema])
            new_checkbox.stateChanged.connect(
                partial(self.checkbox_checked, mode, "themen")
            )
            # new_checkbox.setSizePolicy(SizePolicy_fixed)
            name = name_start + thema
            self.dict_widget_variables[name] = new_checkbox
            layout.addWidget(new_checkbox, row)

            # new_label = create_new_label(parent, dict_klasse[thema], True, True)
            # new_label.clicked.connect(partial(self.click_label_to_check, new_checkbox))
            # layout.addWidget(new_label, row)

            row += 1

        return row

    @report_exceptions
    def create_tab_checkboxes_themen(self, tab_widget, mode):
        # new_tab = add_new_tab(
        #     tab_widget, "{}. Klasse".format(klasse[1])
        # )  # self.tab_widget_gk self.tab_widget_gk_cr
        new_tab = add_new_tab(tab_widget, "Zusatzthemen")
        # new_tab.setStyleSheet(StyleSheet_new_tab)
        # if self.display_mode == 0:
        #     stylesheet = StyleSheet_new_tab
        # else:
        #     stylesheet = StyleSheet_new_tab_dark_mode
        # new_tab.setStyleSheet(stylesheet)

        verticalLayout = create_new_verticallayout(new_tab)
        verticalLayout.setContentsMargins(0,0,0,0)
        scrollarea = QtWidgets.QScrollArea(new_tab)
        scrollarea.setWidgetResizable(True)
        scrollarea.setObjectName("{}".format(scrollarea))

        scrollareacontent = QtWidgets.QWidget()
        scrollareacontent.setGeometry(QtCore.QRect(0, 0, 641, 252))
        scrollareacontent.setObjectName("{}".format(scrollareacontent))

        # gridlayout_scrollarea = create_new_gridlayout(scrollareacontent)
        verticalLayout_scrollarea = create_new_verticallayout(scrollareacontent)

        row = self.create_checkboxes_themen(
            scrollareacontent, verticalLayout_scrollarea, mode
        )

        if mode == "search":
            # dict_klasse = eval("{}_beschreibung".format(klasse))
            dict_klasse = zusatzthemen_beschreibung
            button_check_all = create_new_button(
                scrollareacontent,
                "alle auswählen",
                partial(
                    self.button_all_checkboxes_pressed,
                    dict_klasse,
                    "themen",
                    mode,
                    klasse,
                ),
            )
            # if self.display_mode == 0:
            #     stylesheet = StyleSheet_button_check_all
            # else:
            #     stylesheet = StyleSheet_button_check_all_dark_mode
            # button_check_all.setStyleSheet(stylesheet)
            button_check_all.setSizePolicy(SizePolicy_fixed)


        verticalLayout_scrollarea.addStretch()
        # gridlayout_scrollarea.setRowStretch(row, 1)

        if mode == "search":
            verticalLayout_scrollarea.addWidget(button_check_all, row + 1, QtCore.Qt.AlignRight)

        scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
        scrollarea.setWidget(scrollareacontent)
        verticalLayout.addWidget(scrollarea)

    def create_tab_checkboxes_gk(self, tab_widget, titel, chosen_dictionary, mode):
        new_tab = add_new_tab(
            tab_widget, titel
        ) 
        
        # new_tab.setStyleSheet(StyleSheet_new_tab)
        # self.tab_widget_gk self.tab_widget_gk_cr
        # if self.display_mode == 0:
        #     stylesheet = StyleSheet_new_tab
        # else:
        #     stylesheet = StyleSheet_new_tab_dark_mode
        # new_tab.setStyleSheet(stylesheet)

        gridlayout = create_new_gridlayout(new_tab)
        gridlayout.setContentsMargins(0,0,0,0)
        scrollarea = QtWidgets.QScrollArea(new_tab)
        scrollarea.setWidgetResizable(True)
        scrollarea.setObjectName("{}".format(scrollarea))

        scrollareacontent = QtWidgets.QWidget(scrollarea)
        scrollareacontent.setGeometry(QtCore.QRect(0, 0, 641, 252))
        scrollareacontent.setObjectName("{}".format(scrollareacontent))
        gridLayout_scrollarea = create_new_gridlayout(scrollareacontent)

        row, column = self.create_list_of_all_gk_checkboxes(
            scrollareacontent, gridLayout_scrollarea, mode, chosen_dictionary
        )
        # gridLayout_scrollarea.setRowStretch(row, 10)

        if mode == "search" or mode == "quiz":
            button_check_all = create_new_button(
                scrollarea,
                "alle auswählen",
                partial(
                    self.button_all_checkboxes_pressed, chosen_dictionary, "gk", mode
                ),
            )
            # if self.display_mode == 0:
            #     stylesheet = StyleSheet_button_check_all
            # else:
            #     stylesheet = StyleSheet_button_check_all_dark_mode
            # button_check_all.setStyleSheet(stylesheet)
            button_check_all.setSizePolicy(SizePolicy_fixed)

            gridLayout_scrollarea.addWidget(
                button_check_all, 10, column, 1, 1, QtCore.Qt.AlignRight
            )

        scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
        scrollarea.setWidget(scrollareacontent)
        gridlayout.addWidget(scrollarea, 1, 0, 7, 1)

    def create_list_of_all_gk_checkboxes(self, parent, layout, mode, chosen_dictionary):
        row = 0
        column = 0
        if mode == "creator":
            max_row = 10
            name_start = "checkbox_creator_gk_"
        if mode == "search":
            max_row = 9
            name_start = "checkbox_search_gk_"
        if mode == "quiz":
            max_row = 9
            name_start = "checkbox_quiz_gk_"
        for all in chosen_dictionary:
            new_checkbox = create_new_checkbox(parent, dict_gk[all])
            new_checkbox.setFocusPolicy(QtCore.Qt.NoFocus)
            # background_color = get_color(s)
            # if self.display_mode == 0:
            #     stylesheet = StyleSheet_new_checkbox
            # else:
            #     stylesheet = StyleSheet_new_checkbox_dark_mode
            # new_checkbox.setStyleSheet(stylesheet)
            layout.addWidget(new_checkbox, row, column, 1, 1)
            new_checkbox.stateChanged.connect(
                partial(self.checkbox_checked, mode, "gk")
            )
            name = name_start + all
            self.dict_widget_variables[name] = new_checkbox

            if row > max_row:
                row +=1
                layout.setRowStretch(row,1)
                row = 0
                column += 1
            else:
                row += 1

        layout.setColumnStretch(column, 1)
        

        return row, column

    #######################
    #### Check for Updates
    ##########################
    @report_exceptions
    def check_for_update(self):
        try:
            link = (
                "https://github.com/chrisiweb/lama_latest_update/blob/master/README.md"
            )

            # r = requests.post('https://httpbin.org/post', data = {'key':'value'})
            # f = urlopen(link)
            # url_readme_version = f.read().decode("utf-8")
            readme_content = requests.get(link)
            latest_version = re.search(
                "Aktuelle Version: \[(.+)\]", readme_content.text
            ).group(1)
            if __version__ == latest_version:
                return
        except Exception as e:
            print(
                "Fehler beim Überprüfen der Version. Überprüfung wird übersprungen ..."
            )
            return

        if sys.platform.startswith("linux"):
            information_window(
                "Es ist ein neues Update verfügbar.",
                "Es wird empfohlen die neueste Version von LaMA unter lama.schule/downloads herunterzuladen und damit die alte Version zu ersetzen.",
                titel="Neue Version verfügbar",
            )
            return
        else:
            QtWidgets.QApplication.restoreOverrideCursor()
            ret = question_window(
                "Es ist eine neue Version von LaMA verfügbar.",
                "Möchten Sie das neue Update jetzt installieren?",
                "Neue Version verfügbar",
            )
            QtWidgets.QApplication.setOverrideCursor(
                QtGui.QCursor(QtCore.Qt.WaitCursor)
            )

            if ret == True:
                self.lama_settings["popup_off"] = False
                with open(lama_settings_file, "w+", encoding="utf8") as f:
                    json.dump(self.lama_settings, f, ensure_ascii=False)

                if sys.platform.startswith("darwin"):
                    refresh_ddb(self, auto_update='mac')
                    opened_file = os.path.basename(sys.argv[0])
                    name, extension = os.path.splitext(opened_file)

                    filename_update = os.path.join(
                        path_programm,
                        "_database",
                        "_config",
                        "update",
                        "update_mac",
                        "update%s" % extension,
                    )
                    try:
                        if extension == ".py":
                            os.system("python3 {}".format(filename_update))
                        else:
                            os.system("chmod 777 {}".format(filename_update))
                            os.system(filename_update)
                        sys.exit(0)
                    except Exception as e:
                        warning_window(
                            'Das neue Update von LaMA konnte leider nicht installiert werden! Bitte versuchen Sie es später erneut oder melden Sie den Fehler unter dem Abschnitt "Feedback & Fehler".',
                            'Fehler:\n"{}"'.format(e),
                        )
                else:
                    refresh_ddb(self, auto_update=True)
                    text = "Neue Version von LaMA wird heruntergeladen ..."
                    path_installer = os.path.join(
                        path_home, "Downloads", "LaMA_setup.exe"
                    )

                    Dialog_checkchanges = QtWidgets.QDialog()
                    ui = Ui_Dialog_processing()
                    ui.setupUi(Dialog_checkchanges, text)

                    thread = QtCore.QThread(Dialog_checkchanges)
                    worker = Worker_UpdateLaMA()
                    worker.finished.connect(Dialog_checkchanges.close)
                    worker.moveToThread(thread)
                    thread.started.connect(partial(worker.task, path_installer))
                    thread.start()
                    thread.exit()
                    Dialog_checkchanges.exec()

                    if worker.response == False:
                        critical_window(
                            "LaMA konnte nicht heruntergeladen werden. Bitte überprüfen Sie die Internetverbindung und versuchen Sie es später erneut."
                        )
                        return
                    elif worker.response == True:
                        os.startfile('"' + path_installer + '"')
                        sys.exit(0)
        QtWidgets.QApplication.restoreOverrideCursor()


    def create_Tooltip(self, chosen_dict):
        for all in chosen_dict:
            name = "checkbox_search_gk_" + all
            self.dict_widget_variables[name].setToolTip(chosen_dict[all])
        for all in chosen_dict:
            name = "checkbox_creator_gk_" + all
            self.dict_widget_variables[name].setToolTip(chosen_dict[all])




    @report_exceptions
    def btn_alle_kapitel_clicked_cria(self, klasse):
        dict_klasse = eval("dict_{}".format(klasse))
        comboBox = self.dict_widget_variables[f"combobox_kapitel_search_cria_{klasse}"]
        text_combobox = comboBox.currentText()
        # kapitel = text_combobox[text_combobox.find("(") + 1 : text_combobox.find(")")]
        first_kapitel = text_combobox[text_combobox.find("(") + 1 : text_combobox.find(")")]
        first_unterkapitel = dict_klasse[first_kapitel][0]
        first_checkbox = self.dict_widget_variables[f"checkbox_unterkapitel_{klasse}_{first_kapitel}_{first_unterkapitel}"]

        if first_checkbox.isChecked():
            setchecked = False
        else:
            setchecked = True

        for i in range(0,self.dict_widget_variables[f"combobox_kapitel_search_cria_{klasse}"].count()):
            comboBox.setCurrentIndex(i)
            text_combobox = comboBox.currentText()
            kapitel = text_combobox[text_combobox.find("(") + 1 : text_combobox.find(")")]
            for unterkapitel in dict_klasse[kapitel]:
                # print(unterkapitel)
                checkbox = self.dict_widget_variables[f"checkbox_unterkapitel_{klasse}_{kapitel}_{unterkapitel}"]
                checkbox.setChecked(setchecked)

        comboBox.setCurrentIndex(0)
 
    @report_exceptions
    def btn_alle_unterkapitel_clicked_cria(self, klasse):
        dict_klasse = eval("dict_{}".format(klasse))
        comboBox = self.dict_widget_variables[f"combobox_kapitel_search_cria_{klasse}"]
        text_combobox = comboBox.currentText()
        # kapitel = text_combobox[text_combobox.find("(") + 1 : text_combobox.find(")")]
        kapitel = text_combobox[text_combobox.find("(") + 1 : text_combobox.find(")")]
        first_unterkapitel = dict_klasse[kapitel][0]
        first_checkbox = self.dict_widget_variables[f"checkbox_unterkapitel_{klasse}_{kapitel}_{first_unterkapitel}"]

        if first_checkbox.isChecked():
            setchecked = False
        else:
            setchecked = True

        for unterkapitel in dict_klasse[kapitel]:
            checkbox = self.dict_widget_variables[f"checkbox_unterkapitel_{klasse}_{kapitel}_{unterkapitel}"]
            checkbox.setChecked(setchecked)

        

        # dict_klasse = eval("dict_{}".format(klasse))

        # first_checkbox = "checkbox_unterkapitel_{0}_{1}_{2}".format(
        #     klasse, kapitel, dict_klasse[kapitel][0]
        # )

        # if self.dict_widget_variables[first_checkbox].isChecked() == False:
        #     check_checkboxes = True
        # else:
        #     check_checkboxes = False

        # for all in self.dict_widget_variables:
        #     if all.startswith("checkbox_unterkapitel_{0}_{1}_".format(klasse, kapitel)):
        #         self.dict_widget_variables[all].setChecked(check_checkboxes)


    def checkBox_checked_cria(self, klasse, kapitel, unterkapitel):
        thema_checked = [klasse, kapitel, unterkapitel]
        thema_label = kapitel + "." + unterkapitel + " (" + klasse[1] + ".)"

        label_checkbox = "checkbox_unterkapitel_{0}_{1}_{2}".format(
            klasse, kapitel, unterkapitel
        )

        checkbox = self.dict_widget_variables[label_checkbox]

        if checkbox.isChecked() == True:
            if thema_label not in self.dict_chosen_topics.keys():
                self.dict_chosen_topics[thema_label] = thema_checked
        if checkbox.isChecked() == False:
            if thema_label in self.dict_chosen_topics:
                del self.dict_chosen_topics[thema_label]

        x = ", ".join(self.dict_chosen_topics.keys())

        self.label_ausgew_gk.setText(_translate("MainWindow", x, None))


    @report_exceptions
    def comboBox_kapitel_changed_cr(
        self, parent, layout, klasse,typ ,checked=False # prevent error decorator
    ):  # , verticalLayout_cr_cria, combobox_kapitel, klasse, spacerItem_unterkapitel_cria
        # layout.removeItem(self.spacerItem_unterkapitel_creator_cria)

        if typ == 'search':
            widget_string_kapitel = 'combobox_kapitel_search_cria'
            widget_string_unterkapitel = 'checkbox_unterkapitel'
        elif typ == 'creator':
            widget_string_kapitel = 'combobox_kapitel_creator_cria'
            widget_string_unterkapitel = 'checkbox_unterkapitel_creator'
        # self.delete_all_widgets(layout, 1) ### PROBLEM !!!
        for i in range(1, layout.count()):
            try:
                layout.itemAt(i).widget().hide()
                # layout.itemAt(i).widget().setParent(None)
            except AttributeError:
                pass

            
        text_combobox = self.dict_widget_variables[
            "{0}_{1}".format(widget_string_kapitel, klasse)
        ].currentText()

        kapitel = text_combobox[text_combobox.find("(") + 1 : text_combobox.find(")")]

        dict_klasse = eval("dict_{}".format(klasse))

        for unterkapitel in dict_klasse[kapitel]:
            if (
                "{0}_{1}_{2}_{3}".format(
                    widget_string_unterkapitel,klasse, kapitel, unterkapitel
                )
                in self.dict_widget_variables
            ):
                checkbox = self.dict_widget_variables[
                    "{0}_{1}_{2}_{3}".format(
                        widget_string_unterkapitel,klasse, kapitel, unterkapitel
                    )
                ]
                # layout.insertWidget(layout.count() - 1, checkbox)
                checkbox.show()
            else:
                new_checkbox = create_new_checkbox(
                    parent, dict_unterkapitel[unterkapitel] + " (" + unterkapitel + ")"
                )
                new_checkbox.setToolTip(dict_unterkapitel[unterkapitel])
                # if self.display_mode == 0:
                #     stylesheet = StyleSheet_new_checkbox
                # else:
                #     stylesheet = StyleSheet_new_checkbox_dark_mode
                # new_checkbox.setStyleSheet(stylesheet)
                if typ== 'search':
                    new_checkbox.stateChanged.connect(
                        partial(
                            self.checkBox_checked_cria,
                            klasse,
                            kapitel,
                            unterkapitel))
                elif typ == "creator":
                    new_checkbox.stateChanged.connect(
                        partial(
                            self.checkbox_unterkapitel_checked_cria,
                            new_checkbox,
                            klasse,
                            kapitel,
                            unterkapitel,
                        )
                    )
                self.dict_widget_variables[
                    "{0}_{1}_{2}_{3}".format(
                        widget_string_unterkapitel,klasse, kapitel, unterkapitel
                    )
                ] = new_checkbox

                new_checkbox.setFocusPolicy(QtCore.Qt.NoFocus)
                if typ == "search":
                    layout.insertWidget(layout.count() - 3, new_checkbox)
                else:
                    layout.insertWidget(layout.count() - 1, new_checkbox)



        if typ == "search":
            self.dict_widget_variables[f"btn_alle_unterkapitel_{klasse}"].show()
            self.dict_widget_variables[f"btn_alle_kapitel_{klasse}"].show()
        # layout.insertWidget(layout.count() - 1, self.dict_widget_variables[f"btn_alle_kapitel_{klasse}"])
        # layout.addStretch()
        # layout.addItem(self.spacerItem_unterkapitel_creator_cria)

    def checkbox_unterkapitel_checked_cria(
        self, checkbox, klasse, kapitel, unterkapitel,
    ):
        thema_checked = [klasse, kapitel, unterkapitel]

        if checkbox.isChecked():
            if thema_checked not in self.list_selected_topics_creator:
                self.list_selected_topics_creator.append(thema_checked)
        if checkbox.isChecked() == False:
            self.list_selected_topics_creator.remove(thema_checked)

        list_labels = []
        for all in self.list_selected_topics_creator:
            thema_label = all[1] + "." + all[2] + " (" + all[0][1] + ".)"
            list_labels.append(thema_label)
        x = ", ".join(list_labels)
        self.label_ausgew_gk_creator.setText(_translate("MainWindow", x, None))

    def uncheck_all_checkboxes(self, typ):
        name = "checkbox_search_{}_".format(typ)
        name_creator = "checkbox_creator_{}_".format(typ)

        for all in self.dict_widget_variables:
            if all.startswith(name) or all.startswith(name_creator):
                self.dict_widget_variables[all].setChecked(False)

    def uncheck_all_af_checkboxes(self):
        self.cb_af_rf.setChecked(False)
        self.cb_af_ko.setChecked(False)
        self.cb_af_lt.setChecked(False)
        self.cb_af_mc.setChecked(False)
        self.cb_af_oa.setChecked(False)
        self.cb_af_ta.setChecked(False)
        self.cb_af_zo.setChecked(False)

    def uncheck_all_klassen_checkboxes(self):
        self.cb_k5.setChecked(False)
        self.cb_k6.setChecked(False)
        self.cb_k7.setChecked(False)
        self.cb_k8.setChecked(False)
        self.cb_mat.setChecked(False)
        self.cb_univie.setChecked(False)

    @report_exceptions
    def suchfenster_reset(self, variation=False):
        self.uncheck_all_checkboxes("gk")

        self.uncheck_all_checkboxes("themen")

        self.uncheck_all_af_checkboxes()
        self.uncheck_all_klassen_checkboxes()
        ### LaMA Cria
        # for klasse in list_klassen:
        #     self.dict_widget_variables['combobox_kapitel_creator_cria_{}'.format(klasse)].setCurrentIndex(0)
        # ## Problem with variation

        for all in self.dict_widget_variables:
            if all.startswith("checkbox_unterkapitel_"):
                self.dict_widget_variables[all].setChecked(False)

        for klasse in list_klassen:
            for all in self.dict_widget_variables:
                if all.startswith("radiobutton_kapitel_{}".format(klasse)):
                    self.dict_widget_variables[all].setChecked(True)
                    break

        # klasse = list_klassen[self.tabWidget_klassen_cria.currentIndex()]
        # dict_klasse = eval("dict_{}_name".format(klasse))
        # kapitel = list(dict_klasse.keys())[0]
        # self.chosen_radiobutton(klasse, kapitel)
        
        self.entry_suchbegriffe.setText("")
        self.cb_solution.setChecked(True)
        self.spinBox_punkte.setProperty("value", 1)
        self.comboBox_aufgabentyp_cr.setCurrentIndex(0)
        # self.comboBox_suchbegriffe.setCurrentIndex(0)
        self.comboBox_af.setCurrentIndex(0)
        self.comboBox_klassen_cr.setCurrentIndex(0)
        self.label_ausgew_gk_creator.setText(_translate("MainWindow", "", None))
        # self.label_bild_leer.show()

        self.chosen_variation = None
        # self.reset_variation()

        for image in list(self.dict_picture_path.keys())[:]:
            self.del_picture(image, question=False)    
        # for picture in list(self.dict_widget_variables.keys())[:]:
        #     if picture.startswith("label_bild_creator_"):
        #         self.del_picture(picture, question=False)


        self.lineEdit_titel.setText(_translate("MainWindow", "", None))

        if variation == False:
            self.plainTextEdit.setPlainText(_translate("MainWindow", "", None))

        if self.chosen_gui == "widgets_edit":
            self.enable_widgets_editor(False)
            self.button_choose_file.setText("Aufgabe suchen...")
            # "Aufgabe auswählen"
            self.plainTextEdit.clear()
            self.lineEdit_quelle.clear()
        else:
            self.enable_widgets_editor(True)
            try:
                quelle = self.lama_settings["quelle"]
            except KeyError:
                quelle = ""
            self.lineEdit_quelle.setText(_translate("MainWindow", quelle, None))

        self.cb_matura_tag.setChecked(False)
        self.cb_no_grade_tag.setChecked(False)

    @report_exceptions
    def reset_sage(self, question_reset=True):
        if question_reset == True and (not is_empty(self.list_alle_aufgaben_sage[0]) or not is_empty(self.list_alle_aufgaben_sage[1])):
            response = question_window(
                "Sind Sie sicher, dass Sie das Fenster zurücksetzen wollen und die erstellte Prüfung löschen möchten?",
                titel="Datei löschen?",
            )

            if response == False:
                return

        self.spinBox_nummer.setValue(1)
        self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.comboBox_pruefungstyp.setCurrentIndex(0)
        self.lineEdit_klasse_sage.setText("")
        self.spinBox_default_pkt.setValue(1)
        self.combobox_beurteilung.setCurrentIndex(0)
        # self.radioButton_notenschl.setChecked(True)
        self.spinBox_2.setProperty("value", 91)
        self.spinBox_3.setProperty("value", 80)
        self.spinBox_4.setProperty("value", 64)
        self.spinBox_5.setProperty("value", 50)
        try:
            if self.chosen_program == 'cria':
                key = "notenschluessel_cria"
            else:
                key = "notenschluessel"
            self.cb_ns_halbe_pkt.setChecked(self.lama_settings[key][0])
            self.cb_ns_prozent.setChecked(self.lama_settings[key][1])
        except KeyError:
            self.cb_ns_halbe_pkt.setChecked(False)
            self.cb_ns_prozent.setChecked(False)

        self.comboBox_at_sage.setCurrentIndex(0)
        self.comboBox_gk.setCurrentIndex(0)
        self.comboBox_gk_num.setCurrentIndex(0)
        self.comboBox_klassen.setCurrentIndex(0)
        self.comboBox_kapitel.setCurrentIndex(0)
        self.comboBox_unterkapitel.setCurrentIndex(0)
        self.lineEdit_number.setText("")
        self.dict_all_infos_for_file = {
            "list_alle_aufgaben": [],
            # "dict_ausgleichspunkte": {},
            "data_gesamt": {
                "#": self.spinBox_nummer.value(),
                "Pruefungstyp": self.comboBox_pruefungstyp.currentText(),
                "Datum": [
                    self.dateEdit.date().year(),
                    self.dateEdit.date().month(),
                    self.dateEdit.date().day(),
                ],  # .toPyDate()
                "Klasse": "",
                "Beurteilung": "ns",
                "Notenschluessel": [
                    self.spinBox_2.value(),
                    self.spinBox_3.value(),
                    self.spinBox_4.value(),
                    self.spinBox_5.value(),
                ],
                "Typ1 Standard": self.spinBox_default_pkt.value(),
                # "num_1": 0,
                # "punkte_1": 0,
                # "num_2": 0,
                # "punkte_2": 0,
                # "ausgleichspunkte": 0,
                # "copy_images": [],
            },
        }

        self.list_alle_aufgaben_sage = [[],[]]
        # self.dict_alle_aufgaben_sage = {}
        # self.dict_variablen_label = {}
        self.dict_variablen_punkte = {}
        self.dict_variablen_punkte_halb = {}
        self.dict_variablen_translation = {}
        self.dict_variablen_AB = {}
        self.dict_variablen_abstand = {}
        self.update_punkte()
        self.list_copy_images = []


        for i in reversed(range(self.verticalLayout_scrollArea_sage_typ1.count()+1)):
            self.delete_widget(self.verticalLayout_scrollArea_sage_typ1, i)
        for i in reversed(range(self.verticalLayout_scrollArea_sage_typ2.count()+1)):
            self.delete_widget(self.verticalLayout_scrollArea_sage_typ2, i)
        self.scrollAreaWidgetContents_typ2.hide()    

    @report_exceptions
    def change_program(self, program_change_to):
        if program_change_to == "cria":
            name = "LaMA Cria (Unterstufe)"

            program_name = "LaMA Cria - LaTeX Mathematik Assistent (Unterstufe)"
            icon = logo_cria_path

        elif program_change_to == "lama":
            name = "LaMA (Oberstufe)"
            program_name = "LaMA - LaTeX Mathematik Assistent (Oberstufe)"
            icon = logo_path

        elif program_change_to == "wizard":
            name = "LaMA - Worksheet Wizard"
            program_name = "LaMA - LaTeX Mathematik Assistent (Worksheet Wizard)"
            icon = logo_path

        # if self.chosen_program !='wizard':
        response = question_window(
            "Sind Sie sicher, dass sie zu {} wechseln wollen?\nDadurch werden alle bisherigen Einträge gelöscht!".format(
                name
            ),
            titel="Programm wechseln?",
        )

        if response == False:
            return False

        self.reset_sage(False)
        self.suchfenster_reset()
        self.reset_feedback()



        self.comboBox_pagebreak.setCurrentIndex(0)
        if program_change_to == "cria":
            self.chosen_program = "cria"

            # if self.beispieldaten_dateipfad_cria == None:
            #     self.beispieldaten_dateipfad_cria = self.define_beispieldaten_dateipfad(
            #         "cria"
            #     )

            # self.gridLayout.addWidget(self.groupBox_af, 3, 0, 1, 1)
            # self.gridLayout.addWidget(self.groupBox_punkte, 0, 1, 1, 1)
            # self.gridLayout.addWidget(self.groupBox_aufgabenformat, 0, 2, 1, 1)

            self.action_cria.setVisible(False)
            self.action_lama.setVisible(True)
            self.action_wizard.setVisible(True)

            # self.comboBox_pruefungstyp.removeItem(6)  # delete Quiz
            self.groupBox_af.show()
            self.cb_af_ko.show()
            self.cb_af_rf.show()
            self.cb_af_ta.show()

            # self.comboBox_at_fb.setItemText(0, _translate("MainWindow", "Aufgabenrückmeldung", None))
            # self.comboBox_at_fb.setItemText(1, _translate("MainWindow", "Allgemeine Rückmeldung", None))
            # self.comboBox_at_fb.removeItem(2)

            self.combobox_searchtype.setItemText(
                1,
                _translate(
                    "MainWindow",
                    "Alle Dateien ausgeben, die alle Themengebiete enthalten",
                    None,
                ),
            )
            i = 5
            for all in dict_aufgabenformate:
                if all == "rf" or all == "ta" or all == "ko":
                    add_new_option(self.comboBox_af, i, dict_aufgabenformate[all])
                    i += 1

            self.comboBox_klassen_changed("sage")

            self.label_gesamtbeispiele.setText(
                _translate("MainWindow", "Anzahl der Aufgaben: 0", None)
            )

            self.groupBox_ausgew_gk_cr.setTitle("Ausgewählte Themen")

            self.update_gui("widgets_search")
            self.combobox_beurteilung.removeItem(self.combobox_beurteilung.findText("Beurteilungsraster"))

            # self.beispieldaten_dateipfad_cria = self.define_beispieldaten_dateipfad(
            #     "cria"
            # )

        elif program_change_to == "lama":
            self.chosen_program = "lama"

            # self.gridLayout.addWidget(self.groupBox_af, 1, 1, 1, 1)
            # self.gridLayout.addWidget(self.groupBox_punkte, 0, 2, 1, 1)
            # self.gridLayout.addWidget(self.groupBox_aufgabenformat, 0, 3, 1, 1)

            self.action_cria.setVisible(True)
            self.action_lama.setVisible(False)
            self.action_wizard.setVisible(True)

            self.combobox_searchtype.setItemText(
                1,
                _translate(
                    "MainWindow",
                    "Alle Dateien ausgeben, die ausschließlich diese Themengebiete enthalten",
                    None,
                ),
            )

            # self.comboBox_pruefungstyp.addItem("Quiz")
            self.chosen_aufgabenformat_typ() # show AF when typ 1

            self.cb_af_ko.hide()
            self.cb_af_rf.hide()
            self.cb_af_ta.hide()
            self.comboBox_af.removeItem(7)
            self.comboBox_af.removeItem(6)
            self.comboBox_af.removeItem(5)

            self.label_gesamtbeispiele.setText(
                _translate(
                    "MainWindow", "Anzahl der Aufgaben: 0 (Typ1: 0 / Typ2: 0)", None
                )
            )

            # self.groupBox_ausgew_gk_cr.setTitle("Ausgewählte Grundkompetenzen")
            self.update_gui("widgets_search")
            self.combobox_beurteilung.insertItem(1,"Beurteilungsraster")
        elif program_change_to == 'wizard':
            self.chosen_program = "wizard"
            self.action_cria.setVisible(True)
            self.action_lama.setVisible(True)
            self.action_wizard.setVisible(False)
            self.update_gui("widgets_wizard") 

        self.MainWindow.setWindowTitle(program_name)
        self.MainWindow.setWindowIcon(QtGui.QIcon(icon))
        if self.lama_settings["database"] == 0:
            refresh_ddb(self)

        # self.beispieldaten_dateipfad_1 = self.define_beispieldaten_dateipfad(1)
        # self.beispieldaten_dateipfad_2 = self.define_beispieldaten_dateipfad(2)

    def exit_pressed(self):
        rsp = question_window("Sind Sie sicher, dass Sie LaMA schließen möchten?")
        if rsp == True:
            self.close_app()

    def close_app(self):
        if self.list_alle_aufgaben_sage ==  [[],[]]:
            sys.exit(0)

        if self.no_saved_changes_sage == True:
            sys.exit(0)
        # else:
        #     try:
        #         if os.path.isfile(self.saved_file_path) == True:
        #             path = self.saved_file_path
        #             loaded_file = self.load_file(path)
        #             if loaded_file == self.dict_all_infos_for_file:
        #                 sys.exit(0)
        #     except AttributeError:
        #         pass

        response = question_window(
            "Möchten Sie die Änderungen speichern?", titel="Änderungen speichern?"
        )

        if response == True:
            self.sage_save()
        else:
            sys.exit(0)

    def developer_mode_changed(self):
        if self.developer_mode_active == False:
            self.actionDeveloper.setText("Entwicklermodus")
            self.actionEdit_Files.setText("Lokal gespeicherte Aufgabe bearbeiten")
            # self.actionPush_Database.setVisible(False)
            self.menuBar.removeAction(self.menuDeveloper.menuAction())

        elif self.developer_mode_active == True:
            self.actionDeveloper.setText("Entwicklermodus (aktiv)")
            self.actionEdit_Files.setText("Aufgabe bearbeiten")
            # self.actionPush_Database.setVisible(True)
            self.menuBar.removeAction(self.menuHelp.menuAction())
            self.menuBar.addAction(self.menuDeveloper.menuAction())
            self.menuBar.addAction(self.menuHelp.menuAction())

    @report_exceptions
    def activate_developermode(self):
        if self.developer_mode_active == True:
            response = question_window(
                "Sind Sie sicher, dass Sie den Entwicklermodus deaktivieren möchten?"
            )
            if response == False:
                return

            if sys.platform.startswith("win"):
                path_lama_developer_credentials = os.path.join(
                    os.getenv("LOCALAPPDATA"), "LaMA", "credentials"
                )
            elif sys.platform.startswith("darwin"):
                path_lama_developer_credentials = os.path.join(
                    Path.home(), "Library", "LaMA", "credentials"
                )
            # elif sys.platform.startswith("linux"):
            #     path_lama_developer_credentials = os.path.join(Path.home(), "Library", "LaMA","credentials")

            lama_developer_credentials = os.path.join(
                path_lama_developer_credentials, "developer_credentials.txt"
            )
            if os.path.isfile(lama_developer_credentials):
                os.remove(lama_developer_credentials)
            self.developer_mode_active = False
            self.developer_mode_changed()
            information_window("Der Entwicklermodus wurde deaktiviert.")
        else:
            Dialog = QtWidgets.QDialog(
                None,
                QtCore.Qt.WindowSystemMenuHint
                | QtCore.Qt.WindowTitleHint
                | QtCore.Qt.WindowCloseButtonHint,
            )
            ui = Ui_Dialog_developer()
            ui.setupUi(Dialog)
            # self.Dialog.show()
            response = Dialog.exec()

            if response == 1:
                self.developer_mode_active = ui.developer_mode_active
                self.developer_mode_changed()
                information_window("Der Entwicklermodus wurde erfolgreich aktiviert.")
            # if response == 1:
            #     self.lama_settings = ui.lama_settings

    def open_setup(self):
        Dialog = QtWidgets.QDialog(
            None,
            QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint,
        )
        ui = Ui_Dialog_setup()
        ui.setupUi(Dialog, self)
        # self.Dialog.show()
        response = Dialog.exec()
        if response == 1:
            self.lama_settings = ui.lama_settings


    def show_gk_catalogue(self):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        file_path = os.path.join(path_programm, "_database", "_config", "gkkatalog.pdf")

        if os.path.isfile(file_path) == False:
            refresh_ddb(self, True)

        if sys.platform.startswith("linux"):
            os.system("xdg-open {0}".format(file_path))
        elif sys.platform.startswith("darwin"):
            subprocess.run(
                ["open", "{0}".format(file_path)]
            )

        else:
            subprocess.Popen(file_path, shell = True)        
        QtWidgets.QApplication.restoreOverrideCursor()

    
    def show_info(self):
        QtWidgets.QApplication.restoreOverrideCursor()
        if self.display_mode == 1:
            color = "rgb(88, 111, 124)"
        else:
            color = "rgb(47, 69, 80)"
        link = "https://mylama.github.io/lama/"
        custom_window("""
<h3>LaMA - LaTeX Mathematik Assistent {0}</h3><br>

<b>Authors:</b> Christoph Weberndorfer, Matthias Konzett<br><br>

<b>License:</b> GNU General Public License v3.0<br>
<b>Logo & Icon:</b> Lisa Schultz<br>
<b>Credits:</b> David Fischer<br>
<b>E-Mail-Adresse:</b> lama.helpme@gmail.com<br>
<b>Weiter Infos:</b> <a href='{1}'style="color:{2};">lama.schule</a>
""".format(__version__, link, color),
        titel="Über LaMA - LaTeX Mathematik Assistent",
        set_width=450,
        )


    def copy_style_package(self, package_name, path_new_package, possible_locations):
        for path in possible_locations:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file == package_name:
                        path_file = os.path.join(root, file)
                        try:
                            shutil.copy2(path_new_package, path_file)
                            return root
                        except PermissionError:
                            QtWidgets.QApplication.restoreOverrideCursor()
                            warning_window(
                                "Das Update konnte leider nicht durchgeführt werden, da notwendige Berechtigungen fehlen. Starten Sie LaMA erneut als Administrator (Rechtsklick -> 'Als Administrator ausführen') und versuchen Sie es erneut."
                            )
                            return
        return False

    def delete_style_package_in_teildokument(self, package_name):
        style_package_path = os.path.join(path_programm, "Teildokument", package_name)

        if os.path.isfile(style_package_path):
            os.remove(style_package_path)

    @report_exceptions
    def update_style_package(self):
        response = question_window(
            'Sind Sie sicher, dass Sie das Paket "{}" aktualisieren möchten?'.format(
                "srdp-mathematik.sty"
            )
        )

        if response == False:
            return

        path_new_srdpmathematik_package = os.path.join(
            path_programm, "_database", "_config", "srdp-mathematik.sty"
        )

        path_new_srdptables_package = os.path.join(
            path_programm, "_database", "_config", "srdp-tables.sty"
        )
        
        if os.path.isfile(path_new_srdpmathematik_package) == False or os.path.isfile(path_new_srdptables_package) == False:
            warning_window(
                'Das Paket "srdp-mathematik.sty" konnte nicht gefunden werden. Bitte versuchen Sie es später erneut.'
            )
            return

        # paket_teildokument = os.path.join(path_programm, "Teildokument", package_name)
        # if os.path.isfile(paket_teildokument):
        #     os.remove(paket_teildokument)

        # paket_teildokument = os.path.join(
        #     path_programm, "Teildokument", package_name
        # )
        # if os.path.isfile(paket_teildokument):
        #     os.remove(paket_teildokument)

        if sys.platform.startswith("darwin") or sys.platform.startswith("linux"):
            possible_locations = [os.path.join(path_home, "Library", "texmf")]
        else:
            possible_locations = [
                os.path.join(path_home, "AppData", "Roaming", "MiKTeX"),
                os.path.join(path_home, "AppData", "Local", "Programs", "MiKTeX"),
                os.path.join(path_home, "AppData"),
                os.path.join(os.environ["ProgramFiles"], "MiKTeX 2.9"),
                os.path.join(os.environ["ProgramFiles(x86)"], "MiKTeX 2.9"),
                os.path.join(os.environ["ProgramFiles"]),
                os.path.join(os.environ["ProgramFiles(x86)"]),
                # os.path.join(
                # "C:\Users\Christoph\AppData\Roaming\MiKTeX\2.9\tex\latex\srdp-mathematik\srdp-mathematik.sty
            ]

        # update_successfull=False
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))


        package_list = {
            "srdp-mathematik.sty" : path_new_srdpmathematik_package, 
            "srdp-tables.sty": path_new_srdptables_package,
            }


        for package in package_list:
            if package == "srdp-mathematik.sty":
                response = self.copy_style_package(
                    package, package_list[package], possible_locations
                )

                if response == False:
                    QtWidgets.QApplication.restoreOverrideCursor()
                    critical_window(
                        'Das Update von "srdp-mathematik.sty" konnte leider nicht durchgeführt werden. Aktualisieren Sie das Paket manuell oder wenden Sie sich an lama.helpme@gmail.com für Unterstützung.'
                        )
                    return
                elif response == None:
                    return
                else:
                    location_found = response
            
            else:
                #initexmf --update-fndb
                new_copy = False
                try:
                    for all in possible_locations:
                        if all in location_found:
                            index = possible_locations.index(all)

                    srdptables = os.path.join(location_found, package)
                    if sys.platform.startswith("win"):
                        if not os.path.isfile(srdptables):
                            new_copy = True        
                    shutil.copy2(package_list[package], location_found)
                    if new_copy == True:
                        if index == 3 or index == 4 or index == 5 or index == 6:
                            os.system("initexmf --admin --update-fndb")
                        else:
                            os.system("initexmf --update-fndb")
                except PermissionError:
                    QtWidgets.QApplication.restoreOverrideCursor()
                    warning_window(
                        "Das Update konnte leider nicht durchgeführt werden, da notwendige Berechtigungen fehlen. Starten Sie LaMA erneut als Administrator (Rechtsklick -> 'Als Administrator ausführen') und versuchen Sie es erneut."
                    )
                    
                    return
                
            
            
            self.delete_style_package_in_teildokument(package)

                
            
        QtWidgets.QApplication.restoreOverrideCursor()

        # if update_successfull == False:
        #     critical_window(
        #         'Das Update von "srdp-mathematik.sty" konnte leider nicht durchgeführt werden. Aktualisieren Sie das Paket manuell oder wenden Sie sich an lama.helpme@gmail.com für Unterstützung.'
        #         )
        #     return
        # if update_successfull == True:
        information_window(
            'Das Paket "srdp-mathematik.sty" wurde erfolgreich aktualisiert.'
        )
            # return

    def show_support(self):
        QtWidgets.QApplication.restoreOverrideCursor()
        link = "https://www.buymeacoffee.com/lama.schule"
        if self.display_mode == 1:
            color = "rgb(88, 111, 124)"
        else:
            color = "rgb(47, 69, 80)"
        custom_window("""
Eine kleinen Spende für unsere Kaffeekassa wird nicht benötigt, um LaMA zu finanzieren.<br><br>

<b>Unser Projekt ist und bleibt kostenlos und wir versuchen es auch weiterhin stetig zu verbessern und aktualisieren. Sie dient lediglich als kleine Anerkennung unserer Arbeit.</b><br>

<center><a href='{0}'style="color:{1};">Buy Me A Coffee</a><\center>

<h2> Vielen Dank!</h2>""".format(
                link, color
            ),
            # "LaMA ist gratis und soll es auch bleiben!\n",
            # "Wir freuen uns dennoch sehr über eine Unterstützung für die Weiterentwicklung von LaMA.\n\n"
            # """
            # Name: Matthias Konzett
            # IBAN: AT57 1921 0200 9941 7002
            # BLZ: 19210
            # """,
            titel="LaMA unterstützen",
            set_width=500
        )

    def chosen_aufgabenformat_typ(self):
        # chosen_type = self.label_aufgabentyp.text()[-1]
        chosen_type = self.combobox_aufgabentyp.currentIndex() + 1

        if chosen_type == 1:
            # self.label_aufgabentyp.setText(
            #     _translate("MainWindow", "Aufgabentyp: Typ 1", None)
            # )
            self.groupBox_af.show()
            self.combobox_searchtype.hide()
            # self.refresh_label_update()
        elif chosen_type == 2:
            # self.label_aufgabentyp.setText(
            #     _translate("MainWindow", "Aufgabentyp: Typ 2", None)
            # )
            self.groupBox_af.hide()
            self.combobox_searchtype.show()
            # self.refresh_label_update()

    @report_exceptions
    def combobox_translation_changed(self):
        index = self.combobox_translation.currentIndex()
        if index == 0:
            self.widget_translation.setToolTip("Alle Aufgaben in Deutsch anzeigen")
        elif index == 1:
            self.widget_translation.setToolTip("Aufgaben in Englisch anzeigen, falls vorhanden")
        elif index == 2:
            self.widget_translation.setToolTip("Nur englische Aufgaben anzeigen")

    @report_exceptions
    def button_all_checkboxes_pressed(self, chosen_dictionary, typ, mode, klasse=None):
        if mode == "quiz":
            name_start = "checkbox_quiz_{}_".format(typ)
        else:
            name_start = "checkbox_search_{}_".format(typ)
        # if typ == "themen":
        #     name_start = name_start + klasse + "_"
        first_element = name_start + list(chosen_dictionary.keys())[0]

        if self.dict_widget_variables[first_element].isChecked() == False:
            for all in chosen_dictionary:
                name = name_start + all
                self.dict_widget_variables[name].setChecked(True)
        else:
            for all in chosen_dictionary:
                name = name_start + all
                self.dict_widget_variables[name].setChecked(False)

    def checkbox_checked(self, mode, typ):
        chosen_gk = []
        chosen_themen = []
        self.list_selected_topics_creator = []
        # set_chosen_gk = set([])
        name_checkbox = "checkbox_{0}_".format(mode)

        for widget in self.dict_widget_variables:
            if widget.startswith(name_checkbox):
                if self.dict_widget_variables[widget].isChecked() == True:
                    if "gk" in widget:
                        gk = widget.split("_")[-1]
                        chosen_gk.append(dict_gk[gk])
                        if mode == "creator":
                            self.list_selected_topics_creator.append(dict_gk[gk])
                    elif "themen" in widget:
                        # klasse = widget.split("_")[-2]
                        thema = widget.split("_")[-1]
                        if mode == "creator":
                            self.list_selected_topics_creator.append(thema.upper())
                        # typ, klasse, thema = widget.split(name_checkbox)[1].split('_')
                        chosen_themen.append(thema.upper())

        x = ", ".join(chosen_gk)

        if len(chosen_themen) > 6:
            y = ", ".join(sorted(chosen_themen)[:6])
            y = y + ", ..."
        else:
            y = ", ".join(sorted(chosen_themen))

        if mode == "search":
            if len(chosen_themen) > 0:
                self.label_ausgew_gk_rest.show()
                y = "Weitere: " + y
                self.label_ausgew_gk_rest.setText(str(y))
            else:
                self.label_ausgew_gk_rest.hide()
            self.label_ausgew_gk.setText(str(x))
            
        if mode == "creator":
            if x == "":
                gesamt = y
            elif y == "":
                gesamt = x
            else:
                gesamt = x + ", " + y
            self.label_ausgew_gk_creator.setText(str(gesamt))

    def spinBox_nummer_changed(self):
        if self.comboBox_pruefungstyp.currentText() != "Übungsblatt" and self.comboBox_pruefungstyp.currentText() != "Benutzerdefiniert":
            self.spinBox_nummer_setvalue = self.spinBox_nummer.value()


    def comboBox_pruefungstyp_changed(self):
        self.comboBox_pruefungstyp.setEditable(False)
        self.widgetNummer.setEnabled(True)
        self.widget_datum.setEnabled(True)


        self.spinBox_nummer.setValue(self.spinBox_nummer_setvalue)


        if self.comboBox_pruefungstyp.currentText() == "Grundkompetenzcheck":
            self.combobox_beurteilung.setEnabled(False)
            self.groupBox_notenschl.setEnabled(False)
            self.groupBox_beurteilungsraster.setEnabled(False)
            self.groupBox_klasse_sage.setTitle("Klasse")
            self.pushButton_titlepage.setEnabled(False)
            self.comboBox_at_sage.setEnabled(True)
            self.pushButton_titlepage.setText("Titelblatt anpassen")
        elif self.comboBox_pruefungstyp.currentText() == "Übungsblatt":
            self.combobox_beurteilung.setEnabled(False)
            self.groupBox_notenschl.setEnabled(False)
            self.groupBox_beurteilungsraster.setEnabled(False)
            self.pushButton_titlepage.setEnabled(False)
            self.comboBox_at_sage.setEnabled(True)
            self.pushButton_titlepage.setText("Titelblatt anpassen")
            self.widget_datum.setEnabled(False)
            # self.groupBox_nummer.hide()
            self.widgetNummer.setEnabled(False)
            self.spinBox_nummer_setvalue = self.spinBox_nummer.value()
            self.spinBox_nummer.setValue(0)
            self.groupBox_klasse_sage.setTitle("Überschrift")
        else:
            self.combobox_beurteilung.setEnabled(True)
            self.groupBox_notenschl.setEnabled(True)
            self.groupBox_beurteilungsraster.setEnabled(True)
            self.pushButton_titlepage.setEnabled(True)
            self.comboBox_at_sage.setEnabled(True)
            self.pushButton_titlepage.setText("Titelblatt anpassen")
            self.groupBox_klasse_sage.setTitle("Klasse")
            if self.comboBox_pruefungstyp.currentText() == "Benutzerdefiniert":
                self.comboBox_pruefungstyp.setEditable(True)
                self.comboBox_pruefungstyp.lineEdit().selectAll()
                self.spinBox_nummer_setvalue = self.spinBox_nummer.value()
                self.spinBox_nummer.setValue(0)
                self.widgetNummer.setEnabled(False)
                # self.spinBox_nummer.setEnabled(False)

    ############################################################################
    ############################################################################
    ########################### CREATE PDF ####################################
    ############################################################################

    def cb_drafts_enabled(self):
        if self.cb_drafts.isChecked():
            warning_window(
                "Entwürfe können Fehler enthalten, die das Programm zum Absturz bringen.",
                "Speichern Sie gegebenenfalls eine erstellte Datei vor der Suche!",
                titel="Warnung - Here be dragons!",
            )

    def cb_drafts_sage_enabled(self):
        if self.cb_drafts_sage.isChecked() == True:
            warning_window(
                "Entwürfe können Fehler enthalten, die das Programm zum Absturz bringen.",
                "Speichern Sie gegebenenfalls eine erstellte Datei vor der Suche!",
                titel="Warnung - Here be dragons!",
            )

            # self.add_drafts_to_beispieldaten()

        # if self.cb_drafts_sage.isChecked() == False:
        #     self.delete_drafts_from_beispieldaten()

        self.adapt_choosing_list("sage")

    ############# def prepare_tex_for_pdf #################

    #################################################################
    ###############################################################
    ################### Befehle Creator ###########################
    #############################################################

    @report_exceptions
    def set_infos_chosen_variation(self, aufgabe_total, mode):
        aufgabe = aufgabe_total["name"]

        typ = get_aufgabentyp(self.chosen_program, aufgabe)

        if self.chosen_program == "lama":
            list_comboBox_gk = ["AG", "FA", "AN", "WS", "Zusatzthemen"]

            if typ == 1:
                gk = aufgabe_total["themen"][0]
                short_gk = shorten_gk(gk)
                if short_gk in zusatzthemen_beschreibung:
                    checkbox_gk = "checkbox_creator_themen_{0}".format(short_gk)

                    index = list_comboBox_gk.index("Zusatzthemen")
                else:
                    checkbox_gk = "checkbox_creator_gk_{0}".format(short_gk)
                    index = list_comboBox_gk.index(gk.split(" ")[0].replace("-L", ""))

                self.dict_widget_variables[checkbox_gk].setChecked(True)
                self.tab_widget_gk_cr.setCurrentIndex(index)

                if mode == "creator":
                    self.groupBox_grundkompetenzen_cr.setEnabled(False)
            elif typ == 2:
                for i, gk in enumerate(aufgabe_total["themen"]):
                    short_gk = shorten_gk(gk)

                    if short_gk in zusatzthemen_beschreibung:
                        checkbox_gk = "checkbox_creator_themen_{}".format(short_gk)
                        if i == 0:
                            index = list_comboBox_gk.index("Zusatzthemen")
                    else:
                        checkbox_gk = "checkbox_creator_gk_{}".format(short_gk)

                        try:
                            if i == 0:
                                index = list_comboBox_gk.index(
                                    gk.split(" ")[0].replace("-L", "")
                                )
                            self.dict_widget_variables[checkbox_gk].setChecked(True)
                        except ValueError:
                            warning_window(f"Die geöffnete Aufgabe {aufgabe} ist fehlerhaft!", "Bitte melden Sie dies unter lama.helpme@gmail.com, damit der Fehler behoebn werden kann. Vielen Dank!")

                    
                # self.tab_widget_gk_cr.setCurrentIndex(index)

            self.comboBox_aufgabentyp_cr.setCurrentIndex(typ - 1)
            self.groupBox_aufgabentyp.setEnabled(False)

            klasse = aufgabe_total["klasse"]

            if klasse != None:
                try:
                    full_klasse = Klassen[klasse]
                    index = self.comboBox_klassen_cr.findText(full_klasse)

                    self.comboBox_klassen_cr.setCurrentIndex(index)
                except KeyError:
                    pass

        elif self.chosen_program == "cria":
            klasse = aufgabe_total["klasse"]
            # klasse, nummer = aufgabe.split(".", 1)

            if klasse != None:
                index = list_klassen.index(klasse)
                self.tab_widget_cr_cria.setCurrentIndex(index)
            else:
                self.cb_no_grade_tag.setChecked(True)

            for thema in aufgabe_total["themen"]:

                try:
                    kapitel, unterkapitel = thema.split(".")

                    if klasse == None:
                        for all in list_klassen:

                            dict_klasse_name = eval("dict_{}_name".format(all))
                            if kapitel in dict_klasse_name:
                                thema_name = dict_klasse_name[kapitel]
                                combobox_thema = "combobox_kapitel_creator_cria_{}".format(
                                    all
                                )
                                temp_klasse = all
                                break

                    else:
                        temp_klasse = klasse
                        dict_klasse_name = eval("dict_{}_name".format(klasse))
                        thema_name = dict_klasse_name[kapitel]
                        combobox_thema = "combobox_kapitel_creator_cria_{}".format(klasse)

                    index = self.dict_widget_variables[combobox_thema].findText(
                        thema_name + " (" + kapitel + ")"
                    )

                    self.dict_widget_variables[combobox_thema].setCurrentIndex(index)
                    # continue

                    checkbox_thema = "checkbox_unterkapitel_creator_{0}_{1}_{2}".format(
                        temp_klasse, kapitel, unterkapitel
                    )

                    self.dict_widget_variables[checkbox_thema].setChecked(True)



                    if mode == "creator":
                        self.groupBox_themengebiete_cria.setEnabled(False)
                except KeyError:
                    critical_window('Es ist ein Fehler beim Aufrufen der zugeordneten Themen aufgetreten.',
                    'Das Thema {0} ist in der {1}. Klasse nicht vorhanden.'.format(thema, klasse[1]))

        self.spinBox_punkte.setValue(aufgabe_total["punkte"])

        if aufgabe_total["af"] != None:
            af = aufgabe_total["af"]
            full_aufgabenformat = dict_aufgabenformate[af]

            index = self.comboBox_af.findText(full_aufgabenformat)

            if mode == "creator":
                self.comboBox_af.setEnabled(False)

            self.comboBox_af.setCurrentIndex(index)
        else:
            self.comboBox_af.setCurrentIndex(0)

        if mode == "translation":
            self.widget_basic_settings_creator.setEnabled(False)
            self.groupBox_titel_cr.setEnabled(False)
            self.groupBox_quelle.setEnabled(False)
            # self.groupBox_bilder.setEnabled(False)

            if self.chosen_program == "cria":
                self.groupBox_themengebiete_cria.setEnabled(False)
            elif self.chosen_program == "lama":
                self.groupBox_grundkompetenzen_cr.setEnabled(False)



        self.lineEdit_titel.setText(aufgabe_total["titel"])


        if mode == "editor":
            if not is_empty(aufgabe_total['bilder']):
                # self.label_bild_leer.hide()
                for all in aufgabe_total['bilder']:
                    self.add_image_label(all, None)#, clickable=False

                self.verticalLayout_bilder2.addWidget(self.btn_add_image)

            if aufgabe_total["info"] == "mat":
                self.cb_matura_tag.setChecked(True)
            # else:
            #     self.cb_matura_tag.setChecked(False)


            self.plainTextEdit.clear()
            self.plainTextEdit.insertPlainText(aufgabe_total["content"])
            self.lineEdit_quelle.setText(aufgabe_total["quelle"])
        elif mode == "translation":
            self.lineEdit_quelle.setText(aufgabe_total["quelle"])

    def reset_variation(self):
        self.button_variation_cr.setText("Aufgabenvariation")
        self.button_translation_cr.setText("Übersetzung")
        self.pushButton_save_translation.hide()
        self.pushButton_save.show()
        self.groupBox_grundkompetenzen_cr.setEnabled(True)
        self.groupBox_aufgabentyp.setEnabled(True)
        self.comboBox_af.setEnabled(True)
        self.groupBox_themengebiete_cria.setEnabled(True)
        self.widget_basic_settings_creator.setEnabled(True)

    def reset_edit_file(self):
        self.button_choose_file.setText("Aufgabe suchen...")
        self.enable_widgets_editor(False)
        self.button_language.setToolTip("")
        self.button_language.setText("DE")
        self.button_translation_cr.setText("Übersetzung")
        self.plainTextEdit.clear()
        try:
            del self.temporary_save_edit_plainText_deutsch
        except AttributeError:
            pass
        try:
            del self.temporary_save_edit_plainText_englisch
        except AttributeError:
            pass
        # self.groupBox_grundkompetenzen_cr.setEnabled(True)
        # self.groupBox_aufgabentyp.setEnabled(True)
        # self.comboBox_af.setEnabled(True)
        # self.groupBox_themengebiete_cria.setEnabled(True)

    @report_exceptions
    def button_variation_cr_pressed(self, mode):
        Dialog = QtWidgets.QDialog(
            None,
            QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint,
        )
        ui = Ui_Dialog_variation()

        if mode == "creator":
            show_variations = False
        else:
            show_variations = True

        ui.setupUi(Dialog, self, show_variations, mode)

        response = Dialog.exec()

        if response == 1:
            self.suchfenster_reset(True)
            self.reset_variation()
            if mode == "creator" or mode == "translation":
                _file_ = ui.chosen_variation

                if _file_ != None:
                    if mode == "creator":
                        self.chosen_variation = ui.chosen_variation
                        self.button_variation_cr.setText(
                            "Variation von: {}".format(self.chosen_variation.upper())
                        )
                        self.pushButton_save_translation.hide()
                        self.pushButton_save.show()
                    elif mode == "translation":
                        self.chosen_file_to_edit = ui.chosen_variation
                        typ = get_aufgabentyp(self.chosen_program, self.chosen_file_to_edit)
                        aufgabe_total = get_aufgabe_total(self.chosen_file_to_edit, typ)

                        try:
                            if aufgabe_total['content_translation'] != None:
                                rsp = question_window("Für diese Aufgabe ist bereits eine englische Übersetzung vorhanden. Möchten Sie diese bearbeiten?")
                                if rsp == False:
                                    self.suchfenster_reset(True)
                                    self.reset_variation()
                                    return
                                else:
                                    self.plainTextEdit.setPlainText(aufgabe_total['content_translation'])
                        except KeyError:
                            pass

                        self.pushButton_save_translation.show()
                        self.pushButton_save.hide()
                        self.button_translation_cr.setText(
                            "Übersetzung von: {}".format(self.chosen_file_to_edit.upper())
                        )
                else:
                    self.suchfenster_reset(True)
                    self.reset_variation()
                    return
            elif mode == "editor":
                self.chosen_file_to_edit = ui.chosen_variation
                _file_ = self.chosen_file_to_edit
                if self.chosen_file_to_edit != None:
                    self.button_choose_file.setText(
                        "Gewählte Aufgabe: {}".format(self.chosen_file_to_edit.upper())
                    )
                    self.pushButton_save.hide()
                else:
                    self.suchfenster_reset(True)
                    self.reset_edit_file()
                    return

            typ = get_aufgabentyp(self.chosen_program, _file_)

            aufgabe_total_original = get_aufgabe_total(_file_, typ)

            self.enable_widgets_editor(True)

        if response == 0:
            return

        self.set_infos_chosen_variation(aufgabe_total_original, mode)

    def add_image_label(self, image_name, image_path):
        self.dict_picture_path[image_name] = image_path

        widget_picture = QtWidgets.QWidget(self.groupBox_bilder)
        self.verticalLayout_bilder2.insertWidget(len(self.verticalLayout_bilder2) - 2, widget_picture)
        # self.verticalLayout_bilder.addWidget(widget_picture)

        horizontalLayoutWidget_picture = create_new_horizontallayout(widget_picture)
        horizontalLayoutWidget_picture.setContentsMargins(0,0,0,0)
        label_picture = create_new_label(widget_picture, image_name)       
        horizontalLayoutWidget_picture.addWidget(label_picture)

        # widget_picture_name = "widget_bild_creator_{}".format(image_name)
        self.dict_widget_variables[image_name] = widget_picture

        horizontalLayoutWidget_picture.addStretch()

        pushButton_deletePicture = create_new_button(widget_picture, "", partial(self.del_picture, image_name))
        pushButton_deletePicture.setIcon(QtGui.QIcon(get_icon_path('trash-2.svg')))
        pushButton_deletePicture.setSizePolicy(SizePolicy_fixed)
        horizontalLayoutWidget_picture.addWidget(pushButton_deletePicture)


        # if clickable == True:
        # label_picture.clicked.connect(
            
        # )
        # else:
        #     label_picture.setStyleSheet("color: gray")
        # self.verticalLayout.addWidget(label_picture)

    def open_msg_box_choose_image(self):
        msg = QtWidgets.QMessageBox()
        # msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowIcon(QtGui.QIcon(logo_path))
        msg.setText("Möchten Sie eine neue Grafik hinzufügen oder die Aufgabe mit einer bereits vorhandenen Grafik verknüpfen?")
        # msg.setInformativeText('Möchten Sie das neue Update installieren?')
        msg.setWindowTitle("Grafik hinzufügen")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
        button_new = msg.button(QtWidgets.QMessageBox.Yes)
        button_new.setText("Neue Grafik hinzufügen")
        button_new.setIcon(QtGui.QIcon(get_icon_path('image.svg')))
        button_existing = msg.button(QtWidgets.QMessageBox.No)
        button_existing.setText("Vorhande Grafik verknüpfen")
        button_existing.setIcon(QtGui.QIcon(get_icon_path('link.svg')))
        button_cancel = msg.button(QtWidgets.QMessageBox.Cancel)
        button_cancel.setText("Abbrechen")
        response = msg.exec_()
        return response

    @report_exceptions
    def btn_add_image_pressed(self):
        
        response = self.open_msg_box_choose_image()

        if response == QtWidgets.QMessageBox.Yes:
            mode = 'new'
        elif response == QtWidgets.QMessageBox.No:
            mode = 'existing'
        elif response == QtWidgets.QMessageBox.Cancel:
            return
  

        if mode == 'new':
            try:
                self.saved_file_path
            except AttributeError:
                self.saved_file_path = path_home
            open_path = os.path.dirname(self.saved_file_path)
        elif mode == 'existing':
            if self.developer_mode_active == True:
                open_path = os.path.join(path_database, 'Bilder')
            else:
                if os.path.isdir(os.path.join(path_database, 'Bilder_local')) == False:
                    critical_window("Es konnten keine lokal gespeicherten Grafiken gefunden werden.")
                    return
                else:
                    open_path = os.path.join(path_database, 'Bilder_local')
        list_filename = QtWidgets.QFileDialog.getOpenFileNames(
            None,
            "Grafiken wählen",
            open_path,
            "Grafiken (*.eps)",
        )
        if list_filename[0] == []:
            return
        
        if mode == 'new':
            self.saved_file_path = os.path.dirname(list_filename[0][0])
        elif mode == 'existing':
            if os.path.normpath(os.path.dirname(list_filename[0][0])) == os.path.normpath(os.path.join(path_database, 'Bilder')) or os.path.normpath(os.path.dirname(list_filename[0][0])) == os.path.normpath(os.path.join(path_database, 'Bilder_addon')) or os.path.normpath(os.path.dirname(list_filename[0][0])) == os.path.normpath(os.path.join(path_database, 'Bilder_local')):
                pass
            else:
                critical_window('Die ausgewählte Grafik(en) ist/sind noch nicht in der Datenbank enthalten. Bitte wählen Sie "Neue Grafik hinzufügen", um die Grafik einzubinden.')
                return
        # i = len(self.dict_picture_path)

        # self.label_bild_leer.hide()
        for all in list_filename[0]:
            _, tail = os.path.split(all)

            if tail in self.dict_picture_path.keys():
                information_window("Eine Grafik mit dem Namen {} wurde bereits hinzugefügt.".format(tail))
            else:
                if mode == 'existing':
                    self.add_image_label(tail, 'no_copy')
                else:    
                    # _, tail = os.path.split(all)
                    self.add_image_label(tail, all)

        # self.verticalLayout_bilder.addWidget(self.btn_add_image)

    @report_exceptions
    def del_picture(self, image_name, question=True):
        if question == True:
            rsp = question_window(
                'Sind Sie sicher, dass Sie die Grafik "{}" entfernen möchten?'.format(
                    image_name # self.dict_picture_path[self.dict_widget_variables[picture].text()]
                )
            )
            if rsp == False:
                return
        del self.dict_picture_path[image_name]

        self.dict_widget_variables[image_name].setParent(None)
        # self.dict_widget_variables[image_name].hide()
        # if len(self.dict_picture_path) == 0:
        #     self.label_bild_leer.show()

        del self.dict_widget_variables[image_name]

    @report_exceptions
    def convert_image_eps_clicked(self):
        Dialog = QtWidgets.QDialog(
            None,
            QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint,
        )
        ui = Ui_Dialog_Convert_To_Eps()
        ui.setupUi(Dialog, self)

        Dialog.exec()


    def chosen_aufgabenformat_editor(self):
        if self.comboBox_aufgabentyp_editor.currentText() == "Typ 1":
            self.groupBox_aufgabenformat_editor.setEnabled(True)
            self.comboBox_pagebreak_editor.setCurrentIndex(0)
            # self.label_keine_auswahl.hide()
            # self.comboBox_af.show()
            self.comboBox_af_editor.removeItem(0)
        if self.comboBox_aufgabentyp_editor.currentText() == "Typ 2":
            self.comboBox_af_editor.insertItem(0, "keine Auswahl nötig")
            self.comboBox_pagebreak_editor.setCurrentIndex(1)
            self.comboBox_af_editor.setCurrentIndex(0)
            self.groupBox_aufgabenformat_editor.setEnabled(False)
            # self.label_keine_auswahl.show()
            # self.comboBox_af.hide()         
    
    def chosen_aufgabenformat_cr(self):
        if self.comboBox_aufgabentyp_cr.currentText() == "1":
            self.groupBox_aufgabenformat.setEnabled(True)
            self.comboBox_pagebreak.setCurrentIndex(0)
            # self.label_keine_auswahl.hide()
            # self.comboBox_af.show()
            self.comboBox_af.removeItem(0)
        if self.comboBox_aufgabentyp_cr.currentText() == "2":
            self.comboBox_af.insertItem(0, "keine Auswahl nötig")
            self.comboBox_pagebreak.setCurrentIndex(1)
            self.comboBox_af.setCurrentIndex(0)
            self.groupBox_aufgabenformat.setEnabled(False)
            # self.label_keine_auswahl.show()
            # self.comboBox_af.hide()

    def button_language_pressed(self):
        typ = get_aufgabentyp(self.chosen_program, self.chosen_file_to_edit)
        aufgabe_total = get_aufgabe_total(self.chosen_file_to_edit, typ)
        
        if self.button_language.text() == "DE":
            self.temporary_save_edit_plainText_deutsch = self.plainTextEdit.toPlainText()
            self.plainTextEdit.clear()
            self.button_language.setToolTip("Englisch")
            self.button_language.setText("EN")

            try: 
                self.plainTextEdit.insertPlainText(self.temporary_save_edit_plainText_englisch)
            except AttributeError:
                try:
                    content = aufgabe_total["content_translation"]
                    if content != None: 
                        self.plainTextEdit.insertPlainText(content)
                except KeyError:
                    pass
            
        else:
            self.temporary_save_edit_plainText_englisch = self.plainTextEdit.toPlainText()
            self.plainTextEdit.clear()
            self.button_language.setToolTip("Deutsch")
            self.button_language.setText("DE")
            try: 
                self.plainTextEdit.insertPlainText(self.temporary_save_edit_plainText_deutsch)
            except AttributeError:
                self.plainTextEdit.insertPlainText(aufgabe_total["content"])

            # 
    def get_number_of_included_images(self):
        num = self.plainTextEdit.toPlainText().count("\includegraphics")
        return num

    def check_included_attached_image_ratio(self):
        included = self.get_number_of_included_images()
        attached = len(self.dict_picture_path)
        return included, attached

    def check_entry_creator(self, mode, typ):
        if self.chosen_program == "lama":
            if is_empty(self.list_selected_topics_creator) == True:
                return "Es wurden keine Grundkompetenzen zugewiesen."

            if typ == 1:
                if len(self.list_selected_topics_creator) > 1:
                    return "Es wurden zu viele Grundkompetenzen zugewiesen."

        if (
            self.chosen_program == "cria"
            and is_empty(self.list_selected_topics_creator) == True
        ):
            return "Es wurden keine Themengebiete zugewiesen."

        if (
            typ != 2
            and self.comboBox_af.currentText() == "bitte auswählen"
        ):
            return "Es wurde kein Aufgabenformat ausgewählt."

        if (
            is_empty(self.lineEdit_titel.text()) == True
            or self.lineEdit_titel.text().isspace()
        ):
            return "Bitte geben Sie einen Titel ein."

        if is_empty(self.plainTextEdit.toPlainText()) == True and mode != "translation" and self.button_language.text()=="DE":
            return 'Bitte geben Sie den LaTeX-Quelltext der Aufgabe im Bereich "Aufgabeneingabe" ein.'


        included, attached = self.check_included_attached_image_ratio()
        if included != attached:
            if included > attached:
                str_ = "wenige"
            elif included < attached:
                str_ = "viele"
            warning = "Es sind zu {0} Bilder angehängt ({1}/{2})".format(
                str_, included, attached
            )
            return warning

        if mode == 'save':
            missing_images = []
            for image in self.dict_picture_path.keys():
                output = re.search(r'{{"?{0}"?}}'.format(image), self.plainTextEdit.toPlainText())

                if output == None:
                    missing_images.append('"'+image+'"')
                        
            if not is_empty(missing_images):
                missing_images_string = ', '.join(missing_images)
                return 'Die Grafik(en) {} konnte(n) im Aufgabentext nicht gefunden werden.\n\nGrafiken dürfen nur in der Form "Bild.eps" in dem Quelltext (ohne Angabe eines Dateipfades) eingebunden sein und der Titel muss exakt mit den Titeln der hizugefügten Grafiken übereinstimmen.'.format(missing_images_string)


        if is_empty(self.lineEdit_quelle.text()) == True:
            return "Bitte geben Sie die Quelle an."

        elif (
            self.developer_mode_active == False
            and len(self.lineEdit_quelle.text()) != 6
        ):
            return 'Bitte geben Sie als Quelle ihren Vornamen und Nachnamen im Format "VorNac" (6 Zeichen!) ein.'



    def create_information_aufgabentyp(self):
        if self.chosen_program == "lama":
            aufgabentyp = "Aufgabentyp: {0}\n\n".format(
                self.comboBox_aufgabentyp_cr.currentText()
            )
        if self.chosen_program == "cria":
            aufgabentyp = ""

        return aufgabentyp

    def create_information_titel(self):
        titel = self.lineEdit_titel.text().strip()
        return titel

    def create_information_themen(self):
        if self.chosen_program == "lama":
            themen = ", ".join(self.list_selected_topics_creator)
            if len(self.list_selected_topics_creator) == 1:
                titel_themen = "Grundkompetenz"
            else:
                titel_themen = "Grundkompetenzen"
        if self.chosen_program == "cria":
            list_labels = []
            for all in self.list_selected_topics_creator:
                thema_label = all[1] + "." + all[2] + " (" + all[0][1] + ".)"
                list_labels.append(thema_label)
            themen = ", ".join(list_labels)
            titel_themen = "Themengebiet(e)"
        return titel_themen, themen

    def create_information_bilder(self):
        if self.dict_picture_path != {}:
            bilder = ", ".join(self.dict_picture_path)
            bilder = "\n\nBilder: {}".format(bilder)
        else:
            bilder = ""
        return bilder

    def create_information_aufgabenformat(self):
        if (
            self.chosen_program == "cria"
            or self.comboBox_aufgabentyp_cr.currentText() == "Typ 1"
        ):
            aufgabenformat = "Aufgabenformat: %s\n\n" % self.comboBox_af.currentText()
        else:
            aufgabenformat = ""
        return aufgabenformat

    def create_information_of_file_creator(self):
        aufgabentyp = self.create_information_aufgabentyp()
        titel = self.create_information_titel()
        titel_themen, themen = self.create_information_themen()
        aufgabenformat = self.create_information_aufgabenformat()
        bilder = self.create_information_bilder()
        quelle = self.lineEdit_quelle.text()

        return [
            aufgabentyp,
            titel,
            titel_themen,
            themen,
            aufgabenformat,
            quelle,
            bilder,
        ]

    def check_for_local_save_mode(self):
        local = False
        for all in self.dict_picture_path.values():
            if all == "no_copy":
                local = True
                break

        if (self.chosen_variation != None and "l." in self.chosen_variation.split(" - ")[-1]) or local == True:
            return 'local'
        else:
            return 'general'   

    def open_dialogwindow_save(self, information):
        
        save_mode = self.check_for_local_save_mode()
        

        Dialog_speichern = QtWidgets.QDialog(
            None,
            QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint,
        )
        self.ui_save = Ui_Dialog_speichern()
        self.ui_save.setupUi(Dialog_speichern, self.developer_mode_active, self.chosen_variation,save_mode)
        self.ui_save.label.setText(information)
        # self.ui_save.label.setStyleSheet("padding: 10px")
        return Dialog_speichern

    def create_path_from_list(self, list_):
        path = ""
        for all in list_:
            path = os.path.join(path, all)

        return path

    def get_parent_folder(self, typ_save):
        list_path = [path_programm]

        # if self.local_save == True:
        #     list_path.append("Lokaler_Ordner")
        # else:
        # if typ_save == ["admin", 1]:
        #     list_path.append("_database_inoffiziell")
        # else:
        list_path.append("_database")
        return list_path

    def get_highest_grade_cr(self):
        klasse = 1
        # themen_auswahl = self.get_themen_auswahl()

        for all in self.list_selected_topics_creator:
            if int(all[0][1]) > klasse:
                klasse = int(all[0][1])
        # for all in themen_auswahl:
        #     if int(all[1]) > klasse:
        #         klasse = int(all[1])

        return "k{}".format(klasse)

    def get_max_integer(self, table_lama, typ, themen_auswahl):
        max_integer = 0
        _file_ = Query()

        if self.chosen_variation != None:
            pattern = "{}\[.*\]".format(self.chosen_variation)
            all_files = table_lama.search(_file_.name.matches(pattern))
        elif typ == 1:
            all_files = table_lama.search(_file_.name.matches(themen_auswahl))
        elif typ == None or typ == 2:
            # klasse = self.get_highest_grade_cr()
            #     all_files = table_lama.search(_file_.name.matches(klasse))
            # elif typ == 2:
            all_files = table_lama.all()

        for all in all_files:
            name = all["name"].replace("l.", "").replace("i.", "")
            if typ == 1:
                num = name.split(" - ")[-1]
            elif typ == None or typ == 2:
                #     num = name.split(".")[-1]
                # elif typ == 2:
                num = name

            if self.chosen_variation == None:
                num = int(num.split("[")[0])
            else:
                num = re.search("\[(.*)\]", num)
                num = int(num.group(1))

            if num > max_integer:
                max_integer = num

        return max_integer

    def edit_image_name(self, typ_save, name):
        # if typ_save[0] == "local":
        #     local = "_L_"
        # else:
        #     local = ""
        name = name.replace(" ","")


        if self.chosen_variation == None:
            number = self.max_integer + 1
        else:
            list_ = re.split(" - |_", self.chosen_variation)
            variation_number = list_[-1]
            # _,variation_number = self.chosen_variation.split(" - ")
            number = "{0}[{1}]".format(variation_number, self.max_integer + 1)

        # if typ_save == ["admin", 1]:
        #     number = "i." + str(number)
        if typ_save[0] == "local":
            number = "l." + str(number)

        if self.chosen_program == "cria":
            # highest_grade = self.get_highest_grade_cr()
            name = "{0}-{1}".format(number, name)

        elif self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
            # thema, klasse = self.split_thema_klasse(
            #     self.list_selected_topics_creator[0]
            # )
            # if thema == None:
            thema = shorten_gk(self.list_selected_topics_creator[0]).upper()
            name = "{0}-{1}-{2}".format(thema, number, name)

        elif self.comboBox_aufgabentyp_cr.currentText() == "Typ 2":
            name = "{0}-{1}".format(number, name)

        return name

    def replace_image_name(self, typ_save):
        textBox_Entry = self.plainTextEdit.toPlainText()
        for old_image_name in self.dict_picture_path:
            if self.dict_picture_path[old_image_name] == None:
                continue
            string = "{" + old_image_name + "}"

            if self.dict_picture_path[old_image_name] == "no_copy":
                new_image_name = old_image_name
            else:
                new_image_name = self.edit_image_name(typ_save, old_image_name)
            # if typ_save == ["admin", 0]:
            #     path = "../_database/Bilder/"
            # elif typ_save == ["admin", 1]:
            #     path = "../_database_inoffiziell/Bilder/"
            # elif typ_save[0] == "user":
            #     path = "../_database/Bilder/"
            if typ_save[0] == "local":
                path = "../_database/Bilder_local/"
            else:
                path = "../_database/Bilder/"

            new_image_name = path + new_image_name

            if string in self.plainTextEdit.toPlainText():
                textBox_Entry = textBox_Entry.replace(old_image_name, new_image_name)
            else:
                string = '{"' + old_image_name + '"}'

                if string in self.plainTextEdit.toPlainText():
                    image_name = '"' + old_image_name + '"'
                    textBox_Entry = textBox_Entry.replace(image_name, new_image_name)
                else:
                    return [False, old_image_name]

        return [True, textBox_Entry]

    def copy_image_save(self, typ_save, parent_image_path):
        list_images = []
        for old_image_name in self.dict_picture_path:
            old_image_path = self.dict_picture_path[old_image_name]

            if old_image_path == None: 
                continue

            if old_image_path == 'no_copy':
                list_images.append(old_image_name)
                continue

            # old_image_name = os.path.basename(old_image_path)
            new_image_name = self.edit_image_name(typ_save, old_image_name)

            list_images.append(new_image_name)


            new_image_path = os.path.join(parent_image_path, new_image_name)

            try:
                shutil.copy(old_image_path, new_image_path)
            except FileNotFoundError:
                try:
                    os.mkdir(parent_image_path)
                    shutil.copy(old_image_path, new_image_path)
                except FileNotFoundError:
                    # warning_window(
                    #     'Die Grafik mit dem Dateinamen "{}" konnte im Aufgabentext nicht gefunden werden.'.format(
                    #         old_image_name
                    #     ),
                    #     "Bitte versichern Sie sich, dass der Dateiname korrekt geschrieben ist und Sie die richtige Grafik eingefügt haben.",
                    # )
                    return None, old_image_name
            
        return list_images, None

    def create_file_name(self, typ, max_integer, themen_auswahl, save_typ=""):
        number = max_integer + 1
        if self.chosen_variation != None:
            name = self.chosen_variation + "[{}]".format(number)
        elif typ == 1:
            name = "{0} - {1}{2}".format(themen_auswahl, save_typ, number)
        elif typ == None or typ == 2:
            #     klasse = self.get_highest_grade_cr()
            #     name = "{0}.{1}{2}".format(klasse, save_typ, number)
            # elif typ == 2:
            name = "{0}{1}".format(save_typ, number)

        return name

    def get_themen_auswahl(self):
        themen_auswahl = []
        if self.chosen_program == "cria":
            for all in self.list_selected_topics_creator:
                # if self.cb_no_grade_tag.isChecked:
                #     thema = all[1] + "." + all[2]
                # else:
                thema = all[1] + "." + all[2]
                if thema not in themen_auswahl:
                    themen_auswahl.append(thema)

        elif self.comboBox_aufgabentyp_cr.currentText() == "1":
            themen_auswahl.append(self.list_selected_topics_creator[0])

        elif self.comboBox_aufgabentyp_cr.currentText() == "2":

            for all in self.list_selected_topics_creator:
                themen_auswahl.append(all)

        return themen_auswahl

    def define_themen_string_cria(self):
        list_ = [
            x[1] + "." + x[2] + " (" + x[0][1] + ".)"
            for x in self.list_selected_topics_creator
        ]
        string = ", ".join(list_)
        return string

    def exisiting_variations_AB(self, content):
        rsp = re.search("\\\\variation\{.*\}\{.*\}", content)
        if rsp == None:
            return False
        else:
            return True
        
    def get_all_infos_new_file(self, typ, typ_save):
        if typ_save == "editor":
            name = None
        else:
            if typ_save == "local":
                save_typ = "l."
            else:
                save_typ = ""

            name = self.create_file_name(
                typ, self.max_integer, self.themen_auswahl[0], save_typ=save_typ
            )
            # if typ_save=='local':
            #     gk, number  = name.split(' - ')
            #     name = gk + ' - ' + 'l.' + number
        themen = self.get_themen_auswahl()
        titel = self.lineEdit_titel.text().strip()
        if typ == 2:
            af = None
        else:
            af = list(dict_aufgabenformate.keys())[
                list(dict_aufgabenformate.values()).index(
                    self.comboBox_af.currentText()
                )
            ]
        quelle = self.lineEdit_quelle.text()
        content = self.plainTextEdit.toPlainText()

        group_variation = self.exisiting_variations_AB(content)


        punkte = self.spinBox_punkte.value()

        if self.comboBox_pagebreak.currentIndex() == 0:
            pagebreak = False
        elif self.comboBox_pagebreak.currentIndex() == 1:
            pagebreak = True

        if typ == None:
            if self.cb_no_grade_tag.isChecked():
                klasse = None
            else:
                klasse = self.get_highest_grade_cr()
        elif self.comboBox_klassen_cr.currentIndex() == 0:
            klasse = None
        else:
            klasse = list(Klassen.keys())[self.comboBox_klassen_cr.currentIndex() - 1]

        if self.cb_matura_tag.isChecked():
            info = "mat"
        else:
            info = None

        if typ_save == "editor":
            bilder = []
            for all in self.dict_picture_path.keys():
                bilder.append(all)
        else:
            bilder = None

        if typ_save == "user":
            draft = True
        else:
            draft = False

        abstand = self.spinBox_abstand.value()

        return (
            name,
            themen,
            titel,
            af,
            quelle,
            content,
            group_variation,
            punkte,
            pagebreak,
            klasse,
            info,
            bilder,
            draft,
            abstand,
        )

    def upload_single_file_change(self, name, message):
        if "(lokal)" not in name:
            # if "i." in name:
            #     chosen_ddb = ["_database_addon.json"]
            # else:
            chosen_ddb = ["_database.json"]
            action_push_database(
                False, chosen_ddb, message=message, worker_text="wird hochgeladen ..."
            )

    @report_exceptions
    def button_save_edit_pressed(self, mode):
        if mode == "translation":
            text = "Übersetzung"
        else:
            text = "Änderung"

        rsp = question_window(f"Sind Sie sicher, dass Sie die {text} speichern wollen?")
        if rsp == False:
            return


        name = self.chosen_file_to_edit.replace(" (lokal)", "")
        typ = get_aufgabentyp(self.chosen_program, name)

        warning = self.check_entry_creator(mode, typ)
        if warning != None:
            if self.developer_mode_active == True:
                rsp = question_window(f"WARNUNG: {warning}", "Möchten Sie die Aufgabe dennoch speichern?", default='no')
                if rsp == False:
                    return
            else:
                warning_window(warning)
                return

        (
            _,
            themen,
            titel,
            af,
            quelle,
            content,
            group_variation,
            punkte,
            pagebreak,
            klasse,
            info,
            bilder,
            draft,
            abstand,
        ) = self.get_all_infos_new_file(typ, "editor")

        lama_table = get_table(name, typ)

        if typ == 1:
            if themen[0] in name:
                new_name = name
            else:
                themen_auswahl = self.get_themen_auswahl()
                max_integer = self.get_max_integer(lama_table, typ, themen_auswahl[0])

                if "l." in name:
                    save_typ = "l."
                elif "i." in name:
                    save_typ = "i."
                else:
                    save_typ = ""

                new_name = self.create_file_name(
                    typ, max_integer, themen_auswahl[0], save_typ
                )

        _file_ = Query()

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        if "l." not in name and "i." not in name:
            rsp = check_branches()
            if rsp == False:
                rsp = self.worker_update_database()
                if rsp == False:
                    critical_window(
                        "Beim Synchronisieren ist ein Fehler aufgetreten. Bitte stellen Sie sicher, dass eine Internetverbindung beseteht und versuchen Sie es erneut."
                    )
                    QtWidgets.QApplication.restoreOverrideCursor()
                    return
                lama_table.clear_cache()

        file_id = lama_table.get(_file_.name == name).doc_id

        if mode == "translation":
            if is_empty(content):
                content = None
            lama_table.update({"content_translation": content}, doc_ids=[file_id]) 
        else:
            if typ == 1:
                lama_table.update({"name": new_name}, doc_ids=[file_id])
            lama_table.update({"themen": themen}, doc_ids=[file_id])
            lama_table.update({"titel": titel}, doc_ids=[file_id])
            lama_table.update({"af": af}, doc_ids=[file_id])
            lama_table.update({"quelle": quelle}, doc_ids=[file_id])
            if self.button_language.text()=="DE":
                lama_table.update({"content": content}, doc_ids=[file_id])
                try: 
                    content_englisch = self.temporary_save_edit_plainText_englisch
                    lama_table.update({"content_translation": content_englisch}, doc_ids=[file_id])
                except AttributeError:
                    pass
            elif self.button_language.text()=="EN":
                if is_empty(content):
                    content = None
                lama_table.update({"content_translation": content}, doc_ids=[file_id])
                try: 
                    content_deutsch = self.temporary_save_edit_plainText_deutsch
                    lama_table.update({"content": content_deutsch}, doc_ids=[file_id])
                except AttributeError:
                    pass               
            lama_table.update({"gruppe": group_variation}, doc_ids=[file_id])
            lama_table.update({"punkte": punkte}, doc_ids=[file_id])
            lama_table.update({"pagebreak": pagebreak}, doc_ids=[file_id])
            lama_table.update({"klasse": klasse}, doc_ids=[file_id])
            lama_table.update({"info": info}, doc_ids=[file_id])
            if bilder != [] and bilder != None:
                # aufgabe_total = lama_table.get(_file_.name == aufgabe)
                # old_pictures = aufgabe_total['bilder']
                # for all in old_pictures:
                #     bilder.append(all)
                lama_table.update({"bilder": bilder}, doc_ids=[file_id])

            lama_table.update({"draft": draft}, doc_ids=[file_id])
            lama_table.update({"abstand": abstand}, doc_ids=[file_id])


        QtWidgets.QApplication.restoreOverrideCursor()

        if "l." not in name and "i." not in name:
            self.upload_single_file_change(name, message="Bearbeitet: {}".format(name))

        # if "(lokal)" not in name:
        #     if "i." in new_name:
        #         chosen_ddb = ["_database_addon.json"]
        #     else:
        #         chosen_ddb = ["_database.json"]
        #     action_push_database(False, chosen_ddb, message= "Bearbeitet: {}".format(name), worker_text="Änderung hochladen ...")

        information_window(f"Die {text} wurde erfolgreich gespeichert.")

        self.suchfenster_reset(True)
        self.reset_edit_file()


    def button_vorschau_edit_pressed(self):
        content = self.plainTextEdit.toPlainText()
        file_path = os.path.join(path_localappdata_lama, "Teildokument", "preview.tex")
        if self.comboBox_pagebreak.currentIndex()==0:
            pagebreak = False
        else:
            pagebreak = True
        rsp = create_tex(file_path, content, punkte = self.spinBox_punkte.value(), pagebreak=pagebreak)

        if rsp == True:
            create_pdf("preview")
        else:
            critical_window(
                "Die PDF Datei konnte nicht erstellt werden", detailed_text=rsp
            )

    def button_delete_file_pressed(self):
        name = self.chosen_file_to_edit
        rsp = question_window(
            'Sind Sie sicher, dass Sie die Aufgabe "{}" endgültig und unwiderruflich löschen möchten?'.format(
                name
            )
        )

        if rsp == False:
            return

        typ = get_aufgabentyp(self.chosen_program, name)

        aufgabe_total = get_aufgabe_total(name, typ)
        images = aufgabe_total["bilder"]

        lama_table = get_table(name, typ)

        if "l." not in name:
            rsp = check_branches()
            if rsp == False:
                rsp = self.worker_update_database()
                if rsp == False:
                    critical_window(
                        "Beim Synchronisieren ist ein Fehler aufgetreten. Bitte stellen Sie sicher, dass eine Internetverbindung beseteht und versuchen Sie es erneut."
                    )
                    QtWidgets.QApplication.restoreOverrideCursor()
                    return
                lama_table.clear_cache()


        delete_file(name, typ)

        if "l." not in name:
            if is_empty(images):
                self.upload_single_file_change(
                    name, message="Gelöscht: {}".format(name)
                )
            else:
                self.push_full_database()


        information_window(
            'Die Aufgabe "{}" wurde erfolgreich aus der Datenbank entfernt.'.format(
                name
            )
        )

        self.suchfenster_reset(True)
        self.reset_edit_file()

    def pushButton_save_as_variation_edit_pressed(self):
        Dialog = QtWidgets.QDialog(
            None,
            QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint,
        )
        ui = Ui_Dialog_variation()
        ui.setupUi(
            Dialog,
            self,
            show_variations=False,
            chosen_file_to_edit=self.chosen_file_to_edit,
        )
        # self.Dialog.show()
        response = Dialog.exec()

        if response == 0:
            return

        self.chosen_variation = ui.chosen_variation

        if self.chosen_variation == None:
            self.pushButton_save_as_variation_edit.setText(
                "Als Variation einer anderen Aufgabe speichern"
            )
            return

        # self.pushButton_save_as_variation_edit.setText("")

        if "local" in self.chosen_variation:
            database = _local_database
        else:
            database = _database

        # if typ_save[0] == "local":
        #     database = _local_database
        # else:
        #     database = _database

        if self.chosen_program == "cria":
            typ = None
            typ_name = "cria"
        else:
            typ = self.comboBox_aufgabentyp_cr.currentIndex() + 1
            typ_name = "lama_{}".format(typ)

        table = "table_" + typ_name
        table_lama = database.table(table)

        rsp = check_branches()
        if rsp == False:
            rsp = self.worker_update_database()
            if rsp == False:
                critical_window(
                    "Beim Synchronisieren ist ein Fehler aufgetreten. Bitte stellen Sie sicher, dass eine Internetverbindung beseteht und versuchen Sie es erneut."
                )
                QtWidgets.QApplication.restoreOverrideCursor()
                return
            table_lama.clear_cache()
        # database =
        # if self.chosen_variation == None:
        # save_dateipfad = self.create_aufgabenpfad(typ_save)

        # if self.chosen_variation != None:
        themen_auswahl = None
        # else:
        # themen_auswahl = self.themen_auswahl[0]

        # typ_variation = get_aufgabentyp(self.chosen_program, self.chosen_variation)

        variation_total = get_aufgabe_total(self.chosen_variation, typ)
        aufgabe_total = get_aufgabe_total(self.chosen_file_to_edit, typ)

        if typ == 1 and aufgabe_total["themen"] != variation_total["themen"]:
            rsp = question_window(
                "Sind Sie sicher, dass Sie die Grundkompetenz der Aufgabe von {0} auf {1} ändern möchten?".format(
                    aufgabe_total["themen"][0], variation_total["themen"][0]
                )
            )
            if rsp == False:
                return

        max_integer = self.get_max_integer(table_lama, typ, themen_auswahl)

        name = self.create_file_name(typ, max_integer, themen_auswahl)
        
        _file_ = Query()
        if typ == 1 and aufgabe_total["themen"] != variation_total["themen"]:
            table_lama.update(
                {"themen": variation_total["themen"]},
                _file_.name == self.chosen_file_to_edit,
            )
        table_lama.update({"name": name}, _file_.name == self.chosen_file_to_edit)

        self.upload_single_file_change(
            name,
            message="Gespeichert als Variation: {0} (ehemals: {1})".format(
                name, self.chosen_file_to_edit
            ),
        )

        information_window("Die Änderungen wurden erfolgreich gespeichert.")

        self.suchfenster_reset(True)
        self.reset_edit_file()

    def worker_update_database(self):
        text = "Die Datenbank wird auf den neuesten Stand gebracht ..."
        Dialog_checkchanges = QtWidgets.QDialog()
        ui = Ui_Dialog_processing()
        ui.setupUi(Dialog_checkchanges, text)

        thread = QtCore.QThread(Dialog_checkchanges)
        worker = Worker_UpdateDatabase()
        worker.finished.connect(Dialog_checkchanges.close)
        worker.moveToThread(thread)
        thread.started.connect(worker.task)
        thread.start()
        thread.exit()
        Dialog_checkchanges.exec()

        if self.reset_successfull == False:
            return False
        else:
            return True

    def button_speichern_pressed(self):
        self.local_save = False

        ######## WARNINGS #####
        if self.chosen_program == "cria":
            typ = None
        elif self.comboBox_aufgabentyp_cr.currentText() == "1":
            typ = 1
        elif self.comboBox_aufgabentyp_cr.currentText() == "2":
            typ = 2

        warning = self.check_entry_creator('save', typ)
        if warning != None:
            warning_window(warning)
            return


        ####### Collect information of file ################

        list_information = self.create_information_of_file_creator()

        information = "{0}Titel: {1}\n\n{2}: {3}\n\n{4}Quelle: {5}{6}\n\n".format(
            list_information[0],
            list_information[1],
            list_information[2],
            list_information[3],
            list_information[4],
            list_information[5],
            list_information[6],
        )

        ##### Show Dialog "Saving file"
        try:
            self.chosen_variation
        except AttributeError:
            self.chosen_variation = None

        Dialog_speichern = self.open_dialogwindow_save(information)

        response = Dialog_speichern.exec()
        if response == 0:
            return

        typ_save = self.ui_save.get_output()

        if self.developer_mode_active == True:

            while typ_save == ["user", False] or typ_save == ["local", None]:
                if typ_save == ["user", False]:
                    warning_window(
                        "Bitte bestätigen Sie die Eigenständigkeitserklärung und Lizenzvereinbarung."
                    )
                elif typ_save == ["local", None]:
                    self.local_save = question_window(
                        "Sind Sie sicher, dass Sie diese Aufgabe nur lokal speichern wollen?",
                        "ACHTUNG: Durch nicht überprüfte Aufgaben entstehen möglicherweise Fehler, die das Programm zum Absturz bringen können!",
                        "Aufgabe lokal speichern?",
                    )
                    if self.local_save == True:
                        break

                response = Dialog_speichern.exec()
                if response == 0:
                    return
                typ_save = self.ui_save.get_output()

        self.themen_auswahl = self.get_themen_auswahl()

        if typ_save[0] == "local":
            database = _local_database
        else:
            database = _database

        if self.chosen_program == "cria":
            typ = None
            typ_name = "cria"
        else:
            typ = self.comboBox_aufgabentyp_cr.currentIndex() + 1
            typ_name = "lama_{}".format(typ)
        table = "table_" + typ_name
        table_lama = database.table(table)

        self.max_integer = self.get_max_integer(table_lama, typ, self.themen_auswahl[0])

        ############################################################################

        response = self.replace_image_name(typ_save)

        if response[0] == False:
            critical_window("Es ist ein Fehler beim Einbinden der Bilder passiert. Bitte Überprüfen Sie ihre Eingabe.")
            return
        else:
            content_images_replaced = response[1]


        list_path = self.get_parent_folder(typ_save)

        if typ_save[0] == "local":
            list_path.append("Bilder_local")
        else:
            list_path.append("Bilder")
        parent_image_path = self.create_path_from_list(list_path)

        list_images_new_names, error = self.copy_image_save(typ_save, parent_image_path)


        if list_images_new_names == None:
            warning_window(
                'Die Grafik mit dem Dateinamen "{}" konnte im Aufgabentext nicht gefunden werden.'.format(
                    error
                ),
                "Bitte versichern Sie sich, dass der Dateiname korrekt geschrieben ist und Sie die richtige Grafik eingefügt haben.",
            )
            return

        ###################################################################################
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        if typ_save[0] != "local":
            internet_on = check_internet_connection()
            if internet_on == False:
                QtWidgets.QApplication.restoreOverrideCursor()
                critical_window(
                    "Stellen Sie sicher, dass eine Verbindung zum Internet besteht und versuchen Sie es erneut.",
                    titel="Keine Internetverbindung",
                )  
                return

            rsp = check_branches()
            if rsp == False:
                rsp = self.worker_update_database()

                if rsp == False:
                    critical_window(
                        "Beim Synchronisieren ist ein Fehler aufgetreten. Bitte stellen Sie sicher, dass eine Internetverbindung beseteht und versuchen Sie es erneut."
                    )
                    QtWidgets.QApplication.restoreOverrideCursor()
                    return
                table_lama.clear_cache()
                self.max_integer = self.get_max_integer(
                    table_lama, typ, self.themen_auswahl[0]
                )

        (
            name,
            themen,
            titel,
            af,
            quelle,
            content,
            group_variation,
            punkte,
            pagebreak,
            klasse,
            info,
            bilder,
            draft,
            abstand,
        ) = self.get_all_infos_new_file(typ, typ_save[0])


        content = content_images_replaced
        bilder = list_images_new_names


        rsp = add_file(
            table_lama,
            name,
            themen,
            titel,
            af,
            quelle,
            content,
            group_variation,
            punkte,
            pagebreak,
            klasse,
            info,
            bilder,
            draft,
            abstand,
        )
        QtWidgets.QApplication.restoreOverrideCursor()
        if rsp == False:
            critical_window(
                "Beim Synchronisieren ist ein Fehler aufgetreten. Bitte stellen Sie sicher, dass eine Internetverbindung beseteht und versuchen Sie es erneut."
            )
            QtWidgets.QApplication.restoreOverrideCursor()
            return

        titel = list_information[1]

        QtWidgets.QApplication.restoreOverrideCursor()
        if self.local_save == True:
            text = 'Die Aufgabe mit dem Titel\n\n"{0}"\n\nwurde lokal auf ihrem System gespeichert.'.format(
                titel
            )
        else:
            text = 'Die Aufgabe mit dem Titel\n\n"{0}"\n\nwurde gespeichert.'.format(
                titel
            )

        if self.developer_mode_active == True:
            window_title = "Admin Modus - Aufgabe erfolgreich gespeichert"
        if self.developer_mode_active == False:
            window_title = "Aufgabe erfolgreich gespeichert"

        information = '{0}Titel: "{1}"\n\n{2}: {3}\n\n{4}Quelle: {5}{6}\n\n'.format(
            list_information[0],
            list_information[1],
            list_information[2],
            list_information[3],
            list_information[4],
            list_information[5],
            list_information[6],
        )

        if typ_save[0] != "local":
            file_list = ["_database.json"]
            for image in list_images_new_names:
                name = os.path.join("Bilder", image)
                file_list.append(name)

            action_push_database(False, file_list, message="Neu: {}".format(name))

        information_window(text, "", window_title, information)

        self.suchfenster_reset()

    ##################################################################
    ################## Befehle LAMA SAGE################################

    def action_refreshddb_selected(self):
        refresh_ddb(self)

        if self.chosen_program != 'wizard':
            self.adapt_choosing_list("sage")

    def push_full_database(self):
        rsp = question_window("Sind Sie sicher, dass Sie die Datenbank hochladen möchten?")
        if rsp == False:
            return
        rsp = check_branches()
        if rsp == False:
            response = question_window(
                "Es wurden Änderungen am origin/master vorgenommen. Diese Änderungen werden unwiderruflich gelöscht. Sind Sie sicher, dass Sie die vollständige Datenbank hochladen möchten?",
                titel="Änderungen überschreiben?",
            )
            if response == False:
                return
        action_push_database(
            True, ["_database.json"], "", "Änderungen werden hochgeladen ..."
        )

    def draft_control(self):
        dict_drafts = {}
        for typ in ["cria", "lama_1", "lama_2"]:
            table = "table_" + typ
            table_lama = _database.table(table)

            result = get_drafts(table_lama)
            dict_drafts[typ] = result

        Dialog = QtWidgets.QDialog(
            None,
            QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint,
        )
        ui = Ui_Dialog_draft_control()
        ui.setupUi(Dialog, dict_drafts)

        Dialog.exec_()

    def get_missing_number(self, maximum, list_files):
        missing_numbers = []
        for i in range(1,maximum+1):
            if i not in list_files:
                # string = "{0} - {1}".format(topic, i)
                missing_numbers.append(i)
        return missing_numbers   
                    
    def check_for_missing_files(self, all_files, topic, typ):
        maximum = 0
        list_files = []
        dict_files_variations = {}

        # if typ == "typ1":
        #     progress_maximum = len(dict_gk)
        # else:
        #     progress_maximum = len(all_files)

        for file in all_files:
            # worker_text = "Fehlende Aufgabenummern werden gesucht ... ({0}|{1})".format(index, progress_maximum)
            # ui.label.setText(worker_text)

            variation = check_if_variation(file['name'])
            if typ == "typ1":
                _ ,num = file['name'].split(" - ")
            else:
                num = file['name']
            if variation == True:
                x= re.split(r"\[|\]",num)
                num = int(x[0])
                variation_num = int(x[1])
                if num in dict_files_variations:
                    dict_files_variations[num].append(variation_num)
                else:
                    dict_files_variations[num] = [variation_num]
            else:
                num = int(num)
            list_files.append(num)
            if num > maximum:
                maximum = num

        list_missing_files = []
        missing_numbers = self.get_missing_number(maximum, list_files)


        for all in missing_numbers:
            if typ == "typ1":
                string = "{0} - {1}".format(topic, all)
            else:
                string = str(all)
            list_missing_files.append(string)


        for num in dict_files_variations:
            maximum = max(dict_files_variations[num])
            missing_variation_numbers = self.get_missing_number(maximum, dict_files_variations[num])
        
            for variation_num in missing_variation_numbers:
                if typ == "typ1":
                    string  = "{0} - {1}[{2}]".format(topic, num, variation_num)
                else:
                    string  = "{0}[{1}]".format(num, variation_num)
                list_missing_files.append(string)

        
        return list_missing_files


    def file_clean_up(self):
        dict_missing_files = {}


        #### TYP 1 ###### FUNKTIONIERT!!!
        table_lama = _database.table('table_lama_1')
        _file_ = Query()
        list_missing_file = []

        i=0
        for gk in dict_gk.values():
            all_files = table_lama.search(_file_.themen.any([gk]))
            
            _list = self.check_for_missing_files(all_files, gk, "typ1")

            list_missing_file = list_missing_file + _list


            self.progress_cleanup_value += 1
            self.progress_cleanup.setValue(self.progress_cleanup_value)

            

        dict_missing_files["Typ1 Aufgaben"] = list_missing_file

        ###################################
        #### TYP 2 ###### FUNKTIONIERT!!!
        table_lama = _database.table('table_lama_2')
        all_files = table_lama.all()
        list_missing_file = self.check_for_missing_files(all_files, None, "typ2")
        dict_missing_files["Typ2 Aufgaben"] = list_missing_file

        self.progress_cleanup_value += 1
        self.progress_cleanup.setValue(self.progress_cleanup_value)
        ###################################
        #### CRIA ###### FUNKTIONIERT!!!
        table_lama = _database.table('table_cria')
        all_files = table_lama.all()
        list_missing_file = self.check_for_missing_files(all_files, None, "cria")
        dict_missing_files["Unterstufen Aufgaben"] = list_missing_file

        self.progress_cleanup_value += 1
        self.progress_cleanup.setValue(self.progress_cleanup_value)

        QtWidgets.QApplication.restoreOverrideCursor()
        return dict_missing_files


        
        # maximum = 0
        # _list = []
        # for file in all_files:
        #     variation = check_if_variation(file['name'])
        #     _,num = file['name'].split(" - ")
        #     if variation == True:
        #         x= re.split(r"\[|\]",num)
        #         num = int(x[0])
        #         variation_num = int(x[1])
        #     else:
        #         num = int(num)
        #     _list.append(num)
        #     if num > maximum:
        #         maximum = num



    def worksheet_wizard_reset(self):
        self.comboBox_themen_wizard.setCurrentIndex(0)
        self.spinBox_number_wizard.setValue(20)
        self.spinBox_column_wizard.setValue(2)
        self.combobox_fontsize_wizard.setCurrentIndex(4)
        self.combobox_nummerierung_wizard.setCurrentIndex(0)
        self.combobox_ausrichtung_wizard.setCurrentIndex(0)
        self.checkBox_show_nonogramm.setChecked(True)
        self.combobox_nonogramm_wizard.setCurrentIndex(0)
        
        for i in reversed(range(self.gridLayout_scrollArea_wizard.count())): 
            self.gridLayout_scrollArea_wizard.itemAt(i).widget().setParent(None)


        self.dict_all_examples_worksheet_wizard = {}
        self.list_of_examples_wizard = []


    def themen_changed_wizard(self):
        # self.worksheet_wizard_changed = True
        # index = self.comboBox_themen_wizard.currentIndex()
        thema = self.comboBox_themen_wizard.currentText()
        # self.lineEdit_titel_wizard.setText("Arbeitsblatt - {}".format(thema))

        if thema == themen_worksheet_wizard[0] or thema == themen_worksheet_wizard[1]:
            self.spinbox_zahlenbereich_minimum.setRange(0,999999999)
            self.spinbox_zahlenbereich_minimum.setValue(100)
            self.spinbox_zahlenbereich_maximum.setRange(0,999999999)
            self.spinbox_zahlenbereich_maximum.setValue(999)
            self.spinBox_zahlenbereich_anzahl_wizard.setMaximum(5)  

        if thema == themen_worksheet_wizard[0]:
            self.label_zahlenbereich_anzahl_wizard.setText("Summanden:")
            # self.groupBox_zahlenbereich_anzahl.setTitle("Summanden")
            self.spinBox_zahlenbereich_anzahl_wizard.setRange(2,5)
            self.spinBox_zahlenbereich_anzahl_wizard.setValue(2)
        elif thema == themen_worksheet_wizard[1]:
            self.label_zahlenbereich_anzahl_wizard.setText("Subtrahenden:")
            # self.groupBox_zahlenbereich_anzahl.setTitle("Subtrahenden")
            self.spinBox_zahlenbereich_anzahl_wizard.setRange(1,5)
            self.spinBox_zahlenbereich_anzahl_wizard.setValue(1)
        elif thema == themen_worksheet_wizard[4]:
            self.label_zahlenbereich_anzahl_wizard.setText("Zahlen:")
            self.spinbox_zahlenbereich_minimum.setRange(0,999)
            self.spinbox_zahlenbereich_maximum.setRange(0,999)
            self.spinbox_zahlenbereich_minimum.setValue(0)
            self.spinbox_zahlenbereich_maximum.setValue(20)
            self.spinBox_zahlenbereich_anzahl_wizard.setMaximum(20)
            self.spinBox_zahlenbereich_anzahl_wizard.setRange(2,20)
            # self.groupBox_zahlenbereich_anzahl.setTitle("Zahlen") 

        elif thema == themen_worksheet_wizard[5] or thema == themen_worksheet_wizard[6] or thema == themen_worksheet_wizard[7]:
            self.label_zahlenbereich_anzahl_wizard.setText("Zahlen:")
            self.spinbox_zahlenbereich_minimum.setRange(-999,999)
            self.spinbox_zahlenbereich_maximum.setRange(-999,999)
            self.spinBox_zahlenbereich_anzahl_wizard.setMaximum(20)
            self.spinBox_zahlenbereich_anzahl_wizard.setRange(2,20)
            # self.groupBox_zahlenbereich_anzahl.setTitle("Zahlen")  
            if thema == themen_worksheet_wizard[5]:
                # self.groupBox_zahlenbereich_anzahl.setTitle("Summanden")
                self.spinBox_zahlenbereich_anzahl_wizard.setValue(2)
                self.spinbox_zahlenbereich_minimum.setValue(-20)
                self.spinbox_zahlenbereich_maximum.setValue(20)
            elif thema == themen_worksheet_wizard[6]:
                # self.groupBox_zahlenbereich_anzahl.setTitle("Faktoren") 
                self.spinBox_zahlenbereich_anzahl_wizard.setValue(3)
                self.spinbox_zahlenbereich_minimum.setValue(-10)
                self.spinbox_zahlenbereich_maximum.setValue(10)
            elif thema == themen_worksheet_wizard[7]:
                self.spinBox_zahlenbereich_anzahl_wizard.setValue(4)
                self.spinbox_zahlenbereich_minimum.setValue(-10)
                self.spinbox_zahlenbereich_maximum.setValue(10)                
           

        hiding_list = []
        for all in dict_widgets_wizard:
            if all != thema:
                for widget in dict_widgets_wizard[all]:
                    if widget not in dict_widgets_wizard[thema] and widget not in hiding_list:
                        hiding_list.append(widget)
        
        for widget in hiding_list:
            eval(widget).hide()

        for widget in dict_widgets_wizard[thema]:
            eval(widget).show()


    def worksheet_wizard_setting_changed(self):
        self.worksheet_wizard_changed=True

    def checkBox_show_nonogramm_changed(self):
        if self.checkBox_show_nonogramm.isChecked():
            self.combobox_nonogramm_wizard.setEnabled(True)
        else:
            self.combobox_nonogramm_wizard.setEnabled(False)

    def spinBox_number_wizard_changed(self):
        # self.worksheet_wizard_changed=True
        # maximum = get_max_pixels_nonogram()
        # # max = 0
        # # for nonogram in all_nonogramms.values():
        # #     if len(nonogram)>max:
        # #         max = len(nonogram)
        # try:
        #     num_of_examples = len(self.list_of_examples_wizard) 
        # except AttributeError:
        #     num_of_examples = 0
        # num_of_examples += self.spinBox_number_wizard.value()
        # if num_of_examples >maximum:
        #     self.checkBox_show_nonogramm.setChecked(False)
        #     self.widget_show_nonogramm.setEnabled(False)
        #     # self.checkBox_show_nonogramm.setEnabled(False)
        #     # self.combobox_nonogramm_wizard.setEnabled(False)
        # else:
        #     self.widget_show_nonogramm.setEnabled(True)
        #     # self.checkBox_show_nonogramm.setChecked(True)
        #     # self.checkBox_show_nonogramm.setEnabled(True)
        #     # self.combobox_nonogramm_wizard.setEnabled(True)

        # self.combobox_nonogramm_wizard.clear()
        # add_new_option(self.combobox_nonogramm_wizard, 0, 'Zufällig')
        # i=1
        # for all in all_nonogramms:
        #     if len(all_nonogramms[all])>= num_of_examples:
        #         add_new_option(self.combobox_nonogramm_wizard, i, "{0} ({1})".format(all.capitalize(), len(all_nonogramms[all])))
        #         i+=1 
        self.pushButton_calculate_new_examples.setText(f"{self.spinBox_number_wizard.value()} neue Aufgaben berechnen")                  

    def spinBox_column_wizard_changed(self):
        self.reset_aufgabenboxes_wizard()


    def minimum_changed_wizard(self, min, max):
        # self.worksheet_wizard_changed=True
        if min.value() > max.value():
            max.setValue(min.value()+10)

    def combobox_ausrichtung_wizard_changed(self):
        if self.comboBox_themen_wizard.currentText()=='Subtraktion':
            if self.combobox_ausrichtung_wizard.currentIndex()==0:
                self.widgetZahlenbereich_anzahl.hide()
                self.spinBox_zahlenbereich_anzahl_wizard.setValue(1)
            else:
                self.widgetZahlenbereich_anzahl.show()

    def combobox_divisor_dividend_changed(self):
        # self.worksheet_wizard_changed=True
        if self.combobox_divisor_wizard.currentIndex()==1:
            self.label_divisor_kommastelle_wizard.show()
            self.combobox_divisor_kommastelle_wizard.show()
            self.spinBox_divisor_kommastellen_wizard.show()
            self.spinBox_divisor_kommastellen_wizard.setValue(1)
            self.spinBox_divisor_kommastellen_wizard.setMinimum(1)
            self.combobox_dividend_wizard.setCurrentIndex(1)
            self.combobox_dividend_wizard.setEnabled(False)
        else:
            self.label_divisor_kommastelle_wizard.hide()
            self.combobox_divisor_kommastelle_wizard.hide()
            self.spinBox_divisor_kommastellen_wizard.hide()
            self.spinBox_divisor_kommastellen_wizard.setMinimum(0)
            self.spinBox_divisor_kommastellen_wizard.setValue(0)
            # self.combobox_dividend_wizard.setCurrentIndex(0)
            self.combobox_dividend_wizard.setEnabled(True)

        if self.combobox_divisor_wizard.currentIndex()==0 and self.combobox_dividend_wizard.currentIndex()==0:
            self.label_ergebnis_kommastellen_wizard.hide()
            self.combobox_ergebnis_kommastellen_wizard.hide()
            self.spinbox_ergebnis_kommastellen_wizard.hide()
            self.radioButton_division_ohne_rest.show()
            self.radioButton_division_ohne_rest.setChecked(True)
            self.radioButton_division_rest.show()
        else:
            self.label_ergebnis_kommastellen_wizard.show()
            self.combobox_ergebnis_kommastellen_wizard.show()
            self.spinbox_ergebnis_kommastellen_wizard.show()
            self.radioButton_division_ohne_rest.hide()
            self.radioButton_division_rest.hide()
          


    def create_aufgabenbox_wizard(self, index, example, row, column):
        groupbox = create_new_groupbox(self.scrollAreaWidgetContents_wizard, "{}. Aufgabe".format(index+1))
        groupbox.setSizePolicy(SizePolicy_maximum_width)

        self.gridLayout_scrollArea_wizard.addWidget(groupbox ,row,column,1,1)

        horizontalLayout = create_new_horizontallayout(groupbox)
        label = create_new_label(self.scrollArea_chosen_wizard, example[-1])
        horizontalLayout.addWidget(label)
        
        # horizontalLayout.addStretch()
        # button_refresh = create_new_button(groupbox, "Refresh", still_to_define)
        button_refresh = create_new_button(groupbox, "", partial(self.reload_example, index), icon="refresh-cw.svg")
        button_refresh.setSizePolicy(SizePolicy_fixed)
        horizontalLayout.addWidget(button_refresh)

        button_delete = create_new_button(groupbox, "", partial(self.delete_example, index), icon="trash-2.svg")
        button_delete.setSizePolicy(SizePolicy_fixed)
        horizontalLayout.addWidget(button_delete)
        # button_delete = create_new_button(groupbox, "Delete", still_to_define)
        # button_delete = create_standard_button(groupbox,
        #     "",
        #     still_to_define,
        #     QtWidgets.QStyle.SP_DialogCancelButton)
        # horizontalLayout.addWidget(button_delete)
        self.dict_aufgaben_wizard[index] = label

    def delete_example(self, index):
        self.list_of_examples_wizard.pop(index)

        if is_empty(self.list_of_examples_wizard):
            self.pushButton_addto_worksheet_wizard.setEnabled(False)
        self.reset_aufgabenboxes_wizard()


        # columns = self.spinBox_column_wizard.value()
        # for i in range(self.gridLayout_scrollArea_wizard.count()-2): 
        #     self.gridLayout_scrollArea_wizard.itemAt(i).widget().setTitle("TEST")

        # # num_of_examples = 0
        # # for all in self.dict_all_examples_wizard:
        # num_of_examples = len(self.list_of_examples_wizard)

        # items_per_column= num_of_examples/columns
        # column = 0
        # row = 0
        # index = 0
        # # for thema in self.dict_all_examples_wizard:
        # for example in self.list_of_examples_wizard:
        #     self.create_aufgabenbox_wizard(index, example, row, column)
        #     if row+1 < items_per_column:
        #         row +=1
        #     else:
        #         row +=1
        #         self.gridLayout_scrollArea_wizard.setColumnStretch(row, 1)
        #         self.gridLayout_scrollArea_wizard.setRowStretch(row, 1)
        #         row = 0
        #         column +=1
        #     index +=1
        # print(self.list_of_examples_wizard[index])

    def create_single_example_wizard(self):
        thema = self.comboBox_themen_wizard.currentText()
        minimum = self.spinbox_zahlenbereich_minimum.value()
        maximum = self.spinbox_zahlenbereich_maximum.value()
        commas = self.spinbox_kommastellen_wizard.value()
        

        if thema == 'Addition':
            anzahl_summanden = self.spinBox_zahlenbereich_anzahl_wizard.value()
            smaller_or_equal = self.combobox_kommastellen_wizard.currentIndex()
            new_example = create_single_example_addition(minimum, maximum, commas, anzahl_summanden, smaller_or_equal)
        elif thema == 'Subtraktion':
            anzahl_subtrahenden = self.spinBox_zahlenbereich_anzahl_wizard.value()
            smaller_or_equal = self.combobox_kommastellen_wizard.currentIndex()
            new_example = create_single_example_subtraction(minimum, maximum, commas, self.checkbox_negative_ergebnisse_wizard.isChecked(),anzahl_subtrahenden ,smaller_or_equal)
        elif thema == 'Multiplikation':
            minimum_1 = self.spinBox_first_number_min.value()
            maximum_1 = self.spinBox_first_number_max.value()
            commas_1 = self.spinBox_first_number_decimal.value()
            smaller_or_equal_1 = self.combobox_first_number_decimal.currentIndex()
            minimum_2 = self.spinBox_second_number_min.value()
            maximum_2 = self.spinBox_second_number_max.value()
            commas_2 = self.spinBox_second_number_decimal.value()
            smaller_or_equal_2 = self.combobox_second_number_decimal.currentIndex()
            new_example = create_single_example_multiplication(minimum_1, maximum_1, commas_1, smaller_or_equal_1,minimum_2, maximum_2, commas_2, smaller_or_equal_2)
        elif thema == themen_worksheet_wizard[3]:
            minimum_1 = self.spinbox_dividend_min_wizard.value()
            maximum_1 = self.spinbox_dividend_max_wizard.value()
            minimum_2 = self.spinbox_divisor_min_wizard.value()
            maximum_2 = self.spinbox_divisor_max_wizard.value()
            commas_div = self.spinBox_divisor_kommastellen_wizard.value()
            commas_result = self.spinbox_ergebnis_kommastellen_wizard.value()
            smaller_or_equal_div = self.combobox_divisor_kommastelle_wizard.currentIndex()
            smaller_or_equal_result = self.combobox_ergebnis_kommastellen_wizard.currentIndex()


            if self.combobox_dividend_wizard.currentIndex()==1:
                output_type = 2    
            elif self.radioButton_division_ohne_rest.isChecked():
                output_type = 0
            elif self.radioButton_division_rest.isChecked():
                output_type = 1

            new_example = create_single_example_division(minimum_1, maximum_1, minimum_2, maximum_2, commas_div, smaller_or_equal_div, commas_result, smaller_or_equal_result, output_type)

        elif thema == themen_worksheet_wizard[4] or thema == themen_worksheet_wizard[5] or thema == themen_worksheet_wizard[6] or thema == themen_worksheet_wizard[7]:
            minimum = self.spinbox_zahlenbereich_minimum.value()
            maximum = self.spinbox_zahlenbereich_maximum.value()
            commas = self.spinbox_kommastellen_wizard.value()
            smaller_or_equal = self.combobox_kommastellen_wizard.currentIndex()
            anzahl_summanden = self.spinBox_zahlenbereich_anzahl_wizard.value()
            brackets_allowed = self.checkbox_allow_brackets_wizard.isChecked()

            if thema == themen_worksheet_wizard[5]:
                new_example = create_single_example_ganze_zahlen_strich(minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed)
            elif thema == themen_worksheet_wizard[6]:
                new_example = create_single_example_ganze_zahlen_punkt(minimum, maximum, commas, anzahl_summanden, smaller_or_equal)
            elif thema == themen_worksheet_wizard[4] or thema == themen_worksheet_wizard[7]:
                if thema == themen_worksheet_wizard[4]:
                    show_brackets = False
                else:
                    show_brackets = True
                new_example = create_single_example_ganze_zahlen_grundrechnungsarten(minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed, show_brackets)

        return new_example

    def reload_example(self, index):  
        new_example = self.create_single_example_wizard()
        # result = self.list_of_examples_wizard[index][-2]

        # if self.checkBox_show_nonogramm.isChecked():
        #     for key, value in self.coordinates_nonogramm_wizard.items():
        #         if value == result:
        #             self.coordinates_nonogramm_wizard[key]=new_example[-2]
        #             break

        self.list_of_examples_wizard[index] = new_example
        self.dict_aufgaben_wizard[index].setText(new_example[-1])





    def reset_aufgabenboxes_wizard(self):
        columns = self.spinBox_column_wizard.value()
        for i in reversed(range(self.gridLayout_scrollArea_wizard.count())): 
            self.gridLayout_scrollArea_wizard.itemAt(i).widget().setParent(None)

        # num_of_examples = 0
        # for all in self.dict_all_examples_wizard:
        try:
            num_of_examples = len(self.list_of_examples_wizard)
        except AttributeError:
            self.list_of_examples_wizard = []
            num_of_examples = len(self.list_of_examples_wizard)



        items_per_column= num_of_examples/columns
        column = 0
        row = 0
        index = 0
        # for thema in self.dict_all_examples_wizard:
        for example in self.list_of_examples_wizard:
            self.create_aufgabenbox_wizard(index, example, row, column)
            if row+1 < items_per_column:
                row +=1
            else:
                row +=1
                self.gridLayout_scrollArea_wizard.setColumnStretch(row, 1)
                self.gridLayout_scrollArea_wizard.setRowStretch(row, 1)
                row = 0
                column +=1
            index +=1


        # pushButton_create_new_example = create_new_button(
        #     self.scrollAreaWidgetContents_wizard,
        #     "Neue Aufgabe hinzufügen",
        #     self.add_new_example,
        #     icon = "plus-square.svg"
        #     )
        # self.gridLayout_scrollArea_wizard.addWidget(pushButton_create_new_example ,row,column,1,1)

    def create_list_of_examples_wizard(self):
        thema = self.comboBox_themen_wizard.currentText()
        examples = self.spinBox_number_wizard.value()

        if thema == 'Addition':
            minimum = self.spinbox_zahlenbereich_minimum.value()
            maximum = self.spinbox_zahlenbereich_maximum.value()
            commas = self.spinbox_kommastellen_wizard.value()
            smaller_or_equal = self.combobox_kommastellen_wizard.currentIndex()
            anzahl_summanden = self.spinBox_zahlenbereich_anzahl_wizard.value()
            if minimum>maximum:
                critical_window('Das Maximum muss größer als das Minimum sein.')
                return
            list_of_examples_wizard = create_list_of_examples_addition(examples, minimum, maximum, commas, anzahl_summanden, smaller_or_equal)

        elif thema == 'Subtraktion':
            minimum = self.spinbox_zahlenbereich_minimum.value()
            maximum = self.spinbox_zahlenbereich_maximum.value()
            commas = self.spinbox_kommastellen_wizard.value()
            anzahl_subtrahenden = self.spinBox_zahlenbereich_anzahl_wizard.value()
            smaller_or_equal = self.combobox_kommastellen_wizard.currentIndex()
            if minimum>maximum:
                warning_window('Das Maximum muss größer als das Minimum sein.')
                return
            list_of_examples_wizard = create_list_of_examples_subtraction(examples, minimum, maximum, commas, self.checkbox_negative_ergebnisse_wizard.isChecked(), anzahl_subtrahenden,smaller_or_equal)
        
        elif thema == 'Multiplikation':
            minimum_1 = self.spinBox_first_number_min.value()
            maximum_1 = self.spinBox_first_number_max.value()
            commas_1 = self.spinBox_first_number_decimal.value()
            smaller_or_equal_1 = self.combobox_first_number_decimal.currentIndex()
            minimum_2 = self.spinBox_second_number_min.value()
            maximum_2 = self.spinBox_second_number_max.value()
            commas_2 = self.spinBox_second_number_decimal.value()
            smaller_or_equal_2 = self.combobox_second_number_decimal.currentIndex()
            list_of_examples_wizard = create_list_of_examples_multiplication(examples, minimum_1, maximum_1, commas_1, smaller_or_equal_1 ,minimum_2, maximum_2, commas_2, smaller_or_equal_2)

        elif thema == "Division":
            minimum_1 = self.spinbox_dividend_min_wizard.value()
            maximum_1 = self.spinbox_dividend_max_wizard.value()
            minimum_2 = self.spinbox_divisor_min_wizard.value()
            maximum_2 = self.spinbox_divisor_max_wizard.value()
            commas_div = self.spinBox_divisor_kommastellen_wizard.value()
            smaller_or_equal_div = self.combobox_divisor_kommastelle_wizard.currentIndex()
            commas_result = self.spinbox_ergebnis_kommastellen_wizard.value()
            smaller_or_equal_result = self.combobox_ergebnis_kommastellen_wizard.currentIndex()
            if self.combobox_dividend_wizard.currentIndex()==1:
                output_type = 2    
            elif self.radioButton_division_ohne_rest.isChecked():
                output_type = 0
            elif self.radioButton_division_rest.isChecked():
                output_type = 1           

            list_of_examples_wizard = create_list_of_examples_division(examples, minimum_1, maximum_1, minimum_2, maximum_2, commas_div, smaller_or_equal_div,commas_result,smaller_or_equal_result, output_type)  

        elif thema == themen_worksheet_wizard[4] or thema == themen_worksheet_wizard[5] or thema == themen_worksheet_wizard[6] or thema == themen_worksheet_wizard[7]:
            minimum = self.spinbox_zahlenbereich_minimum.value()
            maximum = self.spinbox_zahlenbereich_maximum.value()
            commas = self.spinbox_kommastellen_wizard.value()
            smaller_or_equal = self.combobox_kommastellen_wizard.currentIndex()
            anzahl_summanden = self.spinBox_zahlenbereich_anzahl_wizard.value()
            brackets_allowed = self.checkbox_allow_brackets_wizard.isChecked()
            show_brackets = True
            if thema == themen_worksheet_wizard[5]:
                typ = 'strich'
            elif thema == themen_worksheet_wizard[6]:
                typ = 'punkt'
            elif thema == themen_worksheet_wizard[4] or thema == themen_worksheet_wizard[7]:
                if thema == themen_worksheet_wizard[4]:
                    show_brackets = False
                typ = 'grundrechnungsarten'

            if minimum>maximum:
                critical_window('Das Maximum muss größer als das Minimum sein.')
                return
            list_of_examples_wizard = create_list_of_examples_ganze_zahlen(typ, examples, minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed, show_brackets)        

        return list_of_examples_wizard

    def get_all_examples_wizard(self):
        list_of_examples = []
        for thema in self.dict_all_examples_wizard:
            for item in self.dict_all_examples_wizard[thema]:
                list_of_examples.append(item)
        return list_of_examples 

    def create_nonogramm_wizard(self):
        list_of_examples = self.get_all_examples_wizard()

        max_pixels = get_max_pixels_nonogram()
        if len(list_of_examples) > max_pixels:
            warning_window("Die maximale Anzahl der Aufgaben zur Verwendung der Selbstkontrolle wurde überschritten ({0}|{1}).".format(len(list_of_examples), max_pixels),
            "Reduzieren Sie die Anzahl der Aufgaben, um die Selbstkontrolle verwenden zu können.")
            self.checkBox_show_nonogramm.setChecked(False)
            self.groupBox_show_nonogramm.setEnabled(False)

        else: 
            self.chosen_nonogram, self.solution_pixel = get_all_solution_pixels(list_of_examples, self.combobox_nonogramm_wizard.currentText())


    def create_new_worksheet_wizard_pressed(self):
        self.pushButton_addto_worksheet_wizard.setEnabled(True)
        self.worksheet_edited = True

        # self.worksheet_wizard_changed = False

        # self.dict_all_examples_wizard = {}
        self.list_of_examples_wizard = self.create_list_of_examples_wizard()

        # self.dict_all_examples_wizard[thema] = list_of_examples_wizard
        # print(self.list_of_examples_wizard)
        
        # return
        # print(self.dict_all_examples_wizard)

        self.reset_aufgabenboxes_wizard()


        # if self.checkBox_show_nonogramm.isChecked():
        #     self.create_nonogramm_wizard()  


        # if self.checkBox_show_nonogramm.isChecked():
        #     self.chosen_nonogram, solution_pixel = get_all_solution_pixels(self.list_of_examples_wizard, self.combobox_nonogramm_wizard.currentText())

        #     self.coordinates_nonogramm_wizard = create_coordinates(self, solution_pixel)


    def add_single_example_wizard(self):
        self.pushButton_addto_worksheet_wizard.setEnabled(True)
        new_example = self.create_single_example_wizard()

        self.list_of_examples_wizard.append(new_example)

        self.reset_aufgabenboxes_wizard()
        # self.dict_aufgaben_wizard[index].setText(new_example[-1])

    def edit_set_of_examples_wizard(self, widget, thema):
        self.pushButton_addto_worksheet_wizard.setEnabled(True)
        if not is_empty(self.list_of_examples_wizard):
            rsp = question_window("Es befinden sich nicht gespeicherte Aufgaben im Bearbeitungsbereich. Sind Sie sicher, dass Sie diese unwiderruflich läschen möchten?")
            if rsp == False:
                return

        self.list_of_examples_wizard = self.dict_all_examples_worksheet_wizard[widget]['list_of_examples']

        self.reset_aufgabenboxes_wizard()

        self.spinBox_number_wizard.setValue(len(self.list_of_examples_wizard))

        self.spinBox_column_wizard.setValue(self.dict_all_examples_worksheet_wizard[widget]['spalten'])

        if self.dict_all_examples_worksheet_wizard[widget]['ausrichtung'] != None:
            self.combobox_ausrichtung_wizard.setCurrentIndex(self.dict_all_examples_worksheet_wizard[widget]['ausrichtung'])
        
        self.comboBox_themen_wizard.setCurrentText(thema)
        del self.dict_all_examples_worksheet_wizard[widget]
        widget.setParent(None)

        self.adapt_nonogramm_selection()

    def delete_set_of_examples_wizard(self, widget):
        rsp = question_window("Sind Sie sicher, dass Sie die Aufgaben vom Arbeitsblatt entfernen wollen?")
        
        if rsp == False:
            return

        widget.setParent(None)
        del self.dict_all_examples_worksheet_wizard[widget]

        self.adapt_nonogramm_selection()


    def get_total_number_of_examples_wizard(self):
        total = 0
        for all in self.dict_all_examples_worksheet_wizard.values():
            total += len(all['list_of_examples'])

        return total


    def adapt_nonogramm_selection(self):
        maximum = get_max_pixels_nonogram()
        num_of_examples = self.get_total_number_of_examples_wizard()

        
        if num_of_examples >maximum:
            self.checkBox_show_nonogramm.setChecked(False)
            self.widget_show_nonogramm.setEnabled(False)
            # self.checkBox_show_nonogramm.setEnabled(False)
            # self.combobox_nonogramm_wizard.setEnabled(False)
        else:
            self.widget_show_nonogramm.setEnabled(True)
            # self.checkBox_show_nonogramm.setChecked(True)
            # self.checkBox_show_nonogramm.setEnabled(True)
            # self.combobox_nonogramm_wizard.setEnabled(True)

        
        auswahl = self.combobox_nonogramm_wizard.currentText()
        self.combobox_nonogramm_wizard.clear()

        
        add_new_option(self.combobox_nonogramm_wizard, 0, 'Zufällig')
        i=1
        for all in all_nonogramms:
            if len(all_nonogramms[all])>= num_of_examples:
                add_new_option(self.combobox_nonogramm_wizard, i, "{0} ({1})".format(all.capitalize(), len(all_nonogramms[all])))
                i+=1 

        self.combobox_nonogramm_wizard.setCurrentText(auswahl)


    def add_to_worksheet_wizard(self):
        self.pushButton_addto_worksheet_wizard.setEnabled(False)


        widget_worksheet = DragDropGroupBox(self, None)
        widget_worksheet.setParent(self.scrollAreaWidgetContents_complete_worksheet_wizard)
        self.verticalLayout_complete_worksheet_wizard.insertWidget(self.verticalLayout_complete_worksheet_wizard.count() - 1, widget_worksheet)

        horizontalLayout_worksheet = create_new_horizontallayout(widget_worksheet)
        horizontalLayout_worksheet.setContentsMargins(0,5,0,5)

        thema = self.comboBox_themen_wizard.currentText()
        anzahl = len(self.list_of_examples_wizard)

        label_worksheet = create_new_label(self.scrollAreaWidgetContents_complete_worksheet_wizard, f"{thema} ({anzahl})", True)
        horizontalLayout_worksheet.addWidget(label_worksheet)

        horizontalLayout_worksheet.addStretch()
        pushButton_edit = create_new_button(self.scrollAreaWidgetContents_complete_worksheet_wizard, "", partial(self.edit_set_of_examples_wizard, widget_worksheet, thema), icon="edit.svg")
        pushButton_edit.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        horizontalLayout_worksheet.addWidget(pushButton_edit)

        pushButton_delete = create_new_button(self.scrollAreaWidgetContents_complete_worksheet_wizard, "", partial(self.delete_set_of_examples_wizard,widget_worksheet), icon="trash-2.svg")
        pushButton_delete.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        horizontalLayout_worksheet.addWidget(pushButton_delete)        

        for all in self.list_of_examples_wizard:
            try:
                tooltip_str += f"\n{all[-1]}"
            except UnboundLocalError:
                tooltip_str = all[-1]

        widget_worksheet.setToolTip(tooltip_str)


        list_solutions =  []
        for all in self.list_of_examples_wizard:
            list_solutions.append(all[-2])

        list_dummy_solutions = []
        i=0
        while i<10:
            dummy_solution = get_random_solution(self, thema)
            if dummy_solution[-2] not in list_solutions:
                list_dummy_solutions.append(dummy_solution)
                i+=1


        if self.comboBox_themen_wizard.currentIndex() == 0 or self.comboBox_themen_wizard.currentIndex() == 1:
            ausrichtung = self.combobox_ausrichtung_wizard.currentIndex()
        
        else:
            ausrichtung = None
        try:
            self.dict_all_examples_worksheet_wizard[widget_worksheet] = {
                'index_thema' : self.comboBox_themen_wizard.currentIndex(),
                'spalten' : self.spinBox_column_wizard.value(),
                'ausrichtung': ausrichtung,
                'list_of_examples' : self.list_of_examples_wizard,
                'dummy_examples' : list_dummy_solutions,
            }

        except AttributeError:
            self.dict_all_examples_worksheet_wizard = {}
            self.dict_all_examples_worksheet_wizard[widget_worksheet] = {
                'index_thema' : self.comboBox_themen_wizard.currentIndex(),
                'spalten' : self.spinBox_column_wizard.value(),
                'ausrichtung': ausrichtung,
                'list_of_examples' : self.list_of_examples_wizard,
                'dummy_examples' : list_dummy_solutions,
            }
        self.list_of_examples_wizard = []

        self.reset_aufgabenboxes_wizard()

        
        self.adapt_nonogramm_selection()



    def create_latex_file_content_wizard(self):
        total_list_of_examples = []
        # print(self.dict_all_examples_worksheet_wizard)



        # print(order_of_examples)
        # for widget in order_of_examples:
        #     set_of_examples = self.dict_all_examples_worksheet_wizard[widget]    
            # print(set_of_examples)
        for all in self.dict_all_examples_worksheet_wizard.values():
            for item in all['list_of_examples']:
                total_list_of_examples.append(item)



        if self.checkBox_show_nonogramm.isChecked():
            nonogram, solution_pixels = get_all_solution_pixels(total_list_of_examples, self.combobox_nonogramm_wizard.currentText())


            all_shuffeled_coordinates = create_coordinates(solution_pixels, self.dict_all_examples_worksheet_wizard)


        titel = self.lineEdit_titel_wizard.text()

        try: 
            if self.show_instructions_wizard == True:
                try:
                    arbeitsanweisung = self.instructions_wizard
                except AttributeError:
                    arbeitsanweisung = "Berechne die folgenden Aufgaben"
            else:
                arbeitsanweisung = False
        except AttributeError:
            arbeitsanweisung = False



        # columns = self.spinBox_column_wizard.value()
        if self.combobox_nummerierung_wizard.currentText() == '-':
            nummerierung = "label={}"
        else:
            nummerierung = self.combobox_nummerierung_wizard.currentText()

        index = self.comboBox_themen_wizard.currentIndex()

        order_of_examples = []
        for i in range(self.verticalLayout_complete_worksheet_wizard.count()):
            if self.verticalLayout_complete_worksheet_wizard.itemAt(i).widget() != None:
                order_of_examples.append(self.verticalLayout_complete_worksheet_wizard.itemAt(i).widget())


        content = create_latex_worksheet(
            order_of_examples,
            self.dict_all_examples_worksheet_wizard,
            index ,titel, arbeitsanweisung, nummerierung,
            self.comboBox_solution_type_wizard.currentIndex(),
            )

        if self.checkBox_show_nonogramm.isChecked():
            content += create_nonogramm(nonogram, all_shuffeled_coordinates)

        return content


    def get_content_worksheet_wizard(self):
        try:
            if is_empty(self.list_of_examples_wizard)==False:
                rsp = question_window("Es existieren temporäre Aufgaben, die nicht zum Arbeitsblatt hinzugefügt wurden.", 
                "Möchten Sie diese Aufgaben zum Arbeitsblatt hizufügen?",
                titel= "Temporäre Aufgaben zum Arbeitsblatt hinzufügen?")

                if rsp == True:
                    self.add_to_worksheet_wizard()

        except AttributeError:
            warning_window("Es wurden keine Aufgaben zum Arbeitsblatt hinzugefügt.")
            return


        try:
            if is_empty(self.dict_all_examples_worksheet_wizard):
                warning_window("Es wurden keine Aufgaben zum Arbeitsblatt hinzugefügt.")
                return
        except AttributeError:
            warning_window("Es wurden keine Aufgaben zum Arbeitsblatt hinzugefügt.")
            return

        content = self.create_latex_file_content_wizard()

        return content


    def create_vorschau_worksheet_wizard(self):
        
        content = self.get_content_worksheet_wizard()

        if content == None:
            return


        path_file = os.path.join(
            path_localappdata_lama, "Teildokument", "worksheet.tex"
            )

        if self.checkbox_solutions_wizard.isChecked() == True:
            show_solution = "solution_on"
        else:
            show_solution = "solution_off"

        try:
            if self.checkBox_show_pagenumbers_wizard == True:
                pagestyle = 'plain'
            else:
                pagestyle = 'empty'
        except AttributeError:
            pagestyle = 'empty'
        # return
        with open(path_file, "w", encoding="utf8") as file:
            file.write(tex_preamble(solution=show_solution, pagestyle=pagestyle, font_size=self.combobox_fontsize_wizard.currentText(), documentclass='extarticle'))

            file.write(content)

            file.write(tex_end)


        create_pdf("worksheet")



    def edit_worksheet_instructions(self):
        Dialog = QtWidgets.QDialog(
            None,
            QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint,
        )
        ui = Ui_Dialog_edit_worksheet_instructions()

        try:
            text = self.instructions_wizard
        except AttributeError:
            text = "Berechne die folgenden Aufgaben"

        try:
            show_instructions = self.show_instructions_wizard
        except AttributeError:
            show_instructions = True


        try:
            show_pagenumbers = self.checkBox_show_pagenumbers_wizard
        except AttributeError:
            show_pagenumbers = False
        ui.setupUi(Dialog, text, show_instructions, show_pagenumbers)

        rsp = Dialog.exec()
        if rsp == QtWidgets.QDialog.Accepted:
            self.show_instructions_wizard = ui.checkBox_hide_instructions.isChecked()
            self.instructions_wizard = ui.plainTextEdit_instructions.toPlainText()
            self.checkBox_show_pagenumbers_wizard = ui.checkBox_show_pagenumbers.isChecked()


    def save_worksheet_wizard(self):
        content = self.get_content_worksheet_wizard()
    

        if content == None:
            return
        # content = self.create_latex_file_content_wizard()
        # try:
        #     self.list_of_examples_wizard 
        # except AttributeError:
        #     self.create_worksheet_wizard_pressed()


        # titel = self.lineEdit_titel_wizard.text()
        # columns = self.spinBox_column_wizard.value()
        # if self.combobox_nummerierung_wizard.currentText() == '-':
        #     nummerierung = "label={}"
        # else:
        #     nummerierung = self.combobox_nummerierung_wizard.currentText()
        # ausrichtung = self.combobox_ausrichtung_wizard.currentIndex()
        # index = self.comboBox_themen_wizard.currentIndex()

        # content = create_latex_worksheet(self.list_of_examples_wizard, index ,titel, columns, nummerierung, ausrichtung, self.comboBox_solution_type_wizard.currentIndex())

        # if self.checkBox_show_nonogramm.isChecked():
        #     content += create_nonogramm(self.coordinates_nonogramm_wizard)

        try:
            self.saved_file_path
        except AttributeError:
            self.saved_file_path = path_home
        path_file = self.get_saving_path()
        if path_file == None:
            return

        index = 0
        for show_solution in ["solution_on", "solution_off"]:
            with open(path_file, "w", encoding="utf8") as file:
                file.write(tex_preamble(solution=show_solution, pagestyle='empty', font_size=self.combobox_fontsize_wizard.currentText(), documentclass='extarticle'))

                file.write(content)

                file.write(tex_end)


            name, extension = os.path.splitext(path_file)


            create_pdf(name, index, 2)
            
            temp_filename = name + ".pdf"
            if index == 0:
                new_filename = name + "_Loesung.pdf"

                shutil.move(temp_filename, new_filename)

            elif index ==1:
                self.reset_latex_file_to_start(path_file)

            index +=1


        if sys.platform.startswith("linux"):
            path_file = os.path.dirname(path_file)
            subprocess.Popen('xdg-open "{}"'.format(path_file), shell=True)
        elif sys.platform.startswith("darwin"):
            path_file = os.path.dirname(path_file)
            subprocess.Popen('open "{}"'.format(path_file), shell=True)
        else:
            path_file = os.path.dirname(path_file).replace("/", "\\")
            subprocess.Popen('explorer "{}"'.format(path_file))
        # return
    

    def image_clean_up(self):
        image_folder = os.path.join(path_database, "Bilder")

        table_lama = _database.table('table_lama_1')
        _file_ = Query()        

        def test_func(value, image):
            if image in value:
                return True
            else:
                return False

        list_unused_images = []

        for image in os.listdir(image_folder):
            table_lama = _database.table('table_lama_1')
            _file_ = Query() 
            _list = table_lama.search(_file_.bilder.test(test_func, image))

            if is_empty(_list):
                table_lama = _database.table('table_lama_2')
                _file_ = Query() 
                _list = table_lama.search(_file_.bilder.test(test_func, image))
            
            if is_empty(_list):
                table_lama = _database.table('table_cria')
                _file_ = Query() 
                _list = table_lama.search(_file_.bilder.test(test_func, image))                

            if is_empty(_list):
                list_unused_images.append(image)

            self.progress_cleanup_value += 1
            self.progress_cleanup.setValue(self.progress_cleanup_value)


        return list_unused_images
            


    def database_clean_up(self):
        refresh_ddb(self, auto_update=True)


        image_folder = os.path.join(path_database, "Bilder")
        progress_maximum = len(dict_gk) + len(os.listdir(image_folder)) + 2

        self.progress_cleanup_value = 0
        self.progress_cleanup = QtWidgets.QProgressDialog("Fehlerbericht wird erstellt ...", "",self.progress_cleanup_value,progress_maximum)
        self.progress_cleanup.setFixedSize(self.progress_cleanup.sizeHint())
        self.progress_cleanup.setWindowTitle("Lade...")
        self.progress_cleanup.setWindowFlags(QtCore.Qt.WindowTitleHint)
        self.progress_cleanup.setWindowIcon(QtGui.QIcon(logo_path))
        self.progress_cleanup.setCancelButton(None)
        self.progress_cleanup.setWindowModality(Qt.WindowModal)

        self.dict_missing_files = self.file_clean_up()
        list_unused_images = self.image_clean_up()
        self.dict_missing_files['Nicht verwendete Bilder'] = list_unused_images

        self.progress_cleanup.cancel()



        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        report = os.path.join(path_localappdata_lama, "Teildokument", "Fehlerbericht.txt")

        with open(report, "w+", encoding="utf8") as f:
            f.write("Fehlende Typ 1 Aufgaben:\n")
            for all in self.dict_missing_files["Typ1 Aufgaben"]:
                f.write("{}\n".format(all))
            f.write("Fehlende Typ 2 Aufgaben:\n")
            for all in self.dict_missing_files["Typ2 Aufgaben"]:
                f.write("{}\n".format(all))
            f.write("Fehlende Unterstufen Aufgaben:\n")
            for all in self.dict_missing_files["Unterstufen Aufgaben"]:
                f.write("{}\n".format(all))
            f.write("Nicht verwendete Bilder:\n")
            for all in self.dict_missing_files["Nicht verwendete Bilder"]:
                f.write("{}\n".format(all))


        if sys.platform.startswith("linux"):
            subprocess.Popen('xdg-open "{}"'.format(report), shell=True)
        elif sys.platform.startswith("darwin"):
            subprocess.Popen('open "{}"'.format(report), shell=True)
        else:
            subprocess.Popen('"{}"'.format(report), shell = True)

        QtWidgets.QApplication.restoreOverrideCursor()


    def enable_widgets_editor(self, enabled):
        self.groupBox_ausgew_gk_cr.setEnabled(enabled)
        self.groupBox_titel_cr.setEnabled(enabled)
        self.groupBox_grundkompetenzen_cr.setEnabled(enabled)
        self.groupBox_bilder.setEnabled(enabled)
        self.groupBox_punkte.setEnabled(enabled)
        self.groupBox_klassen_cr.setEnabled(enabled)
        self.groupBox_aufgabenformat.setEnabled(enabled)
        self.groupBox_beispieleingabe.setEnabled(enabled)
        self.groupBox_quelle.setEnabled(enabled)
        self.pushButton_save_edit.setEnabled(enabled)
        self.pushButton_vorschau_edit.setEnabled(enabled)
        self.pushButton_save_as_variation_edit.setEnabled(enabled)
        self.pushButton_delete_file.setEnabled(enabled)
        self.cb_matura_tag.setEnabled(enabled)
        self.cb_no_grade_tag.setEnabled(enabled)
        self.groupBox_aufgabentyp.setEnabled(enabled)
        self.groupBox_themengebiete_cria.setEnabled(enabled)
        self.groupBox_abstand.setEnabled(enabled)
        self.groupBox_pagebreak.setEnabled(enabled)
        self.button_language.setEnabled(enabled)

    def action_add_file(self):
        self.update_gui("widgets_create")
        self.suchfenster_reset()
        self.reset_variation()
        self.enable_widgets_editor(True)

    def action_edit_files(self):
        self.update_gui("widgets_edit")
        # try:
        #     if self.chosen_file_to_edit == None:
        #         self.enable_widgets_editor(False)
        # except AttributeError:
        #     self.enable_widgets_editor(False)
        self.suchfenster_reset()
        self.reset_edit_file()
        # self.enable_widgets_editor(False)

    def check_if_file_exists(self, aufgabe):  # aufgabe
        typ = get_aufgabentyp(self.chosen_program, aufgabe)

        if typ == 1:
            list_paths = self.beispieldaten_dateipfad_1.values()
        if typ == 2:
            list_paths = self.beispieldaten_dateipfad_2.values()
        if typ == None:
            list_paths = self.beispieldaten_dateipfad_cria.values()
            klasse, aufgabe = self.split_klasse_aufgabe(aufgabe)

        name = aufgabe + ".tex"

        if typ == None:
            for path in list_paths:
                if klasse.lower() in path.lower():
                    if name == os.path.basename(path):
                        file_found = True
                        return file_found
                    else:
                        pass
            file_found = False
            return file_found

        else:
            if any(name == os.path.basename(path) for path in list_paths):
                file_found = True
            else:
                file_found = False
            return file_found

    def load_file(self, path):
        try:
            with open(path, "r", encoding="utf8") as loaded_file:
                loaded_file = json.load(loaded_file)
            return loaded_file
        except json.decoder.JSONDecodeError:
            return

    def update_label_restore_action(self):
        try:
            autosave_file = os.path.join(
                path_localappdata_lama, "Teildokument", "autosave.lama"
            )

            save_time = modification_date(autosave_file).strftime("%d.%m.%Y %H:%M")

            self.actionRestore_sage.setText("Backup ({})".format(save_time))
            self.actionRestore_sage.setEnabled(True)
        except FileNotFoundError:
            self.actionRestore_sage.setText("Backup")
            self.actionRestore_sage.setEnabled(False)

    
    def sage_load_files(self):
        list_aufgaben_errors = []

        for i in reversed(range(0, self.verticalLayout_scrollArea_sage_typ1.count())):
            self.delete_widget(self.verticalLayout_scrollArea_sage_typ1, i)

        for i in reversed(range(0, self.verticalLayout_scrollArea_sage_typ2.count())):
            self.delete_widget(self.verticalLayout_scrollArea_sage_typ2, i)
        self.scrollAreaWidgetContents_typ2.hide()

        # typ = get_aufgabentyp(self.chosen_program, aufgabe)        
        # if typ == 2:
        #     list_index = 1
        #     layout = self.verticalLayout_scrollArea_sage_typ2
        # else:
        #     list_index = 0
        #     layout = self.verticalLayout_scrollArea_sage_typ1

        for list_index in [0,1]:
            if list_index == 0:
                layout = self.verticalLayout_scrollArea_sage_typ1
            elif list_index == 1:
                if not is_empty(self.list_alle_aufgaben_sage[1]):
                    self.scrollAreaWidgetContents_typ2.show()
                layout = self.verticalLayout_scrollArea_sage_typ2    
            for index, aufgabe in enumerate(self.list_alle_aufgaben_sage[list_index]):
                typ = get_aufgabentyp(self.chosen_program, aufgabe)

                aufgabe_total = get_aufgabe_total(aufgabe.replace(" (lokal)", ""), typ)
                if aufgabe_total == None:
                    list_aufgaben_errors.append(aufgabe)
                    continue

                neue_aufgaben_box = self.create_neue_aufgaben_box(
                    index, aufgabe, aufgabe_total
                )

                layout.insertWidget(layout.count() - 1, neue_aufgaben_box)
                # layout.addWidget(neue_aufgaben_box)

                self.add_image_path_to_list(aufgabe.replace(" (lokal)", ""))
                self.progress.setValue(index)


        # self.verticalLayout_scrollArea_sage.addStretch()

        self.update_punkte()

        
        return list_aufgaben_errors

     
    @report_exceptions
    def sage_load(self, external_file_loaded=False, autosave=False):
        if external_file_loaded == False and autosave == False:
            try:
                os.path.dirname(self.saved_file_path)
            except AttributeError:
                self.saved_file_path = path_home
            # QtWidgets.QApplication.restoreOverrideCursor()
            path_backup_file = QtWidgets.QFileDialog.getOpenFileName(
                None,
                "Öffnen",
                os.path.dirname(self.saved_file_path),
                "LaMA Datei (*.lama);; Alle Dateien (*.*)",
            )
            if path_backup_file[0] == "":
                return
            self.saved_file_path = path_backup_file[0]

        if external_file_loaded == True:
            self.saved_file_path = loaded_lama_file_path
        elif autosave == True:
            self.saved_file_path = os.path.join(
                path_localappdata_lama, "Teildokument", "autosave.lama"
            )
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        loaded_file = self.load_file(self.saved_file_path)
        QtWidgets.QApplication.restoreOverrideCursor()
        try:
            if self.chosen_program == loaded_file["data_gesamt"]["program"]:
                if self.list_alle_aufgaben_sage !=  [[],[]]:
                    self.reset_sage()
            else:
                response = self.change_program(loaded_file["data_gesamt"]["program"])
                if response == False:
                    QtWidgets.QApplication.restoreOverrideCursor()
                    return
        except KeyError:
            warning_window(
                "Die geöffnete *.lama-Datei ist veraltet und kann nur mit der Version LaMA 1.x geöffnet werden.",
                "Bitte laden Sie eine aktuelle *.lama-Datei oder kontaktieren Sie lama.helpme@gmail.com, wenn Sie Hilfe benötigen.",
            )
            return
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.update_gui("widgets_sage")
        self.dict_all_infos_for_file = self.load_file(self.saved_file_path)


        self.list_alle_aufgaben_sage = self.dict_all_infos_for_file[
            "list_alle_aufgaben"
        ]

        self.spinBox_nummer.setValue(self.dict_all_infos_for_file["data_gesamt"]["#"])
        self.lineEdit_klasse_sage.setText(
            self.dict_all_infos_for_file["data_gesamt"]["Klasse"]
        )

        try:
            index = self.comboBox_pruefungstyp.findText(
                self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"],
                QtCore.Qt.MatchFixedString,
            )
        except KeyError:
            index = 0
        if index >= 0:
            self.comboBox_pruefungstyp.setCurrentIndex(index)

        if self.dict_all_infos_for_file["data_gesamt"]["Beurteilung"] == "ns":
            self.combobox_beurteilung.setCurrentIndex(0)

        elif self.dict_all_infos_for_file["data_gesamt"]["Beurteilung"] == "br":
            self.combobox_beurteilung.setCurrentIndex(1)

        elif self.dict_all_infos_for_file["data_gesamt"]["Beurteilung"] == "none":
            self.combobox_beurteilung.setCurrentIndex(2)

        year = self.dict_all_infos_for_file["data_gesamt"]["Datum"][0]
        month = self.dict_all_infos_for_file["data_gesamt"]["Datum"][1]
        day = self.dict_all_infos_for_file["data_gesamt"]["Datum"][2]
        self.dateEdit.setDate(QtCore.QDate(year, month, day))

        # try:
        #     self.dict_sage_ausgleichspunkte_chosen = self.dict_all_infos_for_file[
        #         "dict_ausgleichspunkte"
        #     ]
        # except KeyError:
        #     self.dict_sage_ausgleichspunkte_chosen = {}

        try:
            self.dict_sage_hide_show_items_chosen = self.dict_all_infos_for_file[
                "dict_hide_show_items"
            ]
        except KeyError:
            self.dict_sage_hide_show_items_chosen = {}

        try:
            self.dict_sage_individual_change = self.dict_all_infos_for_file[
                "dict_individual_change"
            ]
        except KeyError:
            self.dict_sage_individual_change = {}



        self.progress = QtWidgets.QProgressDialog("Prüfung wird geladen ...", "",0,len(self.list_alle_aufgaben_sage)-1)
        self.progress.setWindowTitle("Lade...")
        self.progress.setWindowFlags(QtCore.Qt.WindowTitleHint)
        self.progress.setWindowIcon(QtGui.QIcon(logo_path))
        self.progress.setCancelButton(None)
        self.progress.setWindowModality(Qt.WindowModal)

        # for aufgabe in self.list_alle_aufgaben_sage:
        list_aufgaben_errors = self.sage_load_files()

        self.progress.cancel()



        if not is_empty(list_aufgaben_errors):
            errors = ", ".join(list_aufgaben_errors)
            if len(list_aufgaben_errors)==1:
                _list = ["Aufgabe","konnte","wurde", "wird"]
            else:
                _list = ["Aufgaben","konnten","wurden", "werden"]
            QtWidgets.QApplication.restoreOverrideCursor()
            warning_window(
                "Die {0} {1} {2} nicht gefunden werden, da sie gelöscht oder umbenannt {3}.\nSie {4} daher ignoriert.".format(
                    _list[0], errors, _list[1], _list[2], _list[3]
                )
            )
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))            
            for aufgabe in list_aufgaben_errors:
                self.dict_all_infos_for_file["list_alle_aufgaben"].remove(aufgabe)

     

        self.update_punkte()


        self.spinBox_default_pkt.setValue(
            self.dict_all_infos_for_file["data_gesamt"]["Typ1 Standard"]
        )

        for list_index in [0,1]:
            for aufgabe in self.list_alle_aufgaben_sage[list_index]:
                try:
                    self.dict_variablen_punkte[aufgabe].setValue(
                        self.dict_all_infos_for_file["dict_alle_aufgaben_pkt_abstand"][
                            aufgabe
                        ][0]
                    )
                    self.dict_variablen_abstand[aufgabe].setValue(
                        self.dict_all_infos_for_file["dict_alle_aufgaben_pkt_abstand"][
                            aufgabe
                        ][1]
                    )

                    self.dict_variablen_punkte_halb[aufgabe].setChecked(self.dict_all_infos_for_file["dict_alle_aufgaben_pkt_abstand"][
                            aufgabe
                        ][2])
                except KeyError:
                    pass

        self.spinBox_2.setValue(
            self.dict_all_infos_for_file["data_gesamt"]["Notenschluessel"][0]
        )
        self.spinBox_3.setValue(
            self.dict_all_infos_for_file["data_gesamt"]["Notenschluessel"][1]
        )
        self.spinBox_4.setValue(
            self.dict_all_infos_for_file["data_gesamt"]["Notenschluessel"][2]
        )
        self.spinBox_5.setValue(
            self.dict_all_infos_for_file["data_gesamt"]["Notenschluessel"][3]
        )

        self.no_saved_changes_sage = True
        
        QtWidgets.QApplication.restoreOverrideCursor()

    @report_exceptions
    def sage_save(self, path_create_tex_file=False, autosave=False):  # path_file
        if autosave == False:
            self.update_gui("widgets_sage")
        try:
            self.saved_file_path
        except AttributeError:
            self.saved_file_path = path_home

        if path_create_tex_file == False and autosave == False:
            path_backup_file = QtWidgets.QFileDialog.getSaveFileName(
                None,
                "Speichern unter",
                os.path.dirname(self.saved_file_path),
                "LaMA Datei (*.lama);; Alle Dateien (*.*)",
            )
            if path_backup_file[0] == "":
                return
            self.collect_all_infos_for_creating_file()
            save_file = path_backup_file[0]

        elif autosave != False:
            save_file = autosave

        else:
            name, _ = os.path.splitext(path_create_tex_file)
            path_create_tex_file = name + "_autosave.lama"
            save_file = path_create_tex_file

        if autosave == False:
            self.saved_file_path = save_file
            self.no_saved_changes_sage = True

        with open(save_file, "w+", encoding="utf8") as saved_file:
            json.dump(self.dict_all_infos_for_file, saved_file, ensure_ascii=False)

        if autosave == True:
            self.update_label_restore_action()

    @report_exceptions
    def define_titlepage(self):
        if self.chosen_program == "lama":
            dict_titlepage = self.dict_titlepage
        elif self.chosen_program == "cria":
            dict_titlepage = self.dict_titlepage_cria

        self.Dialog = QtWidgets.QDialog(
            None,
            QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint,
        )
        self.ui = Ui_Dialog_titlepage()
        self.ui.setupUi(self.Dialog, dict_titlepage)
        # self.Dialog.show()
        self.Dialog.exec()

        if self.chosen_program == "lama":
            self.dict_titlepage = dict_titlepage
            titlepage_save = os.path.join(
                path_localappdata_lama, "Teildokument", "titlepage_save"
            )

            if dict_titlepage['hide_all']==True:
                self.combobox_beurteilung.removeItem(self.combobox_beurteilung.findText("Beurteilungsraster"))
            elif self.combobox_beurteilung.findText("Beurteilungsraster") == -1:
                self.combobox_beurteilung.insertItem(1,"Beurteilungsraster")
        if self.chosen_program == "cria":
            self.dict_titlepage_cria = dict_titlepage
            titlepage_save = os.path.join(
                path_localappdata_lama, "Teildokument", "titlepage_save_cria"
            )

        try:
            with open(titlepage_save, "w+", encoding="utf8") as f:
                json.dump(dict_titlepage, f, ensure_ascii=False)
        except FileNotFoundError:
            os.makedirs(os.path.join(path_localappdata_lama, "Teildokument"))
            with open(titlepage_save, "w+", encoding="utf8") as f:
                json.dump(dict_titlepage, f, ensure_ascii=False)

    def notenanzeige_changed(self):
        if self.combobox_beurteilung.currentText() == "Notenschlüssel":
            self.groupBox_beurteilungsraster.hide()
            self.groupBox_notenschl.show()
        if self.combobox_beurteilung.currentText() == "Beurteilungsraster":
            self.groupBox_notenschl.hide()
            self.groupBox_beurteilungsraster.show()
        if self.combobox_beurteilung.currentText() == "keine Auswahl":
            self.groupBox_notenschl.hide()
            self.groupBox_beurteilungsraster.hide()

        self.update_punkte()

    def get_aufgabenverteilung(self):      
        num_typ1 = len(self.list_alle_aufgaben_sage[0])
        num_typ2 = len(self.list_alle_aufgaben_sage[1])
        # for all in self.list_alle_aufgaben_sage:
        #     typ = get_aufgabentyp(self.chosen_program, all)
        #     if typ == 1:
        #         num_typ1 += 1
        #     if typ == 2:
        #         num_typ2 += 1

        return num_typ1, num_typ2

    @report_exceptions
    def sage_aufgabe_add(self, aufgabe):
        # if self.chosen_program == "lama":

        #     old_num_typ1, old_num_typ2 = self.get_aufgabenverteilung()

        #     typ = get_aufgabentyp(self.chosen_program, aufgabe)
        #     if typ == 1:
        #         self.list_alle_aufgaben_sage.insert(old_num_typ1, aufgabe)
        #     if typ == 2:
        #         self.list_alle_aufgaben_sage.append(aufgabe)

        # if self.chosen_program == "cria":
        #     self.list_alle_aufgaben_sage.append(aufgabe)

        typ = get_aufgabentyp(self.chosen_program, aufgabe)

        if typ == 2:
            self.list_alle_aufgaben_sage[1].append(aufgabe)
        else:
            self.list_alle_aufgaben_sage[0].append(aufgabe)


        num_typ1, num_typ2 = self.get_aufgabenverteilung()
        num_total = num_typ1+num_typ2

        if self.chosen_program == "lama":
            label = "Anzahl der Aufgaben: {0}\n(Typ1: {1} / Typ2: {2})".format(
                num_total, num_typ1, num_typ2
            )
        if self.chosen_program == "cria":
            label = "Anzahl der Aufgaben: {0}".format(num_total)

        self.label_gesamtbeispiele.setText(
            _translate(
                "MainWindow",
                label,
                None,
            )
        )

    def adapt_label_gesamtbeispiele(self):
        # list_sage_examples_typ1 = []
        # list_sage_examples_typ2 = []

        # for all in self.list_alle_aufgaben_sage[0]:
        #     list_sage_examples_typ1.append(all)
        
        # for all in self.list_alle_aufgaben_sage[1]:
        #     list_sage_examples_typ2.append(all)

        #     # if re.search("[A-Z]", all) == None:
        #     #     list_sage_examples_typ2.append(all)
        #     # else:
        #     #     list_sage_examples_typ1.append(all)

        # self.list_alle_aufgaben_sage.clear()
        # self.list_alle_aufgaben_sage.extend(list_sage_examples_typ1)
        # self.list_alle_aufgaben_sage.extend(list_sage_examples_typ2)
        # num_typ1 = len(list_sage_examples_typ1)
        # num_typ2 = len(list_sage_examples_typ2)
        # num_total = len(self.list_alle_aufgaben_sage)
        num_typ1, num_typ2 = self.get_aufgabenverteilung()
        num_total = num_typ1+num_typ2


        if self.chosen_program == "lama":
            self.label_gesamtbeispiele.setText(
                _translate(
                    "MainWindow",
                    "Anzahl der Aufgaben: {0}\n(Typ1: {1} / Typ2: {2})".format(
                        num_total, num_typ1, num_typ2
                    ),
                    None,
                )
            )
        if self.chosen_program == "cria":
            self.label_gesamtbeispiele.setText(
                _translate(
                    "MainWindow", "Anzahl der Aufgaben: {0}".format(num_total), None
                )
            )

    @report_exceptions
    def btn_translation_pressed(self, button, aufgabe):
        if button.text() == "DE":
            button.setText("EN")
        else:
            button.setText("DE")
        self.dict_variablen_translation[aufgabe] = button.text()



    def btn_AB_pressed(self, button, aufgabe):
        self.dict_variablen_AB[aufgabe] = button.isChecked()


    @report_exceptions
    def btn_up_pressed(self, aufgabe):
        typ = get_aufgabentyp(self.chosen_program, aufgabe)

        if typ == 2:
            list_index = 1         
        else:
            list_index = 0
        a, b = (
            self.list_alle_aufgaben_sage[list_index].index(aufgabe),
            self.list_alle_aufgaben_sage[list_index].index(aufgabe) - 1,
        )
        self.list_alle_aufgaben_sage[list_index][a], self.list_alle_aufgaben_sage[list_index][b] = (
            self.list_alle_aufgaben_sage[list_index][b],
            self.list_alle_aufgaben_sage[list_index][a],
        )

        self.build_aufgaben_schularbeit(aufgabe)

    @report_exceptions
    def btn_down_pressed(self, aufgabe):
        typ = get_aufgabentyp(self.chosen_program, aufgabe)
        if typ == 2:
            list_index = 1         
        else:
            list_index = 0

        a, b = (
            self.list_alle_aufgaben_sage[list_index].index(aufgabe),
            self.list_alle_aufgaben_sage[list_index].index(aufgabe) + 1,
        )
        self.list_alle_aufgaben_sage[list_index][a], self.list_alle_aufgaben_sage[list_index][b] = (
            self.list_alle_aufgaben_sage[list_index][b],
            self.list_alle_aufgaben_sage[list_index][a],
        )

        self.build_aufgaben_schularbeit(aufgabe)

    def erase_aufgabe(self, aufgabe):
        typ = get_aufgabentyp(self.chosen_program, aufgabe)
        del self.dict_variablen_punkte[aufgabe]
        if typ == 1:
            del self.dict_variablen_punkte_halb[aufgabe]
        del self.dict_variablen_abstand[aufgabe]

        del self.dict_variablen_translation[aufgabe]
        del self.dict_variablen_AB[aufgabe]

        if typ == 2:
            # del self.dict_variablen_label[aufgabe]
            self.list_alle_aufgaben_sage[1].remove(aufgabe)
        else:
            self.list_alle_aufgaben_sage[0].remove(aufgabe)

        # if aufgabe in self.dict_sage_ausgleichspunkte_chosen:
        #     del self.dict_sage_ausgleichspunkte_chosen[aufgabe]
        if aufgabe in self.dict_sage_hide_show_items_chosen:
            del self.dict_sage_hide_show_items_chosen[aufgabe]
        if aufgabe in self.dict_sage_individual_change:
            del self.dict_sage_individual_change[aufgabe]

    @report_exceptions
    def btn_delete_pressed(self, aufgabe):
        try:
            self.dict_sage_individual_change[aufgabe]
            if self.dict_sage_individual_change[aufgabe][0] != None or self.dict_sage_individual_change[aufgabe][1] != None:
                response = question_window(
                    "Diese Aufgabe wurde abgeändert!\n\nWenn Sie diese Aufgabe löschen, werden auch alle Änderungen, die an dieser Aufgabe vorgenommen wurden, gelöscht.",
                    "Sind Sie sicher, dass Sie diese Aufgaben entfernen möchten?",
                    "Aufgabe entfernen?",
                    default="no",
                )
                if response == False:
                    return
        except KeyError:
            pass
        
        typ = get_aufgabentyp(self.chosen_program, aufgabe)
        if typ == 2:
           list_index = 1
           layout = self.verticalLayout_scrollArea_sage_typ2
        else:
            list_index = 0 
            layout = self.verticalLayout_scrollArea_sage_typ1
        index = self.list_alle_aufgaben_sage[list_index].index(aufgabe)

        if index + 1 == len(self.list_alle_aufgaben_sage[list_index]):
            self.delete_widget(layout, index)
            self.erase_aufgabe(aufgabe)

        else:
            self.erase_aufgabe(aufgabe)
            self.build_aufgaben_schularbeit(self.list_alle_aufgaben_sage[list_index][index])

        if is_empty(self.list_alle_aufgaben_sage[1]):
            self.scrollAreaWidgetContents_typ2.hide() 

        self.update_punkte()
        self.button_was_deleted = True

    def spinbox_pkt_changed(self):  # , aufgabe, spinbox_abstand
        self.update_punkte()

    # def checkbox_pkt_changed(self, aufgabe):
    #     if self.dict_variablen_punkte_halb[aufgabe] ==  False:
    #         self.dict_variablen_punkte_halb[aufgabe] = True
    #     else:
    #         self.dict_variablen_punkte_halb[aufgabe] = False


    def spinbox_abstand_changed(self):  # , aufgabe, spinbox_abstand
        # self.dict_alle_aufgaben_sage[aufgabe][1] = spinbox_abstand.value()
        self.update_punkte()

    def change_scrollbar_position(self):
        try:
            if self.button_was_deleted == True:
                self.button_was_deleted = False
                return
        except AttributeError:
            pass

        pos_maximum = self.scrollArea_chosen.verticalScrollBar().maximum()
        height_aufgabe = 110
        _, num_typ2 = self.get_aufgabenverteilung()
        pos_end_typ1 = pos_maximum - height_aufgabe * num_typ2

        if self.listWidget.currentItem() != None:
            aufgabe = self.listWidget.currentItem().text()
            typ = get_aufgabentyp(self.chosen_program, aufgabe)
            if typ == 2 or typ == None:
                self.scrollArea_chosen.verticalScrollBar().setValue(pos_maximum)
            elif typ == 1:
                self.scrollArea_chosen.verticalScrollBar().setValue(pos_end_typ1)
        else:
            self.scrollArea_chosen.verticalScrollBar().setValue(pos_maximum)

    def get_punkteverteilung(self):
        pkt_typ1 = 0
        pkt_typ2 = 0
        gesamtpunkte = 0
        # print(self.dict_variablen_punkte)
        for all in self.dict_variablen_punkte:
            typ = get_aufgabentyp(self.chosen_program, all)
            if typ == None:
                gesamtpunkte += self.dict_variablen_punkte[all].value()
            elif typ == 1:
                pkt_typ1 += self.dict_variablen_punkte[all].value()
                gesamtpunkte += self.dict_variablen_punkte[all].value()
            elif typ == 2:
                pkt_typ2 += self.dict_variablen_punkte[all].value()
                gesamtpunkte += self.dict_variablen_punkte[all].value()

        return [gesamtpunkte, pkt_typ1, pkt_typ2]

    def update_notenschluessel(self):
        gesamtpunkte = self.get_punkteverteilung()[0]

        verteilung_notenschluessel = []
        for g in range(2, 6):
            r = 0
            x = eval("self.spinBox_{}.value()".format(g))
            if gesamtpunkte * x / 100 == int(gesamtpunkte * x / 100):
                verteilung_notenschluessel.append(int(gesamtpunkte * (x / 100)))
            else:
                verteilung_notenschluessel.append(int(gesamtpunkte * (x / 100)) + 1)
            r += 1

        self.label_sg_pkt.setText(
            _translate(
                "MainWindow", "% (ab {})".format(verteilung_notenschluessel[0]), None
            )
        )
        self.label_g_pkt.setText(
            _translate(
                "MainWindow", "% (ab {})".format(verteilung_notenschluessel[1]), None
            )
        )
        self.label_b_pkt.setText(
            _translate(
                "MainWindow", "% (ab {})".format(verteilung_notenschluessel[2]), None
            )
        )
        self.label_g_2_pkt.setText(
            _translate(
                "MainWindow", "% (ab {})".format(verteilung_notenschluessel[3]), None
            )
        )

    # def get_number_ausgleichspunkte_gesamt(self):
    #     number_ausgleichspkt_gesamt = 0
    #     for aufgabe in self.list_alle_aufgaben_sage:
    #         typ = get_aufgabentyp(self.chosen_program, aufgabe)
    #         if typ == 2:
    #             # collect_content(self, aufgabe)
    #             aufgabe_total = get_aufgabe_total(aufgabe, "lama_2")
    #             number = self.count_ausgleichspunkte(aufgabe_total["content"])
    #             number_ausgleichspkt_gesamt += number

    #     return number_ausgleichspkt_gesamt

    def update_beurteilungsraster(self):

        punkteverteilung = self.get_punkteverteilung()
        # number_ausgleichspunkte_gesamt = self.get_number_ausgleichspunkte_gesamt()
        self.label_typ1_pkt.setText("Punkte Typ 1: {}".format(punkteverteilung[1]))
        self.label_typ2_pkt.setText("Punkte Typ 2: {0}".format(punkteverteilung[2]))

    def update_punkte(self):
        gesamtpunkte = self.get_punkteverteilung()[0]
        num_typ1, num_typ2 = self.get_aufgabenverteilung()
        num_total = num_typ1+num_typ2

        if self.combobox_beurteilung.currentText() == "Notenschlüssel":
            self.update_notenschluessel()

        if self.combobox_beurteilung.currentText() == "Beurteilungsraster":
            self.update_beurteilungsraster()

        if self.chosen_program == "cria":
            self.label_gesamtbeispiele.setText(
                "Anzahl der Aufgaben: {0}".format(num_total)
            )
        if self.chosen_program == "lama":
            self.label_gesamtbeispiele.setText(
                "Anzahl der Aufgaben: {0}\n(Typ1: {1} / Typ2: {2})".format(
                    num_total, num_typ1, num_typ2
                )
            )

        self.label_gesamtpunkte.setText(
            _translate("MainWindow", "Gesamtpunkte: %i" % gesamtpunkte, None)
        )
        self.no_saved_changes_sage = False

    def update_default_pkt(self):
        for all in self.dict_variablen_punkte:
            if get_aufgabentyp(self.chosen_program, all) == 1:
                self.dict_variablen_punkte[all].setValue(
                    self.spinBox_default_pkt.value()
                )

    def get_punkte_aufgabe_sage(self, aufgabe):
        return self.dict_variablen_punkte[aufgabe].value()

    def get_abstand_aufgabe_sage(self, aufgabe):
        try:
            return self.dict_variablen_abstand[aufgabe].value()
        except KeyError:
            return 0

    def get_punkte_halb_aufgabe_sage(self, aufgabe):
        typ = get_aufgabentyp(self.chosen_program, aufgabe)
        if typ == 1:
            return self.dict_variablen_punkte_halb[aufgabe].isChecked()
        else:
            return False




    # def count_ausgleichspunkte(self, content):
    #     number = content.count("\ASubitem")
    #     number = number + content.count("\Aitem")
    #     number = number + content.count("fbox{A}")

    #     return number

    def create_neue_aufgaben_box(self, index, aufgabe, aufgabe_total):
        typ = get_aufgabentyp(self.chosen_program, aufgabe)

        num_typ1, _ = self.get_aufgabenverteilung()

        new_groupbox = DragDropGroupBox(self, aufgabe)
        new_groupbox.setParent(self.scrollAreaWidgetContents_typ1)

        if self.chosen_program == "cria":
            if aufgabe_total["klasse"] == None:
                klasse = ""
            else:
                klasse = "{0}. Klasse - ".format(aufgabe_total["klasse"][1])

            # new_groupbox = DragDropGroupBox()
            # new_groupbox.setParent(self.scrollAreaWidgetContents_2)
            new_groupbox.setTitle("{0}. Aufgabe".format(index + 1))
            # new_groupbox = create_new_groupbox(
            #     self.scrollAreaWidgetContents_2, 
            # )
        elif typ == 2:
            num = num_typ1+index+1
            new_groupbox.setTitle(f"{num}. Aufgabe (Typ2)")
            self.dict_widget_variables[f'groupbox_sage_{aufgabe}'] = new_groupbox
        else:
            new_groupbox.setTitle(f"{index+1}. Aufgabe (Typ1)")
            # new_groupbox = create_new_groupbox(
            #     self.scrollAreaWidgetContents_2,
            #     "{0}. Aufgabe (Typ{1})".format(index + 1, typ),
            # )

        gridLayout_gB = QtWidgets.QGridLayout(new_groupbox)
        gridLayout_gB.setObjectName("gridLayout_gB")

        if typ == None:
            aufgabenformat = " (" + aufgabe_total["af"].upper() + ")"

            label = "{0}{1}{2}".format(klasse, aufgabe, aufgabenformat)

        elif typ == 1:
            aufgabenformat = " (" + aufgabe_total["af"].upper() + ")"


            label = "{0}{1}".format(aufgabe, aufgabenformat)
        elif typ == 2:
            label = "{0}".format(aufgabe)

        label_aufgabe = create_new_label(new_groupbox, label, True)
        gridLayout_gB.addWidget(label_aufgabe, 0, 0, 1, 1)

        label_titel = create_new_label(
            new_groupbox, "Titel: {}".format(aufgabe_total["titel"]), True
        )
        gridLayout_gB.addWidget(label_titel, 1, 0, 1, 1)

        gridLayout_gB.setColumnStretch(2, 1)

        # af = aufgabe_total["af"]
        # if  af == 'oa' or af == 'ta' or af == 'ko' or typ==2:
        #     # widget_AB = create_new_groupbox(new_groupbox, "Gruppe")
        #     widget_AB = QtWidgets.QWidget(new_groupbox)
        #     # widget_AB.setSizePolicy(SizePolicy_fixed)
        #     gridLayout_gB.addWidget(widget_AB, 0,1,2,1,QtCore.Qt.AlignRight)
        #     horizontalLayout_widget_AB = create_new_horizontallayout(widget_AB)
        #     horizontalLayout_widget_AB.setSpacing(0)
            
        #     button_AB = create_new_button(widget_AB, "", still_to_define, "users.svg")
        #     button_AB.setCheckable(True)
        #     button_AB.toggle()
        #     horizontalLayout_widget_AB.addWidget(button_AB)

        #     label_AB = create_new_label(widget_AB, "")
        #     label_AB.setPixmap(QtGui.QPixmap(get_icon_path("users.svg")))
        #     label_AB.setFixedSize(QtCore.QSize(20,20))
        #     label_AB.setScaledContents(True)
        #     horizontalLayout_widget_AB.addWidget(label_AB)

        #     checkbox_AB = create_new_checkbox(widget_AB, " ", True)
        #     checkbox_AB.setSizePolicy(SizePolicy_fixed)
        #     self.dict_widget_variables['checkbox_AB_{}'.format(aufgabe)] = checkbox_AB

        #     try:
        #         gruppe = aufgabe_total['gruppe']
        #     except KeyError:
        #         gruppe = False

        #     if gruppe == False:
        #         checkbox_AB.setChecked(False)
        #         checkbox_AB.setEnabled(False)
        #         checkbox_AB.setToolTip("Derzeit ist für diese Aufgabe keine Gruppen-Variation verfügbar.")
        #     else:
        #         checkbox_AB.setToolTip("Diese Aufgabe wird bei unterschiedlichen Gruppen\ngeringfügig (z.B. durch veränderte Zahlen) variiert.")

        #     horizontalLayout_widget_AB.addWidget(checkbox_AB)


        groupbox_pkt = create_new_groupbox(new_groupbox, "Punkte")
        groupbox_pkt.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        groupbox_pkt.setSizePolicy(SizePolicy_fixed)
        gridLayout_gB.addWidget(groupbox_pkt, 0, 2, 2, 1, QtCore.Qt.AlignRight)


        try:
            self.temp_info
        except AttributeError:
            self.temp_info={}

        if aufgabe in self.temp_info:
            punkte = self.temp_info[aufgabe][0]
        elif typ == 1:
            punkte = self.spinBox_default_pkt.value()
        else:
            punkte = aufgabe_total["punkte"]



        horizontalLayout_groupbox_pkt = QtWidgets.QHBoxLayout(groupbox_pkt)
        horizontalLayout_groupbox_pkt.setObjectName(
            _fromUtf8("horizontalLayout_groupbox_pkt")
        )
        spinbox_pkt = create_new_spinbox(groupbox_pkt)

        spinbox_pkt.setValue(punkte)
        spinbox_pkt.valueChanged.connect(self.spinbox_pkt_changed)
        spinbox_pkt.setToolTip("0 = Punkte ausblenden")
        self.dict_variablen_punkte[aufgabe] = spinbox_pkt

        horizontalLayout_groupbox_pkt.addWidget(spinbox_pkt)

        if typ == 1:
            checkbox_pkt = create_new_checkbox(groupbox_pkt, "1/2")
            checkbox_pkt.setToolTip("Halbe Punkte möglich")
            if aufgabe in self.temp_info:
                state = self.temp_info[aufgabe][1]
            else:
                state= False             
            # checkbox_pkt.stateChanged.connect(partial(self.checkbox_pkt_changed, aufgabe))
            if state == True:
                checkbox_pkt.setChecked(True)
            horizontalLayout_groupbox_pkt.addWidget(checkbox_pkt)
            self.dict_variablen_punkte_halb[aufgabe] = checkbox_pkt

        # if typ == 2:
        #     groupbox_pkt.setToolTip(
        #         "Die Punkte geben die Gesamtpunkte dieser Aufgabe an.\nEs müssen daher auch die Ausgleichspunkte berücksichtigt werden."
        #     )

        if (index % 2) == 1 and (typ == 1 or typ == None):
            if self.display_mode == 0:
                stylesheet = StyleSheet_aufgaben_groupbox
            else:
                stylesheet = StyleSheet_aufgaben_groupbox_dark_mode
            new_groupbox.setStyleSheet(stylesheet)
        if typ == 2:
            if self.display_mode == 0:
                stylesheet = StyleSheet_typ2
            else:
                stylesheet = StyleSheet_typ2_dark_mode
            new_groupbox.setStyleSheet(stylesheet)


        button_translation = QtWidgets.QPushButton(new_groupbox)

        
        if aufgabe in self.temp_info:
            language = self.temp_info[aufgabe][3]
        else:
            language = "DE" 
        
        button_translation.setText(language)
        button_translation.setIcon(QtGui.QIcon(get_icon_path("globe.svg")))
        button_translation.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        button_translation.clicked.connect(lambda: self.btn_translation_pressed(button_translation, aufgabe))

        self.dict_variablen_translation[aufgabe] = button_translation.text()
        # create_new_button(new_groupbox, "DE", partial(self.btn_translation_pressed, button_translation), "globe.svg")

        try:
            if aufgabe_total['content_translation'] == None:
                button_translation.setEnabled(False)
                button_translation.setToolTip("Derzeit ist diese Aufgabe nur in Deutsch verfügbar.")
            else:
                button_translation.setToolTip("Diese Aufgabe kann in Deutsch oder Englisch angezeigt werden.")
        except KeyError:
            button_translation.setEnabled(False)
            button_translation.setToolTip("Derzeit ist diese Aufgabe nur in Deutsch verfügbar.")

        gridLayout_gB.addWidget(button_translation, 0, 4, 1, 1)

        af = aufgabe_total["af"]
        if  af == 'oa' or af == 'ta' or af == 'ko' or typ==2:

            button_AB = QtWidgets.QPushButton(new_groupbox)
            button_AB.setCheckable(True)
            gridLayout_gB.addWidget(button_AB, 1, 4, 1, 1)

            try:
                gruppe = aufgabe_total['gruppe']
            except KeyError:
                gruppe = False

            if gruppe == False:
                button_AB.setChecked(False)
                button_AB.setEnabled(False)
                button_AB.setToolTip("Derzeit ist für diese Aufgabe keine Gruppen-Variation verfügbar.")
            else:
                button_AB.setToolTip("Diese Aufgabe kann bei unterschiedlichen Gruppen\ngeringfügig (z.B. durch veränderte Zahlen) variiert werden.")


            if aufgabe in self.temp_info:
                gruppe_AB = self.temp_info[aufgabe][4]
            else:
                gruppe_AB = True

            button_AB.setChecked(gruppe_AB)  

            self.dict_variablen_AB[aufgabe] = button_AB.isChecked()
            button_AB.setIcon(QtGui.QIcon(get_icon_path("users.svg")))
            button_AB.clicked.connect(lambda: self.btn_AB_pressed(button_AB, aufgabe))

        else:
            self.dict_variablen_AB[aufgabe] = None


        button_up = create_new_button(new_groupbox, "", partial(self.btn_up_pressed, aufgabe))
        button_up.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        button_up.setIcon(QtGui.QIcon(get_icon_path('arrow-up-circle.svg'))) 
        button_up.setSizePolicy(SizePolicy_fixed)
        # button_up = create_standard_button(
        #     new_groupbox,
        #     "",
        #     partial(self.btn_up_pressed, aufgabe),
        #     QtWidgets.QStyle.SP_ArrowUp,
        # )

        gridLayout_gB.addWidget(button_up, 0, 5, 1, 1)
        # number = index + 1
        if index == 0:
            button_up.setEnabled(False)
        # if typ == 2 and number == aufgaben_verteilung[0] + 1:
        #     button_up.setEnabled(False)

        button_down = create_new_button(new_groupbox, "", partial(self.btn_down_pressed, aufgabe))
        button_down.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        button_down.setIcon(QtGui.QIcon(get_icon_path('arrow-down-circle.svg'))) 
        button_down.setSizePolicy(SizePolicy_fixed)

        # button_down = create_standard_button(
        #     new_groupbox,
        #     "",
        #     partial(self.btn_down_pressed, aufgabe),
        #     QtWidgets.QStyle.SP_ArrowDown,
        # )
        gridLayout_gB.addWidget(button_down, 0, 6, 1, 1)

        # if typ == 1 and number == aufgaben_verteilung[0]:
        #     button_down.setEnabled(False)
        # if (typ == 2 or typ == None) and number == len(self.list_alle_aufgaben_sage):
        if typ == 2:
            num_total = len(self.list_alle_aufgaben_sage[1])
        else:
            num_total = len(self.list_alle_aufgaben_sage[0])

        if index == num_total-1:
            button_down.setEnabled(False)


        pushbutton_edit = create_new_button(
            new_groupbox,
            "",
            partial(self.pushButton_edit_pressed, aufgabe),
        )
        pushbutton_edit.setIcon(QtGui.QIcon(get_icon_path('edit.svg')))
        pushbutton_edit.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor)) 
        # pushbutton_ausgleich.setStyleSheet("padding: 6px")
        pushbutton_edit.setSizePolicy(SizePolicy_maximum)

        gridLayout_gB.addWidget(pushbutton_edit, 1, 5, 1, 1)

        button_delete = create_new_button(new_groupbox, "", partial(self.btn_delete_pressed, aufgabe))
        button_delete.setIcon(QtGui.QIcon(get_icon_path('trash-2.svg')))
        button_delete.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor)) 
        button_delete.setSizePolicy(SizePolicy_fixed)

        # button_delete = create_standard_button(
        #     new_groupbox,
        #     "",
        #     partial(self.btn_delete_pressed, aufgabe),
        # )

        gridLayout_gB.addWidget(button_delete, 1, 6, 1, 1)

        # if typ == 2:
        #     self.dict_variablen_abstand[aufgabe] = 0
        # else:
        groupbox_abstand_ausgleich = create_new_groupbox(new_groupbox, "Abstand (cm)  ")
        groupbox_abstand_ausgleich.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        groupbox_abstand_ausgleich.setSizePolicy(SizePolicy_fixed)
        # groupbox_abstand.setMaximumSize(QtCore.QSize(100, 16777215))
        gridLayout_gB.addWidget(groupbox_abstand_ausgleich, 0,3, 2, 1)

        verticalLayout_abstand = QtWidgets.QVBoxLayout(groupbox_abstand_ausgleich)
        verticalLayout_abstand.setObjectName("verticalLayout_abstand")

        if aufgabe in self.temp_info:
            abstand = self.temp_info[aufgabe][2]
        else:
            abstand = aufgabe_total["abstand"]
        spinbox_abstand = create_new_spinbox(groupbox_abstand_ausgleich)
        spinbox_abstand.setValue(abstand)
        self.dict_variablen_abstand[aufgabe] = spinbox_abstand

        spinbox_abstand.valueChanged.connect(self.spinbox_abstand_changed)
        verticalLayout_abstand.addWidget(spinbox_abstand)

        # num_ap = self.count_ausgleichspunkte(aufgabe_total["content"])
        # if typ == 2:
        #     spinbox_abstand.hide()
        #     groupbox_abstand_ausgleich.setTitle("Ausgleichspkte")
            
        #     self.count_ausgleichspunkte(aufgabe_total["content"])
        #     label_ausgleichspkt = create_new_label(
        #         groupbox_abstand_ausgleich,
        #         str(num_ap),
        #     )
        #     label_ausgleichspkt.setStyleSheet("padding-top: 5px; padding-bottom: 5px;")
        #     verticalLayout_abstand.addWidget(label_ausgleichspkt)

        #     self.dict_variablen_label[aufgabe] = label_ausgleichspkt
        if typ == 2:
            groupbox_abstand_ausgleich.hide()
        else:
            groupbox_abstand_ausgleich.setToolTip("Neue Seite: Abstand=99")

        # pushbutton_ausgleich.setMaximumSize(QtCore.QSize(220, 30))
        
        # print(self.temp_info)
        # pushbutton_aufgabe_bearbeiten = create_new_button(groupbox_pkt, 'Aufgabe bearbeiten', still_to_define)
        # gridLayout_gB.addWidget(pushbutton_aufgabe_bearbeiten, 0,1,1,1)

        new_groupbox.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        return new_groupbox

    def get_klasse(self, mode="sage"):
        if mode == "sage":
            if self.comboBox_klassen.currentIndex() == 0:
                klasse = None
            else:
                klasse = list_klassen[self.comboBox_klassen.currentIndex() - 1]
        elif mode == "feedback":
            if self.comboBox_klassen_fb_cria.currentIndex() == 0:
                klasse = None
            else:
                klasse = list_klassen[self.comboBox_klassen_fb_cria.currentIndex() - 1]

        return klasse

    def delete_all_widgets(self, layout, start=0):
        for i in reversed(range(start, layout.count())):
            self.delete_widget(layout, i)

    def delete_widget(self, layout, index):
        try:
            layout.itemAt(index).widget().setParent(None)
        except AttributeError:
            pass

    def split_klasse_aufgabe(self, aufgabe):
        klasse, aufgabe = aufgabe.split("_", 1)
        if "L_" in aufgabe:
            aufgabe = "_" + aufgabe

        return klasse, aufgabe

    # def build_klasse_aufgabe(self, aufgabe):
    #     klasse = self.get_klasse()
    #     if "_L_" in aufgabe:
    #         klasse_aufgabe = klasse + aufgabe
    #     else:
    #         klasse_aufgabe = klasse + "_" + aufgabe
    #     return klasse_aufgabe

    def add_image_path_to_list(self, aufgabe):
        typ = get_aufgabentyp(self.chosen_program, aufgabe)
        aufgabe_total = get_aufgabe_total(aufgabe, typ)
        # content = aufgabe_total["content"]


        for image in aufgabe_total["bilder"]:
            self.list_copy_images.append(image)

        # if "\\includegraphics" in content:
        #     matches = re.findall("/Bilder/(.+.eps)}", content)
        #     for image in matches:
        #         self.list_copy_images.append(image)

    @report_exceptions
    def build_aufgaben_schularbeit(self, aufgabe):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        # try:
        #     self.gridLayout_8.removeItem(self.spacerItem)
        # except AttributeError:
        #     pass
        typ = get_aufgabentyp(self.chosen_program, aufgabe)        
        if typ == 2:
            list_index = 1
            layout = self.verticalLayout_scrollArea_sage_typ2
        else:
            list_index = 0
            layout = self.verticalLayout_scrollArea_sage_typ1
        index = self.list_alle_aufgaben_sage[list_index].index(aufgabe)

        if index == 0:
            start_value = index
        else:
            start_value = index - 1


        self.temp_info = {}
        for all in self.dict_variablen_punkte.keys():
            halbe_punkte = self.get_punkte_halb_aufgabe_sage(all)
            self.temp_info[all] = [self.dict_variablen_punkte[all].value(), halbe_punkte, self.dict_variablen_abstand[all].value(), self.dict_variablen_translation[all], self.dict_variablen_AB[all]]


        for i in reversed(range(start_value, layout.count()+1)):
            self.delete_widget(layout, i)

        for item in self.list_alle_aufgaben_sage[list_index][start_value:]:
            temp_typ = get_aufgabentyp(self.chosen_program, item)
            index_item = self.list_alle_aufgaben_sage[list_index].index(item)
            

            aufgabe_total = get_aufgabe_total(item.replace(" (lokal)", ""), temp_typ)
            neue_aufgaben_box = self.create_neue_aufgaben_box(
                index_item, item, aufgabe_total
            )


            layout.insertWidget(layout.count() - 1, neue_aufgaben_box)
            # if typ== 2:
            #     layout.insertWidget(layout.count() - 1, neue_aufgaben_box)
            # else:
            #     layout.insertWidget(layout.count(), neue_aufgaben_box)
            index_item + 1


        if typ == 1 and not is_empty(self.list_alle_aufgaben_sage[1]):
            num_typ1, _=self.get_aufgabenverteilung()
            for i, item in enumerate(self.list_alle_aufgaben_sage[1]):
                num = num_typ1+i+1
                self.dict_widget_variables[f'groupbox_sage_{item}'].setTitle(f"{num}. Aufgabe (Typ2)")

                
        # self.spacerItem = QtWidgets.QSpacerItem(
        #     20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        # )
        # self.gridLayout_8.addItem(self.spacerItem, index_item + 1, 0, 1, 1)

        self.add_image_path_to_list(aufgabe.replace(" (lokal)", ""))

        self.update_punkte()

        QtWidgets.QApplication.restoreOverrideCursor()

    def pushButton_edit_pressed(self, aufgabe):
        content = collect_content(self, aufgabe)

        # content_no_environment = split_content_no_environment(content)

        typ = get_aufgabentyp(self.chosen_program, aufgabe)

        if typ == 2:
            split_content = self.split_content(aufgabe, content)

            if split_content == False:
                return
            # try:
            #     split_content, index_end = split_aufgaben_content(content)
            #     split_content = split_content[:index_end]
            # except Exception as e1:
            #     try:
            #         split_content = split_aufgaben_content_new_format(content)
            #     except Exception:
            #         # split_content = None
            #         warning_window(
            #             "Es ist ein Fehler bei der Anzeige der Aufgabe {} aufgetreten! (Die Aufgabe kann voraussichtlich dennoch verwendet und individuell in der TeX-Datei bearbeitet werden.)\n".format(
            #                 aufgabe
            #             ),
            #             'Bitte melden Sie den Fehler unter dem Abschnitt "Feedback & Fehler" an das LaMA-Team. Vielen Dank!',
            #         )
            #         return

            # if aufgabe in self.dict_sage_ausgleichspunkte_chosen.keys():
            #     list_sage_ausgleichspunkte_chosen = (
            #         self.dict_sage_ausgleichspunkte_chosen[aufgabe]
            #     )
            # else:
            #     list_sage_ausgleichspunkte_chosen = []
            #     for index, all in enumerate(split_content):
            #         if "\\fbox{A}" in all or "\\ASubitem" in all:
            #             list_sage_ausgleichspunkte_chosen.append(index)
                    # if "\\fbox{A}" in all:
                    #     x = all.replace("\\fbox{A}", "")
                    #     list_sage_ausgleichspunkte_chosen.append(x)
                    # if "\\ASubitem" in all:
                    #     x = all.replace("\\ASubitem", "")
                    #     list_sage_ausgleichspunkte_chosen.append(x)

            if aufgabe in self.dict_sage_hide_show_items_chosen.keys():
                list_sage_hide_show_items_chosen = (
                    self.dict_sage_hide_show_items_chosen[aufgabe]
                )
            else:
                list_sage_hide_show_items_chosen = []

        else:
            list_sage_hide_show_items_chosen = []
            # list_sage_ausgleichspunkte_chosen = []
            split_content = None

        if aufgabe in self.dict_sage_individual_change.keys():
            sage_individual_change = self.dict_sage_individual_change[aufgabe]
        else:
            sage_individual_change = [None, None]

        Dialog = QtWidgets.QDialog(
            None,
            QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint
            | QtCore.Qt.WindowMaximizeButtonHint
            | QtCore.Qt.WindowMinimizeButtonHint,
        )
        ui = Ui_Dialog_ausgleichspunkte()
        ui.setupUi(
            Dialog,
            aufgabe,
            typ,
            content,
            split_content,
            list_sage_hide_show_items_chosen,
            sage_individual_change,
            self.dict_variablen_translation[aufgabe],
            self.display_mode,
            self.developer_mode_active,
            self.chosen_program,
        )

        Dialog.exec_()

        if ui.sage_individual_change == [None, None] and aufgabe in self.dict_sage_individual_change:
            self.dict_sage_individual_change.pop(aufgabe)
        else:
            self.dict_sage_individual_change[aufgabe] = ui.sage_individual_change

        # print(self.dict_sage_individual_change)

            

        if typ == 2:
            # if not is_empty(ui.list_sage_ausgleichspunkte_chosen):
            #     self.dict_sage_ausgleichspunkte_chosen[
            #         aufgabe
            #     ] = ui.list_sage_ausgleichspunkte_chosen
            # elif aufgabe in self.dict_sage_ausgleichspunkte_chosen:
            #     del self.dict_sage_ausgleichspunkte_chosen[aufgabe]

            if not is_empty(ui.list_sage_hide_show_items_chosen):
                self.dict_sage_hide_show_items_chosen[
                    aufgabe
                ] = ui.list_sage_hide_show_items_chosen

            elif aufgabe in self.dict_sage_hide_show_items_chosen:
                del self.dict_sage_hide_show_items_chosen[aufgabe]

            # print(self.dict_sage_hide_show_items_chosen)
            # self.dict_variablen_label[aufgabe].setText(
            #     "{}".format(len(ui.list_sage_ausgleichspunkte_chosen))
            # )

        self.update_punkte()

    # def splitter_sage_moved(self):
    #     self.width_groupBox_sage = self.groupBox_sage.geometry().width()
    #     self.min_width_groupBox_sage = self.groupBox_sage.minimumSizeHint().width()


        # if self.width_groupBox_sage <= self.min_width_groupBox_sage:
        #     self.groupBox_klasse_sage.hide()
        # else:
        #     self.groupBox_klasse_sage.show()
            


    def comboBox_at_sage_changed(self):
        if self.comboBox_at_sage.currentText()[-1] == "1":
            self.comboBox_gk.clear()
            self.lineEdit_number.clear()
            self.comboBox_gk.setEnabled(True)
            self.comboBox_gk_num.setEnabled(True)
            list_comboBox_gk = ["", "AG", "FA", "AN", "WS", "Zusatzthemen"]
            index = 0
            for all in list_comboBox_gk:
                self.comboBox_gk.addItem("")
                self.comboBox_gk.setItemText(index, _translate("MainWindow", all, None))
                index += 1
            self.comboBox_gk_num.clear()

        if self.comboBox_at_sage.currentText()[-1] == "2":
            self.comboBox_gk.setCurrentIndex(0)
            self.comboBox_gk_num.setCurrentIndex(0)
            self.comboBox_gk.setEnabled(False)
            self.comboBox_gk_num.setEnabled(False)

        self.adapt_choosing_list("sage")

    def change_status_combobox_general_feedback(self, status):
        self.comboBox_fb.setEnabled(status)
        self.comboBox_fb_num.setEnabled(status)
        self.lineEdit_number_fb.setEnabled(status)
        self.listWidget_fb.setEnabled(status)

    def comboBox_at_fb_cria_changed(self):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.label_example.setText(
            _translate("MainWindow", "Ausgewählte Aufgabe: -", None)
        )
        if self.comboBox_at_fb_cria.currentText() == "Allgemeine Rückmeldung":
            self.groupBox_alle_aufgaben_fb_cria.setEnabled(False)
            self.comboBox_klassen_fb_cria.setCurrentIndex(0)
            self.comboBox_kapitel_fb_cria.setCurrentIndex(0)
            self.comboBox_unterkapitel_fb_cria.setCurrentIndex(0)
            self.lineEdit_number_fb_cria.clear()
            self.listWidget_fb_cria.clear()
        else:
            self.groupBox_alle_aufgaben_fb_cria.setEnabled(True)
            self.adapt_choosing_list("feedback")

        QtWidgets.QApplication.restoreOverrideCursor()

    def comboBox_at_fb_changed(self):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.label_example.setText(
            _translate("MainWindow", "Ausgewählte Aufgabe: -", None)
        )

        if self.comboBox_at_fb.currentText() == "Allgemeine Rückmeldung":
            self.change_status_combobox_general_feedback(False)
        else:
            self.change_status_combobox_general_feedback(True)

        if self.comboBox_at_fb.currentText()[-1] == "1":
            self.comboBox_fb.clear()
            self.lineEdit_number_fb.clear()
            list_comboBox_gk = ["", "AG", "FA", "AN", "WS", "K5", "K6", "K7", "K8"]
            for all in list_comboBox_gk:
                self.comboBox_fb.addItem(all)

            self.comboBox_fb_num.clear()

        if self.comboBox_at_fb.currentText()[-1] == "2":
            self.comboBox_fb.clear()
            self.comboBox_fb_num.clear()
        self.adapt_choosing_list("feedback")
        QtWidgets.QApplication.restoreOverrideCursor()

    def comboBox_gk_changed(self, list_mode):
        if list_mode == "sage":
            self.comboBox_gk_num.clear()
            if self.comboBox_gk.currentText() == "":
                return

            self.comboBox_gk_num.addItem("")
            self.lineEdit_number.clear()
            # list_klassen = ["k5", "k6", "k7", "k8"]
            if self.comboBox_gk.currentText() == "Zusatzthemen":
                #     x = eval("%s_beschreibung" % self.comboBox_gk.currentText().lower())
                for all in zusatzthemen_beschreibung:
                    label = zusatzthemen_beschreibung[all] + " (" + all + ")"
                    self.comboBox_gk_num.addItem(label)
            else:
                for all in dict_gk.keys():
                    if all.startswith(self.comboBox_gk.currentText().lower()):
                        self.comboBox_gk_num.addItem(dict_gk[all][-3:])
        if list_mode == "feedback":
            self.comboBox_fb_num.clear()
            if self.comboBox_fb.currentText() == "":
                return
            self.comboBox_fb_num.addItem("")
            self.lineEdit_number_fb.clear()
            # list_klassen = ["k5", "k6", "k7", "k8"]
            # if self.comboBox_fb.currentText().lower() in list_klassen:
            #     x = eval("%s_beschreibung" % self.comboBox_fb.currentText().lower())
            #     for all in x.keys():
            #         self.comboBox_fb_num.addItem(all.upper())
            if self.comboBox_fb.currentText() == "Zusatzthemen":
                for all in zusatzthemen_beschreibung:
                    label = zusatzthemen_beschreibung[all] + " (" + all + ")"
                    self.comboBox_fb_num.addItem(label)
            else:
                for all in dict_gk.keys():
                    if all.startswith(self.comboBox_fb.currentText().lower()):
                        self.comboBox_fb_num.addItem(dict_gk[all][-3:])

        self.adapt_choosing_list(list_mode)

    def comboBox_gk_num_changed(self, list_mode):
        self.adapt_choosing_list(list_mode)

    def lineEdit_number_changed(self, list_mode):
        self.adapt_choosing_list(list_mode)

    def check_for_autosave(self):
        try:
            intervall = self.lama_settings["autosave"]
        except KeyError:
            self.lama_settings["autosave"] = 2
            intervall = 2

        if intervall == 0:
            return

        self.collect_all_infos_for_creating_file()
        autosave_file = os.path.join(
            path_localappdata_lama, "Teildokument", "autosave.lama"
        )
        try:
            modification = modification_date(autosave_file).strftime("%y%m%d-%H%M")
            date, time_tag = modification.split("-")
            day_time = datetime.datetime.now()

            day_time = day_time - datetime.timedelta(minutes=intervall)
            today, now_minus_intervall = day_time.strftime("%y%m%d-%H%M").split("-")

            if date != today:
                self.sage_save(autosave=autosave_file)
            elif now_minus_intervall >= time_tag:
                self.sage_save(autosave=autosave_file)
        except FileNotFoundError:
            self.sage_save(autosave=autosave_file)

        self.update_label_restore_action()

    @report_exceptions
    def nummer_clicked(self, item):
        aufgabe = item.text()

        # if self.chosen_program == "cria":
        # klasse = self.get_klasse("sage")
        # aufgabe = klasse + "." + aufgabe
        typ = get_aufgabentyp(self.chosen_program, aufgabe)
        if typ == 2:
            list_index = 1
        else:
            list_index = 0

        if aufgabe in self.list_alle_aufgaben_sage[list_index]:
            return

        self.sage_aufgabe_add(aufgabe)

        if not is_empty(self.list_alle_aufgaben_sage[1]):
            self.scrollAreaWidgetContents_typ2.show()

        self.build_aufgaben_schularbeit(aufgabe)  # aufgabe, aufgaben_verteilung
        # print(self.list_alle_aufgaben_sage)
        self.lineEdit_number.setText("")
        self.lineEdit_number.setFocus()
        self.check_for_autosave()
        self.no_saved_changes_sage = False

    def nummer_clicked_fb(self, item):
        if self.chosen_program == "lama":
            self.label_example.setText(
                _translate(
                    "MainWindow", "Ausgewählte Aufgabe: {}".format(item.text()), None
                )
            )

        if self.chosen_program == "cria":
            self.label_example.setText(
                _translate(
                    "MainWindow",
                    "Ausgewählte Aufgabe: {0}".format(
                        item.text()
                    ),
                    None,
                )
            )

    def comboBox_klassen_changed(self, list_mode):
        if list_mode == "sage":
            combobox_klassen = self.comboBox_klassen
            combobox_kapitel = self.comboBox_kapitel
            combobox_unterkapitel = self.comboBox_unterkapitel
        elif list_mode == "feedback":
            combobox_klassen = self.comboBox_klassen_fb_cria
            combobox_kapitel = self.comboBox_kapitel_fb_cria
            combobox_unterkapitel = self.comboBox_unterkapitel_fb_cria

            self.label_example.setText("Ausgewählte Aufgabe: -")

        dict_klasse_name = eval(
            "dict_{}_name".format(list_klassen[combobox_klassen.currentIndex() - 1])
        )

        combobox_kapitel.clear()
        combobox_unterkapitel.clear()

        if combobox_klassen.currentIndex() != 0:
            combobox_kapitel.addItem("")

            for all in dict_klasse_name.keys():
                combobox_kapitel.addItem(dict_klasse_name[all] + " (" + all + ")")

        self.adapt_choosing_list(list_mode)

    @report_exceptions
    def comboBox_kapitel_changed(self, list_mode, checked=False): # prevent error decorator
        # klasse = self.get_klasse(list_mode)
        if list_mode == "sage":
            combobox_klassen = self.comboBox_klassen
            chosen_kapitel = self.comboBox_kapitel.currentText()
            combobox_unterkapitel = self.comboBox_unterkapitel
        elif list_mode == "feedback":
            combobox_klassen = self.comboBox_klassen_fb_cria
            chosen_kapitel = self.comboBox_kapitel_fb_cria.currentText()
            combobox_unterkapitel = self.comboBox_unterkapitel_fb_cria

        dict_klasse = eval(
            "dict_{}".format(list_klassen[combobox_klassen.currentIndex() - 1])
        )

        chosen_kapitel = extract_topic_abbr(chosen_kapitel)

        combobox_unterkapitel.clear()

        if not is_empty(chosen_kapitel):
            list_unterkapitel = dict_klasse[chosen_kapitel]
            combobox_unterkapitel.addItem("")
            for all in list_unterkapitel:
                combobox_unterkapitel.addItem(dict_unterkapitel[all] + " (" + all + ")")

    def comboBox_unterkapitel_changed(self, list_mode):
        self.adapt_choosing_list(list_mode)

    def delete_zeros_at_beginning(self, string):
        while string.startswith("0"):
            string = string[1:]
        return string

    def add_items_to_listwidget(
        self,
        typ,
        listWidget,
        filtered_items,
        local=False,
    ):
        for _file_ in filtered_items:
            name = _file_["name"]

            item = QtWidgets.QListWidgetItem()

            if local == True:
                name = name + " (lokal)"
                # item.setBackground(blue_4)
                # item.setToolTip("lokal gespeichert")

            elif _file_["draft"] == True:
                item.setBackground(blue_5)
                item.setForeground(white)
                item.setToolTip("Entwurf")

            item.setText(name)

            if check_if_variation(_file_["name"]) == True:
                item.setToolTip("Variation")

            if _file_["draft"] == True and not self.cb_drafts_sage.isChecked():
                continue
            else:
                listWidget.addItem(item)

    @report_exceptions
    def adapt_choosing_list(self, list_mode):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        if list_mode == "sage":
            listWidget = self.listWidget
        elif list_mode == "feedback":
            if self.chosen_program == "lama":
                listWidget = self.listWidget_fb
            elif self.chosen_program == "cria":
                listWidget = self.listWidget_fb_cria

            if self.comboBox_at_fb.currentText() == "Allgemeine Rückmeldung":
                self.comboBox_fb.clear()
                self.comboBox_fb_num.clear()
                self.lineEdit_number_fb.clear()
                listWidget.clear()
                QtWidgets.QApplication.restoreOverrideCursor()
                return
        listWidget.clear()
        if self.chosen_program == "cria":
            typ = "cria"

        elif (
            self.comboBox_at_sage.currentText() == "Typ 1" and list_mode == "sage"
        ) or (self.comboBox_at_fb.currentText() == "Typ 1" and list_mode == "feedback"):
            typ = "lama_1"

        elif (
            self.comboBox_at_sage.currentText() == "Typ 2" and list_mode == "sage"
        ) or (self.comboBox_at_fb.currentText() == "Typ 2" and list_mode == "feedback"):
            typ = "lama_2"

        filter_string = get_filter_string(self, list_mode)

        if list_mode == "sage":
            line_entry = self.lineEdit_number.text()
        elif list_mode == "feedback":
            if self.chosen_program == "lama":
                line_entry = self.lineEdit_number_fb.text()
            elif self.chosen_program == "cria":
                line_entry = self.lineEdit_number_fb_cria.text()

        table = "table_" + typ
        if list_mode == "sage":
            table_lama = _local_database.table(table)
            filtered_items = filter_items(
                self, table_lama, typ, list_mode, filter_string, line_entry
            )

            self.add_items_to_listwidget(typ, listWidget, filtered_items, local=True)

        table_lama = _database.table(table)
        filtered_items = filter_items(
            self, table_lama, typ, list_mode, filter_string, line_entry
        )

        if _database_addon != None:
            table_lama = _database_addon.table(table)
            filtered_items_addon = filter_items(
                self, table_lama, typ, list_mode, filter_string, line_entry
            )
            for all in filtered_items_addon:
                filtered_items.append(all)

        filtered_items.sort(key=order_gesammeltedateien)

        self.add_items_to_listwidget(typ, listWidget, filtered_items)

        QtWidgets.QApplication.restoreOverrideCursor()

    @report_exceptions
    def collect_all_infos_for_creating_file(self):
        self.dict_all_infos_for_file = {}

        self.dict_all_infos_for_file[
            "list_alle_aufgaben"
        ] = self.list_alle_aufgaben_sage

        _dict = {}
        
        for list_index in [0,1]:
            for aufgabe in self.list_alle_aufgaben_sage[list_index]:
                halbe_punkte = self.get_punkte_halb_aufgabe_sage(aufgabe)
                _dict[aufgabe] = [
                    self.get_punkte_aufgabe_sage(aufgabe),
                    self.get_abstand_aufgabe_sage(aufgabe),
                    halbe_punkte,
                ]


        self.dict_all_infos_for_file["dict_alle_aufgaben_pkt_abstand"] = _dict

        # self.dict_all_infos_for_file[
        #     "dict_alle_aufgaben"
        # ] = self.dict_alle_aufgaben_sage

        ### include dictionary of changed 'ausgleichspunkte' ###
        # self.dict_all_infos_for_file[
        #     "dict_ausgleichspunkte"
        # ] = {}

        ### end ###
        ### include dictionary hide/show items ###
        self.dict_all_infos_for_file[
            "dict_hide_show_items"
        ] = self.dict_sage_hide_show_items_chosen

        ### end ###

        self.dict_all_infos_for_file[
            "dict_individual_change"
        ] = self.dict_sage_individual_change

        ### include basic data of test ###
        if self.combobox_beurteilung.currentText() == "Notenschlüssel":
            beurteilung = "ns"
        elif self.combobox_beurteilung.currentText() == "Beurteilungsraster":
            beurteilung = "br"
        elif self.combobox_beurteilung.currentText() == "keine Auswahl":
            beurteilung = "none"

        dict_data_gesamt = {
            "program": self.chosen_program,
            "#": self.spinBox_nummer.value(),
            "Pruefungstyp": self.comboBox_pruefungstyp.currentText(),
            "Datum": [
                self.dateEdit.date().year(),
                self.dateEdit.date().month(),
                self.dateEdit.date().day(),
            ],  # .toPyDate()
            "Klasse": self.lineEdit_klasse_sage.text(),
            "Beurteilung": beurteilung,
            "Notenschluessel": [
                self.spinBox_2.value(),
                self.spinBox_3.value(),
                self.spinBox_4.value(),
                self.spinBox_5.value(),
            ],
            "Typ1 Standard": self.spinBox_default_pkt.value(),
            # "copy_images": self.list_copy_images,
        }

        self.dict_all_infos_for_file["data_gesamt"] = dict_data_gesamt

    def split_content(self, aufgabe, content):
        try:
            split_content, index_end = split_aufgaben_content(content)
            split_content = split_content[:index_end]
            return split_content
        except Exception:
            try:
                split_content = split_aufgaben_content_new_format(content)
                return split_content
            except Exception:
                # split_content = None
                warning_window(
                    "Es ist ein Fehler bei der Anzeige der Aufgabe {} aufgetreten! (Die Aufgabe kann voraussichtlich dennoch verwendet und individuell in der TeX-Datei bearbeitet werden.)\n".format(
                        aufgabe
                    ),
                    'Bitte melden Sie den Fehler unter dem Abschnitt "Feedback & Fehler" an das LaMA-Team. Vielen Dank!',
                )
                return False

    def replace_group_variation_aufgabe(self, content):
        _list = re.findall("\\\\variation\{.*\}\{.*\}", content)

        for all in _list:
            open_count=0
            close_count=0
            for i, char in enumerate(all):
                if char != "{" and char != "}":
                    continue
                elif char == "{":
                    open_count +=1
                elif char == "}":
                    close_count +=1
                if open_count==close_count:
                    start_index = i
                    break

            replacement_string = all[start_index+2:-1].replace("\\", "\\\\")

            content = re.sub("\\\\variation\{.*\}\{.*\}", replacement_string, content)



        return content

    def add_content_to_tex_file(
        self, aufgabe, aufgabe_total, filename_vorschau, first_typ2, ausgabetyp
    ):


        if get_aufgabentyp(self.chosen_program, aufgabe) == 2:
            if first_typ2 == False:
                header = "\\newpage \n\n\\textbf{Typ 2 Aufgaben}\n\n"
                first_typ2 = True
            else:
                header = "\\newpage\n\n"
        else:
            header = ""

        punkte = self.get_punkte_aufgabe_sage(aufgabe)

        halbe_punkte = self.get_punkte_halb_aufgabe_sage(aufgabe)

        abstand = self.get_abstand_aufgabe_sage(aufgabe)
        if punkte == 0:
            begin = "\\begin{enumerate}\item[\\stepcounter{number}\\thenumber.]"
            end = "\end{enumerate}"
        elif aufgabe_total["pagebreak"] == False:
            begin = begin_beispiel(aufgabe_total["themen"], punkte, halbe_punkte)
            end = end_beispiel
        elif aufgabe_total["pagebreak"] == True:
            begin = begin_beispiel_lang(punkte)
            end = end_beispiel_lang

        begin = begin + "\t% Aufgabe: {}\n".format(aufgabe_total["name"])

        if abstand == 99:
            vspace = "\\newpage \n\n"
        elif abstand == 0:
            vspace = ""
        else:
            vspace = "\\vspace{{{0}cm}} \n\n".format(abstand)

        
            # print(f"{aufgabe}: {self.dict_variablen_translation[aufgabe]}")

        
        try:
            if self.dict_sage_individual_change[aufgabe] != [None, None]:
                individual_changes = True
            else:
                individual_changes = False
        except KeyError:
            individual_changes = False


        if individual_changes == True:
            if self.dict_variablen_translation[aufgabe] == "DE":
                index = 0
                entry_key = "content"
            elif self.dict_variablen_translation[aufgabe] == "EN":
                index = 1
                entry_key = "content_translation"


            if self.dict_sage_individual_change[aufgabe][index] != None:
                content = self.dict_sage_individual_change[aufgabe][index]
            else:
                content = aufgabe_total[entry_key]

        elif self.dict_variablen_translation[aufgabe] == "EN":
            content = aufgabe_total["content_translation"]
            
        # elif aufgabe in self.dict_sage_ausgleichspunkte_chosen:
        #     full_content = aufgabe_total["content"]

        #     split_content = self.split_content(aufgabe, aufgabe_total["content"])
        #     content = edit_content_ausgleichspunkte(
        #         self, aufgabe, split_content, full_content
        #     )


        elif aufgabe in self.dict_sage_hide_show_items_chosen:
            full_content = aufgabe_total["content"]
            split_content = self.split_content(aufgabe, aufgabe_total["content"])
            split_content = prepare_content_for_hide_show_items(split_content)
            content = edit_content_hide_show_items(
                self, aufgabe, split_content, full_content
            )


        else:
            content = aufgabe_total["content"]



        if ausgabetyp == "schularbeit" and is_empty(aufgabe_total['bilder'])  == False:
            for image in aufgabe_total['bilder']:
                content = re.sub(r"{{../_database.*{0}}}".format(image),"{{{0}}}".format(image),content)


        show_group_B = False
        if 'checkbox_AB_{}'.format(aufgabe) in self.dict_widget_variables:
            checkbox = self.dict_widget_variables['checkbox_AB_{}'.format(aufgabe)]
            if checkbox.isChecked() and self.comboBox_gruppe_AB.currentIndex()==1:
                show_group_B = True


        with open(filename_vorschau, "a+", encoding="utf8") as vorschau:
            vorschau.write(header)
            if show_group_B == True:
                vorschau.write("\setcounter{Zufall}{1}")    
            vorschau.write(begin)
            vorschau.write(content)
            vorschau.write(end)
            if show_group_B == True:
                vorschau.write("\setcounter{Zufall}{0}")
            vorschau.write(vspace)
            vorschau.write("\n\n")

        return first_typ2

    @report_exceptions
    def create_body_of_tex_file(self, filename_vorschau, ausgabetyp):
        first_typ2 = False

        for aufgabe in self.list_alle_aufgaben_sage[0]:
            name = aufgabe.replace(" (lokal)", "")
            typ = get_aufgabentyp(self.chosen_program, name)
            aufgabe_total = get_aufgabe_total(name, typ)
            if aufgabe_total == None:
                warning_window(
                    "Die Aufgabe {} konnte nicht gefunden werden, da sie gelöscht oder umbenannt wurde. Sie wird daher beim Erstellen ignoriert.".format(
                        name
                    )
                )
                continue

            self.add_content_to_tex_file(
                aufgabe, aufgabe_total, filename_vorschau, first_typ2, ausgabetyp
            )
        
        for aufgabe in self.list_alle_aufgaben_sage[1]:
            name = aufgabe.replace(" (lokal)", "")
            typ = get_aufgabentyp(self.chosen_program, name)
            aufgabe_total = get_aufgabe_total(name, typ)
            if aufgabe_total == None:
                warning_window(
                    "Die Aufgabe {} konnte nicht gefunden werden, da sie gelöscht oder umbenannt wurde. Sie wird daher beim Erstellen ignoriert.".format(
                        name
                    )
                )
                continue

            first_typ2 = self.add_content_to_tex_file(
                aufgabe, aufgabe_total, filename_vorschau, first_typ2, ausgabetyp
            ) 

    @report_exceptions
    def pushButton_vorschau_pressed(
        self,
        ausgabetyp,
        index=0,
        maximum=0,
        pdf=True,
        show_pagenumber='plain',
        single_file_index=None,
        filename_vorschau=os.path.join(
            path_programm, "Teildokument", "Schularbeit_Vorschau.tex"
        ),
    ):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        if ausgabetyp == "vorschau":
            self.collect_all_infos_for_creating_file()


        self.dict_gruppen = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F"}

        if filename_vorschau == "":
            QtWidgets.QApplication.restoreOverrideCursor()
            return

        if self.chosen_program == "lama":
            dict_titlepage = self.dict_titlepage
        if self.chosen_program == "cria":
            dict_titlepage = self.dict_titlepage_cria

        # if self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"] == "Quiz":
        #     beamer_mode = True
        # else:
        #     beamer_mode = False

        if (
            (ausgabetyp == "vorschau" and self.cb_solution_sage.isChecked() == True)
            or (ausgabetyp == "schularbeit" and index % 2 == 0)
            or (ausgabetyp == "schularbeit" and pdf == False)
        ):
            solution = "solution_on"

        else:
            solution = "solution_off"

        if (
            ausgabetyp == "schularbeit" and single_file_index == None
        ):  # and index != self.ui_erstellen.spinBox_sw_gruppen.value() * 2
            gruppe = int(index / 2)
        else:
            gruppe = 0

        str_titlepage = get_titlepage_vorschau(
            self, dict_titlepage, ausgabetyp, maximum, gruppe
        )

        if self.chosen_program == "lama" and (
            self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"] == "Schularbeit"
            or self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
            == "Wiederholungsschularbeit"
            or self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
            == "Nachschularbeit"
        ):
            header = "\\textbf{Typ 1 Aufgaben}\n\n"

        else:
            header = ""

        # vorschau = open(filename_vorschau, "w+", encoding="utf8")

        with open(filename_vorschau, "w+", encoding="utf8") as vorschau:
            vorschau.write(
                tex_preamble(solution=solution, random=gruppe, pagestyle=show_pagenumber)
            )
            vorschau.write(str_titlepage)
            vorschau.write(header)

        if single_file_index != None:
            for group in range(self.ui_erstellen.spinBox_sw_gruppen.value() - 1):
                self.create_body_of_tex_file(filename_vorschau, ausgabetyp)

                str_titlepage = get_titlepage_vorschau(
                    self, dict_titlepage, ausgabetyp, maximum, group + 1
                )
                with open(filename_vorschau, "a", encoding="utf8") as vorschau:
                    vorschau.write("\n\n")
                    vorschau.write("\\newpage\n")
                    vorschau.write(
                        "\setcounter{{Zufall}}{{{0}}}\setcounter{{number}}{{0}}\setcounter{{page}}{{1}}\n\n".format(
                            group + 1
                        )
                    )
                    vorschau.write(str_titlepage)

            self.create_body_of_tex_file(filename_vorschau, ausgabetyp)

            with open(filename_vorschau, "a", encoding="utf8") as vorschau:
                vorschau.write("\n\n")
                vorschau.write(tex_end)

            name, extension = os.path.splitext(filename_vorschau)

            if pdf == True:
                create_pdf(name, index, 2)

                temp_filename = name + ".pdf"
                if index % 2 == 0:
                    new_filename = name + "_Loesung.pdf"

                    shutil.move(temp_filename, new_filename)

                self.reset_latex_file_to_start(filename_vorschau)
            QtWidgets.QApplication.restoreOverrideCursor()
            return single_file_index + 1

        else:
            self.create_body_of_tex_file(filename_vorschau, ausgabetyp)

        if (
            self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
            != "Grundkompetenzcheck"
            and self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
            != "Übungsblatt"
            # and self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"] != "Quiz"
        ):
            # dict_titlepage = check_if_hide_all_exists(dict_titlepage)
            if self.dict_all_infos_for_file["data_gesamt"]["Beurteilung"] == "ns": #or dict_titlepage["hide_all"] == True:
                notenschluessel = self.dict_all_infos_for_file["data_gesamt"][
                    "Notenschluessel"
                ]

                zusatz = ""
                if self.cb_ns_halbe_pkt.isChecked():
                    zusatz = "[1/2]"
                if self.cb_ns_prozent.isChecked():
                    if zusatz == "":
                        zusatz = "[]"
                    zusatz = zusatz + "[prozent]"

                # if self.dict_all_infos_for_file["data_gesamt"]["Beurteilung"] == "br":
                #     gut = 0.875
                #     befriedigend = 0.75
                #     genuegend = 0.625
                #     nichtgenuegend = 0.5
                #     zusatz = "[1/2]"
                # else: 
                gut = notenschluessel[0] / 100
                befriedigend = notenschluessel[1] / 100
                genuegend = notenschluessel[2] / 100
                nichtgenuegend = notenschluessel[3] / 100
                with open(filename_vorschau, "a", encoding="utf8") as vorschau:
                    vorschau.write(
                        "\n\n\\null\\notenschluessel{0}{{{1}}}{{{2}}}{{{3}}}{{{4}}}".format(
                            zusatz,
                            gut,
                            befriedigend,
                            genuegend,
                            nichtgenuegend,
                        )
                    )

        with open(filename_vorschau, "a", encoding="utf8") as vorschau:
            vorschau.write("\n\n")
            vorschau.write(tex_end)
            vorschau.write("\n\n")
            vorschau.write(
                "% Aufgabenliste: {}".format(", ".join(self.list_alle_aufgaben_sage[0]+self.list_alle_aufgaben_sage[1]))
            )

        if ausgabetyp == "schularbeit":
            if index == 0:
                if (
                    dict_titlepage["logo"] == True
                    and dict_titlepage["hide_all"] == False
                ):
                    success = copy_logo_to_target_path(
                        self, dict_titlepage["logo_path"]
                    )
                    if success == False:
                        warning_window(
                            "Das Logo konnte nicht gefunden werden.",
                            "Bitte suchen Sie ein Logo unter: \n\nTitelblatt anpassen - Durchsuchen",
                            "Kein Logo ausgewählt",
                        )

                # if (
                #     is_empty(self.dict_all_infos_for_file["data_gesamt"]["copy_images"])
                #     == False
                # ):
                #     for image in self.dict_all_infos_for_file["data_gesamt"]["copy_images"]:
                #         copy_included_images(self, image)

            elif index == self.ui_erstellen.spinBox_sw_gruppen.value() * 2:
                QtWidgets.QApplication.restoreOverrideCursor()
                return

        # return ## WORKING RETURN
        if ausgabetyp == "vorschau":
            create_pdf("Schularbeit_Vorschau", 0, 0)

        if ausgabetyp == "schularbeit":
            name, extension = os.path.splitext(filename_vorschau)

            if pdf == True:
                create_pdf(name, index, maximum)

                temp_filename = name + ".pdf"

                if maximum > 2:
                    if index % 2 == 0:
                        new_filename = name + "_{}_Loesung.pdf".format(
                            self.dict_gruppen[int(index / 2)]
                        )
                    else:
                        new_filename = name + "_{}.pdf".format(
                            self.dict_gruppen[int(index / 2)]
                        )

                    shutil.move(temp_filename, new_filename)

                elif index % 2 == 0:
                    new_filename = name + "_Loesung.pdf"

                    shutil.move(temp_filename, new_filename)

                if index == maximum - 1:
                    self.reset_latex_file_to_start(filename_vorschau)

        QtWidgets.QApplication.restoreOverrideCursor()

    def reset_latex_file_to_start(self, filename_vorschau):
        with open(filename_vorschau, "r", encoding="utf8") as vorschau:
            text = vorschau.read()
        text = re.sub(r"random=.", "random=0", text)
        text = re.sub(r"Large Gruppe .", "Large Gruppe A", text)

        text = re.sub(r"solution_off", "solution_on", text)

        with open(filename_vorschau, "w", encoding="utf8") as vorschau:
            vorschau.write(text)

    #######################################################################
    ########################################################################

    def reset_feedback(self):
        self.plainTextEdit_fb.setPlainText(_translate("MainWindow", "", None))
        self.comboBox_at_fb.setCurrentIndex(0)
        self.label_example.setText(
            _translate("MainWindow", "Ausgewählte Aufgabe: -", None)
        )
        self.comboBox_fehlertyp.setCurrentIndex(0)
        self.comboBox_at_fb.setCurrentIndex(0)
        self.comboBox_fb.setCurrentIndex(0)
        self.comboBox_fb_num.setCurrentIndex(0)
        self.lineEdit_number_fb.setText(_translate("MainWindow", "", None))
        self.lineEdit_email.setText(_translate("MainWindow", "", None))

    @report_exceptions
    def pushButton_send_pressed(self):
        if (
            self.comboBox_at_fb.currentText() == "Allgemeine Rückmeldung"
            or self.comboBox_at_fb_cria.currentText() == "Allgemeine Rückmeldung"
        ):
            example = "Allgemeiner Bug Report"
            if self.plainTextEdit_fb.toPlainText() == "":
                warning_window(
                    "Bitte geben Sie ein Feedback oder beschreiben Sie das Problem im Textfeld."
                )
                return
        else:
            rest, example = self.label_example.text().split(": ")
            if example == "-":
                warning_window(
                    'Bitte wählen Sie die Aufgabe, zu der Sie eine Rückmeldung geben möchten oder wählen Sie "Allgemeine Rückmeldung" aus.'
                )
                return

        fehler = self.comboBox_fehlertyp.currentText()
        if fehler == "":
            warning_window("Bitte wählen Sie einen Betreff aus.")
            return
        if fehler == "Sonstiges" or fehler == "Feedback":
            if self.plainTextEdit_fb.toPlainText() == "":
                warning_window("Bitte geben Sie nähere Informationen im Textfeld an.")
                return

        if self.plainTextEdit_fb.toPlainText() == "":
            description = "keine Angabe"
        else:
            description = self.plainTextEdit_fb.toPlainText()
        if self.lineEdit_email.text() == "":
            contact = "keine Angabe"
        else:
            contact = self.lineEdit_email.text()

        if self.chosen_program == "cria":
            programm = "LaMA-Cria - "
        else:
            programm = ""
        content = "Subject: {0}{1}: {2}\n\nProblembeschreibung:\n\n{3}\n\n\nKontakt: {4}".format(
            programm, example, fehler, description, contact
        )

        gmail_user = "lamabugfix@gmail.com"
        try:
            fbpassword_path = os.path.join(path_programm, "_database", "_config")
            fbpassword_file = os.path.join(fbpassword_path, "c2skuwwtgh.txt")
            f = open(fbpassword_file, "r")
            fbpassword_check = []
            fbpassword_check.append(f.read().replace(" ", "").replace("\n", ""))
            gmail_password = fbpassword_check[0]

        except FileNotFoundError:
            pw_msg = QtWidgets.QInputDialog(
                None,
                QtCore.Qt.WindowSystemMenuHint
                | QtCore.Qt.WindowTitleHint
                | QtCore.Qt.WindowCloseButtonHint,
            )
            pw_msg.setInputMode(QtWidgets.QInputDialog.TextInput)
            pw_msg.setWindowTitle("Passworteingabe nötig")
            pw_msg.setLabelText("Passwort:")
            pw_msg.setCancelButtonText("Abbrechen")
            pw_msg.setWindowIcon(QtGui.QIcon(logo_path))
            if pw_msg.exec_() == QtWidgets.QDialog.Accepted:
                gmail_password = pw_msg.textValue()
            else:
                return

        try:
            QtWidgets.QApplication.setOverrideCursor(
                QtGui.QCursor(QtCore.Qt.WaitCursor)
            )
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(
                "lamabugfix@gmail.com", "lama.helpme@gmail.com", content.encode("utf8")
            )
            server.close()

            QtWidgets.QApplication.restoreOverrideCursor()

            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowIcon(QtGui.QIcon(logo_path))
            msg.setWindowTitle("Meldung gesendet")
            msg.setText(
                "Das Feedback bzw. die Fehlermeldung wurde erfolgreich gesendet!\n"
            )
            msg.setInformativeText("Vielen Dank für die Mithilfe, LaMA zu verbessern.")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()

            QtWidgets.QApplication.setOverrideCursor(
                QtGui.QCursor(QtCore.Qt.WaitCursor)
            )
            self.reset_feedback()

            QtWidgets.QApplication.restoreOverrideCursor()

            return
        except:
            QtWidgets.QApplication.restoreOverrideCursor()

            if "smtplib.SMTPAuthenticationError" in str(sys.exc_info()[0]):
                text = (
                    "Bitte kontaktieren Sie den Support unter:\nlama.helpme@gmail.com"
                )

            else:
                text = "Überprüfen Sie Ihre Internetverbindung oder kontaktieren Sie den Support für nähere Informationen unter:\nlama.helpme@gmail.com"

            critical_window(
                "Das Feedback konnte leider nicht gesendet werden!",
                text,
                "Fehler beim Senden",
                "Fehlermeldung:\n" + str(sys.exc_info()),
            )

    #######################################################################
    ##########################################################################
    ############################################################################

    @report_exceptions
    def pushButton_erstellen_pressed(self):
        self.collect_all_infos_for_creating_file()
        try:
            self.saved_file_path
        except AttributeError:
            self.saved_file_path = path_home

        if self.chosen_program == "lama":
            dict_titlepage = self.dict_titlepage
        if self.chosen_program == "cria":
            dict_titlepage = self.dict_titlepage_cria

        self.open_dialogwindow_erstellen(
            dict_titlepage,
        )

    @report_exceptions
    def update_gui(self, chosen_gui):

        if chosen_gui == "widgets_search":
            self.stackMainWindow.setCurrentIndex(0)
        elif chosen_gui == "widgets_sage":
            self.stackMainWindow.setCurrentIndex(1)
        elif chosen_gui == "widgets_create" or chosen_gui == "widgets_edit":
            self.stackMainWindow.setCurrentIndex(2)
        elif chosen_gui == "widgets_feedback":
            self.stackMainWindow.setCurrentIndex(3)
        elif chosen_gui == "widgets_wizard":
            self.stackMainWindow.setCurrentIndex(4)

        self.stackMainWindow.minimumSizeHint()
        if self.chosen_program == "cria":
            chosen_gui = chosen_gui + "_cria"

        chosen_gui_list = eval(chosen_gui)

        self.chosen_gui = chosen_gui
        self.MainWindow.setMenuBar(self.menuBar)
        list_delete = []
        for item in list_widgets:
            if item != chosen_gui_list:
                list_delete += item

        for all in list_delete:
            if "action" in all:
                exec("%s.setEnabled(False)" % all)
            elif "layout" in all.lower():
                exec("%s.setParent(None)" % all)
            else:
                exec("%s.hide()" % all)
        for all in chosen_gui_list:
            if "action" in all:
                exec("%s.setEnabled(True)" % all)
            # elif "layout" in all.lower():
            #     exec("self.gridLayout.addLayout({}, 0, 0, 1, 1)".format(all))
            else:
                exec("%s.show()" % all)

        if chosen_gui == "widgets_search":
            if self.combobox_aufgabentyp.currentIndex() == 0:
                self.combobox_searchtype.hide()
        if chosen_gui == "widgets_sage" or chosen_gui == "widgets_sage_cria":
            self.MainWindow.setTabOrder(self.spinBox_nummer, self.dateEdit)
            self.MainWindow.setTabOrder(self.dateEdit, self.lineEdit_klasse_sage)
            self.adapt_choosing_list("sage")
        if chosen_gui == "widgets_feedback" or chosen_gui == "widgets_feedback_cria":
            self.adapt_choosing_list("feedback")


        if self.developer_mode_active == False:
            self.menuBar.removeAction(self.menuDeveloper.menuAction())

        self.check_admin_entry()

        list_all_menubar = [self.menuSuche, self.menuSage, self.menuNeu, self.menuFeedback, self.menuOptionen ,self.menuDeveloper, self.menuHelp]
        list_menubar_wizard = [self.menuWizard, self.menuOptionen ,self.menuHelp]

        if chosen_gui == 'widgets_wizard':
            for all in list_all_menubar:
                if all == self.menuDeveloper and self.developer_mode_active == False:
                    continue
                else:
                    self.menuBar.removeAction(all.menuAction())
            for all in list_menubar_wizard:
                self.menuBar.addAction(all.menuAction())

            self.actionRefresh_Database.setVisible(False)

        else:
            for all in list_menubar_wizard:
                self.menuBar.removeAction(all.menuAction())

            for all in list_all_menubar:
                if all == self.menuDeveloper and self.developer_mode_active == False:
                    continue
                else:
                    self.menuBar.addAction(all.menuAction())
            self.actionRefresh_Database.setVisible(True)


        return

        #     chosen_gui_list = eval(chosen_gui)
        # else:
        chosen_gui_list = eval(chosen_gui)

        self.chosen_gui = chosen_gui
        self.MainWindow.setMenuBar(self.menuBar)
        list_delete = []
        for item in list_widgets:
            if item != chosen_gui_list:
                list_delete += item
        for all in list_delete:
            if "action" in all:
                exec("%s.setEnabled(False)" % all)
                # exec("self.%s.setVisible(False)" % all)
            # elif "menu" in all:
            #     exec("self.menuBar.removeAction(self.%s.menuAction())" % all)
            elif "layout" in all.lower():
                exec("%s.setParent(None)" % all)
            else:
                exec("%s.hide()" % all)
        for all in chosen_gui_list:
            if "action" in all:
                exec("%s.setEnabled(True)" % all)
                # exec("self.%s.setVisible(True)" % all)
            # elif "menu" in all:
            #     exec("self.menuBar.addAction(self.%s.menuAction())" % all)
            elif "layout" in all.lower():
                exec("self.gridLayout.addLayout({}, 0, 0, 1, 1)".format(all))
            else:
                exec("%s.show()" % all)

        if chosen_gui == "widgets_search":
            # if self.label_aufgabentyp.text()[-1] == str(1):
            if self.combobox_aufgabentyp.currentIndex() == 0:
                self.combobox_searchtype.hide()
        # if chosen_type == str(2):
        #     self.label_aufgabentyp.setText(
        #         _translate("MainWindow", "Aufgabentyp: Typ 1", None)
        #     )
        #     self.groupBox_af.show()
        #     self.combobox_searchtype.hide()
        #     self.refresh_label_update()
        #     self.chosen_aufgabenformat_typ()
        if chosen_gui == "widgets_sage" or chosen_gui == "widgets_sage_cria":
            self.MainWindow.setTabOrder(self.spinBox_nummer, self.dateEdit)
            self.MainWindow.setTabOrder(self.dateEdit, self.lineEdit_klasse_sage)
            self.adapt_choosing_list("sage")
            # self.listWidget.itemClicked.connect(self.nummer_clicked)
        if chosen_gui == "widgets_feedback" or chosen_gui == "widgets_feedback_cria":
            self.adapt_choosing_list("feedback")

        if self.developer_mode_active == False:
            self.menuBar.removeAction(self.menuDeveloper.menuAction())
            # self.listWidget_fb.itemClicked.connect(self.nummer_clicked_fb)
            # self.listWidget_fb_cria.itemClicked.connect(self.nummer_clicked_fb)

        self.check_admin_entry()
        list_all_menubar = [self.menuSuche, self.menuSage, self.menuNeu, self.menuFeedback, self.menuOptionen ,self.menuDeveloper, self.menuHelp]
        list_menubar_wizard = [self.menuWizard, self.menuOptionen ,self.menuHelp]

        # if self.developer_mode_active == True:

        if chosen_gui == 'widgets_wizard':
            for all in list_all_menubar:
                if all == self.menuDeveloper and self.developer_mode_active == False:
                    continue
                else:
                    self.menuBar.removeAction(all.menuAction())
            for all in list_menubar_wizard:
                self.menuBar.addAction(all.menuAction())

            self.actionRefresh_Database.setVisible(False)

        else:
            for all in list_menubar_wizard:
                self.menuBar.removeAction(all.menuAction())

            for all in list_all_menubar:
                if all == self.menuDeveloper and self.developer_mode_active == False:
                    continue
                else:
                    self.menuBar.addAction(all.menuAction())
            self.actionRefresh_Database.setVisible(True)



# class WrappedWindow(QtWidgets.QMainWindow):
#     resized = QtCore.pyqtSignal()
#     def  __init__(self, parent=None):
#         super(WrappedWindow, self).__init__(parent=parent)
#         ui = Ui_MainWindow()
#         ui.setupUi(self)
#         self.resized.connect(partial(self.adaptGUItosize, ui))

#     def resizeEvent(self, event):
#         self.resized.emit()
#         return super(WrappedWindow, self).resizeEvent(event)

#     def adaptGUItosize(self, MainWindow):
#         size = QtCore.QSize(self.geometry().width(), self.geometry().height())
#         # MainWindow.label_lamaLogo.setText("TEEEST")
#         # return size
#         width = self.geometry().width()
#         height = self.geometry().height()

        # if width<=350:
        #     MainWindow.widget_searchMenu.hide()
        #     MainWindow.gridLayout.addWidget(MainWindow.btn_suche, 3, 0, 1, 1, QtCore.Qt.AlignRight)
        # else:
        #     MainWindow.widget_searchMenu.show()
        #     MainWindow.gridLayout.addWidget(MainWindow.btn_suche, 3, 1, 1, 1, QtCore.Qt.AlignRight)
            # if height <= 625:
            #     MainWindow.groupBox_ausgew_gk.hide()
            #     MainWindow.groupBox_pdf_output.hide()
            # else:
            #     MainWindow.groupBox_ausgew_gk.show()
            #     MainWindow.groupBox_pdf_output.show()
        # MainWindow.label_warnung.setText(str(size))



if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle("Fusion")
    # dir_ = QtCore.QDir("assets/fonts/IBM_Plex_Sans")
    _id = QtGui.QFontDatabase.addApplicationFont("assets/fonts/IBM_Plex_Sans/IBMPlexSans-Regular.ttf")
    QtGui.QFontDatabase.applicationFontFamilies(_id)
    font = QtGui.QFont("IBM Plex Sans", 8)
    # QtGui.QFontDatabase.addApplicationFont("newfont.otf")   
    # font = QtGui.QFont("Disco Society - Personal Use", 10)
    app.setFont(font)


    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, white)  # Window background
    # palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.black)
    # palette.setColor(QtGui.QPalette.Base, white)
    # palette.setColor(QtGui.QPalette.AlternateBase, blue_2)
    palette.setColor(QtGui.QPalette.ToolTipBase, blue_7)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, black)
    # palette.setColor(QtGui.QPalette.Button, blue_3)  # blue_4

    # # palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.WindowText, gray)
    # palette.setColor(
    #     QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtCore.Qt.darkGray
    # )

    # # palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.Base, QtCore.Qt.gray)
    # # palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    # # palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)

    palette.setColor(QtGui.QPalette.Highlight, blue_7)
    palette.setColor(QtGui.QPalette.HighlightedText, white)

    # ### Dark Mode
    # palette_dark_mode = QtGui.QPalette()
    # palette_dark_mode.setColor(
    #     QtGui.QPalette.Window, QtGui.QColor(53, 53, 53)
    # )  # Window background
    # palette_dark_mode.setColor(QtGui.QPalette.WindowText, white)
    # palette_dark_mode.setColor(QtGui.QPalette.Text, white)
    # palette_dark_mode.setColor(QtGui.QPalette.Base, dark_gray)
    # palette_dark_mode.setColor(QtGui.QPalette.ToolTipBase, blue_7)
    # palette_dark_mode.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    # palette_dark_mode.setColor(QtGui.QPalette.ButtonText, white)
    # palette_dark_mode.setColor(QtGui.QPalette.HighlightedText, white)
    # palette_dark_mode.setColor(QtGui.QPalette.Highlight, blue_6)
    # palette_dark_mode.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Light, dark_gray)
    # palette_dark_mode.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, white)

    # try:
    #     with open(lama_settings_file, "r", encoding="utf8") as f:
    #         _dict = json.load(f)
    #     display_mode = _dict["display"]
    #     if display_mode == 1:
    #         app.setPalette(palette_dark_mode)
    #     else:
    #         app.setPalette(palette)
    # except FileNotFoundError:
    #     app.setPalette(palette)
    app.setPalette(palette)

    from lama_stylesheets import *
    app.setStyleSheet(StyleSheet_application)


    logo = os.path.join(
        path_programm, "_database", "_config", "icon", "LaMA_logo_full.png"
    )
    splash_pix = QtGui.QPixmap(logo)

    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    # splash.setGeometry(0,0,500,210)
    splash.setFixedHeight(160)
    splash.setWindowFlags(
        QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint
    )
    splash.setEnabled(False)
    # splash.setStyleSheet("background-color:white; color: black")
    # splash.setPalette(palette)
    # splash.setStyleSheet("QProgressBar::chunk {background-color: red}")

    # splash = QSplashScreen(splash_pix)
    # adding progress bar
    progressBar = QtWidgets.QProgressBar(splash)
    progressBar.setMaximum(46)
    progressBar.setGeometry(25, splash_pix.height() - 4, splash_pix.width() - 50, 20)

    # splash.setMask(splash_pix.mask())

    splash.show()

    def step_progressbar(i, text):
        progressBar.setValue(i)
        splash.showMessage(
            "{}.py".format(text), QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter
        )
        time.sleep(0.03)
        return i + 1

    i = 0

    app.processEvents()

    import time
    i = step_progressbar(i, "time")
    # Simulate something that takes time
    # i = step_progressbar(i, "threading")
    # import threading

    i = step_progressbar(i, "PyQt5")
    from PyQt5 import QtCore, QtWidgets, QtGui

    i = step_progressbar(i, "PyQt5.QtWidgets")
    from PyQt5.QtWidgets import QMainWindow

    i = step_progressbar(i, "pathlib")
    from pathlib import Path

    i = step_progressbar(i, "datetime")
    import datetime

    # i = step_progressbar(i, "json")
    # import json
    i = step_progressbar(i, "subprocess")
    import subprocess

    i = step_progressbar(i, "shutil")
    import shutil

    i = step_progressbar(i, "re")
    import re



    i = step_progressbar(i, "sys")
    import os

    i= step_progressbar(i, "requestes")
    import requests

    i = step_progressbar(i, "random")
    import random

    # i = step_progressbar(i, "functools")
    # import functools

    i = step_progressbar(i, "partial")
    from functools import partial

    # i = step_progressbar(i, "yaml")
    # import yaml

    # i = step_progressbar(i, "pillow")
    # from PIL import Image  ## pillow

    i = step_progressbar(i, "smtplib")
    import smtplib

    i = step_progressbar(i, "save_titlepage")
    from save_titlepage import check_format_titlepage_save

    i = step_progressbar(i, "git_sync")
    from git_sync import (
        check_internet_connection,
        check_branches,
    )

    i = step_progressbar(i, "create_new_widgets")
    from upload_database import action_push_database

    i = step_progressbar(i, "upload_database")
    from create_new_widgets import *

    i = step_progressbar(i, "list_of_widgets")
    from list_of_widgets import (
        widgets_search,
        widgets_create,
        widgets_sage,
        widgets_feedback,
        widgets_edit,
        widgets_search_cria,
        widgets_sage_cria,
        widgets_create_cria,
        widgets_edit_cria,
        widgets_feedback_cria,
        widgets_wizard,
        list_widgets,
    )

    # i = step_progressbar(i, "subwindows")
    # from subwindows import Ui_Dialog_Welcome_Window
    i = step_progressbar(i, "subwindows")
    from subwindows import Ui_Dialog_choose_type

    i = step_progressbar(i, "subwindows")
    from subwindows import Ui_Dialog_titlepage

    i = step_progressbar(i, "subwindows")
    from subwindows import Ui_Dialog_random_quiz

    i = step_progressbar(i, "subwindows")
    from subwindows import Ui_Dialog_ausgleichspunkte

    i = step_progressbar(i, "subwindows")
    from subwindows import Ui_Dialog_erstellen

    i = step_progressbar(i, "subwindows")
    from subwindows import Ui_Dialog_speichern

    i = step_progressbar(i, "subwindows")
    from subwindows import Ui_Dialog_variation

    i = step_progressbar(i, "subwindows")
    from subwindows import Ui_Dialog_setup

    i = step_progressbar(i, "subwindows")
    from subwindows import Ui_Dialog_developer

    i = step_progressbar(i, "subwindows")
    from subwindows import Ui_Dialog_draft_control

    i = step_progressbar(i, "subwindows")
    from subwindows import Ui_Dialog_Convert_To_Eps

    i = step_progressbar(i, "subwindows")
    from subwindows import Ui_Dialog_edit_worksheet_instructions
    i = step_progressbar(i, "subwindows")
    from subwindows import read_credentials

    i = step_progressbar(i, "translate")
    from translate import _fromUtf8, _translate

    i = step_progressbar(i, "create_pdf")
    from create_pdf import (
        create_tex,
        create_pdf,
        check_if_variation,
    )

    i = step_progressbar(i, "refresh_ddb")
    from refresh_ddb import modification_date, refresh_ddb

    i = step_progressbar(i, "standard_dialog_windows")
    from standard_dialog_windows import (
        warning_window,
        question_window,
        critical_window,
        information_window,
        custom_window,
    )

    i = step_progressbar(i, "predefined_size_policy")
    from predefined_size_policy import *

    i = step_progressbar(i, "work_with_content")
    from work_with_content import (
        collect_content,
        split_aufgaben_content_new_format,
        split_aufgaben_content,
        prepare_content_for_hide_show_items,
    )

    i = step_progressbar(i, "build_titlepage")
    from build_titlepage import get_titlepage_vorschau, check_if_hide_all_exists

    i = step_progressbar(i, "prepare_content_vorschau")
    from prepare_content_vorschau import (
        edit_content_ausgleichspunkte,
        edit_content_hide_show_items,
        copy_logo_to_target_path,
        copy_included_images,
    )

    i = step_progressbar(i, "setup_gui")
    from lama_gui import (
        setup_MenuBar,
        setup_stackSearch,
        setup_stackSage,
        setup_stackCreator,
        setup_stackFeedback,
        setup_stackWizard,
    )
    # i = step_progressbar(i, "convert_image_to_eps")
    # from convert_image_to_eps import convert_image_to_eps

    # i = step_progressbar(i, "lama_stylesheets")
    

    i = step_progressbar(i, "processing_window")
    from processing_window import Ui_Dialog_processing, Ui_ProgressBar

    i = step_progressbar(i, "bcrpyt")
    import bcrypt

    i = step_progressbar(i, "tinydb")

    from tinydb import Query

    i = step_progressbar(i, "database_commands")

    from sort_items import order_gesammeltedateien

    i = step_progressbar(i, "sort_items")

    from database_commands import (
        _database,
        _local_database,
        _database_addon,
        get_aufgabe_total,
        get_aufgabentyp,
        add_file,
        get_table,
        delete_file,
    )

    i = step_progressbar(i, "worksheet_wizard")
    from worksheet_wizard import (
        dict_widgets_wizard, themen_worksheet_wizard,
        get_all_solution_pixels,
        get_max_pixels_nonogram,
        create_latex_worksheet, 
        create_list_of_examples_addition, create_single_example_addition,
        create_list_of_examples_subtraction, create_single_example_subtraction,
        create_list_of_examples_multiplication, create_single_example_multiplication,
        create_list_of_examples_division, create_single_example_division,
        create_list_of_examples_ganze_zahlen, create_single_example_ganze_zahlen_strich, create_single_example_ganze_zahlen_punkt, create_single_example_ganze_zahlen_grundrechnungsarten,
        create_nonogramm, create_coordinates, get_random_solution,list_all_pixels, all_nonogramms, show_all_nonogramms
    )

    i = step_progressbar(i, "tex_minimal")
    from tex_minimal import *

    i = step_progressbar(i, "filter_comands")
    from filter_commands import get_filter_string, filter_items, get_drafts

    i = step_progressbar(i, "mainwindow")

    try:
        loaded_lama_file_path = sys.argv[1]
    except IndexError:
        loaded_lama_file_path = ""

    i = step_progressbar(i, "mainwindow")



    # try:
    MainWindow = QMainWindow()
    # MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    i = step_progressbar(i, "mainwindow")

    
    MainWindow = QMainWindow()
    # MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    screen_resolution = app.desktop().screenGeometry()
    screen_width, screen_height = screen_resolution.width(), screen_resolution.height()

    MainWindow.setGeometry(
        30, 30, round(screen_width * 0.5), round(screen_height * 0.85)
    )
    MainWindow.move(30, 30)
    i = step_progressbar(i, "mainwindow")

    
    ui = Ui_MainWindow()

    splash.finish(MainWindow)
    ui.setupUi(MainWindow)

    MainWindow.show()

    sys.exit(app.exec_())
    # except Exception as e:


    
