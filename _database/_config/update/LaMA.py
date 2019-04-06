#!/usr/bin/python3
# -*- coding: utf-8 -*-
#### Version number ###
__version__='v1.4'
__lastupdate__='04/19'
####################

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
import time
import threading
import sys
import os 
import os.path
from pathlib import Path
import datetime
import json
import subprocess
import shutil
import re
import functools
import yaml
from PIL import Image ## pillow


path_programm=os.path.dirname(sys.argv[0])

if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    if path_programm is '':
        path_programm = "."

print('Loading...')

# Load Config-file
def config_loader(pathToFile,parameter):
    for i in range(5):
        try:
            config1 = yaml.safe_load(open(pathToFile, encoding='utf8'))
            break
        except FileNotFoundError:
            print("File not Found!")
            if sys.platform.startswith('linux'):
                    root = "."
            else:
                    root = ""
            config_path = os.path.join('.','_database','_config')
            if not os.path.exists(config_path):
                print("No worries, we'll create the structure for you.")
                os.makedirs(config_path)
            input("Please place your your config file in '{}' and hit enter. {} tries left!".format(config_path, 5-i))
    return config1[parameter]

config_file = os.path.join(path_programm,'_database','_config','config1.yml')

ag_beschreibung = config_loader(config_file,'ag_beschreibung')
an_beschreibung = config_loader(config_file,'an_beschreibung')
fa_beschreibung = config_loader(config_file,'fa_beschreibung')
ws_beschreibung = config_loader(config_file,'ws_beschreibung')

k5_beschreibung = config_loader(config_file,'k5_beschreibung')
k6_beschreibung = config_loader(config_file,'k6_beschreibung')
k7_beschreibung = config_loader(config_file,'k7_beschreibung')
k8_beschreibung = config_loader(config_file,'k8_beschreibung')

dict_gk = config_loader(config_file,'dict_gk')
dict_aufgabenformate = config_loader(config_file,'dict_aufgabenformate')
Klassen = config_loader(config_file,'Klassen')




try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtWidgets.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtWidgets.QApplication.translate(context, text, disambig)

logo_path=os.path.join(path_programm,'_database','_config','magnifier.png')


widgets_search=['actionRefresh_Database','menuDateityp','menuNeu','menuHelp','label_update','combobox_searchtype','label_aufgabentyp','groupBox_ausgew_gk','groupBox_af',
'groupBox_gk','groupBox_klassen','groupBox_themen_klasse','groupBox_titelsuche','cb_solution','btn_suche'] #'centralwidget'

widgets_create=['menuBild_einf_gen','menuSuche','menuHelp','groupBox_aufgabentyp','groupBox_ausgew_gk_cr','groupBox_bilder',
'groupBox_2', 'groupBox_grundkompetenzen_cr', 'groupBox_punkte','groupBox_klassen_cr','groupBox_aufgabenformat','groupBox_beispieleingabe',
'groupBox_quelle','pushButton_save'] 

