#!/usr/bin/python3
# -*- coding: utf-8 -*-
#### Version number ###
__version__ = "v3.2.2"
__lastupdate__ = "11/21"
##################

print("Loading...")

from start_window import check_if_database_exists

check_if_database_exists()
from prepare_content_vorschau import (
    edit_content_ausgleichspunkte,
    edit_content_hide_show_items,
)
from git_sync import git_reset_repo_to_origin
from standard_dialog_windows import question_window
from config import *
from lama_colors import *
import time
from create_new_widgets import add_action
import json

from config_start import (
    path_programm,
    path_home,
    path_localappdata_lama,
    lama_settings_file,
    database,
    lama_developer_credentials,
)
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
import os

# from tinydb import Query
import requests


class Worker_CleanUp(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    @QtCore.pyqtSlot()
    def task(self, ui):
        #### WORKING
        Ui_MainWindow.dict_missing_files = Ui_MainWindow().file_clean_up(ui)

        ui.label.setText("Nicht verwendete Bilder werden gesucht ...")
        list_unused_images = Ui_MainWindow().image_clean_up(ui)

        Ui_MainWindow.dict_missing_files['Nicht verwendete Bilder'] = list_unused_images

        self.finished.emit()

class Worker_UpdateDatabase(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    @QtCore.pyqtSlot()
    def task(self):
        Ui_MainWindow.reset_successfull = git_reset_repo_to_origin()
        # print(Ui_MainWindow.reset_successfull)
        self.finished.emit()


class Worker_LoadLamaFile(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    @QtCore.pyqtSlot()
    def task(self, MainWindow, ui):
        for aufgabe in MainWindow.list_alle_aufgaben_sage:
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
        # self.dict_alle_aufgaben_sage = {}
        self.list_alle_aufgaben_sage = []
        self.dict_widget_variables = {}
        self.list_selected_topics_creator = []
        self.dict_variablen_punkte = {}
        self.dict_variablen_abstand = {}
        self.dict_variablen_label = {}
        self.dict_sage_ausgleichspunkte_chosen = {}
        self.dict_sage_hide_show_items_chosen = {}
        self.dict_sage_individual_change = {}
        self.dict_chosen_topics = {}
        self.list_copy_images = []
        self.dict_picture_path = {}

        hashed_pw = read_credentials()
        self.developer_mode_active = False
        self.no_saved_changes_sage = True

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

        try:
            self.lama_settings["database"]
        except KeyError:
            self.lama_settings["database"] = 2

        if self.lama_settings["database"] == 0:
            QtWidgets.QApplication.setOverrideCursor(
                QtGui.QCursor(QtCore.Qt.WaitCursor)
            )
            refresh_ddb(self)
            QtWidgets.QApplication.restoreOverrideCursor()
        else:
            database_file = os.path.join(database, ".git", "index")
            refresh_date_ddb= modification_date(database_file).strftime("%Y%m%d")
            refresh_date_ddb_month = modification_date(database_file).strftime("%m")
            today = datetime.datetime.today().strftime("%Y%m%d")
            today_month = datetime.datetime.today().strftime("%m")

            difference = int(today) - int(refresh_date_ddb)
            # print(difference)
            # print(today_month)
            # print(refresh_date_ddb_month)
            if (self.lama_settings["database"] == 1 and difference != 0) or (self.lama_settings["database"] == 2 and difference > 6) or (self.lama_settings["database"] == 3 and refresh_date_ddb_month != today_month):
                QtWidgets.QApplication.setOverrideCursor(
                    QtGui.QCursor(QtCore.Qt.WaitCursor)
                )
                refresh_ddb(self)
                QtWidgets.QApplication.restoreOverrideCursor()


        self.chosen_gui = "widgets_search"
        if self.chosen_program == "cria":
            self.chosen_gui = self.chosen_gui + "_cria"


        ########################
        self.MainWindow = MainWindow
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)

        if self.chosen_program == "lama":
            MainWindow.setWindowTitle(
                _translate(
                    "LaMA - LaTeX Mathematik Assistent (Oberstufe)",
                    "LaMA - LaTeX Mathematik Assistent (Oberstufe)",
                    None,
                )
            )
            MainWindow.setWindowIcon(QtGui.QIcon(logo_path))
        if self.chosen_program == "cria":
            MainWindow.setWindowTitle(
                _translate(
                    "LaMA Cria - LaTeX Mathematik Assistent (Unterstufe)",
                    "LaMA Cria - LaTeX Mathematik Assistent (Unterstufe)",
                    None,
                )
            )
            MainWindow.setWindowIcon(QtGui.QIcon(logo_cria_path))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.gridLayout = create_new_gridlayout(self.centralwidget)
        # self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        # self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        #######################################################
        ############ Menu Bar ###################

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 950, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuBar.setStyleSheet("QMenu::item:disabled{color: gray}")
        # self.menuDateityp = QtWidgets.QMenu(self.menuBar)
        # self.menuDateityp.setObjectName(_fromUtf8("menuDateityp"))
        self.menuDatei = QtWidgets.QMenu(self.menuBar)
        self.menuDatei.setObjectName(_fromUtf8("menuDatei"))
        self.menuNeu = QtWidgets.QMenu(self.menuBar)
        self.menuNeu.setObjectName(_fromUtf8("menuNeu"))
        self.menuSage = QtWidgets.QMenu(self.menuBar)
        self.menuSage.setObjectName(_fromUtf8("menuSage"))
        self.menuSuche = QtWidgets.QMenu(self.menuBar)
        self.menuSuche.setObjectName(_fromUtf8("menuSuche"))
        self.menuFeedback = QtWidgets.QMenu(self.menuBar)
        self.menuFeedback.setObjectName(_fromUtf8("menuFeedback"))
        self.menuOptionen = QtWidgets.QMenu(self.menuBar)
        self.menuOptionen.setObjectName(_fromUtf8("menuOptionen"))
        self.menuOptionen.setTitle("Optionen")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuUpdate = QtWidgets.QMenu(self.menuHelp)
        self.menuUpdate.setObjectName(_fromUtf8("menuUpdate"))
        self.menuUpdate.setTitle("Update...")
        self.menuDeveloper = QtWidgets.QMenu(self.menuBar)
        self.menuDeveloper.setObjectName(_fromUtf8("menuDeveloper"))

        # self.menuDraftControl = QtWidgets.QMenu(self.menuDeveloper)
        # self.menuDraftControl.setObjectName(_fromUtf8("menuDraftControl"))
        # self.menuDeveloper.setStyleSheet("background-color: {};".format(get_color(blue_4)))

        # self.menuBild_einbinden = QtWidgets.QMenu(self.menuBar)
        # self.menuBild_einbinden.setObjectName(_fromUtf8("menuBild_einbinden"))
        MainWindow.setMenuBar(self.menuBar)

        # self.actionReset_creator = add_action(self.menuDatei, "Reset", self.suchfenster_reset)
        # self.actionReset.setShortcut("F4")

        self.actionRefresh_Database = add_action(
            MainWindow,
            self.menuDatei,
            "Datenbank aktualisieren",
            self.action_refreshddb_selected,
        )
        self.actionRefresh_Database.setShortcut("F5")

        # self.menuDatei.addSeparator()

        self.actionPush_Database = add_action(
            MainWindow,
            self.menuDeveloper,
            "Datenbank hochladen",
            self.push_full_database,
        )

        self.actionPush_Database = add_action(
            MainWindow,
            self.menuDeveloper,
            "Entwürfe prüfen",
            self.draft_control,
        )

        self.actionPush_Database = add_action(
            MainWindow,
            self.menuDeveloper,
            "Datenbank aufräumen",
            self.database_clean_up,
        )

        self.menuDatei.addSeparator()

        self.actionBild_convert_image_eps = add_action(
            MainWindow,
            self.menuDatei,
            "Grafik zu eps-Datei konvertieren",
            self.convert_image_eps_clicked,
        )

        self.menuDatei.addSeparator()

        if self.chosen_program == "lama":
            program = "LaMA Cria (Unterstufe)"
        if self.chosen_program == "cria":
            program = "LaMA (Oberstufe)"
        self.actionProgram = add_action(
            MainWindow,
            self.menuDatei,
            'Zu "{}" wechseln'.format(program),
            self.change_program,
        )

        self.actionExit = add_action(MainWindow, self.menuDatei, "Exit", self.exit_pressed)


        self.actionSuche = add_action(
            MainWindow,
            self.menuSuche,
            "Aufgaben suchen...",
            partial(self.update_gui, "widgets_search"),
        )
        # self.actionSuche.setVisible(False)
        self.actionSuche.setEnabled(False)
        self.actionSuche.setShortcut("F1")

        self.menuSuche.addSeparator()

        self.actionReset = add_action(
            MainWindow, self.menuSuche, "Reset", self.suchfenster_reset
        )
        self.actionReset.setShortcut("F4")

        self.actionSage = add_action(
            MainWindow,
            self.menuSage,
            "Prüfung erstellen...",
            partial(self.update_gui, "widgets_sage"),
        )
        self.actionSage.setShortcut("F2")

        self.menuSage.addSeparator()

        self.actionSave = add_action(
            MainWindow, self.menuSage, "Prüfung speichern", self.sage_save
        )
        self.actionSave.setEnabled(False)
        self.actionSave.setShortcut("Ctrl+S")

        self.actionLoad = add_action(
            MainWindow, self.menuSage, "Prüfung laden", self.sage_load
        )
        # self.actionLoad.setEnabled(False)
        self.actionLoad.setShortcut("Ctrl+O")

        self.menuSage.addSeparator()

        self.actionRestore_sage = add_action(
            MainWindow, self.menuSage, "", partial(self.sage_load, autosave=True)
        )
        self.update_label_restore_action()

        self.actionReset_sage = add_action(
            MainWindow, self.menuSage, "Reset Prüfung", partial(self.reset_sage, True)
        )
        self.actionReset_sage.setEnabled(False)
        # self.actionReset_sage.setVisible(False)

        self.actionNeu = add_action(
            MainWindow,
            self.menuNeu,
            "Neue Aufgabe zur Datenbank hinzufügen...",
            self.action_add_file,
        )
        self.actionNeu.setShortcut("F3")

        # self.menuNeu.addSeparator()

        if self.developer_mode_active == True:
            label_action_edit = "Aufgabe bearbeiten"
        else:
            label_action_edit = "Lokal gespeicherte Aufgabe bearbeiten"
        self.actionEdit_Files = add_action(
            MainWindow, self.menuNeu, label_action_edit, self.action_edit_files
        )
        # self.actionBild_einbinden = add_action(
        #     MainWindow, self.menuBild_einbinden, "Durchsuchen...", self.btn_add_image_pressed
        # )

        self.actionFeedback = add_action(
            MainWindow,
            self.menuFeedback,
            "Feedback oder Fehler senden...",
            partial(self.update_gui, "widgets_feedback"),
        )

        self.actionEinstellungen = add_action(
            MainWindow, self.menuOptionen, "LaMA konfigurieren ...", self.open_setup
        )

        self.actionUpdate_srdpmathematik = add_action(
            MainWindow,
            self.menuUpdate,
            '"srdp-mathematik.sty" aktualisieren',
            self.update_style_package,
        )

        # self.actionUpdate_tabu = add_action(
        #     MainWindow,
        #     self.menuUpdate,
        #     '"tabu.sty" aktualisieren',
        #     partial(self.update_style_package, "tabu.sty"),
        # )

        self.menuOptionen.addAction(self.menuUpdate.menuAction())

        self.actionInfo = add_action(
            MainWindow, self.menuHelp, "Über LaMA", self.show_info
        )
        self.actionSupport = add_action(
            MainWindow, self.menuHelp, "LaMA unterstützen", self.show_support
        )



        if self.developer_mode_active == True:
            label = "Entwicklermodus (aktiv)"
        else:
            label = "Entwicklermodus"

        self.actionDeveloper = add_action(
            MainWindow, self.menuOptionen, label, self.activate_developermode
        )

        # self.menuOptionen.addSeparator()

        # self.actionComplete_reset = add_action(MainWindow, self.menuOptionen, "LaMA vollständig zurücksetzen", self.complete_reset)

        self.menuBar.addAction(self.menuDatei.menuAction())
        self.menuBar.addAction(self.menuSuche.menuAction())
        # self.menuBar.addAction(self.menuDateityp.menuAction())
        self.menuBar.addAction(self.menuSage.menuAction())
        self.menuBar.addAction(self.menuNeu.menuAction())
        self.menuBar.addAction(self.menuFeedback.menuAction())
        self.menuBar.addAction(self.menuOptionen.menuAction())

        if self.developer_mode_active == True:
            self.menuBar.addAction(self.menuDeveloper.menuAction())

        self.menuBar.addAction(self.menuHelp.menuAction())

        self.groupBox_ausgew_gk = create_new_groupbox(
            self.centralwidget, "Ausgewählte Grundkompetenzen"
        )
        self.groupBox_ausgew_gk.setMaximumHeight(110)

        self.verticalLayout_2 = create_new_verticallayout(self.groupBox_ausgew_gk)
        # QtWidgets.QVBoxLayout(self.groupBox_ausgew_gk)
        # self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))

        self.scrollArea_ausgew_gk = QtWidgets.QScrollArea(self.groupBox_ausgew_gk)
        self.scrollArea_ausgew_gk.setWidgetResizable(True)
        self.scrollArea_ausgew_gk.setObjectName("scrollArea_ausgew_gk")
        self.scrollAreaWidgetContents_ausgew_gk = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_ausgew_gk.setObjectName(
            "scrollAreaWidgetContents_ausgew_gk"
        )

        self.verticalLayout_scrollA_ausgew_gk = create_new_verticallayout(
            self.scrollAreaWidgetContents_ausgew_gk
        )
        # QtWidgets.QVBoxLayout(
        #     self.scrollAreaWidgetContents_ausgew_gk
        # )
        # self.verticalLayout_scrollA_ausgew_gk.setObjectName(
        #     "verticalLayout_scrollA_ausgew_gk"
        # )

        self.label_ausgew_gk = create_new_label(self.scrollArea_ausgew_gk, "", True)
        self.verticalLayout_scrollA_ausgew_gk.addWidget(self.label_ausgew_gk)

        self.label_ausgew_gk_rest = create_new_label(self.scrollArea_ausgew_gk, "")

        self.verticalLayout_scrollA_ausgew_gk.addWidget(self.label_ausgew_gk_rest)

        self.scrollArea_ausgew_gk.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_ausgew_gk.setWidget(self.scrollAreaWidgetContents_ausgew_gk)
        self.verticalLayout_2.addWidget(self.scrollArea_ausgew_gk)

        self.gridLayout.addWidget(self.groupBox_ausgew_gk, 3, 0, 1, 1)

        self.groupBox_advanced_search = create_new_groupbox(
            self.centralwidget, "Erweiterte Suche:"
        )
        self.groupBox_advanced_search.setSizePolicy(SizePolicy_fixed_height)

        self.gridLayout_10 = create_new_gridlayout(self.groupBox_advanced_search)

        self.comboBox_suchbegriffe = create_new_combobox(self.groupBox_advanced_search)
        self.gridLayout_10.addWidget(self.comboBox_suchbegriffe, 0, 0, 1, 1)
        add_new_option(self.comboBox_suchbegriffe, 0, "")
        self.comboBox_suchbegriffe.currentIndexChanged.connect(
            self.comboBox_suchbegriffe_changed
        )

        i = 1
        suche_auswahl = ["Titel", "Inhalt", "Quelle", "Bilder"]
        for all in suche_auswahl:
            add_new_option(self.comboBox_suchbegriffe, i, all)
            i += 1

        self.entry_suchbegriffe = create_new_lineedit(self.groupBox_advanced_search)
        self.gridLayout_10.addWidget(self.entry_suchbegriffe, 0, 1, 1, 1)
        self.entry_suchbegriffe.setEnabled(False)

        self.gridLayout.addWidget(
            self.groupBox_advanced_search, 4, 1, 1, 1, QtCore.Qt.AlignTop
        )

        self.groupBox_klassen = create_new_groupbox(
            self.centralwidget, "Themen Schulstufe"
        )
        self.gridLayout_14 = create_new_gridlayout(self.groupBox_klassen)

        self.cb_k5 = create_new_checkbox(self.groupBox_klassen, "5. Klasse")
        self.gridLayout_14.addWidget(self.cb_k5, 0, 0, 1, 1)

        self.cb_k6 = create_new_checkbox(self.groupBox_klassen, "6. Klasse")
        self.gridLayout_14.addWidget(self.cb_k6, 1, 0, 1, 1)

        self.cb_k7 = create_new_checkbox(self.groupBox_klassen, "7. Klasse")
        self.gridLayout_14.addWidget(self.cb_k7, 0, 1, 1, 1)

        self.cb_k8 = create_new_checkbox(self.groupBox_klassen, "8. Klasse")
        self.gridLayout_14.addWidget(self.cb_k8, 1, 1, 1, 1)

        self.cb_mat = create_new_checkbox(self.groupBox_klassen, "Matura")
        self.gridLayout_14.addWidget(self.cb_mat, 0, 2, 1, 1)

        self.cb_univie = create_new_checkbox(self.groupBox_klassen, "Uni Wien")
        self.cb_univie.setToolTip(
            "Aufgaben mit dieser Kennzeichnung wurden im Rahmen einer Lehrveranstaltung auf der\nUniverstität Wien von Studierenden erstellt und von den Lehrveranstaltungsleitern evaluiert."
        )
        self.gridLayout_14.addWidget(self.cb_univie, 1, 2, 1, 1)
        self.cb_univie.hide()

        self.gridLayout.addWidget(self.groupBox_klassen, 3, 1, 1, 1)

        self.horizontalLayout_2 = create_new_horizontallayout()

        self.cb_solution = create_new_checkbox(self.centralwidget, "Lösungen", True)
        self.horizontalLayout_2.addWidget(self.cb_solution)
        self.cb_solution.setToolTip(
            "Die gesuchten Aufgaben werden inklusive der Lösungen angezeigt."
        )

        self.cb_show_variation = create_new_checkbox(
            self.centralwidget, "Aufgabenvariationen"
        )
        self.horizontalLayout_2.addWidget(self.cb_show_variation)
        self.cb_show_variation.setToolTip(
            "Es werden alle Aufgabenvariationen angezeigt."
        )

        self.cb_drafts = create_new_checkbox(self.centralwidget, "Entwürfe")
        self.horizontalLayout_2.addWidget(self.cb_drafts)
        self.cb_drafts.setToolTip(
            "Es werden auch eingereichte Aufgaben durchsucht, die bisher noch nicht auf Fehler überprüft\nund in die Datenbank aufgenommen wurden."
        )
        self.cb_drafts.toggled.connect(self.cb_drafts_enabled)

        self.cb_infos = create_new_checkbox(self.centralwidget, "Aufgabeninfos")
        self.horizontalLayout_2.addWidget(self.cb_infos)
        # self.gridLayout.addWidget(self.cb_show_variaton,5, 1,1,1)

        self.btn_suche = create_new_button(
            self.centralwidget, "Suche starten", partial(prepare_tex_for_pdf, self)
        )
        self.btn_suche.setShortcut(_translate("MainWindow", "Return", None))
        self.gridLayout.addWidget(self.btn_suche, 6, 1, 1, 1, QtCore.Qt.AlignRight)
        # self.horizontalLayout_2.addWidget(self.btn_suche)

        self.gridLayout.addLayout(self.horizontalLayout_2, 5, 1, 1, 1)

        # self.label_update = create_new_label(self.centralwidget, "")
        # self.label_update.setMaximumHeight(18)
        # self.horizontalLayout.addWidget(self.label_update)

        # self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.horizontalLayout_aufgabentyp = create_new_horizontallayout()

        self.label_aufgabentyp = create_new_label(self.centralwidget, "Aufgabentyp:")
        self.combobox_aufgabentyp = create_new_combobox(self.centralwidget)
        self.combobox_aufgabentyp.setSizePolicy(SizePolicy_fixed)
        add_new_option(self.combobox_aufgabentyp, 0, "Typ1")
        add_new_option(self.combobox_aufgabentyp, 1, "Typ2")
        self.combobox_aufgabentyp.currentIndexChanged.connect(
            self.chosen_aufgabenformat_typ
        )
        self.horizontalLayout_aufgabentyp.addWidget(self.label_aufgabentyp)
        self.horizontalLayout_aufgabentyp.addWidget(
            self.combobox_aufgabentyp, QtCore.Qt.AlignLeft
        )

        # self.horizontalspacer_at = QtWidgets.QSpacerItem(
        #     40, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        # )
        # self.horizontalLayout_aufgabentyp.addSpacerItem(self.horizontalspacer_at)
        self.horizontalLayout_aufgabentyp.addStretch()  ## problem with creator gui
        self.label_aufgabentyp.setMaximumHeight(18)

        self.gridLayout.addLayout(self.horizontalLayout_aufgabentyp, 0, 0, 1, 1)

        self.combobox_searchtype = create_new_combobox(self.centralwidget)
        self.combobox_searchtype.setMinimumContentsLength(1)

        self.horizontalLayout_combobox = create_new_horizontallayout()
        add_new_option(
            self.combobox_searchtype,
            0,
            "Alle Dateien ausgeben, die zumindest ein Themengebiet enthalten",
        )
        if self.chosen_program == "lama":
            label = "Alle Dateien ausgeben, die ausschließlich diese Themengebiete enthalten"
        if self.chosen_program == "cria":
            label = "Alle Dateien ausgeben, die alle Themengebiete enthalten"

        add_new_option(self.combobox_searchtype, 1, label)

        self.horizontalLayout_combobox.addWidget(self.combobox_searchtype)

        self.gridLayout.addLayout(self.horizontalLayout_combobox, 0, 1, 1, 1)

        self.combobox_searchtype.hide()

        self.groupBox_themen_klasse = create_new_groupbox(
            self.centralwidget, "Themen Schulstufen"
        )

        self.verticalLayout = create_new_verticallayout(self.groupBox_themen_klasse)
        # QtWidgets.QVBoxLayout(self.groupBox_themen_klasse)
        # self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tab_widget_themen = QtWidgets.QTabWidget(self.groupBox_themen_klasse)
        if self.display_mode == 0:
            stylesheet = StyleSheet_tab_widget_themen
        else:
            stylesheet = StyleSheet_tab_widget_themen_dark_mode
        self.tab_widget_themen.setStyleSheet(stylesheet)

        # self.tabWidget.setStyleSheet(set_color_text(white))

        self.tab_widget_themen.setObjectName(_fromUtf8("tab_widget_themen"))
        self.verticalLayout.addWidget(self.tab_widget_themen)

        self.gridLayout.addWidget(self.groupBox_themen_klasse, 1, 1, 2, 1)

        self.groupBox_gk = create_new_groupbox(self.centralwidget, "Grundkompetenzen")

        self.gridLayout_11 = create_new_gridlayout(self.groupBox_gk)

        # QtWidgets.QGridLayout(self.groupBox_gk)
        # self.gridLayout_11.setObjectName(_fromUtf8("gridLayout_11"))
        self.tab_widget_gk = QtWidgets.QTabWidget(self.groupBox_gk)

        if self.display_mode == 0:
            stylesheet = StyleSheet_tabWidget
        else:
            stylesheet = StyleSheet_tabWidget_dark_mode
        self.tab_widget_gk.setStyleSheet(stylesheet)
        # self.tab_widget_gk.setStyleSheet(_fromUtf8("color: {0}".format(white)))
        # self.tab_widget_gk.setStyleSheet("QToolTip { color: white; background-color: rgb(47, 69, 80); border: 0px; }")
        # ))

        #
        self.tab_widget_gk.setObjectName(_fromUtf8("tab_widget_gk"))
        self.gridLayout_11.addWidget(self.tab_widget_gk, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_gk, 1, 0, 2, 1)

        # #### AG #####
        self.create_tab_checkboxes_gk(
            self.tab_widget_gk, "Algebra und Geometrie", ag_beschreibung, "search"
        )

        ### FA ###
        self.create_tab_checkboxes_gk(
            self.tab_widget_gk, "Funktionale Abhängigkeiten", fa_beschreibung, "search"
        )

        ### AN ###
        self.create_tab_checkboxes_gk(
            self.tab_widget_gk, "Analysis", an_beschreibung, "search"
        )

        ### WS ###
        self.create_tab_checkboxes_gk(
            self.tab_widget_gk,
            "Wahrscheinlichkeit und Statistik",
            ws_beschreibung,
            "search",
        )

        ######### Klassenthemen
        ### K5
        self.create_tab_checkboxes_themen(self.tab_widget_themen, "search")

        # ### K6
        # self.create_tab_checkboxes_themen(self.tab_widget_themen, "k6", "search")

        # ### K7
        # self.create_tab_checkboxes_themen(self.tab_widget_themen, "k7", "search")

        # ### K8
        # self.create_tab_checkboxes_themen(self.tab_widget_themen, "k8", "search")

        #### Warnung ### Hinweis ####
        self.label_warnung = QtWidgets.QLabel(self.centralwidget)
        self.label_warnung.setWordWrap(True)
        self.label_warnung.setObjectName(_fromUtf8("label_warnung"))
        color = get_color(red)
        self.label_warnung.setStyleSheet(
            _fromUtf8("border: 2px solid {};".format(color))
        )  # background-color: rgb(195, 58, 63)
        # self.label_warnung.setMaximumSize(QtCore.QSize(375, 16777215))
        self.label_warnung.setText(
            _translate(
                "MainWindow",
                "Achtung: Aufgrund neuer hilfreicher Befehle ist es notwendig, ein Update des srdp-mathematik-Pakets so bald wie möglich durchzuführen! Nähere Infos unter: lama.schule/update",
                None,
            )
        )
        self.gridLayout.addWidget(self.label_warnung, 6, 0, 1, 1)
        self.label_warnung.hide()
        #########################

        ##################################################################
        ################ LAMA CRIA SEARCH #################################
        ###################################################################

        self.groupBox_schulstufe_cria = create_new_groupbox(
            self.centralwidget, "Themen Schulstufe"
        )
        self.groupBox_schulstufe_cria.setMaximumSize(QtCore.QSize(450, 16777215))

        self.verticalLayout_cria = QtWidgets.QVBoxLayout(self.groupBox_schulstufe_cria)
        self.verticalLayout_cria.setObjectName("verticalLayout_cria")

        self.tabWidget_klassen_cria = QtWidgets.QTabWidget(
            self.groupBox_schulstufe_cria
        )
        if self.display_mode == 0:
            stylesheet = StyleSheet_tabWidget
        else:
            stylesheet = StyleSheet_tabWidget_dark_mode
        self.tabWidget_klassen_cria.setStyleSheet(stylesheet)

        self.tabWidget_klassen_cria.setMovable(False)
        self.tabWidget_klassen_cria.setObjectName("tabWidget_klassen_cria")
        # self.tabWidget_klassen_cria.setFocusPolicy(QtCore.Qt.NoFocus)

        # spacerItem_cria = QtWidgets.QSpacerItem(
        #     20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        # )
        for klasse in list_klassen:
            new_tab = add_new_tab(
                self.tabWidget_klassen_cria, "{}. Klasse".format(klasse[1])
            )

            if self.display_mode == 0:
                stylesheet = StyleSheet_new_tab
            else:
                stylesheet = StyleSheet_new_tab_dark_mode
            new_tab.setStyleSheet(stylesheet)
            new_gridlayout = QtWidgets.QGridLayout(new_tab)
            new_gridlayout.setObjectName("{}".format(new_gridlayout))

            new_scrollarea = QtWidgets.QScrollArea(new_tab)
            new_scrollarea.setObjectName("{}".format(new_scrollarea))
            new_scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
            new_scrollarea.setWidgetResizable(True)
            new_scrollareacontent = QtWidgets.QWidget()
            new_scrollareacontent.setGeometry(QtCore.QRect(0, 0, 264, 235))
            new_scrollareacontent.setObjectName("{}".format(new_scrollareacontent))

            new_verticallayout = QtWidgets.QVBoxLayout(new_scrollareacontent)
            new_verticallayout.setObjectName("{}".format(new_verticallayout))

            dict_klasse_name = eval("dict_{}_name".format(klasse))

            group_radiobutton = QtWidgets.QButtonGroup()
            for kapitel in dict_klasse_name:
                new_radiobutton = create_new_radiobutton(
                    new_scrollareacontent,
                    dict_klasse_name[kapitel] + " (" + kapitel + ")",
                )

                new_verticallayout.addWidget(new_radiobutton)
                new_radiobutton.toggled.connect(
                    partial(self.chosen_radiobutton, klasse, kapitel)
                )
                group_radiobutton.addButton(new_radiobutton)
                label = "radiobutton_kapitel_{0}_{1}".format(klasse, kapitel)
                self.dict_widget_variables[label] = new_radiobutton

            new_verticallayout.addStretch()

            btn_alle_kapitel = create_new_button(
                new_scrollareacontent,
                "alle Kapitel der {}. Klasse auswählen".format(klasse[1]),
                partial(self.btn_alle_kapitel_clicked, klasse),
            )
            if self.display_mode == 0:
                stylesheet = StyleSheet_button_check_all
            else:
                stylesheet = StyleSheet_button_check_all_dark_mode
            btn_alle_kapitel.setStyleSheet(stylesheet)
            new_verticallayout.addWidget(btn_alle_kapitel)
            # new_verticallayout.addItem(spacerItem_cria)

            new_scrollarea.setWidget(new_scrollareacontent)

            new_gridlayout.addWidget(new_scrollarea, 5, 0, 1, 1)

        self.groupBox_unterkapitel_cria = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_unterkapitel_cria.setObjectName("groupBox_unterkapitel_cria")
        self.groupBox_unterkapitel_cria.setTitle(
            _translate("MainWindow", "Unterkapitel", None)
        )
        self.gridLayout_11_cria = QtWidgets.QGridLayout(self.groupBox_unterkapitel_cria)
        self.gridLayout_11_cria.setObjectName("gridLayout_11_cria")
        self.gridLayout.addWidget(self.groupBox_unterkapitel_cria, 1, 1, 2, 1)

        self.tabWidget_klassen_cria.currentChanged.connect(
            self.tabWidget_klassen_cria_changed
        )

        self.scrollArea_unterkapitel_cria = QtWidgets.QScrollArea(
            self.groupBox_unterkapitel_cria
        )
        self.scrollArea_unterkapitel_cria.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_unterkapitel_cria.setWidgetResizable(True)
        self.scrollArea_unterkapitel_cria.setObjectName("scrollArea_unterkapitel")
        if self.display_mode == 0:
            stylesheet = StyleSheet_unterkapitel_cria
        else:
            stylesheet = StyleSheet_unterkapitel_cria_dark_mode
        self.scrollArea_unterkapitel_cria.setStyleSheet(stylesheet)
        self.scrollAreaWidgetContents_cria = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_cria.setGeometry(QtCore.QRect(0, 0, 320, 279))
        self.scrollAreaWidgetContents_cria.setObjectName(
            "scrollAreaWidgetContents_cria"
        )
        self.verticalLayout_4_cria = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents_cria
        )
        self.verticalLayout_4_cria.setObjectName("verticalLayout_4_cria")
        self.scrollArea_unterkapitel_cria.setWidget(self.scrollAreaWidgetContents_cria)
        self.gridLayout_11_cria.addWidget(self.scrollArea_unterkapitel_cria, 0, 0, 1, 1)

        self.label_unterkapitel_cria = create_new_label(
            self.scrollAreaWidgetContents_cria, ""
        )
        self.label_unterkapitel_cria.setStyleSheet("padding-bottom: 15px")
        self.verticalLayout_4_cria.addWidget(self.label_unterkapitel_cria)

        self.create_all_checkboxes_unterkapitel()

        self.verticalLayout_cria.addWidget(self.tabWidget_klassen_cria)
        self.gridLayout.addWidget(self.groupBox_schulstufe_cria, 1, 0, 2, 1)
        self.groupBox_ausgew_themen_cria = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_ausgew_themen_cria.setObjectName("groupBox_ausgew_themen_cria")
        self.gridLayout_12_cria = QtWidgets.QGridLayout(
            self.groupBox_ausgew_themen_cria
        )
        self.gridLayout_12_cria.setObjectName("gridLayout_12_cria")
        self.scrollArea_ausgew_themen_cria = QtWidgets.QScrollArea(
            self.groupBox_ausgew_themen_cria
        )
        self.scrollArea_ausgew_themen_cria.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_ausgew_themen_cria.setWidgetResizable(True)
        self.scrollArea_ausgew_themen_cria.setObjectName("scrollArea_ausgew_themen")

        self.scrollAreaWidgetContents_ausgew_themen_cria = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_ausgew_themen_cria.setGeometry(
            QtCore.QRect(0, 0, 320, 279)
        )
        self.scrollAreaWidgetContents_ausgew_themen_cria.setObjectName(
            "scrollAreaWidgetContents_ausgew_themen_cria"
        )
        self.scrollArea_ausgew_themen_cria.setWidget(
            self.scrollAreaWidgetContents_ausgew_themen_cria
        )
        self.gridLayout_12_cria.addWidget(
            self.scrollArea_ausgew_themen_cria, 0, 0, 1, 1
        )
        self.verticalLayout_2_cria = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents_ausgew_themen_cria
        )
        self.verticalLayout_2_cria.setObjectName("verticalLayout_2_cria")
        self.label_ausg_themen_cria = QtWidgets.QLabel(self.groupBox_ausgew_themen_cria)
        self.label_ausg_themen_cria.setWordWrap(False)
        self.label_ausg_themen_cria.setObjectName("label_ausg_themen_cria")
        self.label_ausg_themen_cria.setWordWrap(True)
        self.groupBox_ausgew_themen_cria.setTitle(
            _translate("MainWindow", "Ausgewählte Themen", None)
        )
        # self.groupBox_ausgew_themen_cria.setMaximumHeight(200)
        self.groupBox_ausgew_themen_cria.hide()
        self.verticalLayout_2_cria.addWidget(self.label_ausg_themen_cria)
        self.gridLayout.addWidget(self.groupBox_ausgew_themen_cria, 3, 1, 1, 1)
        self.groupBox_schulstufe_cria.hide()
        self.groupBox_unterkapitel_cria.hide()

        dict_klasse_1 = eval("dict_{}_name".format(list_klassen[0]))
        erstes_kapitel = list(dict_klasse_1.keys())[0]
        self.dict_widget_variables[
            "radiobutton_kapitel_{0}_{1}".format(list_klassen[0], erstes_kapitel)
        ].setChecked(True)

        ##############################################################
        ##################### CREATOR #########################################
        self.groupBox_aufgabentyp = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_aufgabentyp.setObjectName(_fromUtf8("groupBox_aufgabentyp"))
        self.groupBox_aufgabentyp.setSizePolicy(SizePolicy_fixed)
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_aufgabentyp)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))

        self.groupBox_variation_cr = create_new_groupbox(
            self.centralwidget, "Aufgabenvariation"
        )
        self.groupBox_variation_cr.setMaximumWidth(350)
        self.verticalLayout_variation = create_new_verticallayout(
            self.groupBox_variation_cr
        )

        self.button_variation_cr = create_new_button(
            self.groupBox_variation_cr,
            "Variation vorhandender Aufgabe...",
            partial(self.button_variation_cr_pressed, "creator"),
        )
        self.button_variation_cr.setMinimumWidth(0)
        self.verticalLayout_variation.addWidget(self.button_variation_cr)

        self.gridLayout.addWidget(self.groupBox_variation_cr, 0, 0, 1, 1)
        self.groupBox_variation_cr.hide()

        self.groupBox_choose_file = create_new_groupbox(
            self.centralwidget, "Aufgabe auswählen"
        )
        self.groupBox_choose_file.setMaximumWidth(350)
        self.verticalLayout_choose_file = create_new_verticallayout(
            self.groupBox_choose_file
        )

        self.button_choose_file = create_new_button(
            self.groupBox_choose_file,
            "Aufgabe suchen...",
            partial(self.button_variation_cr_pressed, "editor"),
        )
        self.button_choose_file.setMinimumWidth(0)
        self.verticalLayout_choose_file.addWidget(self.button_choose_file)

        self.gridLayout.addWidget(self.groupBox_choose_file, 0, 0, 1, 1)
        self.groupBox_choose_file.hide()

        self.groupBox_grundkompetenzen_cr = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_grundkompetenzen_cr.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.groupBox_grundkompetenzen_cr.setMaximumSize(QtCore.QSize(350, 16777215))
        self.groupBox_grundkompetenzen_cr.setObjectName(
            _fromUtf8("groupBox_grundkompetenzen_cr")
        )
        self.groupBox_grundkompetenzen_cr.setMaximumWidth(350)
        self.gridLayout_11_cr = QtWidgets.QGridLayout(self.groupBox_grundkompetenzen_cr)
        self.gridLayout_11_cr.setObjectName(_fromUtf8("gridLayout_11_cr"))
        self.tab_widget_gk_cr = QtWidgets.QTabWidget(self.groupBox_grundkompetenzen_cr)

        if self.display_mode == 0:
            stylesheet = StyleSheet_tabWidget
        else:
            stylesheet = StyleSheet_tabWidget_dark_mode
        self.tab_widget_gk_cr.setStyleSheet(stylesheet)
        #     _fromUtf8("background-color: rgb(217, 255, 215);")
        # )
        self.tab_widget_gk_cr.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tab_widget_gk_cr.setObjectName(_fromUtf8("tab_widget_gk_cr"))
        self.gridLayout_11_cr.addWidget(self.tab_widget_gk_cr, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_grundkompetenzen_cr, 1, 0, 5, 1)
        self.groupBox_grundkompetenzen_cr.setTitle(
            _translate("MainWindow", "Grundkompetenzen", None)
        )
        self.groupBox_grundkompetenzen_cr.hide()

        self.groupBox_themengebiete_cria = QtWidgets.QGroupBox(self.centralwidget)

        self.groupBox_themengebiete_cria.setObjectName(
            _fromUtf8("groupBox_themengebiete_cria")
        )
        self.groupBox_themengebiete_cria.setMaximumWidth(350)
        self.gridLayout_11_cr_cria = QtWidgets.QGridLayout(
            self.groupBox_themengebiete_cria
        )
        self.gridLayout_11_cr_cria.setObjectName(_fromUtf8("gridLayout_11_cr_cria"))
        self.tab_widget_cr_cria = QtWidgets.QTabWidget(self.groupBox_themengebiete_cria)
        # self.tab_widget_gk_cr.setStyleSheet(_fromUtf8("background-color: rgb(217, 255, 215);")
        if self.display_mode == 0:
            stylesheet = StyleSheet_tabWidget
        else:
            stylesheet = StyleSheet_tabWidget_dark_mode
        self.tab_widget_cr_cria.setStyleSheet(stylesheet)

        # self.tab_widget_cr_cria.setStyleSheet("background-color: rgb(229, 246, 255);")
        self.tab_widget_cr_cria.setObjectName(_fromUtf8("tab_widget_cr_cria"))
        self.tab_widget_cr_cria.setFocusPolicy(QtCore.Qt.NoFocus)
        self.gridLayout_11_cr_cria.addWidget(self.tab_widget_cr_cria, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_themengebiete_cria, 1, 0, 5, 1)
        self.groupBox_themengebiete_cria.setTitle(
            _translate("MainWindow", "Themengebiete", None)
        )
        self.groupBox_themengebiete_cria.hide()

        for klasse in list_klassen:
            name = "tab_{0}".format(klasse)
            new_tab = add_new_tab(
                self.tab_widget_cr_cria, "{}. Klasse".format(klasse[1])
            )
            if self.display_mode == 0:
                stylesheet = StyleSheet_new_tab
            else:
                stylesheet = StyleSheet_new_tab_dark_mode
            new_tab.setStyleSheet(stylesheet)
            new_gridlayout = QtWidgets.QGridLayout(new_tab)
            new_gridlayout.setObjectName("{}".format(new_gridlayout))

            new_scrollarea = QtWidgets.QScrollArea(new_tab)
            new_scrollarea.setObjectName("{}".format(new_scrollarea))
            new_scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
            new_scrollarea.setFocusPolicy(QtCore.Qt.NoFocus)
            new_scrollarea.setWidgetResizable(True)
            # new_scrollarea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            new_scrollareacontent = QtWidgets.QWidget()
            # new_scrollareacontent.setGeometry(QtCore.QRect(0, 0, 264, 235))
            new_scrollareacontent.setObjectName("{}".format(new_scrollareacontent))

            new_verticallayout = QtWidgets.QVBoxLayout(new_scrollareacontent)
            new_verticallayout.setObjectName("{}".format(new_verticallayout))

            combobox_kapitel = create_new_combobox(new_scrollareacontent)
            if self.display_mode == 0:
                stylesheet = StyleSheet_combobox_kapitel
            else:
                stylesheet = StyleSheet_combobox_kapitel_dark_mode
            combobox_kapitel.setStyleSheet(stylesheet)
            combobox_kapitel.setMinimumHeight(25)
            # combobox_kapitel.setSizePolicy(SizePolicy_fixed)
            self.dict_widget_variables[
                "combobox_kapitel_creator_cria_{}".format(klasse)
            ] = combobox_kapitel
            dict_klasse_name = eval("dict_{}_name".format(klasse))
            index = 0
            for kapitel in dict_klasse_name:
                add_new_option(
                    combobox_kapitel,
                    index,
                    dict_klasse_name[kapitel] + " (" + kapitel + ")",
                )
                index += 1
            combobox_kapitel.currentIndexChanged.connect(
                partial(
                    self.comboBox_kapitel_changed_cr,
                    new_scrollareacontent,
                    new_verticallayout,
                    klasse,
                )
            )

            new_verticallayout.addWidget(combobox_kapitel)

            dict_klasse = eval("dict_{}".format(klasse))
            kapitel = list(dict_klasse.keys())[0]

            for unterkapitel in dict_klasse[kapitel]:
                new_checkbox = create_new_checkbox(
                    new_scrollareacontent,
                    dict_unterkapitel[unterkapitel] + " (" + unterkapitel + ")",
                )
                new_checkbox.stateChanged.connect(
                    partial(
                        self.checkbox_unterkapitel_checked_creator_cria,
                        new_checkbox,
                        klasse,
                        kapitel,
                        unterkapitel,
                    )
                )
                self.dict_widget_variables[
                    "checkbox_unterkapitel_creator_{0}_{1}_{2}".format(
                        klasse, kapitel, unterkapitel
                    )
                ] = new_checkbox
                new_verticallayout.addWidget(new_checkbox)
                new_checkbox.setFocusPolicy(QtCore.Qt.NoFocus)

            # new_verticallayout.addStretch()
            # new_verticallayout.addItem(self.spacerItem_unterkapitel_creator_cria)
            new_verticallayout.addStretch()

            new_scrollarea.setWidget(new_scrollareacontent)

            new_gridlayout.addWidget(new_scrollarea, 5, 0, 1, 1)

        # self.comboBox_kapitel_changed_cr(new_scrollareacontent,new_verticallayout, )

        # #################################

        if self.chosen_program == "lama":
            titel = "Ausgewählte Grundkompetenzen"
        else:
            titel = "Ausgewählte Themen"
        self.groupBox_ausgew_gk_cr = create_new_groupbox(self.centralwidget, titel)

        self.groupBox_ausgew_gk_cr.setSizePolicy(SizePolicy_fixed_height)
        self.groupBox_ausgew_gk_cr.setMaximumWidth(350)

        self.verticalLayout_2 = create_new_verticallayout(self.groupBox_ausgew_gk_cr)

        self.label_ausgew_gk_creator = create_new_label(
            self.groupBox_ausgew_gk_cr, "", True
        )

        self.verticalLayout_2.addWidget(self.label_ausgew_gk_creator)
        self.gridLayout.addWidget(self.groupBox_ausgew_gk_cr, 6, 0, 1, 1)

        # self.label_ausgew_gk.setText(_translate("MainWindow", "", None))
        self.groupBox_ausgew_gk_cr.hide()

        self.groupBox_bilder = create_new_groupbox(
            self.centralwidget, "Bilder (klicken, um Bilder zu entfernen)"
        )
        self.groupBox_bilder.setMaximumWidth(350)
        self.groupBox_bilder.setSizePolicy(SizePolicy_maximum_height)
        self.gridLayout_13 = QtWidgets.QGridLayout(self.groupBox_bilder)
        self.gridLayout_13.setObjectName(_fromUtf8("gridLayout_13"))
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox_bilder)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFocusPolicy(QtCore.Qt.NoFocus)
        self.scrollAreaWidgetContents_bilder = QtWidgets.QWidget()

        self.scrollAreaWidgetContents_bilder.setObjectName(
            _fromUtf8("scrollAreaWidgetContents_bilder")
        )
        self.verticalLayout = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents_bilder
        )
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_bilder)
        self.gridLayout_13.addWidget(self.scrollArea, 1, 0, 1, 1)
        self.groupBox_bilder.setTitle(
            _translate("MainWindow", "Bilder (klicken, um Bilder zu entfernen)", None)
        )
        self.groupBox_bilder.setSizePolicy(SizePolicy_maximum_height)
        # self.label_bild_leer = QtWidgets.QLabel(self.scrollAreaWidgetContents_bilder)
        # self.label_bild_leer.setObjectName(_fromUtf8("label_bild_leer"))
        # self.verticalLayout.addWidget(self.label_bild_leer)
        # self.label_bild_leer.setText(_translate("MainWindow", "", None))
        # self.label_bild_leer.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.label_bild_leer.hide()
        self.gridLayout.addWidget(self.groupBox_bilder, 7, 0, 1, 1)

        self.btn_add_image = create_new_button(
            self.groupBox_bilder, "Hinzufügen", self.btn_add_image_pressed
        )
        self.verticalLayout.addWidget(self.btn_add_image)
        self.groupBox_bilder.hide()

        #### CREATE CHECKBOXES ####
        ##### AG #####
        self.create_tab_checkboxes_gk(
            self.tab_widget_gk_cr, "Algebra und Geometrie", ag_beschreibung, "creator"
        )

        # # #### FA ####
        self.create_tab_checkboxes_gk(
            self.tab_widget_gk_cr,
            "Funktionale Abhängigkeiten",
            fa_beschreibung,
            "creator",
        )

        # ##### AN ####
        self.create_tab_checkboxes_gk(
            self.tab_widget_gk_cr, "Analysis", an_beschreibung, "creator"
        )

        # ### WS ####
        self.create_tab_checkboxes_gk(
            self.tab_widget_gk_cr,
            "Wahrscheinlichkeit und Statistik",
            ws_beschreibung,
            "creator",
        )

        # ### 5. Klasse ###
        self.create_tab_checkboxes_themen(self.tab_widget_gk_cr, "creator")

        # # ### 6. Klasse ###
        # self.create_tab_checkboxes_themen(self.tab_widget_gk_cr, "k6", "creator")

        # # ### 7. Klasse ###
        # self.create_tab_checkboxes_themen(self.tab_widget_gk_cr, "k7", "creator")

        # # ### 8. Klasse ###
        # self.create_tab_checkboxes_themen(self.tab_widget_gk_cr, "k8", "creator")

        # self.groupBox_aufgabentyp.setMaximumSize(100, 60)
        self.comboBox_aufgabentyp_cr = QtWidgets.QComboBox(self.groupBox_aufgabentyp)
        self.comboBox_aufgabentyp_cr.setObjectName(_fromUtf8("comboBox_aufgabentyp_cr"))
        # self.comboBox_aufgabentyp_cr.setSizePolicy(SizePolicy_fixed)
        self.comboBox_aufgabentyp_cr.addItem(_fromUtf8(""))
        self.comboBox_aufgabentyp_cr.addItem(_fromUtf8(""))
        # self.comboBox_aufgabentyp_cr.currentIndexChanged.connect(self.comboBox_aufgabentyp_cr_changed)
        self.gridLayout_3.addWidget(self.comboBox_aufgabentyp_cr, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_aufgabentyp, 0, 1, 1, 1)
        self.groupBox_aufgabentyp.setTitle(
            _translate("MainWindow", "Aufgabentyp", None)
        )
        self.comboBox_aufgabentyp_cr.setItemText(
            0, _translate("MainWindow", "Typ 1", None)
        )
        self.comboBox_aufgabentyp_cr.setItemText(
            1, _translate("MainWindow", "Typ 2", None)
        )
        self.groupBox_aufgabentyp.hide()

        self.groupBox_punkte = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_punkte.setObjectName(_fromUtf8("groupBox_punkte"))
        self.groupBox_punkte.setSizePolicy(SizePolicy_fixed)
        # self.groupBox_punkte.setMaximumSize(80, 60)
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_punkte)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.spinBox_punkte = QtWidgets.QSpinBox(self.groupBox_punkte)
        self.spinBox_punkte.setProperty("value", 1)
        self.spinBox_punkte.setObjectName(_fromUtf8("spinBox_punkte"))

        self.spinBox_punkte.setSizePolicy(SizePolicy_fixed)
        self.gridLayout_6.addWidget(self.spinBox_punkte, 0, 0, 1, 1)

        self.groupBox_punkte.setTitle(_translate("MainWindow", "Punkte", None))
        self.groupBox_punkte.hide()

        self.groupBox_aufgabenformat = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_aufgabenformat.setObjectName(_fromUtf8("groupBox_aufgabenformat"))
        self.groupBox_aufgabenformat.setSizePolicy(SizePolicy_fixed)
        # self.groupBox_aufgabenformat.setSizePolicy(SizePolicy_minimum)
        # self.groupBox_aufgabenformat.setMaximumWidth(300)
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_aufgabenformat)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))

        self.comboBox_af = create_new_combobox(self.groupBox_aufgabenformat)
        add_new_option(self.comboBox_af, 0, "bitte auswählen")

        self.gridLayout_7.addWidget(self.comboBox_af, 0, 0, 1, 1)

        if self.chosen_program == "lama":
            self.gridLayout.addWidget(self.groupBox_punkte, 0, 2, 1, 1)
            self.gridLayout.addWidget(self.groupBox_aufgabenformat, 0, 3, 1, 1)
        if self.chosen_program == "cria":
            self.gridLayout.addWidget(self.groupBox_punkte, 0, 1, 1, 1)
            self.gridLayout.addWidget(self.groupBox_aufgabenformat, 0, 2, 1, 1)
        self.groupBox_aufgabenformat.setTitle(
            _translate("MainWindow", "Aufgabenformat", None)
        )

        i = 1
        for all in dict_aufgabenformate:
            add_new_option(self.comboBox_af, i, dict_aufgabenformate[all])

            if self.chosen_program == "lama" and i == 4:
                break
            else:
                i += 1

        self.groupBox_aufgabenformat.hide()
        self.label_keine_auswahl = QtWidgets.QLabel(self.groupBox_aufgabenformat)
        self.label_keine_auswahl.setObjectName(_fromUtf8("label_keine_auswahl"))
        self.label_keine_auswahl.setMinimumSize(QtCore.QSize(145, 0))
        self.gridLayout_7.addWidget(self.label_keine_auswahl)
        self.label_keine_auswahl.setText(
            _translate("MainWindow", "keine Auswahl nötig", None)
        )
        self.label_keine_auswahl.hide()

        self.groupBox_klassen_cr = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_klassen_cr.setObjectName(_fromUtf8("groupBox_klassen_cr"))
        self.groupBox_klassen_cr.setTitle(_translate("MainWindow", "Klasse", None))
        self.groupBox_klassen_cr.setSizePolicy(SizePolicy_fixed)
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox_klassen_cr)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.comboBox_klassen_cr = QtWidgets.QComboBox(self.groupBox_klassen_cr)
        self.comboBox_klassen_cr.setObjectName(_fromUtf8("comboBox_klassen_cr"))
        self.comboBox_klassen_cr.addItem("-")
        for all in Klassen:
            if all != "univie" and all != "mat":
                self.comboBox_klassen_cr.addItem(Klassen[all])

        self.gridLayout_8.addWidget(self.comboBox_klassen_cr, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_klassen_cr, 0, 4, 1, 1)

        self.groupBox_klassen_cr.hide()

        self.groupBox_abstand = create_new_groupbox(self.centralwidget, "Abstand")
        self.groupBox_abstand.setSizePolicy(SizePolicy_fixed)
        self.groupBox_abstand.setToolTip("Abstand unter der Aufgabe (in cm)")
        self.horizontalLayout_abstand = create_new_horizontallayout(
            self.groupBox_abstand
        )
        self.spinBox_abstand = create_new_spinbox(self.groupBox_abstand)
        self.horizontalLayout_abstand.addWidget(self.spinBox_abstand)
        self.gridLayout.addWidget(self.groupBox_abstand, 0, 5, 1, 1)
        self.groupBox_abstand.hide()

        self.groupBox_pagebreak = create_new_groupbox(
            self.centralwidget, "Seitenumbruch"
        )
        self.groupBox_pagebreak.setSizePolicy(SizePolicy_fixed)
        self.horizontalLayout_pagebreak = create_new_horizontallayout(
            self.groupBox_pagebreak
        )
        self.comboBox_pagebreak = create_new_combobox(self.groupBox_pagebreak)
        add_new_option(self.comboBox_pagebreak, 0, "nicht möglich")
        add_new_option(self.comboBox_pagebreak, 1, "möglich")
        self.horizontalLayout_pagebreak.addWidget(self.comboBox_pagebreak)
        self.gridLayout.addWidget(self.groupBox_pagebreak, 0, 6, 1, 1)
        self.groupBox_pagebreak.hide()

        self.cb_matura_tag = create_new_checkbox(self.centralwidget, "Matura")
        self.gridLayout.addWidget(self.cb_matura_tag, 0, 7, 1, 1)
        self.cb_matura_tag.hide()

        self.cb_no_grade_tag = create_new_checkbox(
            self.centralwidget, "klassen-\nunabhängig"
        )
        self.gridLayout.addWidget(self.cb_no_grade_tag, 0, 7, 1, 1)
        self.cb_no_grade_tag.hide()

        self.gridLayout.setRowStretch(7, 1)

        self.groupBox_titel_cr = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_titel_cr.setObjectName(_fromUtf8("groupBox_titel_cr"))
        self.groupBox_titel_cr.setSizePolicy(SizePolicy_fixed_height)
        # self.groupBox_titel_cr.setMaximumHeight(60)
        self.gridLayout_14 = QtWidgets.QGridLayout(self.groupBox_titel_cr)
        self.gridLayout_14.setObjectName(_fromUtf8("gridLayout_14"))
        self.lineEdit_titel = QtWidgets.QLineEdit(self.groupBox_titel_cr)
        self.lineEdit_titel.setObjectName(_fromUtf8("lineEdit_titel"))
        self.lineEdit_titel.textChanged.connect(self.check_admin_entry)
        self.gridLayout_14.addWidget(self.lineEdit_titel, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_titel_cr, 1, 1, 1, 7)
        self.groupBox_titel_cr.setTitle(_translate("MainWindow", "Titel", None))
        self.groupBox_titel_cr.hide()

        self.groupBox_beispieleingabe = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_beispieleingabe.setObjectName(
            _fromUtf8("groupBox_beispieleingabe")
        )
        # self.groupBox_beispieleingabe.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.gridLayout_10 = QtWidgets.QGridLayout(self.groupBox_beispieleingabe)
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.label = QtWidgets.QLabel(self.groupBox_beispieleingabe)
        color = get_color(red)
        self.label.setStyleSheet(_fromUtf8("border: 2px solid {};".format(color)))
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_10.addWidget(self.label, 0, 0, 1, 1)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.groupBox_beispieleingabe)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.plainTextEdit.setTabChangesFocus(True)
        self.gridLayout_10.addWidget(self.plainTextEdit, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_beispieleingabe, 2, 1, 5, 7)
        self.groupBox_beispieleingabe.setTitle(
            _translate("MainWindow", "Aufgabeneingabe", None)
        )
        self.label.setText(
            _translate(
                "MainWindow",
                "Info: Eingabe des Aufgabentextes zwischen \\begin{beispiel}...\\end{beispiel}",
                None,
            )
        )
        self.groupBox_beispieleingabe.hide()

        self.groupBox_quelle = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_quelle.setObjectName(_fromUtf8("groupBox_quelle"))
        # self.groupBox_quelle.setMaximumSize(QtCore.QSize(16777215, 60))
        # self.groupBox_quelle.setMaximumHeight(60)
        # self.groupBox_quelle.setSizePolicy(SizePolicy_fixed_height)
        self.gridLayout_18 = QtWidgets.QGridLayout(self.groupBox_quelle)
        self.gridLayout_18.setObjectName(_fromUtf8("gridLayout_18"))
        self.lineEdit_quelle = QtWidgets.QLineEdit(self.groupBox_quelle)
        self.lineEdit_quelle.setObjectName(_fromUtf8("lineEdit_quelle"))
        try:
            quelle = self.lama_settings["quelle"]
        except KeyError:
            quelle = ""

        self.lineEdit_quelle.setText(quelle)
        self.gridLayout_18.addWidget(self.lineEdit_quelle, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_quelle, 7, 1, 1, 7, QtCore.Qt.AlignTop)
        self.groupBox_quelle.setTitle(
            _translate(
                "MainWindow",
                "Quelle oder Autor (Vorname Nachname) - Eingabe: VorNac",
                None,
            )
        )
        self.groupBox_quelle.hide()

        self.horizontalLayout_buttons = create_new_horizontallayout()
        self.gridLayout.addLayout(self.horizontalLayout_buttons, 8, 1, 1, 7)

        self.horizontalLayout_buttons.addStretch()
        self.pushButton_save = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_save.setObjectName(_fromUtf8("pushButton_save"))
        self.pushButton_save.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_save.setSizePolicy(SizePolicy_fixed)
        self.horizontalLayout_buttons.addWidget(self.pushButton_save)
        self.pushButton_save.setText(_translate("MainWindow", "Speichern", None))

        # # self.pushButton_save.setShortcut(_translate("MainWindow", "Return", None))
        self.pushButton_save.hide()

        self.pushButton_vorschau_edit = create_new_button(
            self.centralwidget, "Vorschau", self.button_vorschau_edit_pressed
        )
        self.pushButton_vorschau_edit.setShortcut("Ctrl+Return")
        self.pushButton_vorschau_edit.setSizePolicy(SizePolicy_fixed)
        self.horizontalLayout_buttons.addWidget(self.pushButton_vorschau_edit)
        self.pushButton_vorschau_edit.hide()

        self.pushButton_delete_file = create_new_button(
            self.centralwidget, "Aufgabe löschen", self.button_delete_file_pressed
        )  #
        # self.pushButton_delete_file.setStyleSheet("color: red")
        self.pushButton_delete_file.setSizePolicy(SizePolicy_fixed)
        self.horizontalLayout_buttons.addWidget(self.pushButton_delete_file)
        self.pushButton_delete_file.hide()

        self.pushButton_save_as_variation_edit = create_new_button(
            self.centralwidget,
            "Als Variation einer anderen Aufgabe speichern",
            self.pushButton_save_as_variation_edit_pressed,
        )
        self.pushButton_save_as_variation_edit.setSizePolicy(SizePolicy_fixed)
        self.horizontalLayout_buttons.addWidget(self.pushButton_save_as_variation_edit)
        self.pushButton_save_as_variation_edit.hide()

        self.pushButton_save_edit = create_new_button(
            self.centralwidget, "Änderung speichern", self.button_save_edit_pressed
        )
        self.pushButton_save_edit.setSizePolicy(SizePolicy_fixed)
        self.pushButton_save_edit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontalLayout_buttons.addWidget(self.pushButton_save_edit)
        self.pushButton_save_edit.hide()

        self.lineEdit_titel.setFocus()
        self.tab_widget_gk.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #         ####################################################
        #         #####################################################
        #         ################# LaMA SAGE ####################
        #         #####################################################

        self.splitter_sage = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_sage.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_sage.setObjectName("splitter_sage")

        self.groupBox_alle_aufgaben = QtWidgets.QGroupBox(self.splitter_sage)
        self.groupBox_alle_aufgaben.setMinimumWidth(1)
        self.groupBox_alle_aufgaben.setObjectName("groupBox_alle_aufgaben")

        self.verticalLayout_sage = QtWidgets.QVBoxLayout(self.groupBox_alle_aufgaben)
        self.verticalLayout_sage.setObjectName("verticalLayout_sage")

        ##### ComboBox LaMA ####
        self.comboBox_at_sage = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
        self.comboBox_at_sage.setObjectName("comboBox_at_sage")
        self.comboBox_at_sage.addItem("")
        self.comboBox_at_sage.addItem("")
        self.verticalLayout_sage.addWidget(self.comboBox_at_sage)
        self.comboBox_at_sage.setItemText(0, _translate("MainWindow", "Typ 1", None))
        self.comboBox_at_sage.setItemText(1, _translate("MainWindow", "Typ 2", None))
        self.comboBox_at_sage.currentIndexChanged.connect(self.comboBox_at_sage_changed)
        self.comboBox_at_sage.setFocusPolicy(QtCore.Qt.ClickFocus)
        # self.comboBox_at_sage.hide()

        self.comboBox_gk = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
        self.comboBox_gk.setObjectName("comboBox_gk")
        list_comboBox_gk = ["", "AG", "FA", "AN", "WS", "Zusatzthemen"]
        index = 0
        for all in list_comboBox_gk:
            self.comboBox_gk.addItem("")
            self.comboBox_gk.setItemText(index, _translate("MainWindow", all, None))
            index += 1
        self.comboBox_gk.currentIndexChanged.connect(
            partial(self.comboBox_gk_changed, "sage")
        )
        self.comboBox_gk.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.verticalLayout_sage.addWidget(self.comboBox_gk)
        self.comboBox_gk_num = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
        self.comboBox_gk_num.setObjectName("comboBox_gk_num")
        self.comboBox_gk_num.currentIndexChanged.connect(
            partial(self.comboBox_gk_num_changed, "sage")
        )
        self.comboBox_gk_num.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.verticalLayout_sage.addWidget(self.comboBox_gk_num)

        ##### ComboBox LaMA Cria ####

        self.comboBox_klassen = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
        self.comboBox_klassen.setObjectName("comboBox_klassen")
        # self.comboBox_gk.addItem("")

        self.comboBox_klassen.addItem("")
        index = 1
        for all in list_klassen:
            self.comboBox_klassen.addItem("")

            self.comboBox_klassen.setItemText(
                index, _translate("MainWindow", all[1] + ". Klasse", None)
            )
            index += 1

        self.comboBox_klassen.currentIndexChanged.connect(
            partial(self.comboBox_klassen_changed, "sage")
        )

        self.comboBox_klassen.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.verticalLayout_sage.addWidget(self.comboBox_klassen)

        self.comboBox_kapitel = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
        self.comboBox_kapitel.setObjectName("comboBox_kapitel")
        # self.comboBox_kapitel.currentIndexChanged.connect(
        #     partial(self.comboBox_kapitel_changed, "sage")
        # )
        self.comboBox_kapitel.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.verticalLayout_sage.addWidget(self.comboBox_kapitel)

        self.comboBox_unterkapitel = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
        self.comboBox_unterkapitel.setObjectName("comboBox_unterkapitel")
        # self.comboBox_unterkapitel.currentIndexChanged.connect(
        #     partial(self.comboBox_unterkapitel_changed, "sage")
        # )
        self.comboBox_unterkapitel.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.verticalLayout_sage.addWidget(self.comboBox_unterkapitel)

        self.lineEdit_number = QtWidgets.QLineEdit(self.groupBox_alle_aufgaben)
        self.lineEdit_number.setObjectName("lineEdit_number")
        # self.lineEdit_number.setValidator(QtGui.QIntValidator())
        self.lineEdit_number.textChanged.connect(
            partial(self.lineEdit_number_changed, "sage")
        )
        self.verticalLayout_sage.addWidget(self.lineEdit_number)
        self.listWidget = QtWidgets.QListWidget(self.groupBox_alle_aufgaben)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_sage.addWidget(self.listWidget)
        self.listWidget.itemClicked.connect(self.nummer_clicked)
        # self.gridLayout.addWidget(self.groupBox_alle_aufgaben, 2, 0, 7, 1)

        # self.groupBox_alle_aufgaben.setTitle(_translate("MainWindow", "Aufgaben", None))
        # self.groupBox_alle_aufgaben.setMinimumWidth(280)
        # self.groupBox_alle_aufgaben.resize(self.groupBox_alle_aufgaben.sizeHint())

        self.groupBox_alle_aufgaben.hide()

        self.groupBox_sage = QtWidgets.QGroupBox(self.splitter_sage)
        self.groupBox_sage.setMinimumWidth(1)
        self.groupBox_sage.setObjectName("groupBox_sage")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_sage)
        self.gridLayout_5.setObjectName("gridLayout_5")
        # self.groupBox_sage.setTitle(
        #     _translate("MainWindow", "Erstellen", None)
        # )

        # self.checkBox_wiederholung = QtWidgets.QCheckBox(self.groupBox_sage)
        # self.checkBox_wiederholung.setObjectName("checkBox_wiederholung")
        # self.checkBox_wiederholung.setFocusPolicy(QtCore.Qt.ClickFocus)
        # self.gridLayout_5.addWidget(self.checkBox_wiederholung, 2, 4, 1, 2)
        # self.checkBox_wiederholung.setText(_translate("MainWindow", "Wiederholung", None))

        self.comboBox_pruefungstyp = QtWidgets.QComboBox(self.groupBox_sage)
        self.comboBox_pruefungstyp.setMinimumContentsLength(1)
        self.comboBox_pruefungstyp.setObjectName("comboBox_pruefungstyp")
        list_comboBox_pruefungstyp = [
            "Schularbeit",
            "Nachschularbeit",
            "Wiederholungsschularbeit",
            "Wiederholungsprüfung",
            "Grundkompetenzcheck",
            "Übungsblatt",
        ]
        # self.comboBox_pruefungstyp.setEditable(True)

        # if self.chosen_program == "lama":
        #     list_comboBox_pruefungstyp.append("Quiz")

        list_comboBox_pruefungstyp.append("Benutzerdefiniert")

        index = 0
        for all in list_comboBox_pruefungstyp:
            self.comboBox_pruefungstyp.addItem("")
            self.comboBox_pruefungstyp.setItemText(
                index, _translate("MainWindow", all, None)
            )
            index += 1
        self.comboBox_pruefungstyp.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.comboBox_pruefungstyp.setMinimumContentsLength(5)
        self.gridLayout_5.addWidget(self.comboBox_pruefungstyp, 0, 4, 1, 2)
        self.comboBox_pruefungstyp.currentIndexChanged.connect(
            self.comboBox_pruefungstyp_changed
        )
        # self.verticalLayout_sage.addWidget(self.comboBox_pruefungstyp)

        self.combobox_beurteilung = create_new_combobox(self.groupBox_sage)
        add_new_option(self.combobox_beurteilung, 0, "Notenschlüssel")
        add_new_option(self.combobox_beurteilung, 1, "Beurteilungsraster")
        add_new_option(self.combobox_beurteilung, 2, "keine Auswahl")
        self.combobox_beurteilung.currentIndexChanged.connect(self.notenanzeige_changed)
        # self.combobox_beurteilung.setMinimumContentsLength(1)
        self.gridLayout_5.addWidget(self.combobox_beurteilung, 1, 4, 1, 2)

        self.pushButton_titlepage = QtWidgets.QPushButton(self.groupBox_sage)
        self.pushButton_titlepage.setObjectName(_fromUtf8("pushButton_titlepage"))
        self.pushButton_titlepage.setText(
            _translate("MainWindow", "Titelblatt anpassen", None)
        )
        if self.chosen_program == "lama":
            self.gridLayout_5.addWidget(self.pushButton_titlepage, 2, 4, 1, 2)
        if self.chosen_program == "cria":
            self.gridLayout_5.addWidget(self.pushButton_titlepage, 2, 4, 1, 2)

        self.groupBox_default_pkt = QtWidgets.QGroupBox(self.groupBox_sage)
        self.groupBox_default_pkt.setObjectName("groupBox_default_pkt")
        # self.groupBox_default_pkt.setSizePolicy(SizePolicy_fixed_height)
        # self.groupBox_default_pkt.setMaximumSize(QtCore.QSize(120, 16777215))
        self.verticalLayout_default_pkt = QtWidgets.QVBoxLayout(
            self.groupBox_default_pkt
        )
        self.verticalLayout_default_pkt.setObjectName("verticalLayout_default_pkt")
        self.spinBox_default_pkt = SpinBox_noWheel(self.groupBox_default_pkt)
        self.spinBox_default_pkt.setSizePolicy(SizePolicy_minimum_fixed)
        self.spinBox_default_pkt.setValue(1)
        self.spinBox_default_pkt.setToolTip("0 = Punkte ausblenden")
        self.spinBox_default_pkt.setObjectName("spinBox_default_pkt")
        self.verticalLayout_default_pkt.addWidget(self.spinBox_default_pkt)
        self.spinBox_default_pkt.valueChanged.connect(self.update_default_pkt)
        self.gridLayout_5.addWidget(self.groupBox_default_pkt, 0, 3, 3, 1)

        self.groupBox_klasse = QtWidgets.QGroupBox(self.groupBox_sage)
        self.groupBox_klasse.setObjectName("groupBox_klasse")
        self.groupBox_klasse.setSizePolicy(SizePolicy_minimum_fixed)
        # self.groupBox_klasse.setMaximumSize(QtCore.QSize(200, 16777215))
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_klasse)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lineEdit_klasse = QtWidgets.QLineEdit(self.groupBox_klasse)
        self.lineEdit_klasse.setObjectName("lineEdit_klasse")
        self.lineEdit_klasse.setSizePolicy(SizePolicy_minimum_fixed)
        self.verticalLayout_4.addWidget(self.lineEdit_klasse)
        self.gridLayout_5.addWidget(self.groupBox_klasse, 0, 2, 3, 1)
        # self.groupBox_klasse.setMaximumSize(QtCore.QSize(90, 16777215))
        self.groupBox_datum = QtWidgets.QGroupBox(self.groupBox_sage)
        self.groupBox_datum.setObjectName("groupBox_datum")
        # self.groupBox_datum.setMinimumWidth(20)
        # self.groupBox_datum.setStyleSheet("padding-left: 10px")
        # self.groupBox_datum.setSizePolicy(SizePolicy_fixed)
        self.groupBox_datum.setSizePolicy(SizePolicy_fixed_height)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_datum)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.dateEdit = QtWidgets.QDateEdit(self.groupBox_datum)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit.setObjectName("dateEdit")
        if self.display_mode == 1:
            self.dateEdit.setStyleSheet(StyleSheet_calender_dark_mode)
        # self.dateEdit.setStyleSheet("""
        # QDateEdit {{
        #     border: 2px solid red;
        # }}
        # """)

        self.verticalLayout_5.addWidget(self.dateEdit)
        self.gridLayout_5.addWidget(self.groupBox_datum, 0, 1, 3, 1)
        # self.groupBox_datum.setMaximumSize(QtCore.QSize(140, 16777215))
        self.groupBox_nummer = QtWidgets.QGroupBox(self.groupBox_sage)
        self.groupBox_nummer.setObjectName("groupBox_nummer")
        self.groupBox_nummer.setSizePolicy(SizePolicy_minimum_fixed)
        self.groupBox_nummer.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
            )
        )
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_nummer)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.spinBox_nummer = QtWidgets.QSpinBox(self.groupBox_nummer)
        self.spinBox_nummer.setValue(1)
        self.spinBox_nummer.setObjectName("spinBox_nummer")
        self.spinBox_nummer.setToolTip("0 = keine Nummerierung")
        # self.groupBox_nummer.setMaximumSize(QtCore.QSize(90, 16777215))
        # self.radioButton_notenschl.setText(
        #     _translate("MainWindow", "Notenschlüssel", None)
        # )
        # self.radioButton_beurteilungsraster.setText(
        #     _translate("MainWindow", "Beurteilungsraster", None)
        # )
        self.groupBox_klasse.setTitle(_translate("MainWindow", "Klasse", None))
        self.groupBox_datum.setTitle(_translate("MainWindow", "Datum", None))
        self.groupBox_nummer.setTitle(_translate("MainWindow", "Nummer", None))
        self.groupBox_default_pkt.setTitle(
            _translate("MainWindow", "Typ1 Standard", None)
        )
        self.verticalLayout_6.addWidget(self.spinBox_nummer)
        self.gridLayout_5.addWidget(self.groupBox_nummer, 0, 0, 3, 1)
        # self.horizontalspacer = QtWidgets.QSpacerItem(
        #     20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        # )
        # self.gridLayout_5.addItem(self.horizontalspacer, 2, 4, 3, 1)
        # self.pushButton_vorschau = QtWidgets.QPushButton(self.groupBox_sage)
        # self.pushButton_vorschau.setMaximumSize(QtCore.QSize(77, 16777215))
        # self.pushButton_vorschau.setObjectName("pushButton_vorschau")
        # self.gridLayout_5.addWidget(self.pushButton_vorschau, 7, 3, 1, 1, QtCore.Qt.AlignRight)

        self.scrollArea_chosen = QtWidgets.QScrollArea(self.groupBox_sage)
        self.scrollArea_chosen.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.scrollArea_chosen.setWidgetResizable(True)
        self.scrollArea_chosen.setObjectName("scrollArea_chosen")
        self.scrollArea_chosen.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 389, 323))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.gridLayout_8 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.scrollArea_chosen.setWidget(self.scrollAreaWidgetContents_2)
        self.scrollArea_chosen.verticalScrollBar().rangeChanged.connect(
            self.change_scrollbar_position
        )
        # self.scrollArea_chosen.verticalScrollBar().rangeChanged.connect(
        #     lambda: self.scrollArea_chosen.verticalScrollBar().setValue(
        #         self.scrollArea_chosen.verticalScrollBar().maximum()
        #     )
        # )
        self.gridLayout_5.addWidget(self.scrollArea_chosen, 5, 0, 1, 6)


        self.sage_loading_progressbar = QtWidgets.QProgressBar(self.scrollAreaWidgetContents_2)
        self.sage_loading_progressbar.hide()
        self.gridLayout_8.addWidget(self.sage_loading_progressbar,0,0,1,1)



        self.groupBox_notenschl = create_new_groupbox(
            self.groupBox_sage, "Notenschlüssel"
        )
        # QtWidgets.QGroupBox(self.groupBox_sage)
        # self.groupBox_notenschl.setObjectName("groupBox_notenschl")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_notenschl)
        self.gridLayout_6.setObjectName("gridLayout_6")

        try:
            if self.chosen_program == 'cria':
                key = "prozente_cria"
            else:
                key = "prozente"

            sehr_gut = self.lama_settings[key][0]
            gut = self.lama_settings[key][1]
            befriedigend = self.lama_settings[key][2]
            genuegend = self.lama_settings[key][3]
        except KeyError:
            sehr_gut = 91
            gut = 80
            befriedigend = 64
            genuegend = 50

        self.label_sg = create_new_label(self.groupBox_notenschl, "Sehr Gut:")
        self.label_sg.setSizePolicy(SizePolicy_fixed)
        self.gridLayout_6.addWidget(self.label_sg, 0, 0, 1, 1)
        self.spinBox_2 = create_new_spinbox(self.groupBox_notenschl, sehr_gut)
        self.spinBox_2.setSizePolicy(SizePolicy_fixed)
        self.spinBox_2.valueChanged.connect(self.update_punkte)
        self.gridLayout_6.addWidget(self.spinBox_2, 0, 1, 1, 1)
        self.label_sg_pkt = create_new_label(self.groupBox_notenschl, "% (ab 0)")
        self.gridLayout_6.addWidget(self.label_sg_pkt, 0, 2, 1, 1)

        self.label_g = create_new_label(self.groupBox_notenschl, "Gut:")
        self.label_g.setSizePolicy(SizePolicy_fixed)
        self.gridLayout_6.addWidget(self.label_g, 0, 3, 1, 1)
        self.spinBox_3 = create_new_spinbox(self.groupBox_notenschl, gut)
        self.spinBox_3.setSizePolicy(SizePolicy_fixed)
        self.spinBox_3.valueChanged.connect(self.update_punkte)
        self.gridLayout_6.addWidget(self.spinBox_3, 0, 4, 1, 1)
        self.label_g_pkt = create_new_label(self.groupBox_notenschl, "% (ab 0)")
        self.gridLayout_6.addWidget(self.label_g_pkt, 0, 5, 1, 1)

        self.label_b = create_new_label(self.groupBox_notenschl, "Befriedigend:")
        self.label_b.setSizePolicy(SizePolicy_fixed)
        self.gridLayout_6.addWidget(self.label_b, 1, 0, 1, 1)
        self.spinBox_4 = create_new_spinbox(self.groupBox_notenschl, befriedigend)
        self.spinBox_4.setSizePolicy(SizePolicy_fixed)
        self.spinBox_4.valueChanged.connect(self.update_punkte)
        self.gridLayout_6.addWidget(self.spinBox_4, 1, 1, 1, 1)
        self.label_b_pkt = create_new_label(self.groupBox_notenschl, "% (ab 0)")
        self.gridLayout_6.addWidget(self.label_b_pkt, 1, 2, 1, 1)

        self.label_g_2 = create_new_label(self.groupBox_notenschl, "Genügend:")
        self.label_g_2.setSizePolicy(SizePolicy_fixed)
        self.gridLayout_6.addWidget(self.label_g_2, 1, 3, 1, 1)
        self.spinBox_5 = create_new_spinbox(self.groupBox_notenschl, genuegend)
        self.spinBox_5.setSizePolicy(SizePolicy_fixed)
        self.spinBox_5.valueChanged.connect(self.update_punkte)
        self.gridLayout_6.addWidget(self.spinBox_5, 1, 4, 1, 1)
        self.label_g_2_pkt = create_new_label(self.groupBox_notenschl, "% (ab 0)")
        self.gridLayout_6.addWidget(self.label_g_2_pkt, 1, 5, 1, 1)

        self.groupBox_notenschl_modus = create_new_groupbox(
            self.groupBox_notenschl, "Anzeige"
        )
        self.gridLayout_6.addWidget(self.groupBox_notenschl_modus, 0, 6, 2, 1)

        self.verticalLayout_ns_modus = create_new_verticallayout(
            self.groupBox_notenschl_modus
        )

        try:
            if self.chosen_program == 'cria':
                key = "notenschluessel_cria"
            else:
                key = "notenschluessel"
            ns_halbe_punkte_checked = self.lama_settings[key][0]
        except KeyError:
            ns_halbe_punkte_checked = False

        self.cb_ns_halbe_pkt = create_new_checkbox(
            self.groupBox_notenschl_modus,
            "Halbe Punkte",
            checked=ns_halbe_punkte_checked,
        )
        self.verticalLayout_ns_modus.addWidget(self.cb_ns_halbe_pkt)

        try:
            if self.chosen_program == 'cria':
                key = "notenschluessel_cria"
            else:
                key = "notenschluessel"
            ns_prozente_checked = self.lama_settings[key][1]
        except KeyError:
            ns_prozente_checked = False

        self.cb_ns_prozent = create_new_checkbox(
            self.groupBox_notenschl_modus, "Prozentangabe", checked=ns_prozente_checked
        )
        self.verticalLayout_ns_modus.addWidget(self.cb_ns_prozent)

        # self.cb_ns_NMS = create_new_checkbox(self.groupBox_notenschl_modus, "Modus: NMS")
        # self.verticalLayout_ns_modus.addWidget(self.cb_ns_NMS)

        self.gridLayout_5.addWidget(self.groupBox_notenschl, 6, 0, 1, 6)

        ### Groupbox Beurteilungsraster #####

        self.groupBox_beurteilungsraster = QtWidgets.QGroupBox(self.groupBox_sage)
        self.groupBox_beurteilungsraster.setObjectName("groupBox_beurteilungsraster")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_beurteilungsraster)
        self.gridLayout_6.setObjectName("gridLayout_6")

        self.label_typ1_pkt = QtWidgets.QLabel(self.groupBox_beurteilungsraster)
        self.label_typ1_pkt.setObjectName("label_typ1_pkt")
        self.gridLayout_6.addWidget(self.label_typ1_pkt, 0, 0, 1, 2)
        # self.label_typ1_pkt.setText(_translate("MainWindow", "Punkte Typ 1: 0",None))

        self.label_typ2_pkt = QtWidgets.QLabel(self.groupBox_beurteilungsraster)
        self.label_typ2_pkt.setObjectName("label_typ2_pkt")
        self.gridLayout_6.addWidget(self.label_typ2_pkt, 1, 0, 1, 2)

        self.groupBox_beurteilungsraster.setTitle(
            _translate("MainWindow", "Beurteilungsraster", None)
        )

        self.gridLayout_5.addWidget(self.groupBox_beurteilungsraster, 6, 0, 1, 6)
        self.groupBox_beurteilungsraster.hide()

        ### Zusammenfassung d. SA ###
        if self.chosen_program == "lama":
            label = "Anzahl der Aufgaben: 0 (Typ1: 0 / Typ2: 0)"

        if self.chosen_program == "cria":
            label = "Anzahl der Aufgaben: 0"

        self.label_gesamtbeispiele = create_new_label(self.groupBox_sage, label, True)
        self.gridLayout_5.addWidget(self.label_gesamtbeispiele, 7, 0, 1, 2)

        self.label_gesamtpunkte = QtWidgets.QLabel(self.groupBox_sage)
        self.gridLayout_5.addWidget(self.label_gesamtpunkte, 8, 0, 1, 2)
        self.label_gesamtpunkte.setObjectName("label_gesamtpunkte")
        self.label_gesamtpunkte.setText(
            _translate("MainWindow", "Gesamtpunkte: 0", None)
        )

        self.cb_solution_sage = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_solution_sage.setObjectName(_fromUtf8("cb_solution"))
        self.cb_solution_sage.setText(
            _translate("MainWindow", "Lösungen anzeigen", None)
        )
        self.cb_solution_sage.setChecked(True)
        self.cb_solution_sage.setSizePolicy(SizePolicy_fixed)
        self.cb_solution_sage.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.gridLayout_5.addWidget(self.cb_solution_sage, 7, 3, 1, 2)

        # self.cb_show_variaton_sage = create_new_checkbox(self.centralwidget, "Aufgabenvariationen anzeigen")
        # self.gridLayout_5.addWidget(self.cb_show_variaton_sage, 8, 4, 1, 1)

        self.cb_drafts_sage = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_drafts_sage.setSizePolicy(SizePolicy_fixed)
        self.cb_drafts_sage.setObjectName(_fromUtf8("cb_drafts_sage"))
        self.gridLayout_5.addWidget(self.cb_drafts_sage, 8, 3, 1, 2)
        self.cb_drafts_sage.setText(_translate("MainWindow", "Entwürfe anzeigen", None))
        # self.horizontalLayout_2.addWidget(self.cb_drafts_sage)
        self.cb_drafts_sage.toggled.connect(self.cb_drafts_sage_enabled)

        self.pushButton_vorschau = QtWidgets.QPushButton(self.groupBox_sage)
        self.pushButton_vorschau.setSizePolicy(SizePolicy_fixed)
        # self.pushButton_vorschau.setMaximumSize(QtCore.QSize(90, 16777215))
        self.pushButton_vorschau.setObjectName("pushButton_vorschau")
        self.pushButton_vorschau.setText(_translate("MainWindow", "Vorschau", None))
        self.pushButton_vorschau.setShortcut(_translate("MainWindow", "Return", None))
        self.gridLayout_5.addWidget(
            self.pushButton_vorschau, 8, 5, 1, 1, QtCore.Qt.AlignRight
        )
        self.pushButton_vorschau.clicked.connect(
            partial(self.pushButton_vorschau_pressed, "vorschau")
        )
        self.pushButton_vorschau.setFocusPolicy(QtCore.Qt.ClickFocus)
        # self.gridLayout.addWidget(self.groupBox_sage, 1, 2, 8, 3)
        self.gridLayout.addWidget(self.splitter_sage, 0, 0, 8, 1)
        self.pushButton_erstellen = QtWidgets.QPushButton(self.groupBox_sage)
        self.pushButton_erstellen.setSizePolicy(SizePolicy_fixed)
        self.pushButton_erstellen.setObjectName("pushButton_erstellen")
        self.pushButton_erstellen.setText(_translate("MainWindow", "Erstellen", None))
        self.pushButton_erstellen.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.pushButton_erstellen.clicked.connect(self.pushButton_erstellen_pressed)
        self.gridLayout_5.addWidget(
            self.pushButton_erstellen, 9, 5, 1, 1, QtCore.Qt.AlignRight
        )
        self.groupBox_sage.hide()
        self.splitter_sage.hide()
        self.comboBox_klassen_changed("sage")

        self.comboBox_kapitel.currentIndexChanged.connect(
            partial(self.comboBox_kapitel_changed, "sage")
        )

        self.comboBox_unterkapitel.currentIndexChanged.connect(
            partial(self.comboBox_unterkapitel_changed, "sage")
        )

        ################################################################
        ################################################################
        ########### FEEDBACK #############################################
        #######################################################################

        self.label_example = QtWidgets.QLabel(self.centralwidget)
        self.label_example.setObjectName(_fromUtf8("label_example"))
        # self.label_update.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label_example.setText(
            _translate("MainWindow", "Ausgewählte Aufgabe: -", None)
        )
        self.gridLayout.addWidget(self.label_example, 0, 1, 1, 1)
        self.label_example.hide()

        self.groupBox_alle_aufgaben_fb = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_alle_aufgaben_fb.setMaximumWidth(250)

        self.groupBox_alle_aufgaben_fb.setObjectName("groupBox_alle_aufgaben_fb")
        self.verticalLayout_fb = QtWidgets.QVBoxLayout(self.groupBox_alle_aufgaben_fb)
        self.verticalLayout_fb.setObjectName("verticalLayout_fb")

        self.comboBox_at_fb = QtWidgets.QComboBox(self.groupBox_alle_aufgaben_fb)
        # self.comboBox_at_fb.setSizePolicy(SizePolicy_fixed)
        self.comboBox_at_fb.setObjectName("comboBox_at_fb")
        self.comboBox_at_fb.addItem("")
        self.comboBox_at_fb.addItem("")
        self.verticalLayout_fb.addWidget(self.comboBox_at_fb)

        self.comboBox_at_fb.setItemText(0, _translate("MainWindow", "Typ 1", None))
        self.comboBox_at_fb.setItemText(1, _translate("MainWindow", "Typ 2", None))
        self.comboBox_at_fb.addItem("")
        self.comboBox_at_fb.setItemText(
            2, _translate("MainWindow", "Allgemeine Rückmeldung", None)
        )
        # if self.chosen_program == 'cria':
        #     self.comboBox_at_fb.setItemText(0, _translate("MainWindow", "Aufgabenrückmeldung", None))
        #     self.comboBox_at_fb.setItemText(1, _translate("MainWindow", "Allgemeine Rückmeldung", None))
        self.comboBox_at_fb.currentIndexChanged.connect(self.comboBox_at_fb_changed)
        # self.comboBox_at_fb.setFocusPolicy(QtCore.Qt.ClickFocus)
        # self.comboBox_at_fb.hide()

        self.comboBox_fb = QtWidgets.QComboBox(self.groupBox_alle_aufgaben_fb)
        self.comboBox_fb.setObjectName("comboBox_fb")
        list_comboBox_fb = ["", "AG", "FA", "AN", "WS", "Zusatzthemen"]
        index = 0
        for all in list_comboBox_fb:
            self.comboBox_fb.addItem("")
            self.comboBox_fb.setItemText(index, _translate("MainWindow", all, None))
            index += 1
        self.comboBox_fb.currentIndexChanged.connect(
            partial(self.comboBox_gk_changed, "feedback")
        )
        self.comboBox_fb.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.verticalLayout_fb.addWidget(self.comboBox_fb)
        self.comboBox_fb_num = QtWidgets.QComboBox(self.groupBox_alle_aufgaben_fb)
        self.comboBox_fb_num.setObjectName("comboBox_gk_num")
        self.comboBox_fb_num.currentIndexChanged.connect(
            partial(self.comboBox_gk_num_changed, "feedback")
        )
        self.comboBox_fb_num.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.verticalLayout_fb.addWidget(self.comboBox_fb_num)
        self.lineEdit_number_fb = QtWidgets.QLineEdit(self.groupBox_alle_aufgaben_fb)
        self.lineEdit_number_fb.setObjectName("lineEdit_number_fb")
        self.lineEdit_number_fb.textChanged.connect(
            partial(self.lineEdit_number_changed, "feedback")
        )
        self.verticalLayout_fb.addWidget(self.lineEdit_number_fb)
        self.listWidget_fb = QtWidgets.QListWidget(self.groupBox_alle_aufgaben)
        self.listWidget_fb.setObjectName("listWidget_fb")
        self.verticalLayout_fb.addWidget(self.listWidget_fb)
        self.listWidget_fb.itemClicked.connect(self.nummer_clicked_fb)

        self.gridLayout.addWidget(self.groupBox_alle_aufgaben_fb, 0, 0, 8, 1)
        self.groupBox_alle_aufgaben_fb.setTitle(
            _translate("MainWindow", "Aufgaben", None)
        )
        self.groupBox_alle_aufgaben_fb.hide()

        #### Feedback Cria ####
        self.comboBox_at_fb_cria = QtWidgets.QComboBox()
        self.comboBox_at_fb_cria.setObjectName("comboBox_at_fb_cria")
        self.comboBox_at_fb_cria.addItem("Aufgabenrückmeldung")
        self.comboBox_at_fb_cria.addItem("Allgemeine Rückmeldung")
        self.comboBox_at_fb_cria.currentIndexChanged.connect(
            self.comboBox_at_fb_cria_changed
        )
        # if self.chosen_program == 'cria':
        #     self.comboBox_at_fb.setItemText(0, _translate("MainWindow", "Aufgabenrückmeldung", None))
        #     self.comboBox_at_fb.setItemText(1, _translate("MainWindow", "Allgemeine Rückmeldung", None))
        # self.comboBox_at_fb.currentIndexChanged.connect(self.comboBox_at_fb_changed)
        # self.comboBox_at_fb.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.gridLayout.addWidget(self.comboBox_at_fb_cria, 0, 0, 1, 1)
        self.comboBox_at_fb_cria.hide()

        self.groupBox_alle_aufgaben_fb_cria = QtWidgets.QGroupBox(self.centralwidget)
        # self.groupBox_alle_aufgaben_fb_cria.setMinimumWidth(100)
        self.groupBox_alle_aufgaben_fb_cria.setMaximumWidth(250)
        # self.groupBox_alle_aufgaben_fb_cria.setMinimumSize(QtCore.QSize(140, 16777215))
        # self.groupBox_alle_aufgaben_fb_cria.setMaximumSize(QtCore.QSize(200, 16777215))
        self.groupBox_alle_aufgaben_fb_cria.setObjectName(
            "groupBox_alle_aufgaben_fb_cria"
        )
        self.verticalLayout_fb_cria = QtWidgets.QVBoxLayout(
            self.groupBox_alle_aufgaben_fb_cria
        )
        self.verticalLayout_fb_cria.setObjectName("verticalLayout_fb_cria")
        self.comboBox_klassen_fb_cria = QtWidgets.QComboBox(
            self.groupBox_alle_aufgaben_fb_cria
        )
        self.comboBox_klassen_fb_cria.setObjectName("self.comboBox_klassen_fb_cria")

        self.comboBox_klassen_fb_cria.addItem("")
        i = 1
        for all in list_klassen:

            self.comboBox_klassen_fb_cria.addItem("")

            self.comboBox_klassen_fb_cria.setItemText(
                i,
                _translate("MainWindow", all[1] + ". Klasse", None),
            )
            i += 1

        self.comboBox_klassen_fb_cria.currentIndexChanged.connect(
            partial(self.comboBox_klassen_changed, "feedback")
        )

        self.comboBox_klassen_fb_cria.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.verticalLayout_fb_cria.addWidget(self.comboBox_klassen_fb_cria)
        self.comboBox_kapitel_fb_cria = QtWidgets.QComboBox(
            self.groupBox_alle_aufgaben_fb_cria
        )
        self.comboBox_kapitel_fb_cria.setObjectName("self.comboBox_kapitel_fb_cria")

        # self.comboBox_kapitel_fb_cria.currentIndexChanged.connect(
        #     partial(self.comboBox_kapitel_changed, "feedback")
        # )
        self.comboBox_kapitel_fb_cria.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.verticalLayout_fb_cria.addWidget(self.comboBox_kapitel_fb_cria)

        self.comboBox_unterkapitel_fb_cria = QtWidgets.QComboBox(
            self.groupBox_alle_aufgaben_fb_cria
        )
        self.comboBox_unterkapitel_fb_cria.setObjectName(
            "self.comboBox_unterkapitel_fb_cria"
        )

        # self.comboBox_unterkapitel_fb_cria.currentIndexChanged.connect(
        #     partial(self.comboBox_unterkapitel_changed, "feedback")
        # )
        self.comboBox_unterkapitel_fb_cria.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.verticalLayout_fb_cria.addWidget(self.comboBox_unterkapitel_fb_cria)

        self.lineEdit_number_fb_cria = QtWidgets.QLineEdit(
            self.groupBox_alle_aufgaben_fb_cria
        )
        self.lineEdit_number_fb_cria.setObjectName("lineEdit_number_fb_cria")

        self.lineEdit_number_fb_cria.textChanged.connect(
            partial(self.adapt_choosing_list, "feedback")
        )
        self.verticalLayout_fb_cria.addWidget(self.lineEdit_number_fb_cria)
        self.listWidget_fb_cria = QtWidgets.QListWidget(
            self.groupBox_alle_aufgaben_fb_cria
        )
        self.listWidget_fb_cria.setObjectName("listWidget_fb_cria")
        self.verticalLayout_fb_cria.addWidget(self.listWidget_fb_cria)
        self.listWidget_fb_cria.itemClicked.connect(self.nummer_clicked_fb)
        self.gridLayout.addWidget(self.groupBox_alle_aufgaben_fb_cria, 1, 0, 6, 1)
        self.groupBox_alle_aufgaben_fb_cria.setTitle(
            _translate("MainWindow", "Aufgaben", None)
        )
        self.groupBox_alle_aufgaben_fb_cria.hide()

        self.comboBox_kapitel_fb_cria.addItem("")
        for all in dict_k1_name:
            self.comboBox_kapitel_fb_cria.addItem(dict_k1_name[all] + " (" + all + ")")

        self.groupBox_fehlertyp = QtWidgets.QGroupBox(self.centralwidget)
        # self.groupBox_fehlertyp.setSizePolicy(SizePolicy_fixed)
        self.groupBox_fehlertyp.setObjectName("groupBox_fehlertyp")
        self.gridLayout_fehlertyp = QtWidgets.QGridLayout(self.groupBox_fehlertyp)
        self.gridLayout_fehlertyp.setObjectName("gridLayout_feedback")
        self.groupBox_fehlertyp.setTitle(_translate("MainWindow", "Betreff", None))

        self.comboBox_fehlertyp = QtWidgets.QComboBox(self.groupBox_fehlertyp)
        self.comboBox_fehlertyp.setObjectName("comboBox_pruefungstyp")
        self.comboBox_fehlertyp.addItem("")
        self.comboBox_fehlertyp.addItem("")
        self.comboBox_fehlertyp.addItem("")
        self.comboBox_fehlertyp.addItem("")
        self.comboBox_fehlertyp.addItem("")
        self.comboBox_fehlertyp.addItem("")
        self.comboBox_fehlertyp.addItem("")
        self.comboBox_fehlertyp.addItem("")
        self.comboBox_fehlertyp.addItem("")
        self.comboBox_fehlertyp.setItemText(
            1, _translate("MainWindow", "Feedback", None)
        )
        self.comboBox_fehlertyp.setItemText(
            2, _translate("MainWindow", "Fehler in der Angabe", None)
        )
        self.comboBox_fehlertyp.setItemText(
            3, _translate("MainWindow", "Fehler in der Lösung", None)
        )
        self.comboBox_fehlertyp.setItemText(
            4, _translate("MainWindow", "Bild wird nicht (richtig) angezeigt", None)
        )
        self.comboBox_fehlertyp.setItemText(
            5, _translate("MainWindow", "Grafik ist unleserlich/fehlerhaft", None)
        )
        self.comboBox_fehlertyp.setItemText(
            6, _translate("MainWindow", "Aufgabe ist doppelt vorhanden", None)
        )
        self.comboBox_fehlertyp.setItemText(
            7,
            _translate(
                "MainWindow",
                "Falsche Kodierung (Grundkompetenz, Aufgabenformat, ...)",
                None,
            ),
        )
        self.comboBox_fehlertyp.setItemText(
            8, _translate("MainWindow", "Sonstiges", None)
        )

        self.comboBox_fehlertyp.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.gridLayout_fehlertyp.addWidget(self.comboBox_fehlertyp, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_fehlertyp, 1, 1, 1, 1)
        self.groupBox_fehlertyp.hide()

        self.groupBox_feedback = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_feedback.setObjectName(_fromUtf8("groupBox_feedback"))
        # self.groupBox_feedback.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding))
        self.gridLayout_fb = QtWidgets.QGridLayout(self.groupBox_feedback)
        self.gridLayout_fb.setObjectName(_fromUtf8("gridLayout_fb"))
        self.plainTextEdit_fb = QtWidgets.QPlainTextEdit(self.groupBox_feedback)
        self.plainTextEdit_fb.setObjectName(_fromUtf8("plainTextEdit_fb"))
        self.plainTextEdit_fb.setTabChangesFocus(True)

        self.gridLayout_fb.addWidget(self.plainTextEdit_fb, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_feedback, 2, 1, 1, 1)
        self.groupBox_feedback.setTitle(
            _translate("MainWindow", "Feedback bzw. Problembeschreibung", None)
        )
        self.groupBox_feedback.hide()

        self.groupBox_email = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_email.setObjectName("groupBox_email")
        # self.groupBox_klasse.setMaximumSize(QtCore.QSize(200, 16777215))
        self.verticalLayout_email = QtWidgets.QVBoxLayout(self.groupBox_email)
        self.verticalLayout_email.setObjectName("verticalLayout_email")
        self.lineEdit_email = QtWidgets.QLineEdit(self.groupBox_email)
        self.lineEdit_email.setObjectName("lineEdit_email")
        self.groupBox_email.setTitle(
            _translate("MainWindow", "E-Mail Adresse für Nachfragen (optional)", None)
        )
        self.verticalLayout_email.addWidget(self.lineEdit_email)
        self.gridLayout.addWidget(self.groupBox_email, 5, 1, 1, 1)
        self.groupBox_email.hide()

        self.pushButton_send = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_send.setObjectName(_fromUtf8("pushButton_send"))
        self.gridLayout.addWidget(
            self.pushButton_send, 7, 1, 1, 1, QtCore.Qt.AlignRight
        )
        self.pushButton_send.setText(_translate("MainWindow", "Senden", None))
        self.pushButton_send.clicked.connect(self.pushButton_send_pressed)
        self.pushButton_send.hide()

        self.comboBox_kapitel_fb_cria.currentIndexChanged.connect(
            partial(self.comboBox_kapitel_changed, "feedback")
        )

        self.comboBox_unterkapitel_fb_cria.currentIndexChanged.connect(
            partial(self.comboBox_unterkapitel_changed, "feedback")
        )

        #         ####################################################################
        #         #####################################################################
        #         ######################################################################
        #         #####################################################################

        # self.gridLayout_11.addWidget(self.tab_widget_gk, 0, 0, 1, 1)
        # self.gridLayout.addWidget(self.groupBox_gk, 1, 1, 2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tab_widget_themen.setCurrentIndex(0)

        self.tab_widget_gk_cr.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #         ############################################################################
        #         ############## Commands ####################################################
        #         ############################################################################

        self.comboBox_aufgabentyp_cr.currentIndexChanged.connect(
            self.chosen_aufgabenformat_cr
        )
        self.pushButton_save.clicked.connect(self.button_speichern_pressed)
        self.pushButton_titlepage.clicked.connect(self.define_titlepage)

        if loaded_lama_file_path != "":
            self.sage_load(external_file_loaded=True)

        ############################################################################################
        ##############################################################################################

    def retranslateUi(self, MainWindow):
        # self.menuDateityp.setTitle(_translate("MainWindow", "Aufgabentyp", None))
        self.menuDatei.setTitle(_translate("MainWindow", "Datei", None))
        self.menuNeu.setTitle(_translate("MainWindow", "Aufgabe", None))
        self.menuSage.setTitle(_translate("MainWindow", "Prüfung", None))
        self.menuSuche.setTitle(_translate("MainWindow", "Suche", None))
        self.menuDeveloper.setTitle(_translate("MainWindow", "Entwicklermodus", None))

        # self.menuBild_einbinden.setTitle(
        #     _translate("MainWindow", "Bild einfügen", None)
        # )
        self.menuFeedback.setTitle(_translate("MainWindow", "Feedback && Fehler", None))

        self.menuHelp.setTitle(_translate("MainWindow", "?", None))

        self.groupBox_klassen.setTitle(_translate("MainWindow", "Suchfilter", None))

        # self.cb_solution.setText(_translate("MainWindow", "Lösungen anzeigen", None))
        # self.cb_drafts.setText(_translate("MainWindow", "Entwürfe anzeigen", None))

        self.combobox_searchtype.setItemText(
            0,
            _translate(
                "MainWindow",
                "Alle Dateien ausgeben, die zumindest ein Themengebiet enthalten",
                None,
            ),
        )

        ##### ONLY NEEDED for Typ1 #####
        self.groupBox_af = QtWidgets.QGroupBox(self.centralwidget)
        # self.groupBox_af.setMaximumSize(QtCore.QSize(375, 16777215))
        self.groupBox_af.setObjectName(_fromUtf8("groupBox_af"))
        # self.groupBox_af.setMaximumHeight(80)
        self.gridLayout_af = QtWidgets.QGridLayout(self.groupBox_af)
        self.gridLayout_af.setObjectName(_fromUtf8("gridLayout_af"))
        self.cb_af_zo = QtWidgets.QCheckBox(self.groupBox_af)
        self.cb_af_zo.setObjectName(_fromUtf8("cb_af_zo"))
        self.gridLayout_af.addWidget(self.cb_af_zo, 0, 2, 1, 1)
        self.cb_af_mc = QtWidgets.QCheckBox(self.groupBox_af)
        self.cb_af_mc.setObjectName(_fromUtf8("cb_af_mc"))
        self.gridLayout_af.addWidget(self.cb_af_mc, 0, 0, 1, 2)
        self.cb_af_oa = QtWidgets.QCheckBox(self.groupBox_af)
        self.cb_af_oa.setObjectName(_fromUtf8("cb_af_oa"))
        self.gridLayout_af.addWidget(self.cb_af_oa, 1, 2, 1, 1)
        self.cb_af_lt = QtWidgets.QCheckBox(self.groupBox_af)
        self.cb_af_lt.setObjectName(_fromUtf8("cb_af_lt"))
        self.gridLayout_af.addWidget(self.cb_af_lt, 1, 0, 1, 1)

        self.cb_af_ta = QtWidgets.QCheckBox(self.groupBox_af)
        self.cb_af_ta.setObjectName("cb_af_ta")
        self.gridLayout_af.addWidget(self.cb_af_ta, 2, 0, 1, 1)

        self.cb_af_rf = QtWidgets.QCheckBox(self.groupBox_af)
        self.cb_af_rf.setObjectName("cb_af_rf")
        self.gridLayout_af.addWidget(self.cb_af_rf, 2, 2, 1, 1)

        self.cb_af_ko = QtWidgets.QCheckBox(self.groupBox_af)
        self.cb_af_ko.setObjectName("cb_af_ko")
        self.gridLayout_af.addWidget(self.cb_af_ko, 3, 0, 1, 1)

        if self.chosen_program != "cria":
            self.cb_af_ko.hide()
            self.cb_af_rf.hide()
            self.cb_af_ta.hide()

        # self.gridLayout.addWidget(self.groupBox_af, 3, 0, 1, 1)
        if self.chosen_program == "lama":
            self.gridLayout.addWidget(self.groupBox_af, 4, 0, 2, 1)
        if self.chosen_program == "cria":
            self.gridLayout.addWidget(self.groupBox_af, 3, 0, 1, 1)

        # #################

        # ##### ONLY NEEDED for Typ1 #####

        self.groupBox_af.setTitle(
            _translate("MainWindow", "Gesuchte Aufgabenformate:", None)
        )
        self.cb_af_zo.setText(_translate("MainWindow", "Zuordnungsformat (ZO)", None))
        self.cb_af_mc.setText(_translate("MainWindow", "Multiplechoice (MC)", None))
        self.cb_af_oa.setText(
            _translate("MainWindow", "Offenes Antwortformat (OA)", None)
        )
        self.cb_af_lt.setText(_translate("MainWindow", "Lückentext (LT)", None))
        self.cb_af_rf.setText(
            _translate("MainWindow", "Richtig/Falsch-Format (RF)", None)
        )
        self.cb_af_ko.setText(_translate("MainWindow", "Konstruktion (KO)", None))
        self.cb_af_ta.setText(_translate("MainWindow", "Textaufgaben (TA)", None))
        #########################

        self.groupBox_themen_klasse.setTitle(
            _translate("MainWindow", "Erweiterungsstoff", None)
        )

        ############# Infos for GKs
        self.create_Tooltip(ag_beschreibung)
        self.create_Tooltip(fa_beschreibung)
        self.create_Tooltip(an_beschreibung)
        self.create_Tooltip(ws_beschreibung)
        #############################################

        if self.chosen_program == "lama":
            program = "LaMA Cria (Unterstufe)"
        if self.chosen_program == "cria":
            program = "LaMA (Oberstufe)"
        self.actionProgram.setText(
            _translate("MainWindow", 'Zu "{}" wechseln'.format(program), None)
        )
        self.actionExit.setText(_translate("MainWindow", "Exit", None))

        print("Done")

        if self.chosen_program == "cria":
            self.update_gui("widgets_search")


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

            if self.ui_erstellen.lama == True: #????????
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
                    self.ui_erstellen.lama,
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

    def check_admin_entry(self):
        if ("###" in self.lineEdit_titel.text() and self.chosen_program == "lama") or (
            self.chosen_gui == "widgets_edit" and self.developer_mode_active == True
        ):
            self.cb_matura_tag.show()
            self.cb_no_grade_tag.hide()
            self.cb_no_grade_tag.setChecked(False)
        elif (
            "###" in self.lineEdit_titel.text() and self.chosen_program == "cria"
        ) or (
            self.chosen_gui == "widgets_edit_cria"
            and self.developer_mode_active == True
        ):
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
            new_checkbox = create_new_checkbox(parent, "")
            new_checkbox.stateChanged.connect(
                partial(self.checkbox_checked, mode, "themen")
            )
            new_checkbox.setSizePolicy(SizePolicy_fixed)
            name = name_start + thema
            self.dict_widget_variables[name] = new_checkbox
            layout.addWidget(new_checkbox, row, 0, 1, 1)

            new_label = create_new_label(parent, dict_klasse[thema], True, True)
            new_label.clicked.connect(partial(self.click_label_to_check, new_checkbox))
            layout.addWidget(new_label, row, 1, 1, 1)

            row += 1

        return row

    def create_tab_checkboxes_themen(self, tab_widget, mode):
        # new_tab = add_new_tab(
        #     tab_widget, "{}. Klasse".format(klasse[1])
        # )  # self.tab_widget_gk self.tab_widget_gk_cr
        new_tab = add_new_tab(tab_widget, "Zusatzthemen")
        if self.display_mode == 0:
            stylesheet = StyleSheet_new_tab
        else:
            stylesheet = StyleSheet_new_tab_dark_mode
        new_tab.setStyleSheet(stylesheet)

        verticalLayout = create_new_verticallayout(new_tab)
        scrollarea = QtWidgets.QScrollArea(new_tab)
        scrollarea.setWidgetResizable(True)
        scrollarea.setObjectName("{}".format(scrollarea))

        scrollareacontent = QtWidgets.QWidget()
        scrollareacontent.setGeometry(QtCore.QRect(0, 0, 641, 252))
        scrollareacontent.setObjectName("{}".format(scrollareacontent))

        gridlayout_scrollarea = create_new_gridlayout(scrollareacontent)

        row = self.create_checkboxes_themen(
            scrollareacontent, gridlayout_scrollarea, mode
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
            if self.display_mode == 0:
                stylesheet = StyleSheet_button_check_all
            else:
                stylesheet = StyleSheet_button_check_all_dark_mode
            button_check_all.setStyleSheet(stylesheet)
            button_check_all.setSizePolicy(SizePolicy_fixed)

        gridlayout_scrollarea.setRowStretch(row, 1)

        if mode == "search":
            gridlayout_scrollarea.addWidget(button_check_all, row + 1, 0, 1, 2)

        scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
        scrollarea.setWidget(scrollareacontent)
        verticalLayout.addWidget(scrollarea)

    def create_tab_checkboxes_gk(self, tab_widget, titel, chosen_dictionary, mode):
        new_tab = add_new_tab(
            tab_widget, titel
        )  # self.tab_widget_gk self.tab_widget_gk_cr
        if self.display_mode == 0:
            stylesheet = StyleSheet_new_tab
        else:
            stylesheet = StyleSheet_new_tab_dark_mode
        new_tab.setStyleSheet(stylesheet)

        gridlayout = create_new_gridlayout(new_tab)

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
            if self.display_mode == 0:
                stylesheet = StyleSheet_button_check_all
            else:
                stylesheet = StyleSheet_button_check_all_dark_mode
            button_check_all.setStyleSheet(stylesheet)
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
            if self.display_mode == 0:
                stylesheet = StyleSheet_new_checkbox
            else:
                stylesheet = StyleSheet_new_checkbox_dark_mode
            new_checkbox.setStyleSheet(stylesheet)
            layout.addWidget(new_checkbox, row, column, 1, 1)
            new_checkbox.stateChanged.connect(
                partial(self.checkbox_checked, mode, "gk")
            )
            name = name_start + all
            self.dict_widget_variables[name] = new_checkbox

            if row > max_row:
                row = 0
                column += 1
            else:
                row += 1

        layout.setColumnStretch(column, 1)

        return row, column

    #######################
    #### Check for Updates
    ##########################

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
            # print(e)
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
                        os.system(path_installer)
                        sys.exit(0)
        QtWidgets.QApplication.restoreOverrideCursor()


    def create_Tooltip(self, chosen_dict):
        for all in chosen_dict:
            name = "checkbox_search_gk_" + all
            self.dict_widget_variables[name].setToolTip(chosen_dict[all])
        for all in chosen_dict:
            name = "checkbox_creator_gk_" + all
            self.dict_widget_variables[name].setToolTip(chosen_dict[all])

    def comboBox_suchbegriffe_changed(self):
        if self.comboBox_suchbegriffe.currentIndex() == 0:
            self.entry_suchbegriffe.setText("")
            self.entry_suchbegriffe.setEnabled(False)
        else:
            self.entry_suchbegriffe.setEnabled(True)

    def tabWidget_klassen_cria_changed(self):
        klasse = list_klassen[self.tabWidget_klassen_cria.currentIndex()]

        for all in self.dict_widget_variables:
            if all.startswith("radiobutton_kapitel_{}".format(klasse)):
                if self.dict_widget_variables[all].isChecked():
                    split_ending = all.rpartition("_")
                    kapitel = split_ending[-1]
                    self.chosen_radiobutton(klasse, kapitel)
                    return

        self.label_unterkapitel_cria.setText("")

        for alle_klassen in list_klassen:
            dict_klasse = eval("dict_{}".format(alle_klassen))
            for alle_kapitel in dict_klasse:

                for unterkapitel in dict_klasse[alle_kapitel]:
                    label = "checkbox_unterkapitel_{0}_{1}_{2}".format(
                        alle_klassen, alle_kapitel, unterkapitel
                    )
                    self.dict_widget_variables[label].hide()
                label_button_check_all = "button_check_all_unterkapitel_{0}_{1}".format(
                    alle_klassen, alle_kapitel
                )
                self.dict_widget_variables[label_button_check_all].hide()
        # self.button_check_all_unterkapitel.hide()

    def create_all_checkboxes_unterkapitel(self):
        for klasse in list_klassen:
            dict_klasse = eval("dict_{}".format(klasse))
            for kapitel in dict_klasse:
                for unterkapitel in dict_klasse[kapitel]:
                    checkbox = create_new_checkbox(
                        self.scrollAreaWidgetContents_cria,
                        dict_unterkapitel[unterkapitel] + " (" + unterkapitel + ")",
                    )
                    checkbox.stateChanged.connect(
                        partial(
                            self.checkBox_checked_cria, klasse, kapitel, unterkapitel
                        )
                    )
                    self.verticalLayout_4_cria.addWidget(checkbox)
                    checkbox.hide()
                    label = "checkbox_unterkapitel_{0}_{1}_{2}".format(
                        klasse, kapitel, unterkapitel
                    )
                    self.dict_widget_variables[
                        label
                    ] = checkbox  #### creates widgets ???

        self.spacerItem_unterkapitel_cria = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )

        self.verticalLayout_4_cria.addItem(self.spacerItem_unterkapitel_cria)

        for klasse in list_klassen:
            dict_klasse = eval("dict_{}".format(klasse))
            for kapitel in dict_klasse:
                button_check_all_unterkapitel = create_new_button(
                    self.scrollAreaWidgetContents_cria, "alle auswählen", None
                )
                if self.display_mode == 0:
                    stylesheet = StyleSheet_button_check_all
                else:
                    stylesheet = StyleSheet_button_check_all_dark_mode
                button_check_all_unterkapitel.setStyleSheet(stylesheet)
                button_check_all_unterkapitel.clicked.connect(
                    partial(self.btn_alle_unterkapitel_clicked_cria, klasse, kapitel)
                )
                self.verticalLayout_4_cria.addWidget(
                    button_check_all_unterkapitel, 0, QtCore.Qt.AlignLeft
                )
                button_check_all_unterkapitel.hide()
                label_button_check_all = "button_check_all_unterkapitel_{0}_{1}".format(
                    klasse, kapitel
                )
                self.dict_widget_variables[
                    label_button_check_all
                ] = button_check_all_unterkapitel


    def btn_alle_kapitel_clicked(self, klasse):
        dict_klasse_name = eval("dict_{}_name".format(klasse))
        dict_klasse = eval("dict_{}".format(klasse))
        first_chapter = list(dict_klasse_name.keys())[0]
        first_radiobutton = "radiobutton_kapitel_{0}_{1}".format(klasse, first_chapter)
        first_checkbox = "checkbox_unterkapitel_{0}_{1}_{2}".format(
            klasse, first_chapter, dict_klasse[first_chapter][0]
        )
        self.dict_widget_variables[first_radiobutton].setChecked(True)

        if self.dict_widget_variables[first_checkbox].isChecked() == True:
            all_checked = True
        else:
            all_checked = False

        for kapitel in dict_klasse_name:
            first_checkbox = "checkbox_unterkapitel_{0}_{1}_{2}".format(
                klasse, kapitel, dict_klasse[kapitel][0]
            )
            if all_checked == True:
                self.dict_widget_variables[first_checkbox].setChecked(True)
            else:
                self.dict_widget_variables[first_checkbox].setChecked(False)

            self.btn_alle_unterkapitel_clicked_cria(klasse, kapitel)

    def chosen_radiobutton(self, klasse, kapitel):
        dict_klasse = eval("dict_{}".format(klasse))
        dict_klasse_name = eval("dict_{}_name".format(klasse))

        self.label_unterkapitel_cria.setText(
            _translate(
                "MainWindow",
                klasse[1] + ". Klasse  - " + dict_klasse_name[kapitel],
                None,
            )
        )

        for alle_klassen in list_klassen:
            dict_klasse = eval("dict_{}".format(alle_klassen))
            for alle_kapitel in dict_klasse:
                for unterkapitel in dict_klasse[alle_kapitel]:
                    label = "checkbox_unterkapitel_{0}_{1}_{2}".format(
                        alle_klassen, alle_kapitel, unterkapitel
                    )
                    if alle_klassen == klasse and alle_kapitel == kapitel:
                        self.dict_widget_variables[label].show()
                    else:
                        self.dict_widget_variables[label].hide()

        label_button_check_all = "button_check_all_unterkapitel_{0}_{1}".format(
            klasse, kapitel
        )
        for button in self.dict_widget_variables:
            if button.startswith("button_check_all_unterkapitel_"):
                if button != label_button_check_all:
                    self.dict_widget_variables[button].hide()
                else:
                    self.dict_widget_variables[label_button_check_all].show()

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

        self.label_ausg_themen_cria.setText(_translate("MainWindow", x, None))

    def btn_alle_unterkapitel_clicked_cria(self, klasse, kapitel):
        dict_klasse = eval("dict_{}".format(klasse))

        first_checkbox = "checkbox_unterkapitel_{0}_{1}_{2}".format(
            klasse, kapitel, dict_klasse[kapitel][0]
        )

        if self.dict_widget_variables[first_checkbox].isChecked() == False:
            check_checkboxes = True
        else:
            check_checkboxes = False

        for all in self.dict_widget_variables:
            if all.startswith("checkbox_unterkapitel_{0}_{1}_".format(klasse, kapitel)):
                self.dict_widget_variables[all].setChecked(check_checkboxes)

    def comboBox_kapitel_changed_cr(
        self, parent, layout, klasse
    ):  # , verticalLayout_cr_cria, combobox_kapitel, klasse, spacerItem_unterkapitel_cria
        # layout.removeItem(self.spacerItem_unterkapitel_creator_cria)

        # self.delete_all_widgets(layout, 1) ### PROBLEM !!!
        for i in range(1, layout.count()):
            try:
                layout.itemAt(i).widget().hide()
            except AttributeError:
                pass

        text_combobox = self.dict_widget_variables[
            "combobox_kapitel_creator_cria_{}".format(klasse)
        ].currentText()
        kapitel = text_combobox[text_combobox.find("(") + 1 : text_combobox.find(")")]

        dict_klasse = eval("dict_{}".format(klasse))

        for unterkapitel in dict_klasse[kapitel]:
            if (
                "checkbox_unterkapitel_creator_{0}_{1}_{2}".format(
                    klasse, kapitel, unterkapitel
                )
                in self.dict_widget_variables
            ):
                checkbox = self.dict_widget_variables[
                    "checkbox_unterkapitel_creator_{0}_{1}_{2}".format(
                        klasse, kapitel, unterkapitel
                    )
                ]
                # layout.insertWidget(layout.count() - 1, checkbox)
                checkbox.show()
            else:
                new_checkbox = create_new_checkbox(
                    parent, dict_unterkapitel[unterkapitel] + " (" + unterkapitel + ")"
                )
                new_checkbox.stateChanged.connect(
                    partial(
                        self.checkbox_unterkapitel_checked_creator_cria,
                        new_checkbox,
                        klasse,
                        kapitel,
                        unterkapitel,
                    )
                )
                self.dict_widget_variables[
                    "checkbox_unterkapitel_creator_{0}_{1}_{2}".format(
                        klasse, kapitel, unterkapitel
                    )
                ] = new_checkbox
                new_checkbox.setFocusPolicy(QtCore.Qt.NoFocus)
                layout.insertWidget(layout.count() - 1, new_checkbox)

        # layout.addStretch()
        # layout.addItem(self.spacerItem_unterkapitel_creator_cria)

    def checkbox_unterkapitel_checked_creator_cria(
        self, checkbox, klasse, kapitel, unterkapitel
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

        klasse = list_klassen[self.tabWidget_klassen_cria.currentIndex()]
        dict_klasse = eval("dict_{}_name".format(klasse))
        kapitel = list(dict_klasse.keys())[0]
        self.chosen_radiobutton(klasse, kapitel)

        self.entry_suchbegriffe.setText("")
        self.cb_solution.setChecked(True)
        self.spinBox_punkte.setProperty("value", 1)
        self.comboBox_aufgabentyp_cr.setCurrentIndex(0)
        self.comboBox_suchbegriffe.setCurrentIndex(0)
        self.comboBox_af.setCurrentIndex(0)
        self.comboBox_klassen_cr.setCurrentIndex(0)
        self.label_ausgew_gk_creator.setText(_translate("MainWindow", "", None))
        # self.label_bild_leer.show()

        self.chosen_variation = None
        self.reset_variation()

        for picture in list(self.dict_widget_variables.keys())[:]:
            if picture.startswith("label_bild_creator_"):
                self.del_picture(picture, question=False)

        if self.lineEdit_titel.text().startswith("###"):
            self.lineEdit_titel.setText(_translate("MainWindow", "###", None))
        else:
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

    def reset_sage(self, question_reset=True):
        if question_reset == True and not is_empty(self.list_alle_aufgaben_sage):
            response = question_window(
                "Sind Sie sicher, dass Sie das Fenster zurücksetzen wollen und die erstellte Prüfung löschen möchten?",
                titel="Datei löschen?",
            )

            if response == False:
                return

        self.spinBox_nummer.setValue(1)
        self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.comboBox_pruefungstyp.setCurrentIndex(0)
        self.lineEdit_klasse.setText("")
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
            "dict_ausgleichspunkte": {},
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

        self.list_alle_aufgaben_sage = []
        # self.dict_alle_aufgaben_sage = {}
        self.dict_variablen_label = {}
        self.dict_variablen_punkte = {}
        self.dict_variablen_abstand = {}
        self.update_punkte()
        self.list_copy_images = []
        for i in reversed(range(self.gridLayout_8.count())):
            self.delete_widget(self.gridLayout_8, i)

    def change_program(self):
        if self.chosen_program == "lama":
            change_to = "LaMA Cria (Unterstufe)"
            program_name = "LaMA Cria - LaTeX Mathematik Assistent (Unterstufe)"
            icon = logo_cria_path

        elif self.chosen_program == "cria":
            change_to = "LaMA (Oberstufe)"
            program_name = "LaMA - LaTeX Mathematik Assistent (Oberstufe)"
            icon = logo_path

        response = question_window(
            "Sind Sie sicher, dass sie zu {} wechseln wollen?\nDadurch werden alle bisherigen Einträge gelöscht!".format(
                change_to
            ),
            titel="Programm wechseln?",
        )

        if response == False:
            return False

        self.reset_sage(False)
        self.suchfenster_reset()
        self.reset_feedback()

        # self.comboBox_fehlertyp.setCurrentIndex(0)
        # self.plainTextEdit.setPlainText("")

        self.actionProgram.setText(
            _translate("MainWindow", 'Zu "{}" wechseln'.format(change_to), None)
        )

        self.comboBox_pagebreak.setCurrentIndex(0)
        if self.chosen_program == "lama":
            self.chosen_program = "cria"

            # if self.beispieldaten_dateipfad_cria == None:
            #     self.beispieldaten_dateipfad_cria = self.define_beispieldaten_dateipfad(
            #         "cria"
            #     )

            self.gridLayout.addWidget(self.groupBox_af, 3, 0, 1, 1)
            self.gridLayout.addWidget(self.groupBox_punkte, 0, 1, 1, 1)
            self.gridLayout.addWidget(self.groupBox_aufgabenformat, 0, 2, 1, 1)
            self.actionProgram.setText(
                _translate("MainWindow", 'Zu "LaMA (Oberstufe)" wechseln', None)
            )
            # self.comboBox_pruefungstyp.removeItem(6)  # delete Quiz
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
            # self.beispieldaten_dateipfad_cria = self.define_beispieldaten_dateipfad(
            #     "cria"
            # )

        elif self.chosen_program == "cria":
            self.chosen_program = "lama"

            self.gridLayout.addWidget(self.groupBox_af, 4, 0, 1, 1)
            self.gridLayout.addWidget(self.groupBox_punkte, 0, 2, 1, 1)
            self.gridLayout.addWidget(self.groupBox_aufgabenformat, 0, 3, 1, 1)
            self.actionProgram.setText(
                _translate("MainWindow", 'Zu "LaMA Cria (Unterstufe)" wechseln', None)
            )
            self.combobox_searchtype.setItemText(
                1,
                _translate(
                    "MainWindow",
                    "Alle Dateien ausgeben, die ausschließlich diese Themengebiete enthalten",
                    None,
                ),
            )

            # self.comboBox_pruefungstyp.addItem("Quiz")
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

            self.groupBox_ausgew_gk_cr.setTitle("Ausgewählte Grundkompetenzen")

        MainWindow.setWindowTitle(program_name)
        MainWindow.setWindowIcon(QtGui.QIcon(icon))
        if self.lama_settings["database"] == 0:
            refresh_ddb(self)
        self.update_gui("widgets_search")
        # self.beispieldaten_dateipfad_1 = self.define_beispieldaten_dateipfad(1)
        # self.beispieldaten_dateipfad_2 = self.define_beispieldaten_dateipfad(2)

    def exit_pressed(self):
        rsp = question_window("Sind Sie sicher, dass Sie LaMA schließen möchten?")
        if rsp == True:
            self.close_app()

    def close_app(self):
        if self.list_alle_aufgaben_sage == []:
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
            self.menuBar.addAction(self.menuDeveloper.menuAction())

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

    # def complete_reset(self):
    #     print("complete reset!")
        # rsp = question_window("Sind Sie wirklich sicher, dass Sie LaMA vollständig zurücksetzen wollen?")
        # if rsp==False:
        #     return

        # if os.path.isfile(os.path.join(database, "_local_database.json")):
        #     delete_local_db = question_window("Möchten Sie auch alle lokal gespeicherten Aufgaben unwiderruflich löschen?")

        # lama_folder = os.path.dirname(database)

        # teildokument_folder = os.path.join(lama_folder, "Teildokument")

        # for all in os.listdir(database):
        #     path = os.path.join(database, all)
        #     if os.path.isdir(path):
        #         if all != "Bilder_local":
        #             shutil.rmtree(path, ignore_errors=True)
        #     elif os.path.isfile(path):
        #         if all != "_local_database.json":
        #             os.remove(path)

        # for root, dirs, files in os.walk(delete_folder):

    def show_info(self):
        QtWidgets.QApplication.restoreOverrideCursor()

        custom_window(
            "LaMA - LaTeX Mathematik Assistent %s  \n\n"
            "Authors: Christoph Weberndorfer, Matthias Konzett\n\n"
            "License: GNU General Public License v3.0  \n" % __version__,
            "Logo & Icon: Lisa Schultz\n"
            "Credits: David Fischer\n\n"
            "E-Mail-Adresse: lama.helpme@gmail.com\n"
            "Weiter Infos: lama.schule",
            titel="Über LaMA - LaTeX Mathematik Assistent",
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
                            warning_window(
                                "Das Update konnte leider nicht durchgeführt werden, da notwendige Berechtigungen fehlen. Starten Sie LaMA erneut als Administrator (Rechtsklick -> 'Als Administrator ausführen') und versuchen Sie es erneut."
                            )
                            return False
        return False

    def delete_style_package_in_teildokument(self, package_name):
        style_package_path = os.path.join(path_programm, "Teildokument", package_name)

        if os.path.isfile(style_package_path):
            os.remove(style_package_path)

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
                os.path.join("c:\\", "Program Files", "MiKTeX 2.9"),
                os.path.join("c:\\", "Program Files (x86)", "MiKTeX 2.9"),
                os.path.join(path_home, "AppData", "Roaming", "MiKTeX"),
                os.path.join(path_home, "AppData", "Local", "Programs", "MiKTeX"),
                os.path.join(path_home, "AppData"),
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
                else:
                    location_found = response
            
            else:
                #initexmf --update-fndb
                new_copy = False
                try:
                    srdptables = os.path.join(location_found, package)
                    if sys.platform.startswith("win"):
                        if not os.path.isfile(srdptables):
                            new_copy = True        
                    shutil.copy2(package_list[package], location_found)
                    if new_copy == True:
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
        custom_window(
            'Eine kleinen Spende für unsere "Kaffeekassa" wird nicht benötigt, um LaMA zu finanzieren.\n\nUnser Projekt ist und bleibt kostenlos und wir versuchen es auch weiterhin stetig zu verbessern und aktualisieren. Sie dient lediglich als kleine Anerkennung unserer Arbeit.\n\nVielen Dank!',
            """<center><a href='{0}'style="color:{1};">Buy Me A Coffee</a><\center>""".format(
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
                y = "Weitere: " + y
            self.label_ausgew_gk.setText(_translate("MainWindow", str(x), None))
            self.label_ausgew_gk_rest.setText(_translate("MainWindow", str(y), None))
        if mode == "creator":
            if x == "":
                gesamt = y
            elif y == "":
                gesamt = x
            else:
                gesamt = x + ", " + y
            self.label_ausgew_gk_creator.setText(
                _translate("MainWindow", str(gesamt), None)
            )

    def comboBox_pruefungstyp_changed(self):
        self.comboBox_pruefungstyp.setEditable(False)
        self.groupBox_nummer.setEnabled(True)
        self.groupBox_datum.setEnabled(True)
        if self.comboBox_pruefungstyp.currentText() == "Grundkompetenzcheck":
            self.combobox_beurteilung.setEnabled(False)
            self.groupBox_notenschl.setEnabled(False)
            self.groupBox_beurteilungsraster.setEnabled(False)
            self.spinBox_nummer.setValue(0)
            self.groupBox_klasse.setTitle("Klasse")
            # if self.comboBox_pruefungstyp.currentText() == "Quiz":
            #     self.pushButton_titlepage.setEnabled(True)
            #     self.pushButton_titlepage.setText("Zufälliges Quiz erstellen")
            #     self.comboBox_at_sage.setCurrentIndex(0)
            #     self.comboBox_at_sage.setEnabled(False)
            #     if self.get_aufgabenverteilung()[1] != 0:
            #         response = question_window(
            #             "Das Quiz ist ausschließlich für Typ1-Aufgaben konzipiert. Sollen alle enthaltenen Typ2-Aufgaben entfernt und das Quiz erstellt werden?",
            #             titel="Typ2 Aufgaben entfernen?",
            #         )
            #         if response == False:
            #             self.comboBox_pruefungstyp.setCurrentIndex(0)
            #             return
            #         else:
            #             for aufgabe in self.list_alle_aufgaben_sage[:]:
            #                 typ = get_aufgabentyp(self.chosen_program, aufgabe)
            #                 if typ == 2:
            #                     self.btn_delete_pressed(aufgabe)

            # else:
            self.pushButton_titlepage.setEnabled(False)
            self.comboBox_at_sage.setEnabled(True)
            self.pushButton_titlepage.setText("Titelblatt anpassen")
        elif self.comboBox_pruefungstyp.currentText() == "Übungsblatt":
            self.combobox_beurteilung.setEnabled(False)
            self.groupBox_notenschl.setEnabled(False)
            self.groupBox_beurteilungsraster.setEnabled(False)
            self.spinBox_nummer.setValue(0)
            self.pushButton_titlepage.setEnabled(False)
            self.comboBox_at_sage.setEnabled(True)
            self.pushButton_titlepage.setText("Titelblatt anpassen")
            self.groupBox_datum.setEnabled(False)
            self.groupBox_nummer.setEnabled(False)
            self.groupBox_klasse.setTitle("Überschrift")
        else:
            self.combobox_beurteilung.setEnabled(True)
            self.groupBox_notenschl.setEnabled(True)
            self.groupBox_beurteilungsraster.setEnabled(True)
            self.pushButton_titlepage.setEnabled(True)
            self.comboBox_at_sage.setEnabled(True)
            self.spinBox_nummer.setValue(1)
            self.pushButton_titlepage.setText("Titelblatt anpassen")
            self.groupBox_klasse.setTitle("Klasse")
            if self.comboBox_pruefungstyp.currentText() == "Benutzerdefiniert":
                self.comboBox_pruefungstyp.setEditable(True)
                self.comboBox_pruefungstyp.lineEdit().selectAll()
                # setCursorPosition(0)
                self.groupBox_nummer.setEnabled(False)
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
                        if i == 0:
                            index = list_comboBox_gk.index(
                                gk.split(" ")[0].replace("-L", "")
                            )

                    self.dict_widget_variables[checkbox_gk].setChecked(True)
                self.tab_widget_gk_cr.setCurrentIndex(index)

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

        if self.lineEdit_titel.text().startswith("###") and mode == "creator":
            self.lineEdit_titel.setText("### " + aufgabe_total["titel"])
        else:
            self.lineEdit_titel.setText(aufgabe_total["titel"])

        # print(aufgabe_total['bilder'])
        # print(aufgabe_total['name'])

        if mode == "editor":
            if not is_empty(aufgabe_total['bilder']):
                # self.label_bild_leer.hide()
                for all in aufgabe_total['bilder']:
                    self.add_image_label(all, None)#, clickable=False

                self.verticalLayout.addWidget(self.btn_add_image)

            if aufgabe_total["info"] == "mat":
                self.cb_matura_tag.setChecked(True)
            # else:
            #     self.cb_matura_tag.setChecked(False)
            self.plainTextEdit.clear()
            self.plainTextEdit.insertPlainText(aufgabe_total["content"])
            self.lineEdit_quelle.setText(aufgabe_total["quelle"])

    def reset_variation(self):
        self.button_variation_cr.setText("Variation vorhandender Aufgabe...")
        self.groupBox_grundkompetenzen_cr.setEnabled(True)
        self.groupBox_aufgabentyp.setEnabled(True)
        self.comboBox_af.setEnabled(True)
        self.groupBox_themengebiete_cria.setEnabled(True)

    def reset_edit_file(self):
        self.button_choose_file.setText("Aufgabe suchen...")
        self.enable_widgets_editor(False)
        self.plainTextEdit.clear()
        # self.groupBox_grundkompetenzen_cr.setEnabled(True)
        # self.groupBox_aufgabentyp.setEnabled(True)
        # self.comboBox_af.setEnabled(True)
        # self.groupBox_themengebiete_cria.setEnabled(True)

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
        elif mode == "editor":
            show_variations = True
        ui.setupUi(Dialog, self, show_variations, mode)

        response = Dialog.exec()

        if response == 1:
            self.suchfenster_reset(True)
            if mode == "creator":
                self.chosen_variation = ui.chosen_variation
                _file_ = self.chosen_variation
                if self.chosen_variation != None:
                    self.button_variation_cr.setText(
                        "Variation von: {}".format(self.chosen_variation.upper())
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
        label_picture = create_new_label(
            self.scrollAreaWidgetContents_bilder, image_name, False, True
        )

        label_picture_name = "label_bild_creator_{}".format(image_name)
        self.dict_widget_variables[label_picture_name] = label_picture
        # if clickable == True:
        label_picture.clicked.connect(
            partial(self.del_picture, label_picture_name)
        )
        # else:
        #     label_picture.setStyleSheet("color: gray")
        self.verticalLayout.addWidget(label_picture)

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
        button_existing = msg.button(QtWidgets.QMessageBox.No)
        button_existing.setText("Vorhande Grafik verknüpfen")
        button_cancel = msg.button(QtWidgets.QMessageBox.Cancel)
        button_cancel.setText("Abbrechen")
        response = msg.exec_()
        return response
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
            if self.check_for_admin_mode() == 'admin' or self.developer_mode_active == True:
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
        i = len(self.dict_picture_path)

        # self.label_bild_leer.hide()
        for all in list_filename[0]:
            _, tail = os.path.split(all)

            if tail in self.dict_picture_path.keys():
                pass
            else:
                if mode == 'existing':
                    self.add_image_label(tail, 'no_copy')
                else:    
                    # _, tail = os.path.split(all)
                    self.add_image_label(tail, all)
                # self.dict_picture_path[tail] = all
                # label_picture = create_new_label(
                #     self.scrollAreaWidgetContents_bilder, tail, False, True
                # )

                # label_picture_name = "label_bild_creator_{}".format(tail)
                # self.dict_widget_variables[label_picture_name] = label_picture
                # label_picture.clicked.connect(
                #     partial(self.del_picture, label_picture_name)
                # )
                # self.verticalLayout.addWidget(label_picture)
        self.verticalLayout.addWidget(self.btn_add_image)

    def del_picture(self, picture, question=True):
        if question == True:
            rsp = question_window(
                'Sind Sie sicher, dass Sie die Grafik "{}" entfernen möchten?'.format(
                    self.dict_widget_variables[picture].text() # self.dict_picture_path[self.dict_widget_variables[picture].text()]
                )
            )
            if rsp == False:
                return
        del self.dict_picture_path[self.dict_widget_variables[picture].text()]
        self.dict_widget_variables[picture].hide()
        # if len(self.dict_picture_path) == 0:
        #     self.label_bild_leer.show()

        del self.dict_widget_variables[picture]

    def convert_image_eps_clicked(self):
        msg = QtWidgets.QMessageBox()
        # msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowIcon(QtGui.QIcon(logo_path))
        msg.setText("Wählen Sie alle Grafiken, die Sie konvertieren möchten.")
        # msg.setInformativeText('Möchten Sie das neue Update installieren?')
        msg.setWindowTitle("Grafik(en) konvertieren")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        button_durchsuchen = msg.button(QtWidgets.QMessageBox.Yes)
        button_durchsuchen.setText("Durchsuchen...")
        buttonN = msg.button(QtWidgets.QMessageBox.No)
        buttonN.setText("Abbrechen")
        ret = msg.exec_()

        if ret == QtWidgets.QMessageBox.Yes:
            # filename =	 filedialog.askopenfilenames(initialdir = last_path,title = "Durchsuchen...",filetypes = (('JPG-Dateien','*.jpg'),("Alle Dateien","*.*")))
            try:
                os.path.dirname(self.saved_file_path)
            except AttributeError:
                self.saved_file_path = path_home

            filename = QtWidgets.QFileDialog.getOpenFileNames(
                None,
                "Select a folder:",
                os.path.dirname(self.saved_file_path),
                "Bilder (*.jpg; *.jpeg; *.png; *.jfif);; Alle Dateien (*.*)",
            )
            if filename[0] != []:
                self.saved_file_path = filename[0][0]
                for image in filename[0]:
                    response = convert_image_to_eps(image)
                    if response != True:
                        break
                if response == True:
                    if len(filename[0]) == 1:
                        text = "wurde {} Datei".format(len(filename[0]))
                    else:
                        text = "wurden {} Dateien".format(len(filename[0]))

                    information_window(
                        "Es {0} erfolgreich konvertiert.".format(text),
                        titel="Grafik(en) erfolgreich konvertiert",
                        detailed_text="Konvertierte Grafik(en):\n{}".format(
                            "\n".join(filename[0])
                        ),
                    )
                else:
                    critical_window(
                        "Beim Konvertieren der folgenden Grafik ist ein Fehler aufgetreten:\n\n{}".format(
                            image
                        ),
                        titel="Fehler beim Konvertieren",
                        detailed_text='Fehlermeldung:\n\n"{0}: {1}"'.format(
                            type(response).__name__, response
                        ),
                    )

    def chosen_aufgabenformat_cr(self):
        if self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
            self.groupBox_aufgabenformat.setEnabled(True)
            self.comboBox_pagebreak.setCurrentIndex(0)
            # self.label_keine_auswahl.hide()
            # self.comboBox_af.show()
            self.comboBox_af.removeItem(0)
        if self.comboBox_aufgabentyp_cr.currentText() == "Typ 2":
            self.comboBox_af.insertItem(0, "keine Auswahl nötig")
            self.comboBox_pagebreak.setCurrentIndex(1)
            self.comboBox_af.setCurrentIndex(0)
            self.groupBox_aufgabenformat.setEnabled(False)
            # self.label_keine_auswahl.show()
            # self.comboBox_af.hide()

    def get_number_of_included_images(self):
        num = self.plainTextEdit.toPlainText().count("\includegraphics")
        return num

    def check_included_attached_image_ratio(self):
        included = self.get_number_of_included_images()
        attached = len(self.dict_picture_path)
        return included, attached

    def check_entry_creator(self, mode):
        if self.chosen_program == "lama":
            if is_empty(self.list_selected_topics_creator) == True:
                return "Es wurden keine Grundkompetenzen zugewiesen."

            if self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
                if len(self.list_selected_topics_creator) > 1:
                    return "Es wurden zu viele Grundkompetenzen zugewiesen."

        if (
            self.chosen_program == "cria"
            and is_empty(self.list_selected_topics_creator) == True
        ):
            return "Es wurden keine Themengebiete zugewiesen."

        if (
            self.comboBox_aufgabentyp_cr.currentText() != "Typ 2"
            and self.comboBox_af.currentText() == "bitte auswählen"
        ):
            return "Es wurde kein Aufgabenformat ausgewählt."

        if (
            is_empty(self.lineEdit_titel.text().replace("###", "")) == True
            or self.lineEdit_titel.text().replace("###", "").isspace()
        ):
            return "Bitte geben Sie einen Titel ein."

        if is_empty(self.plainTextEdit.toPlainText()) == True:
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
            self.check_for_admin_mode() == "user"
            and len(self.lineEdit_quelle.text()) != 6
        ):
            return 'Bitte geben Sie als Quelle ihren Vornamen und Nachnamen im Format "VorNac" (6 Zeichen!) ein.'



    def check_for_admin_mode(self):
        if self.lineEdit_titel.text().startswith("###"):
            mode = "admin"
        else:
            mode = "user"
        return mode

    def create_information_aufgabentyp(self):
        if self.chosen_program == "lama":
            aufgabentyp = "Aufgabentyp: {0}\n\n".format(
                self.comboBox_aufgabentyp_cr.currentText()
            )
        if self.chosen_program == "cria":
            aufgabentyp = ""

        return aufgabentyp

    def create_information_titel(self):
        if self.lineEdit_titel.text().startswith("###"):
            _, titel = self.lineEdit_titel.text().split("###")
            titel = titel.strip()
        else:
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
        self.ui_save.setupUi(Dialog_speichern, self.creator_mode, self.chosen_variation,save_mode)
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

        elif self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
            themen_auswahl.append(self.list_selected_topics_creator[0])

        elif self.comboBox_aufgabentyp_cr.currentText() == "Typ 2":

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
        titel = self.lineEdit_titel.text().replace("###", "").strip()
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
                False, chosen_ddb, message=message, worker_text="Änderung hochladen ..."
            )

    def button_save_edit_pressed(self):
        rsp = question_window(
            "Sind Sie sicher, dass Sie die Änderungen speichern wollen?"
        )
        if rsp == False:
            return

        warning = self.check_entry_creator('edit')
        if warning != None:
            warning_window(warning)
            return

        name = self.chosen_file_to_edit.replace(" (lokal)", "")

        typ = get_aufgabentyp(self.chosen_program, name)

        (
            _,
            themen,
            titel,
            af,
            quelle,
            content,
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

        file_id = lama_table.get(_file_.name == name).doc_id
        # print(bilder)
        # print(self.dict_picture_path)

        if typ == 1:
            lama_table.update({"name": new_name}, doc_ids=[file_id])
        lama_table.update({"themen": themen}, doc_ids=[file_id])
        lama_table.update({"titel": titel}, doc_ids=[file_id])
        lama_table.update({"af": af}, doc_ids=[file_id])
        lama_table.update({"quelle": quelle}, doc_ids=[file_id])
        lama_table.update({"content": content}, doc_ids=[file_id])
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

        # lama_table.update_multiple([
        #    ({"themen" :themen}, _file_.name == aufgabe),
        #    ({"titel" :titel}, _file_.name == aufgabe),
        #    ({"af" :af}, _file_.name == aufgabe),
        #    ({"quelle" :quelle}, _file_.name == aufgabe),
        #    ({"content" :content}, _file_.name == aufgabe),
        #    ({"punkte" :punkte}, _file_.name == aufgabe),
        #    ({"pagebreak" :pagebreak}, _file_.name == aufgabe),
        #    ({"klasse" :klasse}, _file_.name == aufgabe),
        #    ({"info" :info}, _file_.name == aufgabe),
        #    ({"bilder" :bilder}, _file_.name == aufgabe),
        #    ({"draft" :draft}, _file_.name == aufgabe),
        #    ({"abstand" :abstand}, _file_.name == aufgabe),
        # ])
        QtWidgets.QApplication.restoreOverrideCursor()

        if "l." not in name:
            self.upload_single_file_change(name, message="Bearbeitet: {}".format(name))

        # if "(lokal)" not in name:
        #     if "i." in new_name:
        #         chosen_ddb = ["_database_addon.json"]
        #     else:
        #         chosen_ddb = ["_database.json"]
        #     action_push_database(False, chosen_ddb, message= "Bearbeitet: {}".format(name), worker_text="Änderung hochladen ...")

        information_window("Die Änderungen wurden erfolgreich gespeichert.")

        self.suchfenster_reset(True)
        self.reset_edit_file()

    def button_vorschau_edit_pressed(self):
        content = self.plainTextEdit.toPlainText()
        file_path = os.path.join(path_localappdata_lama, "Teildokument", "preview.tex")
        rsp = create_tex(file_path, content)

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
        # image_path = os.path(path_programm, '_database')

        ### Bilder löschen ### disabled
        # if "l." in name:
        #     image_path = os.path.join(database, "Bilder_local")
        # elif "i." in name:
        #     image_path = os.path.join(database, "Bilder_addon")
        # else:
        #     image_path = os.path.join(database, "Bilder")

        # for all in images:
        #     image = os.path.join(image_path, all)
        #     try:
        #         os.remove(image)
        #     except FileNotFoundError:
        #         print('Die Grafik "{}" konnte nicht gefunden werden.'.format(image))

        delete_file(name, typ)

        if "l." not in name:
            if is_empty(images):
                self.upload_single_file_change(
                    name, message="Gelöscht: {}".format(name)
                )
            else:
                self.push_full_database()
        # if "(lokal)" not in name:
        #     file_list = ["_database.json"]
        #     action_push_database(False, file_list, message= "Gelöscht: {}".format(name), worker_text="Aufgabe löschen ...")

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
        
        # print(max_integer)
        # print(name)

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
        # self.creator_mode = "user"
        self.local_save = False

        ######## WARNINGS #####

        warning = self.check_entry_creator('save')
        if warning != None:
            warning_window(warning)
            return

        ###### Check if Admin Mode is activated ####

        self.creator_mode = self.check_for_admin_mode()

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

        if self.creator_mode == "user":

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

        # print(list_images_new_names)
        # return
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

        if self.creator_mode == "admin":
            window_title = "Admin Modus - Aufgabe erfolgreich gespeichert"
        if self.creator_mode == "user":
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

        self.adapt_choosing_list("sage")

    def push_full_database(self):
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
            # print(missing_variation_numbers)




        
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
        # print(list_missing_file)
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
        # # print(maximum)

        # for i in range(1,maximum+1):
        #     if i not in _list:
        #         print(i)
        #     else:
        #         print('existiert: {}'.format(i))    
            
        # print(_database_addon.all())
        # print(database.all())
        # print(files)

    
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
            # print(image)
            if is_empty(_list):
                list_unused_images.append(image)

            self.progress_cleanup_value += 1
            self.progress_cleanup.setValue(self.progress_cleanup_value)


        return list_unused_images
            


    def database_clean_up(self):
        refresh_ddb(self, auto_update=True)


        # table_lama_typ2 = _database.table('table_lama_2')
        # all_files_typ2 = table_lama_typ2.all()


        # table_lama_cria = _database.table('table_cria')
        # all_files_cria = table_lama_cria.all()

        image_folder = os.path.join(path_database, "Bilder")
        progress_maximum = len(dict_gk) + len(os.listdir(image_folder)) + 2

        self.progress_cleanup_value = 0
        self.progress_cleanup = QtWidgets.QProgressDialog("Fehlerbericht wird erstellt ...", "",self.progress_cleanup_value,progress_maximum)
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


        

    # def action_push_database(self, admin, file_list, message = None, worker_text = "Aufgabe wird hochgeladen ..."):
    #     QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
    #     if check_internet_connection() == False:
    #         critical_window("Stellen Sie sicher, dass eine Verbindung zum Internet besteht und versuchen Sie es erneut.",
    #             titel="Keine Internetverbindung",
    #         )
    #         return

    #     # text = worker_text + " (1%)"
    #     # if admin == True:
    #     #     text = "Änderungen überprüfen ..."
    #     # else:
    #     #     text = "Aufgabe wird hochgeladen ... (1%)"

    #     Dialog = QtWidgets.QDialog()
    #     ui = Ui_Dialog_processing()
    #     ui.setupUi(Dialog, worker_text)

    #     thread = QtCore.QThread(Dialog)
    #     worker = Worker_PushDatabase()
    #     worker.finished.connect(Dialog.close)
    #     worker.moveToThread(thread)
    #     thread.started.connect(partial(worker.task, ui, admin, file_list, message, worker_text))
    #     thread.start()
    #     thread.exit()
    #     Dialog.exec()
    #     QtWidgets.QApplication.restoreOverrideCursor()
    #     if worker.changes_found == False:
    #         information_window("Es wurden keine Änderungen gefunden.")
    #     elif worker.changes_found == "error":
    #         critical_window(
    #             "Es ist ein Fehler aufgetreten. Die Datenbank konnte nicht hochgeladen werden. Bitte versuchen Sie es später erneut."
    #         )
    #     elif admin == True:
    #         information_window("Die Datenbank wurde erfolgreich hochgeladen.")

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

    def action_add_file(self):
        self.update_gui("widgets_create")
        self.suchfenster_reset()
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
        i=0
        for aufgabe in self.list_alle_aufgaben_sage:
            index_item = self.list_alle_aufgaben_sage.index(aufgabe)
            typ = get_aufgabentyp(self.chosen_program, aufgabe)

            aufgabe_total = get_aufgabe_total(aufgabe.replace(" (lokal)", ""), typ)
            if aufgabe_total == None:
                list_aufgaben_errors.append(aufgabe)
                continue

            neue_aufgaben_box = self.create_neue_aufgaben_box(
                index_item, aufgabe, aufgabe_total
            )
            self.gridLayout_8.addWidget(neue_aufgaben_box, index_item, 0, 1, 1)
            index_item + 1

            self.add_image_path_to_list(aufgabe.replace(" (lokal)", ""))
            self.progress.setValue(i)
            i+=1
        self.spacerItem = QtWidgets.QSpacerItem(
            20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_8.addItem(self.spacerItem, index_item + 1, 0, 1, 1)

        
        return list_aufgaben_errors

    # def open_progress_bar(self):
    #     # for i in range(100):
    #     #     # print(self.progressbar_value)
    #     #     self.spinBox_2.setValue(i)
    #     #     time.sleep(0.2)
    #     # for i in range(100):
    #     #     self.spinBox_2.setValue(i)
    #     #     time.sleep(0.2)
    #     msgBox = QtWidgets.QMessageBox( QtWidgets.QMessageBox.Warning, "My title", "My text.", QtWidgets.QMessageBox.NoButton )

    #     # Get the layout
    #     l = msgBox.layout()

    #     # Hide the default button
    #     l.itemAtPosition( l.rowCount() - 1, 0 ).widget().hide()

    #     progress = QtWidgets.QProgressBar()

    #     # Add the progress bar at the bottom (last row + 1) and first column with column span
    #     l.addWidget(progress,l.rowCount(), 0, 1, l.columnCount(), Qt.AlignCenter )

    #     msgBox.exec()        

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

        try:
            if self.chosen_program == loaded_file["data_gesamt"]["program"]:
                if self.list_alle_aufgaben_sage != []:
                    self.reset_sage()
            else:
                response = self.change_program()
                if response == False:
                    QtWidgets.QApplication.restoreOverrideCursor()
                    return
        except KeyError:
            warning_window(
                "Die geöffnete *.lama-Datei ist veraltet und kann nur mit der Version LaMA 1.x geöffnet werden.",
                "Bitte laden Sie eine aktuelle *.lama-Datei oder kontaktieren Sie lama.helpme@gmail.com, wenn Sie Hilfe benötigen.",
            )
            return
        self.update_gui("widgets_sage")
        self.dict_all_infos_for_file = self.load_file(self.saved_file_path)


        self.list_alle_aufgaben_sage = self.dict_all_infos_for_file[
            "list_alle_aufgaben"
        ]

        self.spinBox_nummer.setValue(self.dict_all_infos_for_file["data_gesamt"]["#"])
        self.lineEdit_klasse.setText(
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

        try:
            self.dict_sage_ausgleichspunkte_chosen = self.dict_all_infos_for_file[
                "dict_ausgleichspunkte"
            ]
        except KeyError:
            self.dict_sage_ausgleichspunkte_chosen = {}

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

        list_aufgaben_errors = self.sage_load_files()
        self.progress.cancel()



        if not is_empty(list_aufgaben_errors):
            errors = ", ".join(list_aufgaben_errors)
            if len(list_aufgaben_errors)==1:
                _list = ["Aufgabe","konnte","wurde", "wird"]
            else:
                _list = ["Aufgaben","konnten","wurden", "werden"]

            warning_window(
                "Die {0} {1} {2} nicht gefunden werden, da sie gelöscht oder umbenannt {3}.\nSie {4} daher ignoriert.".format(
                    _list[0], errors, _list[1], _list[2], _list[3]
                )
            )             
            for aufgabe in list_aufgaben_errors:
                self.dict_all_infos_for_file["list_alle_aufgaben"].remove(aufgabe)

     

        self.update_punkte()


        self.spinBox_default_pkt.setValue(
            self.dict_all_infos_for_file["data_gesamt"]["Typ1 Standard"]
        )

        for aufgabe in self.list_alle_aufgaben_sage:
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

    def define_titlepage(self):
        if self.comboBox_pruefungstyp.currentText() == "Quiz":
            print("not yet working")
            return
            Dialog = QtWidgets.QDialog(
                None,
                QtCore.Qt.WindowSystemMenuHint
                | QtCore.Qt.WindowTitleHint
                | QtCore.Qt.WindowCloseButtonHint,
            )
            ui = Ui_Dialog_random_quiz()
            ui.setupUi(Dialog, self)
            # self.Dialog.show()
            response = Dialog.exec()
            if response == 0:
                return

            chosen_gks = ui.random_quiz_response[1]

            random_list = []
            for all in self.beispieldaten_dateipfad_1:
                for gks in chosen_gks:
                    if gks in all:
                        _file = os.path.basename(self.beispieldaten_dateipfad_1[all])
                        filename, extension = os.path.splitext(_file)
                        random_list.append(filename)

            if random_list == []:
                for all in self.beispieldaten_dateipfad_1:
                    _file = os.path.basename(self.beispieldaten_dateipfad_1[all])
                    filename, extension = os.path.splitext(_file)
                    if (
                        filename.split(" - ")[0] in dict_gk.values()
                    ):  # ignore all not examples not in gks
                        random_list.append(filename)

            if len(random_list) < ui.random_quiz_response[0]:
                number_examples = len(random_list)
                warning_window(
                    "Es sind insgesamt weniger Aufgaben enthalten ({0}), als die ausgwählte Anzahl der Aufgaben ({1}).".format(
                        len(random_list),
                        ui.random_quiz_response[0],
                    ),
                    "Es werden alle vorhandenen Aufgaben in zufälliger Reihenfolge ausgegeben.",
                    "Anzahl der Aufgaben",
                )
            else:
                number_examples = ui.random_quiz_response[0]

            sampling = random.sample(random_list, number_examples)

            if not is_empty(self.list_alle_aufgaben_sage):
                response = question_window(
                    "Sind Sie sicher, dass Sie das Fenster zurücksetzen wollen und die erstellte Datei löschen möchten?",
                    titel="Datei löschen?",
                )

                if response == False:
                    return

                for aufgabe in self.list_alle_aufgaben_sage[:]:
                    self.btn_delete_pressed(aufgabe)
            # self.list_alle_aufgaben_sage = []

            QtWidgets.QApplication.setOverrideCursor(
                QtGui.QCursor(QtCore.Qt.WaitCursor)
            )

            for aufgabe in sampling:
                self.sage_aufgabe_add(aufgabe)
                infos = self.collect_all_infos_aufgabe(aufgabe)
                self.dict_alle_aufgaben_sage[aufgabe] = infos

                self.build_aufgaben_schularbeit(aufgabe)  # aufgabe, aufgaben_verteilung

            QtWidgets.QApplication.restoreOverrideCursor()

            # self.list_alle_aufgaben_sage = []
            # for all in sampling:
            #     self.list_alle_aufgaben_sage.append(all)

            # for all in self.list_alle_aufgaben_sage:
            #     self.build_aufgaben_schularbeit(all)

        else:
            if self.chosen_program == "lama":
                dict_titlepage = self.dict_titlepage
            if self.chosen_program == "cria":
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
        if self.combobox_beurteilung.currentIndex() == 0:
            self.groupBox_beurteilungsraster.hide()
            self.groupBox_notenschl.show()
        if self.combobox_beurteilung.currentIndex() == 1:
            self.groupBox_notenschl.hide()
            self.groupBox_beurteilungsraster.show()
        if self.combobox_beurteilung.currentIndex() == 2:
            self.groupBox_notenschl.hide()
            self.groupBox_beurteilungsraster.hide()

        self.update_punkte()

    def get_aufgabenverteilung(self):
        num_typ1 = 0
        num_typ2 = 0
        for all in self.list_alle_aufgaben_sage:
            typ = get_aufgabentyp(self.chosen_program, all)
            if typ == 1:
                num_typ1 += 1
            if typ == 2:
                num_typ2 += 1

        return [num_typ1, num_typ2]

    def sage_aufgabe_add(self, aufgabe):
        if self.chosen_program == "lama":

            old_num_typ1, old_num_typ2 = self.get_aufgabenverteilung()

            typ = get_aufgabentyp(self.chosen_program, aufgabe)
            if typ == 1:
                self.list_alle_aufgaben_sage.insert(old_num_typ1, aufgabe)
            if typ == 2:
                self.list_alle_aufgaben_sage.append(aufgabe)

        if self.chosen_program == "cria":
            self.list_alle_aufgaben_sage.append(aufgabe)

        num_typ1, num_typ2 = self.get_aufgabenverteilung()
        num_total = len(self.list_alle_aufgaben_sage)

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
        list_sage_examples_typ1 = []
        list_sage_examples_typ2 = []

        for all in self.list_alle_aufgaben_sage:
            if re.search("[A-Z]", all) == None:
                list_sage_examples_typ2.append(all)
            else:
                list_sage_examples_typ1.append(all)

        self.list_alle_aufgaben_sage.clear()
        self.list_alle_aufgaben_sage.extend(list_sage_examples_typ1)
        self.list_alle_aufgaben_sage.extend(list_sage_examples_typ2)
        num_typ1 = len(list_sage_examples_typ1)
        num_typ2 = len(list_sage_examples_typ2)
        num_total = len(self.list_alle_aufgaben_sage)

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

    def btn_up_pressed(self, aufgabe):
        a, b = (
            self.list_alle_aufgaben_sage.index(aufgabe),
            self.list_alle_aufgaben_sage.index(aufgabe) - 1,
        )
        self.list_alle_aufgaben_sage[a], self.list_alle_aufgaben_sage[b] = (
            self.list_alle_aufgaben_sage[b],
            self.list_alle_aufgaben_sage[a],
        )

        self.build_aufgaben_schularbeit(aufgabe)

    def btn_down_pressed(self, aufgabe):

        a, b = (
            self.list_alle_aufgaben_sage.index(aufgabe),
            self.list_alle_aufgaben_sage.index(aufgabe) + 1,
        )
        self.list_alle_aufgaben_sage[a], self.list_alle_aufgaben_sage[b] = (
            self.list_alle_aufgaben_sage[b],
            self.list_alle_aufgaben_sage[a],
        )

        self.build_aufgaben_schularbeit(aufgabe)

    def erase_aufgabe(self, aufgabe):
        del self.dict_variablen_punkte[aufgabe]
        del self.dict_variablen_abstand[aufgabe]
        self.list_alle_aufgaben_sage.remove(aufgabe)
        if get_aufgabentyp(self.chosen_program, aufgabe) == 2:
            del self.dict_variablen_label[aufgabe]
        if aufgabe in self.dict_sage_ausgleichspunkte_chosen:
            del self.dict_sage_ausgleichspunkte_chosen[aufgabe]
        if aufgabe in self.dict_sage_hide_show_items_chosen:
            del self.dict_sage_hide_show_items_chosen[aufgabe]
        if aufgabe in self.dict_sage_individual_change:
            del self.dict_sage_individual_change[aufgabe]

    def btn_delete_pressed(self, aufgabe):
        try:
            self.dict_sage_individual_change[aufgabe]
            if not is_empty(self.dict_sage_individual_change[aufgabe]):
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
        index = self.list_alle_aufgaben_sage.index(aufgabe)

        if index + 1 == len(self.list_alle_aufgaben_sage):
            self.delete_widget(self.gridLayout_8, index)
            self.erase_aufgabe(aufgabe)

        else:
            self.erase_aufgabe(aufgabe)
            self.build_aufgaben_schularbeit(self.list_alle_aufgaben_sage[index])

        self.update_punkte()
        self.button_was_deleted = True

    def spinbox_pkt_changed(self):  # , aufgabe, spinbox_abstand
        self.update_punkte()

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
        num_typ2 = self.get_aufgabenverteilung()[1]
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

    def get_number_ausgleichspunkte_gesamt(self):
        number_ausgleichspkt_gesamt = 0
        for aufgabe in self.list_alle_aufgaben_sage:
            typ = get_aufgabentyp(self.chosen_program, aufgabe)
            if typ == 2:
                # collect_content(self, aufgabe)
                aufgabe_total = get_aufgabe_total(aufgabe, "lama_2")
                number = self.count_ausgleichspunkte(aufgabe_total["content"])
                number_ausgleichspkt_gesamt += number

        return number_ausgleichspkt_gesamt

    def update_beurteilungsraster(self):

        punkteverteilung = self.get_punkteverteilung()
        number_ausgleichspunkte_gesamt = self.get_number_ausgleichspunkte_gesamt()
        self.label_typ1_pkt.setText(
            _translate(
                "MainWindow", "Punkte Typ 1: {}".format(punkteverteilung[1]), None
            )
        )
        self.label_typ2_pkt.setText(
            _translate(
                "MainWindow",
                "Punkte Typ 2: {0} (davon Ausgleichspunkte: {1})".format(
                    punkteverteilung[2], number_ausgleichspunkte_gesamt
                ),
                None,
            )
        )

    def update_punkte(self):
        gesamtpunkte = self.get_punkteverteilung()[0]
        num_typ1, num_typ2 = self.get_aufgabenverteilung()
        num_total = len(self.list_alle_aufgaben_sage)

        if self.combobox_beurteilung.currentIndex() == 0:
            self.update_notenschluessel()

        if self.combobox_beurteilung.currentIndex() == 1:
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
        return self.dict_variablen_abstand[aufgabe].value()

    def count_ausgleichspunkte(self, content):
        number = content.count("\ASubitem")
        number = number + content.count("\Aitem")
        number = number + content.count("fbox{A}")

        return number

    def create_neue_aufgaben_box(self, index, aufgabe, aufgabe_total):
        typ = get_aufgabentyp(self.chosen_program, aufgabe)

        aufgaben_verteilung = self.get_aufgabenverteilung()

        if self.chosen_program == "cria":
            if aufgabe_total["klasse"] == None:
                klasse = ""
            else:
                klasse = "{0}. Klasse - ".format(aufgabe_total["klasse"][1])

            new_groupbox = create_new_groupbox(
                self.scrollAreaWidgetContents_2, "{0}. Aufgabe".format(index + 1)
            )
        else:
            new_groupbox = create_new_groupbox(
                self.scrollAreaWidgetContents_2,
                "{0}. Aufgabe (Typ{1})".format(index + 1, typ),
            )

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
        gridLayout_gB.addWidget(label_aufgabe, 1, 0, 1, 1)

        label_titel = create_new_label(
            new_groupbox, "Titel: {}".format(aufgabe_total["titel"]), True
        )
        gridLayout_gB.addWidget(label_titel, 2, 0, 1, 1)

        groupbox_pkt = create_new_groupbox(new_groupbox, "Punkte")
        groupbox_pkt.setSizePolicy(SizePolicy_fixed)
        gridLayout_gB.addWidget(groupbox_pkt, 0, 1, 3, 1, QtCore.Qt.AlignRight)

        if typ == 1:
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

        if typ == 2:
            groupbox_pkt.setToolTip(
                "Die Punkte geben die Gesamtpunkte dieser Aufgabe an.\nEs müssen daher auch die Ausgleichspunkte berücksichtigt werden."
            )

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

        button_up = create_standard_button(
            new_groupbox,
            "",
            partial(self.btn_up_pressed, aufgabe),
            QtWidgets.QStyle.SP_ArrowUp,
        )

        gridLayout_gB.addWidget(button_up, 0, 3, 2, 1)
        number = index + 1
        if (typ == 1 or typ == None) and number == 1:
            button_up.setEnabled(False)
        if typ == 2 and number == aufgaben_verteilung[0] + 1:
            button_up.setEnabled(False)

        button_down = create_standard_button(
            new_groupbox,
            "",
            partial(self.btn_down_pressed, aufgabe),
            QtWidgets.QStyle.SP_ArrowDown,
        )
        gridLayout_gB.addWidget(button_down, 0, 4, 2, 1)

        if typ == 1 and number == aufgaben_verteilung[0]:
            button_down.setEnabled(False)
        if (typ == 2 or typ == None) and number == len(self.list_alle_aufgaben_sage):
            button_down.setEnabled(False)

        button_delete = create_standard_button(
            new_groupbox,
            "",
            partial(self.btn_delete_pressed, aufgabe),
            QtWidgets.QStyle.SP_DialogCancelButton,
        )
        gridLayout_gB.addWidget(button_delete, 0, 5, 2, 1)

        groupbox_abstand_ausgleich = create_new_groupbox(new_groupbox, "Abstand (cm)  ")
        groupbox_abstand_ausgleich.setSizePolicy(SizePolicy_fixed)
        # groupbox_abstand.setMaximumSize(QtCore.QSize(100, 16777215))
        gridLayout_gB.addWidget(groupbox_abstand_ausgleich, 0, 2, 3, 1)

        verticalLayout_abstand = QtWidgets.QVBoxLayout(groupbox_abstand_ausgleich)
        verticalLayout_abstand.setObjectName("verticalLayout_abstand")

        abstand = aufgabe_total["abstand"]
        spinbox_abstand = create_new_spinbox(groupbox_abstand_ausgleich)
        spinbox_abstand.setValue(abstand)
        self.dict_variablen_abstand[aufgabe] = spinbox_abstand

        spinbox_abstand.valueChanged.connect(self.spinbox_abstand_changed)
        verticalLayout_abstand.addWidget(spinbox_abstand)

        num_ap = self.count_ausgleichspunkte(aufgabe_total["content"])
        if typ == 2:
            groupbox_abstand_ausgleich.setTitle("Ausgleichspkte")
            spinbox_abstand.hide()
            self.count_ausgleichspunkte(aufgabe_total["content"])
            label_ausgleichspkt = create_new_label(
                groupbox_abstand_ausgleich,
                str(num_ap),
            )
            label_ausgleichspkt.setStyleSheet("padding-top: 5px; padding-bottom: 5px;")
            verticalLayout_abstand.addWidget(label_ausgleichspkt)

            self.dict_variablen_label[aufgabe] = label_ausgleichspkt
        else:
            groupbox_abstand_ausgleich.setToolTip("Neue Seite: Abstand=99")

        pushbutton_ausgleich = create_new_button(
            new_groupbox,
            "Aufgabe bearbeiten...",
            partial(self.pushButton_ausgleich_pressed, aufgabe),
        )
        pushbutton_ausgleich.setStyleSheet("padding: 6px")
        pushbutton_ausgleich.setSizePolicy(SizePolicy_fixed)
        # pushbutton_ausgleich.setMaximumSize(QtCore.QSize(220, 30))
        gridLayout_gB.addWidget(pushbutton_ausgleich, 2, 3, 1, 3)

        # pushbutton_aufgabe_bearbeiten = create_new_button(groupbox_pkt, 'Aufgabe bearbeiten', still_to_define)
        # gridLayout_gB.addWidget(pushbutton_aufgabe_bearbeiten, 0,1,1,1)

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
        # print(content)
        # print(aufgabe_total['bilder'])

        for image in aufgabe_total["bilder"]:
            self.list_copy_images.append(image)

        # if "\\includegraphics" in content:
        #     matches = re.findall("/Bilder/(.+.eps)}", content)
        #     for image in matches:
        #         print(image)
        #         self.list_copy_images.append(image)

    def build_aufgaben_schularbeit(self, aufgabe):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        try:
            self.gridLayout_8.removeItem(self.spacerItem)
        except AttributeError:
            pass

        index = self.list_alle_aufgaben_sage.index(aufgabe)

        if index == 0:
            start_value = index
        else:
            start_value = index - 1

        for i in reversed(range(start_value, self.gridLayout_8.count() + 1)):
            self.delete_widget(self.gridLayout_8, i)

        for item in self.list_alle_aufgaben_sage[start_value:]:
            index_item = self.list_alle_aufgaben_sage.index(item)
            typ = get_aufgabentyp(self.chosen_program, item)

            aufgabe_total = get_aufgabe_total(item.replace(" (lokal)", ""), typ)
            # item_infos = self.collect_all_infos_aufgabe(item)
            neue_aufgaben_box = self.create_neue_aufgaben_box(
                index_item, item, aufgabe_total
            )

            self.gridLayout_8.addWidget(neue_aufgaben_box, index_item, 0, 1, 1)
            index_item + 1

        self.spacerItem = QtWidgets.QSpacerItem(
            20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_8.addItem(self.spacerItem, index_item + 1, 0, 1, 1)

        self.add_image_path_to_list(aufgabe.replace(" (lokal)", ""))

        self.update_punkte()

        QtWidgets.QApplication.restoreOverrideCursor()

    def pushButton_ausgleich_pressed(self, aufgabe):
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

            if aufgabe in self.dict_sage_ausgleichspunkte_chosen.keys():
                list_sage_ausgleichspunkte_chosen = (
                    self.dict_sage_ausgleichspunkte_chosen[aufgabe]
                )
            else:
                list_sage_ausgleichspunkte_chosen = []
                for index, all in enumerate(split_content):
                    if "\\fbox{A}" in all or "\\ASubitem" in all:
                        list_sage_ausgleichspunkte_chosen.append(index)
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
            list_sage_ausgleichspunkte_chosen = []
            split_content = None

        if aufgabe in self.dict_sage_individual_change.keys():
            sage_individual_change = self.dict_sage_individual_change[aufgabe]
        else:
            sage_individual_change = None

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
            list_sage_ausgleichspunkte_chosen,
            list_sage_hide_show_items_chosen,
            sage_individual_change,
            self.display_mode,
            self.developer_mode_active,
            self.chosen_program,
        )

        Dialog.exec_()

        if ui.sage_individual_change != None:
            self.dict_sage_individual_change[aufgabe] = ui.sage_individual_change

        if typ == 2:
            if not is_empty(ui.list_sage_ausgleichspunkte_chosen):
                self.dict_sage_ausgleichspunkte_chosen[
                    aufgabe
                ] = ui.list_sage_ausgleichspunkte_chosen
            elif aufgabe in self.dict_sage_ausgleichspunkte_chosen:
                del self.dict_sage_ausgleichspunkte_chosen[aufgabe]

            if not is_empty(ui.list_sage_hide_show_items_chosen):
                self.dict_sage_hide_show_items_chosen[
                    aufgabe
                ] = ui.list_sage_hide_show_items_chosen
            elif aufgabe in self.dict_sage_hide_show_items_chosen:
                del self.dict_sage_hide_show_items_chosen[aufgabe]

            self.dict_variablen_label[aufgabe].setText(
                "{}".format(len(ui.list_sage_ausgleichspunkte_chosen))
            )

        self.update_punkte()

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

    def nummer_clicked(self, item):
        aufgabe = item.text()

        # if self.chosen_program == "cria":
        # klasse = self.get_klasse("sage")
        # aufgabe = klasse + "." + aufgabe

        if aufgabe in self.list_alle_aufgaben_sage:
            return

        self.sage_aufgabe_add(aufgabe)

        self.build_aufgaben_schularbeit(aufgabe)  # aufgabe, aufgaben_verteilung
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
                    "Ausgewählte Aufgabe: {0} ({1})".format(
                        item.text(),
                        self.comboBox_klassen_fb_cria.currentText(),
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

    def comboBox_kapitel_changed(self, list_mode):
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

    def collect_all_infos_for_creating_file(self):
        self.dict_all_infos_for_file = {}

        self.dict_all_infos_for_file[
            "list_alle_aufgaben"
        ] = self.list_alle_aufgaben_sage

        _dict = {}
        for aufgabe in self.list_alle_aufgaben_sage:
            _dict[aufgabe] = [
                self.get_punkte_aufgabe_sage(aufgabe),
                self.get_abstand_aufgabe_sage(aufgabe),
            ]

        self.dict_all_infos_for_file["dict_alle_aufgaben_pkt_abstand"] = _dict

        # self.dict_all_infos_for_file[
        #     "dict_alle_aufgaben"
        # ] = self.dict_alle_aufgaben_sage

        ### include dictionary of changed 'ausgleichspunkte' ###
        self.dict_all_infos_for_file[
            "dict_ausgleichspunkte"
        ] = self.dict_sage_ausgleichspunkte_chosen

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
        if self.combobox_beurteilung.currentIndex() == 0:
            beurteilung = "ns"
        elif self.combobox_beurteilung.currentIndex() == 1:
            beurteilung = "br"
        elif self.combobox_beurteilung.currentIndex() == 2:
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
            "Klasse": self.lineEdit_klasse.text(),
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

    def add_content_to_tex_file(
        self, aufgabe, aufgabe_total, filename_vorschau, first_typ2, ausgabetyp
    ):

        if get_aufgabentyp(self.chosen_program, aufgabe) == 2:
            if first_typ2 == False:
                header = "\\newpage \n\n\subsubsection{Typ 2 Aufgaben}\n\n"
                first_typ2 = True
            else:
                header = "\\newpage\n\n"
        else:
            header = ""

        punkte = self.get_punkte_aufgabe_sage(aufgabe)
        abstand = self.get_abstand_aufgabe_sage(aufgabe)
        if punkte == 0:
            begin = "\\begin{enumerate}\item[\\stepcounter{number}\\thenumber.]"
            end = "\end{enumerate}"
        elif aufgabe_total["pagebreak"] == False:
            begin = begin_beispiel(aufgabe_total["themen"], punkte)
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

        with open(filename_vorschau, "a+", encoding="utf8") as vorschau:
            vorschau.write(header)
            vorschau.write(begin)

        if aufgabe in self.dict_sage_individual_change:
            content = self.dict_sage_individual_change[aufgabe]
            # with open(filename_vorschau, "a+", encoding="utf8") as vorschau:
            #     vorschau.write(self.dict_sage_individual_change[aufgabe])
        elif aufgabe in self.dict_sage_ausgleichspunkte_chosen:
            full_content = aufgabe_total["content"]

            split_content = self.split_content(aufgabe, aufgabe_total["content"])
            content = edit_content_ausgleichspunkte(
                self, aufgabe, split_content, full_content
            )

            # content = "\n".join(split_content)
            # with open(filename_vorschau, "a+", encoding="utf8") as vorschau:
            #     vorschau.write(content)
        elif aufgabe in self.dict_sage_hide_show_items_chosen:
            full_content = aufgabe_total["content"]
            split_content = self.split_content(aufgabe, aufgabe_total["content"])
            split_content = prepare_content_for_hide_show_items(split_content)
            content = edit_content_hide_show_items(
                self, aufgabe, split_content, full_content
            )
            # print(content)
            # with open(filename_vorschau, "a+", encoding="utf8") as vorschau:
            #     vorschau.write(content)
            # for index in self.dict_sage_ausgleichspunkte_chosen[aufgabe]:
            #     split_content[index] = split_content[index].replace("SUBitem", "")

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

        else:
            content = aufgabe_total["content"]
        if ausgabetyp == "schularbeit" and is_empty(aufgabe_total['bilder'])  == False:
            for image in aufgabe_total['bilder']:
                content = re.sub(r"{{../_database.*{0}}}".format(image),"{{{0}}}".format(image),content)

        

        with open(filename_vorschau, "a+", encoding="utf8") as vorschau:
            vorschau.write(content)
            vorschau.write(end)
            vorschau.write(vspace)
            vorschau.write("\n\n")

        return first_typ2

    def create_body_of_tex_file(self, filename_vorschau, ausgabetyp):
        first_typ2 = False
        for aufgabe in self.list_alle_aufgaben_sage:
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

    def pushButton_vorschau_pressed(
        self,
        ausgabetyp,
        index=0,
        maximum=0,
        pdf=True,
        lama=True,
        single_file_index=None,
        filename_vorschau=os.path.join(
            path_programm, "Teildokument", "Schularbeit_Vorschau.tex"
        ),
    ):

        if ausgabetyp == "vorschau":
            self.collect_all_infos_for_creating_file()
        # print(self.dict_all_infos_for_file)
        # return
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        # if ausgabetyp == "vorschau":
        #     filename_vorschau = os.path.join(
        #         path_programm, "Teildokument", "Schularbeit_Vorschau.tex"
        #     )
        # if ausgabetyp == "schularbeit":

        #     dict_umlaute = {
        #         "Ä": "AE",
        #         "ä": "ae",
        #         "Ö": "OE",
        #         "ö": "oe",
        #         "Ü": "ue",
        #         "ü": "ue",
        #         "ß": "ss",
        #     }
        #     if index == 0:

        #         self.chosen_path_schularbeit_erstellen = (
        #             QtWidgets.QFileDialog.getSaveFileName(
        #                 None,
        #                 "Speicherort wählen",
        #                 os.path.dirname(self.saved_file_path),
        #                 "TeX Dateien (*.tex);; Alle Dateien (*.*)",
        #             )
        #         )

        #         if self.chosen_path_schularbeit_erstellen[0] == "":
        #             QtWidgets.QApplication.restoreOverrideCursor()
        #             return
        #         self.saved_file_path = self.chosen_path_schularbeit_erstellen[0]

        #         dirname = os.path.dirname(self.chosen_path_schularbeit_erstellen[0])
        #         filename = os.path.basename(self.chosen_path_schularbeit_erstellen[0])
        #         if sys.platform.startswith("linux"):
        #             filename = filename + ".tex"

        #         for character in dict_umlaute.keys():
        #             if character in filename:
        #                 filename = filename.replace(character, dict_umlaute[character])
        #         filename_vorschau = os.path.join(dirname, filename)

        #         if lama == True:
        #             Ui_MainWindow.sage_save(self, filename_vorschau)  #

            # else:
            #     dirname = os.path.dirname(self.chosen_path_schularbeit_erstellen[0])
            #     filename = os.path.basename(self.chosen_path_schularbeit_erstellen[0])
            #     for character in dict_umlaute.keys():
            #         if character in filename:
            #             filename = filename.replace(character, dict_umlaute[character])
            #     filename_vorschau = os.path.join(dirname, filename)

        self.dict_gruppen = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F"}

        if filename_vorschau == "":
            QtWidgets.QApplication.restoreOverrideCursor()
            return

        if self.chosen_program == "lama":
            dict_titlepage = self.dict_titlepage
        if self.chosen_program == "cria":
            dict_titlepage = self.dict_titlepage_cria

        if self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"] == "Quiz":
            beamer_mode = True
        else:
            beamer_mode = False

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
            header = "\\subsubsection{Typ 1 Aufgaben}\n\n"

        else:
            header = ""

        # vorschau = open(filename_vorschau, "w+", encoding="utf8")

        with open(filename_vorschau, "w+", encoding="utf8") as vorschau:
            vorschau.write(
                tex_preamble(solution=solution, random=gruppe, beamer_mode=beamer_mode)
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
            if self.dict_all_infos_for_file["data_gesamt"]["Beurteilung"] == "ns":
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

                with open(filename_vorschau, "a", encoding="utf8") as vorschau:
                    vorschau.write(
                        "\n\n\\null\\notenschluessel{0}{{{1}}}{{{2}}}{{{3}}}{{{4}}}".format(
                            zusatz,
                            notenschluessel[0] / 100,
                            notenschluessel[1] / 100,
                            notenschluessel[2] / 100,
                            notenschluessel[3] / 100,
                        )
                    )

        with open(filename_vorschau, "a", encoding="utf8") as vorschau:
            vorschau.write("\n\n")
            vorschau.write(tex_end)
            vorschau.write("\n\n")
            vorschau.write(
                "% Aufgabenliste: {}".format(", ".join(self.list_alle_aufgaben_sage))
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
            msg.setInformativeText("Vielen Dank für die Mithilfe LaMA zu verbessern.")
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

    def update_gui(self, chosen_gui):
        if self.chosen_program == "cria":
            chosen_gui = chosen_gui + "_cria"
        #     chosen_gui_list = eval(chosen_gui)
        # else:
        chosen_gui_list = eval(chosen_gui)

        self.chosen_gui = chosen_gui
        MainWindow.setMenuBar(self.menuBar)
        list_delete = []
        for item in list_widgets:
            if item != chosen_gui_list:
                list_delete += item
        for all in list_delete:
            if "action" in all:
                exec("self.%s.setEnabled(False)" % all)
                # exec("self.%s.setVisible(False)" % all)
            # elif "menu" in all:
            #     exec("self.menuBar.removeAction(self.%s.menuAction())" % all)
            elif "layout" in all.lower():
                exec("self.%s.setParent(None)" % all)
            else:
                exec("self.%s.hide()" % all)
        for all in chosen_gui_list:
            if "action" in all:
                exec("self.%s.setEnabled(True)" % all)
                # exec("self.%s.setVisible(True)" % all)
            # elif "menu" in all:
            #     exec("self.menuBar.addAction(self.%s.menuAction())" % all)
            elif "layout" in all.lower():
                exec("self.gridLayout.addLayout(self.{}, 0, 0, 1, 1)".format(all))
            else:
                exec("self.%s.show()" % all)

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
            MainWindow.setTabOrder(self.spinBox_nummer, self.dateEdit)
            MainWindow.setTabOrder(self.dateEdit, self.lineEdit_klasse)
            self.adapt_choosing_list("sage")
            # self.listWidget.itemClicked.connect(self.nummer_clicked)
        if chosen_gui == "widgets_feedback" or chosen_gui == "widgets_feedback_cria":
            self.adapt_choosing_list("feedback")

        if self.developer_mode_active == False:
            self.menuBar.removeAction(self.menuDeveloper.menuAction())
            # self.listWidget_fb.itemClicked.connect(self.nummer_clicked_fb)
            # self.listWidget_fb_cria.itemClicked.connect(self.nummer_clicked_fb)

        if (chosen_gui == "widgets_create" and "###" in self.lineEdit_titel.text()) or (
            chosen_gui == "widgets_edit"
        ):
            self.cb_matura_tag.show()
            self.cb_no_grade_tag.hide()
        elif (
            chosen_gui == "widgets_create_cria" and "###" in self.lineEdit_titel.text()
        ) or (chosen_gui == "widgets_edit_cria"):
            self.cb_matura_tag.hide()
            self.cb_no_grade_tag.show()

        else:
            self.cb_matura_tag.hide()
            self.cb_no_grade_tag.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle("Fusion")
    app.setStyleSheet(
        """QToolTip {{ color: white; background-color: {0}; border: 0px; }}
    """.format(
            get_color(blue_7)
        )
    )

    # font = QtGui.QFont("Calibri Light", 9)
    # app.setFont(font)
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, white)  # Window background
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.black)
    palette.setColor(QtGui.QPalette.Base, white)
    palette.setColor(QtGui.QPalette.AlternateBase, blue_2)
    palette.setColor(QtGui.QPalette.ToolTipBase, white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, black)
    palette.setColor(QtGui.QPalette.Button, blue_3)  # blue_4

    # palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.WindowText, gray)
    palette.setColor(
        QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, QtCore.Qt.darkGray
    )

    # palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.Base, QtCore.Qt.gray)
    # palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    # palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)

    palette.setColor(QtGui.QPalette.Highlight, blue_7)
    palette.setColor(QtGui.QPalette.HighlightedText, white)

    ### Dark Mode
    palette_dark_mode = QtGui.QPalette()
    palette_dark_mode.setColor(
        QtGui.QPalette.Window, QtGui.QColor(53, 53, 53)
    )  # Window background
    palette_dark_mode.setColor(QtGui.QPalette.WindowText, white)
    palette_dark_mode.setColor(QtGui.QPalette.Text, white)
    palette_dark_mode.setColor(QtGui.QPalette.Base, dark_gray)
    palette_dark_mode.setColor(QtGui.QPalette.ToolTipBase, blue_7)
    palette_dark_mode.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    palette_dark_mode.setColor(QtGui.QPalette.ButtonText, white)
    palette_dark_mode.setColor(QtGui.QPalette.HighlightedText, white)
    palette_dark_mode.setColor(QtGui.QPalette.Highlight, blue_6)
    palette_dark_mode.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Light, dark_gray)
    # palette_dark_mode.setColor(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, white)

    try:
        with open(lama_settings_file, "r", encoding="utf8") as f:
            _dict = json.load(f)
        display_mode = _dict["display"]
        if display_mode == 1:
            app.setPalette(palette_dark_mode)
        else:
            app.setPalette(palette)
    except FileNotFoundError:
        app.setPalette(palette)

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
    splash.setPalette(palette)
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

    # Simulate something that takes time
    i = step_progressbar(i, "threading")
    import threading

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

    i = step_progressbar(i, "random")
    import random

    i = step_progressbar(i, "functools")
    import functools

    i = step_progressbar(i, "partial")
    from functools import partial

    i = step_progressbar(i, "yaml")
    import yaml

    i = step_progressbar(i, "pillow")
    from PIL import Image  ## pillow

    i = step_progressbar(i, "smtplib")
    import smtplib

    i = step_progressbar(i, "save_titlepage")
    from save_titlepage import create_file_titlepage, check_format_titlepage_save

    i = step_progressbar(i, "git_sync")
    from git_sync import (
        git_push_to_origin,
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
    from subwindows import read_credentials

    # from subwindows import (
    # Ui_Dialog_Welcome_Window,
    # Ui_Dialog_choose_type,
    # Ui_Dialog_titlepage,
    # Ui_Dialog_random_quiz,
    # Ui_Dialog_ausgleichspunkte,
    # Ui_Dialog_erstellen,
    # Ui_Dialog_speichern,
    # Ui_Dialog_variation,
    # Ui_Dialog_setup,
    # Ui_Dialog_developer,
    # read_credentials,
    # )
    i = step_progressbar(i, "translate")
    from translate import _fromUtf8, _translate

    i = step_progressbar(i, "create_pdf")
    from create_pdf import (
        prepare_tex_for_pdf,
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
        edit_content_quiz,
    )

    i = step_progressbar(i, "build_titlepage")
    from build_titlepage import get_titlepage_vorschau

    i = step_progressbar(i, "prepare_content_vorschau")
    from prepare_content_vorschau import (
        copy_logo_to_target_path,
        copy_included_images,
    )

    i = step_progressbar(i, "convert_image_to_eps")
    from convert_image_to_eps import convert_image_to_eps

    i = step_progressbar(i, "lama_stylesheets")
    from lama_stylesheets import *

    i = step_progressbar(i, "processing_window")
    from processing_window import Ui_Dialog_processing, Ui_ProgressBar

    i = step_progressbar(i, "bcrpyt")
    import bcrypt

    i = step_progressbar(i, "tinydb")

    from tinydb import Query, TinyDB

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

    i = step_progressbar(i, "tex_minimal")
    from tex_minimal import *

    i = step_progressbar(i, "filter_comands")
    from filter_commands import get_filter_string, filter_items, get_drafts

    i = step_progressbar(i, "mainwindow")
    # form = Form()
    # form.show()

    try:
        loaded_lama_file_path = sys.argv[1]
    except IndexError:
        loaded_lama_file_path = ""

    i = step_progressbar(i, "mainwindow")

    MainWindow = QMainWindow()
    # MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    screen_resolution = app.desktop().screenGeometry()
    screen_width, screen_height = screen_resolution.width(), screen_resolution.height()

    MainWindow.setGeometry(
        30, 30, round(screen_width * 0.5), round(screen_height * 0.8)
    )
    MainWindow.move(30, 30)
    i = step_progressbar(i, "mainwindow")

    ui = Ui_MainWindow()

    splash.finish(MainWindow)
    ui.setupUi(MainWindow)
    # i = step_progressbar(i, "MainWindow")
    # print(i)
    MainWindow.show()

    sys.exit(app.exec_())
