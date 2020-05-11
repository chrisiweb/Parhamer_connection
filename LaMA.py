#!/usr/bin/python3
# -*- coding: utf-8 -*-
#### Version number ###
__version__ = "v1.9.1"
__lastupdate__ = "04/20"
####################

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
import time
import threading
import sys
import os
from pathlib import Path
import datetime
from datetime import date
import json
import subprocess
import shutil
import re
import functools
from functools import partial
import yaml
from PIL import Image  ## pillow
import smtplib
# import qdarkstyle


from config import colors_ui, get_color,config_file, config_loader, path_programm, logo_path, logo_cria_path, SpinBox_noWheel, ClickLabel, bring_to_front, is_empty, shorten_gk
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
    list_widgets
)
from subwindows import Ui_Dialog_choose_type, Ui_Dialog_titlepage, Ui_Dialog_ausgleichspunkte, Ui_Dialog_erstellen, Ui_Dialog_speichern
from translate import _fromUtf8, _translate
from sort_items import natural_keys
from create_pdf import prepare_tex_for_pdf, create_pdf
from refresh_ddb import modification_date, refresh_ddb
from standard_dialog_windows import warning_window, question_window
from predefined_size_policy import *
from work_with_content import collect_content, split_aufgaben_content_new_format, split_aufgaben_content
 
# from cria_commands import create_kapitel_cria

try:
    loaded_lama_file_path = sys.argv[1]
except IndexError:
    loaded_lama_file_path = ""

black =colors_ui['black']
white = colors_ui['white']
gray = colors_ui['gray']
blue_1=colors_ui['blue_1']
blue_2=colors_ui['blue_2']
blue_3=colors_ui['blue_3'] 
blue_4=colors_ui['blue_4']  
blue_5=colors_ui['blue_5']
blue_6=colors_ui['blue_6']
blue_7=colors_ui['blue_7']
red= colors_ui['red']   

def get_color(color):
    color= "rgb({0}, {1}, {2})".format(color.red(), color.green(), color.blue())
    return color

StyleSheet_tabWiget = """
QTabBar::tab:selected {{
background: {0}; color: {1};
padding-right: 10px; padding-left: 10px;
border-top: 2px solid {3};
border-left: 2px solid {3};
border-right: 2px solid {3};
}}

QWidget {{color: {2};background-color: {3}}}
""".format(get_color(blue_2), get_color(black), get_color(white), get_color(blue_7))

StyleSheet_new_tab = """
color: {0};background-color: {1}
""".format(get_color(black), get_color(blue_2))


StyleSheet_typ2 = """
QGroupBox {{background-color: {0}; color: {1}}}
QLabel {{color:  {1}}}
""".format(get_color(blue_3), get_color(black))

## sizePolicy = QtWidgets.QSizePolicy( ######### Breite ############, ######### Höhe ############) 

print("Loading...")

### config_loader, path_programm, logo_path, SpinBox_noWheel



ag_beschreibung = config_loader(config_file, "ag_beschreibung")
an_beschreibung = config_loader(config_file, "an_beschreibung")
fa_beschreibung = config_loader(config_file, "fa_beschreibung")
ws_beschreibung = config_loader(config_file, "ws_beschreibung")
list_topics = [list(ag_beschreibung.keys()), list(an_beschreibung.keys()), list(fa_beschreibung.keys()), list(ws_beschreibung.keys())]

k5_beschreibung = config_loader(config_file, "k5_beschreibung")
k6_beschreibung = config_loader(config_file, "k6_beschreibung")
k7_beschreibung = config_loader(config_file, "k7_beschreibung")
k8_beschreibung = config_loader(config_file, "k8_beschreibung")

dict_gk = config_loader(config_file, "dict_gk")
Klassen = config_loader(config_file, "Klassen")
list_klassen = config_loader(config_file, "list_klassen")
dict_aufgabenformate = config_loader(config_file, "dict_aufgabenformate")



for klasse in list_klassen:
    exec('dict_{0} = config_loader(config_file,"dict_{0}")'.format(klasse))
    exec('dict_{0}_name = config_loader(config_file,"dict_{0}_name")'.format(klasse))

dict_unterkapitel = config_loader(config_file, "dict_unterkapitel")


dict_picture_path = {}



def create_file_titlepage(titlepage_save):
    if os.path.isfile(titlepage_save):
        with open(titlepage_save, encoding="utf8") as f:
            titlepage = json.load(f)
    else:
        titlepage = {
            "logo": False,
            "logo_path": False,
            "titel": True,
            "datum": True,
            "klasse": True,
            "name": True,
            "note": False,
            "unterschrift": False,
            "hide_all": False,
        }
    return titlepage

def simplify_string(string):
    string=string.replace(" ", "").replace(".", "").replace("-", "_")
    return string   


class Ui_MainWindow(object):
    global dict_picture_path#, set_chosen_gk #, list_sage_examples#, dict_alle_aufgaben_sage
    
    def __init__(self):
        self.dict_alle_aufgaben_sage = {}
        self.list_alle_aufgaben_sage = []
        self.dict_widget_variables = {}
        self.list_selected_topics_creator = []
        self.dict_variablen_punkte={}
        self.dict_variablen_label={}
        self.dict_sage_ausgleichspunkte_chosen = {}
        self.dict_sage_hide_show_items_chosen = {}
        self.dict_chosen_topics = {}
        self.list_creator_topics = []
        self.list_copy_images=[]
        

        titlepage_save = os.path.join(path_programm, "Teildokument", "titlepage_save")
        titlepage=create_file_titlepage(titlepage_save)
        self.dict_titlepage=titlepage

        titlepage_save = os.path.join(path_programm, "Teildokument", "titlepage_save_cria")
        titlepage=create_file_titlepage(titlepage_save)
        self.dict_titlepage_cria=titlepage

        app.aboutToQuit.connect(self.close_app)


    # def resizeEvent(self, event):
    #     print('resize')  
    #     QtGui.QMainWindow.resizeEvent(self, event)
        
    # def setupUi(self, MainWindow):
    #     self.check_for_update()
        
    def setupUi(self, MainWindow):
        self.check_for_update()

        ########## Dialog: Choose program ####    
        self.Dialog = QtWidgets.QDialog(
            None,
            QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint,
        )
        self.ui = Ui_Dialog_choose_type()
        self.ui.setupUi(self.Dialog)
        # self.Dialog.setWindowState(QtCore.Qt.WindowActive)
        # self.Dialog.isActiveWindow()
        bring_to_front(self.Dialog)
        # self.Dialog.setWindowFlags(self.Dialog.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        # self.Dialog.show()
        # self.Dialog.setWindowFlags(self.Dialog.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
        # self.Dialog.show()        
        self.Dialog.setFixedSize(self.Dialog.size())
        rsp=self.Dialog.exec_()

        if rsp == QtWidgets.QDialog.Accepted:
            self.chosen_program = self.ui.chosen_program
        if rsp == QtWidgets.QDialog.Rejected:
            sys.exit(0)

        ########################
        self.MainWindow = MainWindow
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        # MainWindow.resize(900, 500)
        # MainWindow.move(30,30)
        # MainWindow.setMaximumSize(QtCore.QSize(1078, 16777215))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        # MainWindow.setStyleSheet(_fromUtf8(""))
        # MainWindow.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        if self.chosen_program=='lama':
            MainWindow.setWindowTitle(
                _translate(
                    "LaMA - LaTeX Mathematik Assistent (Oberstufe)",
                    "LaMA - LaTeX Mathematik Assistent (Oberstufe)",
                    None,
                )
            )
            MainWindow.setWindowIcon(QtGui.QIcon(logo_path))
        if self.chosen_program=='cria':
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
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuBild_einbinden = QtWidgets.QMenu(self.menuBar)
        self.menuBild_einbinden.setObjectName(_fromUtf8("menuBild_einbinden"))
        MainWindow.setMenuBar(self.menuBar)
        self.actionReset = add_action(MainWindow, self.menuDatei, "Reset", self.suchfenster_reset)
        self.actionReset.setShortcut("F4")

        # self.actionReset_creator = add_action(self.menuDatei, "Reset", self.suchfenster_reset)
        # self.actionReset.setShortcut("F4")

        self.actionReset_sage = add_action(MainWindow,self.menuDatei, "Reset Schularbeit", self.reset_sage)
        self.actionReset_sage.setVisible(False)

        self.actionRefresh_Database = add_action(MainWindow,self.menuDatei, "Datenbank aktualisieren", partial(refresh_ddb, self))
        self.actionRefresh_Database.setShortcut("F5")

        self.menuDatei.addSeparator()

        self.actionLoad = add_action(MainWindow,self.menuDatei, "Öffnen", self.sage_load)
        self.actionLoad.setShortcut("Ctrl+O")
        self.actionSave = add_action(MainWindow,self.menuDatei, "Speichern", self.sage_save)
        self.actionSave.setShortcut("Ctrl+S")

        self.menuDatei.addSeparator()

        self.actionBild_konvertieren_jpg_eps = add_action(MainWindow,self.menuDatei, "Grafik konvertieren (jpg/png zu eps)", self.convert_imagetoeps)

        self.menuDatei.addSeparator()

        if self.chosen_program == 'lama':
            program='LaMA Cria (Unterstufe)'
        if self.chosen_program == 'cria':
            program='LaMA (Oberstufe)'
        self.actionProgram = add_action(MainWindow,self.menuDatei, 'Zu "{}" wechseln'.format(program), self.change_program)

        self.actionExit = add_action(MainWindow,self.menuDatei, "Exit", self.close_app)


        self.actionAufgaben_Typ1 = add_action(MainWindow,self.menuDateityp, "Typ1 Aufgaben", self.chosen_aufgabenformat_typ1)
        self.actionAufgaben_Typ1.setShortcut("Ctrl+1")

        self.actionAufgaben_Typ2 = add_action(MainWindow,self.menuDateityp, "Typ2 Aufgaben", self.chosen_aufgabenformat_typ2)
        self.actionAufgaben_Typ2.setShortcut("Ctrl+2") 

        self.actionSuche = add_action(MainWindow,self.menuSuche, "Aufgaben suchen...", partial(self.update_gui, 'widgets_search'))
        self.actionSuche.setShortcut("F1")

        self.actionSage = add_action(MainWindow,self.menuSage, "Neue Schularbeit erstellen...", partial(self.update_gui, 'widgets_sage'))
        self.actionSage.setShortcut("F2")

        self.actionNeu = add_action(MainWindow,self.menuNeu, "Neue Aufgabe erstellen...", partial(self.update_gui, 'widgets_create'))
        self.actionNeu.setShortcut("F3") 

        self.actionBild_einbinden = add_action(MainWindow,self.menuBild_einbinden, "Durchsuchen...", self.add_picture)

        self.actionFeedback = add_action(MainWindow,self.menuFeedback, "Feedback oder Fehler senden...", partial(self.update_gui, 'widgets_feedback'))

        self.actionInfo = add_action(MainWindow,self.menuHelp, "Über LaMA", self.show_info)      


        self.menuBar.addAction(self.menuDatei.menuAction())
        self.menuBar.addAction(self.menuDateityp.menuAction())
        self.menuBar.addAction(self.menuSage.menuAction())
        self.menuBar.addAction(self.menuNeu.menuAction())
        self.menuBar.addAction(self.menuFeedback.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())


        self.groupBox_ausgew_gk = create_new_groupbox(self.centralwidget, "Ausgewählte Grundkompetenzen")
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

        self.verticalLayout_scrollA_ausgew_gk = create_new_verticallayout(self.scrollAreaWidgetContents_ausgew_gk)
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

        self.gridLayout.addWidget(self.groupBox_ausgew_gk, 3, 1, 1, 1)


        self.groupBox_titelsuche = create_new_groupbox(self.centralwidget, "Titelsuche:")
        self.groupBox_titelsuche.setSizePolicy(SizePolicy_fixed_height)

        # self.groupBox_titelsuche = QtWidgets.QGroupBox(self.centralwidget)
        # self.groupBox_titelsuche.setObjectName(_fromUtf8("groupBox_titelsuche"))

        # self.groupBox_titelsuche.setMaximumHeight(65)

        self.gridLayout_10 = create_new_gridlayout(self.groupBox_titelsuche)
        # QtWidgets.QGridLayout(self.groupBox_titelsuche)
        # self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))


        self.entry_suchbegriffe = create_new_lineedit(self.groupBox_titelsuche)
        self.gridLayout_10.addWidget(self.entry_suchbegriffe, 0, 0, 1, 1)

        self.gridLayout.addWidget(self.groupBox_titelsuche, 4, 1, 1, 1, QtCore.Qt.AlignTop)


        self.groupBox_klassen = create_new_groupbox(self.centralwidget, "Themen Schulstufe")
        self.gridLayout_14 = create_new_gridlayout(self.groupBox_klassen)


        self.cb_k5 = create_new_checkbox(self.groupBox_klassen, "5. Klasse")
        self.gridLayout_14.addWidget(self.cb_k5, 0, 0, 1, 1)

        self.cb_k6 = create_new_checkbox(self.groupBox_klassen, "6. Klasse")
        self.gridLayout_14.addWidget(self.cb_k6, 1, 0, 1, 1)

        self.cb_k7 = create_new_checkbox(self.groupBox_klassen, "7. Klasse")
        self.gridLayout_14.addWidget(self.cb_k7, 0, 1, 1, 1)

        self.cb_k8 = create_new_checkbox(self.groupBox_klassen, "8. Klasse")
        self.gridLayout_14.addWidget(self.cb_k8, 1, 1, 1, 1)

        self.cb_matura = create_new_checkbox(self.groupBox_klassen, "Matura")
        self.gridLayout_14.addWidget(self.cb_matura, 0, 2, 1, 1)

        self.cb_univie = create_new_checkbox(self.groupBox_klassen, "Uni Wien")
        self.cb_univie.setToolTip(
        'Aufgaben mit dieser Kennzeichnung wurden im Rahmen einer Lehrveranstaltung auf der\nUniverstität Wien von Studiernden erstellt und von den Lehrveranstaltungsleitern evaluiert.'
        )
        self.gridLayout_14.addWidget(self.cb_univie, 1, 2, 1, 1)

        self.gridLayout.addWidget(self.groupBox_klassen, 3, 0, 1, 1)


        
        self.horizontalLayout_2 = create_new_horizontallayout()
        # QtWidgets.QHBoxLayout()
        # self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))

        self.cb_solution = create_new_checkbox(self.centralwidget, "Lösungen anzeigen", True)
        self.horizontalLayout_2.addWidget(self.cb_solution, QtCore.Qt.AlignLeft)

        self.cb_drafts = create_new_checkbox(self.centralwidget, "Entwürfe anzeigen")
        self.horizontalLayout_2.addWidget(self.cb_drafts)
        self.cb_drafts.toggled.connect(self.cb_drafts_enabled)

        self.btn_suche = create_new_button(self.centralwidget,"Suche starten", partial(prepare_tex_for_pdf,self))
        self.btn_suche.setShortcut(_translate("MainWindow", "Return", None))
        self.horizontalLayout_2.addWidget(self.btn_suche)

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

        self.label_aufgabentyp = create_new_label(self.centralwidget, "Aufgabentyp: Typ 1")
        self.horizontalLayout_combobox.addWidget(self.label_aufgabentyp)

        self.combobox_searchtype = create_new_combobox(self.centralwidget)
        self.combobox_searchtype.setMinimumContentsLength(1)

        add_new_option(self.combobox_searchtype, 0, "Alle Dateien ausgeben, die zumindest ein Suchkriterium enthalten")
        if self.chosen_program=='lama':
            label="Alle Dateien ausgeben, die ausschließlich diese Suchkriterien enthalten"
        if self.chosen_program=='cria':
            label= 'Alle Dateien ausgeben, die alle Suchkriterien enthalten'

        add_new_option(self.combobox_searchtype, 1, label)

        self.horizontalLayout_combobox.addWidget(self.combobox_searchtype)

        self.gridLayout.addLayout(self.horizontalLayout_combobox, 0, 1, 1, 1)
        self.combobox_searchtype.hide()


        self.groupBox_themen_klasse = create_new_groupbox(self.centralwidget, "Themen Schulstufen")

        self.verticalLayout = create_new_verticallayout(self.groupBox_themen_klasse) 
        # QtWidgets.QVBoxLayout(self.groupBox_themen_klasse)
        # self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tab_widget_themen = QtWidgets.QTabWidget(self.groupBox_themen_klasse)
        self.tab_widget_themen.setStyleSheet(StyleSheet_tabWiget)      
        # self.tabWidget.setStyleSheet(set_color_text(white))

        self.tab_widget_themen.setObjectName(_fromUtf8("tab_widget_themen"))
        self.verticalLayout.addWidget(self.tab_widget_themen)

        self.gridLayout.addWidget(self.groupBox_themen_klasse, 1, 0, 2, 1)

        self.groupBox_gk = create_new_groupbox(self.centralwidget, "Grundkompetenzen")

        self.gridLayout_11 = create_new_gridlayout(self.groupBox_gk)
        
        # QtWidgets.QGridLayout(self.groupBox_gk)
        # self.gridLayout_11.setObjectName(_fromUtf8("gridLayout_11"))
        self.tab_widget_gk = QtWidgets.QTabWidget(self.groupBox_gk)

        self.tab_widget_gk.setStyleSheet(StyleSheet_tabWiget)
        # self.tab_widget_gk.setStyleSheet(_fromUtf8("color: {0}".format(white)))
        # self.tab_widget_gk.setStyleSheet("QToolTip { color: white; background-color: rgb(47, 69, 80); border: 0px; }")
        # ))
        
            # 
        #  print(gray.red())
        self.tab_widget_gk.setObjectName(_fromUtf8("tab_widget_gk"))

        # #### AG #####
        self.create_tab_checkboxes_gk(self.tab_widget_gk, "Algebra und Geometrie", ag_beschreibung, 'search')

        ### FA ###
        self.create_tab_checkboxes_gk(self.tab_widget_gk,"Funktionale Abhängigkeiten", fa_beschreibung, 'search')

        ### AN ###
        self.create_tab_checkboxes_gk(self.tab_widget_gk,"Analysis", an_beschreibung, 'search')

        ### WS ###
        self.create_tab_checkboxes_gk(self.tab_widget_gk,"Wahrscheinlichkeit und Statistik", ws_beschreibung, 'search')
        
        ######### Klassenthemen
        ### K5
        self.create_tab_checkboxes_themen(self.tab_widget_themen, "k5", "search")

        ### K6
        self.create_tab_checkboxes_themen(self.tab_widget_themen, "k6", "search")

        ### K7
        self.create_tab_checkboxes_themen(self.tab_widget_themen, "k7", "search")

        ### K8
        self.create_tab_checkboxes_themen(self.tab_widget_themen, "k8", "search")

        #### Warnung ### Hinweis ####
        self.label_warnung = QtWidgets.QLabel(self.centralwidget)
        self.label_warnung.setWordWrap(True)
        self.label_warnung.setObjectName(_fromUtf8("label_warnung"))
        color=get_color(red)
        self.label_warnung.setStyleSheet(_fromUtf8("border: 2px solid {};".format(color))) #background-color: rgb(195, 58, 63)
        #self.label_warnung.setMaximumSize(QtCore.QSize(375, 16777215))
        self.label_warnung.setText(_translate("MainWindow", "Achtung: Aufgrund neuer hilfreicher Befehle ist es notwendig, ein Update des srdp-mathematik-Pakets so bald wie möglich durchzuführen! Nähere Infos unter: lama.schule/update", None))
        self.gridLayout.addWidget(self.label_warnung, 5,0,1,1)
        #########################

        ##################################################################
        ################ LAMA CRIA SEARCH #################################
        ###################################################################

        self.groupBox_schulstufe_cria = create_new_groupbox(self.centralwidget, "Themen Schulstufe")
        self.groupBox_schulstufe_cria.setMaximumSize(QtCore.QSize(450, 16777215))

        self.verticalLayout_cria = QtWidgets.QVBoxLayout(self.groupBox_schulstufe_cria)
        self.verticalLayout_cria.setObjectName("verticalLayout_cria")

        self.tabWidget_klassen_cria = QtWidgets.QTabWidget(self.groupBox_schulstufe_cria)
        self.tabWidget_klassen_cria.setStyleSheet(StyleSheet_tabWiget)

        self.tabWidget_klassen_cria.setMovable(False)
        self.tabWidget_klassen_cria.setObjectName("tabWidget_klassen_cria")
        # self.tabWidget_klassen_cria.setFocusPolicy(QtCore.Qt.NoFocus)


        # spacerItem_cria = QtWidgets.QSpacerItem(
        #     20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        # )
        for klasse in list_klassen:
            new_tab = add_new_tab(self.tabWidget_klassen_cria, "{}. Klasse".format(klasse[1]))
            new_tab.setStyleSheet(StyleSheet_new_tab)
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
                new_radiobutton = create_new_radiobutton(new_scrollareacontent, dict_klasse_name[kapitel] + " (" + kapitel + ")")
              
                new_verticallayout.addWidget(new_radiobutton)
                new_radiobutton.toggled.connect(
                    partial(self.chosen_radiobutton, klasse, kapitel)
                )
                group_radiobutton.addButton(new_radiobutton)
                label = 'radiobutton_kapitel_{0}_{1}'.format(klasse, kapitel)
                self.dict_widget_variables[label]=new_radiobutton


            new_verticallayout.addStretch()

            # new_verticallayout.addItem(spacerItem_cria)

            new_scrollarea.setWidget(new_scrollareacontent)

            new_gridlayout.addWidget(new_scrollarea, 5,0,1,1)

        self.groupBox_unterkapitel_cria = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_unterkapitel_cria.setObjectName("groupBox_unterkapitel_cria")
        self.groupBox_unterkapitel_cria.setTitle(_translate("MainWindow", "Unterkapitel",None))
        self.gridLayout_11_cria = QtWidgets.QGridLayout(self.groupBox_unterkapitel_cria)
        self.gridLayout_11_cria.setObjectName("gridLayout_11_cria")
        self.gridLayout.addWidget(self.groupBox_unterkapitel_cria, 1, 1, 2, 1)

        self.tabWidget_klassen_cria.currentChanged.connect(self.tabWidget_klassen_cria_changed)

        self.scrollArea_unterkapitel_cria = QtWidgets.QScrollArea(self.groupBox_unterkapitel_cria)
        self.scrollArea_unterkapitel_cria.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_unterkapitel_cria.setWidgetResizable(True)
        self.scrollArea_unterkapitel_cria.setObjectName("scrollArea_unterkapitel")
        self.scrollArea_unterkapitel_cria.setStyleSheet("background-color: {}".format(get_color(blue_2)))
        self.scrollAreaWidgetContents_cria = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_cria.setGeometry(QtCore.QRect(0, 0, 320, 279))
        self.scrollAreaWidgetContents_cria.setObjectName("scrollAreaWidgetContents_cria")
        self.verticalLayout_4_cria = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_cria)
        self.verticalLayout_4_cria.setObjectName("verticalLayout_4_cria")
        self.scrollArea_unterkapitel_cria.setWidget(self.scrollAreaWidgetContents_cria)
        self.gridLayout_11_cria.addWidget(self.scrollArea_unterkapitel_cria, 0, 0, 1, 1)

        self.label_unterkapitel_cria = create_new_label(self.scrollAreaWidgetContents_cria,"")
        self.label_unterkapitel_cria.setStyleSheet("padding-bottom: 15px")
        self.verticalLayout_4_cria.addWidget(self.label_unterkapitel_cria)

        self.create_all_checkboxes_unterkapitel()


        self.verticalLayout_cria.addWidget(self.tabWidget_klassen_cria)
        self.gridLayout.addWidget(self.groupBox_schulstufe_cria, 1, 0, 2, 1)
        self.groupBox_ausgew_themen_cria = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_ausgew_themen_cria.setObjectName("groupBox_ausgew_themen_cria")
        self.verticalLayout_2_cria = QtWidgets.QVBoxLayout(self.groupBox_ausgew_themen_cria)
        self.verticalLayout_2_cria.setObjectName("verticalLayout_2_cria")
        self.label_ausg_themen_cria = QtWidgets.QLabel(self.groupBox_ausgew_themen_cria)
        self.label_ausg_themen_cria.setWordWrap(False)
        self.label_ausg_themen_cria.setObjectName("label_ausg_themen_cria")
        self.label_ausg_themen_cria.setWordWrap(True)
        self.groupBox_ausgew_themen_cria.setTitle(_translate("MainWindow", "Ausgewählte Themen",None))
        self.groupBox_ausgew_themen_cria.hide()
        self.verticalLayout_2_cria.addWidget(self.label_ausg_themen_cria)
        self.gridLayout.addWidget(self.groupBox_ausgew_themen_cria, 3, 1, 1, 1)
        self.groupBox_schulstufe_cria.hide()
        self.groupBox_unterkapitel_cria.hide()

        dict_klasse_1 = eval("dict_{}_name".format(list_klassen[0]))
        erstes_kapitel = list(dict_klasse_1.keys())[0]
        self.dict_widget_variables['radiobutton_kapitel_{0}_{1}'.format(list_klassen[0], erstes_kapitel)].setChecked(True)

        ##############################################################
        ##################### CREATOR #########################################
        self.groupBox_aufgabentyp = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_aufgabentyp.setObjectName(_fromUtf8("groupBox_aufgabentyp"))
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_aufgabentyp)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
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

        self.tab_widget_gk_cr.setStyleSheet(StyleSheet_tabWiget)
        #     _fromUtf8("background-color: rgb(217, 255, 215);")
        # )
        self.tab_widget_gk_cr.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tab_widget_gk_cr.setObjectName(_fromUtf8("tab_widget_gk_cr"))
        self.gridLayout_11_cr.addWidget(self.tab_widget_gk_cr, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_grundkompetenzen_cr, 0, 0, 5, 1)
        self.groupBox_grundkompetenzen_cr.setTitle(
            _translate("MainWindow", "Grundkompetenzen", None)
        )
        self.groupBox_grundkompetenzen_cr.hide()

        self.groupBox_themengebiete_cria = QtWidgets.QGroupBox(self.centralwidget)

        self.groupBox_themengebiete_cria.setObjectName(
            _fromUtf8("groupBox_themengebiete_cria")
        )

        self.gridLayout_11_cr_cria = QtWidgets.QGridLayout(self.groupBox_themengebiete_cria)
        self.gridLayout_11_cr_cria.setObjectName(_fromUtf8("gridLayout_11_cr_cria"))
        self.tab_widget_cr_cria = QtWidgets.QTabWidget(self.groupBox_themengebiete_cria)
        # self.tab_widget_gk_cr.setStyleSheet(_fromUtf8("background-color: rgb(217, 255, 215);")
        self.tab_widget_cr_cria.setStyleSheet(StyleSheet_tabWiget)

        # self.tab_widget_cr_cria.setStyleSheet("background-color: rgb(229, 246, 255);")
        self.tab_widget_cr_cria.setObjectName(_fromUtf8("tab_widget_cr_cria"))
        self.tab_widget_cr_cria.setFocusPolicy(QtCore.Qt.NoFocus)
        self.gridLayout_11_cr_cria.addWidget(self.tab_widget_cr_cria, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_themengebiete_cria, 0, 0, 5, 1)
        self.groupBox_themengebiete_cria.setTitle(
            _translate("MainWindow", "Themengebiete",None)
        )
        self.groupBox_themengebiete_cria.hide()


        for klasse in list_klassen:
            name='tab_{0}'.format(klasse)
            new_tab = add_new_tab(self.tab_widget_cr_cria, "{}. Klasse".format(klasse[1]))
            new_tab.setStyleSheet(StyleSheet_new_tab)
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
            selection_background_color=get_color(blue_7)
            selection_text_color=get_color(white)
            combobox_kapitel.setStyleSheet("background-color: {0};selection-background-color: {1}; selection-color: {2}".format(get_color(white) , selection_background_color, selection_text_color))
            combobox_kapitel.setMinimumHeight(25)
            
            self.dict_widget_variables['combobox_kapitel_creator_cria_{}'.format(klasse)]=combobox_kapitel
            dict_klasse_name = eval('dict_{}_name'.format(klasse))
            index=0
            for kapitel in dict_klasse_name:
                add_new_option(combobox_kapitel,index,dict_klasse_name[kapitel] + " (" + kapitel + ")")
                index +=1
            combobox_kapitel.currentIndexChanged.connect(partial(self.comboBox_kapitel_changed_cr, new_scrollareacontent,new_verticallayout, klasse))

            new_verticallayout.addWidget(combobox_kapitel)


            dict_klasse = eval('dict_{}'.format(klasse))
            kapitel= list(dict_klasse.keys())[0]

            for unterkapitel in dict_klasse[kapitel]:
                new_checkbox=create_new_checkbox(new_scrollareacontent, dict_unterkapitel[unterkapitel] + ' (' + unterkapitel +')')
                new_checkbox.stateChanged.connect(partial(self.checkbox_unterkapitel_checked_creator_cria, new_checkbox, klasse, kapitel, unterkapitel))
                self.dict_widget_variables['checkbox_unterkapitel_creator_{0}_{1}_{2}'.format(klasse, kapitel, unterkapitel)]=new_checkbox
                new_verticallayout.addWidget(new_checkbox)
                new_checkbox.setFocusPolicy(QtCore.Qt.NoFocus)

            # new_verticallayout.addStretch()
            # new_verticallayout.addItem(self.spacerItem_unterkapitel_creator_cria)
            new_verticallayout.addStretch()

            new_scrollarea.setWidget(new_scrollareacontent)

            new_gridlayout.addWidget(new_scrollarea, 5,0,1,1)