dict_picture_path={}
set_chosen_gk=set([])
class Ui_MainWindow(object):
	global dict_picture_path, set_chosen_gk
	def setupUi(self, MainWindow):
		self.check_for_update()	
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(1000, 500)
		MainWindow.move(30,30)
		# MainWindow.setMaximumSize(QtCore.QSize(1078, 16777215))
		MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
		MainWindow.setStyleSheet(_fromUtf8(""))
		MainWindow.setWindowIcon(QtGui.QIcon(logo_path))
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
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
		self.menuSuche = QtWidgets.QMenu(self.menuBar)
		self.menuSuche.setObjectName(_fromUtf8("menuSuche"))
		self.menuHelp = QtWidgets.QMenu(self.menuBar)
		self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
		self.menuBild_einf_gen = QtWidgets.QMenu(self.menuBar)
		self.menuBild_einf_gen.setObjectName(_fromUtf8("menuBild_einf_gen"))
		self.actionBild_einf_gen = QtWidgets.QAction(MainWindow)
		self.actionBild_einf_gen.setObjectName(_fromUtf8("actionBild_einf_gen"))
		self.actionBild_konvertieren_jpg_eps = QtWidgets.QAction(MainWindow)
		self.actionBild_konvertieren_jpg_eps.setObjectName(_fromUtf8("actionBild_konvertieren_jpg_eps"))
		MainWindow.setMenuBar(self.menuBar)
		self.actionReset = QtWidgets.QAction(MainWindow)
		self.actionReset.setObjectName(_fromUtf8("actionReset"))
		self.actionAufgaben_Typ1 = QtWidgets.QAction(MainWindow)
		self.actionAufgaben_Typ1.setObjectName(_fromUtf8("actionAufgaben_Typ1"))
		self.actionAufgaben_Typ2 = QtWidgets.QAction(MainWindow)
		self.actionAufgaben_Typ2.setObjectName(_fromUtf8("actionAufgaben_Typ2"))
		self.actionRefresh_Database = QtWidgets.QAction(MainWindow)
		self.actionRefresh_Database.setObjectName(_fromUtf8("actionRefresh_Database"))
		self.actionsuchfenster_reset = QtWidgets.QAction(MainWindow)
		self.actionsuchfenster_reset.setObjectName(_fromUtf8("actionsuchfenster_reset"))
		self.actionNeu = QtWidgets.QAction(MainWindow)
		self.actionNeu.setObjectName(_fromUtf8("actionNeu"))
		self.actionSuche = QtWidgets.QAction(MainWindow)
		self.actionSuche.setObjectName(_fromUtf8("actionSuche"))		
		self.actionInfo = QtWidgets.QAction(MainWindow)
		self.actionInfo.setObjectName(_fromUtf8("actionInfo"))
		self.actionExit = QtWidgets.QAction(MainWindow)
		self.actionExit.setObjectName(_fromUtf8("actionExit"))
		self.menuDateityp.addAction(self.actionAufgaben_Typ1)
		self.menuDateityp.addAction(self.actionAufgaben_Typ2)
		self.menuHelp.addAction(self.actionInfo)
		self.menuDatei.addAction(self.actionRefresh_Database)
		self.menuDatei.addAction(self.actionsuchfenster_reset)
		self.menuDatei.addSeparator()
		self.menuDatei.addAction(self.actionExit)
		self.menuNeu.addAction(self.actionNeu)
		self.menuSuche.addAction(self.actionSuche)
		self.menuBar.addAction(self.menuDatei.menuAction())
		self.menuBar.addAction(self.menuDateityp.menuAction())
		self.menuBar.addAction(self.menuNeu.menuAction())
		self.menuBild_einf_gen.addAction(self.actionBild_einf_gen)
		self.menuBild_einf_gen.addSeparator()
		self.menuBild_einf_gen.addAction(self.actionBild_konvertieren_jpg_eps)
		self.menuBar.addAction(self.menuHelp.menuAction())
		self.groupBox_ausgew_gk = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_ausgew_gk.setObjectName(_fromUtf8("groupBox_ausgew_gk"))
		self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_ausgew_gk)
		self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
		self.label_gk = QtWidgets.QLabel(self.groupBox_ausgew_gk)
		self.label_gk.setWordWrap(True)
		self.label_gk.setObjectName(_fromUtf8("label_gk"))
		self.verticalLayout_2.addWidget(self.label_gk)
		self.label_gk_rest = QtWidgets.QLabel(self.groupBox_ausgew_gk)
		self.label_gk_rest.setWordWrap(False)
		self.label_gk_rest.setObjectName(_fromUtf8("label_gk_rest"))
		self.verticalLayout_2.addWidget(self.label_gk_rest)
		self.gridLayout.addWidget(self.groupBox_ausgew_gk, 3, 3, 1, 1)
		self.groupBox_titelsuche = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_titelsuche.setObjectName(_fromUtf8("groupBox_titelsuche"))
		self.gridLayout_10 = QtWidgets.QGridLayout(self.groupBox_titelsuche)
		self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
		self.entry_suchbegriffe = QtWidgets.QLineEdit(self.groupBox_titelsuche)
									 
		self.entry_suchbegriffe.setObjectName(_fromUtf8("entry_suchbegriffe"))
		self.gridLayout_10.addWidget(self.entry_suchbegriffe, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.groupBox_titelsuche, 4, 3, 1, 1)
		self.groupBox_klassen = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_klassen.setMaximumSize(QtCore.QSize(367, 16777215))
		self.groupBox_klassen.setObjectName(_fromUtf8("groupBox_klassen"))
		self.gridLayout_14 = QtWidgets.QGridLayout(self.groupBox_klassen)
		self.gridLayout_14.setObjectName(_fromUtf8("gridLayout_14"))
		self.cb_k5 = QtWidgets.QCheckBox(self.groupBox_klassen)
											  
		self.cb_k5.setObjectName(_fromUtf8("cb_k5"))
		self.gridLayout_14.addWidget(self.cb_k5, 0, 0, 1, 1)
		self.cb_k7 = QtWidgets.QCheckBox(self.groupBox_klassen)
		self.cb_k7.setObjectName(_fromUtf8("cb_k7"))
		self.gridLayout_14.addWidget(self.cb_k7, 0, 1, 1, 1)
		self.cb_k6 = QtWidgets.QCheckBox(self.groupBox_klassen)
		self.cb_k6.setObjectName(_fromUtf8("cb_k6"))
		self.gridLayout_14.addWidget(self.cb_k6, 1, 0, 1, 1)
		self.cb_k8 = QtWidgets.QCheckBox(self.groupBox_klassen)
		self.cb_k8.setObjectName(_fromUtf8("cb_k8"))
		self.gridLayout_14.addWidget(self.cb_k8, 1, 1, 1, 1)
		self.cb_mat = QtWidgets.QCheckBox(self.groupBox_klassen)
		self.cb_mat.setObjectName(_fromUtf8("cb_mat"))
		self.gridLayout_14.addWidget(self.cb_mat, 0, 2, 1, 1)
		self.gridLayout.addWidget(self.groupBox_klassen, 3, 0, 1, 1)
		self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
		self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
		self.cb_solution = QtWidgets.QCheckBox(self.centralwidget)
		self.cb_solution.setObjectName(_fromUtf8("cb_solution"))
		self.cb_solution.setChecked(True)
		self.horizontalLayout_2.addWidget(self.cb_solution, QtCore.Qt.AlignLeft)
		self.btn_suche = QtWidgets.QPushButton(self.centralwidget)
		self.btn_suche.setEnabled(True)
		self.btn_suche.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
		self.btn_suche.setAcceptDrops(False)
		self.btn_suche.setObjectName(_fromUtf8("btn_suche"))
		self.horizontalLayout_2.addWidget(self.btn_suche)
		self.gridLayout.addLayout(self.horizontalLayout_2, 5, 3, 1, 1)
		self.horizontalLayout = QtWidgets.QHBoxLayout()
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		# self.btn_refreshddb = QtWidgets.QPushButton(self.centralwidget)
		# self.btn_refreshddb.setObjectName(_fromUtf8("btn_refreshddb"))
		# self.horizontalLayout.addWidget(self.btn_refreshddb)
		self.label_update = QtWidgets.QLabel(self.centralwidget)
		self.label_update.setObjectName(_fromUtf8("label_update"))
		self.horizontalLayout.addWidget(self.label_update)
		#self.label_update.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
		self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
		self.horizontalLayout_combobox = QtWidgets.QHBoxLayout()
		self.horizontalLayout_combobox.setObjectName(_fromUtf8("horizontalLayout_combobox"))
		self.label_aufgabentyp = QtWidgets.QLabel(self.centralwidget)
		self.label_aufgabentyp.setObjectName(_fromUtf8("label_aufgabentyp"))
		self.horizontalLayout_combobox.addWidget(self.label_aufgabentyp)
		self.combobox_searchtype = QtWidgets.QComboBox(self.centralwidget)
		self.combobox_searchtype.setEnabled(True)
		self.combobox_searchtype.setObjectName(_fromUtf8("combobox_searchtype"))
		self.combobox_searchtype.addItem(_fromUtf8(""))
		self.combobox_searchtype.addItem(_fromUtf8(""))
		self.horizontalLayout_combobox.addWidget(self.combobox_searchtype)
		self.gridLayout.addLayout(self.horizontalLayout_combobox, 0, 3, 1, 1)
		self.combobox_searchtype.hide()
		self.groupBox_themen_klasse = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_themen_klasse.setMaximumSize(QtCore.QSize(367, 16777215))
		self.groupBox_themen_klasse.setObjectName(_fromUtf8("groupBox_themen_klasse"))
		self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_themen_klasse)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.tabWidget = QtWidgets.QTabWidget(self.groupBox_themen_klasse)
		self.tabWidget.setStyleSheet(_fromUtf8("background-color: rgb(229, 246, 255);"))
		self.tabWidget.setMovable(False)
		self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
		self.verticalLayout.addWidget(self.tabWidget)
		self.gridLayout.addWidget(self.groupBox_themen_klasse, 1, 0, 2, 1)
		self.groupBox_gk = QtWidgets.QGroupBox(self.centralwidget)													  
		self.groupBox_gk.setObjectName(_fromUtf8("groupBox_gk"))
		self.gridLayout_11 = QtWidgets.QGridLayout(self.groupBox_gk)
		self.gridLayout_11.setObjectName(_fromUtf8("gridLayout_11"))
		self.tab_widget_gk = QtWidgets.QTabWidget(self.groupBox_gk)
		#self.tab_widget_gk.setMaximumSize(QtCore.QSize(650, 16777215))
		self.tab_widget_gk.setStyleSheet(_fromUtf8("background-color: rgb(217, 255, 215);"))
		self.tab_widget_gk.setObjectName(_fromUtf8("tab_widget_gk"))


		#### AG #####
		self.tab_ag = QtWidgets.QWidget()
		self.tab_ag.setObjectName(_fromUtf8("tab_ag"))
		self.gridLayout_ag = QtWidgets.QGridLayout(self.tab_ag)
		self.gridLayout_ag.setObjectName(_fromUtf8("gridLayout_ag"))
		self.btn_ag_all = QtWidgets.QPushButton(self.tab_ag)
		self.btn_ag_all.setStyleSheet(_fromUtf8("background-color: rgb(240, 240, 240);"))
		self.btn_ag_all.setObjectName(_fromUtf8("btn_ag_all"))
		self.gridLayout_ag.addWidget(self.btn_ag_all, 10, 2, 1, 1)
		self.btn_ag_all.setMinimumSize(QtCore.QSize(100,0))
		self.btn_ag_all.setMaximumSize(QtCore.QSize(100,16777215))
		self.tab_widget_gk.addTab(self.tab_ag, _fromUtf8(""))
		self.create_checkbox_gk('ag', ag_beschreibung)

		### FA ###
		self.tab_fa = QtWidgets.QWidget()
		self.tab_fa.setObjectName(_fromUtf8("tab_fa"))
		self.gridLayout_fa = QtWidgets.QGridLayout(self.tab_fa)
		self.gridLayout_fa.setObjectName(_fromUtf8("gridLayout_fa"))
		self.btn_fa_all = QtWidgets.QPushButton(self.tab_fa)
		self.btn_fa_all.setStyleSheet(_fromUtf8("background-color: rgb(240, 240, 240);"))
		self.btn_fa_all.setObjectName(_fromUtf8("btn_fa_all"))
		self.gridLayout_fa.addWidget(self.btn_fa_all, 10, 3, 1, 1)
		self.btn_fa_all.setMinimumSize(QtCore.QSize(100,0))
		self.btn_fa_all.setMaximumSize(QtCore.QSize(100,16777215))
		self.tab_widget_gk.addTab(self.tab_fa, _fromUtf8(""))
		self.create_checkbox_gk('fa',fa_beschreibung)

		### AN ###
		self.tab_an = QtWidgets.QWidget()
		self.tab_an.setObjectName(_fromUtf8("tab_an"))
		self.gridLayout_an = QtWidgets.QGridLayout(self.tab_an)
		self.gridLayout_an.setObjectName(_fromUtf8("gridLayout_an"))
		self.btn_an_all = QtWidgets.QPushButton(self.tab_an)
		self.btn_an_all.setStyleSheet(_fromUtf8("background-color: rgb(240, 240, 240);"))
		self.btn_an_all.setObjectName(_fromUtf8("btn_an_all"))
		self.gridLayout_an.addWidget(self.btn_an_all, 10, 3, 1, 1)
		self.btn_an_all.setMinimumSize(QtCore.QSize(100,0))
		self.btn_an_all.setMaximumSize(QtCore.QSize(100,16777215))
		self.tab_widget_gk.addTab(self.tab_an, _fromUtf8(""))
		self.create_checkbox_gk('an', an_beschreibung)


		### WS ###
		self.tab_ws = QtWidgets.QWidget()
		self.tab_ws.setObjectName(_fromUtf8("tab_ws"))
		self.gridLayout_ws = QtWidgets.QGridLayout(self.tab_ws)
		self.gridLayout_ws.setObjectName(_fromUtf8("gridLayout_ws"))
		self.btn_ws_all = QtWidgets.QPushButton(self.tab_ws)
		self.btn_ws_all.setStyleSheet(_fromUtf8("background-color: rgb(240, 240, 240);"))
		self.btn_ws_all.setObjectName(_fromUtf8("btn_ws_all"))
		self.gridLayout_ws.addWidget(self.btn_ws_all, 10, 2, 1, 1)
		self.btn_ws_all.setMinimumSize(QtCore.QSize(100,0))
		self.btn_ws_all.setMaximumSize(QtCore.QSize(100,16777215))
		self.tab_widget_gk.addTab(self.tab_ws, _fromUtf8(""))
		self.create_checkbox_gk('ws',ws_beschreibung)

		######### Klassenthemen
		### K5
		self.tab_k5 = QtWidgets.QWidget()
		self.tab_k5.setObjectName(_fromUtf8("tab_k5"))
		self.gridLayout_k5 = QtWidgets.QGridLayout(self.tab_k5)
		self.gridLayout_k5.setObjectName(_fromUtf8("gridLayout_k5"))
		self.tabWidget.addTab(self.tab_k5, _fromUtf8(""))
		self.create_checkbox_klasse('k5',k5_beschreibung)
		### K6
		self.tab_k6 = QtWidgets.QWidget()
		self.tab_k6.setObjectName(_fromUtf8("tab_k6"))
		self.gridLayout_k6 = QtWidgets.QGridLayout(self.tab_k6)
		self.gridLayout_k6.setObjectName(_fromUtf8("gridLayout_k6"))
		self.tabWidget.addTab(self.tab_k6, _fromUtf8(""))
		self.create_checkbox_klasse('k6',k6_beschreibung)
		### K7
		self.tab_k7 = QtWidgets.QWidget()
		self.tab_k7.setObjectName(_fromUtf8("tab_k7"))
		self.gridLayout_k7 = QtWidgets.QGridLayout(self.tab_k7)
		self.gridLayout_k7.setObjectName(_fromUtf8("gridLayout_k7"))
		self.create_checkbox_klasse('k7',k7_beschreibung)
		self.tabWidget.addTab(self.tab_k7, _fromUtf8(""))
		### K8
		self.tab_k8 = QtWidgets.QWidget()
		self.tab_k8.setObjectName(_fromUtf8("tab_k8"))
		self.gridLayout_k8 = QtWidgets.QGridLayout(self.tab_k8)
		self.gridLayout_k8.setObjectName(_fromUtf8("gridLayout_k8"))
		self.tabWidget.addTab(self.tab_k8, _fromUtf8(""))
		self.create_checkbox_klasse('k8',k8_beschreibung)
		
		##############################################################
		#####################CREATOR #########################################
		##########################################################################


		self.groupBox_aufgabentyp = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_aufgabentyp.setObjectName(_fromUtf8("groupBox_aufgabentyp"))
		self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_aufgabentyp)
		self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
		self.comboBox_aufgabentyp_cr = QtWidgets.QComboBox(self.groupBox_aufgabentyp)
		self.comboBox_aufgabentyp_cr.setObjectName(_fromUtf8("comboBox_aufgabentyp_cr"))
		self.comboBox_aufgabentyp_cr.addItem(_fromUtf8(""))
		self.comboBox_aufgabentyp_cr.addItem(_fromUtf8(""))
		self.gridLayout_3.addWidget(self.comboBox_aufgabentyp_cr, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.groupBox_aufgabentyp, 1, 2, 1, 1)
		self.groupBox_aufgabentyp.setTitle(_translate("MainWindow", "Aufgabentyp", None))
		self.comboBox_aufgabentyp_cr.setItemText(0, _translate("MainWindow", "Typ 1", None))
		self.comboBox_aufgabentyp_cr.setItemText(1, _translate("MainWindow", "Typ 2", None))
		self.groupBox_aufgabentyp.hide()


		self.groupBox_grundkompetenzen_cr = QtWidgets.QGroupBox(self.centralwidget)
		# self.groupBox_grundkompetenzen_cr.setMaximumSize(QtCore.QSize(350, 16777215))
		self.groupBox_grundkompetenzen_cr.setObjectName(_fromUtf8("groupBox_grundkompetenzen_cr"))
		self.gridLayout_11_cr = QtWidgets.QGridLayout(self.groupBox_grundkompetenzen_cr)
		self.gridLayout_11_cr.setObjectName(_fromUtf8("gridLayout_11_cr"))
		self.tab_widget_gk_cr = QtWidgets.QTabWidget(self.groupBox_grundkompetenzen_cr)
		self.tab_widget_gk_cr.setStyleSheet(_fromUtf8("background-color: rgb(217, 255, 215);"))
		self.tab_widget_gk_cr.setObjectName(_fromUtf8("tab_widget_gk_cr"))
		self.gridLayout_11_cr.addWidget(self.tab_widget_gk_cr, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.groupBox_grundkompetenzen_cr, 1, 0, 5, 1)
		self.groupBox_grundkompetenzen_cr.setTitle(_translate("MainWindow", "Grundkompetenzen", None))
		self.groupBox_grundkompetenzen_cr.hide()

		self.groupBox_ausgew_gk_cr = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_ausgew_gk_cr.setMinimumSize(QtCore.QSize(350, 0))
		self.groupBox_ausgew_gk_cr.setObjectName(_fromUtf8("groupBox_ausgew_gk_cr"))
		self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_ausgew_gk_cr)
		self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
		self.label_ausgew_gk = QtWidgets.QLabel(self.groupBox_ausgew_gk_cr)
		self.label_ausgew_gk.setWordWrap(True)
		self.label_ausgew_gk.setObjectName(_fromUtf8("label_ausgew_gk"))
		self.verticalLayout_2.addWidget(self.label_ausgew_gk)
		self.gridLayout.addWidget(self.groupBox_ausgew_gk_cr, 6, 0, 1, 1)
		self.groupBox_ausgew_gk_cr.setTitle(_translate("MainWindow", "Ausgewählte Grundkompetenzen", None))
		self.label_ausgew_gk.setText(_translate("MainWindow", "-", None))
		self.groupBox_ausgew_gk_cr.hide()

		self.groupBox_bilder = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_bilder.setMaximumSize(QtCore.QSize(16777215, 120))
		self.groupBox_bilder.setObjectName(_fromUtf8("groupBox_bilder"))
		self.gridLayout_13 = QtWidgets.QGridLayout(self.groupBox_bilder)
		self.gridLayout_13.setObjectName(_fromUtf8("gridLayout_13"))
		self.scrollArea = QtWidgets.QScrollArea(self.groupBox_bilder)
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
		self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.scrollAreaWidgetContents_bilder = QtWidgets.QWidget()
		self.scrollAreaWidgetContents_bilder.setGeometry(QtCore.QRect(0, 0, 320, 40))
		self.scrollAreaWidgetContents_bilder.setObjectName(_fromUtf8("scrollAreaWidgetContents_bilder"))
		self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_bilder)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.scrollArea.setWidget(self.scrollAreaWidgetContents_bilder)
		self.gridLayout_13.addWidget(self.scrollArea, 1, 0, 1, 1)
		self.groupBox_bilder.setTitle(_translate("MainWindow", "Bilder (klicken, um Bilder zu entfernen)", None))

		self.label_bild_leer= QtWidgets.QLabel(self.scrollAreaWidgetContents_bilder)
		self.label_bild_leer.setObjectName(_fromUtf8("label_bild_leer"))
		self.verticalLayout.addWidget(self.label_bild_leer)
		self.label_bild_leer.setText(_translate("MainWindow", "-", None))
		self.gridLayout.addWidget(self.groupBox_bilder, 7, 0, 1, 1)
		self.groupBox_bilder.hide()

		self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
		self.gridLayout_14 = QtWidgets.QGridLayout(self.groupBox_2)
		self.gridLayout_14.setObjectName(_fromUtf8("gridLayout_14"))
		self.lineEdit_titel = QtWidgets.QLineEdit(self.groupBox_2)
		self.lineEdit_titel.setObjectName(_fromUtf8("lineEdit_titel"))
		self.gridLayout_14.addWidget(self.lineEdit_titel, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.groupBox_2, 2, 2, 1, 4)
		self.groupBox_2.setTitle(_translate("MainWindow", "Titel", None))
		self.groupBox_2.hide()

		self.groupBox_beispieleingabe = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_beispieleingabe.setObjectName(_fromUtf8("groupBox_beispieleingabe"))
		self.gridLayout_10 = QtWidgets.QGridLayout(self.groupBox_beispieleingabe)
		self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
		self.label = QtWidgets.QLabel(self.groupBox_beispieleingabe)
		self.label.setStyleSheet(_fromUtf8("background-color: rgb(255, 178, 178);"))
		self.label.setWordWrap(True)
		self.label.setObjectName(_fromUtf8("label"))
		self.gridLayout_10.addWidget(self.label, 0, 0, 1, 1)
		self.plainTextEdit = QtWidgets.QPlainTextEdit(self.groupBox_beispieleingabe)
		self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
		self.gridLayout_10.addWidget(self.plainTextEdit, 1, 0, 1, 1)
		self.gridLayout.addWidget(self.groupBox_beispieleingabe, 3, 2, 4, 4)
		self.groupBox_beispieleingabe.setTitle(_translate("MainWindow", "Beispieleingabe", None))
		self.label.setText(_translate("MainWindow", "Info: Eingabe des Aufgabentextes zwischen \\begin{beispiel} ... \\end{beispiel}", None))
		self.groupBox_beispieleingabe.hide()

		#### CREATE CHECKBOXES ####
		##### AG #####
		self.tab_ag_cr = QtWidgets.QWidget()
		self.tab_ag_cr.setObjectName(_fromUtf8("tab_ag_cr"))
		self.gridLayout_ag_cr = QtWidgets.QGridLayout(self.tab_ag_cr)
		self.gridLayout_ag_cr.setObjectName(_fromUtf8("gridLayout_ag_cr"))
		self.tab_widget_gk_cr.addTab(self.tab_ag_cr, _fromUtf8(""))
		self.create_checkbox_gk('ag_cr', ag_beschreibung)
		self.tab_widget_gk_cr.setTabText(self.tab_widget_gk_cr.indexOf(self.tab_ag_cr), _translate("MainWindow", "Algebra und Geometrie", None))


		# # #### FA ####
		self.tab_fa_cr = QtWidgets.QWidget()
		self.tab_fa_cr.setObjectName(_fromUtf8("tab_fa_cr"))
		self.gridLayout_fa_cr = QtWidgets.QGridLayout(self.tab_fa_cr)
		self.gridLayout_fa_cr.setObjectName(_fromUtf8("gridLayout_fa_cr"))
		self.tab_widget_gk_cr.addTab(self.tab_fa_cr, _fromUtf8(""))
		self.create_checkbox_gk('fa_cr', fa_beschreibung)
		self.tab_widget_gk_cr.setTabText(self.tab_widget_gk_cr.indexOf(self.tab_fa_cr), _translate("MainWindow", "Funktionale Abhängigkeiten", None))

		# ##### AN ####
		self.tab_an_cr = QtWidgets.QWidget()
		self.tab_an_cr.setObjectName(_fromUtf8("tab_an_cr"))
		self.gridLayout_an_cr = QtWidgets.QGridLayout(self.tab_an_cr)
		self.gridLayout_an_cr.setObjectName(_fromUtf8("gridLayout_an_cr"))
		self.tab_widget_gk_cr.addTab(self.tab_an_cr, _fromUtf8(""))
		self.create_checkbox_gk('an_cr', an_beschreibung)
		self.tab_widget_gk_cr.setTabText(self.tab_widget_gk_cr.indexOf(self.tab_an_cr), _translate("MainWindow", "Analysis", None))

		# ### WS ####
		self.tab_ws_cr = QtWidgets.QWidget()
		self.tab_ws_cr.setObjectName(_fromUtf8("tab_ws_cr"))
		self.gridLayout_ws_cr = QtWidgets.QGridLayout(self.tab_ws_cr)
		self.gridLayout_ws_cr.setObjectName(_fromUtf8("gridLayout_ws_cr"))
		self.tab_widget_gk_cr.addTab(self.tab_ws_cr, _fromUtf8(""))
		self.create_checkbox_gk('ws_cr', ws_beschreibung)
		self.tab_widget_gk_cr.setTabText(self.tab_widget_gk_cr.indexOf(self.tab_ws_cr), _translate("MainWindow", "Wahrscheinlichkeit und Statistik", None))

		# ### 5. Klasse ###
		self.tab_k5_cr = QtWidgets.QWidget()
		self.tab_k5_cr.setObjectName(_fromUtf8("tab_k5_cr"))
		self.gridLayout_k5_cr = QtWidgets.QGridLayout(self.tab_k5_cr)
		self.gridLayout_k5_cr.setObjectName(_fromUtf8("gridLayout_k5_cr"))
		self.tab_widget_gk_cr.addTab(self.tab_k5_cr, _fromUtf8(""))
		self.create_checkbox_klasse('k5_cr',k5_beschreibung)
		self.tab_widget_gk_cr.setTabText(self.tab_widget_gk_cr.indexOf(self.tab_k5_cr), _translate("MainWindow", "5. Klasse", None))

		# ### 6. Klasse ###
		self.tab_k6_cr = QtWidgets.QWidget()
		self.tab_k6_cr.setObjectName(_fromUtf8("tab_k6_cr"))
		self.gridLayout_k6_cr = QtWidgets.QGridLayout(self.tab_k6_cr)
		self.gridLayout_k6_cr.setObjectName(_fromUtf8("gridLayout_k6_cr"))
		self.tab_widget_gk_cr.addTab(self.tab_k6_cr, _fromUtf8(""))
		self.create_checkbox_klasse('k6_cr',k6_beschreibung)
		self.tab_widget_gk_cr.setTabText(self.tab_widget_gk_cr.indexOf(self.tab_k6_cr), _translate("MainWindow", "6. Klasse", None))

		# ### 7. Klasse ###
		self.tab_k7_cr = QtWidgets.QWidget()
		self.tab_k7_cr.setObjectName(_fromUtf8("tab_k7_cr"))
		self.gridLayout_k7_cr = QtWidgets.QGridLayout(self.tab_k7_cr)
		self.gridLayout_k7_cr.setObjectName(_fromUtf8("gridLayout_k7_cr"))
		self.tab_widget_gk_cr.addTab(self.tab_k7_cr, _fromUtf8(""))
		self.create_checkbox_klasse('k7_cr',k7_beschreibung)
		self.tab_widget_gk_cr.setTabText(self.tab_widget_gk_cr.indexOf(self.tab_k7_cr), _translate("MainWindow", "7. Klasse", None))

		# ### 8. Klasse ###
		self.tab_k8_cr = QtWidgets.QWidget()
		self.tab_k8_cr.setObjectName(_fromUtf8("tab_k8_cr"))
		self.gridLayout_k8_cr = QtWidgets.QGridLayout(self.tab_k8_cr)
		self.gridLayout_k8_cr.setObjectName(_fromUtf8("gridLayout_k8_cr"))
		self.tab_widget_gk_cr.addTab(self.tab_k8_cr, _fromUtf8(""))
		self.create_checkbox_klasse('k8_cr',k8_beschreibung)
		self.tab_widget_gk_cr.setTabText(self.tab_widget_gk_cr.indexOf(self.tab_k8_cr), _translate("MainWindow", "8. Klasse", None))

		
		
		self.groupBox_punkte = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_punkte.setObjectName(_fromUtf8("groupBox_punkte"))
		self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_punkte)
		self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
		self.spinBox_punkte = QtWidgets.QSpinBox(self.groupBox_punkte)
		self.spinBox_punkte.setProperty("value", 1)
		self.spinBox_punkte.setObjectName(_fromUtf8("spinBox_punkte"))
		self.gridLayout_6.addWidget(self.spinBox_punkte, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.groupBox_punkte, 1, 3, 1, 1)
		self.groupBox_punkte.setTitle(_translate("MainWindow", "Punkte", None))
		self.groupBox_punkte.hide()


		self.groupBox_aufgabenformat = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_aufgabenformat.setObjectName(_fromUtf8("groupBox_aufgabenformat"))
		self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_aufgabenformat)
		self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
		self.comboBox_af = QtWidgets.QComboBox(self.groupBox_aufgabenformat)
		self.comboBox_af.setObjectName(_fromUtf8("comboBox_af"))
		self.comboBox_af.addItem(_fromUtf8(""))
		self.comboBox_af.addItem(_fromUtf8(""))
		self.comboBox_af.addItem(_fromUtf8(""))
		self.comboBox_af.addItem(_fromUtf8(""))
		self.comboBox_af.addItem(_fromUtf8(""))
		self.gridLayout_7.addWidget(self.comboBox_af, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.groupBox_aufgabenformat, 1, 4, 1, 1)
		self.groupBox_aufgabenformat.setTitle(_translate("MainWindow", "Aufgabenformat", None))
		self.comboBox_af.setItemText(0, _translate("MainWindow", "bitte auswählen", None))
		i=1
		for all in dict_aufgabenformate:
			self.comboBox_af.setItemText(i, _translate("MainWindow", dict_aufgabenformate[all], None))
			i+=1
		self.groupBox_aufgabenformat.hide()
		self.label_keine_auswahl = QtWidgets.QLabel(self.groupBox_aufgabenformat)
		self.label_keine_auswahl.setObjectName(_fromUtf8("label_keine_auswahl"))
		self.label_keine_auswahl.setMinimumSize(QtCore.QSize(139,0))
		self.gridLayout_7.addWidget(self.label_keine_auswahl)
		self.label_keine_auswahl.setText(_translate("MainWindow", "keine Auswahl nötig", None))
		self.label_keine_auswahl.hide()



		self.groupBox_klassen_cr = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_klassen_cr.setObjectName(_fromUtf8("groupBox_klassen_cr"))
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
		self.gridLayout.addWidget(self.groupBox_klassen_cr, 1, 5, 1, 1)
		self.groupBox_klassen_cr.setTitle(_translate("MainWindow", "Klasse", None))
		self.comboBox_klassen_cr.setItemText(0, _translate("MainWindow", "-", None))
		self.comboBox_klassen_cr.setItemText(1, _translate("MainWindow", "5. Klasse", None))
		self.comboBox_klassen_cr.setItemText(2, _translate("MainWindow", "6. Klasse", None))
		self.comboBox_klassen_cr.setItemText(3, _translate("MainWindow", "7. Klasse", None))
		self.comboBox_klassen_cr.setItemText(4, _translate("MainWindow", "8. Klasse", None))
		self.comboBox_klassen_cr.setItemText(5, _translate("MainWindow", "Matura", None))
		self.groupBox_klassen_cr.hide()

		self.groupBox_quelle = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_quelle.setObjectName(_fromUtf8("groupBox_quelle"))
		self.groupBox_quelle.setMaximumSize(QtCore.QSize(16777215, 120))
		self.gridLayout_18 = QtWidgets.QGridLayout(self.groupBox_quelle)
		self.gridLayout_18.setObjectName(_fromUtf8("gridLayout_18"))
		self.lineEdit_quelle = QtWidgets.QLineEdit(self.groupBox_quelle)
		self.lineEdit_quelle.setObjectName(_fromUtf8("lineEdit_quelle"))
		self.gridLayout_18.addWidget(self.lineEdit_quelle, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.groupBox_quelle, 7, 2, 1, 4)
		self.groupBox_quelle.setTitle(_translate("MainWindow", "Quelle oder Autor (Vorname Nachname) - Eingabe: VorNac", None))
		self.groupBox_quelle.hide()

		self.pushButton_save = QtWidgets.QPushButton(self.centralwidget)
		self.pushButton_save.setObjectName(_fromUtf8("pushButton_save"))
		self.gridLayout.addWidget(self.pushButton_save, 8, 5, 1, 1)
		self.pushButton_save.setText(_translate("MainWindow", "Speichern", None))
		self.pushButton_save.setShortcut(_translate("MainWindow", "Return", None))
		self.pushButton_save.hide()

		self.tab_widget_gk.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		MainWindow.setTabOrder(self.comboBox_aufgabentyp_cr, self.spinBox_punkte)
		MainWindow.setTabOrder(self.spinBox_punkte, self.comboBox_af)
		MainWindow.setTabOrder(self.comboBox_af, self.comboBox_klassen_cr)
		MainWindow.setTabOrder(self.comboBox_klassen_cr, self.lineEdit_titel)
		MainWindow.setTabOrder(self.lineEdit_titel, self.plainTextEdit)
		MainWindow.setTabOrder(self.plainTextEdit, self.lineEdit_quelle)
		MainWindow.setTabOrder(self.lineEdit_quelle, self.pushButton_save)
		####################################################
		#####################################################
		####################################################
		#####################################################

		self.gridLayout_11.addWidget(self.tab_widget_gk, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.groupBox_gk, 1, 3, 2, 1)
		MainWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)
		self.actionReset = QtWidgets.QAction(MainWindow)
		self.actionReset.setObjectName(_fromUtf8("actionReset"))

		self.retranslateUi(MainWindow)
		self.tabWidget.setCurrentIndex(0)
		
															   
		self.tab_widget_gk_cr.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		
		
		############################################################################
		############## Commands ####################################################
		############################################################################

		#self.btn_refreshddb.clicked.connect(self.refresh_ddb)
		self.btn_k5.clicked.connect(self.btn_k5_pressed)
		self.btn_k6.clicked.connect(self.btn_k6_pressed)
		self.btn_k7.clicked.connect(self.btn_k7_pressed)
		self.btn_k8.clicked.connect(self.btn_k8_pressed)
		self.btn_ag_all.clicked.connect(self.btn_ag_all_pressed)
		self.btn_an_all.clicked.connect(self.btn_an_all_pressed)
		self.btn_fa_all.clicked.connect(self.btn_fa_all_pressed)
		self.btn_ws_all.clicked.connect(self.btn_ws_all_pressed)
		self.btn_suche.clicked.connect(self.PrepareTeXforPDF)
		self.actionExit.triggered.connect(self.close_app)
		self.actionRefresh_Database.triggered.connect(self.refresh_ddb)
		self.actionsuchfenster_reset.triggered.connect(self.suchfenster_reset)
		self.actionAufgaben_Typ1.triggered.connect(self.chosen_aufgabenformat_typ1)
		self.actionAufgaben_Typ2.triggered.connect(self.chosen_aufgabenformat_typ2)
		self.actionInfo.triggered.connect(self.show_info)
		self.actionNeu.triggered.connect(self.neue_aufgabe_erstellen)
		self.actionSuche.triggered.connect(self.aufgaben_suchen)
		self.actionBild_einf_gen.triggered.connect(self.add_picture)
		self.actionBild_konvertieren_jpg_eps.triggered.connect(self.convert_jpgtoeps)
		self.comboBox_aufgabentyp_cr.currentIndexChanged.connect(self.chosen_aufgabenformat_cr)
		self.pushButton_save.clicked.connect(self.save_file)

		for all in ag_beschreibung:
			x=eval('self.cb_'+all)
			x.stateChanged.connect(self.cb_checked)

		for all in fa_beschreibung:
			x=eval('self.cb_'+all)
			x.stateChanged.connect(self.cb_checked)			
		
		for all in an_beschreibung:
			x=eval('self.cb_'+all)
			x.stateChanged.connect(self.cb_checked)
			

			
		for all in ws_beschreibung:
			x=eval('self.cb_'+all)
			x.stateChanged.connect(self.cb_checked)
		
		for g in range(5,9):
			for all in eval('k%s_beschreibung'%g):
				x=eval('self.cb_k%s_'%g+all)
				x.stateChanged.connect(self.cb_rest_checked)

		for all in {**ag_beschreibung,**fa_beschreibung,**an_beschreibung,**ws_beschreibung}:
			x=eval('self.cb_'+all+'_cr')
			x.stateChanged.connect(lambda: self.gk_checked_cr('gk'))

		for g in range(5,9):
			for all in eval('k%s_beschreibung'%g):
				x=eval('self.cb_k%s_cr_'%g+all+'_cr')
				x.stateChanged.connect(lambda: self.gk_checked_cr('klasse'))
		############################################################################################
		##############################################################################################
	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("LaMA - LaTeX Mathematik Assistent", "LaMA - LaTeX Mathematik Assistent", None))
		self.menuDateityp.setTitle(_translate("MainWindow", "Aufgabentyp", None))
		self.menuDatei.setTitle(_translate("MainWindow", "Datei", None))
		self.menuNeu.setTitle(_translate("MainWindow", "Neue Aufgabe", None))
		self.menuSuche.setTitle(_translate("MainWindow", "Aufgabensuche", None))
		self.menuBild_einf_gen.setTitle(_translate("MainWindow", "Bild einfügen", None))
		self.actionBild_einf_gen.setText(_translate("MainWindow", "Durchsuchen...", None))
		self.actionBild_konvertieren_jpg_eps.setText(_translate("MainWindow", "Bild konvertieren (jpg zu eps)", None))		
		self.menuHelp.setTitle(_translate("MainWindow", "?", None))
		self.actionReset.setText(_translate("MainWindow", "Reset", None))
		self.actionAufgaben_Typ1.setText(_translate("MainWindow", "Typ 1 Aufgaben", None))
		self.actionAufgaben_Typ1.setShortcut('Ctrl+1')
		self.actionAufgaben_Typ2.setText(_translate("MainWindow", "Typ 2 Aufgaben", None))
		self.actionAufgaben_Typ2.setShortcut('Ctrl+2')
		self.actionInfo.setText(_translate("MainWindow", "Über LaMA", None))
		self.actionsuchfenster_reset.setText(_translate("MainWindow", "Reset", None))
		self.actionsuchfenster_reset.setShortcut("F4")
		self.actionNeu.setText(_translate("MainWindow", "Neue Aufgabe erstellen...", None))
		self.actionNeu.setShortcut("F2")
		self.actionSuche.setText(_translate("MainWindow", "Aufgaben suchen...", None))
		self.actionSuche.setShortcut("F3")
		self.actionExit.setText(_translate("MainWindow", "Exit", None))
		self.actionRefresh_Database.setText(_translate("MainWindow", "Refresh Database", None))
		self.actionRefresh_Database.setShortcut("F5")
		self.label_aufgabentyp.setText(_translate("MainWindow", "Aufgabentyp: Typ 1", None))
		self.groupBox_ausgew_gk.setTitle(_translate("MainWindow", "Ausgewählte Grundkompetenzen", None))
		self.groupBox_titelsuche.setTitle(_translate("MainWindow", "Titelsuche:", None))
		self.groupBox_klassen.setTitle(_translate("MainWindow", "Klassen", None))
		self.cb_k7.setText(_translate("MainWindow", "7. Klasse", None))
		self.cb_k5.setText(_translate("MainWindow", "5. Klasse", None))
		self.cb_k6.setText(_translate("MainWindow", "6. Klasse", None))
		self.cb_k8.setText(_translate("MainWindow", "8. Klasse", None))
		self.cb_mat.setText(_translate("MainWindow", "Matura", None))
		self.cb_solution.setText(_translate("MainWindow", "Lösungen anzeigen", None))
		try:
			log_file=os.path.join(path_programm,'Teildokument','log_file_1')
			self.label_update.setText(_translate("MainWindow", 'Letztes Update: ' + self.modification_date(log_file).strftime('%d.%m.%y - %H:%M'), None))
		except FileNotFoundError:
			self.label_update.setText(_translate("MainWindow", "Letztes Update: ---", None))
		self.btn_suche.setText(_translate("MainWindow", "Suche starten", None))


		#self.btn_refreshddb.setText(_translate("MainWindow", "Refresh Database", None))
		# self.menu_aufgabentyp.setItemText(0, _translate("MainWindow", "Typ 1", None))
		# self.menu_aufgabentyp.setItemText(1, _translate("MainWindow", "Typ 2", None))
		self.combobox_searchtype.setItemText(0, _translate("MainWindow", "Alle Dateien ausgeben, die zumindest ein Suchkriterium enthalten", None))

		##### ONLY NEEDED for Typ1 #####
		self.groupBox_af = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_af.setMaximumSize(QtCore.QSize(367, 16777215))
		self.groupBox_af.setObjectName(_fromUtf8("groupBox_af"))
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
		self.gridLayout.addWidget(self.groupBox_af, 4, 0, 2, 1)
			# #################

			# ##### ONLY NEEDED for Typ1 #####

		self.groupBox_af.setTitle(_translate("MainWindow", "Gesuchte Aufgabenformate:", None))
		self.cb_af_zo.setText(_translate("MainWindow", "Zuordnungsformat (ZO)", None))
		self.cb_af_mc.setText(_translate("MainWindow", "Multiplechoice (MC)", None))
		self.cb_af_oa.setText(_translate("MainWindow", "Offenes Antwortformat (OA)", None))
		self.cb_af_lt.setText(_translate("MainWindow", "Lückentext (LT)", None))
		#########################

		### Typ1
		#self.combobox_searchtype.setItemText(1, _translate("MainWindow", "Alle Dateien ausgeben, die alle Suchkriterien enthalten", None))
		######
		
		### Typ2
		self.combobox_searchtype.setItemText(1, _translate("MainWindow", "Alle Dateien ausgeben, die ausschließlich diese Suchkriterien enthalten", None))
		######
		
		self.groupBox_themen_klasse.setTitle(_translate("MainWindow", "Themen Schulstufe", None))
		# self.name_checkbox_klassen(5)
		# self.name_checkbox_klassen(6)
		# self.name_checkbox_klassen(7)
		# self.name_checkbox_klassen(8)																					 

		self.btn_k5.setText(_translate("MainWindow", "alle auswählen", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_k5), _translate("MainWindow", "5. Klasse", None))
		self.btn_k6.setText(_translate("MainWindow", "alle auswählen", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_k6), _translate("MainWindow", "6. Klasse", None))
		self.btn_k7.setText(_translate("MainWindow", "alle auswählen", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_k7), _translate("MainWindow", "7. Klasse", None))
		self.btn_k8.setText(_translate("MainWindow", "alle auswählen", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_k8), _translate("MainWindow", "8. Klasse", None))
		self.groupBox_gk.setTitle(_translate("MainWindow", "Grundkompetenzen", None))
		self.btn_suche.setShortcut(_translate("MainWindow", "Return", None))
		#self.btn_refreshddb.setShortcut(_translate("MainWindow", "F5", None))
		


