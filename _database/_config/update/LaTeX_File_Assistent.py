#!/usr/bin/python3
# -*- coding: utf-8 -*-
#### Version number ###
__version__='v1.2'
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
import yaml


# Load Config-file
def config_loader(pathToFile,parameter):
    config1 = yaml.safe_load(open(pathToFile, encoding='utf8'))
    return config1[parameter]

config_file = './_database/_config/config1.yml'

ag_beschreibung = config_loader(config_file,'ag_beschreibung')
an_beschreibung = config_loader(config_file,'an_beschreibung')
fa_beschreibung = config_loader(config_file,'fa_beschreibung')
ws_beschreibung = config_loader(config_file,'ws_beschreibung')

k5_beschreibung = config_loader(config_file,'k5_beschreibung')
k6_beschreibung = config_loader(config_file,'k6_beschreibung')
k7_beschreibung = config_loader(config_file,'k7_beschreibung')
k8_beschreibung = config_loader(config_file,'k8_beschreibung')

dict_gk = config_loader(config_file,'dict_gk')
set_af = config_loader(config_file,'set_af')
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



class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		self.check_for_update()	
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(950, 583)
		MainWindow.setMaximumSize(QtCore.QSize(1078, 16777215))
		MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
		MainWindow.setStyleSheet(_fromUtf8(""))
		#MainWindow.setWindowIcon(QtWidgets.QIcon(r'C:\Users\Christoph\Desktop\lupe.png'))
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)
		self.menuBar = QtWidgets.QMenuBar(MainWindow)
		self.menuBar.setGeometry(QtCore.QRect(0, 0, 378, 21))
		self.menuBar.setObjectName(_fromUtf8("menuBar"))
		self.menuDateityp = QtWidgets.QMenu(self.menuBar)
		self.menuDateityp.setObjectName(_fromUtf8("menuDateityp"))
		self.menuDatei = QtWidgets.QMenu(self.menuBar)
		self.menuDatei.setObjectName(_fromUtf8("menuDatei"))
		self.menuHelp = QtWidgets.QMenu(self.menuBar)
		self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
		MainWindow.setMenuBar(self.menuBar)
		self.actionNew = QtWidgets.QAction(MainWindow)
		self.actionNew.setObjectName(_fromUtf8("actionNew"))
		self.actionAufgaben_Typ1 = QtWidgets.QAction(MainWindow)
		self.actionAufgaben_Typ1.setObjectName(_fromUtf8("actionAufgaben_Typ1"))
		self.actionAufgaben_Typ2 = QtWidgets.QAction(MainWindow)
		self.actionAufgaben_Typ2.setObjectName(_fromUtf8("actionAufgaben_Typ2"))
		self.actionRefresh_Database = QtWidgets.QAction(MainWindow)
		self.actionRefresh_Database.setObjectName(_fromUtf8("actionRefresh_Database"))
		self.actionsuchfenster_reset = QtWidgets.QAction(MainWindow)
		self.actionsuchfenster_reset.setObjectName(_fromUtf8("actionsuchfenster_reset"))
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
		self.menuBar.addAction(self.menuDatei.menuAction())
		self.menuBar.addAction(self.menuDateityp.menuAction())
		self.menuBar.addAction(self.menuHelp.menuAction())
		self.groupBox_ausgew_gk = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_ausgew_gk.setObjectName(_fromUtf8("groupBox_ausgew_gk"))
		self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_ausgew_gk)
		self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
		self.label_gk = QtWidgets.QLabel(self.groupBox_ausgew_gk)
		self.label_gk.setWordWrap(True)
		self.label_gk.setObjectName(_fromUtf8("label_gk"))
		self.verticalLayout_2.addWidget(self.label_gk)
		# self.label_gk_an = QtWidgets.QLabel(self.groupBox_ausgew_gk)
		# self.label_gk_an.setObjectName(_fromUtf8("label_gk_an"))
		# self.verticalLayout_2.addWidget(self.label_gk_an)
		# self.label_gk_fa = QtWidgets.QLabel(self.groupBox_ausgew_gk)
		# self.label_gk_fa.setObjectName(_fromUtf8("label_gk_fa"))
		# self.verticalLayout_2.addWidget(self.label_gk_fa)
		# self.label_gk_ws = QtWidgets.QLabel(self.groupBox_ausgew_gk)
		# self.label_gk_ws.setObjectName(_fromUtf8("label_gk_ws"))
		# self.verticalLayout_2.addWidget(self.label_gk_ws)
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
		# self.menu_aufgabentyp = QtWidgets.QComboBox(self.centralwidget)
		# self.menu_aufgabentyp.setObjectName(_fromUtf8("menu_aufgabentyp"))
		# self.menu_aufgabentyp.addItem(_fromUtf8(""))
		# self.menu_aufgabentyp.addItem(_fromUtf8(""))
		# self.horizontalLayout_combobox.addWidget(self.menu_aufgabentyp)
		self.menu_searchtype = QtWidgets.QComboBox(self.centralwidget)
		self.menu_searchtype.setEnabled(True)
		self.menu_searchtype.setObjectName(_fromUtf8("menu_searchtype"))
		self.menu_searchtype.addItem(_fromUtf8(""))
		self.menu_searchtype.addItem(_fromUtf8(""))
		self.horizontalLayout_combobox.addWidget(self.menu_searchtype)
		self.gridLayout.addLayout(self.horizontalLayout_combobox, 0, 3, 1, 1)
		self.menu_searchtype.hide()
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
		self.tab_widget_gk.setMaximumSize(QtCore.QSize(650, 16777215))
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
		
		########
		self.gridLayout_11.addWidget(self.tab_widget_gk, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.groupBox_gk, 1, 3, 2, 1)
		MainWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)
		self.actionNew = QtWidgets.QAction(MainWindow)
		self.actionNew.setObjectName(_fromUtf8("actionNew"))

		self.retranslateUi(MainWindow)
		self.tabWidget.setCurrentIndex(0)
		
															   
		self.tab_widget_gk.setCurrentIndex(0)
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

	
		############################################################################################
		##############################################################################################
	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("LaTeX File Assistent", "LaTeX File Assistent", None))
		self.menuDateityp.setTitle(_translate("MainWindow", "Aufgabentyp", None))
		self.menuDatei.setTitle(_translate("MainWindow", "Datei", None))
		self.menuHelp.setTitle(_translate("MainWindow", "?", None))
		self.actionNew.setText(_translate("MainWindow", "Reset", None))
		self.actionAufgaben_Typ1.setText(_translate("MainWindow", "Typ 1 Aufgaben", None))
		self.actionAufgaben_Typ1.setShortcut('Ctrl+1')
		self.actionAufgaben_Typ2.setText(_translate("MainWindow", "Typ 2 Aufgaben", None))
		self.actionAufgaben_Typ2.setShortcut('Ctrl+2')
		self.actionInfo.setText(_translate("MainWindow", "Info", None))
		self.actionsuchfenster_reset.setText(_translate("MainWindow", "Reset", None))
		self.actionsuchfenster_reset.setShortcut("F4")
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
			log_file=os.path.join(os.path.dirname('__file__'),'Teildokument','log_file_1')
			self.label_update.setText(_translate("MainWindow", 'Letztes Update: ' + self.modification_date(log_file).strftime('%d.%m.%y - %H:%M'), None))
		except FileNotFoundError:
			self.label_update.setText(_translate("MainWindow", "Letztes Update: ---", None))
		self.btn_suche.setText(_translate("MainWindow", "Suche starten", None))


		#self.btn_refreshddb.setText(_translate("MainWindow", "Refresh Database", None))
		# self.menu_aufgabentyp.setItemText(0, _translate("MainWindow", "Typ 1", None))
		# self.menu_aufgabentyp.setItemText(1, _translate("MainWindow", "Typ 2", None))
		self.menu_searchtype.setItemText(0, _translate("MainWindow", "Alle Dateien ausgeben, die zumindest ein Suchkriterium enthalten", None))

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
		#self.menu_searchtype.setItemText(1, _translate("MainWindow", "Alle Dateien ausgeben, die alle Suchkriterien enthalten", None))
		######
		
		### Typ2
		self.menu_searchtype.setItemText(1, _translate("MainWindow", "Alle Dateien ausgeben, die ausschließlich diese Suchkriterien enthalten", None))
		######
		
		self.groupBox_themen_klasse.setTitle(_translate("MainWindow", "Themen Schulstufe", None))
		self.name_checkbox_klassen(5)
		self.name_checkbox_klassen(6)
		self.name_checkbox_klassen(7)
		self.name_checkbox_klassen(8)																					 

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
		for all in ag_beschreibung:
			x=eval('self.cb_'+all)
			x.setToolTip(ag_beschreibung[all])
			
		for all in an_beschreibung:
			x=eval('self.cb_'+all)
			x.setToolTip(an_beschreibung[all])

		for all in fa_beschreibung:
			x=eval('self.cb_'+all)
			x.setToolTip(fa_beschreibung[all])
			
		for all in ws_beschreibung:
			x=eval('self.cb_'+all)
			x.setToolTip(ws_beschreibung[all])
			
