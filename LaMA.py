#!/usr/bin/python3
# -*- coding: utf-8 -*-
#### Version number ###
__version__ = "v2.3.0"
__lastupdate__ = "01/21"
##################
print("Loading...")
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
import git
from git import Repo, remote
import time
import threading
import sys
import os
from pathlib import Path
import datetime
import time
import json
import subprocess
import shutil
import re
import random
import functools
from functools import partial
import yaml
from PIL import Image  ## pillow
import smtplib
import urllib.request
from save_titlepage import create_file_titlepage, check_format_titlepage_save

from config import *

from create_new_widgets import *
from list_of_widgets import (
    widgets_search,
    widgets_create,
    widgets_sage,
    widgets_feedback,
    widgets_search_cria,
    widgets_sage_cria,
    widgets_create_cria,
    widgets_feedback_cria,
    list_widgets,
)
from subwindows import (
    Ui_Dialog_Welcome_Window,
    Ui_Dialog_choose_type,
    Ui_Dialog_titlepage,
    Ui_Dialog_random_quiz,
    Ui_Dialog_ausgleichspunkte,
    Ui_Dialog_erstellen,
    Ui_Dialog_speichern,
    Ui_Dialog_variation,
    Ui_Dialog_setup,
    Ui_Dialog_developer,
    read_credentials,
)
from translate import _fromUtf8, _translate
from sort_items import natural_keys, sorted_gks
from create_pdf import prepare_tex_for_pdf, create_pdf
from refresh_ddb import modification_date, refresh_ddb, search_files
from standard_dialog_windows import (
    warning_window,
    question_window,
    critical_window,
    information_window,
    custom_window,
)
from predefined_size_policy import *
from work_with_content import (
    collect_content,
    split_content_no_environment,
    split_aufgaben_content_new_format,
    split_aufgaben_content,
    edit_content_quiz,
    get_section_from_content,
)
from build_titlepage import get_titlepage_vorschau
from prepare_content_vorschau import (
    edit_content_vorschau,
    copy_logo_to_target_path,
    copy_included_images,
    split_content_at_beispiel_umgebung,
)
from convert_image_to_eps import convert_image_to_eps
from lama_colors import *
from lama_stylesheets import *
from processing_window import Ui_Dialog_processing
import bcrypt


try:
    loaded_lama_file_path = sys.argv[1]
except IndexError:
    loaded_lama_file_path = ""


dict_picture_path = {}