# #################################


        self.groupBox_ausgew_gk_cr = create_new_groupbox(self.centralwidget, "Ausgewählte Grundkompetenzen")
        self.groupBox_ausgew_gk_cr.setSizePolicy(SizePolicy_fixed_height)
        self.groupBox_ausgew_gk_cr.setMaximumWidth(500)
        
        self.verticalLayout_2 = create_new_verticallayout(self.groupBox_ausgew_gk_cr)



        self.label_ausgew_gk_creator = create_new_label(self.groupBox_ausgew_gk_cr, "", True)

        self.verticalLayout_2.addWidget(self.label_ausgew_gk_creator)
        self.gridLayout.addWidget(self.groupBox_ausgew_gk_cr, 5, 0, 1, 1)

        # self.label_ausgew_gk.setText(_translate("MainWindow", "", None))
        self.groupBox_ausgew_gk_cr.hide()

        
        self.groupBox_bilder = create_new_groupbox(self.centralwidget, "Bilder (klicken, um Bilder zu entfernen)")
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
        self.gridLayout.addWidget(self.groupBox_bilder, 6, 0, 1, 1)
        self.groupBox_bilder.hide()

        #### CREATE CHECKBOXES ####
        ##### AG #####
        self.create_tab_checkboxes_gk(self.tab_widget_gk_cr, "Algebra und Geometrie", ag_beschreibung, 'creator')

        # # #### FA ####
        self.create_tab_checkboxes_gk(self.tab_widget_gk_cr, "Funktionale Abhängigkeiten", fa_beschreibung, 'creator')

        # ##### AN ####
        self.create_tab_checkboxes_gk(self.tab_widget_gk_cr, "Analysis", an_beschreibung, 'creator')

        # ### WS ####
        self.create_tab_checkboxes_gk(self.tab_widget_gk_cr, "Wahrscheinlichkeit und Statistik", ws_beschreibung, 'creator')

        # ### 5. Klasse ###
        self.create_tab_checkboxes_themen(self.tab_widget_gk_cr,"k5", "creator")

        # ### 6. Klasse ###
        self.create_tab_checkboxes_themen(self.tab_widget_gk_cr,"k6", "creator")

        # ### 7. Klasse ###
        self.create_tab_checkboxes_themen(self.tab_widget_gk_cr,"k7", "creator")

        # ### 8. Klasse ###
        self.create_tab_checkboxes_themen(self.tab_widget_gk_cr,"k8", "creator")

        # self.groupBox_aufgabentyp.setMaximumSize(100, 60)
        self.comboBox_aufgabentyp_cr = QtWidgets.QComboBox(self.groupBox_aufgabentyp)
        self.comboBox_aufgabentyp_cr.setObjectName(_fromUtf8("comboBox_aufgabentyp_cr"))
        self.comboBox_aufgabentyp_cr.setSizePolicy(SizePolicy_fixed)
        self.comboBox_aufgabentyp_cr.addItem(_fromUtf8(""))
        self.comboBox_aufgabentyp_cr.addItem(_fromUtf8(""))
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
        self.groupBox_punkte.setSizePolicy(SizePolicy_fixed_height)
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


        if self.chosen_program=='lama':
            self.gridLayout.addWidget(self.groupBox_punkte, 0, 2, 1, 1)
            self.gridLayout.addWidget(self.groupBox_aufgabenformat, 0, 3, 1, 1)
        if self.chosen_program=='cria':
            self.gridLayout.addWidget(self.groupBox_punkte, 0, 1, 1, 1)
            self.gridLayout.addWidget(self.groupBox_aufgabenformat, 0, 2, 1, 1)
        self.groupBox_aufgabenformat.setTitle(
            _translate("MainWindow", "Aufgabenformat", None)
        )



        i = 1
        for all in dict_aufgabenformate:
            add_new_option(self.comboBox_af, i, dict_aufgabenformate[all])
        
            if self.chosen_program=='lama' and i==4:
                break
            else:
                i+=1

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
        # self.groupBox_klassen_cr.setMaximumSize(100, 60)
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox_klassen_cr)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.comboBox_klassen_cr = QtWidgets.QComboBox(self.groupBox_klassen_cr)
        self.comboBox_klassen_cr.setObjectName(_fromUtf8("comboBox_klassen_cr"))
        self.comboBox_klassen_cr.addItem(_fromUtf8(""))
        self.comboBox_klassen_cr.addItem(_fromUtf8(""))
        self.comboBox_klassen_cr.addItem(_fromUtf8(""))
        self.comboBox_klassen_cr.addItem(_fromUtf8(""))
        self.comboBox_klassen_cr.addItem(_fromUtf8(""))
        self.comboBox_klassen_cr.addItem(_fromUtf8(""))
        self.gridLayout_8.addWidget(self.comboBox_klassen_cr, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_klassen_cr, 0, 4, 1, 1)
        self.groupBox_klassen_cr.setTitle(_translate("MainWindow", "Klasse", None))
        self.comboBox_klassen_cr.setItemText(0, _translate("MainWindow", "-", None))
        self.comboBox_klassen_cr.setItemText(
            1, _translate("MainWindow", "5. Klasse", None)
        )
        self.comboBox_klassen_cr.setItemText(
            2, _translate("MainWindow", "6. Klasse", None)
        )
        self.comboBox_klassen_cr.setItemText(
            3, _translate("MainWindow", "7. Klasse", None)
        )
        self.comboBox_klassen_cr.setItemText(
            4, _translate("MainWindow", "8. Klasse", None)
        )
        self.comboBox_klassen_cr.setItemText(
            5, _translate("MainWindow", "Matura", None)
        )
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
        self.gridLayout.addWidget(self.groupBox_beispieleingabe, 2, 1, 4, 5)
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
        self.gridLayout_18.addWidget(self.lineEdit_quelle, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_quelle, 6, 1, 1, 5, QtCore.Qt.AlignTop)
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
        self.gridLayout.addWidget(self.pushButton_save, 7, 5, 1, 1)
        self.pushButton_save.setText(_translate("MainWindow", "Speichern", None))
        # self.pushButton_save.setShortcut(_translate("MainWindow", "Return", None))
        self.pushButton_save.hide()

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
        list_comboBox_gk = ["", "AG", "FA", "AN", "WS", "K5", "K6", "K7", "K8"]
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
        self.comboBox_kapitel.currentIndexChanged.connect(
            partial(self.comboBox_kapitel_changed, "sage")
        )
        self.comboBox_kapitel.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.verticalLayout_sage.addWidget(self.comboBox_kapitel)

        self.comboBox_unterkapitel = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
        self.comboBox_unterkapitel.setObjectName("comboBox_unterkapitel")
        self.comboBox_unterkapitel.currentIndexChanged.connect(
            partial(self.comboBox_unterkapitel_changed, "sage")
        )
        self.comboBox_unterkapitel.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.verticalLayout_sage.addWidget(self.comboBox_unterkapitel)





        self.lineEdit_number = QtWidgets.QLineEdit(self.groupBox_alle_aufgaben)
        self.lineEdit_number.setObjectName("lineEdit_number")
        self.lineEdit_number.textChanged.connect(
            partial(self.lineEdit_number_changed, "sage")
        )
        self.verticalLayout_sage.addWidget(self.lineEdit_number)
        self.listWidget = QtWidgets.QListWidget(self.groupBox_alle_aufgaben)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_sage.addWidget(self.listWidget)
        #self.gridLayout.addWidget(self.groupBox_alle_aufgaben, 2, 0, 7, 1)

        self.groupBox_alle_aufgaben.setTitle(_translate("MainWindow", "Aufgaben", None))
        # print(self.groupBox_alle_aufgaben.height())
        # print(self.groupBox_alle_aufgaben.sizeHint())
        # print(self.groupBox_alle_aufgaben.minimumSizeHint())
        # self.groupBox_alle_aufgaben.setMinimumWidth(280)
        # self.groupBox_alle_aufgaben.resize(self.groupBox_alle_aufgaben.sizeHint())
        
        self.groupBox_alle_aufgaben.hide()

        self.groupBox_sage = QtWidgets.QGroupBox(self.splitter_sage)
        self.groupBox_sage.setMinimumWidth(1)
        self.groupBox_sage.setObjectName("groupBox_sage")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_sage)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.groupBox_sage.setTitle(
            _translate("MainWindow", "Schularbeitserstellung", None)
        )

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
        add_new_option(self.combobox_beurteilung, 0, 'Notenschlüssel')
        add_new_option(self.combobox_beurteilung, 1, 'Beurteilungsraster')
        self.combobox_beurteilung.currentIndexChanged.connect(self.notenanzeige_changed)
        # self.combobox_beurteilung.setMinimumContentsLength(1)
        self.gridLayout_5.addWidget(self.combobox_beurteilung, 1,4,1,2)


        self.pushButton_titlepage = QtWidgets.QPushButton(self.groupBox_sage)
        self.pushButton_titlepage.setObjectName(_fromUtf8("pushButton_titlepage"))
        self.pushButton_titlepage.setText(
            _translate("MainWindow", "Titelblatt anpassen", None)
        )
        if self.chosen_program=='lama':
            self.gridLayout_5.addWidget(self.pushButton_titlepage, 2, 4, 1, 2)
        if self.chosen_program=='cria':
            self.gridLayout_5.addWidget(self.pushButton_titlepage, 2, 4, 1, 2)
        

        self.groupBox_default_pkt = QtWidgets.QGroupBox(self.groupBox_sage)
        self.groupBox_default_pkt.setObjectName("groupBox_default_pkt")
        self.groupBox_default_pkt.setSizePolicy(SizePolicy_fixed_height)
        # self.groupBox_default_pkt.setMaximumSize(QtCore.QSize(120, 16777215))
        self.verticalLayout_default_pkt = QtWidgets.QVBoxLayout(
            self.groupBox_default_pkt
        )
        self.verticalLayout_default_pkt.setObjectName("verticalLayout_default_pkt")
        self.spinBox_default_pkt = SpinBox_noWheel(self.groupBox_default_pkt)
        self.spinBox_default_pkt.setValue(1)
        self.spinBox_default_pkt.setObjectName("spinBox_default_pkt")
        self.verticalLayout_default_pkt.addWidget(self.spinBox_default_pkt)
        self.spinBox_default_pkt.valueChanged.connect(self.update_default_pkt)
        self.gridLayout_5.addWidget(self.groupBox_default_pkt, 0, 3, 3, 1)

        self.groupBox_klasse = QtWidgets.QGroupBox(self.groupBox_sage)
        self.groupBox_klasse.setObjectName("groupBox_klasse")
        self.groupBox_klasse.setSizePolicy(SizePolicy_fixed_height)
        # self.groupBox_klasse.setMaximumSize(QtCore.QSize(200, 16777215))
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_klasse)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lineEdit_klasse = QtWidgets.QLineEdit(self.groupBox_klasse)
        self.lineEdit_klasse.setObjectName("lineEdit_klasse")
        self.verticalLayout_4.addWidget(self.lineEdit_klasse)
        self.gridLayout_5.addWidget(self.groupBox_klasse, 0, 2, 3, 1)
        # self.groupBox_klasse.setMaximumSize(QtCore.QSize(90, 16777215))
        self.groupBox_datum = QtWidgets.QGroupBox(self.groupBox_sage)
        self.groupBox_datum.setObjectName("groupBox_datum")
        self.groupBox_datum.setStyleSheet("padding-right: 10px")
        self.groupBox_datum.setSizePolicy(SizePolicy_fixed_height)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_datum)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.dateEdit = QtWidgets.QDateEdit(self.groupBox_datum)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit.setObjectName("dateEdit")
        self.verticalLayout_5.addWidget(self.dateEdit)
        self.gridLayout_5.addWidget(self.groupBox_datum, 0, 1, 3, 1)
        # self.groupBox_datum.setMaximumSize(QtCore.QSize(140, 16777215))
        self.groupBox_nummer = QtWidgets.QGroupBox(self.groupBox_sage)
        self.groupBox_nummer.setObjectName("groupBox_nummer")
        self.groupBox_nummer.setSizePolicy(SizePolicy_fixed_height)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_nummer)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.spinBox_nummer = QtWidgets.QSpinBox(self.groupBox_nummer)
        self.spinBox_nummer.setValue(1)
        self.spinBox_nummer.setObjectName("spinBox_nummer")
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
        self.scrollArea_chosen.verticalScrollBar().rangeChanged.connect(lambda: self.scrollArea_chosen.verticalScrollBar().setValue(self.scrollArea_chosen.verticalScrollBar().maximum()))
        self.gridLayout_5.addWidget(self.scrollArea_chosen, 5, 0, 1, 6)


        self.groupBox_notenschl = create_new_groupbox(self.groupBox_sage, "Notenschlüssel")
        # QtWidgets.QGroupBox(self.groupBox_sage)
        # self.groupBox_notenschl.setObjectName("groupBox_notenschl")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_notenschl)
        self.gridLayout_6.setObjectName("gridLayout_6")

        self.label_sg = create_new_label(self.groupBox_notenschl,"Sehr Gut:")
        self.label_sg.setSizePolicy(SizePolicy_fixed)
        self.gridLayout_6.addWidget(self.label_sg,0,0,1,1)
        self.spinBox_2 = create_new_spinbox(self.groupBox_notenschl, 91)
        self.spinBox_2.setSizePolicy(SizePolicy_fixed)
        self.spinBox_2.valueChanged.connect(self.update_punkte)
        self.gridLayout_6.addWidget(self.spinBox_2,0,1,1,1)
        self.label_sg_pkt = create_new_label(self.groupBox_notenschl, "% (ab 0)")
        self.gridLayout_6.addWidget(self.label_sg_pkt,0,2,1,1)


        self.label_g = create_new_label(self.groupBox_notenschl,"Gut:")
        self.label_g.setSizePolicy(SizePolicy_fixed)
        self.gridLayout_6.addWidget(self.label_g,0,3,1,1)
        self.spinBox_3 = create_new_spinbox(self.groupBox_notenschl, 80)
        self.spinBox_3.setSizePolicy(SizePolicy_fixed)
        self.spinBox_3.valueChanged.connect(self.update_punkte)
        self.gridLayout_6.addWidget(self.spinBox_3,0,4,1,1)
        self.label_g_pkt = create_new_label(self.groupBox_notenschl, "% (ab 0)")
        self.gridLayout_6.addWidget(self.label_g_pkt,0,5,1,1)


        self.label_b = create_new_label(self.groupBox_notenschl,"Befriedigend:")
        self.label_b.setSizePolicy(SizePolicy_fixed)
        self.gridLayout_6.addWidget(self.label_b,1,0,1,1)
        self.spinBox_4 = create_new_spinbox(self.groupBox_notenschl, 64)
        self.spinBox_4.setSizePolicy(SizePolicy_fixed)
        self.spinBox_4.valueChanged.connect(self.update_punkte)
        self.gridLayout_6.addWidget(self.spinBox_4,1,1,1,1)
        self.label_b_pkt = create_new_label(self.groupBox_notenschl, "% (ab 0)")
        self.gridLayout_6.addWidget(self.label_b_pkt,1,2,1,1)

        self.label_g_2 = create_new_label(self.groupBox_notenschl,"Genügend:")
        self.label_g_2.setSizePolicy(SizePolicy_fixed)
        self.gridLayout_6.addWidget(self.label_g_2,1,3,1,1)
        self.spinBox_5 = create_new_spinbox(self.groupBox_notenschl, 50)
        self.spinBox_5.setSizePolicy(SizePolicy_fixed)
        self.spinBox_5.valueChanged.connect(self.update_punkte)
        self.gridLayout_6.addWidget(self.spinBox_5,1,4,1,1)
        self.label_g_2_pkt = create_new_label(self.groupBox_notenschl, "% (ab 0)")
        self.gridLayout_6.addWidget(self.label_g_2_pkt,1,5,1,1)

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
        if self.chosen_program == 'lama':
            label = "Anzahl der Aufgaben: 0 (Typ1: 0 / Typ2: 0)"
            # self.label_gesamtbeispiele.setText(
            #     _translate(
            #         "MainWindow", "Anzahl der Aufgaben: 0\n(Typ1: 0 / Typ2: 0)", None
            #     )
            # )
        if self.chosen_program == 'cria':
            label = "Anzahl der Aufgaben: 0"
            # self.label_gesamtbeispiele.setText(
            #     _translate(
            #         "MainWindow",
            #         "Anzahl der Aufgaben: 0",None))


        self.label_gesamtbeispiele = create_new_label(self.groupBox_sage, label, True)
        # QtWidgets.QLabel(self.groupBox_sage)
        self.gridLayout_5.addWidget(self.label_gesamtbeispiele, 7, 0, 1, 3)
        # self.label_gesamtbeispiele.setObjectName("label_gesamtbeispiele")


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
        self.gridLayout_5.addWidget(
            self.cb_solution_sage, 7, 4, 1, 1)

        self.cb_drafts_sage = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_drafts_sage.setSizePolicy(SizePolicy_fixed)
        self.cb_drafts_sage.setObjectName(_fromUtf8("cb_drafts_sage"))
        self.gridLayout_5.addWidget(self.cb_drafts_sage, 8, 4, 1, 1)
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
            self.pushButton_vorschau, 7, 5, 1, 1, QtCore.Qt.AlignRight)
        self.pushButton_vorschau.clicked.connect(
            partial(self.pushButton_vorschau_pressed, "vorschau")
        )
        self.pushButton_vorschau.setFocusPolicy(QtCore.Qt.ClickFocus)
        # self.gridLayout.addWidget(self.groupBox_sage, 1, 2, 8, 3)
        self.gridLayout.addWidget(self.splitter_sage, 0, 0, 8, 2)
        self.pushButton_erstellen = QtWidgets.QPushButton(self.groupBox_sage)
        self.pushButton_erstellen.setSizePolicy(SizePolicy_fixed)
        self.pushButton_erstellen.setObjectName("pushButton_erstellen")
        self.pushButton_erstellen.setText(_translate("MainWindow", "Erstellen", None))
        self.pushButton_erstellen.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.pushButton_erstellen.clicked.connect(self.pushButton_erstellen_pressed)
        self.gridLayout_5.addWidget(
            self.pushButton_erstellen, 8, 5, 1, 1, QtCore.Qt.AlignRight
        )
        self.groupBox_sage.hide()
        self.splitter_sage.hide()
        self.comboBox_klassen_changed("sage")

        ################################################################
        ################################################################
        ########### FEEDBACK #############################################
        #######################################################################
        
        self.comboBox_at_fb = QtWidgets.QComboBox(self.centralwidget)
        # self.comboBox_at_fb.setSizePolicy(SizePolicy_fixed)
        self.comboBox_at_fb.setObjectName("comboBox_at_fb")
        self.comboBox_at_fb.addItem("")
        self.comboBox_at_fb.addItem("")
        self.comboBox_at_fb.addItem("")
        self.gridLayout.addWidget(self.comboBox_at_fb, 0, 0, 1, 1)
        self.comboBox_at_fb.setItemText(0, _translate("MainWindow", "Typ 1", None))
        self.comboBox_at_fb.setItemText(1, _translate("MainWindow", "Typ 2", None))
        self.comboBox_at_fb.setItemText(
            2, _translate("MainWindow", "Allgemeine Rückmeldung", None)
        )
        self.comboBox_at_fb.currentIndexChanged.connect(self.comboBox_at_fb_changed)
        self.comboBox_at_fb.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.comboBox_at_fb.hide()

        self.label_example = QtWidgets.QLabel(self.centralwidget)
        self.label_example.setObjectName(_fromUtf8("label_example"))
        # self.label_update.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label_example.setText(
            _translate("MainWindow", "Ausgewählte Aufgabe: -", None)
        )
        self.gridLayout.addWidget(self.label_example, 0, 1, 1, 1)
        self.label_example.hide()

        self.groupBox_alle_aufgaben_fb = QtWidgets.QGroupBox(self.centralwidget)
        # self.groupBox_alle_aufgaben_fb.setSizePolicy(SizePolicy_fixed_width)
        # self.groupBox_alle_aufgaben_fb.setMinimumSize(QtCore.QSize(140, 16777215))
        # self.groupBox_alle_aufgaben_fb.setMaximumSize(QtCore.QSize(180, 16777215))
        self.groupBox_alle_aufgaben_fb.setObjectName("groupBox_alle_aufgaben_fb")
        # self.groupBox_alle_aufgaben_fb.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        self.verticalLayout_fb = QtWidgets.QVBoxLayout(self.groupBox_alle_aufgaben_fb)
        self.verticalLayout_fb.setObjectName("verticalLayout_fb")
        self.comboBox_fb = QtWidgets.QComboBox(self.groupBox_alle_aufgaben_fb)
        self.comboBox_fb.setObjectName("comboBox_fb")
        list_comboBox_fb = ["", "AG", "FA", "AN", "WS", "K5", "K6", "K7", "K8"]
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
        self.listWidget_fb.setObjectName("listWidget")
        self.verticalLayout_fb.addWidget(self.listWidget_fb)
        self.gridLayout.addWidget(self.groupBox_alle_aufgaben_fb, 1, 0, 5, 1)
        self.groupBox_alle_aufgaben_fb.setTitle(
            _translate("MainWindow", "Aufgaben", None)
        )
        self.groupBox_alle_aufgaben_fb.hide()


        #### Feedback Cria ####

        self.groupBox_alle_aufgaben_fb_cria = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_alle_aufgaben_fb_cria.setMinimumWidth(100)
        # self.groupBox_alle_aufgaben_fb_cria.setMinimumSize(QtCore.QSize(140, 16777215))
        # self.groupBox_alle_aufgaben_fb_cria.setMaximumSize(QtCore.QSize(200, 16777215))
        self.groupBox_alle_aufgaben_fb_cria.setObjectName("groupBox_alle_aufgaben_fb_cria")
        self.verticalLayout_fb_cria = QtWidgets.QVBoxLayout(self.groupBox_alle_aufgaben_fb_cria)
        self.verticalLayout_fb_cria.setObjectName("verticalLayout_fb_cria")
        self.comboBox_klassen_fb_cria = QtWidgets.QComboBox(self.groupBox_alle_aufgaben_fb_cria)
        self.comboBox_klassen_fb_cria.setObjectName("self.comboBox_klassen_fb_cria")

        i = 0
        for all in list_klassen:

            self.comboBox_klassen_fb_cria.addItem("")

            self.comboBox_klassen_fb_cria.setItemText(
                i, _translate("MainWindow", all[1] + ". Klasse",None),
            )
            i += 1

        self.comboBox_klassen_fb_cria.currentIndexChanged.connect(
            partial(self.comboBox_klassen_changed, "feedback")
        )

        self.comboBox_klassen_fb_cria.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.verticalLayout_fb_cria.addWidget(self.comboBox_klassen_fb_cria)
        self.comboBox_kapitel_fb_cria = QtWidgets.QComboBox(self.groupBox_alle_aufgaben_fb_cria)
        self.comboBox_kapitel_fb_cria.setObjectName("self.comboBox_kapitel_fb_cria")

        self.comboBox_kapitel_fb_cria.currentIndexChanged.connect(
            partial(self.comboBox_kapitel_changed, "feedback")
        )
        self.comboBox_kapitel_fb_cria.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.verticalLayout_fb_cria.addWidget(self.comboBox_kapitel_fb_cria)


        self.comboBox_unterkapitel_fb_cria = QtWidgets.QComboBox(
            self.groupBox_alle_aufgaben_fb_cria
        )
        self.comboBox_unterkapitel_fb_cria.setObjectName("self.comboBox_unterkapitel_fb_cria")

        self.comboBox_unterkapitel_fb_cria.currentIndexChanged.connect(
            partial(self.comboBox_unterkapitel_changed, "feedback")
        )
        self.comboBox_unterkapitel_fb_cria.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.verticalLayout_fb_cria.addWidget(self.comboBox_unterkapitel_fb_cria)

        self.lineEdit_number_fb_cria = QtWidgets.QLineEdit(self.groupBox_alle_aufgaben_fb_cria)
        self.lineEdit_number_fb_cria.setObjectName("lineEdit_number_fb_cria")

        self.lineEdit_number_fb_cria.textChanged.connect(
            partial(self.adapt_choosing_list, "feedback")
        )
        self.verticalLayout_fb_cria.addWidget(self.lineEdit_number_fb_cria)
        self.listWidget_fb_cria= QtWidgets.QListWidget(self.groupBox_alle_aufgaben_fb_cria)
        self.listWidget_fb_cria.setObjectName("listWidget_fb_cria")
        self.verticalLayout_fb_cria.addWidget(self.listWidget_fb_cria)
        self.gridLayout.addWidget(self.groupBox_alle_aufgaben_fb_cria, 1, 0, 5, 1)
        self.groupBox_alle_aufgaben_fb_cria.setTitle(_translate("MainWindow", "Aufgaben",None))
        self.groupBox_alle_aufgaben_fb_cria.hide()

        self.comboBox_kapitel_fb_cria.addItem("")
        for all in dict_k1_name:
            self.comboBox_kapitel_fb_cria.addItem(
                dict_k1_name[all] + " (" + all + ")"
            )



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
        self.gridLayout.addWidget(self.groupBox_fehlertyp, 1, 1, 1, 3)
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
        self.gridLayout.addWidget(self.groupBox_feedback, 2, 1, 1, 3)
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
        self.gridLayout.addWidget(self.groupBox_email, 4, 1, 1, 3)
        self.groupBox_email.hide()

        self.pushButton_send = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_send.setObjectName(_fromUtf8("pushButton_send"))
        self.gridLayout.addWidget(
            self.pushButton_send, 5, 3, 1, 1, QtCore.Qt.AlignRight
        )
        self.pushButton_send.setText(_translate("MainWindow", "Senden", None))
        self.pushButton_send.clicked.connect(self.pushButton_send_pressed)
        self.pushButton_send.hide()