############# Infos for GKs
		self.create_Tooltip(ag_beschreibung)
		self.create_Tooltip(fa_beschreibung)
		self.create_Tooltip(an_beschreibung)
		self.create_Tooltip(ws_beschreibung)
		# # for all in ag_beschreibung:
		# # 	x=eval('self.cb_'+all)
		# # 	x.setToolTip(ag_beschreibung[all])
		# # 	y=eval('self.cb_'+all+'_cr')
		# # 	y.setToolTip(ag_beschreibung[all])
			
		# for all in an_beschreibung:
		# 	x=eval('self.cb_'+all)
		# 	x.setToolTip(an_beschreibung[all])

		# for all in fa_beschreibung:
		# 	x=eval('self.cb_'+all)
		# 	x.setToolTip(fa_beschreibung[all])
			
		# for all in ws_beschreibung:
		# 	x=eval('self.cb_'+all)
		# 	x.setToolTip(ws_beschreibung[all])
			
#########################################
		# self.name_checkbox_gk(ag_beschreibung)
		# self.name_checkbox_gk(an_beschreibung)
		# self.name_checkbox_gk(fa_beschreibung)
		# self.name_checkbox_gk(ws_beschreibung)

		self.btn_ag_all.setText(_translate("MainWindow", "alle auswählen", None))
		self.tab_widget_gk.setTabText(self.tab_widget_gk.indexOf(self.tab_ag), _translate("MainWindow", "Algebra und Geometrie", None))
		self.btn_an_all.setText(_translate("MainWindow", "alle auswählen", None))
		self.tab_widget_gk.setTabText(self.tab_widget_gk.indexOf(self.tab_an), _translate("MainWindow", "Analysis", None))
		self.btn_fa_all.setText(_translate("MainWindow", "alle auswählen", None))
		self.tab_widget_gk.setTabText(self.tab_widget_gk.indexOf(self.tab_fa), _translate("MainWindow", "Funktionale Abhängigkeiten", None))		
		self.btn_fa_all.setText(_translate("MainWindow", "alle auswählen", None))
		self.tab_widget_gk.setTabText(self.tab_widget_gk.indexOf(self.tab_fa), _translate("MainWindow", "Funktionale Abhängigkeiten", None))		
		self.btn_ws_all.setText(_translate("MainWindow", "alle auswählen", None))
		self.tab_widget_gk.setTabText(self.tab_widget_gk.indexOf(self.tab_ws), _translate("MainWindow", "Wahrscheinlichkeit und Statistik", None))		
		self.actionReset.setText(_translate("MainWindow", "Reset", None))
		self.label_gk_rest.setText(_translate("MainWindow", "", None))
		self.label_gk.setText(_translate("MainWindow", "", None))
		# self.label_gk_an.setText(_translate("MainWindow", "", None))
		# self.label_gk_fa.setText(_translate("MainWindow", "", None))
		# self.label_gk_ws.setText(_translate("MainWindow", "", None))
		self.actionExit.setText(_translate("MainWindow", "Exit", None))
		
		print('Done')
	# def change_to_full_gk_name(self,chosen_dict):
	# 	x=' '
	# 	for all in chosen_dict:
	# 		if all[-1]=='L':
	# 			x='-L '
	# 		print(all[:2].upper()+x+all[2]+'.'+all[3])

	#######################
	#### Check for Updates
	##########################

	def check_for_update(self):
		for i in range(5):
			try:
				version_path = os.path.join(path_programm,'_database','_config','update')
				version_file = os.path.join(version_path,'__version__.txt')
				f=open(version_file,'r')
				break
			except FileNotFoundError:
				input("Please place your your config file in '{}' and hit enter. {} tries left!".format(version_path, 5-i))
			if i == 4:
			    print("No version set. Skipping version check!")
			    return False

		if __version__ not in f.read():
		    msg = QtWidgets.QMessageBox()
		    msg.setIcon(QtWidgets.QMessageBox.Question)
		    msg.setWindowIcon(QtGui.QIcon(logo_path))
		    msg.setText('Es ist ein neues Update vorhanden.')
		    msg.setInformativeText('Möchten Sie das neue Update installieren?')
		    msg.setWindowTitle("Update vorhanden")
		    msg.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
		    buttonY = msg.button(QtWidgets.QMessageBox.Yes)
		    buttonY.setText('Ja')
		    buttonN = msg.button(QtWidgets.QMessageBox.No)
		    buttonN.setText('Nein')
		    ret=msg.exec_()


		    if ret==QtWidgets.QMessageBox.Yes:
			    opened_file=os.path.basename(sys.argv[0])
			    name, extension=os.path.splitext(opened_file)

			    filename_update=os.path.join(path_programm,'_database','_config','update','update%s'%extension)
			    #if extension=='.py':
			#	    filename_update=os.path.join(path_programm,'_database','_config','update','update.py')
			 #   elif extension=='.exe':
			#	    filename_update=os.path.join(path_programm,'_database','_config','update','update.exe')
			    if sys.platform.startswith('linux'):
				    os.system(filename_update)
			    elif sys.platform.startswith('darwin'):
				    os.system(filename_update)
			    else:
				    os.startfile(filename_update)										
			    sys.exit(0)



	def create_Tooltip(self,chosen_dict):
		for all in chosen_dict:
			x=eval('self.cb_'+all)
			x.setToolTip(chosen_dict[all])
			y=eval('self.cb_'+all+'_cr')
			y.setToolTip(chosen_dict[all])

	def suchfenster_reset(self):
		global dict_picture_path
		for all in ag_beschreibung:
			x=eval('self.cb_'+all)
			x.setChecked(False)
			y=eval('self.cb_'+all+'_cr')
			y.setChecked(False)
		for all in an_beschreibung:
			x=eval('self.cb_'+all)
			x.setChecked(False)
			y=eval('self.cb_'+all+'_cr')
			y.setChecked(False)
		for all in fa_beschreibung:
			x=eval('self.cb_'+all)
			x.setChecked(False)
			y=eval('self.cb_'+all+'_cr')
			y.setChecked(False)
		for all in ws_beschreibung:
			x=eval('self.cb_'+all)
			x.setChecked(False)
			y=eval('self.cb_'+all+'_cr')
			y.setChecked(False)
		for r in range(5,9):
			dict_klasse=eval('k'+str(r)+'_beschreibung')	
			for all in dict_klasse:
				x=eval('self.cb_k'+str(r)+'_'+all)
				x.setChecked(False)
				y=eval('self.cb_k'+str(r)+'_cr_'+all+'_cr')
				y.setChecked(False)
		for all in Klassen:
			x=eval('self.cb_'+all)
			x.setChecked(False)
		for all in list(dict_aufgabenformate.keys()):
			x=eval('self.cb_af_'+all)
			x.setChecked(False)
		self.entry_suchbegriffe.setText('')	
		self.cb_solution.setChecked(True)	
		self.spinBox_punkte.setProperty("value", 1)
		# self.comboBox_aufgabentyp.setCurrentIndex(0)
		self.comboBox_aufgabentyp_cr.setCurrentIndex(0)
		self.comboBox_af.setCurrentIndex(0)
		self.comboBox_klassen_cr.setCurrentIndex(0)
		self.label_ausgew_gk.setText(_translate("MainWindow", "-", None))
		self.label_bild_leer.show()

		for i in range(len(dict_picture_path)):
			x=eval('self.label_bild_'+str(i))
			x.hide()
		dict_picture_path={}			
		if self.lineEdit_titel.text().startswith('###'):
			self.lineEdit_titel.setText(_translate("MainWindow", "###", None))
		else:
			self.lineEdit_titel.setText(_translate("MainWindow", "", None))
		self.lineEdit_quelle.setText(_translate("MainWindow", "", None))
		self.plainTextEdit.setPlainText(_translate("MainWindow", "", None))




	def close_app(self):
		sys.exit(0)

	def show_info(self):
		QtWidgets.QApplication.restoreOverrideCursor()
		
		msg = QtWidgets.QMessageBox()

		#msg.setIcon(QtWidgets.QMessageBox.Information)
		pixmap = QtGui.QPixmap(logo_path)


		#pixmap.scaled(1,1, QtCore.Qt.KeepAspectRatio)
		#pixmap.resize(20,20)
		msg.setIconPixmap(pixmap)
		msg.setWindowIcon(QtGui.QIcon(logo_path))
		msg.setText("LaMA - LaTeX Mathematik Assistent %s  \n\n"
		"License: GNU General Public License v3.0  \n"	
		"Author: Christoph Weberndorfer  \n\n"
		"Credits: Matthias Konzett, David Fischer   "%__version__)
		msg.setInformativeText("Logo & Icon: Lisa Schultz")
		msg.setWindowTitle("Über LaMA - LaTeX Mathematik Assistent")
		#msg.setDetailedText("The details are as follows:")
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		retval = msg.exec_()
	
	def get_logfile(self):
		try:
			x='log_file_%s'%self.label_aufgabentyp.text()[-1]
			log_file=os.path.join(path_programm,'Teildokument',x)
			self.label_update.setText(_translate("MainWindow", 'Letztes Update: ' + self.modification_date(log_file).strftime('%d.%m.%y - %H:%M'), None))
		except FileNotFoundError:
			self.label_update.setText(_translate("MainWindow", "Letztes Update: ---", None))

	def chosen_aufgabenformat_typ1(self):
		self.label_aufgabentyp.setText(_translate("MainWindow", "Aufgabentyp: Typ 1", None))
		self.groupBox_af.show()
		self.combobox_searchtype.hide()
		self.get_logfile()
	
		
	
	def chosen_aufgabenformat_typ2(self):
		self.label_aufgabentyp.setText(_translate("MainWindow", "Aufgabentyp: Typ 2", None))
		self.groupBox_af.hide()
		self.combobox_searchtype.show()
		self.get_logfile()

	def create_checkbox_gk(self,gk_type,chosen_dict):
		
		row=0
		column=0
		if 'cr' in gk_type:
			max_row=8
		else:
			max_row=9
		for all in chosen_dict:
			if 'cr' in gk_type:
				cb_name=str(all+'_cr')
			else:
				cb_name=all
			#print('self.cb_'+cb_name+'=QtWidgets.QCheckBox(self.tab_'+gk_type+')')
			exec('self.cb_'+cb_name+'=QtWidgets.QCheckBox(self.tab_'+gk_type+')')
			exec('self.cb_'+cb_name+'.setObjectName(_fromUtf8("cb_'+cb_name+'"))')
			x=eval('self.cb_'+cb_name)
			x.setText(_translate("MainWindow", dict_gk[all], None))
			grid=eval('self.gridLayout_'+gk_type)
			grid.addWidget(x, row,column, 1, 1)

			if row>max_row:
				row=0
				column+=1
			else:
				row+=1


	def create_checkbox_klasse(self,klasse,chosen_dict):
		row=0
		column=0
		max_row=9

		for all in chosen_dict:
			if 'cr' in klasse:
				cb_name=str(all+'_cr')
				cb_label=chosen_dict[all].replace('\n', ' ')
			else:
				cb_name=all
				cb_label=chosen_dict[all]
			exec('self.cb_'+klasse+'_'+cb_name+'= QtWidgets.QCheckBox(self.tab_'+klasse+')')	
			exec('self.cb_'+klasse+'_'+cb_name+'.setObjectName(_fromUtf8("cb_'+klasse+'_'+cb_name+'"))')
			grid=eval('self.gridLayout_'+klasse)
			x=eval('self.cb_'+klasse+'_'+cb_name)	
			x.setText(_translate("MainWindow", cb_label, None))
			grid.addWidget(x, row,column, 1, 1)	

			if row>max_row:
				row=0
				column+=1
			else:
				row+=1

			if 'cr' in klasse:
				pass
			else:
				exec('self.btn_'+klasse+'= QtWidgets.QPushButton(self.tab_'+klasse+')')
				exec('self.btn_%s.setStyleSheet(_fromUtf8("background-color: rgb(240, 240, 240);"))'%klasse)
				exec('self.btn_'+klasse+'.setObjectName(_fromUtf8("btn_'+klasse+'"))')
				exec('self.gridLayout_'+klasse+'.addWidget(self.btn_'+klasse+', max_row, column+1, 1, 1, QtCore.Qt.AlignRight)')


	# def name_checkbox_gk(self, chosen_dict):
	# 	for all in chosen_dict:
	# 		x=eval('self.cb_'+all)
	# 		x.setText(_translate("MainWindow", dict_gk[all], None))

	# def name_checkbox_klassen(self, klasse):
	# 	chosen_dict=eval('k'+str(klasse)+'_beschreibung')
	# 	for all in chosen_dict:
	# 		x=eval('self.cb_k'+str(klasse)+'_'+all)
	# 		x.setText(_translate("MainWindow", chosen_dict[all], None))		

	def btn_k5_pressed(self):
		if self.cb_k5_fu.isChecked()==False:
			for all in k5_beschreibung:
				x=eval('self.cb_k5_'+all)
				x.setChecked(True)
		elif self.cb_k5_fu.isChecked()==True:
			for all in k5_beschreibung:
				x=eval('self.cb_k5_'+all)
				x.setChecked(False)

	def btn_k6_pressed(self):
		if self.cb_k6_bsw.isChecked()==False:
			for all in k6_beschreibung:
				x=eval('self.cb_k6_'+all)
				x.setChecked(True)
		elif self.cb_k6_bsw.isChecked()==True:
			for all in k6_beschreibung:
				x=eval('self.cb_k6_'+all)
				x.setChecked(False)

	def btn_k7_pressed(self):
		if self.cb_k7_dr.isChecked()==False:
			for all in k7_beschreibung:
				x=eval('self.cb_k7_'+all)
				x.setChecked(True)
		elif self.cb_k7_dr.isChecked()==True:
			for all in k7_beschreibung:
				x=eval('self.cb_k7_'+all)
				x.setChecked(False)

	def btn_k8_pressed(self):
		if self.cb_k8_ddg.isChecked()==False:
			for all in k8_beschreibung:
				x=eval('self.cb_k8_'+all)
				x.setChecked(True)
		elif self.cb_k8_ddg.isChecked()==True:
			for all in k8_beschreibung:
				x=eval('self.cb_k8_'+all)
				x.setChecked(False)
				
	def btn_ag_all_pressed(self):
		if self.cb_ag11.isChecked()==False:
			for all in ag_beschreibung:
				x=eval('self.cb_'+all)
				x.setChecked(True)
		elif self.cb_ag11.isChecked()==True:
			for all in ag_beschreibung:
				x=eval('self.cb_'+all)
				x.setChecked(False)
				
	def btn_an_all_pressed(self):
		if self.cb_an11.isChecked()==False:
			for all in an_beschreibung:
				x=eval('self.cb_'+all)
				x.setChecked(True)
		elif self.cb_an11.isChecked()==True:
			for all in an_beschreibung:
				x=eval('self.cb_'+all)
				x.setChecked(False)

	def btn_fa_all_pressed(self):
		if self.cb_fa11.isChecked()==False:
			for all in fa_beschreibung:
				x=eval('self.cb_'+all)
				x.setChecked(True)
		elif self.cb_fa11.isChecked()==True:
			for all in fa_beschreibung:
				x=eval('self.cb_'+all)
				x.setChecked(False)	
				
	def btn_ws_all_pressed(self):
		if self.cb_ws11.isChecked()==False:
			for all in ws_beschreibung:
				x=eval('self.cb_'+all)
				x.setChecked(True)
		elif self.cb_ws11.isChecked()==True:
			for all in ws_beschreibung:
				x=eval('self.cb_'+all)
				x.setChecked(False)

	# def cb_checked(self):
	# 	set_chosen_gk=set([])

				
	def cb_checked(self):
		chosen_gk=[]

		list_gk=['ag','fa','an','ws']

		for thema in list_gk:
			exec('set_chosen_gk_%s=set([])'%thema)
			for all in eval('%s_beschreibung'%thema):
				x=eval('self.cb_'+all)
				if x.isChecked()==True:
					eval('set_chosen_gk_%s.add(x.text())'%thema)
			eval('chosen_gk.extend(sorted(set_chosen_gk_%s))'%thema)

		if len(chosen_gk)>35:	
			x=', '.join(chosen_gk[:35])
			x=x + ', ...'
		else:
			x=', '.join(chosen_gk)

		self.label_gk.setText(_translate("MainWindow", str(x), None))

		# set_chosen_gk_ag=set([])
		# for all in ag_beschreibung:
		# 	x=eval('self.cb_'+all)
		# 	if x.isChecked()==True:
		# 		set_chosen_gk_ag.add(x.text())
		# chosen_gk.extend(sorted(set_chosen_gk_ag))

		# set_chosen_gk_fa=set([])
		# for all in fa_beschreibung:
		# 	x=eval('self.cb_'+all)
		# 	if x.isChecked()==True:
		# 		set_chosen_gk_fa.add(x.text())
		# chosen_gk.extend(sorted(set_chosen_gk_fa))		
		
		# set_chosen_gk_an=set([])
		# for all in an_beschreibung:
		# 	x=eval('self.cb_'+all)
		# 	if x.isChecked()==True:
		# 		set_chosen_gk_an.add(x.text())
		# chosen_gk.extend(sorted(set_chosen_gk_an))

		# set_chosen_gk_ws=set([])
		# for all in ws_beschreibung:
		# 	x=eval('self.cb_'+all)
		# 	if x.isChecked()==True:
		# 		set_chosen_gk_ws.add(x.text())
		# chosen_gk.extend(sorted(set_chosen_gk_ws))



	
	def cb_rest_checked(self):
		set_chosen_gk=set([])
		for all in k5_beschreibung:
			x=eval('self.cb_k5_'+all)
			if x.isChecked()==True:
				set_chosen_gk.add(all.upper()+'(5)')
		for all in k6_beschreibung:
			x=eval('self.cb_k6_'+all)
			if x.isChecked()==True:
				set_chosen_gk.add(all.upper() + '(6)')
		for all in k7_beschreibung:
			x=eval('self.cb_k7_'+all)
			if x.isChecked()==True:
				set_chosen_gk.add(all.upper() + '(7)')
		for all in k8_beschreibung:
			x=eval('self.cb_k8_'+all)
			if x.isChecked()==True:
				set_chosen_gk.add(all.upper() + '(8)')		
		if len(set_chosen_gk)>6:
			x= ', '.join(list(sorted(set_chosen_gk))[:6])
			x=x+', ...'
		else:
			x= ', '.join(sorted(set_chosen_gk))
		if len(set_chosen_gk)>0:
			x='Weitere: '+x
		self.label_gk_rest.setText(_translate("MainWindow", str(x), None))

			

	############################################################################
	############################################################################
	######### Button REFRESH DATABASE ######################################
	############################################################################

	def modification_date(self,filename):
		t = os.path.getmtime(filename)
		return datetime.datetime.fromtimestamp(t)	
		
	def refresh_ddb(self):
		QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		beispieldaten_dateipfad = {}
		beispieldaten = []
		chosen_aufgabenformat='Typ%sAufgaben'%self.label_aufgabentyp.text()[-1]
		filename= 0
		########################################################
		##### Suche offizielle Beispiele ####################
		##################################################

		for root, dirs, files in os.walk(os.path.join(path_programm,'_database', chosen_aufgabenformat)):
			for all in files:
				if all.endswith('.tex') or all.endswith('.ltx'):
					if not ('Gesamtdokument' in all) and not ('Teildokument' in all):
						file=open(os.path.join(root,all), encoding='ISO-8859-1')
						for i, line in enumerate(file):
							if not line == "\n":			
								beispieldaten_dateipfad[line]=os.path.join(root,all)
								beispieldaten.append(line)
								break
						file.close()

		################################################
		#### Suche inoffizielle Beispiele ######
		#############################################

		for root, dirs, files in os.walk(os.path.join(path_programm,'_database_inoffiziell', chosen_aufgabenformat)):
			for all in files:
				if all.endswith('.tex') or all.endswith('.ltx'):
					if not ('Gesamtdokument' in all) and not ('Teildokument' in all):
						file=open(os.path.join(root,all), encoding='ISO-8859-1')
						for i, line in enumerate(file):
							if not line == "\n":			
								beispieldaten_dateipfad[line]=os.path.join(root,all)
								beispieldaten.append(line)
								break
						file.close()
		
		temp_dict_beispieldaten={}
		temp_list=list(beispieldaten_dateipfad.keys())
		temp_list.sort(key=self.natural_keys)
		for all in temp_list:
			temp_dict_beispieldaten.update({all:beispieldaten_dateipfad[all]})

		beispieldaten_dateipfad=temp_dict_beispieldaten
		
		log_file=os.path.join(path_programm,'Teildokument','log_file_%s'%self.label_aufgabentyp.text()[-1])
		
		try:
			with open(log_file, 'w+') as f:
				json.dump(beispieldaten_dateipfad, f,ensure_ascii=False)
		except FileNotFoundError:
			os.makedirs(os.path.join(path_programm,'Teildokument'))
			with open(log_file, 'w+') as f:
				json.dump(beispieldaten_dateipfad, f,ensure_ascii=False)		

		self.label_update.setText(_translate("MainWindow", 'Last Update: ' + self.modification_date(log_file).strftime('%d.%m.%y - %H:%M'), None))
		QtWidgets.QApplication.restoreOverrideCursor()


		
		
	############################################################################
	############################################################################
	########################### CREATE PDF ####################################		
	############################################################################
	def atoi(self,text):
		return int(text) if text.isdigit() else text	
	
	def natural_keys(self,text):
		return [ self.atoi(c) for c in re.split('(\d+)', text) ]

	def create_pdf(self):

		chosen_aufgabenformat=self.label_aufgabentyp.text()[-1]

		if sys.platform.startswith('linux'):
			subprocess.Popen('cd "{0}/Teildokument" ; latex --synctex=-1 Teildokument_{1}.tex ; dvips Teildokument_{1}.dvi ; ps2pdf -dNOSAFER Teildokument_{1}.ps'.format(path_programm, chosen_aufgabenformat),shell=True).wait()
			subprocess.run(['xdg-open', "{0}/Teildokument/Teildokument_{1}.pdf".format(path_programm, chosen_aufgabenformat)])
		elif sys.platform.startswith('darwin'):
			subprocess.Popen('cd "{0}/Teildokument" ; latex --synctex=-1 Teildokument_{1}.tex ; dvips Teildokument_{1}.dvi ; ps2pdf -dNOSAFER Teildokument_{1}.ps'.format(path_programm, chosen_aufgabenformat),shell=True).wait()
			subprocess.run(['open', "{0}/Teildokument/Teildokument_{1}.pdf".format(path_programm, chosen_aufgabenformat)])
		else:
			subprocess.Popen('cd "{0}/Teildokument" & latex --synctex=-1 Teildokument_{1}.tex& dvips Teildokument_{1}.dvi & ps2pdf -dNOSAFER Teildokument_{1}.ps'.format(path_programm, chosen_aufgabenformat),shell=True).wait()
			subprocess.Popen('cd "{0}/Teildokument" & Teildokument_{1}.pdf'.format(path_programm, chosen_aufgabenformat), shell=True).poll()
		## -interaction=nonstopmode -halt-on-error Don't stop when error occurs, while compiling
		os.unlink('{0}/Teildokument/Teildokument_{1}.aux'.format(path_programm, chosen_aufgabenformat))
		os.unlink('{0}/Teildokument/Teildokument_{1}.log'.format(path_programm, chosen_aufgabenformat))
		os.unlink('{0}/Teildokument/Teildokument_{1}.dvi'.format(path_programm, chosen_aufgabenformat))
		os.unlink('{0}/Teildokument/Teildokument_{1}.ps'.format(path_programm, chosen_aufgabenformat))
	
	def PrepareTeXforPDF(self):
		chosen_aufgabenformat='Typ%sAufgaben'%self.label_aufgabentyp.text()[-1]

		QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		
		if not os.path.isfile(os.path.join(path_programm,'Teildokument','log_file_%s'%self.label_aufgabentyp.text()[-1])):
			self.refresh_ddb()
		else: ##  Automatic update once per month
			log_file=os.path.join(path_programm,'Teildokument','log_file_%s'%self.label_aufgabentyp.text()[-1])
			month_update_log_file=self.modification_date(log_file).strftime('%m')
			month_today=datetime.date.today().strftime('%m')
			if month_today!= month_update_log_file:
				self.refresh_ddb()

		suchbegriffe = []
		

					
		#### ALGEBRA UND GEOMETRIE
		for all in ag_beschreibung:
			x=eval('self.cb_'+all)
			if x.isChecked()==True:
				suchbegriffe.append(all)
				
		#### ANALYSIS
		for all in an_beschreibung:
			x=eval('self.cb_'+all)
			if x.isChecked()==True:
				suchbegriffe.append(all)
		
		#### FUNKTIONALE ABHÄNGIGKEITEN	
		for all in fa_beschreibung:
			x=eval('self.cb_'+all)
			if x.isChecked()==True:
				suchbegriffe.append(all)		
		#### WAHRSCHEINLICHKEIT UND STATISTIK
		for all in ws_beschreibung:
			x=eval('self.cb_'+all)
			if x.isChecked()==True:
				suchbegriffe.append(all)
				
		temp_suchbegriffe=[]
		for all in suchbegriffe:
			temp_suchbegriffe.append(dict_gk[all])
		suchbegriffe=temp_suchbegriffe

		#### Suche der Schulstufe 
		for y in range(5,9):
			themen_klasse=eval('k%s_beschreibung'%y)
			for all in themen_klasse:
				x=eval('self.cb_k%s_'%y+all)
				grade='K'+str(y)
				if x.isChecked()==True:
					# if grade not in suchbegriffe:
						# suchbegriffe.append('K'+str(y))
					suchbegriffe.append(all.upper())
					
		#### typ1 ###
		# log_file=os.path.join(path_programm,'Typ 2 Aufgaben','Teildokument','log_file')
		######

		log_file=os.path.join(path_programm,'Teildokument','log_file_%s'%self.label_aufgabentyp.text()[-1])

		with open(log_file) as f:
			beispieldaten_dateipfad = json.load(f)
			#beispieldaten_dateipfad=eval(beispieldaten_dateipfad)
			beispieldaten=list(beispieldaten_dateipfad.keys())					  
		

		#### typ1 ###
		# filename_teildokument = os.path.join(path_programm,'Typ 2 Aufgaben','Teildokument','Teildokument.tex')
		#####

		filename_teildokument = os.path.join(path_programm,'Teildokument','Teildokument_%s.tex'%self.label_aufgabentyp.text()[-1])
		try:
			file=open(filename_teildokument,"w", encoding='ISO-8859-1')
		except FileNotFoundError:
			os.makedirs(filename_teildokument) # If dir is not found make it recursivly
		file.write("\documentclass[a4paper,12pt]{report}\n\n"
		"\\usepackage{geometry}\n"	
		"\geometry{a4paper,left=18mm,right=18mm, top=2cm, bottom=2cm}\n\n" 
		"\\usepackage{lmodern}\n"
		"\\usepackage[T1]{fontenc}\n"
		"\\usepackage{eurosym}\n"
		"\\usepackage[latin1]{inputenc}\n"
		"\\usepackage[ngerman]{babel}\n")
		if self.cb_solution.isChecked()==True:
			file.write('\\usepackage[solution_on]{srdp-mathematik} % solution_on/off\n')
		else:
			file.write('\\usepackage[solution_off]{srdp-mathematik} % solution_on/off\n')
		file.write("\setcounter{Zufall}{0}\n\n\n"
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
		'\shorthandoff{"}\n')
		file.close()
		

		
		#### Typ1 ####			
	# 	if self.combobox_searchtype.currentText()=='Alle Dateien ausgeben, die alle Suchkriterien enthalten':
		#######
		if self.combobox_searchtype.currentText()=='Alle Dateien ausgeben, die ausschließlich diese Suchkriterien enthalten' and chosen_aufgabenformat=='Typ2Aufgaben':
			liste_kompetenzbereiche ={}
			gkliste = []
			r=1
			for all in list(beispieldaten_dateipfad.keys()):
				gkliste = []
				for gkbereich in dict_gk:
					if dict_gk[gkbereich] in all:
						gkliste.append(dict_gk[gkbereich])		
				liste_kompetenzbereiche.update({r:gkliste})
				r+=1
			for r in range(1,len(liste_kompetenzbereiche)+1):
				if liste_kompetenzbereiche[r]==[]:
					liste_kompetenzbereiche[r].append('-')
				for all in suchbegriffe:
					if all in liste_kompetenzbereiche[r]:
						liste_kompetenzbereiche[r].remove(all)
	

			gesammeltedateien=[]
			gesammeltedateien_temporary=[]
			for r in range(1,len(liste_kompetenzbereiche)+1):
				if liste_kompetenzbereiche[r] == []:
					gesammeltedateien.append(list(beispieldaten_dateipfad.keys())[r-1])
			#return
			# for all in gesammeltedateien:	
			# 	if entry_suchbegriffe.get().lower() in all.lower():
			# 		gesammeltedateien_temporary.append(all)
			gesammeltedateien=sorted(gesammeltedateien)

			# print(liste_kompetenzbereiche)
			# print(gesammeltedateien)
			# return
	# 		gesammeltedateien=list(beispieldaten_dateipfad.keys())
	# 		for item in suchbegriffe:
	# 			for all in gesammeltedateien[:]:
	# 				if item not in all:
	# 					gesammeltedateien.remove(all)
			
	# 		dict_gesammeltedateien={}
	# 		for all in gesammeltedateien:
	# 			dict_gesammeltedateien[all]=beispieldaten_dateipfdad[all]

					
		if self.combobox_searchtype.currentText()=='Alle Dateien ausgeben, die zumindest ein Suchkriterium enthalten' or chosen_aufgabenformat=='Typ1Aufgaben':
			gesammeltedateien=[]
			for all in suchbegriffe:
				for element in list(beispieldaten_dateipfad.keys())[:]:
					if all in element:
						gesammeltedateien.append(element)
			

		if not len(self.entry_suchbegriffe.text()) ==0:
			suchbegriffe.append(self.entry_suchbegriffe.text())
			if self.combobox_searchtype.currentText()=='Alle Dateien ausgeben, die zumindest ein Suchkriterium enthalten' or chosen_aufgabenformat=='Typ1Aufgaben':
				if len(gesammeltedateien)==0 and len(suchbegriffe)!=0:
					gesammeltedateien=list(beispieldaten_dateipfad.keys())				
			for all in gesammeltedateien[:]:			
				if self.entry_suchbegriffe.text().lower() not in all.lower():
						gesammeltedateien.remove(all)
		

		# if not len(self.entry_suchbegriffe.text())==0:
		# 	suchbegriffe.append(self.entry_suchbegriffe.text())

		gesammeltedateien.sort(key=self.natural_keys)
														

									
													
																   
		dict_gesammeltedateien={}
  

							 
		for all in gesammeltedateien:
			dict_gesammeltedateien[all]=beispieldaten_dateipfad[all]
	

		# print(dict_gesammeltedateien)
		# return	

	#### typ1 ###
	# ###############################################	
	# #### Auswahl der gesuchten Antwortformate ####
	# ###############################################
		if chosen_aufgabenformat=='Typ1Aufgaben':
			if self.cb_af_mc.isChecked() or self.cb_af_lt.isChecked() or self.cb_af_zo.isChecked() or self.cb_af_oa.isChecked()==True:
				if suchbegriffe==[]:
					dict_gesammeltedateien=beispieldaten_dateipfad
				for all_formats in list(dict_aufgabenformate.keys()):
					x=eval('self.cb_af_'+all_formats)
					if x.isChecked()==False:
						for all in list(dict_gesammeltedateien):
							if all_formats.upper() in all:
								del dict_gesammeltedateien[all]	
								
							# if all_formats in all:
								# del dict_gesammeltedateien[all]
					if x.isChecked()==True:
						suchbegriffe.append(all_formats)
	########################################################

	###############################################	
	#### Auswahl der gesuchten Klassen #########
	###############################################
		selected_klassen=[]
		if self.cb_k5.isChecked() or self.cb_k6.isChecked() or self.cb_k7.isChecked() or self.cb_k8.isChecked()==True or self.cb_mat.isChecked()==True:
			if suchbegriffe==[]:
				dict_gesammeltedateien=beispieldaten_dateipfad
			for all_formats in list(Klassen.keys()):
				x=eval('self.cb_'+all_formats)
				if x.isChecked()==True:
					selected_klassen.append(all_formats.upper())
					suchbegriffe.append(all_formats.upper())


			for all in list(dict_gesammeltedateien):
				if not any(all_formats.upper() in all for all_formats in selected_klassen):
					del dict_gesammeltedateien[all]

				
		#print(dict_gesammeltedateien)

		##############################
		if not dict_gesammeltedateien:
			QtWidgets.QApplication.restoreOverrideCursor()
			msg = QtWidgets.QMessageBox()
			msg.setIcon(QtWidgets.QMessageBox.Warning)
			msg.setWindowIcon(QtGui.QIcon(logo_path))
			msg.setText("Es wurden keine passenden Beispiele gefunden!")
			msg.setInformativeText('Es wird keine Datei ausgegeben.')
			msg.setWindowTitle("Warnung")
			#msg.setDetailedText("The details are as follows:")
			msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
			retval = msg.exec_()
			return




		beispieldaten.sort(key=self.natural_keys)
		file=open(filename_teildokument,"a", encoding='ISO-8859-1')
		file.write('\n \\scriptsize Suchbegriffe: ')
		for all in suchbegriffe:
			if all == suchbegriffe[-1]:
				file.write(all)
			else:	
				file.write(all + ', ')
		file.write('\\normalsize \n \n')


		for key, value in dict_gesammeltedateien.items():
			value=value.replace('\\','/') 
			file=open(filename_teildokument,"a", encoding='ISO-8859-1')
			### newpage only with typ2 !!

			if chosen_aufgabenformat=='Typ1Aufgaben':
				file.write('\input{"'+value+'"}%\n'
				'\hrule  \leer\n\n')
			elif chosen_aufgabenformat=='Typ2Aufgaben':
				file.write('\input{"'+value+'"}%\n'
				'\\newpage \n')
			# else:
			# 	if chosen_aufgabenformat=='Typ 1 Aufgaben':
			# 		file.write('\input{".'+value+'"}%\n'
			# 		'\hrule  \leer\n\n')
			# 	elif chosen_aufgabenformat=='Typ 2 Aufgaben':		
			# 		file.write('\input{".'+value+'"}%\n'
			# 		'\\newpage \n')

		file.write('\shorthandoff{"}\n'
		"\end{document}")

		file.close()
		

		QtWidgets.QApplication.restoreOverrideCursor()
		msg = QtWidgets.QMessageBox()
		msg.setIcon(QtWidgets.QMessageBox.Question)
		msg.setWindowIcon(QtGui.QIcon(logo_path))
		msg.setText('Insgesamt wurden '+ str(len(dict_gesammeltedateien)) + ' Beispiele gefunden.\n ')
		msg.setInformativeText('Soll die PDF Datei erstellt werden?')
		msg.setWindowTitle("Datei ausgeben?")
		msg.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
		buttonY = msg.button(QtWidgets.QMessageBox.Yes)
		buttonY.setText('Ja')
		buttonN = msg.button(QtWidgets.QMessageBox.No)
		buttonN.setText('Nein')
		msg.setDefaultButton(QtWidgets.QMessageBox.Yes)
		ret=msg.exec_()
		
		if ret==QtWidgets.QMessageBox.Yes:
			MainWindow.close()
			self.create_pdf()
			sys.exit(0)
		
		
		
	