class Worker_DownloadDatabase(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    @QtCore.pyqtSlot()
    def task(self, database):
        try:
            # username = "chrisiweb"
            #lama-contributor
            # password = "access token"
            # remote = f"https://{username}:{password}@github.com/chrisiweb/lama_latest_update.git"
            remote = "https://github.com/chrisiweb/lama_latest_update.git"
            git.Repo.clone_from(remote, database)
            self.download_successfull = True
        except git.exc.GitCommandError:
            self.download_successfull = False

        self.finished.emit()       


class Ui_MainWindow(object):
    global dict_picture_path  # , set_chosen_gk #, list_sage_examples#, dict_alle_aufgaben_sage

    def __init__(self):
        path_programdata = os.getenv('PROGRAMDATA')
        database = os.path.join(path_programdata, "LaMA", "_database")    
        if not os.path.isdir(database):
            Dialog_Welcome = QtWidgets.QDialog(
                None,
                QtCore.Qt.WindowSystemMenuHint
                | QtCore.Qt.WindowTitleHint
                | QtCore.Qt.WindowCloseButtonHint,
            )
            ui = Ui_Dialog_Welcome_Window()
            ui.setupUi(Dialog_Welcome)

            bring_to_front(Dialog_Welcome)

            # self.Dialog.setFixedSize(self.Dialog.size())
            rsp = Dialog_Welcome.exec_()
            if rsp == 0:
                sys.exit(0)
            elif rsp == 1:
                text = "Die Datenbank wird heruntergeladen.\n\nDies kann einige Minuten dauern ..."
                Dialog = QtWidgets.QDialog()
                ui = Ui_Dialog_processing()
                ui.setupUi(Dialog, text, False)

                thread = QtCore.QThread(Dialog)
                worker = Worker_DownloadDatabase()
                worker.finished.connect(Dialog.close)
                worker.moveToThread(thread)
                rsp = thread.started.connect(partial(worker.task, database))
                thread.start()
                thread.exit()
                Dialog.exec()
                if worker.download_successfull == False:
                    critical_window("""
Datenbank konnte nicht heruntergeladen werden. Stellen Sie sicher, dass eine Verbindung zum Internet besteht und versuchen Sie es erneut.

Sollte das Problem weiterhin bestehen, melden Sie sich unter lama.helpme@gmail.com
""")
                    sys.exit()
                elif worker.download_successfull == True:
                    information_window(
"""Die Datenbank wurde erfolgreich heruntergeladen. LaMA kann ab sofort verwendet werden!
"""
                )



        self.dict_alle_aufgaben_sage = {}
        self.list_alle_aufgaben_sage = []
        self.dict_widget_variables = {}
        self.list_selected_topics_creator = []
        self.dict_variablen_punkte = {}
        self.dict_variablen_label = {}
        self.dict_sage_ausgleichspunkte_chosen = {}
        self.dict_sage_hide_show_items_chosen = {}
        self.dict_sage_individual_change = {}
        self.dict_chosen_topics = {}
        self.list_copy_images = []

        hashed_pw = read_credentials()
        path_lama_developer_credentials = os.path.join(os.getenv('LOCALAPPDATA'), "LaMA", "credentials")
        lama_developer_credentials = os.path.join(path_lama_developer_credentials, "developer_credentials.txt")
        self.developer_mode_active = False
        if os.path.isfile(lama_developer_credentials):
            with open(lama_developer_credentials, "rb") as file:
                password = file.read()
            if bcrypt.checkpw(password, hashed_pw):
                self.developer_mode_active = True
        print(self.developer_mode_active)   
        # with open(lama)
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
        self.check_for_update()
        try: 
            self.lama_settings["start_program"]
        except KeyError:
            self.lama_settings["start_program"] = 0
        if loaded_lama_file_path == "" and self.lama_settings["start_program"]==0:
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
            self.chosen_program= 'cria'
        elif self.lama_settings["start_program"] == 2:
            self.chosen_program = 'lama'


        try: 
            self.lama_settings["database"]
        except KeyError:
            self.lama_settings["database"] = 2

        if self.lama_settings["database"] == 0:
            refresh_ddb(self) 
 
        if self.chosen_program == "cria":
            self.beispieldaten_dateipfad_cria = self.define_beispieldaten_dateipfad(
                "cria"
            )
            self.beispieldaten_dateipfad_1 = None
            self.beispieldaten_dateipfad_2 = None
        else:
            self.beispieldaten_dateipfad_1 = self.define_beispieldaten_dateipfad(1)
            self.beispieldaten_dateipfad_2 = self.define_beispieldaten_dateipfad(2)
            self.beispieldaten_dateipfad_cria = None

        ########################
        self.MainWindow = MainWindow
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        # MainWindow.resize(900, 500)
        # MainWindow.move(30,30)
        # MainWindow.setMaximumSize(QtCore.QSize(1078, 16777215))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        # MainWindow.setStyleSheet(_fromUtf8(""))
        # MainWindow.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
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
        self.menuDateityp = QtWidgets.QMenu(self.menuBar)
        self.menuDateityp.setObjectName(_fromUtf8("menuDateityp"))
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

        self.menuBild_einbinden = QtWidgets.QMenu(self.menuBar)
        self.menuBild_einbinden.setObjectName(_fromUtf8("menuBild_einbinden"))
        MainWindow.setMenuBar(self.menuBar)
        self.actionReset = add_action(
            MainWindow, self.menuDatei, "Reset", self.suchfenster_reset
        )
        self.actionReset.setShortcut("F4")

        # self.actionReset_creator = add_action(self.menuDatei, "Reset", self.suchfenster_reset)
        # self.actionReset.setShortcut("F4")

        self.actionReset_sage = add_action(
            MainWindow, self.menuDatei, "Reset Datei", partial(self.reset_sage, True)
        )
        self.actionReset_sage.setVisible(False)

        self.actionRefresh_Database = add_action(
            MainWindow,
            self.menuDatei,
            "Datenbank aktualisieren",
            self.action_refreshddb_selected,
        )
        self.actionRefresh_Database.setShortcut("F5")

        self.actionPush_Database = add_action(
            MainWindow,
            self.menuDatei,
            "Datenbank hochladen (Entwicklermodus)",
            self.action_push_database
        )
        if self.developer_mode_active == False:
            self.actionPush_Database.setVisible(False)

        self.menuDatei.addSeparator()

        self.actionLoad = add_action(
            MainWindow, self.menuDatei, "Öffnen", self.sage_load
        )
        self.actionLoad.setShortcut("Ctrl+O")
        self.actionSave = add_action(
            MainWindow, self.menuDatei, "Speichern", self.sage_save
        )
        self.actionSave.setShortcut("Ctrl+S")

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

        self.actionExit = add_action(MainWindow, self.menuDatei, "Exit", self.close_app)

        self.actionAufgaben_Typ1 = add_action(
            MainWindow,
            self.menuDateityp,
            "Typ1 Aufgaben",
            self.chosen_aufgabenformat_typ,
        )
        self.actionAufgaben_Typ1.setShortcut("Ctrl+1")

        self.actionAufgaben_Typ2 = add_action(
            MainWindow,
            self.menuDateityp,
            "Typ2 Aufgaben",
            self.chosen_aufgabenformat_typ,
        )
        self.actionAufgaben_Typ2.setShortcut("Ctrl+2")

        self.actionSuche = add_action(
            MainWindow,
            self.menuSuche,
            "Aufgaben suchen...",
            partial(self.update_gui, "widgets_search"),
        )
        self.actionSuche.setShortcut("F1")

        self.actionSage = add_action(
            MainWindow,
            self.menuSage,
            "Neue Datei erstellen...",
            partial(self.update_gui, "widgets_sage"),
        )
        self.actionSage.setShortcut("F2")

        self.actionNeu = add_action(
            MainWindow,
            self.menuNeu,
            "Neue Aufgabe zur Datenbank hinzufügen...",
            partial(self.update_gui, "widgets_create"),
        )
        self.actionNeu.setShortcut("F3")

        self.actionBild_einbinden = add_action(
            MainWindow, self.menuBild_einbinden, "Durchsuchen...", self.add_picture
        )

        self.actionFeedback = add_action(
            MainWindow,
            self.menuFeedback,
            "Feedback oder Fehler senden...",
            partial(self.update_gui, "widgets_feedback"),
        )

        self.actionEinstellungen = add_action(
            MainWindow, self.menuOptionen, 'LaMA konfigurieren ...', self.open_setup
            )  

        self.actionUpdate_srdpmathematik = add_action(
            MainWindow, self.menuUpdate, '"srdp-mathematik.sty" aktualisieren', self.update_srdpmathematik
            )

        self.menuOptionen.addAction(self.menuUpdate.menuAction())
        self.actionInfo = add_action(
            MainWindow, self.menuHelp, "Über LaMA", self.show_info
        )
        self.actionSupport = add_action(
            MainWindow, self.menuHelp, "LaMA unterstützen", self.show_support
        )

        self.actionPUSH = add_action(
            MainWindow, self.menuOptionen, 'PUSH', self.git_push
            ) 

        self.actionPULL = add_action(
            MainWindow, self.menuOptionen, 'PULL', self.git_pull
            )

        self.actionCHECK = add_action(
            MainWindow, self.menuOptionen, 'CHANGES?', self.git_check_changes
            )   

        self.actionPULLREQUEST = add_action(
            MainWindow, self.menuOptionen, "PULLREQUEST", self.git_pull_request
        )         

        if self.developer_mode_active == True:
            label = "Entwicklermodus (aktiv)"
        else:
            label = "Entwicklermodus"
        
        self.actionDeveloper = add_action(
            MainWindow, self.menuOptionen, label, self.activate_developermode
            ) 

        self.menuBar.addAction(self.menuDatei.menuAction())
        self.menuBar.addAction(self.menuDateityp.menuAction())
        self.menuBar.addAction(self.menuSage.menuAction())
        self.menuBar.addAction(self.menuNeu.menuAction())
        self.menuBar.addAction(self.menuFeedback.menuAction())
        self.menuBar.addAction(self.menuOptionen.menuAction())

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

        self.groupBox_titelsuche = create_new_groupbox(
            self.centralwidget, "Titelsuche:"
        )
        self.groupBox_titelsuche.setSizePolicy(SizePolicy_fixed_height)

        # self.groupBox_titelsuche = QtWidgets.QGroupBox(self.centralwidget)
        # self.groupBox_titelsuche.setObjectName(_fromUtf8("groupBox_titelsuche"))

        # self.groupBox_titelsuche.setMaximumHeight(65)

        self.gridLayout_10 = create_new_gridlayout(self.groupBox_titelsuche)
        # QtWidgets.QGridLayout(self.groupBox_titelsuche)
        # self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))

        self.entry_suchbegriffe = create_new_lineedit(self.groupBox_titelsuche)
        self.gridLayout_10.addWidget(self.entry_suchbegriffe, 0, 0, 1, 1)

        self.gridLayout.addWidget(
            self.groupBox_titelsuche, 4, 1, 1, 1, QtCore.Qt.AlignTop
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
            'Es werden auch jene Aufgaben durchsucht, die sich im "Beispieleinreichung"-Ordner befinden,\njedoch bisher noch nicht auf Fehler überprüft und in die Datenbank aufgenommen wurden.'
        )
        self.cb_drafts.toggled.connect(self.cb_drafts_enabled)

        # self.gridLayout.addWidget(self.cb_show_variaton,5, 1,1,1)

        self.btn_suche = create_new_button(
            self.centralwidget, "Suche starten", partial(prepare_tex_for_pdf, self)
        )
        self.btn_suche.setShortcut(_translate("MainWindow", "Return", None))
        self.gridLayout.addWidget(self.btn_suche, 6, 1, 1, 1, QtCore.Qt.AlignRight)
        # self.horizontalLayout_2.addWidget(self.btn_suche)

        self.gridLayout.addLayout(self.horizontalLayout_2, 5, 1, 1, 1)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

        self.label_update = create_new_label(self.centralwidget, "")
        self.label_update.setMaximumHeight(18)
        self.horizontalLayout.addWidget(self.label_update)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.horizontalLayout_combobox = create_new_horizontallayout()
        # QtWidgets.QHBoxLayout()
        # self.horizontalLayout_combobox.setObjectName(
        # _fromUtf8("horizontalLayout_combobox")
        # )

        self.label_aufgabentyp = create_new_label(
            self.centralwidget, "Aufgabentyp: Typ 1"
        )
        self.horizontalLayout_combobox.addWidget(self.label_aufgabentyp)

        self.combobox_searchtype = create_new_combobox(self.centralwidget)
        self.combobox_searchtype.setMinimumContentsLength(1)

        add_new_option(
            self.combobox_searchtype,
            0,
            "Alle Dateien ausgeben, die zumindest ein Suchkriterium enthalten",
        )
        if self.chosen_program == "lama":
            label = "Alle Dateien ausgeben, die ausschließlich diese Suchkriterien enthalten"
        if self.chosen_program == "cria":
            label = "Alle Dateien ausgeben, die alle Suchkriterien enthalten"

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

            btn_alle_kapitel = create_new_button(new_scrollareacontent,"alle Kapitel der {}. Klasse auswählen".format(klasse[1]),partial(self.btn_alle_kapitel_clicked, klasse))
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
        self.gridLayout_12_cria = QtWidgets.QGridLayout(self.groupBox_ausgew_themen_cria)
        self.gridLayout_12_cria.setObjectName("gridLayout_12_cria")
        self.scrollArea_ausgew_themen_cria = QtWidgets.QScrollArea(
            self.groupBox_ausgew_themen_cria
        )
        self.scrollArea_ausgew_themen_cria.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_ausgew_themen_cria.setWidgetResizable(True)
        self.scrollArea_ausgew_themen_cria.setObjectName("scrollArea_ausgew_themen")

        self.scrollAreaWidgetContents_ausgew_themen_cria = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_ausgew_themen_cria.setGeometry(QtCore.QRect(0, 0, 320, 279))
        self.scrollAreaWidgetContents_ausgew_themen_cria.setObjectName(
            "scrollAreaWidgetContents_ausgew_themen_cria"
        )
        self.scrollArea_ausgew_themen_cria.setWidget(self.scrollAreaWidgetContents_ausgew_themen_cria)
        self.gridLayout_12_cria.addWidget(self.scrollArea_ausgew_themen_cria, 0, 0, 1, 1)
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
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_aufgabentyp)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))

        self.groupBox_variation_cr = create_new_groupbox(
            self.centralwidget, "Aufgabenvariation"
        )
        self.verticalLayout_variation = create_new_verticallayout(
            self.groupBox_variation_cr
        )

        self.button_variation_cr = create_new_button(
            self.groupBox_variation_cr,
            "Variation vorhandender Aufgabe...",
            self.button_variation_cr_pressed,
        )
        self.button_variation_cr.setMinimumWidth(0)
        self.verticalLayout_variation.addWidget(self.button_variation_cr)

        self.gridLayout.addWidget(self.groupBox_variation_cr, 0, 0, 1, 1)
        self.groupBox_variation_cr.hide()

        self.groupBox_grundkompetenzen_cr = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_grundkompetenzen_cr.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.groupBox_grundkompetenzen_cr.setMaximumSize(QtCore.QSize(350, 16777215))
        self.groupBox_grundkompetenzen_cr.setObjectName(
            _fromUtf8("groupBox_grundkompetenzen_cr")
        )
        self.groupBox_grundkompetenzen_cr.setMaximumWidth(500)
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
            new_scrollareacontent = QtWidgets.QWidget()
            new_scrollareacontent.setGeometry(QtCore.QRect(0, 0, 264, 235))
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

        self.groupBox_ausgew_gk_cr = create_new_groupbox(
            self.centralwidget, "Ausgewählte Grundkompetenzen"
        )
        self.groupBox_ausgew_gk_cr.setSizePolicy(SizePolicy_fixed_height)
        # self.groupBox_ausgew_gk_cr.setMaximumWidth(500)

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
        # self.groupBox_bilder.setMaximumWidth(500)
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

        self.label_bild_leer = QtWidgets.QLabel(self.scrollAreaWidgetContents_bilder)
        self.label_bild_leer.setObjectName(_fromUtf8("label_bild_leer"))
        self.verticalLayout.addWidget(self.label_bild_leer)
        self.label_bild_leer.setText(_translate("MainWindow", "", None))
        self.label_bild_leer.setFocusPolicy(QtCore.Qt.NoFocus)
        self.gridLayout.addWidget(self.groupBox_bilder, 7, 0, 2, 1)
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
        self.comboBox_aufgabentyp_cr.setSizePolicy(SizePolicy_fixed)
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
        self.groupBox_punkte.setSizePolicy(SizePolicy_minimum_fixed)
        # self.groupBox_punkte.setMaximumSize(80, 60)
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_punkte)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.spinBox_punkte = QtWidgets.QSpinBox(self.groupBox_punkte)
        self.spinBox_punkte.setProperty("value", 1)
        self.spinBox_punkte.setObjectName(_fromUtf8("spinBox_punkte"))
        # self.spinBox_punkte.setSizePolicy(SizePolicy_minimum_height)
        self.gridLayout_6.addWidget(self.spinBox_punkte, 0, 0, 1, 1)

        self.groupBox_punkte.setTitle(_translate("MainWindow", "Punkte", None))
        self.groupBox_punkte.hide()

        self.groupBox_aufgabenformat = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_aufgabenformat.setObjectName(_fromUtf8("groupBox_aufgabenformat"))
        self.groupBox_aufgabenformat.setSizePolicy(SizePolicy_fixed_height)
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
        # self.groupBox_klassen_cr.setMaximumSize(100, 60)
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox_klassen_cr)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.comboBox_klassen_cr = QtWidgets.QComboBox(self.groupBox_klassen_cr)
        self.comboBox_klassen_cr.setObjectName(_fromUtf8("comboBox_klassen_cr"))
        self.comboBox_klassen_cr.addItem("-")
        for all in Klassen:
            if all != "univie":
                self.comboBox_klassen_cr.addItem(Klassen[all])

        self.gridLayout_8.addWidget(self.comboBox_klassen_cr, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_klassen_cr, 0, 4, 1, 1)

        self.groupBox_klassen_cr.hide()

        self.gridLayout.setRowStretch(5, 1)

        self.groupBox_titel_cr = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_titel_cr.setObjectName(_fromUtf8("groupBox_titel_cr"))
        self.groupBox_titel_cr.setSizePolicy(SizePolicy_fixed_height)
        # self.groupBox_titel_cr.setMaximumHeight(60)
        self.gridLayout_14 = QtWidgets.QGridLayout(self.groupBox_titel_cr)
        self.gridLayout_14.setObjectName(_fromUtf8("gridLayout_14"))
        self.lineEdit_titel = QtWidgets.QLineEdit(self.groupBox_titel_cr)
        self.lineEdit_titel.setObjectName(_fromUtf8("lineEdit_titel"))
        self.gridLayout_14.addWidget(self.lineEdit_titel, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_titel_cr, 1, 1, 1, 5)
        self.groupBox_titel_cr.setTitle(_translate("MainWindow", "Titel", None))
        self.groupBox_titel_cr.hide()

        self.groupBox_beispieleingabe = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_beispieleingabe.setObjectName(
            _fromUtf8("groupBox_beispieleingabe")
        )
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
        self.gridLayout.addWidget(self.groupBox_beispieleingabe, 2, 1, 5, 5)
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
        self.groupBox_quelle.setSizePolicy(SizePolicy_fixed_height)
        self.gridLayout_18 = QtWidgets.QGridLayout(self.groupBox_quelle)
        self.gridLayout_18.setObjectName(_fromUtf8("gridLayout_18"))
        self.lineEdit_quelle = QtWidgets.QLineEdit(self.groupBox_quelle)
        self.lineEdit_quelle.setObjectName(_fromUtf8("lineEdit_quelle"))
        try:
            quelle = self.lama_settings['quelle']
        except KeyError:
            quelle = ""

        self.lineEdit_quelle.setText(quelle)
        self.gridLayout_18.addWidget(self.lineEdit_quelle, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_quelle, 7, 1, 1, 5, QtCore.Qt.AlignTop)
        self.groupBox_quelle.setTitle(
            _translate(
                "MainWindow",
                "Quelle oder Autor (Vorname Nachname) - Eingabe: VorNac",
                None,
            )
        )
        self.groupBox_quelle.hide()

        self.pushButton_save = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_save.setObjectName(_fromUtf8("pushButton_save"))
        self.pushButton_save.setFocusPolicy(QtCore.Qt.NoFocus)
        self.gridLayout.addWidget(self.pushButton_save, 8, 5, 1, 1)
        self.pushButton_save.setText(_translate("MainWindow", "Speichern", None))
        # self.pushButton_save.setShortcut(_translate("MainWindow", "Return", None))
        self.pushButton_save.hide()
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
        index = 0
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

        if self.chosen_program == "lama":
            list_comboBox_pruefungstyp.append("Quiz")

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
        ))
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
        self.scrollArea_chosen.verticalScrollBar().rangeChanged.connect(self.change_scrollbar_position)
        # self.scrollArea_chosen.verticalScrollBar().rangeChanged.connect(
        #     lambda: self.scrollArea_chosen.verticalScrollBar().setValue(
        #         self.scrollArea_chosen.verticalScrollBar().maximum()
        #     )
        # )
        self.gridLayout_5.addWidget(self.scrollArea_chosen, 5, 0, 1, 6)

        self.groupBox_notenschl = create_new_groupbox(
            self.groupBox_sage, "Notenschlüssel"
        )
        # QtWidgets.QGroupBox(self.groupBox_sage)
        # self.groupBox_notenschl.setObjectName("groupBox_notenschl")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_notenschl)
        self.gridLayout_6.setObjectName("gridLayout_6")

        self.label_sg = create_new_label(self.groupBox_notenschl, "Sehr Gut:")
        self.label_sg.setSizePolicy(SizePolicy_fixed)
        self.gridLayout_6.addWidget(self.label_sg, 0, 0, 1, 1)
        self.spinBox_2 = create_new_spinbox(self.groupBox_notenschl, 91)
        self.spinBox_2.setSizePolicy(SizePolicy_fixed)
        self.spinBox_2.valueChanged.connect(self.update_punkte)
        self.gridLayout_6.addWidget(self.spinBox_2, 0, 1, 1, 1)
        self.label_sg_pkt = create_new_label(self.groupBox_notenschl, "% (ab 0)")
        self.gridLayout_6.addWidget(self.label_sg_pkt, 0, 2, 1, 1)

        self.label_g = create_new_label(self.groupBox_notenschl, "Gut:")
        self.label_g.setSizePolicy(SizePolicy_fixed)
        self.gridLayout_6.addWidget(self.label_g, 0, 3, 1, 1)
        self.spinBox_3 = create_new_spinbox(self.groupBox_notenschl, 80)
        self.spinBox_3.setSizePolicy(SizePolicy_fixed)
        self.spinBox_3.valueChanged.connect(self.update_punkte)
        self.gridLayout_6.addWidget(self.spinBox_3, 0, 4, 1, 1)
        self.label_g_pkt = create_new_label(self.groupBox_notenschl, "% (ab 0)")
        self.gridLayout_6.addWidget(self.label_g_pkt, 0, 5, 1, 1)

        self.label_b = create_new_label(self.groupBox_notenschl, "Befriedigend:")
        self.label_b.setSizePolicy(SizePolicy_fixed)
        self.gridLayout_6.addWidget(self.label_b, 1, 0, 1, 1)
        self.spinBox_4 = create_new_spinbox(self.groupBox_notenschl, 64)
        self.spinBox_4.setSizePolicy(SizePolicy_fixed)
        self.spinBox_4.valueChanged.connect(self.update_punkte)
        self.gridLayout_6.addWidget(self.spinBox_4, 1, 1, 1, 1)
        self.label_b_pkt = create_new_label(self.groupBox_notenschl, "% (ab 0)")
        self.gridLayout_6.addWidget(self.label_b_pkt, 1, 2, 1, 1)

        self.label_g_2 = create_new_label(self.groupBox_notenschl, "Genügend:")
        self.label_g_2.setSizePolicy(SizePolicy_fixed)
        self.gridLayout_6.addWidget(self.label_g_2, 1, 3, 1, 1)
        self.spinBox_5 = create_new_spinbox(self.groupBox_notenschl, 50)
        self.spinBox_5.setSizePolicy(SizePolicy_fixed)
        self.spinBox_5.valueChanged.connect(self.update_punkte)
        self.gridLayout_6.addWidget(self.spinBox_5, 1, 4, 1, 1)
        self.label_g_2_pkt = create_new_label(self.groupBox_notenschl, "% (ab 0)")
        self.gridLayout_6.addWidget(self.label_g_2_pkt, 1, 5, 1, 1)

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

        self.gridLayout.addWidget(self.groupBox_alle_aufgaben_fb, 0, 0, 6, 1)
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
        self.groupBox_alle_aufgaben_fb_cria.setMinimumWidth(100)
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

        i = 0
        for all in list_klassen:

            self.comboBox_klassen_fb_cria.addItem("")

            self.comboBox_klassen_fb_cria.setItemText(
                i, _translate("MainWindow", all[1] + ". Klasse", None),
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
        self.gridLayout.addWidget(self.groupBox_alle_aufgaben_fb_cria, 1, 0, 5, 1)
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
        self.gridLayout.addWidget(self.groupBox_email, 4, 1, 1, 1)
        self.groupBox_email.hide()

        self.pushButton_send = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_send.setObjectName(_fromUtf8("pushButton_send"))
        self.gridLayout.addWidget(
            self.pushButton_send, 5, 1, 1, 1, QtCore.Qt.AlignRight
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
            self.sage_load(True)

        ############################################################################################
        ##############################################################################################

    def retranslateUi(self, MainWindow):
        self.menuDateityp.setTitle(_translate("MainWindow", "Aufgabentyp", None))
        self.menuDatei.setTitle(_translate("MainWindow", "Datei", None))
        self.menuNeu.setTitle(_translate("MainWindow", "Aufgabe hinzufügen", None))
        self.menuSage.setTitle(_translate("MainWindow", "Erstellen", None))
        self.menuSuche.setTitle(_translate("MainWindow", "Aufgabensuche", None))
        self.menuBild_einbinden.setTitle(
            _translate("MainWindow", "Bild einfügen", None)
        )
        self.menuFeedback.setTitle(_translate("MainWindow", "Feedback && Fehler", None))

        self.menuHelp.setTitle(_translate("MainWindow", "?", None))

        self.groupBox_titelsuche.setTitle(_translate("MainWindow", "Titelsuche:", None))
        self.groupBox_klassen.setTitle(_translate("MainWindow", "Suchfilter", None))

        # self.cb_solution.setText(_translate("MainWindow", "Lösungen anzeigen", None))
        # self.cb_drafts.setText(_translate("MainWindow", "Entwürfe anzeigen", None))

        try:
            if self.chosen_program == "lama":
                log_file = os.path.join(path_localappdata_lama, "Teildokument","log_file_1")
            if self.chosen_program == "cria":
                log_file = os.path.join(path_localappdata_lama, "Teildokument","log_file_cria")
            self.label_update.setText(
                _translate(
                    "MainWindow",
                    "Letztes Update: "
                    + modification_date(log_file).strftime("%d.%m.%y - %H:%M"),
                    None,
                )
            )
        except FileNotFoundError:
            self.label_update.setText(
                _translate("MainWindow", "Letztes Update: ---", None)
            )

        self.combobox_searchtype.setItemText(
            0,
            _translate(
                "MainWindow",
                "Alle Dateien ausgeben, die zumindest ein Suchkriterium enthalten",
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

    def open_dialogwindow_erstellen(
        self, dict_titlepage,
    ):  # , dict_gesammeltedateien
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
        )
        rsp = self.Dialog.exec_()

        if rsp == QtWidgets.QDialog.Accepted:
            for index in range(self.ui_erstellen.spinBox_sw_gruppen.value() * 2):
                self.pushButton_vorschau_pressed(
                    "schularbeit",
                    index,
                    self.ui_erstellen.spinBox_sw_gruppen.value() * 2,
                    self.ui_erstellen.pdf,
                    self.ui_erstellen.lama,
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
            # background_color = get_color(blue_7)
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
        for i in range(5):
            try:
                version_path = os.path.join(
                    path_programm, "_database", "_config", "update"
                )
                version_file = os.path.join(version_path, "__version__.txt")
                f = open(version_file, "r")
                break
            except FileNotFoundError:
                input(
                    "Please place your config file in '{}' and hit enter. {} tries left!".format(
                        version_path, 5 - i
                    )
                )
            if i == 4:
                print("No version set. Skipping version check!")
                return False

        update_check = []
        update_check.append(f.read().replace(" ", "").replace("\n", ""))
        f.close()
        update_check.append(__version__)

        if update_check[0] != update_check[1]:
            if sys.platform.startswith("linux"):
                information_window(
                    "Es ist ein neues Update verfügbar.",
                    "Es wird empfohlen die neueste Version von LaMA unter lama.schule/downloads herunterzuladen und damit die alte Version zu ersetzen.",
                    titel="Neue Version verfügbar",
                )
            else:
                ret = question_window(
                    "Es ist eine neue Version von LaMA verfügbar.",
                    "Möchten Sie das neue Update jetzt installieren?",
                    "Neue Version verfügbar",
                )
                # msg = QtWidgets.QMessageBox()
                # msg.setIcon(QtWidgets.QMessageBox.Question)
                # msg.setWindowIcon(QtGui.QIcon(logo_path))
                # msg.setText("Es ist eine neue Version von LaMA verfügbar.")
                # msg.setInformativeText("Möchten Sie das neue Update installieren?")
                # msg.setWindowTitle("Neue Version verfügbar")
                # msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                # buttonY = msg.button(QtWidgets.QMessageBox.Yes)
                # buttonY.setText("Ja")
                # buttonN = msg.button(QtWidgets.QMessageBox.No)
                # buttonN.setText("Nein")
                # ret = msg.exec_()

                if ret == True:
                    opened_file = os.path.basename(sys.argv[0])
                    name, extension = os.path.splitext(opened_file)
                    if sys.platform.startswith("darwin"):
                        system_folder = "update_mac"
                    # elif sys.platform.startswith("linux"):
                    #     system_folder="update_linux"
                    else:
                        system_folder = "update_windows"
                    filename_update = os.path.join(
                        path_programm,
                        "_database",
                        "_config",
                        "update",
                        system_folder,
                        "update%s" % extension,
                    )

                    try:
                        if sys.platform.startswith("linux") or sys.platform.startswith(
                            "darwin"
                        ):
                            if extension == ".py":
                                os.system("python3 {}".format(filename_update))
                            else:
                                os.system("chmod 777 {}".format(filename_update))
                                os.system(filename_update)
                        else:
                            os.startfile(filename_update)
                        sys.exit(0)
                    except Exception as e:
                        warning_window(
                            'Das neue Update von LaMA konnte leider nicht installiert werden! Bitte versuchen Sie es später erneut oder melden Sie den Fehler unter dem Abschnitt "Feedback & Fehler".',
                            'Fehler:\n"{}"'.format(e),
                        )

    def create_Tooltip(self, chosen_dict):
        for all in chosen_dict:
            name = "checkbox_search_gk_" + all
            self.dict_widget_variables[name].setToolTip(chosen_dict[all])
        for all in chosen_dict:
            name = "checkbox_creator_gk_" + all
            self.dict_widget_variables[name].setToolTip(chosen_dict[all])

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
                        dict_unterkapitel[unterkapitel] + " ("+unterkapitel + ")",
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

        # self.button_check_all_unterkapitel = create_new_button(self.scrollAreaWidgetContents_cria, 'alle auswählen',None)
        # self.button_check_all_unterkapitel.setStyleSheet("background-color: rgb(240, 240, 240);")
        # self.verticalLayout_4_cria.addWidget(self.button_check_all_unterkapitel, 0, QtCore.Qt.AlignLeft)
        # self.button_check_all_unterkapitel.hide()

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

        self.delete_all_widgets(layout, 1)

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
                layout.insertWidget(layout.count() - 1, checkbox)
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

    def suchfenster_reset(self, variation=False):

        global dict_picture_path

        self.uncheck_all_checkboxes("gk")

        self.uncheck_all_checkboxes("themen")

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
        self.comboBox_af.setCurrentIndex(0)
        self.comboBox_klassen_cr.setCurrentIndex(0)
        self.label_ausgew_gk_creator.setText(_translate("MainWindow", "", None))
        self.label_bild_leer.show()

        self.chosen_variation = None
        self.reset_variation()

        for picture in list(self.dict_widget_variables.keys())[:]:
            if picture.startswith("label_bild_creator_"):
                self.del_picture(picture)

        if self.lineEdit_titel.text().startswith("###"):
            self.lineEdit_titel.setText(_translate("MainWindow", "###", None))
        else:
            self.lineEdit_titel.setText(_translate("MainWindow", "", None))
        try:
            quelle = self.lama_settings['quelle']
        except KeyError:
            quelle = ""
        self.lineEdit_quelle.setText(_translate("MainWindow", quelle, None))

        if variation == False:
            self.plainTextEdit.setPlainText(_translate("MainWindow", "", None))

    def reset_sage(self, question_reset=True):
        if question_reset == True and not is_empty(self.list_alle_aufgaben_sage):
            response = question_window(
                "Sind Sie sicher, dass Sie das Fenster zurücksetzen wollen und die erstellte Datei löschen möchten?",
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
                "copy_images": [],
            },
        }

        self.list_alle_aufgaben_sage = []
        self.dict_alle_aufgaben_sage = {}
        self.dict_variablen_label = {}
        self.dict_variablen_punkte = {}
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

        if self.chosen_program == "lama":
            self.chosen_program = "cria"

            if self.beispieldaten_dateipfad_cria == None:
                self.beispieldaten_dateipfad_cria = self.define_beispieldaten_dateipfad(
                    "cria"
                )

            self.gridLayout.addWidget(self.groupBox_af, 3, 0, 1, 1)
            self.gridLayout.addWidget(self.groupBox_punkte, 0, 1, 1, 1)
            self.gridLayout.addWidget(self.groupBox_aufgabenformat, 0, 2, 1, 1)
            self.actionProgram.setText(
                _translate("MainWindow", 'Zu "LaMA (Oberstufe)" wechseln', None)
            )
            self.comboBox_pruefungstyp.removeItem(6)  # delete Quiz
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
                    "Alle Dateien ausgeben, die alle Suchkriterien enthalten",
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
            self.beispieldaten_dateipfad_cria = self.define_beispieldaten_dateipfad(
                "cria"
            )

        elif self.chosen_program == "cria":
            self.chosen_program = "lama"

            if (
                self.beispieldaten_dateipfad_1 == None
                or self.beispieldaten_dateipfad_2 == None
            ):
                self.beispieldaten_dateipfad_1 = self.define_beispieldaten_dateipfad(1)
                self.beispieldaten_dateipfad_2 = self.define_beispieldaten_dateipfad(2)

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
                    "Alle Dateien ausgeben, die ausschließlich diese Suchkriterien enthalten",
                    None,
                ),
            )

            # self.comboBox_at_fb.setItemText(0, _translate("MainWindow", "Typ 1", None))
            # self.comboBox_at_fb.setItemText(1, _translate("MainWindow", "Typ 2", None))
            # # self.comboBox_at_fb.addItem("")
            # self.comboBox_at_fb.setItemText(2, _translate("MainWindow", "Allgemeine Rückmeldung", None))
            self.comboBox_pruefungstyp.addItem("Quiz")
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

        MainWindow.setWindowTitle(program_name)
        MainWindow.setWindowIcon(QtGui.QIcon(icon))
        if self.lama_settings["database"]==0:
            refresh_ddb(self)
        self.update_gui("widgets_search")
        self.beispieldaten_dateipfad_1 = self.define_beispieldaten_dateipfad(1)
        self.beispieldaten_dateipfad_2 = self.define_beispieldaten_dateipfad(2)

    def close_app(self):
        if self.list_alle_aufgaben_sage == []:
            sys.exit(0)

        else:
            try:
                if os.path.isfile(self.saved_file_path) == True:
                    path = self.saved_file_path
                    loaded_file = self.load_file(path)
                    if loaded_file == self.dict_all_infos_for_file:
                        sys.exit(0)
            except AttributeError:
                pass

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
            self.actionPush_Database.setVisible(False)

        elif self.developer_mode_active == True:
            self.actionDeveloper.setText("Entwicklermodus (aktiv)")
            self.actionPush_Database.setVisible(True)

    def activate_developermode(self):
        if self.developer_mode_active == True:
            response = question_window("Sind Sie sicher, dass Sie den Entwicklermodus deaktivieren möchten?")
            if response == False:
                return
            path_lama_developer_credentials = os.path.join(os.getenv('LOCALAPPDATA'), "LaMA", "credentials")
            lama_developer_credentials = os.path.join(path_lama_developer_credentials, "developer_credentials.txt")
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


    def git_pull(self):
        # QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        path_programdata = os.getenv('PROGRAMDATA')
        database = os.path.join(path_programdata, "LaMA", "_database")
        repo = git.Repo(database)
        print('pull')
        # repo.git.add(A=True)
        # repo.git.fetch('--all')
        # 
        repo.git.reset('--hard')
        repo.git.clean('-xdf')
        o = repo.remotes.origin        
        o.pull()
        print('done')
        # QtWidgets.QApplication.restoreOverrideCursor()

    def git_push(self):
        # QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        path_programdata = os.getenv('PROGRAMDATA')
        database = os.path.join(path_programdata, "LaMA", "_database")
        repo = git.Repo(database)
        print('push')
        repo.git.add(A=True)
        repo.index.commit('new commit')
        o = repo.remotes.origin
        o.push()
        print('done')
        # QtWidgets.QApplication.restoreOverrideCursor()

    def git_check_changes(self):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        path_programdata = os.getenv('PROGRAMDATA')
        database = os.path.join(path_programdata, "LaMA", "_database")
        repo = git.Repo(database)
        # QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        if repo.is_dirty(untracked_files=True):
            print('changes detected')
        else:
            print('no changes found')
        QtWidgets.QApplication.restoreOverrideCursor()        

    def git_pull_request(self):
        # QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        path_programdata = os.getenv('PROGRAMDATA')
        database = os.path.join(path_programdata, "LaMA", "_database")
        repo = git.Repo(database) 

        repo.create_pull(title='Test')      

    def show_info(self):
        QtWidgets.QApplication.restoreOverrideCursor()

        custom_window(
            "LaMA - LaTeX Mathematik Assistent %s  \n\n"
            "Authors: Christoph Weberndorfer, Matthias Konzett\n\n"
            "License: GNU General Public License v3.0  \n\n" % __version__,
            "Credits: David Fischer\n"
            "Logo & Icon: Lisa Schultz\n\n"
            "E-Mail-Adresse: lama.helpme@gmail.com\n"
            "Weiter Infos: lama.schule",
            titel="Über LaMA - LaTeX Mathematik Assistent",
        )

    def update_srdpmathematik(self):
        response = question_window('Sind Sie sicher, dass Sie das Paket "srdp-mathematik.sty" aktualisieren möchten?')
        
        if response==False:
            return
        
        ### get version from webpage
        # uf = urllib.request.urlopen("https://chrisiweb.github.io/lama_latest_update/")
        # html = uf.read()
        # print(html)
        # text = re.search("Version: \[(.*)\]",str(html))

        # print(text)
        # version = text.group(1)
        # print(version)

        # print(path_programm)
        path_home=Path.home()
        path_new_package = os.path.join(path_programm, "_database", "_config", "srdp-mathematik.sty")
        if os.path.isfile(path_new_package)==False:
            warning_window("Das neue srdp-mathematik-Paket konnte nicht gefunden werden. Bitte versuchen Sie es später erneut.")
            return

        # print(path_home)
        # mac_path = os.path.join(path_home, "Library","texmf","tex","latex","srdp-mathematik.sty")
        # print(mac_path)
        # print(os.path.isfile(mac_path))

        if sys.platform.startswith("darwin") or sys.platform.startswith("linux"):
            possible_locations = [
                os.path.join(path_home, "Library","texmf")
            ]
        else:
            possible_locations = [
                os.path.join("c:\\","Program Files","MiKTeX 2.9"),
                os.path.join("c:\\","Program Files (x86)","MiKTeX 2.9"),
                os.path.join(path_home, "AppData", "Roaming", "MiKTeX")
                # os.path.join(
                # "C:\Users\Christoph\AppData\Roaming\MiKTeX\2.9\tex\latex\srdp-mathematik\srdp-mathematik.sty
            ]

        update_successfull=False
        for path in possible_locations:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file == "srdp-mathematik.sty":
                        path_file = os.path.join(root, file)
                        try:
                            shutil.copy2(path_new_package, path_file)
                        except PermissionError:
                            warning_window("Das Update konnte leider nicht durchgeführt werden, da notwendige Berechtigungen fehlen. Starten Sie LaMA erneut als Administrator (Rechtsklick -> 'Als Administrator ausführen') und versuchen Sie es erneut.")
                            return
                        update_successfull=True

        if update_successfull == False:
            critical_window("Das Update konnte leider nicht durchgeführt werden. Aktualisieren Sie das Paket manuell oder wenden Sie sich an lama.helpme@gmail.com für Unterstützung.")
            return
        if update_successfull == True:
            information_window("Das Paket wurde erfolgreich aktualisiert.")
            return

    def show_support(self):
        QtWidgets.QApplication.restoreOverrideCursor()

        custom_window(
            "LaMA ist gratis und soll es auch bleiben!\n",
            "Wir freuen uns dennoch sehr über eine Unterstützung für die Weiterentwicklung von LaMA.\n\n"
            """ 
            Name: Matthias Konzett
            IBAN: AT57 1921 0200 9941 7002
            BLZ: 19210 
            """,
            titel="LaMA unterstützen",
        )

        # msg = QtWidgets.QMessageBox()

        # pixmap = QtGui.QPixmap(logo_path)

        # msg.setIconPixmap(pixmap.scaled(110, 110, QtCore.Qt.KeepAspectRatio))
        # msg.setWindowIcon(QtGui.QIcon(logo_path))
        # msg.setText(
        #     "LaMA - LaTeX Mathematik Assistent %s  \n\n"
        #     "Authors: Christoph Weberndorfer, Matthias Konzett\n\n"
        #     "License: GNU General Public License v3.0  \n\n"
        #     "Credits: David Fischer	" % __version__
        # )
        # msg.setInformativeText("Logo & Icon: Lisa Schultz")
        # msg.setWindowTitle("Über LaMA - LaTeX Mathematik Assistent")
        # # msg.setDetailedText("The details are as follows:")
        # msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        # msg.exec_()

    def refresh_label_update(self):
        try:
            if self.chosen_program == "cria":
                log_file = "log_file_cria"
            else:
                log_file = "log_file_%s" % self.label_aufgabentyp.text()[-1]
            path_log_file = os.path.join(path_localappdata_lama, "Teildokument",log_file)
            self.label_update.setText(
                _translate(
                    "MainWindow",
                    "Letztes Update: "
                    + modification_date(path_log_file).strftime("%d.%m.%y - %H:%M"),
                    None,
                )
            )
        except FileNotFoundError:
            self.label_update.setText(
                _translate("MainWindow", "Letztes Update: ---", None)
            )

    def chosen_aufgabenformat_typ(self):
        chosen_type = self.label_aufgabentyp.text()[-1]
        if chosen_type == str(2):
            self.label_aufgabentyp.setText(
                _translate("MainWindow", "Aufgabentyp: Typ 1", None)
            )
            self.groupBox_af.show()
            self.combobox_searchtype.hide()
            self.refresh_label_update()
        elif chosen_type == str(1):
            self.label_aufgabentyp.setText(
                _translate("MainWindow", "Aufgabentyp: Typ 2", None)
            )
            self.groupBox_af.hide()
            self.combobox_searchtype.show()
            self.refresh_label_update()

    # def chosen_aufgabenformat_typ2(self):
    #     self.label_aufgabentyp.setText(
    #         _translate("MainWindow", "Aufgabentyp: Typ 2", None)
    #     )
    #     self.groupBox_af.hide()
    #     self.combobox_searchtype.show()
    #     self.refresh_label_update()

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
        if (
            self.comboBox_pruefungstyp.currentText() == "Grundkompetenzcheck"
            or self.comboBox_pruefungstyp.currentText() == "Übungsblatt"
            or self.comboBox_pruefungstyp.currentText() == "Quiz"
        ):
            self.combobox_beurteilung.setEnabled(False)
            self.groupBox_notenschl.setEnabled(False)
            self.groupBox_beurteilungsraster.setEnabled(False)
            self.spinBox_nummer.setValue(0)
            if self.comboBox_pruefungstyp.currentText() == "Quiz":
                self.pushButton_titlepage.setEnabled(True)
                self.pushButton_titlepage.setText("Zufälliges Quiz erstellen")
                self.comboBox_at_sage.setCurrentIndex(0)
                self.comboBox_at_sage.setEnabled(False)
                if self.get_aufgabenverteilung()[1] != 0:
                    response = question_window(
                        "Das Quiz ist ausschließlich für Typ1-Aufgaben konzipiert. Sollen alle enthaltenen Typ2-Aufgaben entfernt und das Quiz erstellt werden?",
                        titel="Typ2 Aufgaben entfernen?",
                    )
                    if response == False:
                        self.comboBox_pruefungstyp.setCurrentIndex(0)
                        return
                    else:
                        for aufgabe in self.list_alle_aufgaben_sage[:]:
                            typ = self.get_aufgabentyp(aufgabe)
                            if typ == 2:
                                self.btn_delete_pressed(aufgabe)

            else:
                self.pushButton_titlepage.setEnabled(False)
                self.comboBox_at_sage.setEnabled(True)
                self.pushButton_titlepage.setText("Titelblatt anpassen")
        else:
            self.combobox_beurteilung.setEnabled(True)
            self.groupBox_notenschl.setEnabled(True)
            self.groupBox_beurteilungsraster.setEnabled(True)
            self.pushButton_titlepage.setEnabled(True)
            self.comboBox_at_sage.setEnabled(True)
            self.spinBox_nummer.setValue(1)
            self.pushButton_titlepage.setText("Titelblatt anpassen")
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

    # def comboBox_aufgabentyp_cr_changed(self):
    #     if self.comboBox_aufgabentyp_cr.currentIndex() == 0:
    #         self.spinBox_punkte.setValue(1)
    #     elif self.comboBox_aufgabentyp_cr.currentIndex() == 1:
    #         self.spinBox_punkte.setValue(0)

    def add_drafts_to_beispieldaten(self):
        drafts_path = os.path.join(path_programm, "Beispieleinreichung")
        beispieldaten_dateipfad_draft = search_files(drafts_path)
        for section in beispieldaten_dateipfad_draft.keys():
            path = beispieldaten_dateipfad_draft[section]
            aufgabentyp = self.get_aufgabentyp_from_path(path)
            if self.chosen_program == "lama":
                if aufgabentyp == 1:
                    self.beispieldaten_dateipfad_1[section] = path
                elif aufgabentyp == 2:
                    self.beispieldaten_dateipfad_2[section] = path
            elif self.chosen_program == "cria" and aufgabentyp == None:
                self.beispieldaten_dateipfad_cria[section] = path

    def delete_drafts_from_beispieldaten(self):
        drafts_path = os.path.join(path_programm, "Beispieleinreichung")
        beispieldaten_dateipfad_draft = search_files(drafts_path)
        for section in beispieldaten_dateipfad_draft.keys():
            path = beispieldaten_dateipfad_draft[section]
            aufgabentyp = self.get_aufgabentyp_from_path(path)
            if self.chosen_program == "lama":
                if section in self.beispieldaten_dateipfad_1:
                    del self.beispieldaten_dateipfad_1[section]
                elif section in self.beispieldaten_dateipfad_2:
                    del self.beispieldaten_dateipfad_2[section]
            elif (
                self.chosen_program == "cria"
                and section in self.beispieldaten_dateipfad_cria
            ):
                del self.beispieldaten_dateipfad_cria[section]

    def cb_drafts_sage_enabled(self):
        if self.cb_drafts_sage.isChecked() == True:
            warning_window(
                "Entwürfe können Fehler enthalten, die das Programm zum Absturz bringen.",
                "Speichern Sie gegebenenfalls eine erstellte Datei vor der Suche!",
                titel="Warnung - Here be dragons!",
            )

            self.add_drafts_to_beispieldaten()

        if self.cb_drafts_sage.isChecked() == False:
            self.delete_drafts_from_beispieldaten()

        self.adapt_choosing_list("sage")

    ############# def prepare_tex_for_pdf #################

    #################################################################
    ###############################################################
    ################### Befehle Creator ###########################
    #############################################################

    def collect_data_aufgabe(self, aufgabe):
        content = collect_content(self, aufgabe)

        section = get_section_from_content(content)

        if section == None:
            warning_window(
                'Die gewählte Aufgabe {} ist fehlerhaft.\nBitte melden Sie diese unter "Feedback & Fehler".\nVielen Dank!'.format(
                    aufgabe
                )
            )
            return

        list_collected_data = re.split("{| - |}", section)[1:-1]

        dict_collected_data = {}

        dict_collected_data["aufgabe"] = aufgabe

        dict_collected_data["klasse"] = None
        for all in list_collected_data:
            if re.match("K[0-9]", all) or all == "MAT":
                dict_collected_data["klasse"] = all
        typ = self.get_aufgabentyp(aufgabe)
        info = self.collect_all_infos_aufgabe(aufgabe)

        if typ == None:
            themen = list_collected_data[1].split(", ")
            dict_collected_data["thema"] = themen
        elif typ == 1:
            dict_collected_data["thema"] = [list_collected_data[0]]
        elif typ == 2:
            gks = list_collected_data[-3].split(", ")
            dict_collected_data["thema"] = gks
            # dict_collected_data['titel']=  list_collected_data[-]

        dict_collected_data["titel"] = info[2]

        if isinstance(info[3], int):
            dict_collected_data["aufgabenformat"] = None
        else:
            dict_collected_data["aufgabenformat"] = info[3]
        dict_collected_data["quelle"] = list_collected_data[-1]

        return dict_collected_data

    def set_infos_chosen_variation(self, dict_collected_data):
        aufgabe = dict_collected_data["aufgabe"]
        typ = self.get_aufgabentyp(aufgabe)

        if self.chosen_program == "lama":
            list_comboBox_gk = ["AG", "FA", "AN", "WS", "Zusatzthemen"]

            if typ == 1:
                gk, nummer = aufgabe.split(" - ")
                short_gk = shorten_gk(gk)
                if short_gk in zusatzthemen_beschreibung:
                    checkbox_gk = "checkbox_creator_themen_{}".format(short_gk)
                    index = list_comboBox_gk.index("Zusatzthemen")
                else:
                    checkbox_gk = "checkbox_creator_gk_{}".format(short_gk)
                    index = list_comboBox_gk.index(gk.split(" ")[0].replace("-L",""))

                self.dict_widget_variables[checkbox_gk].setChecked(True)
                self.tab_widget_gk_cr.setCurrentIndex(index)

            elif typ == 2:
                for i, gk in enumerate(dict_collected_data["thema"]):
                    short_gk = shorten_gk(gk)
                    if short_gk in zusatzthemen_beschreibung:
                        checkbox_gk = "checkbox_creator_themen_{}".format(short_gk)
                        if i == 0:
                            index = list_comboBox_gk.index("Zusatzthemen")
                    else:                   
                        checkbox_gk = "checkbox_creator_gk_{}".format(short_gk)
                        if i == 0:
                            index = list_comboBox_gk.index(gk.split(" ")[0].replace("-L",""))
                        # index = list_comboBox_gk.index(gk.split(" ")[0].replace("-L",""))

                    self.dict_widget_variables[checkbox_gk].setChecked(True)
                self.tab_widget_gk_cr.setCurrentIndex(index)
                # self.tab_widget_gk_cr.setCurrentIndex(
                #     list_comboBox_gk.index(
                #         dict_collected_data["thema"][0].split(" ")[0]
                #     )
                # )

            self.groupBox_grundkompetenzen_cr.setEnabled(False)

            self.comboBox_aufgabentyp_cr.setCurrentIndex(typ - 1)
            self.groupBox_aufgabentyp.setEnabled(False)

        elif self.chosen_program == "cria":
            klasse = dict_collected_data["klasse"].lower()
            index = list_klassen.index(klasse)
            self.tab_widget_cr_cria.setCurrentIndex(index)

            for thema in dict_collected_data["thema"]:
                kapitel, unterkapitel = thema.split(".")

                combobox_thema = "combobox_kapitel_creator_cria_{}".format(klasse)
                dict_klasse_name = eval("dict_{}_name".format(klasse))
                thema_name = dict_klasse_name[kapitel]
                index = self.dict_widget_variables[combobox_thema].findText(
                    thema_name + " (" + kapitel + ")"
                )
                self.dict_widget_variables[combobox_thema].setCurrentIndex(index)

                checkbox_thema = "checkbox_unterkapitel_creator_{0}_{1}_{2}".format(
                    klasse, kapitel, unterkapitel
                )
                self.dict_widget_variables[checkbox_thema].setChecked(True)

                self.groupBox_themengebiete_cria.setEnabled(False)

        punkte = self.get_punkte_aufgabe(aufgabe)

        self.spinBox_punkte.setValue(punkte)
        if dict_collected_data["aufgabenformat"] != None:
            try:
                full_aufgabenformat = dict_aufgabenformate[
                    dict_collected_data["aufgabenformat"].lower()
                ]
                index = self.comboBox_af.findText(full_aufgabenformat)
                self.comboBox_af.setEnabled(False)
            except AttributeError:
                warning_window(
                    'Die gewählte Aufgabe {} ist fehlerhaft.\nBitte melden Sie diese unter "Feedback & Fehler".\nVielen Dank!'.format(
                        aufgabe
                    )
                )
                index = 0
            self.comboBox_af.setCurrentIndex(index)
        else:
            self.comboBox_af.setCurrentIndex(0)

        if dict_collected_data["klasse"] != None and typ != None:
            try:
                full_klasse = Klassen[dict_collected_data["klasse"].lower()]
                index = self.comboBox_klassen_cr.findText(full_klasse)
            except AttributeError:
                warning_window(
                    'Die gewählte Aufgabe {} ist fehlerhaft.\nBitte melden Sie diese unter "Feedback & Fehler".\nVielen Dank!'.format(
                        aufgabe
                    )
                )
                index = 0
            self.comboBox_klassen_cr.setCurrentIndex(index)
        else:
            self.comboBox_klassen_cr.setCurrentIndex(0)

        if self.lineEdit_titel.text().startswith("###"):
            self.lineEdit_titel.setText("### " + dict_collected_data["titel"])
        else:
            self.lineEdit_titel.setText(dict_collected_data["titel"])
        # self.lineEdit_quelle.setText(dict_collected_data["quelle"])

    def reset_variation(self):
        self.button_variation_cr.setText("Variation vorhandender Aufgabe...")
        self.groupBox_grundkompetenzen_cr.setEnabled(True)
        self.groupBox_aufgabentyp.setEnabled(True)
        self.comboBox_af.setEnabled(True)
        self.groupBox_themengebiete_cria.setEnabled(True)

    def button_variation_cr_pressed(self):
        Dialog = QtWidgets.QDialog(
            None,
            QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint,
        )
        ui = Ui_Dialog_variation()
        ui.setupUi(Dialog, self)
        # self.Dialog.show()
        response = Dialog.exec()

        if response == 1:
            self.suchfenster_reset(True)
            self.chosen_variation = ui.chosen_variation
            if self.chosen_variation != None:
                self.button_variation_cr.setText(
                    "Variation von: {}".format(self.chosen_variation.upper())
                )
                dict_collected_data = self.collect_data_aufgabe(self.chosen_variation)
            else:
                self.suchfenster_reset(True)
                self.reset_variation()
                return

        if response == 0:
            return

        self.set_infos_chosen_variation(dict_collected_data)


    def add_picture(self):
        try:
            self.saved_file_path
        except AttributeError:
            self.saved_file_path = path_programm
        list_filename = QtWidgets.QFileDialog.getOpenFileNames(
            None, "Grafiken wählen", self.saved_file_path, "Grafiken (*.eps)"
        )
        if list_filename[0] == []:
            return
        self.saved_file_path = os.path.dirname(list_filename[0][0])

        i = len(dict_picture_path)

        self.label_bild_leer.hide()
        for all in list_filename[0]:
            head, tail = os.path.split(all)

            if tail in dict_picture_path.keys():
                pass
            else:
                head, tail = os.path.split(all)
                dict_picture_path[tail] = all
                label_picture = create_new_label(
                    self.scrollAreaWidgetContents_bilder, tail, False, True
                )
                label_picture_name = "label_bild_creator_{}".format(tail)
                self.dict_widget_variables[label_picture_name] = label_picture
                label_picture.clicked.connect(
                    partial(self.del_picture, label_picture_name)
                )
                self.verticalLayout.addWidget(label_picture)

    def del_picture(self, picture):
        del dict_picture_path[self.dict_widget_variables[picture].text()]
        self.dict_widget_variables[picture].hide()
        if len(dict_picture_path) == 0:
            self.label_bild_leer.show()

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
                self.saved_file_path = path_programm

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
            # self.label_keine_auswahl.hide()
            # self.comboBox_af.show()
            self.comboBox_af.removeItem(0)
        if self.comboBox_aufgabentyp_cr.currentText() == "Typ 2":
            self.comboBox_af.insertItem(0, "keine Auswahl nötig")
            self.comboBox_af.setCurrentIndex(0)
            self.groupBox_aufgabenformat.setEnabled(False)
            # self.label_keine_auswahl.show()
            # self.comboBox_af.hide()

    def get_number_of_included_images(self):
        num = self.plainTextEdit.toPlainText().count("\includegraphics")
        return num

    def check_included_attached_image_ratio(self):
        included = self.get_number_of_included_images()
        attached = len(dict_picture_path)
        return included, attached

    def check_entry_creator(self):
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

        if is_empty(self.lineEdit_titel.text().replace("###","")) == True or self.lineEdit_titel.text().replace("###","").isspace():
            return "Bitte geben Sie einen Titel ein."

        if is_empty(self.plainTextEdit.toPlainText()) == True:
            return 'Bitte geben Sie den LaTeX-Quelltext der Aufgabe im Bereich "Aufgabeneingabe" ein.'

        if is_empty(self.lineEdit_quelle.text()) == True:
            return "Bitte geben Sie die Quelle an."

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
        if dict_picture_path != {}:
            bilder = ", ".join(dict_picture_path)
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

    def open_dialogwindow_save(self, information):
        Dialog_speichern = QtWidgets.QDialog(
            None,
            QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint,
        )
        self.ui_save = Ui_Dialog_speichern()
        self.ui_save.setupUi(Dialog_speichern, self.creator_mode, self.chosen_variation)
        self.ui_save.label.setText(information)
        # self.ui_save.label.setStyleSheet("padding: 10px")
        return Dialog_speichern

    def get_highest_grade(self):
        highest_grade = 1
        for all in self.list_selected_topics_creator:
            if int(all[0][1]) > int(highest_grade):
                highest_grade = all[0][1]
        klasse = "k{}".format(highest_grade)
        return klasse

    # def split_thema_klasse(self, thema):
    #     if re.search("\(.\.\)", thema) != None:
    #         thema, klasse = thema.split("(")
    #         thema = thema.lower().strip()
    #         klasse = klasse.strip(".)")

    #         return thema, klasse
    #     return None, None

    def create_path_from_list(self, list_):
        path = ""
        for all in list_:
            path = os.path.join(path, all)

        return path

    def get_parent_folder(self, typ_save):
        list_path = [path_programm]

        if self.local_save == True:
            list_path.append("Lokaler_Ordner")
        else:
            if typ_save == ["admin", 1]:
                list_path.append("_database_inoffiziell")
            else:
                list_path.append("_database")
        return list_path

    def create_aufgabenpfad(self, typ_save):
        list_path = self.get_parent_folder(typ_save)

        ####
        if self.chosen_program == "lama":
            if self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
                list_path.append("Typ1Aufgaben")
            if self.comboBox_aufgabentyp_cr.currentText() == "Typ 2":
                list_path.append("Typ2Aufgaben")
        elif self.chosen_program == "cria":
            highest_grade = self.get_highest_grade()
            list_path.append(highest_grade)

        #####

        if self.chosen_program == "lama" and self.local_save == False:
            if self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
                if (
                    self.list_selected_topics_creator[0].lower()
                    in zusatzthemen_beschreibung
                ):
                    list_path.append("Zusatzthemen")
                else:
                    list_path.append("_Grundkompetenzen")
                # _, klasse = self.split_thema_klasse(
                #     self.list_selected_topics_creator[0]
                # )
                # if klasse == None:
                #     list_path.append("_Grundkompetenzen")
                # else:
                #     list_path.append("{}.Klasse".format(klasse))
            elif self.comboBox_aufgabentyp_cr.currentText() == "Typ 2":
                list_path.append("Einzelbeispiele")

        elif self.chosen_program == "cria" and self.local_save == False:
            list_path.append("Einzelbeispiele")

        #####

        if self.chosen_program == "lama" and self.local_save == False:
            if self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
                thema = self.list_selected_topics_creator[0]

                if thema.lower() in zusatzthemen_beschreibung:
                    list_path.append(thema)
                else:
                    list_path.append(self.list_selected_topics_creator[0][:2])
                    list_path.append(self.list_selected_topics_creator[0])
                    list_path.append("Einzelbeispiele")
                # thema, klasse = self.split_thema_klasse(
                #     self.list_selected_topics_creator[0]
                # )
                # if klasse == None:
                #     list_path.append(self.list_selected_topics_creator[0][:2])
                #     list_path.append(self.list_selected_topics_creator[0])
                #     list_path.append("Einzelbeispiele")
                # else:

        #####
        path = self.create_path_from_list(list_path)

        return path

    def get_integer(self, file_name):
        file_integer = file_name.rsplit("-", 1)[-1]
        file_integer = file_integer.replace(".tex", "").strip()
        file_integer = file_integer.split("[")[0]
        file_integer = file_integer.replace("i.","")
        file_integer = file_integer.replace("_L_","")
        return file_integer

    def get_max_integer_file_variation(self, save_dateipfad):
        max_integer_file = 0
        if self.chosen_program == "cria":
            variation_of = self.chosen_variation.split("_")[1]
        else:
            variation_of = self.chosen_variation

        for file in os.listdir(save_dateipfad):
            if re.match("{}\[.+\].tex".format(variation_of), file):
                split_file = re.split("\[|\]", file)
                max_int = int(split_file[1])
                if max_int > max_integer_file:
                    max_integer_file = max_int
        path_beispieleinreichung = self.get_path_beispieleinreichung()
        for path, dirs, files in os.walk(path_beispieleinreichung):
            for all in files:
                if re.match("{}\[.+\].tex".format(variation_of), all):
                    split_file = re.split("\[|\]", all)
                    max_int = int(split_file[1])
                    if max_int > max_integer_file:
                        max_integer_file = max_int
        return max_integer_file

    def check_files_beispieleinreichung_variation(self, max_integer_file):
        path = self.get_path_beispieleinreichung()

    def get_max_integer_file(self, typ_save, path):
        max_integer_file = self.check_files_path(typ_save, path)
        
        if typ_save[0] != "local" and typ_save != ['admin',1]:
            max_integer_file = self.check_files_beispieleinreichung(
                typ_save, max_integer_file
            )

        return max_integer_file

    def check_files_path(self, typ_save, path):
        max_integer_file = 0

        if not os.path.exists(path):
            try:
                os.makedirs(path)
                print('Creating "{}" for you.'.format(path))
            except PermissionError:
                return max_integer_file

          
        for all in os.listdir(path):
            if all.endswith(".tex"):
                file_integer = self.get_integer(all)
                if int(file_integer) > max_integer_file:
                    max_integer_file = int(file_integer)

        return max_integer_file

    def get_path_beispieleinreichung(self):
        list_path = [path_programm, "Beispieleinreichung"]
        if self.chosen_program == "cria":
            highest_grade = self.get_highest_grade()
            list_path.append(highest_grade)

        path = self.create_path_from_list(list_path)
        return path

    def check_files_beispieleinreichung(self, typ_save, max_integer_file):
        path = self.get_path_beispieleinreichung()

        if self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
            typ = 1
            name = self.list_selected_topics_creator[0]

        if self.comboBox_aufgabentyp_cr.currentText() == "Typ 2":
            typ = 2
        try:
            for all in os.listdir(path):
                if all.endswith(".tex"):
                    file_integer = self.get_integer(all)
                    if self.chosen_program == "cria":
                        if int(file_integer) > max_integer_file:
                            max_integer_file = int(file_integer)
                    elif typ == 1 and name in all:
                        if int(file_integer) > max_integer_file:
                            max_integer_file = int(file_integer)
                    elif typ == 2 and self.get_aufgabentyp(all)==2:
                        if int(file_integer) > max_integer_file:
                            max_integer_file = int(file_integer)

        except FileNotFoundError:
            critical_window(
                'Der Ordner "Beispieleinreichung" konnte nicht gefunden werden und\nmuss zuerst für Sie freigegeben werden.',
                "Derzeit können keine neuen Aufgaben eingegeben werden.\nBitte melden Sie sich unter lama.helpme@gmail.com!",
            )

        return max_integer_file

    def edit_image_name(self, typ_save, name):
        if typ_save[0] == "local":
            local = "_L_"
        else:
            local = ""
        
        if self.chosen_variation == None:
            number = self.max_integer_file + 1
        else:
            list_ = re.split(" - |_", self.chosen_variation)
            variation_number = list_[-1]
            # _,variation_number = self.chosen_variation.split(" - ")
            number = "{0}[{1}]".format(variation_number, self.max_integer_file + 1) 
            # print(number)               

        if typ_save == ['admin', 1]:
            number = "i."+str(number)
 

        if self.chosen_program == "cria":
            highest_grade = self.get_highest_grade()
            name = "{0}{1}_{2}_{3}".format(
                local, highest_grade, number, name
            )

        elif self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
            # thema, klasse = self.split_thema_klasse(
            #     self.list_selected_topics_creator[0]
            # )
            # if thema == None:
            thema = shorten_gk(self.list_selected_topics_creator[0]).upper()
            name = "{0}{1}_{2}_{3}".format(
                local, thema, number, name
            )
            # print(self.chosen_variation)
            # print(name)
            # else:
            #     name = "{0}k{1}_{2}_{3}_{4}".format(
            #         local, klasse, thema, self.max_integer_file + 1, name
            #     )

        elif self.comboBox_aufgabentyp_cr.currentText() == "Typ 2":
            name = "{0}{1}_{2}".format(local, number, name)

        return name

    def replace_image_name(self, typ_save):
        textBox_Entry = self.plainTextEdit.toPlainText()
        for old_image_name in dict_picture_path:
            string = "{" + old_image_name + "}"

            new_image_name = self.edit_image_name(typ_save, old_image_name)
            if typ_save == ["admin", 0]:
                path = "../_database/Bilder/"
            elif typ_save == ["admin", 1]:
                path = "../_database_inoffiziell/Bilder/"
            elif typ_save[0] == "user":
                path = "../Beispieleinreichung/Bilder/"
            elif typ_save[0] == "local":
                path = "../Lokaler_Ordner/Bilder/"

            new_image_name = path + new_image_name

            if string in self.plainTextEdit.toPlainText():
                textBox_Entry = textBox_Entry.replace(old_image_name, new_image_name)
            else:
                return [False, old_image_name]

        return [True, textBox_Entry]

    def copy_image_save(self, typ_save, parent_image_path):
        for old_image_path in list(dict_picture_path.values()):
            old_image_name = os.path.basename(old_image_path)
            new_image_name = self.edit_image_name(typ_save, old_image_name)
            # print(new_image_name)
            # return
            new_image_path = os.path.join(parent_image_path, new_image_name)
            try:
                shutil.copy(old_image_path, new_image_path)
            except FileNotFoundError:
                try:
                    os.mkdir(new_image_path)
                    shutil.copy(old_image_path, new_image_path)
                except FileNotFoundError:
                    warning_window(
                        'Die Grafik mit dem Dateinamen "{}" konnte im Aufgabentext nicht gefunden werden.'.format(
                            old_image_name
                        ),
                        "Bitte versichern Sie sich, dass der Dateiname korrekt geschrieben ist und Sie die richtige Grafik eingefügt haben.",
                    )
                    return

    def create_file_name(self, typ_save):
        number = self.max_integer_file + 1
        if typ_save == ['admin', 1] and self.chosen_variation == None:
            number = "i."+str(number)
            
        if self.chosen_variation != None:
            if self.chosen_program == "cria":
                klasse, filenumber = self.chosen_variation.split("_")
                name = "{0}[{1}].tex".format(filenumber, number)
            else:
                name = "{0}[{1}].tex".format(self.chosen_variation, number)
        elif self.chosen_program == "cria":
            name = "{0}.tex".format(number)
        elif self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
            # thema, klasse = self.split_thema_klasse(
            #     self.list_selected_topics_creator[0]
            # )
            # if thema == None:
            name = "{0} - {1}.tex".format(
                self.list_selected_topics_creator[0], number
            )
            # else:
            #     name = "K{0} - {1} - {2}.tex".format(klasse, thema.upper(), number)
        else:
            name = "{0}.tex".format(number)

        if self.local_save == True:
            name = "_L_" + name

        return name

    def get_klasse_section(self):
        if self.chosen_program == "cria":
            klasse = self.get_highest_grade().upper()
        if self.chosen_program == "lama":
            if self.comboBox_klassen_cr.currentIndex() != 0:
            #     _, klasse = self.split_thema_klasse(
            #         self.list_selected_topics_creator[0]
            #     )
            #     if klasse != None:
            #         temp_list = []
            #         for all in self.list_selected_topics_creator:
            #             temp_themen, temp_klasse = self.split_thema_klasse(all)
            #             if int(temp_klasse) > int(klasse):
            #                 klasse = temp_klasse
            #             temp_list.append(temp_themen)
            #         klasse = "K" + klasse
            # else:
                klasse = list(Klassen.keys())[
                    self.comboBox_klassen_cr.currentIndex() - 1
                ]
                klasse = klasse.upper()
            else:
                klasse = ""

        # if klasse == None:
        #     klasse = ""
        return klasse

    def get_themen_section(self):
        if self.chosen_program == "cria":
            themen_auswahl = []
            for all in self.list_selected_topics_creator:
                thema = all[1] + "." + all[2]
                if thema not in themen_auswahl:
                    themen_auswahl.append(thema)
            themen = ", ".join(sorted(themen_auswahl))

        elif self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
            # themen, _ = self.split_thema_klasse(self.list_selected_topics_creator[0])
            # if themen == None:  # Typ1 - GK
            themen = self.list_selected_topics_creator[0]
            # else:  # Typ1 - Zusatzthemen
                # themen = themen.upper()

        elif (
            self.comboBox_aufgabentyp_cr.currentText() == "Typ 2"
        ):  # Typ2 - GK & Zusatzthemen
            # list_ = []
            # for all in self.list_selected_topics_creator:
                # thema, _ = self.split_thema_klasse(all)
                # if thema == None:
                # list_.append(all)
                # else:
                    # list_.append(thema.upper())
            themen = ", ".join(self.list_selected_topics_creator)

        return themen

    def create_section_string(self, list_):
        section_string = str(list_[0])
        for all in list_[1:]:
            section_string = section_string + " - " + str(all)

        return section_string

    def create_section(self, typ_save):
        if self.chosen_variation != None:
            if self.chosen_program == "lama":
                x = self.chosen_variation.split(" - ")
            else:
                x = self.chosen_variation.split("_")
            variation_nummer = x[-1]

            nummer = "{0}[{1}]".format(variation_nummer, self.max_integer_file + 1)

        else:
            nummer = self.max_integer_file + 1
            if typ_save == ['admin', 1]:
                nummer = "i."+str(nummer)


        klasse = self.get_klasse_section()

        themen = self.get_themen_section()

        titel = self.create_information_titel().replace(" - ", "-")
        try:
            aufgabenformat = list(dict_aufgabenformate.keys())[
                list(dict_aufgabenformate.values()).index(
                    self.comboBox_af.currentText()
                )
            ]
            aufgabenformat = aufgabenformat.upper()
        except ValueError:
            aufgabenformat = ""
        quelle = self.lineEdit_quelle.text().replace(" - ", "-")

        if self.chosen_program == "cria":
            list_section = [
                klasse,
                themen,
                nummer,
                titel,
                aufgabenformat,
                quelle,
            ]  # Unterstufe

        elif self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
            # thema, _ = self.split_thema_klasse(self.list_selected_topics_creator[0])

            if klasse == "":
                list_section = [
                    themen,
                    nummer,
                    titel,
                    aufgabenformat,
                    quelle,
                ]  # Typ1 - GK (ohne Klasse)
            else:
                list_section = [
                    themen,
                    nummer,
                    klasse,
                    titel,
                    aufgabenformat,
                    quelle,
                ]  # Typ1 - GK (mit Klasse)

            # else:
            #     list_section = [
            #         klasse,
            #         themen,
            #         nummer,
            #         titel,
            #         aufgabenformat,
            #         quelle,
            #     ]  # Typ1 - Zusatzthemen

        elif self.comboBox_aufgabentyp_cr.currentText() == "Typ 2":
            if klasse == "":
                list_section = [
                    nummer,
                    themen,
                    titel,
                    quelle,
                ]  # Typ2 - GK (ohne Klasse)
            else:
                list_section = [
                    nummer,
                    klasse,
                    themen,
                    titel,
                    quelle,
                ]  # Typ2 - GK (mit Klasse) bzw. nur Zusatzthemen

        section = self.create_section_string(list_section)

        if self.local_save == True:
            local = "*Lokal* "
        else:
            local = ""

        section = local + section

        section = "\section{" + section + "}"

        return section

    def define_themen_string_cria(self):
        list_ = [
            x[1] + "." + x[2] + " (" + x[0][1] + ".)"
            for x in self.list_selected_topics_creator
        ]
        string = ", ".join(list_)
        return string

    def button_speichern_pressed(self):
        # self.creator_mode = "user"
        self.local_save = False

        ######## WARNINGS #####

        warning = self.check_entry_creator()
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

        if self.chosen_variation == None:
            save_dateipfad = self.create_aufgabenpfad(typ_save)

            self.max_integer_file = self.get_max_integer_file(typ_save, save_dateipfad)

        else:
            dateipfad = self.get_dateipfad_aufgabe(self.chosen_variation)
            save_dateipfad = os.path.dirname(dateipfad)

            self.max_integer_file = self.get_max_integer_file_variation(save_dateipfad)

        ############################################################################

        response = self.replace_image_name(typ_save)
        if response[0] == False:
            warning_window(
                'Die Grafik mit dem Dateinamen "{}" konnte im Aufgabentext nicht gefunden werden.'.format(
                    response[1]
                ),
                "Bitte versichern Sie sich, dass der Dateiname korrekt geschrieben ist und Sie die richtige Grafik eingefügt haben.",
            )
            return
        else:
            textBox_Entry = response[1]

        list_path = self.get_parent_folder(typ_save)
        if typ_save[0] == "user":
            list_path[1] = "Beispieleinreichung"
        list_path.append("Bilder")
        parent_image_path = self.create_path_from_list(list_path)

        self.copy_image_save(typ_save, parent_image_path)

        file_name = self.create_file_name(typ_save)

        if typ_save[0] == "user":
            save_dateipfad = self.get_path_beispieleinreichung()

        abs_path_file = os.path.join(save_dateipfad, file_name)

        section = self.create_section(typ_save)

        with open(abs_path_file, "w", encoding="utf8") as file:
            file.write(section + "\n\n")
            if self.chosen_program == "cria":
                string_themen = self.define_themen_string_cria()
                file.write(
                    "\\begin{{langesbeispiel}}\item[{0}] %PUNKTE DER AUFGABE\n{1}\n\n\\antwort{{Themen: {2}}}\n\\end{{langesbeispiel}}".format(
                        self.spinBox_punkte.value(), textBox_Entry, string_themen
                    )
                )
            elif self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
                file.write(
                    "\\begin{{beispiel}}[{0}]{{{1}}}\n{2}\n\\end{{beispiel}}".format(
                        self.list_selected_topics_creator[0],
                        self.spinBox_punkte.value(),
                        textBox_Entry,
                    )
                )
            else:
                file.write(
                    "\\begin{{langesbeispiel}}\item[{0}] %PUNKTE DER AUFGABE\n{1}\n\n\\antwort{{GK/Themen: {2}}}\n\\end{{langesbeispiel}}".format(
                        self.spinBox_punkte.value(),
                        textBox_Entry,
                        ", ".join(self.list_selected_topics_creator),
                    )
                )

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

        QtWidgets.QApplication.restoreOverrideCursor()
        information_window(text, "", window_title, information)

        self.suchfenster_reset()

    ##################################################################
    ################## Befehle LAMA SAGE################################

    def action_refreshddb_selected(self):
        refresh_ddb(self)
        if self.chosen_program == "lama":
            self.beispieldaten_dateipfad_1 = self.define_beispieldaten_dateipfad(1)
            self.beispieldaten_dateipfad_2 = self.define_beispieldaten_dateipfad(2)
        elif self.chosen_program == "cria":
            self.beispieldaten_dateipfad_cria = self.define_beispieldaten_dateipfad(
                "cria"
            )

        self.refresh_label_update()
        if self.cb_drafts_sage.isChecked() == True:
            self.add_drafts_to_beispieldaten()
        self.adapt_choosing_list("sage")
    
    def action_push_database(self):
        path_programdata = os.getenv('PROGRAMDATA')
        database = os.path.join(path_programdata, "LaMA", "_database")
        repo = git.Repo(database)
        if not repo.is_dirty(untracked_files=True):
            information_window("Es wurden keine Änderungen an der Datenbank vorgenommen.")
            return

        response = question_window("Sind Sie sicher, dass Sie die Datenbank hochladen möchten?")
        if response == False:
            return

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))       
        repo.git.add(A=True)
        repo.index.commit('new commit')
        o = repo.remotes.origin
        o.push()
        QtWidgets.QApplication.restoreOverrideCursor()
        information_window("Die Datenbank wurde erfolgreich hochgeladen.")


    def define_beispieldaten_dateipfad(self, typ):

        log_file = os.path.join(
            path_localappdata_lama,"Teildokument", "log_file_{}".format(typ)
        )

        beispieldaten_dateipfad = self.get_beispieldaten_dateipfad(log_file)

        return beispieldaten_dateipfad

    def check_if_file_exists(self, aufgabe):  # aufgabe
        typ = self.get_aufgabentyp(aufgabe)

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

    def sage_load(self, external_file_loaded):
        if external_file_loaded == False:
            try:
                os.path.dirname(self.saved_file_path)
            except AttributeError:
                self.saved_file_path = path_programm

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

        loaded_file = self.load_file(self.saved_file_path)

        try:
            if self.chosen_program == loaded_file["data_gesamt"]["program"]:
                if self.list_alle_aufgaben_sage != []:
                    self.reset_sage()
            else:
                response = self.change_program()
                if response == False:
                    return
        except KeyError:
            warning_window(
                "Die geöffnete *.lama-Datei ist veraltet und kann nur mit der Version LaMA 1.x geöffnet werden.",
                "Bitte laden Sie eine aktuelle *.lama-Datei oder kontaktieren Sie lama.helpme@gmail.com, wenn Sie Hilfe benötigen.",
            )
            return

        self.dict_all_infos_for_file = self.load_file(self.saved_file_path)

        self.update_gui("widgets_sage")

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        self.list_alle_aufgaben_sage = self.dict_all_infos_for_file[
            "list_alle_aufgaben"
        ]
        self.dict_alle_aufgaben_sage = self.dict_all_infos_for_file[
            "dict_alle_aufgaben"
        ]

        for aufgabe in self.list_alle_aufgaben_sage:
            file_found = self.check_if_file_exists(aufgabe)
            if file_found == False:
                QtWidgets.QApplication.restoreOverrideCursor()
                response = question_window(
                    'Die Aufgabe "{}" konnte in der Datenbank nicht gefunden werden. Dies könnte daran liegen, dass die Datenbank veraltet ist (Tipp: Datenbank aktualisieren)'.format(
                        aufgabe
                    ),
                    "Wollen Sie diese Aufgabe entfernen? (Ansonsten wird die Datei nicht geladen)",
                    "Aufgabe nicht gefunden",
                )

                if response == True:
                    self.list_alle_aufgaben_sage.remove(aufgabe)
                    del self.dict_alle_aufgaben_sage[aufgabe]
                    QtWidgets.QApplication.setOverrideCursor(
                        QtGui.QCursor(QtCore.Qt.WaitCursor)
                    )
                if response == False:
                    return

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

        self.list_copy_images = self.dict_all_infos_for_file["data_gesamt"][
            "copy_images"
        ]

        for aufgabe in self.list_alle_aufgaben_sage:
            self.build_aufgaben_schularbeit(aufgabe)

        self.spinBox_default_pkt.setValue(
            self.dict_all_infos_for_file["data_gesamt"]["Typ1 Standard"]
        )
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

        QtWidgets.QApplication.restoreOverrideCursor()

    def sage_save(self, path_create_tex_file=False, autosave = False):  # path_file
        try:
            self.saved_file_path
        except AttributeError:
            self.saved_file_path = path_programm

        if path_create_tex_file == False and autosave == False:
            path_backup_file = QtWidgets.QFileDialog.getSaveFileName(
                None,
                "Speichern unter",
                self.saved_file_path,
                "LaMA Datei (*.lama);; Alle Dateien (*.*)",
            )
            if path_backup_file[0] == "":
                return
            self.collect_all_infos_for_creating_file()
            save_file = path_backup_file[0]

        elif autosave != False:
            save_file = autosave

        else:
            name, extension = os.path.splitext(path_create_tex_file)
            path_create_tex_file = name + "_autosave.lama"
            save_file = path_create_tex_file

        if autosave == False:
            self.update_gui("widgets_sage")

            self.saved_file_path = save_file

        with open(save_file, "w+", encoding="utf8") as saved_file:
            json.dump(self.dict_all_infos_for_file, saved_file, ensure_ascii=False)

    def define_titlepage(self):
        if self.comboBox_pruefungstyp.currentText() == "Quiz":
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
                        len(random_list), ui.random_quiz_response[0],
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
                    path_localappdata_lama,"Teildokument", "titlepage_save"
                )
            if self.chosen_program == "cria":
                self.dict_titlepage_cria = dict_titlepage
                titlepage_save = os.path.join(
                    path_localappdata_lama,"Teildokument", "titlepage_save_cria"
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

    def get_aufgabentyp(self, aufgabe):
        aufgabe = aufgabe.replace("_L_", "")
        if self.chosen_program == "cria":
            typ = None
        elif re.search("[A-Z]", aufgabe) == None:
            typ = 2
        else:
            typ = 1
        return typ

    def get_aufgabenverteilung(self):
        num_typ1 = 0
        num_typ2 = 0
        for all in self.list_alle_aufgaben_sage:
            typ = self.get_aufgabentyp(all)
            if typ == 1:
                num_typ1 += 1
            if typ == 2:
                num_typ2 += 1

        return [num_typ1, num_typ2]

    def sage_aufgabe_add(self, aufgabe):
        if self.chosen_program == "lama":

            old_num_typ1, old_num_typ2 = self.get_aufgabenverteilung()

            typ = self.get_aufgabentyp(aufgabe)
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

        self.label_gesamtbeispiele.setText(_translate("MainWindow", label, None,))

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
        del self.dict_alle_aufgaben_sage[aufgabe]
        del self.dict_variablen_punkte[aufgabe]
        self.list_alle_aufgaben_sage.remove(aufgabe)
        if self.get_aufgabentyp(aufgabe) == 2:
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
                "Aufgabe entfernen?")
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

    def spinbox_pkt_changed(self, aufgabe, spinbox_pkt):
        self.dict_alle_aufgaben_sage[aufgabe][0] = spinbox_pkt.value()
        self.update_punkte()

    def spinbox_abstand_changed(self, aufgabe, spinbox_abstand):
        self.dict_alle_aufgaben_sage[aufgabe][1] = spinbox_abstand.value()
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
        pos_end_typ1 = pos_maximum - height_aufgabe*num_typ2

        if self.listWidget.currentItem() != None:
            aufgabe = self.listWidget.currentItem().text()
            typ = self.get_aufgabentyp(aufgabe)
            if typ == 2 or typ == None:
                self.scrollArea_chosen.verticalScrollBar().setValue(pos_maximum)
            elif typ == 1:
                self.scrollArea_chosen.verticalScrollBar().setValue(pos_end_typ1)
        else:
            self.scrollArea_chosen.verticalScrollBar().setValue(pos_maximum)

        


    def get_punkteverteilung(self):
        pkt_typ1 = 0
        pkt_typ2 = 0
        pkt_ausgleich = 0
        gesamtpunkte = 0
        for all in self.dict_variablen_punkte:
            typ = self.get_aufgabentyp(all)
            if typ == None:
                gesamtpunkte += self.dict_variablen_punkte[all].value()
            elif typ == 1:
                pkt_typ1 += self.dict_variablen_punkte[all].value()
                gesamtpunkte += self.dict_variablen_punkte[all].value()
            elif typ == 2:
                pkt_typ2 += self.dict_variablen_punkte[all].value()
                pkt_ausgleich += self.dict_alle_aufgaben_sage[all][3]
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
            if self.get_aufgabentyp(aufgabe) == 2:
                number_ausgleichspkt_gesamt += self.dict_alle_aufgaben_sage[aufgabe][3]

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

        if self.chosen_program == 'cria':
            self.label_gesamtbeispiele.setText("Anzahl der Aufgaben: {0}"
                .format(num_total)
            )
        if self.chosen_program == 'lama':
            self.label_gesamtbeispiele.setText("Anzahl der Aufgaben: {0}\n(Typ1: {1} / Typ2: {2})"
                .format(
                    num_total, num_typ1, num_typ2
                    )
            )

        self.label_gesamtpunkte.setText(
            _translate("MainWindow", "Gesamtpunkte: %i" % gesamtpunkte, None)
        )

    def update_default_pkt(self):
        for all in self.dict_variablen_punkte:
            if self.get_aufgabentyp(all) == 1:
                self.dict_variablen_punkte[all].setValue(
                    self.spinBox_default_pkt.value()
                )
                self.dict_alle_aufgaben_sage[all][0] = self.spinBox_default_pkt.value()

    def create_neue_aufgaben_box(self, index, aufgabe, aufgaben_infos):
        typ = self.get_aufgabentyp(aufgabe)
        aufgaben_verteilung = self.get_aufgabenverteilung()
        if self.chosen_program == "cria":
            klasse, aufgaben_nummer = self.split_klasse_aufgabe(aufgabe)
            klasse = klasse[1]

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
            try:
                aufgabenformat = (
                    " (" + dict_aufgabenformate[aufgaben_infos[3].lower() + ")"]
                )
            except KeyError:
                aufgabenformat = ""
            if "_L_" in aufgaben_nummer:
                x = aufgaben_nummer.replace("_L_", "")
                label = "{0}. Klasse - {1} (lokal){2}".format(klasse, x, aufgabenformat)
            else:
                label = "{0}. Klasse - {1}{2}".format(
                    klasse, aufgaben_nummer, aufgabenformat
                )
        elif typ == 1:
            try:
                aufgabenformat = (
                    " (" + dict_aufgabenformate[aufgaben_infos[3].lower()] + ")"
                )
            except KeyError:
                aufgabenformat = ""
            label = "{0}{1}".format(aufgabe, aufgabenformat)
        elif typ == 2:
            label = "{0}".format(aufgabe)

        label_aufgabe = create_new_label(new_groupbox, label, True)
        gridLayout_gB.addWidget(label_aufgabe, 1, 0, 1, 1)

        label_titel = create_new_label(
            new_groupbox, "Titel: {}".format(aufgaben_infos[2]), True
        )
        gridLayout_gB.addWidget(label_titel, 2, 0, 1, 1)

        groupbox_pkt = create_new_groupbox(new_groupbox, "Punkte")
        groupbox_pkt.setSizePolicy(SizePolicy_fixed)
        gridLayout_gB.addWidget(groupbox_pkt, 0, 1, 3, 1, QtCore.Qt.AlignRight)

        punkte = self.dict_alle_aufgaben_sage[aufgabe][0]

        horizontalLayout_groupbox_pkt = QtWidgets.QHBoxLayout(groupbox_pkt)
        horizontalLayout_groupbox_pkt.setObjectName(
            _fromUtf8("horizontalLayout_groupbox_pkt")
        )
        spinbox_pkt = create_new_spinbox(groupbox_pkt)
        spinbox_pkt.setValue(punkte)
        spinbox_pkt.valueChanged.connect(
            partial(self.spinbox_pkt_changed, aufgabe, spinbox_pkt)
        )
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

        abstand = self.dict_alle_aufgaben_sage[aufgabe][1]
        spinbox_abstand = create_new_spinbox(groupbox_abstand_ausgleich)
        spinbox_abstand.setValue(abstand)
        spinbox_abstand.valueChanged.connect(
            partial(self.spinbox_abstand_changed, aufgabe, spinbox_abstand)
        )
        verticalLayout_abstand.addWidget(spinbox_abstand)


        if typ == 2:
            groupbox_abstand_ausgleich.setTitle("Ausgleichspkte")
            spinbox_abstand.hide()

            label_ausgleichspkt = create_new_label(
                groupbox_abstand_ausgleich,
                "{}".format(self.dict_alle_aufgaben_sage[aufgabe][3]),
            )
            label_ausgleichspkt.setStyleSheet("padding-top: 5px; padding-bottom: 5px;")
            verticalLayout_abstand.addWidget(label_ausgleichspkt)

            self.dict_variablen_label[aufgabe] = label_ausgleichspkt
        else:
            groupbox_abstand_ausgleich.setToolTip("Neue Seite: Abstand=99")

            # label_ausgleichspkt.setSizePolicy(SizePolicy_min)
            # label_ausgleichspkt.setToolTip("Anzahl der Ausgleichspunkte")            

            #groupbox_abstand.hide()

        # if typ == 2:
            # label_ausgleichspkt = create_new_label(
            #     groupbox_pkt,
            #     "AP: {}".format(self.dict_alle_aufgaben_sage[aufgabe][3]),
            # )
            # # label_ausgleichspkt.setSizePolicy(SizePolicy_min)
            # label_ausgleichspkt.setToolTip("Anzahl der Ausgleichspunkte")
            
            # gridLayout_gB.addWidget(label_ausgleichspkt, 2, 2, 1, 1, QtCore.Qt.AlignCenter)
            
        # if typ == 2:
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

    def get_klasse(self, aufgabe):
        klasse = list_klassen[self.comboBox_klassen.currentIndex()]

        return klasse

    def collect_all_infos_aufgabe(self, aufgabe):
        typ = self.get_aufgabentyp(aufgabe)

        if typ == None:
            punkte = self.get_punkte_aufgabe(aufgabe)
            klasse, aufgabe = self.split_klasse_aufgabe(aufgabe)
            name = aufgabe + ".tex"
            for all in self.beispieldaten_dateipfad_cria:
                if klasse.upper() in all:
                    filename = os.path.basename(self.beispieldaten_dateipfad_cria[all])
                    if name == filename:
                        info = split_section(all, self.chosen_program)
                        titel = info[3]
                        typ_info = info[4]  # Aufgabenformat

        elif typ == 1:
            name = aufgabe + ".tex"
            for all in self.beispieldaten_dateipfad_1:
                filename = os.path.basename(self.beispieldaten_dateipfad_1[all])
                if name == filename:
                    x = all.split(" - ")
                    titel = x[-3]
                    typ_info = x[-2]  # Aufgabenformat
            punkte = self.spinBox_default_pkt.value()

        elif typ == 2:
            name = aufgabe + ".tex"
            for all in self.beispieldaten_dateipfad_2:
                filename = os.path.basename(self.beispieldaten_dateipfad_2[all])
                if name == filename:
                    x = all.split(" - ")
                    titel = x[-2]
                    typ_info = self.get_number_ausgleichspunkte(
                        aufgabe
                    )  # Ausgleichspunkte

            punkte = self.get_punkte_aufgabe(aufgabe)

        return [punkte, 0, titel, typ_info]

    def get_punkte_aufgabe(self, aufgabe):
        content = collect_content(self, aufgabe)
        start = re.findall("begin{beispiel}.*\{[0-9][0-9]?\}", content)
        typ = "beispiel"
        if start == []:
            start = re.findall("begin{langesbeispiel}.*\\\item\[[0-9][0-9]?\]", content)
            typ = "langesbeispiel"
        try:
            if typ == "langesbeispiel":
                punkte = int(re.findall(r"\[([0-9][0-9]?)\]", start[0])[0])
            else:
                punkte = int(re.findall(r"\{([0-9][0-9]?)\}", start[0])[0])

            return punkte
        except IndexError:
            return 0

    def get_dateipfad_from_filename(self, list_path, filename, klasse=None):
        if self.chosen_program == "cria":
            for path in list_path:
                if klasse.lower() in path.lower():
                    if filename == os.path.basename(path):
                        dateipfad = path
                        break
        elif self.chosen_program == "lama":
            for path in list_path:
                if filename == os.path.basename(path):
                    dateipfad = path
                    break
        return dateipfad

    def get_dateipfad_aufgabe(self, aufgabe, draft=False):
        typ = self.get_aufgabentyp(aufgabe)
        klasse = None

        if self.chosen_program == "cria":
            list_path = self.beispieldaten_dateipfad_cria.values()
            klasse, aufgabe = self.split_klasse_aufgabe(aufgabe)
            filename = aufgabe + ".tex"

        if self.chosen_program == "lama":
            if typ == 1:
                list_path = self.beispieldaten_dateipfad_1.values()
            elif typ == 2:
                list_path = self.beispieldaten_dateipfad_2.values()
            filename = aufgabe + ".tex"

        dateipfad = self.get_dateipfad_from_filename(list_path, filename, klasse)

        return dateipfad

    def get_number_ausgleichspunkte(self, aufgabe):
        typ = self.get_aufgabentyp(aufgabe)

        if typ == 2:
            content = collect_content(self, aufgabe)

            number_ausgleichspunkte = content.count("\\fbox{A}")
            number_ausgleichspunkte = number_ausgleichspunkte + content.count(
                "\\ASubitem"
            )

            return number_ausgleichspunkte

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

    def build_klasse_aufgabe(self, aufgabe):
        klasse = self.get_klasse(aufgabe)
        if "_L_" in aufgabe:
            klasse_aufgabe = klasse + aufgabe
        else:
            klasse_aufgabe = klasse + "_" + aufgabe
        return klasse_aufgabe

    def add_image_path_to_list(self, aufgabe):
        content = collect_content(self, aufgabe)

        if "\\includegraphics" in content:
            matches = re.findall("/Bilder/(.+.eps)}", content)
            for image in matches:
                self.list_copy_images.append(image)

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
            item_infos = self.collect_all_infos_aufgabe(item)
            neue_aufgaben_box = self.create_neue_aufgaben_box(
                index_item, item, item_infos
            )
            self.gridLayout_8.addWidget(neue_aufgaben_box, index_item, 0, 1, 1)
            index_item + 1


        self.spacerItem = QtWidgets.QSpacerItem(
            20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_8.addItem(self.spacerItem, index_item + 1, 0, 1, 1)

        self.add_image_path_to_list(aufgabe)

        self.update_punkte()

            
        # pos_value = self.scrollArea_chosen.verticalScrollBar().value()
        # pos_maximum = self.scrollArea_chosen.verticalScrollBar().maximum()
        # print(pos_maximum)
        # # height_aufgabe = 110
        # # print(self.get_aufgabenverteilung())
        # # num_typ2 = self.get_aufgabenverteilung()[1]
        # # pos_end_typ1 = pos_maximum - height_aufgabe*num_typ2 + 400
        # self.scrollbar_position = [pos_value, pos_end_typ1]
        # self.scrollArea_chosen.verticalScrollBar().setValue(pos_maximum)
        
        # print(self.scrollbar_position)

        QtWidgets.QApplication.restoreOverrideCursor()

      


    def pushButton_ausgleich_pressed(self, aufgabe):
        content = collect_content(self, aufgabe)

        content_no_environment = split_content_no_environment(content)

        # print(aufgabe)
        typ = self.get_aufgabentyp(aufgabe)
        # return
        if typ == 2:
            try:
                split_content, index_end = split_aufgaben_content(content)
                split_content = split_content[:index_end]
            except Exception as e1:
                try:
                    split_content = split_aufgaben_content_new_format(content)
                except Exception as e2:
                    split_content = None
                if split_content == None:
                    warning_window(
                        "Es ist ein Fehler bei der Anzeige der Aufgabe {} aufgetreten! (Die Aufgabe kann voraussichtlich dennoch verwendet und individuell in der TeX-Datei bearbeitet werden.)\n".format(
                            aufgabe
                        ),
                        'Bitte melden Sie den Fehler unter dem Abschnitt "Feedback & Fehler" an das LaMA-Team. Vielen Dank!',
                    )
                    return

            
            if aufgabe in self.dict_sage_ausgleichspunkte_chosen.keys():
                list_sage_ausgleichspunkte_chosen = self.dict_sage_ausgleichspunkte_chosen[
                    aufgabe
                ]
            else:
                list_sage_ausgleichspunkte_chosen = []
                for all in split_content:
                    if "\\fbox{A}" in all:
                        x = all.replace("\\fbox{A}", "")
                        list_sage_ausgleichspunkte_chosen.append(x)
                    if "\\ASubitem" in all:
                        x = all.replace("\\ASubitem", "")
                        list_sage_ausgleichspunkte_chosen.append(x)

            if aufgabe in self.dict_sage_hide_show_items_chosen.keys():
                list_sage_hide_show_items_chosen = self.dict_sage_hide_show_items_chosen[
                    aufgabe
                ]
            else:
                list_sage_hide_show_items_chosen = []

            if aufgabe in self.dict_sage_individual_change.keys():
                list_sage_individual_change = self.dict_sage_individual_change[aufgabe]
            else:
                list_sage_individual_change = []
        else:
            if aufgabe in self.dict_sage_individual_change.keys():
                list_sage_individual_change = self.dict_sage_individual_change[aufgabe]
            else:
                list_sage_individual_change = []
            list_sage_hide_show_items_chosen = []
            list_sage_ausgleichspunkte_chosen = []
            # list_sage_individual_change =  []
            split_content = None

        self.Dialog = QtWidgets.QDialog(
            None,
            QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint
            | QtCore.Qt.WindowMaximizeButtonHint
            | QtCore.Qt.WindowMinimizeButtonHint,
        )
        self.ui = Ui_Dialog_ausgleichspunkte()
        self.ui.setupUi(
            self.Dialog,
            aufgabe,
            typ,
            content_no_environment,
            split_content,
            list_sage_ausgleichspunkte_chosen,
            list_sage_hide_show_items_chosen,
            list_sage_individual_change,
            self.display_mode,
        )

        self.Dialog.exec_()

        self.dict_sage_individual_change[
            aufgabe
        ] = self.ui.list_sage_individual_change
        # print(self.ui.list_sage_individual_change)
        # print(self.dict_sage_individual_change)
        # print(self.dict_alle_aufgaben_sage)
        if typ == 2:
            self.dict_sage_ausgleichspunkte_chosen[
                aufgabe
            ] = self.ui.list_sage_ausgleichspunkte_chosen

            self.dict_sage_hide_show_items_chosen[
                aufgabe
            ] = self.ui.list_sage_hide_show_items_chosen

            self.dict_alle_aufgaben_sage[aufgabe][3] = len(
                self.ui.list_sage_ausgleichspunkte_chosen
            )

            self.dict_variablen_label[aufgabe].setText(
                _translate(
                    "MainWindow",
                    "{}".format(
                        len(self.ui.list_sage_ausgleichspunkte_chosen)
                    ),
                    None,
                )
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
            intervall = self.lama_settings['autosave']
        except KeyError:
            self.lama_settings['autosave'] = 2
            intervall = 2

        if intervall == 0:
            return

        self.collect_all_infos_for_creating_file()
        autosave_file = os.path.join(path_localappdata_lama,"Teildokument", "autosave.lama")
        try: 
            modification = modification_date(autosave_file).strftime("%y%m%d-%H%M")
            date, time_tag = modification.split("-")
            day_time = datetime.datetime.now()

            day_time = day_time - datetime.timedelta(minutes=intervall)
            today, now_minus_intervall  = day_time.strftime("%y%m%d-%H%M").split("-")

            if date != today:
                self.sage_save(autosave=autosave_file)
            elif now_minus_intervall>time_tag:
                self.sage_save(autosave=autosave_file)
        except FileNotFoundError:
            self.sage_save(autosave=autosave_file)


    def nummer_clicked(self, item):
        if "(Entwurf)" in item.text():
            aufgabe = item.text().replace(" (Entwurf)", "")
            # draft=True
        elif "(lokal)" in item.text():
            aufgabe = item.text().replace(" (lokal)", "")
            # draft=False
        else:
            aufgabe = item.text()
            # draft=False

        if self.chosen_program == "cria":
            aufgabe = self.build_klasse_aufgabe(aufgabe)

        if aufgabe in self.list_alle_aufgaben_sage:
            return

        try:
            collect_content(self, aufgabe)
        except FileNotFoundError:
            warning_window(
                'Die Datei konnte nicht gefunden werden.\nBitte wählen Sie "Refresh Database" (F5) und versuchen Sie es erneut.'
            )
            return

        self.sage_aufgabe_add(aufgabe)
        infos = self.collect_all_infos_aufgabe(aufgabe)
        self.dict_alle_aufgaben_sage[aufgabe] = infos

        self.build_aufgaben_schularbeit(aufgabe)  # aufgabe, aufgaben_verteilung
        self.lineEdit_number.setText("")
        self.lineEdit_number.setFocus()
        self.check_for_autosave()


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
                        item.text(), self.comboBox_klassen_fb_cria.currentText(),
                    ),
                    None,
                )
            )

    def comboBox_klassen_changed(self, list_mode):
        if list_mode == "sage":
            dict_klasse_name = eval(
                "dict_{}_name".format(
                    list_klassen[self.comboBox_klassen.currentIndex()]
                )
            )
            self.comboBox_kapitel.clear()
            self.comboBox_unterkapitel.clear()
            self.comboBox_kapitel.addItem("")
        if list_mode == "feedback":
            self.label_example.setText(
                _translate("MainWindow", "Ausgewählte Aufgabe: -", None)
            )
            dict_klasse_name = eval(
                "dict_{}_name".format(
                    list_klassen[self.comboBox_klassen_fb_cria.currentIndex()]
                )
            )
            self.listWidget_fb_cria.clear()
            self.comboBox_kapitel_fb_cria.clear()
            self.comboBox_unterkapitel_fb_cria.clear()
            self.comboBox_kapitel_fb_cria.addItem("")

        for all in dict_klasse_name.keys():
            if list_mode == "sage":
                self.comboBox_kapitel.addItem(dict_klasse_name[all] + " (" + all + ")")
            if list_mode == "feedback":
                self.comboBox_kapitel_fb_cria.addItem(
                    dict_klasse_name[all] + " (" + all + ")"
                )

        # self.adapt_choosing_list(list_mode)

    def comboBox_kapitel_changed(self, list_mode):
        dict_klasse = eval(
            "dict_{}".format(list_klassen[self.comboBox_klassen.currentIndex()])
        )

        if list_mode == "sage":
            dict_klasse = eval(
                "dict_{}".format(list_klassen[self.comboBox_klassen.currentIndex()])
            )
            self.comboBox_unterkapitel.clear()

            kapitel_shortcut = list(dict_klasse.keys())[
                self.comboBox_kapitel.currentIndex() - 1
            ]

            # self.comboBox_unterkapitel.clear()
            self.comboBox_unterkapitel.addItem("")

        if list_mode == "feedback":
            dict_klasse = eval(
                "dict_{}".format(
                    list_klassen[self.comboBox_klassen_fb_cria.currentIndex()]
                )
            )
            self.comboBox_unterkapitel_fb_cria.clear()

            kapitel_shortcut = list(dict_klasse.keys())[
                self.comboBox_kapitel_fb_cria.currentIndex() - 1
            ]
            self.comboBox_unterkapitel_fb_cria.addItem("")

        index = 1
        for all in dict_klasse[kapitel_shortcut]:
            if list_mode == "sage":
                self.comboBox_unterkapitel.addItem(
                    dict_unterkapitel[all] + " (" + all + ")"
                )

            if list_mode == "feedback":
                self.comboBox_unterkapitel_fb_cria.addItem(
                    dict_unterkapitel[all] + " (" + all + ")"
                )

            index += 1

        if list_mode == "sage":
            if self.comboBox_kapitel.currentIndex() == 0:
                self.comboBox_unterkapitel.clear()
        if list_mode == "feedback":
            if self.comboBox_kapitel_fb_cria.currentIndex() == 0:
                self.comboBox_unterkapitel_fb_cria.clear()

        self.adapt_choosing_list(list_mode)

    def comboBox_unterkapitel_changed(self, list_mode):
        self.adapt_choosing_list(list_mode)

    def get_beispieldaten_dateipfad(self, log_file):
        try:
            with open(log_file, encoding="utf8") as f:
                dictionary = json.load(f)
        except FileNotFoundError:
            refresh_ddb(self)
            with open(log_file, encoding="utf8") as f:
                dictionary = json.load(f)

        return dictionary

    def get_name_from_path(self, path):
        path, filename = os.path.split(path)
        filename, extension = os.path.splitext(filename)

        return filename

    def get_aufgabentyp_from_path(self, abs_path):
        path, filename = os.path.split(abs_path)
        parent_folder = os.path.basename(path)

        if parent_folder != "Beispieleinreichung":
            typ = None
        elif re.search("[A-Z]", filename) == None:
            typ = 2
        else:
            typ = 1

        return typ

    def get_beispieldaten_dateipfad_draft(self, typ):
        drafts_path = os.path.join(path_programm, "Beispieleinreichung")
        list_section = []
        list_path = []
        beispieldaten_dateipfad_draft = search_files(drafts_path)

        for section in beispieldaten_dateipfad_draft.keys():
            path = beispieldaten_dateipfad_draft[section]
            aufgabentyp = self.get_aufgabentyp_from_path(path)
            if aufgabentyp == typ:
                list_section.append(section)
                list_path.append(path)

        return list_section, list_path

    def delete_item_without_string_from_list(self, string, list_):
        for section in list_[:]:
            if string not in section:
                list_.remove(section)

        return list_

    # def split_section(self, section):
    #     section = re.split(" - |{|}", section)
    #     info = [item.strip() for item in section]
    #     info.pop(0)
    #     info.pop(-1)

    #     return info

    def delete_zeros_at_beginning(self, string):
        while string.startswith("0"):
            string = string[1:]
        return string

    def search_for_number(self, list_, line_entry, list_mode):
        for section in list_[:]:
            info = split_section(section, self.chosen_program)
            if self.chosen_program == "lama":
                if list_mode == "sage":
                    combobox_at = self.comboBox_at_sage.currentText()
                elif list_mode == "feedback":
                    combobox_at = self.comboBox_at_fb.currentText()

                if combobox_at == "Typ 1":
                    number = self.delete_zeros_at_beginning(info[2])
                if combobox_at == "Typ 2":
                    number = self.delete_zeros_at_beginning(info[0])

            elif self.chosen_program == "cria":
                number = self.delete_zeros_at_beginning(info[2])
            number = number.replace("i.","")
            if not number.startswith(line_entry):
                list_.remove(section)
        return list_

    def add_items_to_listwidget(
        self,
        list_beispieldaten_sections,
        beispieldaten_dateipfad,
        listWidget,
        listWidget_mode,
    ):
        for section in list_beispieldaten_sections:
            try:
                path = beispieldaten_dateipfad[section]
            except KeyError:
                drafts_path = os.path.join(path_programm, "Beispieleinreichung")
                beispieldaten_dateipfad_draft = search_files(drafts_path)
                path = beispieldaten_dateipfad_draft[section]

            name, extension = os.path.splitext(os.path.basename(path))
            item = QtWidgets.QListWidgetItem()

            # if "Beispieleinreichung" in path:
            #     item.setText(name + ' (Entwurf)')
            # elif "Lokaler_Ordner" in path:
            #     item.setText(name + ' (lokal)')
            # else:
            item.setText(name)

            if name.startswith("_L_"):
                if listWidget_mode == "feedback":
                    pass
                else:
                    # local_item_background_color = blue_4
                    # # local_item_background_color = blue_3
                    # item.setBackground(local_item_background_color)
                    item.setToolTip("lokal gespeichert")
                    listWidget.addItem(item)

            elif "Beispieleinreichung" in path:
                if listWidget_mode == "feedback":
                    pass
                else:
                    item.setBackground(blue_5)
                    item.setForeground(white)
                    item.setToolTip("Entwurf")
                    listWidget.addItem(item)

            elif re.search("\[.+\]", name) != None:
                # item.setForeground(QtGui.QColor(108, 159, 103))
                item.setToolTip("Variation")
                listWidget.addItem(item)
            else:
                listWidget.addItem(item)
            # item.setToolTip(path)

        listWidget.setFocusPolicy(QtCore.Qt.ClickFocus)

    def get_string_in_parantheses(self, string):
        kapitel = re.findall("\((..?.)\)", string)
        return kapitel[-1]

    def adjust_beispieldaten_combobox_lama(
        self, list_beispieldaten_sections, combobox_gk, combobox_gk_num
    ):
        if combobox_gk == "Zusatzthemen":
            if is_empty(combobox_gk_num) == True:
                for section in list_beispieldaten_sections[:]:
                    section_split = split_section(section, self.chosen_program)
                    thema = section_split[0]
                    if thema.lower() not in zusatzthemen_beschreibung:
                        list_beispieldaten_sections.remove(section)
            else:
                list_beispieldaten_sections = self.delete_item_without_string_from_list(
                    combobox_gk_num.upper(), list_beispieldaten_sections
                )

        elif is_empty(combobox_gk) == False:

            if is_empty(combobox_gk_num) == True:
                string = combobox_gk
            else:
                short_gk = shorten_gk(combobox_gk.lower() + combobox_gk_num)
                string = dict_gk[short_gk]

            list_beispieldaten_sections = self.delete_item_without_string_from_list(
                string, list_beispieldaten_sections
            )
        return list_beispieldaten_sections

    def adjust_beispieldaten_combobox_cria(
        self,
        list_beispieldaten_sections,
        combobox_klasse,
        combobox_kapitel,
        combobox_unterkapitel,
    ):
        klasse = "K" + combobox_klasse[0]
        for section in list_beispieldaten_sections[:]:
            info = split_section(section, self.chosen_program)
            if klasse not in info[0]:
                list_beispieldaten_sections.remove(section)

        if is_empty(combobox_kapitel) == False:
            kapitel = self.get_string_in_parantheses(combobox_kapitel)
            if is_empty(combobox_unterkapitel) == True:
                list_beispieldaten_sections = self.delete_item_without_string_from_list(
                    kapitel, list_beispieldaten_sections
                )
            else:
                unterkapitel = self.get_string_in_parantheses(combobox_unterkapitel)
                string = kapitel + "." + unterkapitel
                list_beispieldaten_sections = self.delete_item_without_string_from_list(
                    string, list_beispieldaten_sections
                )

        return list_beispieldaten_sections

    def adapt_choosing_list(self, list_mode):
        if list_mode == "sage":
            listWidget = self.listWidget
        if list_mode == "feedback":
            if self.chosen_program == "lama":
                listWidget = self.listWidget_fb
            elif self.chosen_program == "cria":
                listWidget = self.listWidget_fb_cria

            if self.comboBox_at_fb.currentText() == "Allgemeine Rückmeldung":
                self.comboBox_fb.clear()
                self.comboBox_fb_num.clear()
                self.lineEdit_number_fb.clear()
                listWidget.clear()
                return

        if self.chosen_program == "cria":
            typ = None
            beispieldaten_dateipfad = self.beispieldaten_dateipfad_cria
        else:
            if (
                self.comboBox_at_sage.currentText() == "Typ 1" and list_mode == "sage"
            ) or (
                self.comboBox_at_fb.currentText() == "Typ 1" and list_mode == "feedback"
            ):
                typ = 1
                beispieldaten_dateipfad = self.beispieldaten_dateipfad_1
            elif (
                self.comboBox_at_sage.currentText() == "Typ 2" and list_mode == "sage"
            ) or (
                self.comboBox_at_fb.currentText() == "Typ 2" and list_mode == "feedback"
            ):
                typ = 2
                beispieldaten_dateipfad = self.beispieldaten_dateipfad_2

        list_beispieldaten_sections = list(beispieldaten_dateipfad.keys())

        if self.chosen_program == "lama":
            if list_mode == "sage":
                combobox_gk = self.comboBox_gk.currentText()
                result = re.findall("\(([a-z]+)\)", self.comboBox_gk_num.currentText())
                if not is_empty(result):
                    combobox_gk_num = result[-1]
                else:
                    combobox_gk_num = self.comboBox_gk_num.currentText()

            elif list_mode == "feedback":
                combobox_gk = self.comboBox_fb.currentText()
                result = re.findall("\(([a-z]+)\)", self.comboBox_fb_num.currentText())
                if not is_empty(result):
                    combobox_gk_num = result[-1]
                else:
                    combobox_gk_num = self.comboBox_fb_num.currentText()

                # combobox_gk = self.comboBox_fb.currentText()
                # combobox_gk_num = self.comboBox_fb_num.currentText()

            list_beispieldaten_sections = self.adjust_beispieldaten_combobox_lama(
                list_beispieldaten_sections, combobox_gk, combobox_gk_num,
            )

        if self.chosen_program == "cria":
            if list_mode == "sage":
                combobox_klasse = self.comboBox_klassen.currentText()
                combobox_kapitel = self.comboBox_kapitel.currentText()
                combobox_unterkapitel = self.comboBox_unterkapitel.currentText()
            elif list_mode == "feedback":
                combobox_klasse = self.comboBox_klassen_fb_cria.currentText()
                combobox_kapitel = self.comboBox_kapitel_fb_cria.currentText()
                combobox_unterkapitel = self.comboBox_unterkapitel_fb_cria.currentText()

            list_beispieldaten_sections = self.adjust_beispieldaten_combobox_cria(
                list_beispieldaten_sections,
                combobox_klasse,
                combobox_kapitel,
                combobox_unterkapitel,
            )

        if list_mode == "sage":
            line_entry = self.lineEdit_number.text()
        elif list_mode == "feedback":
            if self.chosen_program == "lama":
                line_entry = self.lineEdit_number_fb.text()
            elif self.chosen_program == "cria":
                line_entry = self.lineEdit_number_fb_cria.text()

        if is_empty(line_entry) == False:
            list_beispieldaten_sections = self.search_for_number(
                list_beispieldaten_sections, line_entry, list_mode
            )

        list_beispieldaten_sections = sorted_gks(
            list_beispieldaten_sections, self.chosen_program
        )

        listWidget.clear()

        self.add_items_to_listwidget(
            list_beispieldaten_sections, beispieldaten_dateipfad, listWidget, list_mode
        )

    def collect_all_infos_for_creating_file(self):
        self.dict_all_infos_for_file = {}

        self.dict_all_infos_for_file[
            "list_alle_aufgaben"
        ] = self.list_alle_aufgaben_sage

        self.dict_all_infos_for_file[
            "dict_alle_aufgaben"
        ] = self.dict_alle_aufgaben_sage

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
            "copy_images": self.list_copy_images,
        }

        self.dict_all_infos_for_file["data_gesamt"] = dict_data_gesamt

    def get_dict_gesammeltedateien(self):
        dict_gesammeltedateien = {}

        if self.chosen_program == "lama":
            for aufgabe in self.list_alle_aufgaben_sage:
                typ = self.get_aufgabentyp(aufgabe)
                if typ == 1:
                    beispieldaten_dateipfad = self.beispieldaten_dateipfad_1
                elif typ == 2:
                    beispieldaten_dateipfad = self.beispieldaten_dateipfad_2

                for path in beispieldaten_dateipfad.values():
                    name = self.get_name_from_path(path)

                    if aufgabe == name:
                        dict_gesammeltedateien[aufgabe] = path
                        break

        if self.chosen_program == "cria":
            beispieldaten_dateipfad = self.beispieldaten_dateipfad_cria

            for item in self.list_alle_aufgaben_sage:
                klasse, aufgabe = self.split_klasse_aufgabe(item)
                for path in beispieldaten_dateipfad.values():
                    name = self.get_name_from_path(path)
                    if (klasse in path) and (aufgabe == name):
                        dict_gesammeltedateien[aufgabe] = path

        return dict_gesammeltedateien

    def add_content_to_tex_file(
        self, aufgabe, split_content, filename_vorschau, first_typ2
    ):
        if self.get_aufgabentyp(aufgabe) == 1:
            gk = aufgabe.replace("_L_", "")
            grundkompetenz = "[" + gk.split("-")[0].strip() + "]"
        else:
            grundkompetenz = ""

        path_aufgabe = self.get_dateipfad_aufgabe(aufgabe)

        spinbox_pkt = self.dict_alle_aufgaben_sage[aufgabe][0]

        if self.get_aufgabentyp(aufgabe) == 2:
            if first_typ2 == False:
                start = "\\newpage \n\n\subsubsection{Typ 2 Aufgaben}\n\n"
                first_typ2 = True
            else:
                start = "\\newpage\n\n"
        else:
            start = ""

        if spinbox_pkt == 0:
            split_content[0] = "\\begin{enumerate}\item[\\stepcounter{number}\\thenumber.] "
            split_content[-1] = "\end{enumerate}"

        elif "langesbeispiel" in split_content[0]:
            split_content[
                0
            ] = "{0}\\begin{{langesbeispiel}} \item[{1}] %PUNKTE DES BEISPIELS".format(
                start, spinbox_pkt
            )

        elif "beispiel" in split_content[0]:
            split_content[
                0
            ] = "{0}\\begin{{beispiel}}{1}{{{2}}} %PUNKTE DES BEISPIELS\n".format(
                start, grundkompetenz, spinbox_pkt
            )

        spinbox_abstand = self.dict_alle_aufgaben_sage[aufgabe][1]
        if spinbox_abstand != 0:
            if spinbox_abstand == 99:
                split_content[2] = split_content[2] + "\\newpage \n\n"
            else:
                split_content[2] = split_content[2] + "\\vspace{{{0}cm}} \n\n".format(
                    spinbox_abstand
                )

        with open(filename_vorschau, "a+", encoding="utf8") as vorschau:
            for all in split_content:
                vorschau.write(all + "\n")
            vorschau.write("\n\n")

        return first_typ2

    def pushButton_vorschau_pressed(
        self, ausgabetyp, index=0, maximum=0, pdf=True, lama=True
    ):
        self.collect_all_infos_for_creating_file()

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        dict_gesammeltedateien = self.get_dict_gesammeltedateien()

        if ausgabetyp == "vorschau":
            filename_vorschau = os.path.join(
                path_programm, "Teildokument", "Schularbeit_Vorschau.tex"
            )
        if ausgabetyp == "schularbeit":
            dict_umlaute = {
                "Ä": "AE",
                "ä": "ae",
                "Ö": "OE",
                "ö": "oe",
                "Ü": "ue",
                "ü": "ue",
                "ß": "ss",
            }
            if index == 0:

                # self.saved_file_path=path_programm

                self.chosen_path_schularbeit_erstellen = QtWidgets.QFileDialog.getSaveFileName(
                    None,
                    "Speicherort wählen",
                    os.path.dirname(self.saved_file_path),
                    "TeX Dateien (*.tex);; Alle Dateien (*.*)",
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

                if lama == True:
                    Ui_MainWindow.sage_save(self, filename_vorschau)  #

            else:
                dirname = os.path.dirname(self.chosen_path_schularbeit_erstellen[0])
                filename = os.path.basename(self.chosen_path_schularbeit_erstellen[0])
                for character in dict_umlaute.keys():
                    if character in filename:
                        filename = filename.replace(character, dict_umlaute[character])
                filename_vorschau = os.path.join(dirname, filename)

                # filename_vorschau=self.chosen_path_schularbeit_erstellen[0]

        self.dict_gruppen = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F"}

        if filename_vorschau == "":
            QtWidgets.QApplication.restoreOverrideCursor()
            return

        if self.chosen_program == "lama":
            dict_titlepage = self.dict_titlepage
        if self.chosen_program == "cria":
            dict_titlepage = self.dict_titlepage_cria

        if self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"] == "Quiz":
            documentclass = "\documentclass[18pt]{beamer}\n\n"
            geometry = (
                "\let\oldframe\\frame"
                "\\renewcommand\\frame[1][allowframebreaks, c]{\oldframe[#1]}\n"
                "\\usetheme{Boadilla}\n"
                "\\usecolortheme{seahorse}\n"
                "\date{}\n"
            )
            spacing = ""
        else:
            documentclass = "\documentclass[a4paper,12pt]{report}\n\n"
            geometry = (
                "\geometry{a4paper,left=18mm,right=18mm, top=2cm, bottom=2cm}\n\n"
            )
            spacing = "\onehalfspacing %Zeilenabstand\n"

        dict_vorschau = {}
        if (ausgabetyp == "vorschau" and self.cb_solution_sage.isChecked() == True) or (
            ausgabetyp == "schularbeit" and index % 2 == 0
        ):
            dict_vorschau["solution"] = "on"
        else:
            dict_vorschau["solution"] = "off"

        dict_vorschau["index"] = int(index / 2)

        # if maximum > 2:
        #     dict_vorschau["comment"] = " %Gruppen: 0=A, 1=B, 2=C, ..."
        # else:
        #     dict_vorschau["comment"] = ""

        dict_vorschau["pagestyle"] = "plain"
        # if ausgabetyp == "vorschau" or ausgabetyp == "schularbeit":
        #     dict_vorschau["pagestyle"] = "plain"
        # else:
        #     dict_vorschau["pagestyle"] = "empty"

        dict_vorschau["titlepage"] = get_titlepage_vorschau(
            self, dict_titlepage, ausgabetyp, maximum, index
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

        vorschau = open(filename_vorschau, "w+", encoding="utf8")

        vorschau.write(
            "{0}"
            "\\usepackage{{geometry}}\n"
            "{1}"
            # "\documentclass[a4paper,12pt]{{report}}\n\n" #documentclass
            # "\geometry{{a4paper,left=18mm,right=18mm, top=2cm, bottom=2cm}}\n\n"
            "\\usepackage{{lmodern}}\n"
            "\\usepackage[T1]{{fontenc}}\n"
            "\\usepackage[utf8]{{inputenc}}\n"
            "\\usepackage[ngerman]{{babel}}\n"
            "\\usepackage[solution_{2}, random={3}]{{srdp-mathematik}} % solution_on/off, random=0,1,2,...\n\n"
            # "\setcounter{{Zufall}}{{{3}}}\n\n\n"
            "\pagestyle{{{4}}} %PAGESTYLE: empty, plain\n"
            "{5}"  # "\onehalfspacing %Zeilenabstand\n"
            "\setcounter{{secnumdepth}}{{-1}} % keine Nummerierung der Ueberschriften\n\n\n\n"
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
            "%%%%%%%%%%%%%%%%%% DOKUMENT - ANFANG %%%%%%%%%%%%%%%%%%\n"
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n"
            "\\begin{{document}}\n"
            "{6}"
            "{7}".format(
                documentclass,
                geometry,
                dict_vorschau["solution"],
                dict_vorschau["index"],
                # dict_vorschau["comment"],
                dict_vorschau["pagestyle"],
                spacing,
                dict_vorschau["titlepage"],
                header,
            )
        )

        vorschau.close()

        first_typ2 = False
        aufgaben_nummer = 1
        for aufgabe in self.list_alle_aufgaben_sage:
            content = edit_content_vorschau(self, aufgabe, ausgabetyp)

            split_content = split_content_at_beispiel_umgebung(content)
            if split_content == False:
                text = "".join(content)
                critical_window(
                    'Es ist ein Fehler beim Erstellen der Datei aufgetreten, da die Formatierung der Aufgabe "{}" fehlerhaft ist.'.format(
                        aufgabe
                    ),
                    'Bitte überprüfen Sie die Formatierung der Aufgabe oder informieren Sie das LaMA-Team via "Feedback & Fehler".',
                    detailed_text='Fehlerhafter LaTeX-Aufgabentext:\n\n"""\n'
                    + text
                    + '\n"""',
                )
                QtWidgets.QApplication.restoreOverrideCursor()
                return

            if self.comboBox_pruefungstyp.currentText() == "Quiz":
                with open(filename_vorschau, "a+", encoding="utf8") as vorschau:
                    for i in range(2):
                        vorschau.write(
                            "\n\n\\setcounter{{Antworten}}{{{0}}}\n\n".format(i)
                        )
                        if i == 0:
                            vorschau.write(
                                "\\title{{Aufgabe {0}}}\maketitle\n\n".format(
                                    aufgaben_nummer
                                )
                            )
                            solution = False
                        elif i == 1:
                            vorschau.write(
                                "\\title{{\\textcolor{{red}}{{Aufgabe {0} (Lösung)}}}}\maketitle\n\n".format(
                                    aufgaben_nummer
                                )
                            )
                            solution = True

                        content = edit_content_quiz(split_content[1], solution)
                        vorschau.write(
                            "\\begin{frame}\n" + content + "\n\\end{frame}\n\n"
                        )
                        # vorschau.write("\n\n\\framebreak\n\n")
                aufgaben_nummer += 1
            else:
                first_typ2 = self.add_content_to_tex_file(
                    aufgabe, split_content, filename_vorschau, first_typ2
                )

        if (
            self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
            != "Grundkompetenzcheck"
            and self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
            != "Übungsblatt"
            and self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"] != "Quiz"
        ):
            if self.dict_all_infos_for_file["data_gesamt"]["Beurteilung"] == "ns":
                notenschluessel = self.dict_all_infos_for_file["data_gesamt"][
                    "Notenschluessel"
                ]

                with open(filename_vorschau, "a", encoding="utf8") as vorschau:
                    vorschau.write(
                        "\n\n\\null\\notenschluessel{{{0}}}{{{1}}}{{{2}}}{{{3}}}".format(
                            notenschluessel[0] / 100,
                            notenschluessel[1] / 100,
                            notenschluessel[2] / 100,
                            notenschluessel[3] / 100,
                        )
                    )

        with open(filename_vorschau, "a", encoding="utf8") as vorschau:
            vorschau.write("\n\n\end{document}")

        if ausgabetyp == "schularbeit":
            if dict_titlepage["logo"] == True:
                success = copy_logo_to_target_path(self, dict_titlepage["logo_path"])
                if success == False:
                    warning_window(
                        "Das Logo konnte nicht gefunden werden.",
                        "Bitte suchen Sie ein Logo unter: \n\nTitelblatt anpassen - Durchsuchen",
                        "Kein Logo ausgewählt",
                    )

            if (
                is_empty(self.dict_all_infos_for_file["data_gesamt"]["copy_images"])
                == False
            ):
                for image in self.dict_all_infos_for_file["data_gesamt"]["copy_images"]:
                    copy_included_images(self, image)

        if ausgabetyp == "vorschau":
            create_pdf("Schularbeit_Vorschau", 0, 0)

        if ausgabetyp == "schularbeit":
            name, extension = os.path.splitext(filename_vorschau)

            if pdf == True:
                create_pdf(name, index, maximum)

                temp_filename = name + ".pdf"

                # if maximum>2:
                #     if index%2==0:
                #         shutil.move(name+'.pdf', name+'_{}_Loesung.pdf'.format(self.dict_gruppen[int(index/2)]))
                #     else:
                #         shutil.move(name+'.pdf', name+'_{}.pdf'.format(self.dict_gruppen[int(index/2)]))
                # else:
                #     if index%2==0:
                #         shutil.move(name+'.pdf', name+'_Loesung.pdf')

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
                    with open(filename_vorschau, "r", encoding="utf8") as vorschau:
                        text = vorschau.read()

                    text = re.sub(
                        r"setcounter{Zufall}{.}", "setcounter{Zufall}{0}", text
                    )
                    text = re.sub(r"Large Gruppe .", "Large Gruppe A", text)

                    with open(filename_vorschau, "w", encoding="utf8") as vorschau:
                        vorschau.write(text)

        QtWidgets.QApplication.restoreOverrideCursor()

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
        if self.comboBox_at_fb.currentText() == "Allgemeine Rückmeldung" or self.comboBox_at_fb_cria.currentText()  == "Allgemeine Rückmeldung":
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
            print(gmail_password)
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
            server.login(gmail_user,gmail_password)
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
                text = "Bitte kontaktieren Sie den Support unter:\nlama.helpme@gmail.com"

            else:
                text = "Überprüfen Sie Ihre Internetverbindung oder kontaktieren Sie den Support für nähere Informationen unter:\nlama.helpme@gmail.com"

            critical_window(
                "Das Feedback konnte leider nicht gesendet werden!",
                text,
                "Fehler beim Senden",
                "Fehlermeldung:\n" + str(sys.exc_info()))


    #######################################################################
    ##########################################################################
    ############################################################################

    def pushButton_erstellen_pressed(self):
        self.collect_all_infos_for_creating_file()
        try:
            self.saved_file_path
        except AttributeError:
            self.saved_file_path = path_programm

        if self.chosen_program == "lama":
            dict_titlepage = self.dict_titlepage
        if self.chosen_program == "cria":
            dict_titlepage = self.dict_titlepage_cria

        self.open_dialogwindow_erstellen(
            # self.dict_all_infos_for_file,
            # self.chosen_program,
            # self.beispieldaten_dateipfad_1,
            # self.beispieldaten_dateipfad_2,
            # self.beispieldaten_dateipfad_cria,
            dict_titlepage,
            # self.saved_file_path,
        )

    def update_gui(self, chosen_gui):
        if self.chosen_program == "cria":
            chosen_gui = eval(chosen_gui + "_cria")
        else:
            chosen_gui = eval(chosen_gui)

        MainWindow.setMenuBar(self.menuBar)
        list_delete = []
        for item in list_widgets:
            if item != chosen_gui:
                list_delete += item
        for all in list_delete:
            if "action" in all:
                exec("self.%s.setVisible(False)" % all)
            elif "menu" in all:
                exec("self.menuBar.removeAction(self.%s.menuAction())" % all)
            else:
                exec("self.%s.hide()" % all)
        for all in chosen_gui:
            if "action" in all:
                exec("self.%s.setVisible(True)" % all)
            elif "menu" in all:
                exec("self.menuBar.addAction(self.%s.menuAction())" % all)
            else:
                exec("self.%s.show()" % all)

        if chosen_gui == widgets_search:
            if self.label_aufgabentyp.text()[-1] == str(1):
                self.combobox_searchtype.hide()
        # if chosen_type == str(2):
        #     self.label_aufgabentyp.setText(
        #         _translate("MainWindow", "Aufgabentyp: Typ 1", None)
        #     )
        #     self.groupBox_af.show()
        #     self.combobox_searchtype.hide()
        #     self.refresh_label_update()
        #     self.chosen_aufgabenformat_typ()
        if chosen_gui == widgets_sage or chosen_gui == widgets_sage_cria:
            MainWindow.setTabOrder(self.spinBox_nummer, self.dateEdit)
            MainWindow.setTabOrder(self.dateEdit, self.lineEdit_klasse)
            self.adapt_choosing_list("sage")
            # self.listWidget.itemClicked.connect(self.nummer_clicked)
        if chosen_gui == widgets_feedback or chosen_gui == widgets_feedback_cria:
            self.adapt_choosing_list("feedback")
            # self.listWidget_fb.itemClicked.connect(self.nummer_clicked_fb)
            # self.listWidget_fb_cria.itemClicked.connect(self.nummer_clicked_fb)


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
    palette_dark_mode.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))  # Window background
    palette_dark_mode.setColor(QtGui.QPalette.WindowText, white)
    palette_dark_mode.setColor(QtGui.QPalette.Text, white)
    palette_dark_mode.setColor(QtGui.QPalette.Base, dark_gray)
    palette_dark_mode.setColor(QtGui.QPalette.ToolTipBase, blue_7)
    palette_dark_mode.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    palette_dark_mode.setColor(QtGui.QPalette.ButtonText, white)
    palette_dark_mode.setColor(QtGui.QPalette.HighlightedText, white)
    palette_dark_mode.setColor(QtGui.QPalette.Highlight, blue_6)

    try: 
        with open(lama_settings_file, "r", encoding="utf8") as f:
            _dict = json.load(f)
        display_mode = _dict['display']
        if display_mode == 1:
            app.setPalette(palette_dark_mode)
        else:
            app.setPalette(palette)    
    except Exception:
            app.setPalette(palette)
    
    

    MainWindow = QMainWindow()
    # MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    screen_resolution = app.desktop().screenGeometry()
    screen_width, screen_height = screen_resolution.width(), screen_resolution.height()

    MainWindow.setGeometry(
        30, 30, round(screen_width * 0.5), round(screen_height * 0.8)
    )
    MainWindow.move(30, 30)

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()

    sys.exit(app.exec_())