#         ####################################################################
#         #####################################################################
#         ######################################################################
#         #####################################################################

        self.gridLayout_11.addWidget(self.tab_widget_gk, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_gk, 1, 1, 2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)


        self.retranslateUi(MainWindow)
        self.tab_widget_themen.setCurrentIndex(0)

        self.tab_widget_gk_cr.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        print(self.MainWindow.geometry())

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
        self.menuNeu.setTitle(_translate("MainWindow", "Neue Aufgabe", None))
        self.menuSage.setTitle(_translate("MainWindow", "Neue Schularbeit", None))
        self.menuSuche.setTitle(_translate("MainWindow", "Aufgabensuche", None))
        self.menuBild_einbinden.setTitle(_translate("MainWindow", "Bild einfügen", None))
        self.menuFeedback.setTitle(_translate("MainWindow", "Feedback && Fehler", None))

        self.menuHelp.setTitle(_translate("MainWindow", "?", None))

        self.groupBox_titelsuche.setTitle(_translate("MainWindow", "Titelsuche:", None))
        self.groupBox_klassen.setTitle(_translate("MainWindow", "Suchfilter", None))

        self.cb_solution.setText(_translate("MainWindow", "Lösungen anzeigen", None))
        self.cb_drafts.setText(_translate("MainWindow", "Entwürfe anzeigen", None))

        try:
            if self.chosen_program=='lama':
                log_file = os.path.join(path_programm, "Teildokument", "log_file_1")
            if self.chosen_program=='cria':
                log_file = os.path.join(path_programm, "Teildokument", "log_file_cria")
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
        #self.groupBox_af.setMaximumSize(QtCore.QSize(375, 16777215))
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


        if self.chosen_program!='cria':
            self.cb_af_ko.hide()
            self.cb_af_rf.hide()
            self.cb_af_ta.hide()

        # self.gridLayout.addWidget(self.groupBox_af, 3, 0, 1, 1)
        if self.chosen_program=="lama":
            self.gridLayout.addWidget(self.groupBox_af, 4, 0, 1, 1)
        if self.chosen_program=='cria':
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
        self.cb_af_rf.setText(_translate("MainWindow", "Richtig/Falsch-Format (RF)",None))
        self.cb_af_ko.setText(_translate("MainWindow", "Konstruktion (KO)",None))
        self.cb_af_ta.setText(_translate("MainWindow", "Textaufgaben (TA)",None))
        #########################

        ### Typ1
        # self.combobox_searchtype.setItemText(1, _translate("MainWindow", "Alle Dateien ausgeben, die alle Suchkriterien enthalten", None))
        ######

        ### Typ2
        # self.combobox_searchtype.setItemText(
        #     1,
        #     _translate(
        #         "MainWindow",
        #         "Alle Dateien ausgeben, die ausschließlich diese Suchkriterien enthalten",
        #         None,
        #     ),
        # )
        ######

        self.groupBox_themen_klasse.setTitle(
            _translate("MainWindow", "Themen Schulstufe", None)
        )

        ############# Infos for GKs
        self.create_Tooltip(ag_beschreibung)
        self.create_Tooltip(fa_beschreibung)
        self.create_Tooltip(an_beschreibung)
        self.create_Tooltip(ws_beschreibung)
        #############################################

        if self.chosen_program == 'lama':
            program='LaMA Cria (Unterstufe)'
        if self.chosen_program == 'cria':
            program='LaMA (Oberstufe)'
        self.actionProgram.setText(_translate("MainWindow", 'Zu "{}" wechseln'.format(program), None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))

        print("Done")

        if self.chosen_program == 'cria':
            self.update_gui('widgets_search')



    def open_dialogwindow_erstellen(
        self,
        dict_all_infos_for_file,
        beispieldaten_dateipfad_1,
        beispieldaten_dateipfad_2,
        dict_titlepage,
        saved_file_path,
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
            # self,
            dict_all_infos_for_file,
            beispieldaten_dateipfad_1,
            beispieldaten_dateipfad_2,
            dict_titlepage,
            saved_file_path,
        )
        # self.Dialog.show()
        rsp= self.Dialog.exec_()

        if rsp == QtWidgets.QDialog.Accepted:
            for index in range(self.ui_erstellen.spinBox_sw_gruppen.value() * 2):
                self.pushButton_vorschau_pressed(
                    "schularbeit",
                    index,
                    self.ui_erstellen.spinBox_sw_gruppen.value() * 2,
                    self.ui_erstellen.pdf,
                    self.ui_erstellen.lama,
                )

            # MainWindow.show()

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
        if new_checkbox.isChecked()==False:
            new_checkbox.setChecked(True)
        else:
            new_checkbox.setChecked(False) 



    def create_checkboxes_themen(self,parent, layout, klasse, mode):
        if mode=='creator':       
            name_start='checkbox_creator_themen_{}_'.format(klasse)
        if mode=='search':
            name_start='checkbox_search_themen_{}_'.format(klasse)


        dict_klasse = eval('{}_beschreibung'.format(klasse))
        row=0

        for thema in dict_klasse:
            new_checkbox = create_new_checkbox(parent, "")
            new_checkbox.stateChanged.connect(partial(self.checkbox_checked, mode, 'themen'))
            new_checkbox.setSizePolicy(SizePolicy_fixed)
            name = name_start+thema
            self.dict_widget_variables[name]=new_checkbox
            layout.addWidget(new_checkbox, row,0,1,1)

            new_label = create_new_label(parent, dict_klasse[thema], True,True)
            new_label.clicked.connect(partial(self.click_label_to_check, new_checkbox))
            layout.addWidget(new_label, row, 1, 1, 1)

            row+=1

        return row


    def create_tab_checkboxes_themen(self, tab_widget ,klasse, mode):
        new_tab = add_new_tab(tab_widget, "{}. Klasse".format(klasse[1]))    #self.tab_widget_gk self.tab_widget_gk_cr
        new_tab.setStyleSheet(StyleSheet_new_tab)
        
        verticalLayout = create_new_verticallayout(new_tab)
        scrollarea = QtWidgets.QScrollArea(new_tab)
        scrollarea.setWidgetResizable(True)
        scrollarea.setObjectName("{}".format(scrollarea))

        scrollareacontent = QtWidgets.QWidget()
        scrollareacontent.setGeometry(QtCore.QRect(0, 0, 641, 252))
        scrollareacontent.setObjectName("{}".format(scrollareacontent))

        gridlayout_scrollarea = create_new_gridlayout(scrollareacontent)

        row=self.create_checkboxes_themen(scrollareacontent, gridlayout_scrollarea, klasse, mode)

        
        if mode=='search':
            dict_klasse = eval('{}_beschreibung'.format(klasse))
            button_check_all = create_new_button(scrollareacontent, "alle auswählen", partial(self.button_all_checkboxes_pressed,dict_klasse, 'themen', klasse))
            button_check_all.setStyleSheet("background-color: {}; ".format(get_color(blue_3)))
            button_check_all.setSizePolicy(SizePolicy_fixed)

        gridlayout_scrollarea.setRowStretch(row, 1)

        if mode=='search':
            gridlayout_scrollarea.addWidget(button_check_all, row+1, 0, 1,2)      

        scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
        scrollarea.setWidget(scrollareacontent)
        verticalLayout.addWidget(scrollarea)


    def create_tab_checkboxes_gk(self,tab_widget, titel, chosen_dictionary, mode):
        new_tab=add_new_tab(tab_widget, titel)    #self.tab_widget_gk self.tab_widget_gk_cr
        new_tab.setStyleSheet(StyleSheet_new_tab)
        # self.tab_ag = QtWidgets.QWidget()
        # self.tab_ag.setObjectName(_fromUtf8("tab_ag"))
        gridlayout=create_new_gridlayout(new_tab)
        # self.gridLayout_ag = QtWidgets.QGridLayout(self.tab_ag)
        # self.gridLayout_ag.setObjectName(_fromUtf8("gridLayout_ag"))
        scrollarea = QtWidgets.QScrollArea(new_tab)
        scrollarea.setWidgetResizable(True)
        scrollarea.setObjectName("{}".format(scrollarea))

        scrollareacontent = QtWidgets.QWidget(scrollarea)
        scrollareacontent.setGeometry(QtCore.QRect(0, 0, 641, 252))
        scrollareacontent.setObjectName("{}".format(scrollareacontent))
        gridLayout_scrollarea = create_new_gridlayout(scrollareacontent)    

          
      
        row, column = self.create_list_of_all_gk_checkboxes(scrollareacontent, gridLayout_scrollarea, mode, chosen_dictionary)


        if mode=='search':
            button_check_all = create_new_button(scrollarea, "alle auswählen", partial(self.button_all_checkboxes_pressed,chosen_dictionary, 'gk'))
            button_check_all.setStyleSheet("background-color: {}; ".format(get_color(blue_3)))
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
        if mode=='creator':       
        # if "cr" in gk_type:
            max_row = 10
            name_start='checkbox_creator_gk_'
        if mode=='search':
        # else:
            max_row = 9
            name_start='checkbox_search_gk_'
        for all in chosen_dictionary:
            new_checkbox = create_new_checkbox(parent, dict_gk[all])
            new_checkbox.setFocusPolicy(QtCore.Qt.NoFocus)
            background_color=get_color(blue_7)
            new_checkbox.setStyleSheet("""QToolTip {{ color: white; background-color: {}; border: 0px; }}       
            QCheckBox {{padding-right: 10px, padding-bottom: 10px}}
            """.format(background_color))
            layout.addWidget(new_checkbox, row, column, 1, 1)
            new_checkbox.stateChanged.connect(partial(self.checkbox_checked, mode, 'gk')) 
            name=name_start+all
            self.dict_widget_variables[name]=new_checkbox

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
        update_check.append(__version__)

        if update_check[0] != update_check[1]:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Question)
            msg.setWindowIcon(QtGui.QIcon(logo_path))
            msg.setText("Es ist ein neues Update vorhanden.")
            msg.setInformativeText("Möchten Sie das neue Update installieren?")
            msg.setWindowTitle("Update vorhanden")
            msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            buttonY = msg.button(QtWidgets.QMessageBox.Yes)
            buttonY.setText("Ja")
            buttonN = msg.button(QtWidgets.QMessageBox.No)
            buttonN.setText("Nein")
            ret = msg.exec_()

            if ret == QtWidgets.QMessageBox.Yes:
                opened_file = os.path.basename(sys.argv[0])
                name, extension = os.path.splitext(opened_file)
                if sys.platform.startswith("darwin"):
                    system_folder="update_mac"
                elif sys.platform.startswith("linux"):
                    system_folder="update_linux"
                else:
                    system_folder="update_windows"
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
            name='checkbox_search_gk_'+all
            self.dict_widget_variables[name].setToolTip(chosen_dict[all])
        for all in chosen_dict:
            name='checkbox_creator_gk_'+all
            self.dict_widget_variables[name].setToolTip(chosen_dict[all])



    def tabWidget_klassen_cria_changed(self):
        klasse =list_klassen[self.tabWidget_klassen_cria.currentIndex()]
    
        for all in self.dict_widget_variables:
            if all.startswith('radiobutton_kapitel_{}'.format(klasse)):
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
                    label='checkbox_unterkapitel_{0}_{1}_{2}'.format(alle_klassen, alle_kapitel, unterkapitel)
                    self.dict_widget_variables[label].hide()
                label_button_check_all = 'button_check_all_unterkapitel_{0}_{1}'.format(alle_klassen, alle_kapitel)
                self.dict_widget_variables[label_button_check_all].hide()
        # self.button_check_all_unterkapitel.hide()         

    def create_all_checkboxes_unterkapitel(self):
        for klasse in list_klassen:
            dict_klasse = eval("dict_{}".format(klasse))
            for kapitel in dict_klasse:
                for unterkapitel in dict_klasse[kapitel]:
                    checkbox = create_new_checkbox(self.scrollAreaWidgetContents_cria, dict_unterkapitel[unterkapitel])
                    checkbox.stateChanged.connect(partial(self.checkBox_checked_cria, klasse, kapitel, unterkapitel))
                    self.verticalLayout_4_cria.addWidget(checkbox)
                    checkbox.hide()
                    label='checkbox_unterkapitel_{0}_{1}_{2}'.format(klasse, kapitel, unterkapitel)
                    self.dict_widget_variables[label]=checkbox  #### creates widgets ???



        self.spacerItem_unterkapitel_cria = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )

        self.verticalLayout_4_cria.addItem(self.spacerItem_unterkapitel_cria)    

        for klasse in list_klassen:
            dict_klasse = eval("dict_{}".format(klasse))
            for kapitel in dict_klasse:
                button_check_all_unterkapitel = create_new_button(self.scrollAreaWidgetContents_cria, 'alle auswählen',None)
                # button_check_all_unterkapitel.setStyleSheet("background-color: rgb(240, 240, 240);")
                button_check_all_unterkapitel.clicked.connect(partial(self.btn_alle_unterkapitel_clicked_cria, klasse, kapitel))                  
                self.verticalLayout_4_cria.addWidget(button_check_all_unterkapitel, 0, QtCore.Qt.AlignLeft)
                button_check_all_unterkapitel.hide()
                label_button_check_all = 'button_check_all_unterkapitel_{0}_{1}'.format(klasse, kapitel)
                self.dict_widget_variables[label_button_check_all]=button_check_all_unterkapitel

        # self.button_check_all_unterkapitel = create_new_button(self.scrollAreaWidgetContents_cria, 'alle auswählen',None)
        # self.button_check_all_unterkapitel.setStyleSheet("background-color: rgb(240, 240, 240);")                  
        # self.verticalLayout_4_cria.addWidget(self.button_check_all_unterkapitel, 0, QtCore.Qt.AlignLeft)
        # self.button_check_all_unterkapitel.hide()                 

    def chosen_radiobutton(self, klasse, kapitel):
        dict_klasse = eval("dict_{}".format(klasse))
        dict_klasse_name = eval("dict_{}_name".format(klasse))

        self.label_unterkapitel_cria.setText(_translate(
                "MainWindow",
                klasse[1]
                + ". Klasse  - "
                + dict_klasse_name[kapitel],
                None
            ))        

        for alle_klassen in list_klassen:
            dict_klasse = eval("dict_{}".format(alle_klassen))
            for alle_kapitel in dict_klasse:
                for unterkapitel in dict_klasse[alle_kapitel]:
                    label='checkbox_unterkapitel_{0}_{1}_{2}'.format(alle_klassen, alle_kapitel, unterkapitel)
                    if alle_klassen==klasse and alle_kapitel==kapitel:
                        self.dict_widget_variables[label].show()
                    else:
                        self.dict_widget_variables[label].hide()  

        label_button_check_all = 'button_check_all_unterkapitel_{0}_{1}'.format(klasse, kapitel)
        for button in self.dict_widget_variables:
            if button.startswith('button_check_all_unterkapitel_'):
                if button != label_button_check_all:
                    self.dict_widget_variables[button].hide()
                else:
                    self.dict_widget_variables[label_button_check_all].show()



    def checkBox_checked_cria(self, klasse, kapitel, unterkapitel):      
        thema_checked = [klasse, kapitel, unterkapitel]
        thema_label = kapitel + "." + unterkapitel + " (" + klasse[1] + ".)"
        
        label_checkbox = 'checkbox_unterkapitel_{0}_{1}_{2}'.format(klasse, kapitel, unterkapitel)

        checkbox = self.dict_widget_variables[label_checkbox]
 
        if checkbox.isChecked() == True:
            if thema_label not in self.dict_chosen_topics.keys():
                self.dict_chosen_topics[thema_label] = thema_checked
        if checkbox.isChecked() == False:
            del self.dict_chosen_topics[thema_label]
        x = ", ".join(self.dict_chosen_topics.keys())
        # print(self.dict_chosen_topics)
        self.label_ausg_themen_cria.setText(_translate("MainWindow", x, None))


    def btn_alle_unterkapitel_clicked_cria(self, klasse, kapitel):
        dict_klasse = eval("dict_{}".format(klasse))

        first_checkbox= 'checkbox_unterkapitel_{0}_{1}_{2}'.format(klasse, kapitel, dict_klasse[kapitel][0])

        if self.dict_widget_variables[first_checkbox].isChecked()==False:
            check_checkboxes = True
        else:
            check_checkboxes = False
            

        for all in self.dict_widget_variables:
            if all.startswith('checkbox_unterkapitel_{0}_{1}_'.format(klasse, kapitel)):
                self.dict_widget_variables[all].setChecked(check_checkboxes)

 

    def comboBox_kapitel_changed_cr(self, parent, layout, klasse): # , verticalLayout_cr_cria, combobox_kapitel, klasse, spacerItem_unterkapitel_cria
        # layout.removeItem(self.spacerItem_unterkapitel_creator_cria)

        self.delete_all_widgets(layout,1)

        text_combobox=self.dict_widget_variables['combobox_kapitel_creator_cria_{}'.format(klasse)].currentText()
        kapitel=text_combobox[text_combobox.find("(")+1:text_combobox.find(")")]
        
        dict_klasse = eval("dict_{}".format(klasse))

        for unterkapitel in dict_klasse[kapitel]:
            if 'checkbox_unterkapitel_creator_{0}_{1}_{2}'.format(klasse, kapitel, unterkapitel) in self.dict_widget_variables:
                checkbox = self.dict_widget_variables['checkbox_unterkapitel_creator_{0}_{1}_{2}'.format(klasse, kapitel, unterkapitel)]
                layout.insertWidget(layout.count()-1, checkbox) 
            else:
                new_checkbox=create_new_checkbox(parent, dict_unterkapitel[unterkapitel])              
                new_checkbox.stateChanged.connect(partial(self.checkbox_unterkapitel_checked_creator_cria,new_checkbox, klasse, kapitel, unterkapitel))
                self.dict_widget_variables['checkbox_unterkapitel_creator_{0}_{1}_{2}'.format(klasse, kapitel, unterkapitel)]=new_checkbox
                new_checkbox.setFocusPolicy(QtCore.Qt.NoFocus)
                layout.insertWidget(layout.count()-1, new_checkbox)

        # layout.addStretch()
        # layout.addItem(self.spacerItem_unterkapitel_creator_cria)




    def checkbox_unterkapitel_checked_creator_cria(self, checkbox, klasse, kapitel, unterkapitel):
        thema_checked = [klasse, kapitel, unterkapitel]

        if checkbox.isChecked():
            if thema_checked not in self.list_creator_topics:
                self.list_creator_topics.append(thema_checked)
        if checkbox.isChecked() == False:
            self.list_creator_topics.remove(thema_checked)

        list_labels = []
        for all in self.list_creator_topics:
            thema_label = all[1] + "." + all[2] + " (" + all[0][1] + ".)"
            list_labels.append(thema_label)
        x = ", ".join(list_labels)
        self.label_ausgew_gk_creator.setText(_translate("MainWindow", x, None))


    def uncheck_all_checkboxes(self, typ):
        name='checkbox_search_{}_'.format(typ)
        name_creator='checkbox_creator_{}_'.format(typ)  


        for all in self.dict_widget_variables:
            if all.startswith(name) or all.startswith(name_creator):
                self.dict_widget_variables[all].setChecked(False)

       

    def suchfenster_reset(self):
        global dict_picture_path

        self.uncheck_all_checkboxes('gk')

        self.uncheck_all_checkboxes('themen')


        ### LaMA Cria      
        for klasse in list_klassen:
            self.dict_widget_variables['combobox_kapitel_creator_cria_{}'.format(klasse)].setCurrentIndex(0)

        for all in self.dict_widget_variables:
            if all.startswith('checkbox_unterkapitel_'):
                self.dict_widget_variables[all].setChecked(False)

        for klasse in list_klassen:
            for all in self.dict_widget_variables:
                if all.startswith('radiobutton_kapitel_{}'.format(klasse)):
                    self.dict_widget_variables[all].setChecked(True)
                    break


        klasse=list_klassen[self.tabWidget_klassen_cria.currentIndex()]
        dict_klasse = eval('dict_{}_name'.format(klasse))
        kapitel=list(dict_klasse.keys())[0]
        self.chosen_radiobutton(klasse, kapitel)
 
        self.entry_suchbegriffe.setText("")
        self.cb_solution.setChecked(True)
        self.spinBox_punkte.setProperty("value", 1)
        self.comboBox_aufgabentyp_cr.setCurrentIndex(0)
        self.comboBox_af.setCurrentIndex(0)
        self.comboBox_klassen_cr.setCurrentIndex(0)
        self.label_ausgew_gk_creator.setText(_translate("MainWindow", "", None))
        self.label_bild_leer.show()

        for i in range(len(dict_picture_path)):
            x = eval("self.label_bild_" + str(i))
            x.hide()
        dict_picture_path = {}
        if self.lineEdit_titel.text().startswith("###"):
            self.lineEdit_titel.setText(_translate("MainWindow", "###", None))
        else:
            self.lineEdit_titel.setText(_translate("MainWindow", "", None))
        self.lineEdit_quelle.setText(_translate("MainWindow", "", None))
        self.plainTextEdit.setPlainText(_translate("MainWindow", "", None))

    def reset_sage(self, program_changed=False):
        if program_changed==False:
            response=question_window('Schularbeit löschen?',
            'Sind Sie sicher, dass Sie das Fenster zurücksetzen wollen und die erstellte Schularbeit löschen möchten?')

            if response==False:
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
                "num_1": 0,
                "punkte_1": 0,
                "num_2": 0,
                "punkte_2": 0,
                "ausgleichspunkte": 0,
                "copy_images": [],
            },
        }

        self.list_alle_aufgaben_sage = []
        self.dict_alle_aufgaben_sage={}
        self.dict_variablen_label={}
        self.dict_variablen_punkte={}
        for i in reversed(range(self.gridLayout_8.count())):
            self.delete_widget(self.gridLayout_8, i)



    def change_program(self):
        if self.chosen_program=='lama':
            change_to = "LaMA Cria (Unterstufe)"
            program_name= "LaMA Cria - LaTeX Mathematik Assistent (Unterstufe)"
            icon = logo_cria_path
            
        elif self.chosen_program=='cria':
            change_to = "LaMA (Oberstufe)"
            program_name = "LaMA - LaTeX Mathematik Assistent (Oberstufe)"
            icon = logo_path


        response = question_window('Programm wechseln?',
        'Sind Sie sicher, dass sie zu {} wechseln wollen?\nDadurch werden alle bisherigen Einträge gelöscht!'.format(change_to))

        if response == False:
            return

        self.reset_sage(True)
        self.suchfenster_reset()
        self.reset_feedback()
        # self.comboBox_fehlertyp.setCurrentIndex(0)
        # self.plainTextEdit.setPlainText("")
        


        self.actionProgram.setText(_translate("MainWindow", 'Zu "{}" wechseln'.format(change_to), None))

        if self.chosen_program=='lama':
            self.chosen_program = 'cria'

            self.gridLayout.addWidget(self.groupBox_af, 3, 0, 1, 1)
            self.gridLayout.addWidget(self.groupBox_punkte, 0, 1, 1, 1)
            self.gridLayout.addWidget(self.groupBox_aufgabenformat, 0, 2, 1, 1)
            self.actionProgram.setText(_translate("MainWindow", 'Zu "LaMA (Oberstufe)" wechseln', None))
            self.cb_af_ko.show()
            self.cb_af_rf.show()
            self.cb_af_ta.show()
            self.combobox_searchtype.setItemText(1, _translate("MainWindow", "Alle Dateien ausgeben, die alle Suchkriterien enthalten", None))
            i=5
            for all in dict_aufgabenformate:
                if all == 'rf' or all == 'ta' or all=='ko':
                    add_new_option(self.comboBox_af, i, dict_aufgabenformate[all])
                    i+=1

            self.comboBox_klassen_changed("sage")
            
            self.label_gesamtbeispiele.setText(
                _translate(
                    "MainWindow",
                    "Anzahl der Aufgaben: 0",None))

        elif self.chosen_program=='cria':
            self.chosen_program = 'lama'

            self.gridLayout.addWidget(self.groupBox_af, 4, 0, 1, 1)
            self.gridLayout.addWidget(self.groupBox_punkte, 0, 2, 1, 1)
            self.gridLayout.addWidget(self.groupBox_aufgabenformat, 0, 3, 1, 1)
            self.combobox_searchtype.setItemText(1, _translate("MainWindow", "Alle Dateien ausgeben, die ausschließlich diese Suchkriterien enthalten", None))
            
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

        self.update_gui('widgets_search')



    def close_app(self):
        if self.list_alle_aufgaben_sage==[]:
            sys.exit(0)

        else:
            try:
                if os.path.isfile(self.saved_file_path)==True:
                    path=self.saved_file_path
                    loaded_file=self.load_file(path)
                    if loaded_file == self.dict_all_infos_for_file:
                        sys.exit(0)
            except AttributeError:
                pass

        


        response=question_window("Änderungen speichern?", "Möchten Sie die Änderungen speichern?")

        if response == True:
            self.sage_save()
        else:
            sys.exit(0)

    def show_info(self):
        QtWidgets.QApplication.restoreOverrideCursor()

        msg = QtWidgets.QMessageBox()

        pixmap = QtGui.QPixmap(logo_path)

        msg.setIconPixmap(pixmap.scaled(110, 110, QtCore.Qt.KeepAspectRatio))
        msg.setWindowIcon(QtGui.QIcon(logo_path))
        msg.setText(
            "LaMA - LaTeX Mathematik Assistent %s  \n\n"
            "Authors: Christoph Weberndorfer, Matthias Konzett\n\n"
            "License: GNU General Public License v3.0  \n\n"
            "Credits: David Fischer	" % __version__
        )
        msg.setInformativeText("Logo & Icon: Lisa Schultz")
        msg.setWindowTitle("Über LaMA - LaTeX Mathematik Assistent")
        # msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def get_logfile(self):
        try:
            x = "log_file_%s" % self.label_aufgabentyp.text()[-1]
            log_file = os.path.join(path_programm, "Teildokument", x)
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

    def chosen_aufgabenformat_typ1(self):
        self.label_aufgabentyp.setText(
            _translate("MainWindow", "Aufgabentyp: Typ 1", None)
        )
        self.groupBox_af.show()
        self.combobox_searchtype.hide()
        self.get_logfile()

    def chosen_aufgabenformat_typ2(self):
        self.label_aufgabentyp.setText(
            _translate("MainWindow", "Aufgabentyp: Typ 2", None)
        )
        self.groupBox_af.hide()
        self.combobox_searchtype.show()
        self.get_logfile()



    def button_all_checkboxes_pressed(self, chosen_dictionary, typ, klasse=None): 
        name_start='checkbox_search_{}_'.format(typ)
        if typ=='themen':
            name_start=name_start+klasse+'_'
        first_element=name_start+list(chosen_dictionary.keys())[0]

        if self.dict_widget_variables[first_element].isChecked() == False:
            for all in chosen_dictionary:
                name=name_start+all
                self.dict_widget_variables[name].setChecked(True)
        else:
            for all in chosen_dictionary:
                name=name_start+all
                self.dict_widget_variables[name].setChecked(False)           


    def checkbox_checked(self, mode, typ):
        chosen_gk = []
        chosen_themen = []
        self.list_selected_topics_creator=[]
        # set_chosen_gk = set([])
        name_checkbox='checkbox_{0}_'.format(mode)


        for widget in self.dict_widget_variables:
            if widget.startswith(name_checkbox):
                if self.dict_widget_variables[widget].isChecked()==True:
                    if 'gk' in widget:
                        # print(widget)
                        # widget.split('_'))
                        gk=widget.split('_')[-1]
                        chosen_gk.append(dict_gk[gk])
                        if mode == 'creator':
                            self.list_selected_topics_creator.append(dict_gk[gk])                        
                    if 'themen' in widget:
                        klasse = widget.split('_')[-2]
                        thema = widget.split('_')[-1]
                        if mode == 'creator':
                            self.list_selected_topics_creator.append(thema.upper() + " ("+ klasse[1]+ ".)")
                        # typ, klasse, thema = widget.split(name_checkbox)[1].split('_')
                        chosen_themen.append(thema.upper() + " ("+ klasse[1]+ ")")                   


        x = ", ".join(chosen_gk)
        if len(chosen_themen) > 6:
            y = ", ".join(sorted(chosen_themen)[:6])
            y = y + ", ..."
        else:
            y = ", ".join(sorted(chosen_themen))

        if mode=='search':
            if len(chosen_themen) > 0:
                y = "Weitere: " + y
            self.label_ausgew_gk.setText(_translate("MainWindow", str(x), None))
            self.label_ausgew_gk_rest.setText(_translate("MainWindow", str(y), None))
        if mode=='creator':
            if x=='':
                gesamt=y
            elif y=='':
                gesamt=x
            else:
                gesamt = x + ', ' + y
            self.label_ausgew_gk_creator.setText(_translate("MainWindow", str(gesamt), None))



    def comboBox_pruefungstyp_changed(self):
        if (
            self.comboBox_pruefungstyp.currentText() == "Grundkompetenzcheck"
            or self.comboBox_pruefungstyp.currentText() == "Übungsblatt"
        ):
            self.combobox_beurteilung.setEnabled(False)
            self.groupBox_notenschl.setEnabled(False)
            self.groupBox_beurteilungsraster.setEnabled(False)
            self.pushButton_titlepage.setEnabled(False)
        else:
            self.combobox_beurteilung.setEnabled(True)
            self.groupBox_notenschl.setEnabled(True)
            self.groupBox_beurteilungsraster.setEnabled(True)
            self.pushButton_titlepage.setEnabled(True)





    ############################################################################
    ############################################################################
    ########################### CREATE PDF ####################################
    ############################################################################

    def cb_drafts_enabled(self):
        if self.cb_drafts.isChecked():
            warning_window(
                "Entwürfe können Fehler enthalten, die das Programm zum Absturz bringen.",
                "Speichern Sie gegebenenfalls eine erstellte Schularbeit vor der Suche!",
                "Warnung - Here be dragons!",
            )

    def cb_drafts_sage_enabled(self):
        if self.cb_drafts_sage.isChecked():
            warning_window(
                "Entwürfe können Fehler enthalten, die das Programm zum Absturz bringen.",
                "Speichern Sie gegebenenfalls eine erstellte Schularbeit vor dem Erstellen!",
                "Warnung - Here be dragons!",
            )
        self.adapt_choosing_list("sage")


    ############# def prepare_tex_for_pdf #################


    #################################################################
    ###############################################################
    ################### Befehle Creator ###########################
    #############################################################


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
                name_of_image = "self.label_bild_" + str(i)

                label_picture = create_new_label(self.scrollAreaWidgetContents_bilder, tail, False, True)
                label_picture.clicked.connect(partial(self.del_picture, label_picture))
                self.verticalLayout.addWidget(label_picture)


    def del_picture(self, label_picture):
        del dict_picture_path[label_picture.text()]
        label_picture.hide()
        if len(dict_picture_path) == 0:
            self.label_bild_leer.show()

    def convert_imagetoeps(self):
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
                "Bilder (*.jpg; *.png)",
            )
            if filename[0] != []:
                self.saved_file_path = filename[0][0]
                for all in filename[0]:
                    # print(all)
                    name, ext = os.path.splitext(all)
                    if ext.lower() == ".jpg" or ext.lower() == ".jpeg":
                        output = str(name) + ".eps"
                        # output=all.replace('jpg','eps')
                        img = Image.open(str(all))
                        img.save(output)
                    elif ext.lower() == ".png":
                        output = str(name) + ".eps"
                        img = Image.open(str(all))
                        img = img.convert("RGB")
                        img.save(output)
                    else:
                        warning_window(
                            "Die Datei konnte nicht konvertiert werden."
                        )
                        return
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setWindowIcon(QtGui.QIcon(logo_path))
                if len(filename[0]) == 1:
                    msg.setText(
                        "Es wurde "
                        + str(len(filename[0]))
                        + " Datei erfolgreich konvertiert."
                    )
                else:
                    msg.setText(
                        "Es wurden "
                        + str(len(filename[0]))
                        + " Dateien erfolgreich konvertiert."
                    )

                msg.setWindowTitle("Grafik(en) konvertieren")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                ret = msg.exec_()
                return

    def chosen_aufgabenformat_cr(self):
        if self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
            self.label_keine_auswahl.hide()
            self.comboBox_af.show()
        if self.comboBox_aufgabentyp_cr.currentText() == "Typ 2":
            self.label_keine_auswahl.show()
            self.comboBox_af.hide()


     

    # def check_entry_creator(self):
    #     for all in lama_entry:
    #         structure =self.is_empty(all)
    #         if structure  == True:
    #             return idx

    def get_number_of_included_images(self):
        num = self.plainTextEdit.toPlainText().count("\includegraphics")
        return num

    def check_included_attached_image_ratio(self):
        included = self.get_number_of_included_images()
        attached = len(dict_picture_path)
        return included, attached
 

    def check_entry_creator(self):
        if self.chosen_program=='lama':
            if is_empty(self.list_selected_topics_creator)==True:
                return "Es wurden keine Grundkompetenzen zugewiesen."

            if self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
                if len(self.list_selected_topics_creator) > 1:
                    return "Es wurden zu viele Grundkompetenzen zugewiesen."

        if self.chosen_program=='cria' and is_empty(self.list_creator_topics)==True:
            return "Es wurden keine Themengebiete zugewiesen."

        if self.comboBox_aufgabentyp_cr.currentText() != "Typ 2" and self.comboBox_af.currentText() == "bitte auswählen":
            return "Es wurde kein Aufgabenformat ausgewählt."

        if is_empty(self.lineEdit_titel.text())==True:
            return "Bitte geben Sie einen Titel ein."

        if is_empty(self.plainTextEdit.toPlainText())==True:
            return 'Bitte geben Sie den LaTeX-Quelltext der Aufgabe im Bereich "Aufgabeneingabe" ein.'

        if is_empty(self.lineEdit_quelle.text())==True:
            return "Bitte geben Sie die Quelle an."

        included, attached = self.check_included_attached_image_ratio()
        if included != attached:
            if included > attached:
                str_='wenige'
            elif included < attached:
                str_='viele'
            warning = "Es sind zu {0} Bilder angehängt ({1}/{2})".format(str_, included, attached)    
            return warning
 

    def check_for_admin_mode(self):
        if self.lineEdit_titel.text().startswith("###"):
            _,titel = self.lineEdit_titel.text().split("###")
            titel = titel.strip()
            self.creator_mode = "admin"
        else:
            titel = self.lineEdit_titel.text().strip()
        return titel


    def open_dialogwindow_save(self, information):
        Dialog_speichern = QtWidgets.QDialog(            
        None,
        QtCore.Qt.WindowSystemMenuHint
        | QtCore.Qt.WindowTitleHint
        | QtCore.Qt.WindowCloseButtonHint,)
        self.ui_save = Ui_Dialog_speichern()
        self.ui_save.setupUi(Dialog_speichern, self.creator_mode)
        self.ui_save.label.setText(information)
        # self.ui_save.label.setStyleSheet("padding: 10px")
        return Dialog_speichern



    def button_speichern_pressed(self):
        self.creator_mode = "user"
        local_save = False

        ######## WARNINGS #####

        warning = self.check_entry_creator()
        if warning != None:
            warning_window(warning)
            return

        #######

        textBox_Entry = self.plainTextEdit.toPlainText()
        list_chosen_gk = self.list_selected_topics_creator


        ###### Check if Admin Mode is activated ####

        edit_titel = self.check_for_admin_mode()

        ################################################



        if self.chosen_program=='lama':
            themen = ', '.join(self.list_selected_topics_creator)

        if self.chosen_program =='cria':
            list_labels = []
            for all in self.list_creator_topics:
                thema_label = all[1] + "." + all[2] + " (" + all[0][1] + ".)"
                list_labels.append(thema_label)
            themen = ", ".join(list_labels)

        if dict_picture_path != {}:
            bilder = ", ".join(dict_picture_path)
            bilder = '\n\nBilder: {bilder}'
        else:
            bilder = ''


        if self.chosen_program=='cria' or self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
            aufgabenformat = "Aufgabenformat: %s\n\n" % self.comboBox_af.currentText()
        else:
            aufgabenformat = ""

        if self.chosen_program=='lama':
            aufgabentyp="Aufgabentyp: {0}\n\n".format(self.comboBox_aufgabentyp_cr.currentText())
            titel_themen =  'Grundkompetenz(en)'
        if self.chosen_program=='cria':
            aufgabentyp = ''
            titel_themen =  'Themengebiet(e)'

        
        information="{0}Titel: {1}\n\n{2}{3}: {4}\n\nQuelle: {5}{6}\n\n".format(
            aufgabentyp,
            edit_titel,
            aufgabenformat,
            titel_themen,
            themen,
            self.lineEdit_quelle.text(),
            bilder,
        )


        Dialog_speichern = self.open_dialogwindow_save(information)

        response = Dialog_speichern.exec()

        if response == 0:
            return

        confirmed=self.ui_save.get_output()

        if self.creator_mode == "user":
            local_save = False

            while confirmed == (True, False) or confirmed == (False, None):
                if confirmed == (True, False):
                    warning_window(
                        "Bitte bestätigen Sie die Eigenständigkeitserklärung und Lizenzvereinbarung."
                    )
                elif confirmed == (False, None):
                    local_save = question_window("Aufgabe lokal speichern?",
                    "Sind Sie sicher, dass Sie diese Aufgabe nur lokal speichern wollen?",
                    "ACHTUNG: Durch nicht überprüfte Aufgaben entstehen möglicherweise Fehler, die das Programm zum Absturz bringen können!",
                    )
                    if local_save == True:
                        break
              
                response = Dialog_speichern.exec()
                if response == 0:
                    return
                confirmed=self.ui_save.get_output() 

        print(confirmed)
        print(list_chosen_gk)
        for all in list_chosen_gk:        
            print(shorten_gk(all))

        return


        ##### GET MAX FILENUMBER IN DIR #####
        if self.chosen_program=='lama':
            if self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
                # print(set_chosen_gk)
                if list_chosen_gk[0] in {
                    **k5_beschreibung,
                    **k6_beschreibung,
                    **k7_beschreibung,
                    **k8_beschreibung,
                }:  ## merged dictionaries
                    if list_chosen_gk[0] in k5_beschreibung:
                        path_folder = "5.Klasse"
                    elif list_chosen_gk[0] in k6_beschreibung:
                        path_folder = "6.Klasse"
                    elif list_chosen_gk[0] in k7_beschreibung:
                        path_folder = "7.Klasse"
                    elif list_chosen_gk[0] in k8_beschreibung:
                        path_folder = "8.Klasse"

                    if self.creator_mode == "admin" and self.cb_save.isChecked() == True:
                        gk_path_temp = os.path.join(
                            path_programm,
                            "_database_inoffiziell",
                            "Typ1Aufgaben",
                            path_folder,
                            list_chosen_gk[0],
                            "Einzelbeispiele",
                        )

                    elif self.creator_mode == "user" and local_save == True:
                        gk_path_temp = os.path.join(
                            path_programm, "Lokaler_Ordner", "Typ1Aufgaben"
                        )

                    else:
                        gk_path_temp = os.path.join(
                            path_programm,
                            "_database",
                            "Typ1Aufgaben",
                            path_folder,
                            list_chosen_gk[0],
                            "Einzelbeispiele",
                        )

                    if local_save == True:
                        z = " - "
                    else:
                        z = list_chosen_gk[0].upper() + " - "

                else:
                    path_folder = "_Grundkompetenzen"
                    if self.creator_mode == "admin" and self.cb_save.isChecked() == True:
                        gk_path_temp = os.path.join(
                            path_programm,
                            "_database_inoffiziell",
                            "Typ1Aufgaben",
                            path_folder,
                            dict_gk[list_chosen_gk[0]][:2],
                            dict_gk[list_chosen_gk[0]],
                            "Einzelbeispiele",
                        )
                    elif self.creator_mode == "user" and local_save == True:
                        gk_path_temp = os.path.join(
                            path_programm, "Lokaler_Ordner", "Typ1Aufgaben"
                        )

                    else:
                        gk_path_temp = os.path.join(
                            path_programm,
                            "_database",
                            "Typ1Aufgaben",
                            path_folder,
                            dict_gk[list_chosen_gk[0]][:2],
                            dict_gk[list_chosen_gk[0]],
                            "Einzelbeispiele",
                        )
                    if local_save == True:
                        z = " - "
                    else:
                        z = dict_gk[list_chosen_gk[0]] + " - "

                if self.creator_mode == "admin" and self.cb_save.isChecked() == True:
                    max_integer_file = 1000
                else:
                    max_integer_file = 0

                if not os.path.exists(gk_path_temp):
                    print("Creating {} for you.".format(gk_path_temp))
                    os.makedirs(gk_path_temp)
                for all in os.listdir(gk_path_temp):
                    if all.endswith(".tex"):
                        x, y = all.split(z)
                        file_integer, file_extension = y.split(".tex")
                        if int(file_integer) > max_integer_file:
                            max_integer_file = int(file_integer)

                # print(max_integer_file)

            if self.comboBox_aufgabentyp_cr.currentText() == "Typ 2":
                if self.creator_mode == "admin" and self.cb_save.isChecked() == True:
                    gk_path_temp = os.path.join(
                        path_programm,
                        "_database_inoffiziell",
                        "Typ2Aufgaben",
                        "Einzelbeispiele",
                    )

                elif self.creator_mode == "user" and local_save == True:
                    gk_path_temp = os.path.join(
                        path_programm, "Lokaler_Ordner", "Typ2Aufgaben"
                    )

                else:
                    gk_path_temp = os.path.join(
                        path_programm, "_database", "Typ2Aufgaben", "Einzelbeispiele"
                    )
                max_integer_file = 0

                if not os.path.exists(gk_path_temp):
                    print("Creating {} for you.".format(gk_path_temp))
                    os.makedirs(gk_path_temp)
                for all in os.listdir(gk_path_temp):
                    if all.endswith(".tex"):
                        file_integer, file_extension = all.split(".tex")
                        file_integer = file_integer.replace("_L_", "")

                        if int(file_integer) > max_integer_file:
                            max_integer_file = int(file_integer)


        if self.chosen_program=='cria':
            highest_grade = 1
            for all in self.list_creator_topics:
                if int(all[0][1]) > highest_grade:
                    highest_grade = int(all[0][1])

            path_folder = "k" + str(highest_grade)

            if self.creator_mode == 'admin' and self.cb_save.isChecked()==True:
                max_integer_file = 1000
                klasse_path_temp = os.path.join(
                    path_programm, "_database_inoffiziell", path_folder, "Einzelbeispiele"
                )
            elif self.creator_mode == "user" and local_save == True:
                max_integer_file = 0
                klasse_path_temp = os.path.join(
                    path_programm, "Lokaler_Ordner", path_folder
                )
            else:
                max_integer_file = 0
                klasse_path_temp = os.path.join(
                    path_programm, "_database", path_folder, "Einzelbeispiele"
                )
            # print(klasse_path_temp)

            

            if not os.path.exists(klasse_path_temp):
                print("Creating {} for you.".format(klasse_path_temp))
                os.makedirs(klasse_path_temp)
            for all in os.listdir(klasse_path_temp):
                if all.endswith(".tex"):
                    if local_save == True:
                        filename=all.replace("_L_","")
                    else:
                        filename=all
                    file_integer, file_extension = filename.split(".tex")
                    if int(file_integer) > max_integer_file:
                        max_integer_file = int(file_integer) 

        ####### Checks files in 'Beispieleinreichung' #####
        ##################################################

        if local_save == True:
            pass
        else:
            try:
                if self.chosen_program=='lama':
                    path_saved_files = os.path.join(path_programm, "Beispieleinreichung")
                    if list_chosen_gk[0] in {
                        **k5_beschreibung,
                        **k6_beschreibung,
                        **k7_beschreibung,
                        **k8_beschreibung,
                    }:  ## merged dictionaries
                        if list_chosen_gk[0] in k5_beschreibung:
                            file_name_klasse = "K5"
                        elif list_chosen_gk[0] in k6_beschreibung:
                            file_name_klasse = "K6"
                        elif list_chosen_gk[0] in k7_beschreibung:
                            file_name_klasse = "K7"
                        elif list_chosen_gk[0] in k8_beschreibung:
                            file_name_klasse = "K8"
                        z = file_name_klasse + " - " + list_chosen_gk[0].upper() + " - "

                    else:
                        z = dict_gk[list_chosen_gk[0]] + " - "
                    if self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
                        for all in os.listdir(path_saved_files):
                            if all.endswith(".tex"):
                                if z in all:
                                    x, y = all.split(z)
                                    file_integer, file_extension = y.split(".tex")
                                    if int(file_integer) > max_integer_file:
                                        max_integer_file = int(file_integer)

                    if self.comboBox_aufgabentyp_cr.currentText() == "Typ 2":
                        for all in os.listdir(path_saved_files):
                            if all.endswith(".tex"):
                                if "-" in all:
                                    pass
                                else:
                                    file_integer, file_extension = all.split(".tex")
                                    if int(file_integer) > max_integer_file:
                                        max_integer_file = int(file_integer)
                if self.chosen_program=='cria':
                    klasse = "k" + str(highest_grade)
                    path_saved_files_klasse = os.path.join(path_programm, "Beispieleinreichung", klasse)

                    if not os.path.exists(path_saved_files_klasse):
                        os.makedirs(path_saved_files_klasse)

                    for all in os.listdir(path_saved_files_klasse):
                        if all.endswith(".tex"):
                            file_integer, file_extension = all.split(".tex")
                            if int(file_integer) > max_integer_file:
                                max_integer_file = int(file_integer)

            except FileNotFoundError:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Fehlermeldung")
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setWindowIcon(QtGui.QIcon(logo_path))
                msg.setText(
                    'Der Ordner "Beispieleinreichung" konnte nicht gefunden werden und\nmuss zuerst für Sie freigegeben werden.'
                )
                msg.setInformativeText(
                    "Derzeit können keine neuen Aufgaben eingegeben werden."
                )
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                retval = msg.exec_()
                return
        ############################################################################

        for all in dict_picture_path:
            head, tail = os.path.split(all)
            x = "{" + tail + "}"
            # name, ext =os.path.splitext(tail)
            if self.creator_mode == "admin" and self.cb_save.isChecked() == True:
                str_image_path = "../_database_inoffiziell/Bilder/"
            elif self.creator_mode == "admin" and self.cb_save.isChecked() == False:
                str_image_path = "../_database/Bilder/"
            elif local_save == True:
                str_image_path = "../Lokaler_Ordner/Bilder/"
            else:
                str_image_path = "../Beispieleinreichung/Bilder/"

            if self.chosen_program=='lama':    
                if (
                    x in textBox_Entry
                    and self.comboBox_aufgabentyp_cr.currentText() == "Typ 1"
                ):
                    textBox_Entry = str(textBox_Entry).replace(
                        tail,
                        str_image_path
                        + list_chosen_gk[0].upper()
                        + "_"
                        + str(max_integer_file + 1)
                        + "_"
                        + tail,
                    )
                if (
                    x in textBox_Entry
                    and self.comboBox_aufgabentyp_cr.currentText() == "Typ 2"
                ):
                    textBox_Entry = str(textBox_Entry).replace(
                        tail, str_image_path + str(max_integer_file + 1) + "_" + tail
                    )
            if self.chosen_program=='cria':
                if x in textBox_Entry:
                    
                    textBox_Entry = str(textBox_Entry).replace(
                        tail,
                        str_image_path
                        + klasse
                        + "_"
                        + str(max_integer_file + 1)
                        + "_"
                        + tail,
                    )

        # copy_image_path=os.path.join(path_programm,'_database','Bilder') ### direct save
        if self.creator_mode == "admin" and self.cb_save.isChecked() == False:
            copy_image_path = os.path.join(
                path_programm, "_database", "Bilder"
            )  ### direct save
        elif self.creator_mode == "admin" and self.cb_save.isChecked() == True:
            copy_image_path = os.path.join(
                path_programm, "_database_inoffiziell", "Bilder"
            )  ### direct save
        elif local_save == True:
            copy_image_path = os.path.join(path_programm, "Lokaler_Ordner", "Bilder")
        else:
            copy_image_path = os.path.join(
                path_programm, "Beispieleinreichung", "Bilder"
            )  ### indirect save

        for all in list(dict_picture_path.values()):
            image_path_temp = all
            head, tail = os.path.split(image_path_temp)
            copy_image_file_temp = os.path.join(copy_image_path, tail)
            try:
                shutil.copy(image_path_temp, copy_image_file_temp)
            except FileNotFoundError:
                try:
                    os.mkdir(copy_image_path)
                    shutil.copy(image_path_temp, copy_image_file_temp)
                except FileNotFoundError:
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle("Fehlermeldung")
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setWindowIcon(QtGui.QIcon(logo_path))
                    msg.setText(
                        'Der Ordner "Beispieleinreichung" konnte nicht gefunden werden und\nmuss zuerst für Sie freigegeben werden.'
                    )
                    msg.setInformativeText(
                        "Derzeit können keine neuen Aufgaben eingegeben werden."
                    )
                    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    retval = msg.exec_()
                    return

            if self.chosen_program == 'lama':
                if self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
                    if self.creator_mode == "admin":
                        if self.cb_save.isChecked() == False:
                            x = os.rename(
                                copy_image_file_temp,
                                "%s/_database/Bilder/" % path_programm
                                + list_chosen_gk[0].upper()
                                + "_"
                                + str(max_integer_file + 1)
                                + "_"
                                + tail,
                            )  ### direct save
                        if self.cb_save.isChecked() == True:
                            x = os.rename(
                                copy_image_file_temp,
                                "%s/_database_inoffiziell/Bilder/" % path_programm
                                + list_chosen_gk[0].upper()
                                + "_"
                                + str(max_integer_file + 1)
                                + "_"
                                + tail,
                            )  ### direct save
                    else:
                        if local_save == True:
                            x = os.rename(
                                copy_image_file_temp,
                                "%s/Lokaler_Ordner/Bilder/" % path_programm
                                + list_chosen_gk[0].upper()
                                + "_"
                                + str(max_integer_file + 1)
                                + "_"
                                + tail,
                            )  ### indirect
                        else:
                            x = os.rename(
                                copy_image_file_temp,
                                "%s/Beispieleinreichung/Bilder/" % path_programm
                                + list_chosen_gk[0].upper()
                                + "_"
                                + str(max_integer_file + 1)
                                + "_"
                                + tail,
                            )  ### indirect

                if self.comboBox_aufgabentyp_cr.currentText() == "Typ 2":
                    if self.creator_mode == "admin":
                        if self.cb_save.isChecked() == False:
                            x = os.rename(
                                copy_image_file_temp,
                                "%s/_database/Bilder/" % path_programm
                                + str(max_integer_file + 1)
                                + "_"
                                + tail,
                            )  ### direct save
                        if self.cb_save.isChecked() == True:
                            x = os.rename(
                                copy_image_file_temp,
                                "%s/_database_inoffiziell/Bilder/" % path_programm
                                + str(max_integer_file + 1)
                                + "_"
                                + tail,
                            )  ### direct save
                    else:
                        if local_save == True:
                            x = os.rename(
                                copy_image_file_temp,
                                "%s/Lokaler_Ordner/Bilder/" % path_programm
                                + str(max_integer_file + 1)
                                + "_"
                                + tail,
                            )  ### indirect
                        else:
                            x = os.rename(
                                copy_image_file_temp,
                                "%s/Beispieleinreichung/Bilder/" % path_programm
                                + str(max_integer_file + 1)
                                + "_"
                                + tail,
                            )  ### indirect save
            
            if self.chosen_program=='cria':
                if self.creator_mode == "admin":
                    if self.cb_save.isChecked() == False:               
                        x = os.rename(
                            copy_image_file_temp,
                            "%s/_database/Bilder/" % path_programm
                            + klasse
                            + "_"
                            + str(max_integer_file + 1)
                            + "_"
                            + tail,
                        )  ### direct official save
                    if self.cb_save.isChecked() == True:               
                        x = os.rename(
                            copy_image_file_temp,
                            "%s/_database_inoffiziell/Bilder/" % path_programm
                            + klasse
                            + "_"
                            + str(max_integer_file + 1)
                            + "_"
                            + tail,
                        )  ### direct inofficial save
                else:
                    if local_save == True:
                        x = os.rename(
                            copy_image_file_temp,
                            "%s/Lokaler_Ordner/Bilder/" % path_programm
                            + klasse
                            + "_"
                            + str(max_integer_file + 1)
                            + "_"
                            + tail,
                        )  ### direct local
                    else:
                        x = os.rename(
                            copy_image_file_temp,
                            "%s/Beispieleinreichung/Bilder/" % path_programm
                            + klasse
                            + "_"
                            + str(max_integer_file + 1)
                            + "_"
                            + tail,
                        )  ### indirect

        if self.chosen_program=='cria':
            themen_auswahl = []

            for all in self.list_creator_topics:
                thema = all[1] + "." + all[2]
                if thema not in themen_auswahl:
                    themen_auswahl.append(thema)

            themen_auswahl_joined = ", ".join(sorted(themen_auswahl))

            if self.creator_mode == "admin":
                if self.cb_save.isChecked() == False:
                    file_name = os.path.join(
                        path_programm,
                        "_database",
                        klasse,
                        "Einzelbeispiele",
                        str(max_integer_file + 1) + ".tex",
                    )  ### direct official save
                    file = open(file_name, "w", encoding="utf8")
                if self.cb_save.isChecked() == True:
                    file_name = os.path.join(
                        path_programm,
                        "_database_inoffiziell",
                        klasse,
                        "Einzelbeispiele",
                        str(max_integer_file + 1) + ".tex",
                    )  ### direct inofficial save
                    file = open(file_name, "w", encoding="utf8")
            else:
                if local_save == True:
                    file_name = os.path.join(
                        path_programm,
                        "Lokaler_Ordner",
                        klasse,
                        "_L_" + str(max_integer_file + 1) + ".tex",
                    )  ### direct local save
                else:
                    file_name = os.path.join(
                        path_programm,
                        "Beispieleinreichung",
                        klasse,
                        str(max_integer_file + 1) + ".tex",
                    )  ### indirect save

                try:
                    file = open(file_name, "w", encoding="utf8")
                except FileNotFoundError:
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle("Fehlermeldung")
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setWindowIcon(QtGui.QIcon(logo_path))
                    msg.setText(
                        'Der Ordner "Beispieleinreichung" konnte nicht gefunden werden und\nmuss zuerst für Sie freigegeben werden.'
                    )
                    msg.setInformativeText(
                        "Derzeit können keine neuen Aufgaben eingegeben werden."
                    )
                    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    msg.exec_()
                    return

            chosen_af_lang = self.comboBox_af.currentText()
            chosen_af = list(dict_aufgabenformate.keys())[
                list(dict_aufgabenformate.values()).index(chosen_af_lang)
            ]




        if " - " in edit_titel:
            edit_titel = edit_titel.replace(" - ", "-")

        if " - " in self.lineEdit_quelle.text():
            quelle = self.lineEdit_quelle.text().replace(" - ", "-")
        else:
            quelle = self.lineEdit_quelle.text()

        if local_save == True:
            local = "*Lokal* "
        else:
            local = ""


        if self.chosen_program == 'cria':
            file.write(
                "\section{"
                + local
                + klasse.upper()
                + " - "
                + themen_auswahl_joined
                + " - "
                + str(max_integer_file + 1)
                + " - "
                + edit_titel
                + " - "
                + chosen_af.upper()
                + " - "
                + quelle
                + "}\n\n"
                "\\begin{langesbeispiel} \item["
                + str(self.spinBox_punkte.value())
                + "] %PUNKTE DES BEISPIELS\n"
                + textBox_Entry
                + "\n\\end{langesbeispiel}"
            )

            file.close() 

        if self.chosen_program=='lama':
            if self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
                if self.creator_mode == "admin" or local_save == True:

                    pass
                else:
                    gk_path_temp = os.path.join(
                        path_programm, "Beispieleinreichung"
                    )  ## not direct save (path changed - comment/uncomment)

                if list_chosen_gk[0] in {
                    **k5_beschreibung,
                    **k6_beschreibung,
                    **k7_beschreibung,
                    **k8_beschreibung,
                }:  ## merged dictionaries
                    if list_chosen_gk[0] in k5_beschreibung:
                        file_name_klasse = "K5"
                    elif list_chosen_gk[0] in k6_beschreibung:
                        file_name_klasse = "K6"
                    elif list_chosen_gk[0] in k7_beschreibung:
                        file_name_klasse = "K7"
                    elif list_chosen_gk[0] in k8_beschreibung:
                        file_name_klasse = "K8"
                    if local_save == True:
                        file_name = os.path.join(
                            "_L_" + gk_path_temp,
                            file_name_klasse
                            + " - "
                            + list_chosen_gk[0].upper()
                            + " - "
                            + str(max_integer_file + 1)
                            + ".tex",
                        )
                    else:
                        file_name = os.path.join(
                            gk_path_temp,
                            file_name_klasse
                            + " - "
                            + list_chosen_gk[0].upper()
                            + " - "
                            + str(max_integer_file + 1)
                            + ".tex",
                        )

                    chosen_af = list(dict_aufgabenformate.keys())[
                        list(dict_aufgabenformate.values()).index(
                            self.comboBox_af.currentText()
                        )
                    ].upper()

                    # print('\section{'+file_name_klasse+' - '+list_chosen_gk[0].upper()+" - "+str(max_integer_file+1) +" - " + self.lineEdit_titel.text()+" - "+chosen_af+' - '+self.lineEdit_quelle.text())
                    try:
                        file = open(file_name, "w", encoding="utf8")
                    except FileNotFoundError:
                        msg = QtWidgets.QMessageBox()
                        msg.setWindowTitle("Fehlermeldung")
                        msg.setIcon(QtWidgets.QMessageBox.Critical)
                        msg.setWindowIcon(QtGui.QIcon(logo_path))
                        msg.setText(
                            'Der Ordner "Beispieleinreichung" konnte nicht gefunden werden und\nmuss zuerst für Sie freigegeben werden.'
                        )
                        msg.setInformativeText(
                            "Derzeit können keine neuen Aufgaben eingegeben werden."
                        )
                        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        retval = msg.exec_()
                        return

                    file.write(
                        "\section{"
                        + local
                        + file_name_klasse
                        + " - "
                        + list_chosen_gk[0].upper()
                        + " - "
                        + str(max_integer_file + 1)
                        + " - "
                        + edit_titel
                        + " - "
                        + chosen_af
                        + " - "
                        + quelle
                        + "}\n\n"
                        "\\begin{beispiel}["
                        + file_name_klasse
                        + " - "
                        + list_chosen_gk[0].upper()
                        + "]{"
                        + str(self.spinBox_punkte.value())
                        + "}\n"
                        + textBox_Entry
                        + "\n\\end{beispiel}"
                    )
                    file.close()

                else:
                    if local_save == True:
                        file_name = os.path.join(
                            gk_path_temp,
                            "_L_"
                            + dict_gk[list_chosen_gk[0]]
                            + " - "
                            + str(max_integer_file + 1)
                            + ".tex",
                        )
                    else:
                        file_name = os.path.join(
                            gk_path_temp,
                            dict_gk[list_chosen_gk[0]]
                            + " - "
                            + str(max_integer_file + 1)
                            + ".tex",
                        )

                    try:
                        file = open(file_name, "w", encoding="utf8")
                    except FileNotFoundError:
                        msg = QtWidgets.QMessageBox()
                        msg.setWindowTitle("Fehlermeldung")
                        msg.setIcon(QtWidgets.QMessageBox.Critical)
                        msg.setWindowIcon(QtGui.QIcon(logo_path))
                        msg.setText(
                            'Der Ordner "Beispieleinreichung" konnte nicht gefunden werden und\nmuss zuerst für Sie freigegeben werden.'
                        )
                        msg.setInformativeText(
                            "Derzeit können keine neuen Aufgaben eingegeben werden."
                        )
                        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        retval = msg.exec_()
                        return

                    if self.comboBox_klassen_cr.currentText() == "-":
                        chosen_af = list(dict_aufgabenformate.keys())[
                            list(dict_aufgabenformate.values()).index(
                                self.comboBox_af.currentText()
                            )
                        ].upper()
                        file.write(
                            "\section{"
                            + local
                            + dict_gk[list_chosen_gk[0]]
                            + " - "
                            + str(max_integer_file + 1)
                            + " - "
                            + edit_titel
                            + " - "
                            + chosen_af
                            + " - "
                            + quelle
                            + "}\n\n"
                            "\\begin{beispiel}["
                            + dict_gk[list_chosen_gk[0]]
                            + "]{"
                            + str(self.spinBox_punkte.value())
                            + "}\n"
                            + textBox_Entry
                            + "\n\\end{beispiel}"
                        )
                    else:
                        try:
                            klasse = (
                                "K"
                                + re.search(
                                    r"\d+", self.comboBox_klassen_cr.currentText()
                                ).group()
                            )  ### get selected grade
                        except AttributeError:
                            klasse = "MAT"
                        chosen_af = list(dict_aufgabenformate.keys())[
                            list(dict_aufgabenformate.values()).index(
                                self.comboBox_af.currentText()
                            )
                        ].upper()
                        file.write(
                            "\section{"
                            + local
                            + dict_gk[list_chosen_gk[0]]
                            + " - "
                            + str(max_integer_file + 1)
                            + " - "
                            + klasse
                            + " - "
                            + edit_titel
                            + " - "
                            + chosen_af
                            + " - "
                            + quelle
                            + "}\n\n"
                            "\\begin{beispiel}["
                            + dict_gk[list_chosen_gk[0]]
                            + "]{"
                            + str(self.spinBox_punkte.value())
                            + "}\n"
                            + textBox_Entry
                            + "\n\\end{beispiel}"
                        )
                    file.close()

            if self.comboBox_aufgabentyp_cr.currentText() == "Typ 2":
                themen_klasse_auswahl = []
                gk_auswahl = []

                # print(list_chosen_gk)
                for all in list_chosen_gk:
                    if all in {
                        **k5_beschreibung,
                        **k6_beschreibung,
                        **k7_beschreibung,
                        **k8_beschreibung,
                    }:
                        themen_klasse_auswahl.append(all.upper())
                    else:
                        gk_auswahl.append(dict_gk[all])

                gk_auswahl_joined = ", ".join(sorted(gk_auswahl))
                themen_klasse_auswahl_joined = ", ".join(sorted(themen_klasse_auswahl))

                if self.creator_mode == "admin":
                    if self.cb_save.isChecked() == False:
                        file_name = os.path.join(
                            path_programm,
                            "_database",
                            "Typ2Aufgaben",
                            "Einzelbeispiele",
                            str(max_integer_file + 1) + ".tex",
                        )  ### direct save
                    if self.cb_save.isChecked() == True:
                        file_name = os.path.join(
                            path_programm,
                            "_database_inoffiziell",
                            "Typ2Aufgaben",
                            "Einzelbeispiele",
                            str(max_integer_file + 1) + ".tex",
                        )  ### direct save
                else:
                    if local_save == True:
                        file_name = os.path.join(
                            path_programm,
                            "Lokaler_Ordner",
                            "Typ2Aufgaben",
                            "_L_" + str(max_integer_file + 1) + ".tex",
                        )  ### not direct save
                    else:
                        file_name = os.path.join(
                            path_programm,
                            "Beispieleinreichung",
                            str(max_integer_file + 1) + ".tex",
                        )  ### not direct save

                try:
                    file = open(file_name, "w", encoding="utf8")
                except FileNotFoundError:
                    msg = QtWidgets.QMessageBox()
                    msg.setWindowTitle("Fehlermeldung")
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setWindowIcon(QtGui.QIcon(logo_path))
                    msg.setText(
                        'Der Ordner "Beispieleinreichung" konnte nicht gefunden werden und\nmuss zuerst für Sie freigegeben werden.'
                    )
                    msg.setInformativeText(
                        "Derzeit können keine neuen Aufgaben eingegeben werden."
                    )
                    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    retval = msg.exec_()
                    return

                klasse = ""
                themen_klasse = ""
                gk = ""

                if self.comboBox_klassen_cr.currentText() == "-":
                    pass
                else:
                    try:
                        klasse = (
                            "K"
                            + re.search(
                                r"\d+", self.comboBox_klassen_cr.currentText()
                            ).group()
                            + " - "
                        )  ### get selected grade
                    except AttributeError:
                        klasse = "MAT - "

                if themen_klasse_auswahl == []:
                    gk = gk_auswahl_joined + " - "

                else:  # elif gk_auswahl==[]
                    themen_klasse = themen_klasse_auswahl_joined + " - "
                    x = 9
                    for all in themen_klasse_auswahl:
                        if all.lower() in k5_beschreibung:
                            if x > 5:
                                x = 5
                        elif all.lower() in k6_beschreibung:
                            if x > 6:
                                x = 6
                        elif all.lower() in k7_beschreibung:
                            if x > 7:
                                x = 7
                        elif all.lower() in k8_beschreibung:
                            if x > 8:
                                x = 8
                    if x < 9 and klasse == "":
                        klasse = "K%s - " % x

                    if gk_auswahl != []:
                        gk = gk_auswahl_joined + " - "

                file.write(
                    "\section{"
                    + local
                    + str(max_integer_file + 1)
                    + " - "
                    + klasse
                    + themen_klasse
                    + gk
                    + edit_titel
                    + " - "
                    + quelle
                    + "}\n\n"
                    "\\begin{langesbeispiel} \item["
                    + str(self.spinBox_punkte.value())
                    + "] %PUNKTE DES BEISPIELS\n"
                    + textBox_Entry
                    + "\n\n\\antwort{GK: "
                    + gk_auswahl_joined
                    + "}"
                    + "\n\\end{langesbeispiel}"
                )

                file.close()

        if dict_picture_path != {}:
            images = ", ".join(dict_picture_path)
        else:
            images = "-"

        if self.chosen_program=='lama':
            chosen_typ = self.comboBox_aufgabentyp_cr.currentText()[-1]
            if chosen_typ == "1":
                if list_chosen_gk[0] in {
                    **k5_beschreibung,
                    **k6_beschreibung,
                    **k7_beschreibung,
                    **k8_beschreibung,
                }:  ## merged dictionaries
                    if list_chosen_gk[0] in k5_beschreibung:
                        file_name_klasse = "K5"
                    elif list_chosen_gk[0] in k6_beschreibung:
                        file_name_klasse = "K6"
                    elif list_chosen_gk[0] in k7_beschreibung:
                        file_name_klasse = "K7"
                    elif list_chosen_gk[0] in k8_beschreibung:
                        file_name_klasse = "K8"
                    chosen_gk = file_name_klasse + " - " + list_chosen_gk[0].upper()
                else:
                    chosen_gk = dict_gk[list_chosen_gk[0]]
            if chosen_typ == "2":
                chosen_gk = ", ".join(sorted(gk_auswahl + themen_klasse_auswahl))

        if self.creator_mode == "admin":
            if self.cb_save.isChecked() == False:
                zusatz_info = " (Offiziell)"
            if self.cb_save.isChecked() == True:
                zusatz_info = " (Inoffiziell)"
        elif local_save == True:
            zusatz_info = " (Lokaler Ordner)"
        else:
            zusatz_info = ""

        QtWidgets.QApplication.restoreOverrideCursor()
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        if self.creator_mode == 'admin':
            msg.setWindowTitle("Admin Modus - Aufgabe erfolgreich gespeichert")
        if self.creator_mode == 'user':
            msg.setWindowTitle("Aufgabe erfolgreich gespeichert")
        msg.setWindowIcon(QtGui.QIcon(logo_path))

        if local_save == True:
            msg.setText(
                'Die Typ{0}-Aufgabe mit dem Titel\n\n"{1}"\n\nwurde lokal auf ihrem System gespeichert.'.format(
                    chosen_typ, edit_titel
                )
            )
        else:
            if self.chosen_program=='lama':
                msg.setText(
                    'Die Typ{0}-Aufgabe mit dem Titel\n\n"{1}"\n\nwurde gespeichert.'.format(
                        chosen_typ, edit_titel
                    )
                )

            elif self.chosen_program=='cria':
                msg.setText(
                    'Die Aufgabe mit dem Titel\n\n"{0}"\n\nwurde gespeichert.'.format(
                        edit_titel
                    )
                )


        if self.chosen_program=='lama':
            msg.setDetailedText(
                "Details{0}\n"
                "Grundkompetenz(en): {1}\n"
                "Punkte: {2}\n"
                "Klasse: {3}\n"
                "Bilder: {4}".format(
                    zusatz_info,
                    chosen_gk,
                    self.spinBox_punkte.value(),
                    self.comboBox_klassen_cr.currentText(),
                    images,
                )
            )

        elif self.chosen_program=='cria':
            msg.setDetailedText(
                "Details\n"
                "Thema/Themen: {0}\n"
                "Punkte: {1}\n"
                "Klasse: {2}. Klasse\n"
                "Bilder: {3}".format(
                    themen_auswahl_joined, self.spinBox_punkte.value(), klasse[-1], images
                )
            )                

        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()
        self.suchfenster_reset()

    ##################################################################
    ################## Befehle LAMA SAGE################################

    def create_log_file(self, typ):
        if typ==None:
            program='cria'
            log_file=os.path.join(path_programm, "Teildokument", "log_file_cria")
        else:
            program='lama'
            if typ==1:
                log_file=os.path.join(path_programm, "Teildokument", "log_file_1")
            if typ==2:
                log_file=os.path.join(path_programm, "Teildokument", "log_file_2")

        refresh_ddb(self, program)
        with open(log_file, encoding="utf8") as f:
            beispieldaten_dateipfad = json.load(f)
        
        return beispieldaten_dateipfad


    def check_if_log_file_exists(self, typ):
        for i in range(2):
            while True:
                try:
                    if typ==None:
                        search_list=self.beispieldaten_dateipfad_cria.values() 
                    elif typ==1:
                        search_list=self.beispieldaten_dateipfad_1.values()
                    elif typ==2:
                        search_list=self.beispieldaten_dateipfad_2.values()
                    break
                except AttributeError:
                    if typ==None:
                        self.beispieldaten_dateipfad_cria=self.create_log_file(typ) 
                    elif typ==1:
                        self.beispieldaten_dateipfad_1=self.create_log_file(typ)
                    elif typ==2:
                        self.beispieldaten_dateipfad_2=self.create_log_file(typ)
                break



    def check_if_file_exists(self, aufgabe): #aufgabe
        typ=self.get_aufgabentyp(aufgabe)
        self.check_if_log_file_exists(typ)
                            
        if typ==1:
            list_paths = self.beispieldaten_dateipfad_1.values()
        if typ==2:
            list_paths = self.beispieldaten_dateipfad_2.values()
        if typ==None:
            list_paths = self.beispieldaten_dateipfad_cria.values()
            klasse, aufgabe=self.split_klasse_aufgabe(aufgabe)

        name=aufgabe + ".tex"
        
        if typ==None:
            for path in list_paths:
                if klasse.lower() in path.lower():
                    if name == os.path.basename(path):                        
                        file_found=True
                        return file_found
                    else:
                        pass
            file_found=False             
            return file_found              
                        
        else:
            if any(name == os.path.basename(path) for path in list_paths):
                file_found=True
            else:
                file_found=False
            return file_found


    def load_file(self, path):
        with open(path, "r", encoding="utf8") as loaded_file:
            loaded_file=json.load(loaded_file)
            # print(loaded_file)
        return loaded_file

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


        

        loaded_file=self.load_file(self.saved_file_path)

        try:
            if self.chosen_program==loaded_file["data_gesamt"]['program']:
                if self.list_alle_aufgaben_sage != []:              
                    self.reset_sage()
            else:
                self.change_program()
        except KeyError:
            warning_window('Die geöffnete *.lama-Datei ist veraltet und kann nur mit der Version LaMA 1.x geöffnet werden.',
            'Bitte laden Sie ein aktuelle *.lama-Datei oder kontaktieren Sie lama.helpme@gmail.com, wenn Sie Hilfe benötigen.')
            return

        self.dict_all_infos_for_file =self.load_file(self.saved_file_path)


        self.update_gui('widgets_sage')
        
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))


        self.list_alle_aufgaben_sage = self.dict_all_infos_for_file["list_alle_aufgaben"]
        self.dict_alle_aufgaben_sage = self.dict_all_infos_for_file["dict_alle_aufgaben"]


        for aufgabe in self.list_alle_aufgaben_sage:
            file_found=self.check_if_file_exists(aufgabe)
            if file_found==False:
                QtWidgets.QApplication.restoreOverrideCursor()
                response=question_window("Aufgabe nicht gefunden",
                'Die Aufgabe "{}" konnte in der Datenbank nicht gefunden werden. Dies könnte daran liegen, dass die Datenbank veraltet ist (Tipp: Datenbank aktualisieren)'.format(aufgabe),
                'Wollen Sie diese Aufgabe entfernen?')

                if response==True:
                    self.list_alle_aufgaben_sage.remove(aufgabe)
                    del self.dict_alle_aufgaben_sage[aufgabe]
                    QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
                if response==False:
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

        if self.dict_all_infos_for_file["data_gesamt"]["Beurteilung"] == "br":
            self.combobox_beurteilung.setCurrentIndex(1)


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

        self.list_copy_images = self.dict_all_infos_for_file["data_gesamt"]["copy_images"]


        for aufgabe in self.list_alle_aufgaben_sage:
            self.build_aufgaben_schularbeit(aufgabe, True)


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
    
    def sage_save(self, path_create_tex_file=False):  # path_file
        try:
            self.saved_file_path
        except AttributeError:
            self.saved_file_path = path_programm

        if path_create_tex_file == False:
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

        else:
            name, extension = os.path.splitext(path_create_tex_file)
            path_create_tex_file = name + "_autosave.lama"
            save_file = path_create_tex_file

        self.update_gui('widgets_sage')    


        self.saved_file_path = save_file



        with open(save_file, "w+", encoding="utf8") as saved_file:
            json.dump(self.dict_all_infos_for_file, saved_file, ensure_ascii=False)



    def define_titlepage(self):
        if self.chosen_program=='lama':
            dict_titlepage=self.dict_titlepage
        if self.chosen_program=='cria':
            dict_titlepage=self.dict_titlepage_cria

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

        if self.chosen_program=='lama':
            self.dict_titlepage = dict_titlepage
            titlepage_save = os.path.join(path_programm, "Teildokument", "titlepage_save")
        if self.chosen_program=='cria':
            self.dict_titlepage_cria = dict_titlepage
            titlepage_save = os.path.join(path_programm, "Teildokument", "titlepage_save_cria")            

        try:
            with open(titlepage_save, "w+", encoding="utf8") as f:
                json.dump(dict_titlepage, f, ensure_ascii=False)
        except FileNotFoundError:
            os.makedirs(os.path.join(path_programm, "Teildokument"))
            with open(titlepage_save, "w+", encoding="utf8") as f:
                json.dump(dict_titlepage, f, ensure_ascii=False)




    def notenanzeige_changed(self):
        if self.combobox_beurteilung.currentIndex()==0:
            self.groupBox_beurteilungsraster.hide()
            self.groupBox_notenschl.show()
        if self.combobox_beurteilung.currentIndex()==1:
            self.groupBox_notenschl.hide()
            self.groupBox_beurteilungsraster.show()



        self.update_punkte()

    def get_aufgabentyp(self, aufgabe):
        aufgabe=aufgabe.replace('_L_','')
        if self.chosen_program=='cria':
            typ=None
        elif re.search("[A-Z]", aufgabe) == None:
            typ=2
        else:
            typ=1
        return typ

    def get_aufgabenverteilung(self):
        num_typ1=0
        num_typ2=0
        for all in self.list_alle_aufgaben_sage:
            typ=self.get_aufgabentyp(all)
            if typ==1:
                num_typ1 +=1
            if typ==2:
                num_typ2 +=1


        return [num_typ1, num_typ2]

    def sage_aufgabe_add(self, aufgabe):
        if self.chosen_program=='lama':

            old_num_typ1, old_num_typ2 = self.get_aufgabenverteilung()

            typ=self.get_aufgabentyp(aufgabe)
            if typ==1:
                self.list_alle_aufgaben_sage.insert(old_num_typ1, aufgabe)
            if typ==2:
                self.list_alle_aufgaben_sage.append(aufgabe)   


        if self.chosen_program =='cria':
            self.list_alle_aufgaben_sage.append(aufgabe)

        num_typ1, num_typ2 = self.get_aufgabenverteilung()
        num_total = len(self.list_alle_aufgaben_sage)


        if self.chosen_program =='lama':
            label = "Anzahl der Aufgaben: {0}\n(Typ1: {1} / Typ2: {2})".format(num_total, num_typ1, num_typ2)
        if self.chosen_program == 'cria':
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

        if self.chosen_program == 'lama':
            self.label_gesamtbeispiele.setText(
                _translate(
                    "MainWindow",
                    "Anzahl der Aufgaben: {0}\n(Typ1: {1} / Typ2: {2})".format(
                        num_total, num_typ1, num_typ2
                    ),
                    None,
                )
            )
        if self.chosen_program == 'cria':
            self.label_gesamtbeispiele.setText(
                _translate(
                    "MainWindow",
                    "Anzahl der Aufgaben: {0}".format(num_total),None))

    def btn_up_pressed(self, aufgabe):
        a, b = self.list_alle_aufgaben_sage.index(aufgabe), self.list_alle_aufgaben_sage.index(aufgabe) - 1
        self.list_alle_aufgaben_sage[a], self.list_alle_aufgaben_sage[b] = (
            self.list_alle_aufgaben_sage[b],
            self.list_alle_aufgaben_sage[a],
        )

        self.build_aufgaben_schularbeit(aufgabe)


    def btn_down_pressed(self, aufgabe):

        a, b = self.list_alle_aufgaben_sage.index(aufgabe), self.list_alle_aufgaben_sage.index(aufgabe) + 1
        self.list_alle_aufgaben_sage[a], self.list_alle_aufgaben_sage[b] = (
            self.list_alle_aufgaben_sage[b],
            self.list_alle_aufgaben_sage[a],
        )  

        self.build_aufgaben_schularbeit(aufgabe)



    def erase_aufgabe(self, aufgabe):
        del self.dict_alle_aufgaben_sage[aufgabe]
        del self.dict_variablen_punkte[aufgabe]
        self.list_alle_aufgaben_sage.remove(aufgabe)
        if self.get_aufgabentyp(aufgabe)==2:
            del self.dict_variablen_label[aufgabe]
        if aufgabe in self.dict_sage_ausgleichspunkte_chosen:
            del self.dict_sage_ausgleichspunkte_chosen[aufgabe]
        if aufgabe in self.dict_sage_hide_show_items_chosen:
            del self.dict_sage_hide_show_items_chosen[aufgabe]



    def btn_delete_pressed(self, aufgabe):

        index=self.list_alle_aufgaben_sage.index(aufgabe)

        if index+1 == len(self.list_alle_aufgaben_sage):
            self.delete_widget(self.gridLayout_8, index)
            self.erase_aufgabe(aufgabe) 

        else:
            self.erase_aufgabe(aufgabe)
            self.build_aufgaben_schularbeit(self.list_alle_aufgaben_sage[index])
        
        self.update_punkte()




    def spinbox_pkt_changed(self, aufgabe, spinbox_pkt):
        self.dict_alle_aufgaben_sage[aufgabe][0]=spinbox_pkt.value()
        self.update_punkte()

    def spinbox_abstand_changed(self, aufgabe, spinbox_abstand):
        self.dict_alle_aufgaben_sage[aufgabe][1]=spinbox_abstand.value()
        self.update_punkte()


    def get_punkteverteilung(self):
        pkt_typ1=0
        pkt_typ2=0
        pkt_ausgleich=0
        gesamtpunkte=0
        for all in self.dict_variablen_punkte:
            typ=self.get_aufgabentyp(all)
            if typ==None:
                gesamtpunkte += self.dict_variablen_punkte[all].value()
            elif typ==1:
                pkt_typ1 += self.dict_variablen_punkte[all].value()
                gesamtpunkte += self.dict_variablen_punkte[all].value()
            elif typ==2:
                pkt_typ2 += self.dict_variablen_punkte[all].value()
                pkt_ausgleich += self.dict_alle_aufgaben_sage[all][3]
                gesamtpunkte += self.dict_variablen_punkte[all].value()

        return [gesamtpunkte, pkt_typ1, pkt_typ2]

    def update_notenschluessel(self):
        gesamtpunkte= self.get_punkteverteilung()[0]

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
            _translate("MainWindow", "% (ab {})".format(verteilung_notenschluessel[0]), None)
        )
        self.label_g_pkt.setText(
            _translate("MainWindow", "% (ab {})".format(verteilung_notenschluessel[1]), None)
        )
        self.label_b_pkt.setText(
            _translate("MainWindow", "% (ab {})".format(verteilung_notenschluessel[2]), None)
        )
        self.label_g_2_pkt.setText(
            _translate("MainWindow", "% (ab {})".format(verteilung_notenschluessel[3]), None)
        )


    def get_number_ausgleichspunkte_gesamt(self):
        number_ausgleichspkt_gesamt=0
        for aufgabe in self.list_alle_aufgaben_sage:
            if self.get_aufgabentyp(aufgabe)==2:  
                number_ausgleichspkt_gesamt += self.dict_alle_aufgaben_sage[aufgabe][3]

        return number_ausgleichspkt_gesamt

    def update_beurteilungsraster(self):

        punkteverteilung= self.get_punkteverteilung()
        number_ausgleichspunkte_gesamt=self.get_number_ausgleichspunkte_gesamt()
        self.label_typ1_pkt.setText(
            _translate("MainWindow", "Punkte Typ 1: {}".format(punkteverteilung[1]), None)
        )
        self.label_typ2_pkt.setText(
            _translate("MainWindow", "Punkte Typ 2: {0} (davon Ausgleichspunkte: {1})".format(punkteverteilung[2], number_ausgleichspunkte_gesamt), None)
        )

        

    def update_punkte(self):

        gesamtpunkte = self.get_punkteverteilung()[0]

        if self.combobox_beurteilung.currentIndex()==0:
            self.update_notenschluessel()

        if self.combobox_beurteilung.currentIndex()==1:
            self.update_beurteilungsraster()


        self.label_gesamtpunkte.setText(
            _translate("MainWindow", "Gesamtpunkte: %i" % gesamtpunkte, None)
        )     


    def update_default_pkt(self):
        for all in self.dict_variablen_punkte:
            if self.get_aufgabentyp(all)==1:
                self.dict_variablen_punkte[all].setValue(self.spinBox_default_pkt.value())
                self.dict_alle_aufgaben_sage[all][0]=self.spinBox_default_pkt.value()





    def create_neue_aufgaben_box(self,index, aufgabe, aufgaben_infos):
        typ=self.get_aufgabentyp(aufgabe)
        aufgaben_verteilung=self.get_aufgabenverteilung()
        if self.chosen_program=='cria':
            klasse, aufgaben_nummer=self.split_klasse_aufgabe(aufgabe)
            klasse=klasse[1]

            new_groupbox=create_new_groupbox(self.scrollAreaWidgetContents_2,
            "{0}. Aufgabe".format(index+1))
        else:
            new_groupbox=create_new_groupbox(self.scrollAreaWidgetContents_2,
            "{0}. Aufgabe (Typ{1})".format(index+1, typ))



        gridLayout_gB = QtWidgets.QGridLayout(new_groupbox)
        gridLayout_gB.setObjectName("gridLayout_gB")

        
        if typ==None:
            try:
                aufgabenformat = " ("+dict_aufgabenformate[aufgaben_infos[3].lower()+")"]
            except KeyError:
                aufgabenformat = "" 
            if '_L_' in aufgaben_nummer:
                x= aufgaben_nummer.replace("_L_","")
                label="{0}. Klasse - {1} (lokal){2}".format(klasse, x, aufgabenformat)
            else:
                label="{0}. Klasse - {1}{2}".format(klasse, aufgaben_nummer, aufgabenformat)
        elif typ==1:
            try:
                aufgabenformat = " ("+dict_aufgabenformate[aufgaben_infos[3].lower()]+")"
            except KeyError:
                aufgabenformat = "" 
            label="{0}{1}".format(aufgabe, aufgabenformat)
        elif typ == 2:
            label="{0}".format(aufgabe)

        label_aufgabe = create_new_label(new_groupbox, label, True)
        gridLayout_gB.addWidget(label_aufgabe, 0, 0, 1, 1)

        label_titel = create_new_label(new_groupbox, "Titel: {}".format(aufgaben_infos[2]),True)
        gridLayout_gB.addWidget(label_titel, 1, 0, 1, 1)



        groupbox_pkt = create_new_groupbox(new_groupbox, "Punkte")
        gridLayout_gB.addWidget(groupbox_pkt, 0, 1, 2, 1,QtCore.Qt.AlignRight)
        punkte=self.dict_alle_aufgaben_sage[aufgabe][0]

        horizontalLayout_groupbox_pkt = QtWidgets.QHBoxLayout(groupbox_pkt)
        horizontalLayout_groupbox_pkt.setObjectName(_fromUtf8("horizontalLayout_groupbox_pkt"))
        spinbox_pkt = create_new_spinbox(groupbox_pkt)
        spinbox_pkt.setValue(punkte)
        spinbox_pkt.valueChanged.connect(partial(self.spinbox_pkt_changed, aufgabe, spinbox_pkt))
        self.dict_variablen_punkte[aufgabe]=spinbox_pkt


        horizontalLayout_groupbox_pkt.addWidget(spinbox_pkt)

        if typ == 2:
            groupbox_pkt.setToolTip(
                "Die Punkte geben die Gesamtpunkte dieser Aufgabe an.\nEs müssen daher auch die Ausgleichspunkte berücksichtigt werden."
            )


        if (index % 2) == 1 and (typ==1 or typ==None):
            background_color=get_color(blue_1)
            new_groupbox.setStyleSheet(_fromUtf8("QGroupBox {{background-color: {0};}} ".format(background_color)))
        if typ == 2:
            new_groupbox.setStyleSheet(StyleSheet_typ2)



        button_up = create_standard_button(new_groupbox, "",
        partial(self.btn_up_pressed, aufgabe),
        QtWidgets.QStyle.SP_ArrowUp)
        
        gridLayout_gB.addWidget(button_up, 0, 3, 2, 1)
        number=index+1
        if (typ==1 or typ==None) and number==1:
            button_up.setEnabled(False)
        if typ==2 and number==aufgaben_verteilung[0]+1:
            button_up.setEnabled(False)

        button_down = create_standard_button(new_groupbox, "",
        partial(self.btn_down_pressed,aufgabe),
        QtWidgets.QStyle.SP_ArrowDown)
        gridLayout_gB.addWidget(button_down, 0, 4, 2, 1)

        if typ==1 and number==aufgaben_verteilung[0]:
            button_down.setEnabled(False)
        if (typ==2 or typ==None) and number==len(self.list_alle_aufgaben_sage):
            button_down.setEnabled(False)


        button_delete = create_standard_button(new_groupbox, "",
        partial(self.btn_delete_pressed, aufgabe),
        QtWidgets.QStyle.SP_TitleBarCloseButton)
        gridLayout_gB.addWidget(button_delete, 0, 5, 2, 1)


        groupbox_abstand = create_new_groupbox(new_groupbox, "Abstand (cm)")
        groupbox_abstand.setSizePolicy(SizePolicy_fixed)
        groupbox_abstand.setToolTip("Neue Seite: Abstand=99")
        # groupbox_abstand.setMaximumSize(QtCore.QSize(100, 16777215))
        gridLayout_gB.addWidget(groupbox_abstand, 0, 2, 2, 1)
        
        verticalLayout_abstand = QtWidgets.QVBoxLayout(groupbox_abstand)
        verticalLayout_abstand.setObjectName("verticalLayout_abstand")

        if self.chosen_program=='lama' and typ == 2:
            groupbox_abstand.hide()

        
        abstand=self.dict_alle_aufgaben_sage[aufgabe][1]
        spinbox_abstand = create_new_spinbox(groupbox_abstand)
        spinbox_abstand.setValue(abstand)
        spinbox_abstand.valueChanged.connect(partial(self.spinbox_abstand_changed, aufgabe, spinbox_abstand))
        verticalLayout_abstand.addWidget(spinbox_abstand)

        
        if typ==2:
            label_ausgleichspkt = create_new_label(groupbox_pkt, 'Ausgleichspunkte: {}'.format(self.dict_alle_aufgaben_sage[aufgabe][3]))
            gridLayout_gB.addWidget(label_ausgleichspkt, 0, 2, 1, 1)
            self.dict_variablen_label[aufgabe]=label_ausgleichspkt

            pushbutton_ausgleich = create_new_button(new_groupbox,"Aufgabe bearbeiten...",
            partial(self.pushButton_ausgleich_pressed, aufgabe))
            pushbutton_ausgleich.setStyleSheet("padding: 6px")
            pushbutton_ausgleich.setSizePolicy(SizePolicy_fixed)
            # pushbutton_ausgleich.setMaximumSize(QtCore.QSize(220, 30))
            gridLayout_gB.addWidget(pushbutton_ausgleich, 1, 2, 1, 1)

            # pushbutton_aufgabe_bearbeiten = create_new_button(groupbox_pkt, 'Aufgabe bearbeiten', still_to_define)
            # gridLayout_gB.addWidget(pushbutton_aufgabe_bearbeiten, 0,1,1,1)



        return new_groupbox


    def get_klasse(self, aufgabe):
        klasse=list_klassen[self.comboBox_klassen.currentIndex()]
        
        return klasse


    def collect_all_infos_aufgabe(self, aufgabe):
        typ=self.get_aufgabentyp(aufgabe)

        if typ==None:
            klasse, aufgabe=self.split_klasse_aufgabe(aufgabe)
            name=aufgabe + ".tex"
            for all in self.beispieldaten_dateipfad_cria:
                if klasse.upper() in all:
                    filename = os.path.basename(self.beispieldaten_dateipfad_cria[all])
                    if name == filename:
                        section_split = all.split(" - ")
                        titel=section_split[3]
                        typ_info=section_split[4] # Aufgabenformat
            punkte=0


        if typ==1:
            name = aufgabe + ".tex"
            for all in self.beispieldaten_dateipfad_1:
                filename = os.path.basename(self.beispieldaten_dateipfad_1[all])
                if name == filename:
                    x = all.split(" - ")
                    titel = x[-3]
                    typ_info=x[-2] #Aufgabenformat
            punkte=self.spinBox_default_pkt.value()

        elif typ==2:
            name = aufgabe + ".tex"
            for all in self.beispieldaten_dateipfad_2:
                filename = os.path.basename(self.beispieldaten_dateipfad_2[all])
                if name == filename:
                    x = all.split(" - ")
                    titel = x[-2]
                    typ_info=self.get_number_ausgleichspunkte(aufgabe) # Ausgleichspunkte
            punkte=0

        return [punkte, 0, titel, typ_info]

    def get_dateipfad_aufgabe(self, aufgabe):
        typ=self.get_aufgabentyp(aufgabe)
        if self.chosen_program=='cria':
            list_path = self.beispieldaten_dateipfad_cria.values()
            klasse, aufgabe = self.split_klasse_aufgabe(aufgabe)
            name = aufgabe + ".tex"
            for path in list_path:
                if klasse.lower() in path.lower():
                    if name == os.path.basename(path):
                        dateipfad = path

        if self.chosen_program=='lama':
            if typ==1:
                list_path = self.beispieldaten_dateipfad_1.values()
            elif typ==2:
                list_path = self.beispieldaten_dateipfad_2.values()        
            name = aufgabe + ".tex"
            for path in list_path:
                if name == os.path.basename(path):
                    dateipfad = path


        return dateipfad


    def get_number_ausgleichspunkte(self, aufgabe):
        typ=self.get_aufgabentyp(aufgabe)

        if typ==2:
            content=collect_content(self, aufgabe)

            number_ausgleichspunkte = content.count("\\fbox{A}")
        
            return number_ausgleichspunkte

    def delete_all_widgets(self, layout, start=0):
        for i in reversed(range(start, layout.count())):
            self.delete_widget(layout, i)

    def delete_widget(self, layout , index):
        try:
            layout.itemAt(index).widget().setParent(None)
        except AttributeError:
            pass        


    def split_klasse_aufgabe(self, aufgabe):
        klasse, aufgabe=aufgabe.split("_",1)
        if 'L_' in aufgabe:
            aufgabe='_'+aufgabe   

        return klasse, aufgabe

    def build_klasse_aufgabe(self, aufgabe):
        klasse=self.get_klasse(aufgabe)
        if '_L_' in aufgabe:
            klasse_aufgabe=klasse+aufgabe
        else:    
            klasse_aufgabe=klasse+'_'+aufgabe 
        return klasse_aufgabe       

    def add_image_path_to_list(self, aufgabe):
        content = collect_content(self, aufgabe)

        if "\\includegraphics" in content:
            matches = re.findall("/Bilder/(.+.eps)}", content)
            for image in matches:
                self.list_copy_images.append(image)
        # print(self.list_copy_images) 

    def build_aufgaben_schularbeit(self, aufgabe, file_loaded=False): 
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        try:
            self.gridLayout_8.removeItem(self.spacerItem)
        except AttributeError:
            pass

 
        index=self.list_alle_aufgaben_sage.index(aufgabe)


        if index==0:
            start_value=index          
        else:
            start_value=index-1


        for i in reversed(range(start_value, self.gridLayout_8.count()+1)):
            self.delete_widget(self.gridLayout_8, i)



        for item in self.list_alle_aufgaben_sage[start_value:]:
            index_item = self.list_alle_aufgaben_sage.index(item)
            item_infos = self.collect_all_infos_aufgabe(item)             
            neue_aufgaben_box=self.create_neue_aufgaben_box(index_item, item, item_infos)            
            self.gridLayout_8.addWidget(neue_aufgaben_box, index_item, 0, 1, 1)
            index_item+1




        self.spacerItem = QtWidgets.QSpacerItem(
            20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_8.addItem(self.spacerItem, index_item+1, 0, 1, 1)

        
        self.add_image_path_to_list(aufgabe)


        self.update_punkte()
        QtWidgets.QApplication.restoreOverrideCursor()




    def pushButton_ausgleich_pressed(self, aufgabe):
        content = collect_content(self, aufgabe)

        try:
            split_content, index_end = split_aufgaben_content(content)
            split_content = split_content[:index_end]
        except Exception as e1:
            try:
                split_content = split_aufgaben_content_new_format(content)
            except Exception as e2:
                split_content=None
            if split_content==None:
                warning_window(
                    "Es ist ein Fehler bei der Anzeige der Aufgabe {} aufgetreten! (Die Aufgabe kann voraussichtlich dennoch verwendet und individuell in der TeX-Datei bearbeitet werden.)\n".format(
                        aufgabe
                    ),
                    'Bitte melden Sie den Fehler unter dem Abschnitt "Feedback & Fehler" an das LaMA-Team. Vielen Dank!'
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

        # print(list_sage_ausgleichspunkte_chosen)
        if aufgabe in self.dict_sage_hide_show_items_chosen.keys():
            list_sage_hide_show_items_chosen = self.dict_sage_hide_show_items_chosen[aufgabe]
        else:
            list_sage_hide_show_items_chosen=[]
        self.Dialog = QtWidgets.QDialog(
            None,
            QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint,
        )
        self.ui = Ui_Dialog_ausgleichspunkte()
        self.ui.setupUi(
            self.Dialog, split_content, list_sage_ausgleichspunkte_chosen, list_sage_hide_show_items_chosen
        )
        # self.Dialog.show()
        self.Dialog.exec_()

        self.dict_sage_ausgleichspunkte_chosen[
            aufgabe
        ] = self.ui.list_sage_ausgleichspunkte_chosen

        self.dict_sage_hide_show_items_chosen[aufgabe]= self.ui.list_sage_hide_show_items_chosen

        # print(self.dict_sage_ausgleichspunkte_chosen)
        print(self.dict_sage_hide_show_items_chosen)

        self.dict_alle_aufgaben_sage[aufgabe][3]=len(self.ui.list_sage_ausgleichspunkte_chosen)

        self.dict_variablen_label[aufgabe].setText(_translate("MainWindow","Ausgleichspunkte: {}".format(len(self.ui.list_sage_ausgleichspunkte_chosen)), None))
        self.update_punkte()
        #### Predefined Ausgleichspunkte überschreiben gewählte


    def comboBox_at_sage_changed(self):
        if self.comboBox_at_sage.currentText()[-1] == "1":
            self.comboBox_gk.clear()
            self.lineEdit_number.clear()
            list_comboBox_gk = ["", "AG", "FA", "AN", "WS", "K5", "K6", "K7", "K8"]
            index = 0
            for all in list_comboBox_gk:
                self.comboBox_gk.addItem("")
                self.comboBox_gk.setItemText(index, _translate("MainWindow", all, None))
                index += 1
            self.comboBox_gk_num.clear()

        if self.comboBox_at_sage.currentText()[-1] == "2":
            self.comboBox_gk.clear()
            self.comboBox_gk.addItem("-")
            self.comboBox_gk_num.clear()
            self.comboBox_gk_num.addItem("-")
        self.adapt_choosing_list("sage")

    def comboBox_at_fb_changed(self):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.label_example.setText(
            _translate("MainWindow", "Ausgewählte Aufgabe: -", None)
        )

        if self.comboBox_at_fb.currentText() == "Allgemeine Rückmeldung":
            self.groupBox_alle_aufgaben_fb.setEnabled(False)
        else:
            self.groupBox_alle_aufgaben_fb.setEnabled(True)
        if self.comboBox_at_fb.currentText()[-1] == "1":
            self.comboBox_fb.clear()
            self.lineEdit_number_fb.clear()
            list_comboBox_gk = ["", "AG", "FA", "AN", "WS", "K5", "K6", "K7", "K8"]
            for all in list_comboBox_gk:
                self.comboBox_fb.addItem(all)

            self.comboBox_fb_num.clear()

        if self.comboBox_at_fb.currentText()[-1] == "2":
            self.comboBox_fb.clear()
            self.comboBox_fb.addItem("-")
            self.comboBox_fb_num.clear()
            self.comboBox_fb_num.addItem("-")
        self.adapt_choosing_list("feedback")
        QtWidgets.QApplication.restoreOverrideCursor()

    def comboBox_gk_changed(self, list_mode):
        self.adapt_choosing_list(list_mode)

        if list_mode == "sage":
            self.comboBox_gk_num.clear()
            if self.comboBox_gk.currentText()=="":
                return
            self.comboBox_gk_num.addItem("")
            self.lineEdit_number.clear()
            list_klassen = ["k5", "k6", "k7", "k8"]
            if self.comboBox_gk.currentText().lower() in list_klassen:
                x = eval("%s_beschreibung" % self.comboBox_gk.currentText().lower())
                for all in x.keys():
                    self.comboBox_gk_num.addItem(all.upper())
            else:
                for all in dict_gk.keys():
                    if all.startswith(self.comboBox_gk.currentText().lower()):
                        self.comboBox_gk_num.addItem(dict_gk[all][-3:])
        if list_mode == "feedback":
            self.comboBox_fb_num.clear()
            if self.comboBox_fb.currentText()=="":
                return
            self.comboBox_fb_num.addItem("")
            self.lineEdit_number_fb.clear()
            list_klassen = ["k5", "k6", "k7", "k8"]
            if self.comboBox_fb.currentText().lower() in list_klassen:
                x = eval("%s_beschreibung" % self.comboBox_fb.currentText().lower())
                for all in x.keys():
                    self.comboBox_fb_num.addItem(all.upper())
            else:
                for all in dict_gk.keys():
                    if all.startswith(self.comboBox_fb.currentText().lower()):
                        self.comboBox_fb_num.addItem(dict_gk[all][-3:])

    def comboBox_gk_num_changed(self, list_mode):
        self.adapt_choosing_list(list_mode)

    def lineEdit_number_changed(self, list_mode):
        self.adapt_choosing_list(list_mode)

    def nummer_clicked(self, item):
        aufgabe=item.text().replace("*E-", "")
        if self.chosen_program=='cria':
            aufgabe=self.build_klasse_aufgabe(aufgabe)

        if aufgabe in self.list_alle_aufgaben_sage:
            return

        try:
            collect_content(self, aufgabe)
        except FileNotFoundError:
            warning_window('Die Datei konnte nicht gefunden werden.\nBitte wählen Sie "Refresh Database" (F5) und versuchen Sie es erneut.')
            return
    
        self.sage_aufgabe_add(aufgabe)
        infos=self.collect_all_infos_aufgabe(aufgabe)
        self.dict_alle_aufgaben_sage[aufgabe]=infos

        self.build_aufgaben_schularbeit(aufgabe) # aufgabe, aufgaben_verteilung
        self.lineEdit_number.setText("")
        self.lineEdit_number.setFocus()

    def nummer_clicked_fb(self, item):
        # print(item.text())
        if self.chosen_program=='lama':
            self.label_example.setText(
                _translate(
                    "MainWindow", "Ausgewählte Aufgabe: {}".format(item.text()), None
                )
            )

        if self.chosen_program=='cria':
            self.label_example.setText(
                _translate(
                    "MainWindow",
                    "Ausgewählte Aufgabe: {0} ({1})".format(
                        item.text(), self.comboBox_klassen_fb_cria.currentText(),
                    ),None
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
            self.listWidget_fb.clear()
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

        self.adapt_choosing_list(list_mode)



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
                "dict_{}".format(list_klassen[self.comboBox_klassen_fb_cria.currentIndex()])
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
                # self.comboBox_unterkapitel.setItemText(index, _translate("MainWindow", dict_unterkapitel[all] + ' ('+all+')'))
            if list_mode == "feedback":
                self.comboBox_unterkapitel_fb_cria.addItem(
                    dict_unterkapitel[all] + " (" + all + ")"
                )
                # self.comboBox_unterkapitel_fb.setItemText(index, _translate("MainWindow", dict_unterkapitel[all] + ' ('+all+')'))
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


    def add_filename_to_list(self, list_mode, file_path, list_beispieldaten):
        filename_all = os.path.basename(file_path)
        name, extension = os.path.splitext(filename_all)
        if list_mode == "sage":
            if name.startswith(self.lineEdit_number.text()):
                if "Beispieleinreichung" in file_path:
                    list_beispieldaten.append("*E-" + name)
                else:
                    list_beispieldaten.append(name)
        if list_mode == "feedback":
            if name.startswith(self.lineEdit_number_fb.text()) and self.chosen_program=='lama':
                list_beispieldaten.append(name)
            if name.startswith(self.lineEdit_number_fb_cria.text()) and self.chosen_program=='cria':
                list_beispieldaten.append(name)

    def get_dictionary_of_file_paths(self, log_file):
        try:
            with open(log_file, encoding="utf8") as f:
                dictionary = json.load(f)
        except FileNotFoundError:
            refresh_ddb(self)  # 1
            with open(log_file, encoding="utf8") as f:
                dictionary = json.load(f)

        return dictionary       

    def adapt_choosing_list(self, list_mode):
        if list_mode == "sage":
            listWidget = self.listWidget
        if list_mode == "feedback":
            if self.chosen_program=='lama':
                listWidget = self.listWidget_fb
            if self.chosen_program=='cria':
                listWidget = self.listWidget_fb_cria

            if self.comboBox_at_fb.currentText() == "Allgemeine Rückmeldung":
                self.comboBox_fb.clear()
                self.comboBox_fb_num.clear()
                self.lineEdit_number_fb.clear()
                listWidget.clear()
                return

        listWidget.clear()

        log_file_1 = os.path.join(path_programm, "Teildokument", "log_file_1")
        log_file_2 = os.path.join(path_programm, "Teildokument", "log_file_2")
        log_file_cria = os.path.join(path_programm, "Teildokument", "log_file_cria")


        if self.chosen_program == 'lama':
            beispieldaten_dateipfad_1 = self.get_dictionary_of_file_paths(log_file_1)
            self.beispieldaten_dateipfad_1 = beispieldaten_dateipfad_1

            beispieldaten_dateipfad_2 = self.get_dictionary_of_file_paths(log_file_2)
            self.beispieldaten_dateipfad_2 = beispieldaten_dateipfad_2


        if self.chosen_program == 'cria':
            beispieldaten_dateipfad_cria = self.get_dictionary_of_file_paths(log_file_cria)
            self.beispieldaten_dateipfad_cria = beispieldaten_dateipfad_cria



        if self.cb_drafts_sage.isChecked():
            drafts_path = os.path.join(path_programm, "Beispieleinreichung")
            if self.chosen_program == 'lama':
                for all in os.listdir(drafts_path):
                    if all.endswith(".tex") or all.endswith(".ltx"):
                        pattern = re.compile("[A-Z][A-Z]")
                        if int(self.comboBox_at_sage.currentText()[-1]) == 1:
                            if pattern.match(all):
                                file = open(os.path.join(drafts_path, all), encoding="utf8")
                                for i, line in enumerate(file):
                                    if not line == "\n":
                                        # line=line.replace('\section{', 'section{ENTWURF ')
                                        self.beispieldaten_dateipfad_1[line] = os.path.join(
                                            drafts_path, all
                                        )
                                        # beispieldaten.append(line)
                                        break
                                file.close()
                        if int(self.comboBox_at_sage.currentText()[-1]) == 2:
                            if not pattern.match(all):
                                file = open(os.path.join(drafts_path, all), encoding="utf8")
                                for i, line in enumerate(file):
                                    if not line == "\n":
                                        # line=line.replace('\section{', 'section{ENTWURF ')
                                        self.beispieldaten_dateipfad_2[line] = os.path.join(
                                            drafts_path, all
                                        )
                                        # beispieldaten.append(line)
                                        break
                                file.close()
            if self.chosen_program == 'cria':
                for klasse in list_klassen:
                    try:
                        drafts_path = os.path.join(path_programm, "Beispieleinreichung",klasse)
                        for all in os.listdir(drafts_path):
                            file = open(os.path.join(drafts_path, all), encoding="utf8")
                            for i, line in enumerate(file):
                                if not line == "\n":
                                    # line=line.replace('\section{', 'section{ENTWURF ')
                                    self.beispieldaten_dateipfad_cria[line] = os.path.join(drafts_path, all)
                                    break
                            file.close()
                    except FileNotFoundError:
                        pass                


        list_beispieldaten = []
        if list_mode == "sage":
            if self.chosen_program == 'lama':
                beispieldaten_dateipfad = eval(
                    "beispieldaten_dateipfad_%s" % self.comboBox_at_sage.currentText()[-1]
                )
                for all in beispieldaten_dateipfad.values():
                    filename_all = os.path.basename(all)
                    name, extension = os.path.splitext(filename_all)
                    if self.comboBox_at_sage.currentText()[-1] == "2":
                        if name.startswith(self.lineEdit_number.text()):
                            if "Beispieleinreichung" in all:
                                list_beispieldaten.append("*E-" + name)
                            else:
                                list_beispieldaten.append(name)
                    else:
                        if (
                            self.comboBox_gk.currentText() in name
                            and self.comboBox_gk_num.currentText() in name
                        ):
                            try:
                                int(self.lineEdit_number.text())
                                number = name.split(" - ")
                                if (
                                    self.lineEdit_number.text() == ""
                                    or number[1] == self.lineEdit_number.text()
                                ):  # number[1]==self.lineEdit_number.text():
                                    if "Beispieleinreichung" in all:
                                        list_beispieldaten.append("*E-" + name)
                                    else:
                                        list_beispieldaten.append(name)
                            except ValueError:
                                if (
                                    self.lineEdit_number.text() == ""
                                    or self.lineEdit_number.text().lower() in name.lower()
                                ):  # number[1]==self.lineEdit_number.text():
                                    if "Beispieleinreichung" in all:
                                        list_beispieldaten.append("*E-" + name)
                                    else:
                                        list_beispieldaten.append(name)

                            # and self.lineEdit_number.text().lower() in name.lower()
            
            if self.chosen_program == 'cria':
                dict_klasse_name = eval(
                    "dict_{}_name".format(
                        list_klassen[self.comboBox_klassen.currentIndex()]
                    )
                )
                if self.comboBox_kapitel.currentText() is not "":
                    kapitel_shortcut = list(dict_klasse_name.keys())[
                        self.comboBox_kapitel.currentIndex() - 1
                    ]
                else:
                    kapitel_shortcut = ""

                if self.comboBox_unterkapitel.currentText() is not "":
                    shortcut = re.findall(
                        r"\((.*)\)", self.comboBox_unterkapitel.currentText()
                    )
                    unterkapitel_shortcut = shortcut[-1]
                else:
                    unterkapitel_shortcut = ""

                for all in beispieldaten_dateipfad_cria.keys():
                    file_path = beispieldaten_dateipfad_cria[all]
                    if str(list_klassen[self.comboBox_klassen.currentIndex()]) in file_path:
                        if kapitel_shortcut == "":
                            self.add_filename_to_list(list_mode, file_path, list_beispieldaten)
                        else:
                            if unterkapitel_shortcut == "":
                                if kapitel_shortcut in all:
                                    self.add_filename_to_list(list_mode, file_path, list_beispieldaten)
                            else:
                                thema_shortcut = (
                                    kapitel_shortcut + "." + unterkapitel_shortcut
                                )
                                if thema_shortcut in all:
                                    self.add_filename_to_list(list_mode, file_path, list_beispieldaten)


        if list_mode == "feedback":
            if self.chosen_program == 'lama':
                beispieldaten_dateipfad = eval(
                    "beispieldaten_dateipfad_%s" % self.comboBox_at_fb.currentText()[-1]
                )
                for all in beispieldaten_dateipfad.values():
                    filename_all = os.path.basename(all)
                    name, extension = os.path.splitext(filename_all)
                    if self.comboBox_at_fb.currentText()[-1] == "2":
                        if name.startswith(self.lineEdit_number_fb.text()):
                            list_beispieldaten.append(name)
                    else:
                        if (
                            name.startswith(self.comboBox_fb.currentText())
                            and self.comboBox_fb_num.currentText() in name
                        ):
                            number = name.split(" - ")
                            if (
                                self.lineEdit_number_fb.text() == ""
                                or number[1] == self.lineEdit_number_fb.text()
                            ):
                                list_beispieldaten.append(name)
                            # and self.lineEdit_number.text().lower() in name.lower()
            if self.chosen_program == 'cria':         
                dict_klasse_name = eval(
                    "dict_{}_name".format(
                        list_klassen[self.comboBox_klassen_fb_cria.currentIndex()]
                    )
                )
                if self.comboBox_kapitel_fb_cria.currentText() is not "":
                    kapitel_shortcut = list(dict_klasse_name.keys())[
                        self.comboBox_kapitel_fb_cria.currentIndex() - 1
                    ]
                else:
                    kapitel_shortcut = ""

                if self.comboBox_unterkapitel_fb_cria.currentText() is not "":
                    shortcut = re.findall(
                        r"\((.*)\)", self.comboBox_unterkapitel_fb_cria.currentText()
                    )
                    unterkapitel_shortcut = shortcut[-1]
                else:
                    unterkapitel_shortcut = ""

                for all in beispieldaten_dateipfad_cria.keys():
                    file_path = beispieldaten_dateipfad_cria[all]
                    if str(list_klassen[self.comboBox_klassen_fb_cria.currentIndex()]) in file_path:
                        if kapitel_shortcut == "":
                            self.add_filename_to_list(list_mode, file_path, list_beispieldaten)
                        else:
                            if unterkapitel_shortcut == "":
                                if kapitel_shortcut in all:
                                    self.add_filename_to_list(list_mode, file_path, list_beispieldaten)
                            else:
                                thema_shortcut = (
                                    kapitel_shortcut + "." + unterkapitel_shortcut
                                )
                                if thema_shortcut in all:
                                    self.add_filename_to_list(list_mode, file_path, list_beispieldaten)   


        list_beispieldaten = sorted(list_beispieldaten, key=natural_keys)
        for all in list_beispieldaten:
            if list_mode == "feedback" and all.startswith("_L_"):
                pass
            else:
                listWidget.addItem(all)
                listWidget.setFocusPolicy(QtCore.Qt.ClickFocus)

    def collect_all_infos_for_creating_file(self):
        self.dict_all_infos_for_file = {}
        #self.dict_list_input_examples = {}
        num_typ1 = 0
        num_typ2 = 0
        self.pkt_typ1 = 0
        self.pkt_typ2 = 0

        self.dict_all_infos_for_file["list_alle_aufgaben"] = self.list_alle_aufgaben_sage

        self.dict_all_infos_for_file["dict_alle_aufgaben"]= self.dict_alle_aufgaben_sage



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


        ### include basic data of test ###
        if self.combobox_beurteilung.currentIndex() == 0:
            beurteilung = "ns"
        if self.combobox_beurteilung.currentIndex() == 1:
            beurteilung = "br"


        try:
            self.num_ausgleichspkt_gesamt
        #     self.list_copy_images
        except AttributeError:
            self.num_ausgleichspkt_gesamt = 0
        #     self.list_copy_images = []

        dict_data_gesamt = {
            "program":self.chosen_program,
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
            "num_1": num_typ1,
            "punkte_1": self.pkt_typ1,
            "num_2": num_typ2,
            "punkte_2": self.pkt_typ2,
            "ausgleichspunkte": self.num_ausgleichspkt_gesamt,
            "copy_images": self.list_copy_images,
        }
        
        self.dict_all_infos_for_file["data_gesamt"] = dict_data_gesamt
        ### end ###


    def pushButton_vorschau_pressed(
        self, ausgabetyp, index=0, maximum=0, pdf=True, lama=True
    ):
        self.collect_all_infos_for_creating_file()


        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        dict_gesammeltedateien = {}

        if self.chosen_program=='lama':

            for all in self.beispieldaten_dateipfad_1.values():
                filename_all = os.path.basename(all)
                name, extension = os.path.splitext(filename_all)
                for files in self.list_alle_aufgaben_sage:
                    if files == name:
                        dict_gesammeltedateien[name] = all

            for all in self.beispieldaten_dateipfad_2.values():
                filename_all = os.path.basename(all)
                name, extension = os.path.splitext(filename_all)
                for files in self.list_alle_aufgaben_sage:
                    if files == name:
                        dict_gesammeltedateien[name] = all

        elif self.chosen_program == 'cria':
            for aufgabe in self.list_alle_aufgaben_sage:
                klasse, name = self.split_klasse_aufgabe(aufgabe)

                name = name + ".tex"
                
                for all in self.beispieldaten_dateipfad_cria:
                    filename_all = os.path.basename(all)
                    if klasse.upper() in all:
                        if name == os.path.basename(self.beispieldaten_dateipfad_cria[all]):
                            dict_gesammeltedateien[
                                aufgabe
                            ] = self.beispieldaten_dateipfad_cria[all]


        dict_months = {
            1: "Jänner",
            2: "Februar",
            3: "März",
            4: "April",
            5: "Mai",
            6: "Juni",
            7: "Juli",
            8: "August",
            9: "September",
            10: "Oktober",
            11: "November",
            12: "Dezember",
        }
        dict_wochentag = {
            0: "Montag",
            1: "Dienstag",
            2: "Mittwoch",
            3: "Donnerstag",
            4: "Freitag",
            5: "Samstag",
            6: "Sonntag",
        }

        # print(str(self.spinBox_nummer.value()) +str(self.dateEdit.date().day()) +'. '+dict_months[self.dateEdit.date().month()]+' '+ str(self.dateEdit.date().year()))
        raw_date = self.dict_all_infos_for_file["data_gesamt"]["Datum"]
        datum_kurz = (
            str(raw_date[2]) + ". " + str(raw_date[1]) + ". " + str(raw_date[0])
        )
        datum = (
            str(raw_date[2]) + ". " + dict_months[raw_date[1]] + " " + str(raw_date[0])
        )
        wochentag = dict_wochentag[
            datetime.datetime(raw_date[0], raw_date[1], raw_date[2]).weekday()
        ]
        datum = wochentag + ", " + datum

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
                # print(self.chosen_path_schularbeit_erstellen[0])

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

        dict_gruppen = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F"}

        if filename_vorschau == "":
            QtWidgets.QApplication.restoreOverrideCursor()
            return

        if self.chosen_program=='lama':
            dict_titlepage=self.dict_titlepage
        if self.chosen_program=='cria':
            dict_titlepage=self.dict_titlepage_cria


        vorschau = open(filename_vorschau, "w+", encoding="utf8")

        vorschau.write(
            "\documentclass[a4paper,12pt]{report}\n\n"
            "\\usepackage{geometry}\n"
            "\geometry{a4paper,left=18mm,right=18mm, top=2cm, bottom=2cm}\n\n"
            "\\usepackage{lmodern}\n"
            "\\usepackage[T1]{fontenc}\n"
            "\\usepackage[utf8]{inputenc}\n"
            "\\usepackage[ngerman]{babel}\n"
        )
        if ausgabetyp == "vorschau":
            if self.cb_solution_sage.isChecked() == True:
                vorschau.write(
                    "\\usepackage[solution_on]{srdp-mathematik} % solution_on/off\n"
                )
            else:
                vorschau.write(
                    "\\usepackage[solution_off]{srdp-mathematik} % solution_on/off\n"
                )
        if ausgabetyp == "schularbeit":
            if index % 2 == 0:
                vorschau.write(
                    "\\usepackage[solution_on]{srdp-mathematik} % solution_on/off\n"
                )
            if index % 2 == 1:
                vorschau.write(
                    "\\usepackage[solution_off]{srdp-mathematik} % solution_on/off\n"
                )
        if maximum > 2:
            comment = " %Gruppen: 0=A, 1=B, 2=C, ..."
        else:
            comment = ""

        vorschau.write(
            "\setcounter{{Zufall}}{{{0}}}{1}\n\n\n".format(int(index / 2), comment)
        )
        if ausgabetyp == "vorschau" or ausgabetyp == "schularbeit":
            vorschau.write("\pagestyle{plain} %PAGESTYLE: empty, plain\n")
        else:
            vorschau.write("\pagestyle{empty} %PAGESTYLE: empty, plain\n")
        vorschau.write(
            "\onehalfspacing %Zeilenabstand\n"
            "\setcounter{secnumdepth}{-1} % keine Nummerierung der Ueberschriften\n\n\n\n"
            "%\n"
            "%\n"
            "%%%%%%%%%%%%%%%%%% DOKUMENT - ANFANG %%%%%%%%%%%%%%%%%%%"
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
            "%\n"
            "%\n"
            "\\begin{document}\n"
        )

        if ausgabetyp == "schularbeit":
            gruppe = dict_gruppen[int(index / 2)]



        if (
            self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
            == "Grundkompetenzcheck"
        ):
            if ausgabetyp == "schularbeit" and maximum > 2:
                vorschau.write(
                    "\\textsc{{Grundkompetenzcheck -- {0}}} \\hfill \\textsc{{Name:}} \\rule{{8cm}}{{0.4pt}} \\normalsize \\\ \\vspace{{\\baselineskip}} \n\n".format(
                        gruppe
                    )
                )
            else:
                vorschau.write(
                    "\\textsc{Grundkompetenzcheck} \\hfill \\textsc{Name:} \\rule{8cm}{0.4pt} \\normalsize \\\ \\vspace{\\baselineskip} \n\n"
                )
        elif (
            self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
            == "Übungsblatt"
        ):
            vorschau.write("\\subsection{Übungsblatt}")
        
            

        else:
            try:
                dict_titlepage["hide_all"]
            except KeyError:
                dict_titlepage["hide_all"]=False
                titlepage_save = os.path.join(path_programm, "Teildokument", "titlepage_save")
                with open(titlepage_save, "w+", encoding="utf8") as f:
                    json.dump(dict_titlepage, f, ensure_ascii=False)



            if dict_titlepage["hide_all"] == True:
                if (
                    self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
                    == "Wiederholungsprüfung"
                ):
                    vorschau.write("\\textsc{{Name:}} \\rule{{8cm}}{{0.4pt}}"
                    "\\subsection{{{0} \\hfill {1}}}".format(self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"], datum_kurz)
                    )
                else:
                    vorschau.write("\\textsc{{Name:}} \\rule{{8cm}}{{0.4pt}}"
                    "\\subsection{{{0}. {1} \\hfill {2}}}".format(self.dict_all_infos_for_file["data_gesamt"]["#"],self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"], datum_kurz)
                    )  
            
            else:
                vorschau.write("\\begin{titlepage}\n" "\\flushright\n")
                if dict_titlepage["logo"] == True:
                    logo_name = os.path.basename(dict_titlepage["logo_path"])
                    logo_titlepage_path = os.path.join(
                        path_programm, "Teildokument", logo_name
                    )
                    if os.path.isfile(logo_titlepage_path):
                        vorschau.write(
                            "\\begin{{minipage}}[t]{{0.4\\textwidth}} \\vspace{{0pt}} \\includegraphics[width=1\\textwidth]{{{0}}}\\end{{minipage}} \\\ \\vfil \n".format(
                                logo_name
                            )
                        )
                    else:
                        msg = QtWidgets.QMessageBox()
                        msg.setIcon(QtWidgets.QMessageBox.Warning)
                        msg.setWindowIcon(QtGui.QIcon(logo_path))
                        msg.setText("Das Logo konnte nicht gefunden werden.")
                        msg.setInformativeText(
                            "Bitte suchen Sie ein Logo unter: \n\nTitelblatt anpassen - Durchsuchen"
                        )
                        msg.setWindowTitle("Kein Logo ausgewählt")
                        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        msg.exec_()

                        vorschau.write("~\\vfil \n")

                else:
                    vorschau.write("~\\vfil \n")
                if dict_titlepage["titel"] == True:
                    if (
                        self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
                        == "Wiederholungsprüfung"
                    ):
                        vorschau.write("\\textsc{{\\Huge Wiederholungsprüfung}} \\\ \n")
                    else:
                        vorschau.write(
                            "\\textsc{{\\Huge {0}. Mathematikschularbeit}} \\\ \n".format(
                                self.dict_all_infos_for_file["data_gesamt"]["#"]
                            )
                        )
                        if (
                            self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
                            == "Wiederholungsschularbeit"
                        ):
                            vorschau.write("[0.5cm]" "\\textsc{\Large Wiederholung} \\\ \n")
                        if (
                            self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
                            == "Nachschularbeit"
                        ):
                            vorschau.write(
                                "[0.5cm]" "\\textsc{\Large Nachschularbeit} \\\ \n"
                            )
                        vorschau.write("[2cm] \n")
                if dict_titlepage["datum"] == True:
                    vorschau.write("\\textsc{{\Large am {0}}}\\\ [1cm] \n".format(datum))
                if dict_titlepage["klasse"] == True:
                    vorschau.write(
                        "\\textsc{{\Large Klasse {0}}} \\\ [1cm] \n".format(
                            self.dict_all_infos_for_file["data_gesamt"]["Klasse"]
                        )
                    )

                if ausgabetyp == "schularbeit" and maximum > 2:
                    vorschau.write(
                        "\\textsc{{\\Large Gruppe {0}}} \\\ [1cm]\n".format(gruppe)
                    )

                if dict_titlepage["name"] == True:
                    vorschau.write("\\Large Name: \\rule{8cm}{0.4pt} \\\ \n")
                vorschau.write("\\vfil\\vfil\\vfil \n")
                if dict_titlepage["note"] == True:
                    vorschau.write("\\Large Note: \\rule{8cm}{0.4pt} \\\ [1cm]\n")
                if dict_titlepage["unterschrift"] == True:
                    vorschau.write("\\Large Unterschrift: \\rule{8cm}{0.4pt} \\\ \n")

                if self.dict_all_infos_for_file["data_gesamt"]["Beurteilung"] == "br":
                    exkl_teil2_pkt = (
                        self.dict_all_infos_for_file["data_gesamt"]["punkte_2"]
                        - self.dict_all_infos_for_file["data_gesamt"]["ausgleichspunkte"]
                    )
                    vorschau.write(
                        "\\newpage \n"
                        "\\flushleft \\normalsize\n"
                        "\\thispagestyle{{empty}}\n"
                        "\\beurteilungsraster{{0.85}}{{0.68}}{{0.5}}{{1/3}}{{ % Prozentschluessel\n"
                        "T1={{{0}}}, % Punkte im Teil 1\n"
                        "AP={{{1}}}, % Ausgleichspunkte aus Teil 2\n"
                        "T2={{{2}}}, % Punkte im Teil 2\n"
                        "}} \\newpage".format(
                            self.dict_all_infos_for_file["data_gesamt"]["punkte_1"],
                            self.dict_all_infos_for_file["data_gesamt"][
                                "ausgleichspunkte"
                            ],
                            exkl_teil2_pkt,
                        )
                    )

                vorschau.write("\\end{titlepage}\n\n")
        vorschau.close()

        vorschau = open(filename_vorschau, "a", encoding="utf8")
        list_chosen_examples = []

        control_counter = 0

        for aufgabe in self.list_alle_aufgaben_sage:
            if self.chosen_program == 'lama':
                typ=self.get_aufgabentyp(aufgabe)


                spinbox_pkt = self.dict_alle_aufgaben_sage[aufgabe][0]
                spinbox_abstand = self.dict_alle_aufgaben_sage[aufgabe][1]
                
                f = open(dict_gesammeltedateien[aufgabe], "r", encoding="utf8")
                content = f.readlines()
                f.close()


                ##### adapt content for	 creation ###

                if aufgabe in self.dict_all_infos_for_file["dict_ausgleichspunkte"].keys():
                    content = [line.replace("\\fbox{A}", "") for line in content]
                    for ausgleichspunkte in self.dict_all_infos_for_file[
                        "dict_ausgleichspunkte"
                    ][aufgabe]:
                        ausgleichspunkte = ausgleichspunkte.replace('ITEM','').replace('SUBitem','').strip()
                        if ausgleichspunkte.startswith('{'):
                            ausgleichspunkte = ausgleichspunkte[1:]
             
                        content = [
                            line.replace(
                                ausgleichspunkte.partition("\n")[0],
                                "\\fbox{A} " + ausgleichspunkte.partition("\n")[0],
                            )
                            for line in content
                        ]
                ### end ###

                if aufgabe in self.dict_all_infos_for_file["dict_hide_show_items"].keys():
                    # print(content)        
                    for item in self.dict_all_infos_for_file["dict_hide_show_items"][aufgabe]:
                        hide_item = item.split('\n')[0]
                        hide_item = hide_item.replace('ITEM','').replace('SUBitem','').strip()

                        start_index=-1
                        end_index=-1
                        for idx, line in enumerate(content):
                            if start_index == -1:
                                if hide_item in line:
                                    start_index=idx
                                    continue
                            else:
                                if '\\item' in line:
                                    end_index=idx
                                    break
                                if "\\end{aufgabenstellung}" in line:
                                    end_index=idx
                                    break
                                if "Lösungserwartung" in line:
                                    break
                        if start_index==-1 or end_index==-1:
                            warning_window("Das Ein- bzw. Ausblenden von Aufgabenstellungen in Aufgabe {} konnte leider nicht durchgeführt werden.\n"
                            "Die Aufgabe wird daher vollständig angezeigt. Bitte bearbeiten sie diese Aufgabe manuell.".format(aufgabe))                
                        else:
                            for i in reversed(range(start_index+1)):
                                if '\\item' in content[i]:         
                                    start_index=i
                                    break
                            for index, line in enumerate(content[start_index:end_index]):
                                content[start_index+index]='% '+line

                            # del content[start_index:end_index]

            if self.chosen_program == 'cria':
                # bsp_string=all
                # list_input = "self.list_input_{}".format(bsp_string)
                spinbox_pkt = self.dict_alle_aufgaben_sage[aufgabe][0]
                spinbox_abstand = self.dict_alle_aufgaben_sage[aufgabe][1]
                
                f = open(dict_gesammeltedateien[aufgabe], "r", encoding="utf8")
                content = f.readlines()
                f.close()             


            if ausgabetyp == "schularbeit":
                if index == 0:
                    if dict_titlepage["logo"] == True:
                        logo_name = os.path.basename(dict_titlepage["logo_path"])
                        logo_titlepage_path = os.path.join(
                            path_programm, "Teildokument", logo_name
                        )
                        if os.path.isfile(logo_titlepage_path):
                            shutil.copy(
                                logo_titlepage_path,
                                os.path.join(
                                    os.path.dirname(
                                        self.chosen_path_schularbeit_erstellen[0]
                                    ),
                                    logo_name,
                                ),
                            )
                        else:
                            warning_window("Das Logo konnte nicht gefunden werden.", 
                            "Bitte suchen Sie ein Logo unter: \n\nTitelblatt anpassen - Durchsuchen",
                            "Kein Logo ausgewählt")


                    if (
                        self.dict_all_infos_for_file["data_gesamt"]["copy_images"]
                        == []
                    ):
                        pass
                    else:
                        for image in self.dict_all_infos_for_file["data_gesamt"][
                            "copy_images"
                        ]:
                            if os.path.isfile(
                                os.path.join(
                                    path_programm, "_database", "Bilder", image
                                )
                            ):
                                shutil.copy(
                                    os.path.join(
                                        path_programm, "_database", "Bilder", image
                                    ),
                                    os.path.join(
                                        os.path.dirname(
                                            self.chosen_path_schularbeit_erstellen[0]
                                        ),
                                        image,
                                    ),
                                )

                            elif os.path.isfile(
                                os.path.join(
                                    path_programm,
                                    "_database_inoffiziell",
                                    "Bilder",
                                    image,
                                )
                            ):
                                shutil.copy(
                                    os.path.join(
                                        path_programm,
                                        "_database_inoffiziell",
                                        "Bilder",
                                        image,
                                    ),
                                    os.path.join(
                                        os.path.dirname(
                                            self.chosen_path_schularbeit_erstellen[0]
                                        ),
                                        image,
                                    ),
                                )

                            elif os.path.isfile(
                                os.path.join(
                                    path_programm,
                                    "Beispieleinreichung",
                                    "Bilder",
                                    image,
                                )
                            ):
                                shutil.copy(
                                    os.path.join(
                                        path_programm,
                                        "Beispieleinreichung",
                                        "Bilder",
                                        image,
                                    ),
                                    os.path.join(
                                        os.path.dirname(
                                            self.chosen_path_schularbeit_erstellen[0]
                                        ),
                                        image,
                                    ),
                                )


                for image in self.dict_all_infos_for_file["data_gesamt"][
                    "copy_images"
                ]:
                    content = [
                        line.replace("../_database/Bilder/", "") for line in content
                    ]
                    content = [
                        line.replace("../_database_inoffiziell/Bilder/", "")
                        for line in content
                    ]
                    content = [
                        line.replace("../Beispieleinreichung/Bilder/", "")
                        for line in content
                    ]


            for line in content:
                if "begin{beispiel}" in line:
                    beginning = line
                    start = content.index(line) + 1
                    beispiel_typ = "beispiel"
                if "begin{langesbeispiel}" in line:
                    beginning = line
                    start = content.index(line) + 1
                    beispiel_typ = "langesbeispiel"

                if "end{beispiel}" in line or "end{langesbeispiel}" in line:
                    ending = line
                    end = content.index(line)

            content = content[start:end]
            joined_content = "".join(content)
            sub_list = []
            sub_list.append(beginning)
            sub_list.append(joined_content)
            sub_list.append(ending)
            list_chosen_examples.append(sub_list)

            example = list_chosen_examples[self.list_alle_aufgaben_sage.index(aufgabe)]
            try:
                x, y = example[0].split("[")
                gk, z = y.split("]")
            except ValueError:
                gk = ""

            if (
                self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
                == "Grundkompetenzcheck"
                or self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
                == "Übungsblatt"
            ):
                header = ""
            else:
                if self.change_program=='lama' and control_counter == 0 and typ == 1:
                    header = "\\subsubsection{Typ 1 Aufgaben}\n\n"
                    control_counter += 1
                elif self.change_program=='lama' and control_counter == 1 and typ == 2:
                    header = "\\subsubsection{Typ 2 Aufgaben}\n\n"
                    control_counter += 1
                else:
                    header = ""

            if beispiel_typ == "beispiel":
                if gk == "":
                    vorschau.write(
                        "%s\\begin{beispiel}{" % header
                        + str(spinbox_pkt)
                        + "}\n"
                        + example[1]
                        + "\n"
                        + example[2]
                        + "\n\n"
                    )

                else:
                    vorschau.write(
                        "%s\\begin{beispiel}[" % header
                        + gk
                        + "]{"
                        + str(spinbox_pkt)
                        + "}\n"
                        + example[1]
                        + "\n"
                        + example[2]
                        + "\n\n"
                    )

            elif self.chosen_program=='lama' and beispiel_typ == "langesbeispiel":
                vorschau.write(
                    "\\newpage\n\n%s\\begin{langesbeispiel} \item[" % header
                    + str(spinbox_pkt)
                    + "]\n"
                    + example[1]
                    + "\n"
                    + example[2]
                    + "\n\n"
                )

            elif self.chosen_program=='cria' and beispiel_typ == "langesbeispiel":
                vorschau.write(
                    "\\begin{langesbeispiel} \item["
                    + str(spinbox_pkt)
                    + "]\n"
                    + example[1]
                    + "\n"
                    + example[2]
                    + "\n\n"
                )

            if spinbox_abstand != 0:
                if spinbox_abstand == 99:
                    vorschau.write("\\newpage \n\n")
                else:
                    vorschau.write("\\vspace{" + str(spinbox_abstand) + "cm} \n\n")

        if (
            self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
            != "Grundkompetenzcheck"
            and self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
            != "Übungsblatt"
        ):
            if self.dict_all_infos_for_file["data_gesamt"]["Beurteilung"] == "ns":
                notenschluessel = self.dict_all_infos_for_file["data_gesamt"][
                    "Notenschluessel"
                ]
                vorschau.write(
                    "\n\n\\notenschluessel{{{0}}}{{{1}}}{{{2}}}{{{3}}}".format(
                        notenschluessel[0] / 100,
                        notenschluessel[1] / 100,
                        notenschluessel[2] / 100,
                        notenschluessel[3] / 100,
                    )
                )
        vorschau.write("\n\n\end{document}")
        vorschau.close()

        # MainWindow.hide()
        # msg.setIcon(QtWidgets.QMessageBox.Question)
        # msg.setInformativeText('Möchten Sie das neue Update installieren?')

        if ausgabetyp == "vorschau":
            if sys.platform.startswith("linux"):
                MainWindow.hide()
            create_pdf("Schularbeit_Vorschau", 0, 0)
            if sys.platform.startswith("linux"):
                MainWindow.show()
        if ausgabetyp == "schularbeit":
            name, extension = os.path.splitext(filename_vorschau)

            if pdf == True:
                if sys.platform.startswith("linux"):
                    MainWindow.hide()

                create_pdf(name, index, maximum)
                if sys.platform.startswith("linux"):
                    MainWindow.show()

                if maximum > 2:
                    if index % 2 == 0:
                        shutil.move(
                            name + ".pdf",
                            name
                            + "_{}_Loesung.pdf".format(dict_gruppen[int(index / 2)]),
                        )
                    else:
                        shutil.move(
                            name + ".pdf",
                            name + "_{}.pdf".format(dict_gruppen[int(index / 2)]),
                        )
                else:
                    if index % 2 == 0:
                        shutil.move(name + ".pdf", name + "_Loesung.pdf")

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

        # sys.exit[0]

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
        if self.comboBox_at_fb.currentText() == "Allgemeine Rückmeldung":
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
                warning_window(
                    "Bitte geben Sie nähere Informationen im Textfeld an."
                )
                return

        if self.plainTextEdit_fb.toPlainText() == "":
            description = "keine Angabe"
        else:
            description = self.plainTextEdit_fb.toPlainText()
        if self.lineEdit_email.text() == "":
            contact = "keine Angabe"
        else:
            contact = self.lineEdit_email.text()

        if self.chosen_program=='cria':
            programm='LaMA-Cria - '
        else:
            programm=''
        content = "Subject: {0}{1}: {2}\n\nProblembeschreibung:\n\n{3}\n\n\nKontakt: {4}".format(
            programm, example, fehler, description, contact
        )

        gmail_user = "lamabugfix@gmail.com"
        try:
            fbpassword_path = os.path.join(path_programm, "_database", "_config")
            fbpassword_file = os.path.join(fbpassword_path, "fbpassword.txt")
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
                warning_window(
                    "Das eingebene Passwort ist nicht korrekt!",
                    "Bitte kontaktieren Sie den Support für nähere Informationen:\n\nlama.helpme@gmail.com",
                )
            else:
                warning_window(
                    "Die Meldung konnte leider nicht gesendet werden!",
                    "Überprüfen Sie Ihre Internetverbindung oder versuchen Sie es später erneut.",
                )

    #######################################################################
    ##########################################################################
    ############################################################################

    def pushButton_erstellen_pressed(self):
        self.collect_all_infos_for_creating_file()
        try:
            self.saved_file_path
        except AttributeError:
            self.saved_file_path = path_programm

        if self.chosen_program=='lama':
            dict_titlepage=self.dict_titlepage
        if self.chosen_program=='cria':
            dict_titlepage=self.dict_titlepage_cria

        self.open_dialogwindow_erstellen(
            self.dict_all_infos_for_file,
            self.beispieldaten_dateipfad_1,
            self.beispieldaten_dateipfad_2,
            dict_titlepage,
            self.saved_file_path,
        )


    def update_gui(self, chosen_gui):
        if self.chosen_program=='cria':
            chosen_gui=eval(chosen_gui+'_cria')
        else:
            chosen_gui=eval(chosen_gui)

        MainWindow.setMenuBar(self.menuBar)
        list_delete=[]
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

        if chosen_gui==widgets_sage or chosen_gui==widgets_sage_cria:
            MainWindow.setTabOrder(self.spinBox_nummer, self.dateEdit)
            MainWindow.setTabOrder(self.dateEdit, self.lineEdit_klasse)
            self.adapt_choosing_list("sage")
            self.listWidget.itemClicked.connect(self.nummer_clicked)
        if chosen_gui==widgets_feedback or chosen_gui==widgets_feedback_cria:
            self.adapt_choosing_list("feedback")
            self.listWidget_fb.itemClicked.connect(self.nummer_clicked_fb)
            self.listWidget_fb_cria.itemClicked.connect(self.nummer_clicked_fb)                                          


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle('Fusion')
    app.setStyleSheet("""QToolTip {{ color: white; background-color: {0}; border: 0px; }}
    """.format(get_color(blue_7)))
    # font = QtGui.QFont("Calibri Light", 9)
    # app.setFont(font)
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, white) # Window background
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.black) 
    palette.setColor(QtGui.QPalette.Base, white)
    palette.setColor(QtGui.QPalette.AlternateBase, blue_2)
    palette.setColor(QtGui.QPalette.ToolTipBase, white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, blue_6)
    palette.setColor(QtGui.QPalette.Button, blue_3) #blue_4

    # palette.setColor(QtGui.QPalette.Inactive,QtGui.QPalette.WindowText, gray)
    palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.WindowText, QtCore.Qt.darkGray)
    # palette.setColor(QtGui.QPalette.Disabled,QtGui.QPalette.Base, QtCore.Qt.gray)
    # palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    # palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
         
    palette.setColor(QtGui.QPalette.Highlight, blue_7)
    palette.setColor(QtGui.QPalette.HighlightedText, white)
    app.setPalette(palette)

    MainWindow = QMainWindow()
    screen_resolution = app.desktop().screenGeometry()
    screen_width, screen_height = screen_resolution.width(), screen_resolution.height()

    MainWindow.setGeometry(30, 30, screen_width * 0.5, screen_height * 0.8)
    MainWindow.move(30, 30)

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()

    sys.exit(app.exec_())