#################################################################
###############################################################
################### Befehle Creator ###########################
#############################################################


	def add_picture(self):
			try:
				last_path=list(dict_picture_path.values())[-1]		
			except IndexError:
				last_path='C:\\'
			list_filename = QtWidgets.QFileDialog.getOpenFileNames(None, 'Select a folder:', last_path,  'Grafiken (*.eps)')
			i=len(dict_picture_path)

			self.label_bild_leer.hide()
			for all in list_filename[0]:
				head,tail=os.path.split(all)
				if tail in dict_picture_path.keys():
					pass
				else:
					head,tail=os.path.split(all)
					dict_picture_path[tail]=all
					x='self.label_bild_'+str(i)
					exec('%s= QtWidgets.QLabel(self.scrollAreaWidgetContents_bilder)'%x)
					eval(x).setObjectName(_fromUtf8("label_bild_%s"%i))
					# eval(x).setFrameShape(QtWidgets.QFrame.StyledPanel)
					eval(x).mousePressEvent = functools.partial(self.del_picture, name_of_image=x)
					self.verticalLayout.addWidget(eval(x))	
					eval(x).setText(_translate("MainWindow",tail, None))
					i+=1


	def del_picture(self, event, name_of_image=None):
		del dict_picture_path[eval(name_of_image).text()]
		eval(name_of_image).hide()
		if len(dict_picture_path)==0:
			self.label_bild_leer.show()


	def convert_jpgtoeps(self):
			msg = QtWidgets.QMessageBox()
			# msg.setIcon(QtWidgets.QMessageBox.Question)
			msg.setWindowIcon(QtGui.QIcon(logo_path))
			msg.setText('Wählen Sie alle Grafiken, die Sie konvertieren möchten.')
			#msg.setInformativeText('Möchten Sie das neue Update installieren?')
			msg.setWindowTitle("jpg2eps")
			msg.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
			button_durchsuchen = msg.button(QtWidgets.QMessageBox.Yes)
			button_durchsuchen.setText('Durchsuchen...')
			buttonN = msg.button(QtWidgets.QMessageBox.No)
			buttonN.setText('Abbrechen')
			ret=msg.exec_()	

			if ret==QtWidgets.QMessageBox.Yes:
				#filename =  filedialog.askopenfilenames(initialdir = last_path,title = "Durchsuchen...",filetypes = (('JPG-Dateien','*.jpg'),("Alle Dateien","*.*")))
				filename = QtWidgets.QFileDialog.getOpenFileNames(None, 'Select a folder:', 'C:\\',  'Bilder (*.jpg)')
				if filename[0]!=[]:
					for all in filename[0]:
						output=all.replace('jpg','eps')
						img=Image.open(all)
						img.save(output)

					msg = QtWidgets.QMessageBox()
					msg.setIcon(QtWidgets.QMessageBox.Information)
					if len(filename[0])==1:
						msg.setText('Es wurde '+str(len(filename[0]))+' Datei erfolgreich konvertiert.')
					else:
						msg.setText('Es wurden '+str(len(filename[0]))+' Dateien erfolgreich konvertiert.')	

					msg.setWindowTitle("jpg2eps")
					msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
					ret=msg.exec_()	
					return

	def chosen_aufgabenformat_cr(self):
		if self.comboBox_aufgabentyp_cr.currentText()=='Typ 1':
			self.label_keine_auswahl.hide()
			self.comboBox_af.show()
		if self.comboBox_aufgabentyp_cr.currentText()=='Typ 2':
			self.label_keine_auswahl.show()
			self.comboBox_af.hide()

	def gk_checked_cr(self, thema):
		global set_chosen_gk
		set_chosen_gk=set([])
		set_chosen_gk_label=set([])
		for all in {**ag_beschreibung,**fa_beschreibung,**an_beschreibung,**ws_beschreibung}: ## merged dictionionaries
			x=eval('self.cb_'+all+'_cr')
			if x.isChecked()==True:
				set_chosen_gk.add(all)
				set_chosen_gk_label.add(x.text())
		for all in k5_beschreibung:
			x=eval('self.cb_k5_cr_'+all+'_cr')
			if x.isChecked()==True:
				set_chosen_gk.add(all)
				set_chosen_gk_label.add(all.upper()+'(5)')
		for all in k6_beschreibung:
			x=eval('self.cb_k6_cr_'+all+'_cr')
			if x.isChecked()==True:
				set_chosen_gk.add(all)
				set_chosen_gk_label.add(all.upper() + '(6)')
		for all in k7_beschreibung:
			x=eval('self.cb_k7_cr_'+all+'_cr')
			if x.isChecked()==True:
				set_chosen_gk.add(all)
				set_chosen_gk_label.add(all.upper() + '(7)')
		for all in k8_beschreibung:
			x=eval('self.cb_k8_cr_'+all+'_cr')
			if x.isChecked()==True:
				set_chosen_gk.add(all)
				set_chosen_gk_label.add(all.upper() + '(8)')		

		x= ', '.join(sorted(set_chosen_gk_label))
		self.label_ausgew_gk.setText(_translate("MainWindow", str(x), None))


	def warning_window(self, text):
		QtWidgets.QApplication.restoreOverrideCursor()
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle("Warnung")
		msg.setIcon(QtWidgets.QMessageBox.Warning)
		msg.setWindowIcon(QtGui.QIcon(logo_path))
		msg.setText(text)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		retval = msg.exec_()


	def save_file(self):
		self.creator_mode='user'
		########################### WARNINGS ##### 
		######################################
		
		if set_chosen_gk==set([]):
			self.warning_window('Es wurden keine Grundkompetenzen zugewiesen.')
			return
		

		if self.comboBox_aufgabentyp_cr.currentText()=='Typ 1':
			if self.comboBox_af.currentText()=='bitte auswählen':
				self.warning_window('Es wurde kein Aufgabenformat ausgewählt.')
				return

			if len(set_chosen_gk)>1:
				self.warning_window('Es wurden zu viele Grundkompetenzen zugewiesen.')
				return

		textBox_Entry=self.plainTextEdit.toPlainText()
		list_chosen_gk=list(set_chosen_gk)


		####### CHECK INCL. & ATTACHED IMAGE RATIO ####

		if textBox_Entry.count('\includegraphics')>len(dict_picture_path):
			self.warning_window('Es sind zu wenige Bilder angehängt (' + str(len(dict_picture_path))+'/'+str(textBox_Entry.count('\includegraphics'))+').')
			return
		if textBox_Entry.count('\includegraphics')<len(dict_picture_path):
			self.warning_window('Es sind zu viele Bilder angehängt (' + str(len(dict_picture_path))+'/'+str(textBox_Entry.count('\includegraphics'))+').')
			return

		###############################	
		###### Check if Admin Mode is activated ####

		if self.lineEdit_titel.text().startswith('###'):
			try:
				x,y = self.lineEdit_titel.text().split('### ')
			except ValueError:
				x,y = self.lineEdit_titel.text().split('###')
			self.creator_mode='admin'
			edit_titel=y
		else:
			edit_titel=self.lineEdit_titel.text()	
		################################################

		QtWidgets.QApplication.restoreOverrideCursor()
		msg = QtWidgets.QMessageBox()
		msg.setIcon(QtWidgets.QMessageBox.Question)
		msg.setWindowIcon(QtGui.QIcon(logo_path))

		if len(list_chosen_gk)>1:
			temp_list_chosen_gk=[]
			for all in list_chosen_gk:
				if all in {**k5_beschreibung,**k6_beschreibung,**k7_beschreibung,**k8_beschreibung}:
					temp_list_chosen_gk.append(all.upper())	
				else:	
					temp_list_chosen_gk.append(dict_gk[all])
			# print(temp_list_chosen_gk)
			gk= ', '.join(sorted(temp_list_chosen_gk))
		else:
			if list_chosen_gk[0] in {**k5_beschreibung,**k6_beschreibung,**k7_beschreibung,**k8_beschreibung}:
				gk=list_chosen_gk[0].upper()

			else:
				gk=dict_gk[list_chosen_gk[0]]	

		if dict_picture_path!={}:
			bilder= ', '.join(dict_picture_path)
		else:
			bilder='-'

		if self.creator_mode=='user':
			if self.comboBox_aufgabentyp_cr.currentText()=='Typ 1':
				aufgabenformat='Aufgabenformat: %s\n'%self.comboBox_af.currentText()
			else:
				aufgabenformat=''
			msg.setWindowTitle("Aufgabe speichern")
			msg.setText(
			'Sind Sie sicher, dass Sie die folgendene Aufgabe speichern wollen?\n\n'
			'Aufgabentyp: {0}\n'
			'Titel: {1}\n{2}'
			'Grundkompetenz: {3}\n'
			'Quelle: {4}\n'
			'Bilder: {5}\n'.format(self.comboBox_aufgabentyp_cr.currentText(),
			edit_titel,aufgabenformat,gk,self.lineEdit_quelle.text(),bilder))
			# msg.setInformativeText('Soll die PDF Datei erstellt werden?')
			self.cb_confirm= QtWidgets.QCheckBox("Hiermit bestätige ich, dass ich die eingegebene Aufgabe eigenständig\nund unter Berücksichtigung des Urheberrechtsgesetzes verfasst habe.")									  
			self.cb_confirm.setObjectName(_fromUtf8("cb_confirm"))
			msg.setCheckBox(self.cb_confirm)
			msg.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
			buttonY = msg.button(QtWidgets.QMessageBox.Yes)
			buttonY.setText('Speichern')
			msg.setDefaultButton(QtWidgets.QMessageBox.Yes)
			buttonN = msg.button(QtWidgets.QMessageBox.No)
			buttonN.setText('Abbrechen')
			ret=msg.exec_()

		
			if ret==QtWidgets.QMessageBox.Yes:
				while self.cb_confirm.isChecked()==False:
					if ret==QtWidgets.QMessageBox.No:
						return
					else:
						self.warning_window('Bitte bestätigen Sie die Eigenständigkeitserklärung.')	
						ret=msg.exec_()
			else:
				return		
		
		if self.creator_mode=='admin':
			if self.comboBox_aufgabentyp_cr.currentText()=='Typ 1':
				aufgabenformat='Aufgabenformat: %s\n'%self.comboBox_af.currentText()
			else:
				aufgabenformat=''
			msg.setWindowTitle("Admin Modus - Aufgabe speichern")
			msg.setText(
			'Sind Sie sicher, dass Sie die folgendene Aufgabe speichern wollen?\n\n'
			'Aufgabentyp: {0}\n'
			'Titel: {1}\n{2}'
			'Grundkompetenz: {3}\n'
			'Quelle: {4}\n'
			'Bilder: {5}\n'.format(self.comboBox_aufgabentyp_cr.currentText(),
			edit_titel,aufgabenformat,gk,self.lineEdit_quelle.text(),bilder))
			self.cb_save=QtWidgets.QCheckBox("inoffizielle Aufgabe")
			self.cb_save.setObjectName(_fromUtf8("cb_save"))
			self.cb_save.setChecked(True)
			msg.setCheckBox(self.cb_save)
			
			msg.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
			buttonY = msg.button(QtWidgets.QMessageBox.Yes)
			buttonY.setText('Speichern')
			msg.setDefaultButton(QtWidgets.QMessageBox.Yes)
			buttonN = msg.button(QtWidgets.QMessageBox.No)
			buttonN.setText('Abbrechen')
			ret=msg.exec_()

			if ret==QtWidgets.QMessageBox.Yes:
				pass
			else:
				return			


		##### GET MAX FILENUMBER IN DIR #####
		if self.comboBox_aufgabentyp_cr.currentText()=='Typ 1':
			# print(set_chosen_gk)
			if list_chosen_gk[0] in {**k5_beschreibung,**k6_beschreibung,**k7_beschreibung,**k8_beschreibung}: ## merged dictionaries
				if list_chosen_gk[0] in k5_beschreibung:
					path_folder='5.Klasse'
				elif list_chosen_gk[0] in k6_beschreibung:
					path_folder='6.Klasse'
				elif list_chosen_gk[0] in k7_beschreibung:
					path_folder='7.Klasse'
				elif list_chosen_gk[0] in k8_beschreibung:
					path_folder='8.Klasse'
				
				if self.creator_mode=='admin' and self.cb_save.isChecked()==True:
					gk_path_temp=os.path.join(path_programm,'_database_inoffiziell','Typ1Aufgaben',path_folder,list_chosen_gk[0],'Einzelbeispiele')
				else:
					gk_path_temp=os.path.join(path_programm,'_database','Typ1Aufgaben',path_folder,list_chosen_gk[0],'Einzelbeispiele')


				
				z=list_chosen_gk[0].upper()+' - '
			else:
				path_folder='_Grundkompetenzen'
				if self.creator_mode=='admin' and self.cb_save.isChecked()==True:
					gk_path_temp=os.path.join(path_programm,'_database_inoffiziell','Typ1Aufgaben',path_folder,dict_gk[list_chosen_gk[0]][:2],dict_gk[list_chosen_gk[0]],'Einzelbeispiele')
				else:
					gk_path_temp=os.path.join(path_programm,'_database','Typ1Aufgaben',path_folder,dict_gk[list_chosen_gk[0]][:2],dict_gk[list_chosen_gk[0]],'Einzelbeispiele')
				z=dict_gk[list_chosen_gk[0]]+' - '

			if self.creator_mode=='admin' and self.cb_save.isChecked()==True:
				max_integer_file=1000
			else:
				max_integer_file=0
	    
			if not os.path.exists(gk_path_temp):
				print("Creating {} for you.".format(gk_path_temp))
				os.makedirs(gk_path_temp)
			for all in os.listdir(gk_path_temp):
				if all.endswith('.tex'):
					x,y=all.split(z)
					file_integer, file_extension=y.split('.tex')
					if int(file_integer)>max_integer_file:
						max_integer_file=int(file_integer)



		if self.comboBox_aufgabentyp_cr.currentText()=='Typ 2':
			if self.creator_mode=='admin' and self.cb_save.isChecked()==True:
				gk_path_temp=os.path.join(path_programm,'_database_inoffiziell','Typ2Aufgaben','Einzelbeispiele')
			else:
				gk_path_temp=os.path.join(path_programm,'_database','Typ2Aufgaben','Einzelbeispiele')
			max_integer_file=0
			for all in os.listdir(gk_path_temp):
		
				if all.endswith('.tex'):
					file_integer, file_extension=all.split('.tex')
					if int(file_integer)>max_integer_file:
						max_integer_file=int(file_integer)
		

		####### Checks files in 'Beispieleinreichung' #####
		##################################################


		if self.creator_mode=='admin':
			pass
		else:
			try:
				path_saved_files=os.path.join(path_programm,'Beispieleinreichung')
				if list_chosen_gk[0] in {**k5_beschreibung,**k6_beschreibung,**k7_beschreibung,**k8_beschreibung}: ## merged dictionaries
					if list_chosen_gk[0] in k5_beschreibung:
						file_name_klasse='K5'
					elif list_chosen_gk[0] in k6_beschreibung:
						file_name_klasse='K6'
					elif list_chosen_gk[0] in k7_beschreibung:
						file_name_klasse='K7'
					elif list_chosen_gk[0] in k8_beschreibung:
						file_name_klasse='K8'				
					z=file_name_klasse+' - '+list_chosen_gk[0].upper()+' - '			

				else:
					z=dict_gk[list_chosen_gk[0]]+' - '
				if self.comboBox_aufgabentyp_cr.currentText()=='Typ 1':
					for all in os.listdir(path_saved_files):
						if all.endswith('.tex'):
							if z in all:
								x,y=all.split(z)
								file_integer, file_extension=y.split('.tex')
								if int(file_integer)>max_integer_file:
									max_integer_file=int(file_integer)

				if self.comboBox_aufgabentyp_cr.currentText()=='Typ 2':
					for all in os.listdir(path_saved_files): 	
						if all.endswith('.tex'):
							if '-' in all:
								pass
							else:
								file_integer, file_extension=all.split('.tex')
								if int(file_integer)>max_integer_file:
									max_integer_file=int(file_integer)
			except FileNotFoundError:
				msg = QtWidgets.QMessageBox()
				msg.setWindowTitle("Fehlermeldung")
				msg.setIcon(QtWidgets.QMessageBox.Critical)
				msg.setWindowIcon(QtGui.QIcon(logo_path))
				msg.setText('Der Ordner "Beispieleinreichung" konnte nicht gefunden werden und\nmuss zuerst für Sie freigegeben werden.')
				msg.setInformativeText('Derzeit können keine neuen Aufgaben eingegeben werden.')
				msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
				retval = msg.exec_()
				return		
		############################################################################

		for all in dict_picture_path:
			head, tail=os.path.split(all)
			x = '{'+tail+'}'
			name, ext =os.path.splitext(tail)
			if self.creator_mode=='admin' and self.cb_save.isChecked()==True:
				if x in textBox_Entry and self.comboBox_aufgabentyp_cr.currentText()=='Typ 1':
					textBox_Entry=str(textBox_Entry).replace(tail,'../_database_inoffiziell/Bilder/'+list_chosen_gk[0].upper()+'_'+str(max_integer_file+1)+'_'+tail)
				if x in textBox_Entry and self.comboBox_aufgabentyp_cr.currentText()=='Typ 2':
					textBox_Entry=str(textBox_Entry).replace(tail,'../_database_inoffiziell/Bilder/'+str(max_integer_file+1)+'_'+tail)
			else:
				if x in textBox_Entry and self.comboBox_aufgabentyp_cr.currentText()=='Typ 1':
					textBox_Entry=str(textBox_Entry).replace(tail,'../_database/Bilder/'+list_chosen_gk[0].upper()+'_'+str(max_integer_file+1)+'_'+tail)
				if x in textBox_Entry and self.comboBox_aufgabentyp_cr.currentText()=='Typ 2':
					textBox_Entry=str(textBox_Entry).replace(tail,'../_database/Bilder/'+str(max_integer_file+1)+'_'+tail)
		

		#copy_image_path=os.path.join(path_programm,'_database','Bilder') ### direct save
		if self.creator_mode=='admin':
			if self.cb_save.isChecked()==False:
				copy_image_path=os.path.join(path_programm,'_database','Bilder') ### direct save
			if self.cb_save.isChecked()==True:
				copy_image_path=os.path.join(path_programm,'_database_inoffiziell','Bilder') ### direct save
		else:	
			copy_image_path=os.path.join(path_programm,'Beispieleinreichung','Bilder') ### indirect save

		for all in list(dict_picture_path.values()):
			image_path_temp=all
			head, tail=os.path.split(image_path_temp)
			copy_image_file_temp=os.path.join(copy_image_path,tail)
			try:
				shutil.copy(image_path_temp,copy_image_file_temp)
			except FileNotFoundError:
				try: 
					os.mkdir(copy_image_path)
					shutil.copy(image_path_temp,copy_image_file_temp)
				except FileNotFoundError:
					msg = QtWidgets.QMessageBox()
					msg.setWindowTitle("Fehlermeldung")
					msg.setIcon(QtWidgets.QMessageBox.Critical)
					msg.setWindowIcon(QtGui.QIcon(logo_path))
					msg.setText('Der Ordner "Beispieleinreichung" konnte nicht gefunden werden und\nmuss zuerst für Sie freigegeben werden.')
					msg.setInformativeText('Derzeit können keine neuen Aufgaben eingegeben werden.')
					msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
					retval = msg.exec_()
					return	

			if self.comboBox_aufgabentyp_cr.currentText()=='Typ 1':
				if self.creator_mode=='admin':
					if self.cb_save.isChecked()==False:
						x=os.rename(copy_image_file_temp,'%s/_database/Bilder/'% path_programm +list_chosen_gk[0].upper()+'_'+str(max_integer_file+1)+'_'+tail) ### direct save
					if self.cb_save.isChecked()==True:
						x=os.rename(copy_image_file_temp,'%s/_database_inoffiziell/Bilder/'% path_programm +list_chosen_gk[0].upper()+'_'+str(max_integer_file+1)+'_'+tail) ### direct save
				else:
					x=os.rename(copy_image_file_temp,'%s/Beispieleinreichung/Bilder/'% path_programm +list_chosen_gk[0].upper()+'_'+str(max_integer_file+1)+'_'+tail) ### indirect
			if self.comboBox_aufgabentyp_cr.currentText()=='Typ 2':
				if self.creator_mode=='admin':
					if self.cb_save.isChecked()==False:
						x=os.rename(copy_image_file_temp,'%s/_database/Bilder/'% path_programm +str(max_integer_file+1)+'_'+tail) ### direct save
					if self.cb_save.isChecked()==True:
						x=os.rename(copy_image_file_temp,'%s/_database_inoffiziell/Bilder/'% path_programm +str(max_integer_file+1)+'_'+tail) ### direct save
				else:
					x=os.rename(copy_image_file_temp,'%s/Beispieleinreichung/Bilder/'%path_programm +str(max_integer_file+1)+'_'+tail) ### indirect save		



		if self.comboBox_aufgabentyp_cr.currentText()=='Typ 1':
			if self.creator_mode=='admin':
				pass
			else:
				gk_path_temp=os.path.join(path_programm,'Beispieleinreichung') ## not direct save (path changed - comment/uncomment)

			if list_chosen_gk[0] in {**k5_beschreibung,**k6_beschreibung,**k7_beschreibung,**k8_beschreibung}: ## merged dictionaries
				if list_chosen_gk[0] in k5_beschreibung:
					file_name_klasse='K5'
				elif list_chosen_gk[0] in k6_beschreibung:
					file_name_klasse='K6'
				elif list_chosen_gk[0] in k7_beschreibung:
					file_name_klasse='K7'
				elif list_chosen_gk[0] in k8_beschreibung:
					file_name_klasse='K8'				
				file_name=os.path.join(gk_path_temp,file_name_klasse+' - '+list_chosen_gk[0].upper()+' - '+str(max_integer_file+1)+'.tex')
				
				chosen_af=list(dict_aufgabenformate.keys())[list(dict_aufgabenformate.values()).index(self.comboBox_af.currentText())].upper()

				#print('\section{'+file_name_klasse+' - '+list_chosen_gk[0].upper()+" - "+str(max_integer_file+1) +" - " + self.lineEdit_titel.text()+" - "+chosen_af+' - '+self.lineEdit_quelle.text())
				try:
					file=open(file_name,"w")
				except FileNotFoundError:
					msg = QtWidgets.QMessageBox()
					msg.setWindowTitle("Fehlermeldung")
					msg.setIcon(QtWidgets.QMessageBox.Critical)
					msg.setWindowIcon(QtGui.QIcon(logo_path))
					msg.setText('Der Ordner "Beispieleinreichung" konnte nicht gefunden werden und\nmuss zuerst für Sie freigegeben werden.')
					msg.setInformativeText('Derzeit können keine neuen Aufgaben eingegeben werden.')
					msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
					retval = msg.exec_()
					return	
				
				
				file.write('\section{'+file_name_klasse+' - '+list_chosen_gk[0].upper()+" - "+str(max_integer_file+1) +" - " + edit_titel+" - "+chosen_af+' - '+self.lineEdit_quelle.text()+"}\n\n"
				"\\begin{beispiel}["+file_name_klasse+' - '+list_chosen_gk[0].upper()+"]{"+str(self.spinBox_punkte.value())+"}\n"+textBox_Entry+
				"\n\\end{beispiel}")
				file.close()

			else:
				file_name=os.path.join(gk_path_temp,dict_gk[list_chosen_gk[0]]+' - '+str(max_integer_file+1)+'.tex')
				
				try:
					file=open(file_name,"w")
				except FileNotFoundError:
					msg = QtWidgets.QMessageBox()
					msg.setWindowTitle("Fehlermeldung")
					msg.setIcon(QtWidgets.QMessageBox.Critical)
					msg.setWindowIcon(QtGui.QIcon(logo_path))
					msg.setText('Der Ordner "Beispieleinreichung" konnte nicht gefunden werden und\nmuss zuerst für Sie freigegeben werden.')
					msg.setInformativeText('Derzeit können keine neuen Aufgaben eingegeben werden.')
					msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
					retval = msg.exec_()
					return

				if self.comboBox_klassen_cr.currentText()=='-':
					chosen_af=list(dict_aufgabenformate.keys())[list(dict_aufgabenformate.values()).index(self.comboBox_af.currentText())].upper()
					file.write("\section{"+dict_gk[list_chosen_gk[0]]+" - "+str(max_integer_file+1) +" - "+edit_titel+" - "+chosen_af+" - "+self.lineEdit_quelle.text()+"}\n\n"
					"\\begin{beispiel}["+dict_gk[list_chosen_gk[0]]+"]{"+str(self.spinBox_punkte.value())+"}\n"+textBox_Entry+
					"\n\\end{beispiel}")
				else:
					try:
						klasse='K'+re.search(r'\d+',self.comboBox_klassen_cr.currentText()).group() ### get selected grade
					except AttributeError:
						klasse='MAT'			
					chosen_af=list(dict_aufgabenformate.keys())[list(dict_aufgabenformate.values()).index(self.comboBox_af.currentText())].upper()
					file.write("\section{"+dict_gk[list_chosen_gk[0]]+" - "+str(max_integer_file+1) +' - '+ klasse +" - "+edit_titel+" - "+chosen_af+" - "+self.lineEdit_quelle.text()+"}\n\n"
					"\\begin{beispiel}["+dict_gk[list_chosen_gk[0]]+"]{"+str(self.spinBox_punkte.value())+"}\n"+textBox_Entry+
					"\n\\end{beispiel}")		
				file.close()			



		if self.comboBox_aufgabentyp_cr.currentText()=='Typ 2':
			themen_klasse_auswahl=[]
			gk_auswahl=[]

			# print(list_chosen_gk)
			for all in list_chosen_gk:
				if all in {**k5_beschreibung,**k6_beschreibung,**k7_beschreibung,**k8_beschreibung}:
					themen_klasse_auswahl.append(all.upper())
				else:
					gk_auswahl.append(dict_gk[all])

			gk_auswahl_joined=', '.join(sorted(gk_auswahl))
			themen_klasse_auswahl_joined=', '.join(sorted(themen_klasse_auswahl)) 			 


			if self.creator_mode=='admin':
				if self.cb_save.isChecked()==False:
					file_name=os.path.join(path_programm,'_database','Typ2Aufgaben','Einzelbeispiele',str(max_integer_file+1)+'.tex') ### direct save
				if self.cb_save.isChecked()==True:
					file_name=os.path.join(path_programm,'_database_inoffiziell','Typ2Aufgaben','Einzelbeispiele',str(max_integer_file+1)+'.tex') ### direct save
			else:
				file_name=os.path.join(path_programm,'Beispieleinreichung',str(max_integer_file+1)+'.tex') ### not direct save

			try:
				file=open(file_name,"w")
			except FileNotFoundError:
				msg = QtWidgets.QMessageBox()
				msg.setWindowTitle("Fehlermeldung")
				msg.setIcon(QtWidgets.QMessageBox.Critical)
				msg.setWindowIcon(QtGui.QIcon(logo_path))
				msg.setText('Der Ordner "Beispieleinreichung" konnte nicht gefunden werden und\nmuss zuerst für Sie freigegeben werden.')
				msg.setInformativeText('Derzeit können keine neuen Aufgaben eingegeben werden.')
				msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
				retval = msg.exec_()
				return

			klasse=''
			themen_klasse=''
			gk=''

			if self.comboBox_klassen_cr.currentText()=='-':
				pass	
			else:	
				try:
					klasse='K'+re.search(r'\d+',self.comboBox_klassen_cr.currentText()).group()+' - ' ### get selected grade
				except AttributeError:
					klasse='MAT - '

			if themen_klasse_auswahl==[]:
				gk=gk_auswahl_joined+' - '

			else: #elif gk_auswahl==[]
				themen_klasse=themen_klasse_auswahl_joined+' - '
				x=9
				for all in themen_klasse_auswahl:
					if all.lower() in k5_beschreibung:
						if x>5:
							x=5
					elif all.lower() in k6_beschreibung:
						if x>6:
							x=6
					elif all.lower() in k7_beschreibung:
						if x>7:
							x=7
					elif all.lower() in k8_beschreibung:
						if x>8:
							x=8
				if x<9 and klasse=='':
					klasse='K%s - '%x

				if gk_auswahl !=[]:
					gk=gk_auswahl_joined+' - '

			file.write("\section{"+str(max_integer_file+1)+' - '+klasse + themen_klasse + gk +edit_titel+" - "+self.lineEdit_quelle.text()+"}\n\n"
			"\\begin{langesbeispiel} \item["+str(self.spinBox_punkte.value())+"] %PUNKTE DES BEISPIELS\n"+textBox_Entry+
			"\n\\end{langesbeispiel}")			

			file.close()




		if dict_picture_path!={}:
			x= ', '.join(dict_picture_path)
		else:
			x='-'


		chosen_typ=self.comboBox_aufgabentyp_cr.currentText()[-1]
		if chosen_typ=='1':
			if list_chosen_gk[0] in {**k5_beschreibung,**k6_beschreibung,**k7_beschreibung,**k8_beschreibung}: ## merged dictionaries
				if list_chosen_gk[0] in k5_beschreibung:
					file_name_klasse='K5'
				elif list_chosen_gk[0] in k6_beschreibung:
					file_name_klasse='K6'
				elif list_chosen_gk[0] in k7_beschreibung:
					file_name_klasse='K7'
				elif list_chosen_gk[0] in k8_beschreibung:
					file_name_klasse='K8'				
				chosen_gk=file_name_klasse+' - '+list_chosen_gk[0].upper()
			else:
				chosen_gk = dict_gk[list_chosen_gk[0]]
		if chosen_typ=='2':
			chosen_gk= ', '.join(sorted(gk_auswahl+themen_klasse_auswahl))

		if self.creator_mode=='admin':
			if self.cb_save.isChecked()==False:
				zusatz_info=' (offiziell)'
			if self.cb_save.isChecked()==True:
				zusatz_info=' (inoffiziell)'
		else:
			zusatz_info=''

		QtWidgets.QApplication.restoreOverrideCursor()
		msg = QtWidgets.QMessageBox()
		msg.setIcon(QtWidgets.QMessageBox.Information)
		msg.setWindowTitle("Admin Modus - Aufgabe erfolgreich gespeichert")
		msg.setWindowIcon(QtGui.QIcon(logo_path))
		msg.setText('Die Typ{0}-Aufgabe mit dem Titel\n\n"{1}"\n\nwurde gespeichert.'.format(chosen_typ, edit_titel))
		msg.setDetailedText('Details{0}\n'
		'Grundkompetenz(en): {1}\n'
		'Punkte: {2}\n'
		'Klasse: {3}\n'
		'Bilder: {4}'.format(zusatz_info,chosen_gk, self.spinBox_punkte.value(), self.comboBox_klassen_cr.currentText(), x))
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		retval = msg.exec_()
		self.suchfenster_reset()