#########################################
		self.name_checkbox_gk(ag_beschreibung)
		self.name_checkbox_gk(an_beschreibung)
		self.name_checkbox_gk(fa_beschreibung)
		self.name_checkbox_gk(ws_beschreibung)

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
		self.actionNew.setText(_translate("MainWindow", "Reset", None))
		self.label_gk_rest.setText(_translate("MainWindow", "", None))
		self.label_gk.setText(_translate("MainWindow", "", None))
		# self.label_gk_an.setText(_translate("MainWindow", "", None))
		# self.label_gk_fa.setText(_translate("MainWindow", "", None))
		# self.label_gk_ws.setText(_translate("MainWindow", "", None))
		self.actionExit.setText(_translate("MainWindow", "Exit", None))
		
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
		f=open('_database/_config/update/__version__.txt','r')
		if __version__ not in f.read():
			msg = QtWidgets.QMessageBox()
			msg.setIcon(QtWidgets.QMessageBox.Question)
			#msg.setWindowIcon(QtWidgets.QIcon(r'C:\Users\Christoph\Desktop\lupe.png'))
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
				if extension=='.py':
					filename_update=os.path.join(os.path.dirname('__file__'),'_database','_config','update','update.py')
				elif extension=='.exe':
					filename_update=os.path.join(os.path.dirname('__file__'),'_database','_config','update','update.exe')
				if sys.platform.startswith('linux'):
				    os.system(filename_update)
				elif sys.platform.startswith('darwin'):
				    os.system(filename_update)
				else:
				    os.startfile(filename_update)										
				sys.exit(0)



	############################################################################
	############################################################################
	############### Buttons Check_ALL ######################################
	############################################################################
	############################################################################

	def suchfenster_reset(self):
		for all in ag_beschreibung:
			x=eval('self.cb_'+all)
			x.setChecked(False)
		for all in an_beschreibung:
			x=eval('self.cb_'+all)
			x.setChecked(False)
		for all in fa_beschreibung:
			x=eval('self.cb_'+all)
			x.setChecked(False)
		for all in ws_beschreibung:
			x=eval('self.cb_'+all)
			x.setChecked(False)
		for r in range(5,9):
			dict_klasse=eval('k'+str(r)+'_beschreibung')	
			for all in dict_klasse:
				x=eval('self.cb_k'+str(r)+'_'+all)
				x.setChecked(False)
		for all in Klassen:
			x=eval('self.cb_'+all)
			x.setChecked(False)
		for all in set_af:
			x=eval('self.cb_af_'+all)
			x.setChecked(False)
		self.entry_suchbegriffe.setText('')	
		self.cb_solution.setChecked(True)	




	def close_app(self):
		sys.exit(0)

	def show_info(self):
		QtWidgets.QApplication.restoreOverrideCursor()
		msg = QtWidgets.QMessageBox()
		msg.setIcon(QtWidgets.QMessageBox.Information)
		#msg.setWindowIcon(QtWidgets.QIcon(r'C:\Users\Christoph\Desktop\lupe.png'))
		msg.setText("LaTeX File Assistent %s\n\nAuthor: Christoph Weberndorfer\nLicense: GNU General Public License v3.0"%__version__)
		msg.setInformativeText("Last Update: 03/19")
		msg.setWindowTitle("Über LaTeX File Assitent")
		#msg.setDetailedText("The details are as follows:")
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		retval = msg.exec_()
	
	def get_logfile(self):
		try:
			x='log_file_%s'%self.label_aufgabentyp.text()[-1]
			log_file=os.path.join(os.path.dirname('__file__'),'Teildokument',x)
			self.label_update.setText(_translate("MainWindow", 'Letztes Update: ' + self.modification_date(log_file).strftime('%d.%m.%y - %H:%M'), None))
		except FileNotFoundError:
			self.label_update.setText(_translate("MainWindow", "Letztes Update: ---", None))

	def chosen_aufgabenformat_typ1(self):
		self.label_aufgabentyp.setText(_translate("MainWindow", "Aufgabentyp: Typ 1", None))
		self.groupBox_af.show()
		self.menu_searchtype.hide()
		self.get_logfile()
	
		
		#self.gridLayout.addWidget(self.groupBox, 4, 0, 2, 1)
	
	def chosen_aufgabenformat_typ2(self):
		self.label_aufgabentyp.setText(_translate("MainWindow", "Aufgabentyp: Typ 2", None))
		self.groupBox_af.hide()
		self.menu_searchtype.show()
		self.get_logfile()

	def create_checkbox_gk(self,gk_type,chosen_dict):
		row=0
		column=0
		max_row=9
		for all in chosen_dict:
			exec('self.cb_'+all+'=QtWidgets.QCheckBox(self.tab_'+gk_type+')')
			exec('self.cb_'+all+'.setObjectName(_fromUtf8("cb_'+all+'"))')
			x=eval('self.cb_'+all)
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
			exec('self.cb_'+klasse+'_'+all+'= QtWidgets.QCheckBox(self.tab_'+klasse+')')	
			exec('self.cb_'+klasse+'_'+all+'.setObjectName(_fromUtf8("cb_'+klasse+'_'+all+'"))')
			grid=eval('self.gridLayout_'+klasse)
			x=eval('self.cb_'+klasse+'_'+all)
			grid.addWidget(x, row,column, 1, 1)	

			if row>max_row:
				row=0
				column+=1
			else:
				row+=1

			exec('self.btn_'+klasse+'= QtWidgets.QPushButton(self.tab_'+klasse+')')
			exec('self.btn_%s.setStyleSheet(_fromUtf8("background-color: rgb(240, 240, 240);"))'%klasse)
			exec('self.btn_'+klasse+'.setObjectName(_fromUtf8("btn_'+klasse+'"))')
			exec('self.gridLayout_'+klasse+'.addWidget(self.btn_'+klasse+', max_row, column+1, 1, 1, QtCore.Qt.AlignRight)')


	def name_checkbox_gk(self, chosen_dict):
		for all in chosen_dict:
			x=eval('self.cb_'+all)
			x.setText(_translate("MainWindow", dict_gk[all], None))

	def name_checkbox_klassen(self, klasse):
		chosen_dict=eval('k'+str(klasse)+'_beschreibung')
		for all in chosen_dict:
			x=eval('self.cb_k'+str(klasse)+'_'+all)
			x.setText(_translate("MainWindow", chosen_dict[all], None))		

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

		for root, dirs, files in os.walk(os.path.join('.','_database', chosen_aufgabenformat)):
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

		for root, dirs, files in os.walk(os.path.join('.','_database_inoffiziell', chosen_aufgabenformat)):
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
		
		log_file=os.path.join(os.path.dirname('__file__'),'Teildokument','log_file_%s'%self.label_aufgabentyp.text()[-1])
		
		try:
			with open(log_file, 'w+') as f:
				json.dump(beispieldaten_dateipfad, f,ensure_ascii=False)
		except FileNotFoundError:
			os.makedirs(os.path.join(os.path.dirname('__file__'),'Teildokument'))
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
			subprocess.Popen('cd "Teildokument" ; latex --synctex=-1 Teildokument_{0}.tex ; dvips Teildokument_{0}.dvi ; ps2pdf -dNOSAFER Teildokument_{0}.ps'.format(chosen_aufgabenformat),shell=True).wait()
			subprocess.run(['xdg-open', "Teildokument/Teildokument_%s.pdf"%chosen_aufgabenformat])
		elif sys.platform.startswith('darwin'):
			subprocess.Popen('cd "Teildokument" ; latex --synctex=-1 Teildokument_{0}.tex ; dvips Teildokument_{0}.dvi ; ps2pdf -dNOSAFER Teildokument_{0}.ps'.format(chosen_aufgabenformat),shell=True).wait()
			subprocess.run(['xdg-open', '"Teildokument/Teildokument_%s.pdf"'%chosen_aufgabenformat])
		else:
			subprocess.Popen('cd "Teildokument" & latex --synctex=-1 Teildokument_{0}.tex& dvips Teildokument_{0}.dvi & ps2pdf -dNOSAFER Teildokument_{0}.ps'.format(chosen_aufgabenformat),shell=True).wait()
			subprocess.Popen('cd "Teildokument" & Teildokument_{0}.pdf'.format(chosen_aufgabenformat), shell=True).poll()
		## -interaction=nonstopmode -halt-on-error Don't stop when error occurs, while compiling
		os.unlink('Teildokument/Teildokument_%s.aux'%chosen_aufgabenformat)
		os.unlink('Teildokument/Teildokument_%s.log'%chosen_aufgabenformat)
		os.unlink('Teildokument/Teildokument_%s.dvi'%chosen_aufgabenformat)
		os.unlink('Teildokument/Teildokument_%s.ps'%chosen_aufgabenformat)
	
	def PrepareTeXforPDF(self):
		chosen_aufgabenformat='Typ%sAufgaben'%self.label_aufgabentyp.text()[-1]

		QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
		
		if not os.path.isfile(os.path.join('Teildokument','log_file_%s'%self.label_aufgabentyp.text()[-1])):
			self.refresh_ddb()
		else: ##  Automatic update once per month
			log_file=os.path.join(os.path.dirname('__file__'),'Teildokument','log_file_%s'%self.label_aufgabentyp.text()[-1])
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
		# log_file=os.path.join(os.path.dirname('__file__'),'Typ 2 Aufgaben','Teildokument','log_file')
		######

		log_file=os.path.join(os.path.dirname('__file__'),'Teildokument','log_file_%s'%self.label_aufgabentyp.text()[-1])

		with open(log_file) as f:
			beispieldaten_dateipfad = json.load(f)
			#beispieldaten_dateipfad=eval(beispieldaten_dateipfad)
			beispieldaten=list(beispieldaten_dateipfad.keys())					  
		

		#### typ1 ###
		# filename_teildokument = os.path.join(os.path.dirname('__file__'),'Typ 2 Aufgaben','Teildokument','Teildokument.tex')
		#####

		filename_teildokument = os.path.join(os.path.dirname('__file__'),'Teildokument','Teildokument_%s.tex'%self.label_aufgabentyp.text()[-1])
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
	# 	if self.menu_searchtype.currentText()=='Alle Dateien ausgeben, die alle Suchkriterien enthalten':
		#######
		if self.menu_searchtype.currentText()=='Alle Dateien ausgeben, die ausschließlich diese Suchkriterien enthalten' and chosen_aufgabenformat=='Typ2Aufgaben':
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

					
		if self.menu_searchtype.currentText()=='Alle Dateien ausgeben, die zumindest ein Suchkriterium enthalten' or chosen_aufgabenformat=='Typ1Aufgaben':
			gesammeltedateien=[]
			for all in suchbegriffe:
				for element in list(beispieldaten_dateipfad.keys())[:]:
					if all in element:
						gesammeltedateien.append(element)
			

		if not len(self.entry_suchbegriffe.text()) ==0:
			suchbegriffe.append(self.entry_suchbegriffe.text())
			if self.menu_searchtype.currentText()=='Alle Dateien ausgeben, die zumindest ein Suchkriterium enthalten' or chosen_aufgabenformat=='Typ1Aufgaben':
				if len(gesammeltedateien)==0 and len(suchbegriffe)!=0:
					gesammeltedateien=list(beispieldaten_dateipfad.keys())				
			for all in gesammeltedateien[:]:			
				if self.entry_suchbegriffe.text().lower() not in all.lower():
						gesammeltedateien.remove(all)
		

		if not len(self.entry_suchbegriffe.text())==0:
			suchbegriffe.append(self.entry_suchbegriffe.text())

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
				for all_formats in set_af:
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
			#msg.setWindowIcon(QtWidgets.QIcon(r'C:\Users\Christoph\Desktop\lupe.png'))
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
				file.write('\input{".'+value+'"}%\n'
				'\hrule  \leer\n\n')
			elif chosen_aufgabenformat=='Typ2Aufgaben':
				file.write('\input{".'+value+'"}%\n'
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
		#msg.setWindowIcon(QtWidgets.QIcon(r'C:\Users\Christoph\Desktop\lupe.png'))
		msg.setText('Insgesamt wurden '+ str(len(dict_gesammeltedateien)) + ' Beispiel gefunden.\n ')
		msg.setInformativeText('Soll die PDF Datei erstellt werden?')
		msg.setWindowTitle("Datei ausgeben?")
		msg.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
		buttonY = msg.button(QtWidgets.QMessageBox.Yes)
		buttonY.setText('Ja')
		buttonN = msg.button(QtWidgets.QMessageBox.No)
		buttonN.setText('Nein')
		ret=msg.exec_()
		
		if ret==QtWidgets.QMessageBox.Yes:
			MainWindow.close()
			self.create_pdf()
			sys.exit(0)
		
		
		
		
		##################################################
		################################################
		###### Windows Loading Bar ######################
		###############################################

		# LoadingWindow = QtWidgets.QDialog()
		# ui = Ui_Dialog()
		# ui.setupUi(LoadingWindow)
		# LoadingWindow.exec()
		

	
if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	MainWindow = QMainWindow()

	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)

	MainWindow.show()
	sys.exit(app.exec_())


