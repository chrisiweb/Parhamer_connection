#!/usr/bin/python3
# -*- coding: utf-8 -*-
#### Version number ###
__version__='v1.0'
####################

from PyQt5 import QtCore, QtWidgets, QtWidgets  ### pyqt5
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
import yaml ##pyyaml
from PIL import Image ## pillow


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

dict_picture_path={}
set_chosen_gk=set([])
class Ui_MainWindow(object):
	global dict_picture_path, set_chosen_gk
	def setupUi(self, MainWindow):
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.setMaximumSize(QtCore.QSize(1078, 16777215))
		MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
		MainWindow.setStyleSheet(_fromUtf8(""))
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
		self.groupBox_grundkompetenzen = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_grundkompetenzen.setMaximumSize(QtCore.QSize(350, 16777215))
		self.groupBox_grundkompetenzen.setObjectName(_fromUtf8("groupBox_grundkompetenzen"))
		self.gridLayout_11 = QtWidgets.QGridLayout(self.groupBox_grundkompetenzen)
		self.gridLayout_11.setObjectName(_fromUtf8("gridLayout_11"))
		self.tab_widget_gk = QtWidgets.QTabWidget(self.groupBox_grundkompetenzen)
		self.tab_widget_gk.setStyleSheet(_fromUtf8("background-color: rgb(217, 255, 215);"))
		self.tab_widget_gk.setObjectName(_fromUtf8("tab_widget_gk"))
		self.gridLayout_11.addWidget(self.tab_widget_gk, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.groupBox_grundkompetenzen, 1, 0, 5, 1)
		self.groupBox_punkte = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_punkte.setObjectName(_fromUtf8("groupBox_punkte"))
		self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_punkte)
		self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
		self.spinBox_punkte = QtWidgets.QSpinBox(self.groupBox_punkte)
		self.spinBox_punkte.setProperty("value", 1)
		self.spinBox_punkte.setObjectName(_fromUtf8("spinBox_punkte"))
		self.gridLayout_6.addWidget(self.spinBox_punkte, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.groupBox_punkte, 1, 3, 1, 1)
		self.groupBox_klassen = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_klassen.setObjectName(_fromUtf8("groupBox_klassen"))
		self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox_klassen)
		self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
		self.comboBox_klassen = QtWidgets.QComboBox(self.groupBox_klassen)
		self.comboBox_klassen.setObjectName(_fromUtf8("comboBox_klassen"))
		self.comboBox_klassen.addItem(_fromUtf8(""))
		self.comboBox_klassen.addItem(_fromUtf8(""))
		self.comboBox_klassen.addItem(_fromUtf8(""))
		self.comboBox_klassen.addItem(_fromUtf8(""))
		self.comboBox_klassen.addItem(_fromUtf8(""))
		self.comboBox_klassen.addItem(_fromUtf8(""))
		self.gridLayout_8.addWidget(self.comboBox_klassen, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.groupBox_klassen, 1, 5, 1, 1)
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
		self.label_keine_auswahl = QtWidgets.QLabel(self.groupBox_aufgabenformat)
		self.label_keine_auswahl.setObjectName(_fromUtf8("label_keine_auswahl"))
		self.label_keine_auswahl.setMinimumSize(QtCore.QSize(139,0))
		self.gridLayout_7.addWidget(self.label_keine_auswahl)
		self.label_keine_auswahl.hide()
		self.groupBox_aufgabentyp = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_aufgabentyp.setObjectName(_fromUtf8("groupBox_aufgabentyp"))
		self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_aufgabentyp)
		self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
		self.comboBox_aufgabentyp = QtWidgets.QComboBox(self.groupBox_aufgabentyp)
		self.comboBox_aufgabentyp.setObjectName(_fromUtf8("comboBox_aufgabentyp"))
		self.comboBox_aufgabentyp.addItem(_fromUtf8(""))
		self.comboBox_aufgabentyp.addItem(_fromUtf8(""))
		self.gridLayout_3.addWidget(self.comboBox_aufgabentyp, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.groupBox_aufgabentyp, 1, 2, 1, 1)
		self.groupBox_ausgew_gk = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_ausgew_gk.setMinimumSize(QtCore.QSize(350, 0))
		self.groupBox_ausgew_gk.setObjectName(_fromUtf8("groupBox_ausgew_gk"))
		self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_ausgew_gk)
		self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
		self.label_ausgew_gk = QtWidgets.QLabel(self.groupBox_ausgew_gk)
		self.label_ausgew_gk.setWordWrap(True)
		self.label_ausgew_gk.setObjectName(_fromUtf8("label_ausgew_gk"))
		self.verticalLayout_2.addWidget(self.label_ausgew_gk)
		self.gridLayout.addWidget(self.groupBox_ausgew_gk, 6, 0, 1, 1)
		self.groupBox_bilder = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_bilder.setMaximumSize(QtCore.QSize(350, 16777215))
		self.groupBox_bilder.setObjectName(_fromUtf8("groupBox_bilder"))
		self.gridLayout_13 = QtWidgets.QGridLayout(self.groupBox_bilder)
		self.gridLayout_13.setObjectName(_fromUtf8("gridLayout_13"))
		self.scrollArea = QtWidgets.QScrollArea(self.groupBox_bilder)
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
		self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.scrollAreaWidgetContents_bilder = QtWidgets.QWidget()
		self.scrollAreaWidgetContents_bilder.setGeometry(QtCore.QRect(0, 0, 320, 67))
		self.scrollAreaWidgetContents_bilder.setObjectName(_fromUtf8("scrollAreaWidgetContents_bilder"))
		self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_bilder)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.scrollArea.setWidget(self.scrollAreaWidgetContents_bilder)
		self.gridLayout_13.addWidget(self.scrollArea, 1, 0, 1, 1)

		self.label_bild_leer= QtWidgets.QLabel(self.scrollAreaWidgetContents_bilder)
		self.label_bild_leer.setObjectName(_fromUtf8("label_bild_leer"))
		self.verticalLayout.addWidget(self.label_bild_leer)
		self.label_bild_leer.setText(_translate("MainWindow", "-", None))
		# self.gridLayout_13.addWidget(self.label_bild_0, 0, 0, 1, 1)		
		# for i in range(5):
		# 	x=eval('self.label_bild_'+str(i))
		# 	x.setObjectName(_fromUtf8("label_bild_%s"%i))
		# 	x.mousePressEvent = self.del_picture
		# 	self.gridLayout_13.addWidget(x, 0, i, 1, 1)
		# 	x.setText(_translate("MainWindow", str(i), None))

		
		self.gridLayout.addWidget(self.groupBox_bilder, 7, 0, 1, 1)
		self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
		self.gridLayout_14 = QtWidgets.QGridLayout(self.groupBox_2)
		self.gridLayout_14.setObjectName(_fromUtf8("gridLayout_14"))
		self.lineEdit_titel = QtWidgets.QLineEdit(self.groupBox_2)
		self.lineEdit_titel.setObjectName(_fromUtf8("lineEdit_titel"))
		self.gridLayout_14.addWidget(self.lineEdit_titel, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.groupBox_2, 2, 2, 1, 4)
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
		self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox.setObjectName(_fromUtf8("groupBox"))
		self.gridLayout_18 = QtWidgets.QGridLayout(self.groupBox)
		self.gridLayout_18.setObjectName(_fromUtf8("gridLayout_18"))
		self.lineEdit_quelle = QtWidgets.QLineEdit(self.groupBox)
		self.lineEdit_quelle.setObjectName(_fromUtf8("lineEdit_quelle"))
		self.gridLayout_18.addWidget(self.lineEdit_quelle, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.groupBox, 7, 2, 1, 4)
		self.pushButton_save = QtWidgets.QPushButton(self.centralwidget)
		self.pushButton_save.setObjectName(_fromUtf8("pushButton_save"))
		self.gridLayout.addWidget(self.pushButton_save, 8, 5, 1, 1)
		MainWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)
		self.menuBar = QtWidgets.QMenuBar(MainWindow)
		self.menuBar.setGeometry(QtCore.QRect(0, 0, 782, 21))
		self.menuBar.setObjectName(_fromUtf8("menuBar"))
		self.menuDatei = QtWidgets.QMenu(self.menuBar)
		self.menuDatei.setObjectName(_fromUtf8("menuDatei"))
		self.menuHelp = QtWidgets.QMenu(self.menuBar)
		self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
		self.menuBild_einf_gen = QtWidgets.QMenu(self.menuBar)
		self.menuBild_einf_gen.setObjectName(_fromUtf8("menuBild_einf_gen"))
		MainWindow.setMenuBar(self.menuBar)
		self.actionNew = QtWidgets.QAction(MainWindow)
		self.actionNew.setObjectName(_fromUtf8("actionNew"))
		# self.actionAufgaben_Typ1 = QtWidgets.QAction(MainWindow)
		# self.actionAufgaben_Typ1.setObjectName(_fromUtf8("actionAufgaben_Typ1"))
		# self.actionTyp_2_Aufgaben = QtWidgets.QAction(MainWindow)
		# self.actionTyp_2_Aufgaben.setObjectName(_fromUtf8("actionTyp_2_Aufgaben"))
		self.actionsuchfenster_reset = QtWidgets.QAction(MainWindow)
		self.actionsuchfenster_reset.setObjectName(_fromUtf8("actionsuchfenster_reset"))
		self.actionExit = QtWidgets.QAction(MainWindow)
		self.actionExit.setObjectName(_fromUtf8("actionExit"))
		self.actionRefresh_Database = QtWidgets.QAction(MainWindow)
		self.actionRefresh_Database.setObjectName(_fromUtf8("actionRefresh_Database"))
		self.actionBild_einf_gen = QtWidgets.QAction(MainWindow)
		self.actionBild_einf_gen.setObjectName(_fromUtf8("actionBild_einf_gen"))
		self.actionBild_konvertieren_jpg_eps = QtWidgets.QAction(MainWindow)
		self.actionBild_konvertieren_jpg_eps.setObjectName(_fromUtf8("actionBild_konvertieren_jpg_eps"))
		self.actionInfo = QtWidgets.QAction(MainWindow)
		self.actionInfo.setObjectName(_fromUtf8("actionInfo"))
		self.menuDatei.addAction(self.actionsuchfenster_reset)
		self.menuDatei.addSeparator()
		self.menuDatei.addAction(self.actionExit)
		self.menuBild_einf_gen.addAction(self.actionBild_einf_gen)
		self.menuBild_einf_gen.addSeparator()
		self.menuBild_einf_gen.addAction(self.actionBild_konvertieren_jpg_eps)
		self.menuHelp.addAction(self.actionInfo)
		self.menuBar.addAction(self.menuDatei.menuAction())
		self.menuBar.addAction(self.menuBild_einf_gen.menuAction())
		self.menuBar.addAction(self.menuHelp.menuAction())
		#### CREATE CHECKBOXES ####
		##### AG #####
		self.tab_ag = QtWidgets.QWidget()
		self.tab_ag.setObjectName(_fromUtf8("tab_ag"))
		self.gridLayout_ag = QtWidgets.QGridLayout(self.tab_ag)
		self.gridLayout_ag.setObjectName(_fromUtf8("gridLayout_ag"))
		self.tab_widget_gk.addTab(self.tab_ag, _fromUtf8(""))
		self.create_checkbox_gk('ag', ag_beschreibung)

		#### FA ####
		self.tab_fa = QtWidgets.QWidget()
		self.tab_fa.setObjectName(_fromUtf8("tab_fa"))
		self.gridLayout_fa = QtWidgets.QGridLayout(self.tab_fa)
		self.gridLayout_fa.setObjectName(_fromUtf8("gridLayout_fa"))
		self.tab_widget_gk.addTab(self.tab_fa, _fromUtf8(""))
		self.create_checkbox_gk('fa', fa_beschreibung)

		##### AN ####
		self.tab_an = QtWidgets.QWidget()
		self.tab_an.setObjectName(_fromUtf8("tab_an"))
		self.gridLayout_an = QtWidgets.QGridLayout(self.tab_an)
		self.gridLayout_an.setObjectName(_fromUtf8("gridLayout_an"))
		self.tab_widget_gk.addTab(self.tab_an, _fromUtf8(""))
		self.create_checkbox_gk('an', an_beschreibung)

		### WS ####
		self.tab_ws = QtWidgets.QWidget()
		self.tab_ws.setObjectName(_fromUtf8("tab_ws"))
		self.gridLayout_ws = QtWidgets.QGridLayout(self.tab_ws)
		self.gridLayout_ws.setObjectName(_fromUtf8("gridLayout_ws"))
		self.tab_widget_gk.addTab(self.tab_ws, _fromUtf8(""))
		self.create_checkbox_gk('ws', ws_beschreibung)

		### 5. Klasse ###
		self.tab_k5 = QtWidgets.QWidget()
		self.tab_k5.setObjectName(_fromUtf8("tab_k5"))
		self.gridLayout_k5 = QtWidgets.QGridLayout(self.tab_k5)
		self.gridLayout_k5.setObjectName(_fromUtf8("gridLayout_k5"))
		self.tab_widget_gk.addTab(self.tab_k5, _fromUtf8(""))
		self.create_checkbox_klasse('k5',k5_beschreibung)

		### 6. Klasse ###
		self.tab_k6 = QtWidgets.QWidget()
		self.tab_k6.setObjectName(_fromUtf8("tab_k6"))
		self.gridLayout_k6 = QtWidgets.QGridLayout(self.tab_k6)
		self.gridLayout_k6.setObjectName(_fromUtf8("gridLayout_k6"))
		self.tab_widget_gk.addTab(self.tab_k6, _fromUtf8(""))
		self.create_checkbox_klasse('k6',k6_beschreibung)

		### 7. Klasse ###
		self.tab_k7 = QtWidgets.QWidget()
		self.tab_k7.setObjectName(_fromUtf8("tab_k7"))
		self.gridLayout_k7 = QtWidgets.QGridLayout(self.tab_k7)
		self.gridLayout_k7.setObjectName(_fromUtf8("gridLayout_k7"))
		self.tab_widget_gk.addTab(self.tab_k7, _fromUtf8(""))
		self.create_checkbox_klasse('k7',k7_beschreibung)

		### 8. Klasse ###
		self.tab_k8 = QtWidgets.QWidget()
		self.tab_k8.setObjectName(_fromUtf8("tab_k8"))
		self.gridLayout_k8 = QtWidgets.QGridLayout(self.tab_k8)
		self.gridLayout_k8.setObjectName(_fromUtf8("gridLayout_k8"))
		self.tab_widget_gk.addTab(self.tab_k8, _fromUtf8(""))
		self.create_checkbox_klasse('k8',k8_beschreibung)

		self.retranslateUi(MainWindow)
		self.tab_widget_gk.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		MainWindow.setTabOrder(self.comboBox_aufgabentyp, self.spinBox_punkte)
		MainWindow.setTabOrder(self.spinBox_punkte, self.comboBox_af)
		MainWindow.setTabOrder(self.comboBox_af, self.comboBox_klassen)
		MainWindow.setTabOrder(self.comboBox_klassen, self.lineEdit_titel)
		MainWindow.setTabOrder(self.lineEdit_titel, self.plainTextEdit)
		MainWindow.setTabOrder(self.plainTextEdit, self.lineEdit_quelle)
		MainWindow.setTabOrder(self.lineEdit_quelle, self.pushButton_save)
	
		
		for all in {**ag_beschreibung,**fa_beschreibung,**an_beschreibung,**ws_beschreibung}:
			x=eval('self.cb_'+all)
			x.stateChanged.connect(lambda: self.gk_checked('gk'))

		for g in range(5,9):
			for all in eval('k%s_beschreibung'%g):
				x=eval('self.cb_k%s_'%g+all)
				x.stateChanged.connect(lambda: self.gk_checked('klasse'))

		self.actionExit.triggered.connect(self.close_app)	
		self.actionsuchfenster_reset.triggered.connect(self.suchfenster_reset)
		self.actionBild_konvertieren_jpg_eps.triggered.connect(self.convert_jpgtoeps)
		self.actionBild_einf_gen.triggered.connect(self.add_picture)
		self.actionInfo.triggered.connect(self.show_info)
		self.comboBox_aufgabentyp.currentIndexChanged.connect(self.chosen_aufgabenformat)
		self.pushButton_save.clicked.connect(self.save_file)
		

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("LaTeX File Creator", "LaTeX File Creator", None))
		self.groupBox_grundkompetenzen.setTitle(_translate("MainWindow", "Grundkompetenzen", None))
		self.tab_widget_gk.setTabText(self.tab_widget_gk.indexOf(self.tab_ag), _translate("MainWindow", "Algebra und Geometrie", None))
		self.tab_widget_gk.setTabText(self.tab_widget_gk.indexOf(self.tab_fa), _translate("MainWindow", "Funktionale Abhängigkeiten", None))
		self.tab_widget_gk.setTabText(self.tab_widget_gk.indexOf(self.tab_an), _translate("MainWindow", "Analysis", None))
		self.tab_widget_gk.setTabText(self.tab_widget_gk.indexOf(self.tab_ws), _translate("MainWindow", "Wahrscheinlichkeit und Statistik", None))
		self.name_checkbox_gk(ag_beschreibung)
		self.name_checkbox_gk(fa_beschreibung)
		self.name_checkbox_gk(an_beschreibung)
		self.name_checkbox_gk(ws_beschreibung)

		self.cb_k5_fu.setText(_translate("MainWindow", "Funktionen (FU)", None))
		self.cb_k5_mzr.setText(_translate("MainWindow", "Mengen, Zahlen, Rechengesetze (MZR)", None))
		self.cb_k5_tr.setText(_translate("MainWindow", "Trigonometrie (TR)", None))
		self.cb_k5_vag2.setText(_translate("MainWindow", "Vektoren und analytische Geometrie (VAG2)", None))
		self.cb_k5_gl.setText(_translate("MainWindow", "Gleichungen und Gleichungssysteme (GL)", None))
		self.tab_widget_gk.setTabText(self.tab_widget_gk.indexOf(self.tab_k5), _translate("MainWindow", "5. Klasse", None))
		self.cb_k6_vag3.setText(_translate("MainWindow", "Vektoren und analytische Geometrie\n"
"in R3 und Rn (VAG3)", None))
		self.cb_k6_bsw.setText(_translate("MainWindow", "Beschreibende Statistik und Wahrscheinlichkeit (BSW)", None))
		self.cb_k6_pwlu.setText(_translate("MainWindow", "Potenzen, Wurzeln, Logarithmen\n"
"und Ungleichungen (PWLU)", None))
		self.cb_k6_rf.setText(_translate("MainWindow", "Reelle Funktionen (RF)", None))
		self.cb_k6_fo.setText(_translate("MainWindow", "Folgen (FO)", None))
		self.cb_k6_re.setText(_translate("MainWindow", "Reihen (RE)", None))
		self.tab_widget_gk.setTabText(self.tab_widget_gk.indexOf(self.tab_k6), _translate("MainWindow", "6. Klasse", None))
		self.cb_k7_dr.setText(_translate("MainWindow", "Differentialrechnung (DR)", None))
		self.cb_k7_kkk.setText(_translate("MainWindow", "Kreise, Kugeln, Kegelschnittslinien\n"
"und andere Kurven (KKK)", None))
		self.cb_k7_dwv.setText(_translate("MainWindow", "Diskrete Wahrscheinlichkeitsverteilungen (DWV)", None))
		self.cb_k7_ghg.setText(_translate("MainWindow", "Gleichungen höheren Grades als 2 (GHG)", None))
		self.cb_k7_wm.setText(_translate("MainWindow", "Wirtschaftsmathematik (WM)", None))
		self.cb_k7_kz.setText(_translate("MainWindow", "Komplexe Zahlen (KZ)", None))
		self.tab_widget_gk.setTabText(self.tab_widget_gk.indexOf(self.tab_k7), _translate("MainWindow", "7. Klasse", None))
		self.cb_k8_ddg.setText(_translate("MainWindow", "Differenzen- und Differentialgleichungen\n"
"Grundlagen der Systemdynamik (DDG)", None))
		self.cb_k8_sws.setText(_translate("MainWindow", "Stetgie Wahrscheinlichkeitsverteilungen\n"
"Beurteilende Statistik (SWS)", None))
		self.cb_k8_ir.setText(_translate("MainWindow", "Integralrechnung (IR)", None))
		self.cb_k8_wm.setText(_translate("MainWindow", "Wirtschaftsmathematik (WM)", None))
		self.tab_widget_gk.setTabText(self.tab_widget_gk.indexOf(self.tab_k8), _translate("MainWindow", "8. Klasse", None))
		self.groupBox_punkte.setTitle(_translate("MainWindow", "Punkte", None))
		self.groupBox_klassen.setTitle(_translate("MainWindow", "Klasse", None))
		self.comboBox_klassen.setItemText(0, _translate("MainWindow", "-", None))
		self.comboBox_klassen.setItemText(1, _translate("MainWindow", "5. Klasse", None))
		self.comboBox_klassen.setItemText(2, _translate("MainWindow", "6. Klasse", None))
		self.comboBox_klassen.setItemText(3, _translate("MainWindow", "7. Klasse", None))
		self.comboBox_klassen.setItemText(4, _translate("MainWindow", "8. Klasse", None))
		self.comboBox_klassen.setItemText(5, _translate("MainWindow", "Matura", None))
		self.groupBox_aufgabenformat.setTitle(_translate("MainWindow", "Aufgabenformat", None))
		self.comboBox_af.setItemText(0, _translate("MainWindow", "bitte auswählen", None))
		i=1
		for all in dict_aufgabenformate:
			self.comboBox_af.setItemText(i, _translate("MainWindow", dict_aufgabenformate[all], None))
			i+=1
		# self.comboBox_af.setItemText(2, _translate("MainWindow", "Multiple Choice", None))
		# self.comboBox_af.setItemText(3, _translate("MainWindow", "Offenes Antwortformat", None))
		# self.comboBox_af.setItemText(4, _translate("MainWindow", "Zuordnungsformat", None))
		self.groupBox_aufgabentyp.setTitle(_translate("MainWindow", "Aufgabentyp", None))
		self.comboBox_aufgabentyp.setItemText(0, _translate("MainWindow", "Typ 1", None))
		self.comboBox_aufgabentyp.setItemText(1, _translate("MainWindow", "Typ 2", None))
		self.label_keine_auswahl.setText(_translate("MainWindow", "keine Auswahl nötig", None))
		self.groupBox_ausgew_gk.setTitle(_translate("MainWindow", "Ausgewählte Grundkompetenzen", None))
		self.label_ausgew_gk.setText(_translate("MainWindow", "-", None))
		self.groupBox_bilder.setTitle(_translate("MainWindow", "Bilder (klicken, um Bilder zu entfernen)", None))
		self.groupBox_2.setTitle(_translate("MainWindow", "Titel", None))
		self.groupBox_beispieleingabe.setTitle(_translate("MainWindow", "Beispieleingabe", None))
		self.label.setText(_translate("MainWindow", "Info: Eingabe des Aufgabentextes zwischen \\begin{beispiel} ... \\end{beispiel}", None))
		self.groupBox.setTitle(_translate("MainWindow", "Quelle oder Autor (Vorname Nachname) - Eingabe: VorNac", None))
		self.pushButton_save.setText(_translate("MainWindow", "Speichern", None))
		self.pushButton_save.setShortcut(_translate("MainWindow", "Return", None))
		self.menuDatei.setTitle(_translate("MainWindow", "Datei", None))
		self.menuBild_einf_gen.setTitle(_translate("MainWindow", "Bild einfügen", None))
		self.actionNew.setText(_translate("MainWindow", "Reset", None))
		# self.actionAufgaben_Typ1.setText(_translate("MainWindow", "Typ 1 Aufgaben", None))
		# self.actionTyp_2_Aufgaben.setText(_translate("MainWindow", "Typ 2 Aufgaben", None))
		self.actionInfo.setText(_translate("MainWindow", "Info", None))
		self.actionsuchfenster_reset.setText(_translate("MainWindow", "Reset", None))
		self.actionsuchfenster_reset.setShortcut("F4")
		self.actionExit.setText(_translate("MainWindow", "Exit", None))
		self.actionRefresh_Database.setText(_translate("MainWindow", "Refresh Database", None))
		self.actionBild_einf_gen.setText(_translate("MainWindow", "Durchsuchen...", None))
		self.actionBild_konvertieren_jpg_eps.setText(_translate("MainWindow", "Bild konvertieren (jpg zu eps)", None))
		self.menuHelp.setTitle(_translate("MainWindow", "?", None))

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


	def create_checkbox_gk(self,gk_type,chosen_dict):
		row=0
		column=0
		max_row=8
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


	def name_checkbox_gk(self, chosen_dict):
		for all in chosen_dict:
			x=eval('self.cb_'+all)
			x.setText(_translate("MainWindow", dict_gk[all], None))

	
	def gk_checked(self, thema):
		global set_chosen_gk
		set_chosen_gk=set([])
		set_chosen_gk_label=set([])
		for all in {**ag_beschreibung,**fa_beschreibung,**an_beschreibung,**ws_beschreibung}: ## merged dictionionaries
			x=eval('self.cb_'+all)
			if x.isChecked()==True:
				set_chosen_gk.add(all)
				set_chosen_gk_label.add(x.text())
		for all in k5_beschreibung:
			x=eval('self.cb_k5_'+all)
			if x.isChecked()==True:
				set_chosen_gk.add(all)
				set_chosen_gk_label.add(all.upper()+'(5)')
		for all in k6_beschreibung:
			x=eval('self.cb_k6_'+all)
			if x.isChecked()==True:
				set_chosen_gk.add(all)
				set_chosen_gk_label.add(all.upper() + '(6)')
		for all in k7_beschreibung:
			x=eval('self.cb_k7_'+all)
			if x.isChecked()==True:
				set_chosen_gk.add(all)
				set_chosen_gk_label.add(all.upper() + '(7)')
		for all in k8_beschreibung:
			x=eval('self.cb_k8_'+all)
			if x.isChecked()==True:
				set_chosen_gk.add(all)
				set_chosen_gk_label.add(all.upper() + '(8)')		

		x= ', '.join(sorted(set_chosen_gk_label))
		self.label_ausgew_gk.setText(_translate("MainWindow", str(x), None))
		print(set_chosen_gk)
		print(set_chosen_gk_label)

	def chosen_aufgabenformat(self):
		if self.comboBox_aufgabentyp.currentText()=='Typ 1':
			self.label_keine_auswahl.hide()
			self.comboBox_af.show()
		if self.comboBox_aufgabentyp.currentText()=='Typ 2':
			self.label_keine_auswahl.show()
			self.comboBox_af.hide()
			
	def show_info(self):
		QtWidgets.QApplication.restoreOverrideCursor()
		msg = QtWidgets.QMessageBox()
		msg.setIcon(QtWidgets.QMessageBox.Information)
		#msg.setWindowIcon(QtWidgets.QIcon(r'C:\Users\Christoph\Desktop\lupe.png'))
		msg.setText("LaTeX File Creator %s\n\nAuthor: Christoph Weberndorfer\nLicense: GNU General Public License v3.0"%__version__)
		msg.setInformativeText("Last Update: 03/19")
		msg.setWindowTitle("Über LaTeX File Creator")
		#msg.setDetailedText("The details are as follows:")
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		retval = msg.exec_()


	def close_app(self):
		sys.exit(0)

	
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

	def suchfenster_reset(self):
		global dict_picture_path
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
		self.spinBox_punkte.setProperty("value", 1)
		self.comboBox_aufgabentyp.setCurrentIndex(0)
		self.comboBox_af.setCurrentIndex(0)
		self.comboBox_klassen.setCurrentIndex(0)
		self.label_ausgew_gk.setText(_translate("MainWindow", "-", None))
		self.label_bild_leer.show()

		for i in range(len(dict_picture_path)):
			x=eval('self.label_bild_'+str(i))
			x.hide()
		dict_picture_path={}			
	
		self.lineEdit_titel.setText(_translate("MainWindow", "", None))
		self.lineEdit_quelle.setText(_translate("MainWindow", "", None))
		self.plainTextEdit.setPlainText(_translate("MainWindow", "", None))

	def convert_jpgtoeps(self):
		msg = QtWidgets.QMessageBox()
		# msg.setIcon(QtWidgets.QMessageBox.Question)
		#msg.setWindowIcon(QtWidgets.QIcon(r'C:\Users\Christoph\Desktop\lupe.png'))
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
			if len(filename)>0:
				for all in filename:
					output=all.replace('jpg','eps')
					img=Image.open(all)
					img.save(output)

				msg = QtWidgets.QMessageBox()
				msg.setIcon(QtWidgets.QMessageBox.Information)
				if len(filename)==1:
					msg.setText('Es wurde '+str(len(filename))+' Datei erfolgreich konvertiert.')
				else:
					msg.setText('Es wurden '+str(len(filename))+' Dateien erfolgreich konvertiert.')	

				msg.setWindowTitle("jpg2eps")
				msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
				ret=msg.exec_()	
				return

	def warning_window(self, text):
		QtWidgets.QApplication.restoreOverrideCursor()
		msg = QtWidgets.QMessageBox()
		msg.setWindowTitle("Warnung")
		msg.setIcon(QtWidgets.QMessageBox.Warning)
		#msg.setWindowIcon(QtWidgets.QIcon(r'C:\Users\Christoph\Desktop\lupe.png'))
		msg.setText(text)
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		retval = msg.exec_()


	def save_file(self):
		########################### WARNINGS ##### 
		######################################

		if set_chosen_gk==set([]):
			self.warning_window('Es wurden keine Grundkompetenzen zugewiesen.')
			return
		


		if self.comboBox_aufgabentyp.currentText()=='Typ 1':
			if self.comboBox_af.currentText()=='bitte auswählen':
				self.warning_window('Es wurde kein Aufgabenformat ausgewählt.')
				return

			if len(set_chosen_gk)>1:
				self.warning_window('Es wurden zu viele Grundkompetenzen zugewiesen.')
				return

		textBox_Entry=self.plainTextEdit.toPlainText()
		list_chosen_gk=list(set_chosen_gk)			
		###############################	


		QtWidgets.QApplication.restoreOverrideCursor()
		msg = QtWidgets.QMessageBox()
		msg.setIcon(QtWidgets.QMessageBox.Question)
		msg.setWindowTitle("Aufgabe speichern?")
		#msg.setWindowIcon(QtWidgets.QIcon(r'C:\Users\Christoph\Desktop\lupe.png'))

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

		if self.comboBox_aufgabentyp.currentText()=='Typ 1':
			aufgabenformat='Aufgabenformat: %s\n'%self.comboBox_af.currentText()
		else:
			aufgabenformat=''
		msg.setText(
		'Sind Sie sicher, dass Sie die folgenden Aufgabe speichern wollen?\n\n'
		'Aufgabentyp: {0}\n'
		'Titel: {1}\n{2}'
		'Grundkompetenz: {3}\n'
		'Quelle: {4}\n'
		'Bilder: {5}'.format(self.comboBox_aufgabentyp.currentText(),
		self.lineEdit_titel.text(),aufgabenformat,gk,self.lineEdit_quelle.text(),bilder))
		# msg.setInformativeText('Soll die PDF Datei erstellt werden?')
		msg.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
		buttonY = msg.button(QtWidgets.QMessageBox.Yes)
		buttonY.setText('Speichern')
		buttonN = msg.button(QtWidgets.QMessageBox.No)
		buttonN.setText('Abbrechen')
		ret=msg.exec_()
		
		if ret==QtWidgets.QMessageBox.Yes:
			pass
		else:
			return		

		####### CHECK INCL. & ATTACHED IMAGE RATIO ####

		if textBox_Entry.count('\includegraphics')>len(dict_picture_path):
			self.warning_window('Es sind zu wenige Bilder angehängt (' + str(len(dict_picture_path))+'/'+str(textBox_Entry.count('\includegraphics'))+').')
			return
		if textBox_Entry.count('\includegraphics')<len(dict_picture_path):
			self.warning_window('Es sind zu viele Bilder angehängt (' + str(len(dict_picture_path))+'/'+str(textBox_Entry.count('\includegraphics'))+').')
			return



		##### GET MAX FILENUMBER IN DIR #####
		if self.comboBox_aufgabentyp.currentText()=='Typ 1':
			print(set_chosen_gk)
			if list_chosen_gk[0] in {**k5_beschreibung,**k6_beschreibung,**k7_beschreibung,**k8_beschreibung}: ## merged dictionaries
				if list_chosen_gk[0] in k5_beschreibung:
					path_folder='5.Klasse'
				elif list_chosen_gk[0] in k6_beschreibung:
					path_folder='6.Klasse'
				elif list_chosen_gk[0] in k7_beschreibung:
					path_folder='7.Klasse'
				elif list_chosen_gk[0] in k8_beschreibung:
					path_folder='8.Klasse'
				gk_path_temp=os.path.join(os.path.dirname('__file__'),'_database','Typ1Aufgaben',path_folder,list_chosen_gk[0],'Einzelbeispiele')
				z=list_chosen_gk[0].upper()+' - '
			else:
				path_folder='_Grundkompetenzen'
				gk_path_temp=os.path.join(os.path.dirname('__file__'),'_database','Typ1Aufgaben',path_folder,dict_gk[list_chosen_gk[0]][:2],dict_gk[list_chosen_gk[0]],'Einzelbeispiele')
				z=dict_gk[list_chosen_gk[0]]+' - '
	
				
			max_integer_file=0
			for all in os.listdir(gk_path_temp):
				if all.endswith('.tex'):
					x,y=all.split(z)
					file_integer, file_extension=y.split('.tex')
					if int(file_integer)>max_integer_file:
						max_integer_file=int(file_integer)

	

		if self.comboBox_aufgabentyp.currentText()=='Typ 2':
			gk_path_temp=os.path.join(os.path.dirname('__file__'),'_database','Typ2Aufgaben','Einzelbeispiele')
			max_integer_file=0
			for all in os.listdir(gk_path_temp):
		
				if all.endswith('.tex'):
					file_integer, file_extension=all.split('.tex')
					if int(file_integer)>max_integer_file:
						max_integer_file=int(file_integer)
		

		for all in dict_picture_path:
			head, tail=os.path.split(all)
			x = '{'+tail+'}'
			name, ext =os.path.splitext(tail)
			if x in textBox_Entry and self.comboBox_aufgabentyp.currentText()=='Typ 1':
				textBox_Entry=str(textBox_Entry).replace(tail,'../_database/Bilder/'+list_chosen_gk[0].upper()+'_'+str(max_integer_file+1)+'_'+tail)
			if x in textBox_Entry and self.comboBox_aufgabentyp.currentText()=='Typ 2':
				textBox_Entry=str(textBox_Entry).replace(tail,'../_database/Bilder/'+str(max_integer_file+1)+'_'+tail)
		

		copy_image_path=os.path.join(os.path.dirname('__file__'),'_database','Bilder')
		for all in list(dict_picture_path.values()):
			image_path_temp=all
			head, tail=os.path.split(image_path_temp)
			copy_image_file_temp=os.path.join(copy_image_path,tail)
			shutil.copy(image_path_temp,copy_image_file_temp)
			if self.comboBox_aufgabentyp.currentText()=='Typ 1':
				x=os.rename(copy_image_file_temp,'_database/Bilder/'+list_chosen_gk[0].upper()+'_'+str(max_integer_file+1)+'_'+tail)
			if self.comboBox_aufgabentyp.currentText()=='Typ 2':
				x=os.rename(copy_image_file_temp,'_database/Bilder/'+str(max_integer_file+1)+'_'+tail)		



		if self.comboBox_aufgabentyp.currentText()=='Typ 1':
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
				file=open(file_name,"w")
				file.write('\section{'+file_name_klasse+' - '+list_chosen_gk[0].upper()+" - "+str(max_integer_file+1) +" - " + self.lineEdit_titel.text()+" - "+chosen_af+' - '+self.lineEdit_quelle.text()+"}\n\n"
				"\\begin{beispiel}["+file_name_klasse+' - '+list_chosen_gk[0].upper()+"]{"+str(self.spinBox_punkte.value())+"}\n"+textBox_Entry+
				"\n\\end{beispiel}")
				file.close()

			else:
				print(list_chosen_gk[0][:2].upper(),dict_gk[list_chosen_gk[0]])
				print(self.comboBox_klassen.currentText())

				file_name=os.path.join(gk_path_temp,dict_gk[list_chosen_gk[0]]+' - '+str(max_integer_file+1)+'.tex')
				
				file=open(file_name,"w")					
				if self.comboBox_klassen.currentText()=='-':
					chosen_af=list(dict_aufgabenformate.keys())[list(dict_aufgabenformate.values()).index(self.comboBox_af.currentText())].upper()
					file.write("\section{"+dict_gk[list_chosen_gk[0]]+" - "+str(max_integer_file+1) +" - "+self.lineEdit_titel.text()+" - "+chosen_af+" - "+self.lineEdit_quelle.text()+"}\n\n"
					"\\begin{beispiel}["+dict_gk[list_chosen_gk[0]]+"]{"+str(self.spinBox_punkte.value())+"}\n"+textBox_Entry+
					"\n\\end{beispiel}")
				else:
					try:
						klasse='K'+re.search(r'\d+',self.comboBox_klassen.currentText()).group() ### get selected grade
					except AttributeError:
						klasse='MAT'			
					chosen_af=list(dict_aufgabenformate.keys())[list(dict_aufgabenformate.values()).index(self.comboBox_af.currentText())].upper()
					file.write("\section{"+dict_gk[list_chosen_gk[0]]+" - "+str(max_integer_file+1) +' - '+ klasse +" - "+self.lineEdit_titel.text()+" - "+chosen_af+" - "+self.lineEdit_quelle.text()+"}\n\n"
					"\\begin{beispiel}["+dict_gk[list_chosen_gk[0]]+"]{"+str(self.spinBox_punkte.value())+"}\n"+textBox_Entry+
					"\n\\end{beispiel}")		
				file.close()			



		if self.comboBox_aufgabentyp.currentText()=='Typ 2':
			themen_klasse_auswahl=[]
			gk_auswahl=[]

			print(list_chosen_gk)
			for all in list_chosen_gk:
				if all in {**k5_beschreibung,**k6_beschreibung,**k7_beschreibung,**k8_beschreibung}:
					themen_klasse_auswahl.append(all.upper())
				else:
					gk_auswahl.append(dict_gk[all])

			gk_auswahl_joined=', '.join(sorted(gk_auswahl))
			themen_klasse_auswahl_joined=', '.join(sorted(themen_klasse_auswahl)) 			 
			print(gk_auswahl)
			print(themen_klasse_auswahl)


			file_name=os.path.join(os.path.dirname('__file__'),'_database','Typ2Aufgaben','Einzelbeispiele',str(max_integer_file+1)+'.tex')
			file=open(file_name,"w")
			klasse=''
			themen_klasse=''
			gk=''

			if self.comboBox_klassen.currentText()=='-':
				pass	
			else:	
				try:
					klasse='K'+re.search(r'\d+',self.comboBox_klassen.currentText()).group()+' - ' ### get selected grade
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

			file.write("\section{"+str(max_integer_file+1)+' - '+klasse + themen_klasse + gk +self.lineEdit_titel.text()+" - "+self.lineEdit_quelle.text()+"}\n\n"
			"\\begin{langesbeispiel} \item["+str(self.spinBox_punkte.value())+"] %PUNKTE DES BEISPIELS\n"+textBox_Entry+
			"\n\\end{langesbeispiel}")			

			file.close()




		if dict_picture_path!={}:
			x= ', '.join(dict_picture_path)
		else:
			x='-'


		chosen_typ=self.comboBox_aufgabentyp.currentText()[-1]
		if chosen_typ=='1':
			chosen_gk = dict_gk[list_chosen_gk[0]]
		if chosen_typ=='2':
			chosen_gk= ', '.join(sorted(gk_auswahl+themen_klasse_auswahl))


		QtWidgets.QApplication.restoreOverrideCursor()
		msg = QtWidgets.QMessageBox()
		msg.setIcon(QtWidgets.QMessageBox.Information)
		msg.setWindowTitle("Aufgabe erfolgreich gespeichert")
		#msg.setWindowIcon(QtWidgets.QIcon(r'C:\Users\Christoph\Desktop\lupe.png'))
		msg.setText('Die Typ{0}-Aufgabe mit dem Titel\n"{1}"\nwurde gespeichert.'.format(chosen_typ, self.lineEdit_titel.text()))
		msg.setDetailedText('Details\n'
		'Grundkompetenz(en): {0}\n'
		'Punkte: {1}\n'
		'Klasse: {2}\n'
		'Bilder: {3}'.format(chosen_gk, self.spinBox_punkte.value(), self.comboBox_klassen.currentText(), x))
		msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
		retval = msg.exec_()
		self.suchfenster_reset()
		

if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	MainWindow = QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())