##################################################################
##################################################################

	def aufgaben_suchen(self):
		for all in widgets_create:
			if 'action' in all:
				exec('self.%s.setVisible(False)'%all)
			elif 'menu' in all:
				exec('self.menuBar.removeAction(self.%s.menuAction())'%all)	
			else:
				exec('self.%s.hide()'%all)

		for all in widgets_search:
			if 'action' in all:
				exec('self.%s.setVisible(True)'%all)
			elif 'menu' in all:
				exec('self.menuBar.addAction(self.%s.menuAction())'%all)	
			else:
				if all == 'combobox_searchtype':
					if self.label_aufgabentyp.text()[-1]=='2':
						exec('self.%s.show()'%all)
				else:
					exec('self.%s.show()'%all)


	def neue_aufgabe_erstellen(self):
		MainWindow.setMenuBar(self.menuBar)

		for all in widgets_search:		
			if 'action' in all:
				exec('self.%s.setVisible(False)'%all)
			elif 'menu' in all:
				exec('self.menuBar.removeAction(self.%s.menuAction())'%all)	
			else:
				exec('self.%s.hide()'%all)

		for all in widgets_create:
			if 'action' in all:
				exec('self.%s.setVisible(True)'%all)
			elif 'menu' in all:
				exec('self.menuBar.addAction(self.%s.menuAction())'%all)	
			else:
				exec('self.%s.show()'%all)

		
	
if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	MainWindow = QMainWindow()

	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)

	MainWindow.show()
	sys.exit(app.exec_())


