#!/usr/bin/python3
# -*- coding: utf-8 -*-
#### Version number ###
__version__ = "v1.8.6"
__lastupdate__ = "03/20"
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

from config import config_loader, path_programm, logo_path

from list_of_widgets import (
    widgets_search,
    widgets_create,
    widgets_sage,
    widgets_feedback,
)
from subwindows import Ui_Dialog_titlepage, Ui_Dialog_ausgleichspunkte
from translate import _fromUtf8, _translate
from sort_items import natural_keys
from create_pdf import create_pdf

try:
    loaded_lama_file_path = sys.argv[1]
except IndexError:
    loaded_lama_file_path = ""


print("Loading...")

### config_loader, path_programm, logo_path

config_file = os.path.join(path_programm, "_database", "_config", "config1.yml")

ag_beschreibung = config_loader(config_file, "ag_beschreibung")
an_beschreibung = config_loader(config_file, "an_beschreibung")
fa_beschreibung = config_loader(config_file, "fa_beschreibung")
ws_beschreibung = config_loader(config_file, "ws_beschreibung")

k5_beschreibung = config_loader(config_file, "k5_beschreibung")
k6_beschreibung = config_loader(config_file, "k6_beschreibung")
k7_beschreibung = config_loader(config_file, "k7_beschreibung")
k8_beschreibung = config_loader(config_file, "k8_beschreibung")

dict_gk = config_loader(config_file, "dict_gk")
dict_aufgabenformate = config_loader(config_file, "dict_aufgabenformate")
Klassen = config_loader(config_file, "Klassen")


dict_picture_path = {}
set_chosen_gk = set([])
list_sage_examples = []


### list_of_widgets


class SpinBox_noWheel(QtWidgets.QSpinBox):
    def wheelEvent(self, event):
        event.ignore()


### translate

#### Dialogue Window -- Titelblatt anpassen

#### Dialog Window - Ausgleichspunkte

### sort_items

### create_pdf


#### Dialog Window - Schularbeit erstellen
class Ui_Dialog_erstellen(object):
    def setupUi(
        self,
        Dialog,
        dict_list_input_examples,
        beispieldaten_dateipfad_1,
        beispieldaten_dateipfad_2,
        dict_titlepage,
        saved_file_path,
    ):
        # print(dict_list_input_examples)
        # print( beispieldaten_dateipfad_1)
        self.dict_list_input_examples = dict_list_input_examples
        self.beispieldaten_dateipfad_1 = beispieldaten_dateipfad_1
        self.beispieldaten_dateipfad_2 = beispieldaten_dateipfad_2
        self.dict_titlepage = dict_titlepage
        self.data_gesamt = self.dict_list_input_examples["data_gesamt"]
        self.saved_file_path = saved_file_path
        # print(self.data_gesamt)
        self.Dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(468, 208)
        Dialog.setWindowIcon(QtGui.QIcon(logo_path))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_sw_save = QtWidgets.QPushButton(Dialog)
        self.pushButton_sw_save.setObjectName("pushButton_sw_save")
        self.pushButton_sw_save.clicked.connect(self.pushButton_sw_save_pressed)
        self.gridLayout.addWidget(self.pushButton_sw_save, 5, 3, 1, 1)
        self.pushButton_sw_back = QtWidgets.QPushButton(Dialog)
        self.pushButton_sw_back.setObjectName("pushButton_sw_back")
        self.pushButton_sw_back.clicked.connect(self.pushButton_sw_back_pressed)
        self.gridLayout.addWidget(self.pushButton_sw_back, 4, 3, 1, 1)
        self.groupBox_sw_data = QtWidgets.QGroupBox(Dialog)
        self.groupBox_sw_data.setObjectName("groupBox_sw_data")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_sw_data)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_sw_num_ges = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_num_ges.setObjectName("label_sw_num_ges")
        self.gridLayout_2.addWidget(self.label_sw_num_ges, 6, 0, 1, 1)
        self.label_sw_num_1 = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_num_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_sw_num_1.setObjectName("label_sw_num_1")
        self.gridLayout_2.addWidget(
            self.label_sw_num_1, 3, 0, 1, 1, QtCore.Qt.AlignLeft
        )
        self.label_sw_num_2 = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_num_2.setObjectName("label_sw_num_2")
        self.gridLayout_2.addWidget(
            self.label_sw_num_2, 4, 0, 1, 1, QtCore.Qt.AlignLeft
        )
        self.label_sw_pkt_ges = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_pkt_ges.setObjectName("label_sw_pkt_ges")
        self.gridLayout_2.addWidget(self.label_sw_pkt_ges, 6, 3, 1, 1)
        self.label_sw_pkt_2 = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_pkt_2.setObjectName("label_sw_pkt_2")
        self.gridLayout_2.addWidget(self.label_sw_pkt_2, 4, 3, 1, 1)
        self.label_sw_pkt_1 = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_pkt_1.setObjectName("label_sw_pkt_1")
        self.gridLayout_2.addWidget(self.label_sw_pkt_1, 3, 3, 1, 1)
        self.label_sw_date = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_date.setObjectName("label_sw_date")
        self.gridLayout_2.addWidget(self.label_sw_date, 1, 0, 1, 1)
        self.label_sw_num_ges_int = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_num_ges_int.setObjectName("label_sw_num_ges_int")
        self.gridLayout_2.addWidget(self.label_sw_num_ges_int, 6, 1, 1, 1)
        self.label_sw_num_2_int = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_num_2_int.setObjectName("label_sw_num_2_int")
        self.gridLayout_2.addWidget(self.label_sw_num_2_int, 4, 1, 1, 1)
        self.label_sw_num_1_int = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_num_1_int.setObjectName("label_sw_num_1_int")
        self.gridLayout_2.addWidget(self.label_sw_num_1_int, 3, 1, 1, 1)
        self.label_sw_pkt_1_int = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_pkt_1_int.setObjectName("label_sw_pkt_1_int")
        self.gridLayout_2.addWidget(self.label_sw_pkt_1_int, 3, 4, 1, 1)
        self.label_sw_pkt_2_int = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_pkt_2_int.setObjectName("label_sw_pkt_2_int")
        self.gridLayout_2.addWidget(self.label_sw_pkt_2_int, 4, 4, 1, 1)
        self.line = QtWidgets.QFrame(self.groupBox_sw_data)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 5, 0, 1, 5)
        self.label_sw_pkt_ges_int = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_pkt_ges_int.setObjectName("label_sw_pkt_ges_int")
        self.gridLayout_2.addWidget(self.label_sw_pkt_ges_int, 6, 4, 1, 1)
        self.label_sw_klasse = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_klasse.setObjectName("label_sw_klasse")
        self.gridLayout_2.addWidget(self.label_sw_klasse, 1, 3, 1, 1)
        self.gridLayout.addWidget(self.groupBox_sw_data, 1, 0, 5, 3)
        self.groupBox_sw_gruppen = QtWidgets.QGroupBox(Dialog)
        self.groupBox_sw_gruppen.setObjectName("groupBox_sw_gruppen")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_sw_gruppen)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.spinBox_sw_gruppen = QtWidgets.QSpinBox(self.groupBox_sw_gruppen)
        self.spinBox_sw_gruppen.setMinimum(1)
        self.spinBox_sw_gruppen.setMaximum(5)
        self.spinBox_sw_gruppen.setObjectName("spinBox_sw_gruppen")
        if self.data_gesamt["Pruefungstyp"] == "Übungsblatt":
            self.groupBox_sw_gruppen.setEnabled(False)
        self.gridLayout_3.addWidget(self.spinBox_sw_gruppen, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_sw_gruppen, 3, 3, 1, 1)
        self.radioButton_sw_br = QtWidgets.QRadioButton(Dialog)
        self.radioButton_sw_br.setEnabled(False)
        self.radioButton_sw_br.setObjectName("radioButton_sw_br")
        self.gridLayout.addWidget(self.radioButton_sw_br, 2, 3, 1, 1)
        self.radioButton_sw_ns = QtWidgets.QRadioButton(Dialog)
        self.radioButton_sw_ns.setEnabled(False)
        self.radioButton_sw_ns.setObjectName("radioButton_sw_ns")
        self.gridLayout.addWidget(self.radioButton_sw_ns, 1, 3, 1, 1)
        if self.data_gesamt["Beurteilung"] == "ns":
            self.radioButton_sw_ns.setChecked(True)
        if self.data_gesamt["Beurteilung"] == "br":
            self.radioButton_sw_br.setChecked(True)
        self.cb_create_tex = QtWidgets.QCheckBox(Dialog)
        self.cb_create_tex.setObjectName(_fromUtf8("cb_create_tex"))
        self.cb_create_tex.setText(".tex")
        self.cb_create_tex.setChecked(True)
        self.cb_create_tex.setEnabled(False)
        self.gridLayout.addWidget(self.cb_create_tex, 6, 0, 1, 1)
        self.cb_create_pdf = QtWidgets.QCheckBox(Dialog)
        self.cb_create_pdf.setObjectName(_fromUtf8("cb_create_pdf"))
        self.cb_create_pdf.setText(".pdf")
        self.cb_create_pdf.setChecked(True)
        self.cb_create_pdf.toggled.connect(self.cb_create_pdf_checked)
        self.gridLayout.addWidget(self.cb_create_pdf, 6, 1, 1, 1)
        self.cb_create_lama = QtWidgets.QCheckBox(Dialog)
        self.cb_create_lama.setObjectName(_fromUtf8("cb_create_lama"))
        self.cb_create_lama.setText("Autosave (.lama)")
        self.cb_create_lama.setChecked(True)
        self.gridLayout.addWidget(self.cb_create_lama, 6, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        datum = (
            str(self.data_gesamt["Datum"][2])
            + "."
            + str(self.data_gesamt["Datum"][1])
            + "."
            + str(self.data_gesamt["Datum"][0])
        )
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Erstellen", "Erstellen"))
        self.radioButton_sw_ns.setText(_translate("Dialog", "Notenschlüssel"))
        self.pushButton_sw_save.setText(_translate("Dialog", "Speichern"))
        self.pushButton_sw_back.setText(_translate("Dialog", "Zurück "))
        if self.data_gesamt["Pruefungstyp"] == "Schularbeit":
            self.groupBox_sw_data.setTitle(
                _translate("Dialog", "%i. Schularbeit" % self.data_gesamt["#"])
            )
        else:
            self.groupBox_sw_data.setTitle(
                _translate("Dialog", self.data_gesamt["Pruefungstyp"])
            )
        self.label_sw_num_ges.setText(_translate("Dialog", "Aufgaben gesamt:"))
        self.label_sw_num_1.setText(_translate("Dialog", "Typ1 Aufgaben:"))
        self.label_sw_num_2.setText(_translate("Dialog", "Typ2 Aufgaben:"))
        self.label_sw_pkt_ges.setText(_translate("Dialog", "Gesamtpunkte:"))
        self.label_sw_pkt_2.setText(_translate("Dialog", "Punkte Typ2:"))
        self.label_sw_pkt_1.setText(_translate("Dialog", "Punkte Typ1:"))
        self.label_sw_date.setText(_translate("Dialog", "Datum: %s" % datum))
        self.label_sw_num_ges_int.setText(
            _translate(
                "Dialog",
                "%s" % str(self.data_gesamt["num_1"] + self.data_gesamt["num_2"]),
            )
        )
        self.label_sw_num_2_int.setText(
            _translate("Dialog", "%i" % self.data_gesamt["num_2"])
        )
        self.label_sw_num_1_int.setText(
            _translate("Dialog", "%i" % self.data_gesamt["num_1"])
        )
        self.label_sw_pkt_1_int.setText(
            _translate("Dialog", "{0}".format(self.data_gesamt["punkte_1"]))
        )
        self.label_sw_pkt_2_int.setText(
            _translate(
                "Dialog",
                "{0} (davon {1} AP)".format(
                    self.data_gesamt["punkte_2"], self.data_gesamt["ausgleichspunkte"]
                ),
            )
        )
        self.label_sw_pkt_ges_int.setText(
            _translate(
                "Dialog",
                "%s" % str(self.data_gesamt["punkte_1"] + self.data_gesamt["punkte_2"]),
            )
        )  # +self.data_gesamt['ausgleichspunkte']
        self.label_sw_klasse.setText(
            _translate("Dialog", "Klasse: %s" % self.data_gesamt["Klasse"])
        )
        self.groupBox_sw_gruppen.setTitle(_translate("Dialog", "Anzahl der Gruppen"))
        self.radioButton_sw_br.setText(_translate("Dialog", "Beurteilungsraster"))

    def cb_create_pdf_checked(self):
        if (
            self.cb_create_pdf.isChecked() == True
            and self.data_gesamt["Pruefungstyp"] != "Übungsblatt"
        ):
            self.groupBox_sw_gruppen.setEnabled(True)
        else:
            self.groupBox_sw_gruppen.setEnabled(False)

    def pushButton_sw_back_pressed(self):
        self.Dialog.reject()

    def pushButton_sw_save_pressed(self):
        self.Dialog.reject()
        MainWindow.hide()

        if self.cb_create_pdf.isChecked():
            pdf = True
        else:
            pdf = False

        if self.cb_create_lama.isChecked():
            lama = True
        else:
            lama = False
        for index in range(self.spinBox_sw_gruppen.value() * 2):
            Ui_MainWindow.pushButton_vorschau_pressed(
                self,
                "schularbeit",
                index,
                self.spinBox_sw_gruppen.value() * 2,
                pdf,
                lama,
            )

        MainWindow.show()

        if sys.platform.startswith("linux"):
            file_path = os.path.dirname(self.saved_file_path)
            subprocess.Popen('xdg-open "{}"'.format(file_path), shell=True)
        elif sys.platform.startswith("darwin"):
            file_path = os.path.dirname(self.saved_file_path)
            subprocess.Popen('open "{}"'.format(file_path), shell=True)

        # subprocess.run(['xdg-open', "{0}/Teildokument/{1}.pdf".format(path_programm, dateiname)])
        else:
            file_path = os.path.dirname(self.saved_file_path).replace("/", "\\")
            # print(file_path)
            # .replace('\n', ' ')
            subprocess.Popen('explorer "{}"'.format(file_path))
            # subprocess.Popen('explorer "C:\Users\Christoph\Desktop"')


class Ui_MainWindow(object):
    global dict_picture_path, set_chosen_gk, list_sage_examples

    def __init__(self):
        self.dict_sage_ausgleichspunkte_chosen = {}
        titlepage_save = os.path.join(path_programm, "Teildokument", "titlepage_save")
        if os.path.isfile(titlepage_save):
            with open(titlepage_save, encoding="utf8") as f:
                self.dict_titlepage = json.load(f)
        else:
            self.dict_titlepage = {
                "logo": False,
                "logo_path": False,
                "titel": True,
                "datum": True,
                "klasse": True,
                "name": True,
                "note": False,
                "unterschrift": False,
            }

        app.aboutToQuit.connect(self.close_app)

    def open_subwindow(
        self,
        dict_list_input_examples,
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
        self.ui = Ui_Dialog_erstellen()
        self.ui.setupUi(
            self.Dialog,
            dict_list_input_examples,
            beispieldaten_dateipfad_1,
            beispieldaten_dateipfad_2,
            dict_titlepage,
            saved_file_path
        )  # , dict_gesammeltedateien
        self.Dialog.show()
        self.Dialog.exec_()

    def setupUi(self, MainWindow):

        self.check_for_update()
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        # MainWindow.resize(900, 500)
        # MainWindow.move(30,30)
        # MainWindow.setMaximumSize(QtCore.QSize(1078, 16777215))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setStyleSheet(_fromUtf8(""))
        MainWindow.setWindowIcon(QtGui.QIcon(logo_path))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        # self.warnung = QtWidgets.QLabel(self.centralwidget)
        # self.warnung.setWordWrap(True)
        # self.warnung.setObjectName(_fromUtf8("warnung"))
        # self.warnung.setText(_translate("MainWindow", "Test", None))
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
        self.menuSage = QtWidgets.QMenu(self.menuBar)
        self.menuSage.setObjectName(_fromUtf8("menuSage"))
        self.menuSuche = QtWidgets.QMenu(self.menuBar)
        self.menuSuche.setObjectName(_fromUtf8("menuSuche"))
        self.menuFeedback = QtWidgets.QMenu(self.menuBar)
        self.menuFeedback.setObjectName(_fromUtf8("menuFeedback"))
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuBild_einf_gen = QtWidgets.QMenu(self.menuBar)
        self.menuBild_einf_gen.setObjectName(_fromUtf8("menuBild_einf_gen"))
        self.actionBild_einf_gen = QtWidgets.QAction(MainWindow)
        self.actionBild_einf_gen.setObjectName(_fromUtf8("actionBild_einf_gen"))
        self.actionBild_konvertieren_jpg_eps = QtWidgets.QAction(MainWindow)
        self.actionBild_konvertieren_jpg_eps.setObjectName(
            _fromUtf8("actionBild_konvertieren_jpg_eps")
        )
        MainWindow.setMenuBar(self.menuBar)
        self.actionReset = QtWidgets.QAction(MainWindow)
        self.actionReset.setObjectName(_fromUtf8("actionReset"))
        self.actionReset_sage = QtWidgets.QAction(MainWindow)
        self.actionReset_sage.setObjectName(_fromUtf8("actionReset_sage"))
        self.actionLoad = QtWidgets.QAction(MainWindow)
        self.actionLoad.setObjectName(_fromUtf8("actionLoad"))
        # self.actionLoad.setVisible(False)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        # self.actionSave.setVisible(False)
        self.actionAufgaben_Typ1 = QtWidgets.QAction(MainWindow)
        self.actionAufgaben_Typ1.setObjectName(_fromUtf8("actionAufgaben_Typ1"))
        self.actionAufgaben_Typ2 = QtWidgets.QAction(MainWindow)
        self.actionAufgaben_Typ2.setObjectName(_fromUtf8("actionAufgaben_Typ2"))
        self.actionRefresh_Database = QtWidgets.QAction(MainWindow)
        self.actionRefresh_Database.setObjectName(_fromUtf8("actionRefresh_Database"))
        self.actionNeu = QtWidgets.QAction(MainWindow)
        self.actionNeu.setObjectName(_fromUtf8("actionNeu"))
        self.actionSage = QtWidgets.QAction(MainWindow)
        self.actionSage.setObjectName(_fromUtf8("actionSage"))
        self.actionSuche = QtWidgets.QAction(MainWindow)
        self.actionSuche.setObjectName(_fromUtf8("actionSuche"))
        self.actionInfo = QtWidgets.QAction(MainWindow)
        self.actionInfo.setObjectName(_fromUtf8("actionInfo"))
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionFeedback = QtWidgets.QAction(MainWindow)
        self.actionFeedback.setObjectName(_fromUtf8("actionFeedback"))
        self.menuDateityp.addAction(self.actionAufgaben_Typ1)
        self.menuDateityp.addAction(self.actionAufgaben_Typ2)
        self.menuFeedback.addAction(self.actionFeedback)
        self.menuHelp.addAction(self.actionInfo)
        self.menuDatei.addAction(self.actionRefresh_Database)
        self.menuDatei.addAction(self.actionReset)
        self.menuDatei.addAction(self.actionReset_sage)
        self.actionReset_sage.setVisible(False)
        self.menuDatei.addSeparator()
        self.menuDatei.addAction(self.actionLoad)
        self.menuDatei.addAction(self.actionSave)
        self.menuDatei.addSeparator()
        self.menuDatei.addAction(self.actionBild_konvertieren_jpg_eps)
        self.menuDatei.addSeparator()
        self.menuDatei.addAction(self.actionExit)
        self.menuSage.addAction(self.actionSage)
        self.menuNeu.addAction(self.actionNeu)
        self.menuSuche.addAction(self.actionSuche)
        self.menuBar.addAction(self.menuDatei.menuAction())
        self.menuBar.addAction(self.menuDateityp.menuAction())
        self.menuBar.addAction(self.menuSage.menuAction())
        self.menuBar.addAction(self.menuNeu.menuAction())
        self.menuBar.addAction(self.menuFeedback.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.menuBild_einf_gen.addAction(self.actionBild_einf_gen)
        self.menuBild_einf_gen.addSeparator()
        # self.menuBild_einf_gen.addAction(self.actionBild_konvertieren_jpg_eps)
        self.groupBox_ausgew_gk = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_ausgew_gk.setObjectName(_fromUtf8("groupBox_ausgew_gk"))
        self.groupBox_ausgew_gk.setMaximumHeight(110)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_ausgew_gk)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.scrollArea_ausgew_gk = QtWidgets.QScrollArea(self.groupBox_ausgew_gk)
        self.scrollArea_ausgew_gk.setWidgetResizable(True)
        self.scrollArea_ausgew_gk.setObjectName("scrollArea_ausgew_gk")
        self.scrollAreaWidgetContents_ausgew_gk = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_ausgew_gk.setObjectName(
            "scrollAreaWidgetContents_ausgew_gk"
        )
        self.verticalLayout_scrollA_ausgew_gk = QtWidgets.QVBoxLayout(
            self.scrollAreaWidgetContents_ausgew_gk
        )
        self.verticalLayout_scrollA_ausgew_gk.setObjectName(
            "verticalLayout_scrollA_ausgew_gk"
        )

        self.label_gk = QtWidgets.QLabel(self.scrollArea_ausgew_gk)
        self.label_gk.setWordWrap(True)
        self.label_gk.setObjectName(_fromUtf8("label_gk"))
        self.verticalLayout_scrollA_ausgew_gk.addWidget(self.label_gk)
        self.label_gk_rest = QtWidgets.QLabel(self.scrollArea_ausgew_gk)
        self.label_gk_rest.setWordWrap(False)
        self.label_gk_rest.setObjectName(_fromUtf8("label_gk_rest"))
        self.verticalLayout_scrollA_ausgew_gk.addWidget(self.label_gk_rest)
        self.scrollArea_ausgew_gk.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_ausgew_gk.setWidget(self.scrollAreaWidgetContents_ausgew_gk)
        self.verticalLayout_2.addWidget(self.scrollArea_ausgew_gk)
        self.gridLayout.addWidget(self.groupBox_ausgew_gk, 3, 3, 1, 1)

        self.groupBox_titelsuche = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_titelsuche.setObjectName(_fromUtf8("groupBox_titelsuche"))

        # self.groupBox_titelsuche.setMaximumHeight(65)
        self.gridLayout_10 = QtWidgets.QGridLayout(self.groupBox_titelsuche)
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.entry_suchbegriffe = QtWidgets.QLineEdit(self.groupBox_titelsuche)

        self.entry_suchbegriffe.setObjectName(_fromUtf8("entry_suchbegriffe"))
        self.gridLayout_10.addWidget(self.entry_suchbegriffe, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_titelsuche, 4, 3, 1, 1)
        self.groupBox_klassen = QtWidgets.QGroupBox(self.centralwidget)
        # self.groupBox_klassen.setMaximumSize(QtCore.QSize(367, 16777215))
        self.groupBox_klassen.setObjectName(_fromUtf8("groupBox_klassen"))
        # self.groupBox_klassen.setMaximumHeight(100)
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
        self.cb_univie = QtWidgets.QCheckBox(self.groupBox_klassen)
        self.cb_univie.setObjectName(_fromUtf8("cb_univie"))
        self.gridLayout_14.addWidget(self.cb_univie, 1, 2, 1, 1)
        self.gridLayout.addWidget(self.groupBox_klassen, 3, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.cb_solution = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_solution.setObjectName(_fromUtf8("cb_solution"))
        self.cb_solution.setChecked(True)
        self.horizontalLayout_2.addWidget(self.cb_solution, QtCore.Qt.AlignLeft)
        self.cb_drafts = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_drafts.setObjectName(_fromUtf8("cb_drafts"))
        self.horizontalLayout_2.addWidget(self.cb_drafts)
        self.cb_drafts.toggled.connect(self.cb_drafts_enabled)
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
        self.label_update.setMaximumHeight(18)
        self.horizontalLayout.addWidget(self.label_update)
        # self.label_update.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_combobox = QtWidgets.QHBoxLayout()
        self.horizontalLayout_combobox.setObjectName(
            _fromUtf8("horizontalLayout_combobox")
        )
        self.label_aufgabentyp = QtWidgets.QLabel(self.centralwidget)
        self.label_aufgabentyp.setObjectName(_fromUtf8("label_aufgabentyp"))
        self.horizontalLayout_combobox.addWidget(self.label_aufgabentyp)
        self.combobox_searchtype = QtWidgets.QComboBox(self.centralwidget)
        # self.combobox_searchtype.setEnabled(True)
        self.combobox_searchtype.setMinimumContentsLength(1)
        # self.combobox_searchtype.setFrame(True)
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
        # self.tab_widget_gk.setMaximumSize(QtCore.QSize(650, 16777215))
        self.tab_widget_gk.setStyleSheet(
            _fromUtf8("background-color: rgb(217, 255, 215);")
        )
        self.tab_widget_gk.setObjectName(_fromUtf8("tab_widget_gk"))

        #### AG #####
        self.tab_ag = QtWidgets.QWidget()
        self.tab_ag.setObjectName(_fromUtf8("tab_ag"))
        self.gridLayout_ag = QtWidgets.QGridLayout(self.tab_ag)
        self.gridLayout_ag.setObjectName(_fromUtf8("gridLayout_ag"))
        self.scrollArea_ag = QtWidgets.QScrollArea(self.tab_ag)
        self.scrollArea_ag.setWidgetResizable(True)
        self.scrollArea_ag.setObjectName("scrollArea_ag")
        self.scrollAreaWidgetContents_ag = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_ag.setGeometry(QtCore.QRect(0, 0, 641, 252))
        self.scrollAreaWidgetContents_ag.setObjectName("scrollAreaWidgetContents_ag")
        self.gridLayout_scrollA_ag = QtWidgets.QGridLayout(
            self.scrollAreaWidgetContents_ag
        )
        self.gridLayout_scrollA_ag.setObjectName("gridLayout_scrollA_ag")
        self.btn_ag_all = QtWidgets.QPushButton(self.scrollArea_ag)
        self.btn_ag_all.setStyleSheet(
            _fromUtf8("background-color: rgb(240, 240, 240);")
        )
        self.btn_ag_all.setObjectName(_fromUtf8("btn_ag_all"))
        self.gridLayout_scrollA_ag.addWidget(
            self.btn_ag_all, 10, 4, 1, 1, QtCore.Qt.AlignRight
        )
        self.btn_ag_all.setMinimumSize(QtCore.QSize(100, 22))
        # self.btn_ag_all.setMaximumSize(QtCore.QSize(100,22))
        self.tab_widget_gk.addTab(self.tab_ag, _fromUtf8(""))
        self.create_checkbox_gk("ag", ag_beschreibung)
        self.scrollArea_ag.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_ag.setWidget(self.scrollAreaWidgetContents_ag)
        self.gridLayout_ag.addWidget(self.scrollArea_ag, 1, 0, 7, 1)
        #

        ### FA ###
        self.tab_fa = QtWidgets.QWidget()
        self.tab_fa.setObjectName(_fromUtf8("tab_fa"))
        self.gridLayout_fa = QtWidgets.QGridLayout(self.tab_fa)
        self.gridLayout_fa.setObjectName(_fromUtf8("gridLayout_fa"))
        self.scrollArea_fa = QtWidgets.QScrollArea(self.tab_fa)
        self.scrollArea_fa.setWidgetResizable(True)
        self.scrollArea_fa.setObjectName("scrollArea_fa")
        self.scrollAreaWidgetContents_fa = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents_ag.setGeometry(QtCore.QRect(0, 0, 641, 252))
        self.scrollAreaWidgetContents_fa.setObjectName("scrollAreaWidgetContents_fa")
        self.gridLayout_scrollA_fa = QtWidgets.QGridLayout(
            self.scrollAreaWidgetContents_fa
        )
        self.gridLayout_scrollA_fa.setObjectName("gridLayout_scrollA_fa")
        self.btn_fa_all = QtWidgets.QPushButton(self.scrollArea_fa)
        self.btn_fa_all.setStyleSheet(
            _fromUtf8("background-color: rgb(240, 240, 240);")
        )
        self.btn_fa_all.setObjectName(_fromUtf8("btn_fa_all"))
        self.gridLayout_scrollA_fa.addWidget(
            self.btn_fa_all, 10, 6, 1, 1, QtCore.Qt.AlignRight
        )
        self.btn_fa_all.setMinimumSize(QtCore.QSize(100, 22))
        # self.btn_fa_all.setMaximumSize(QtCore.QSize(100,22))
        self.tab_widget_gk.addTab(self.tab_fa, _fromUtf8(""))
        self.create_checkbox_gk("fa", fa_beschreibung)
        self.scrollArea_fa.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_fa.setWidget(self.scrollAreaWidgetContents_fa)
        self.gridLayout_fa.addWidget(self.scrollArea_fa, 1, 0, 7, 1)

        ### AN ###
        self.tab_an = QtWidgets.QWidget()
        self.tab_an.setObjectName(_fromUtf8("tab_an"))
        self.gridLayout_an = QtWidgets.QGridLayout(self.tab_an)
        self.gridLayout_an.setObjectName(_fromUtf8("gridLayout_an"))
        self.scrollArea_an = QtWidgets.QScrollArea(self.tab_an)
        self.scrollArea_an.setWidgetResizable(True)
        self.scrollArea_an.setObjectName("scrollArea_an")
        self.scrollAreaWidgetContents_an = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents_ag.setGeometry(QtCore.QRect(0, 0, 641, 252))
        self.scrollAreaWidgetContents_an.setObjectName("scrollAreaWidgetContents_an")
        self.gridLayout_scrollA_an = QtWidgets.QGridLayout(
            self.scrollAreaWidgetContents_an
        )
        self.gridLayout_scrollA_an.setObjectName("gridLayout_scrollA_an")
        self.btn_an_all = QtWidgets.QPushButton(self.scrollArea_an)
        self.btn_an_all.setStyleSheet(
            _fromUtf8("background-color: rgb(240, 240, 240);")
        )
        self.btn_an_all.setObjectName(_fromUtf8("btn_an_all"))
        self.gridLayout_scrollA_an.addWidget(
            self.btn_an_all, 10, 2, 1, 1, QtCore.Qt.AlignRight
        )
        self.btn_an_all.setMinimumSize(QtCore.QSize(100, 22))
        # self.btn_an_all.setMaximumSize(QtCore.QSize(100,22))
        self.tab_widget_gk.addTab(self.tab_an, _fromUtf8(""))
        self.create_checkbox_gk("an", an_beschreibung)
        self.scrollArea_an.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_an.setWidget(self.scrollAreaWidgetContents_an)
        self.gridLayout_an.addWidget(self.scrollArea_an, 1, 0, 7, 1)

        ### WS ###
        self.tab_ws = QtWidgets.QWidget()
        self.tab_ws.setObjectName(_fromUtf8("tab_ws"))
        self.gridLayout_ws = QtWidgets.QGridLayout(self.tab_ws)
        self.gridLayout_ws.setObjectName(_fromUtf8("gridLayout_ws"))
        self.scrollArea_ws = QtWidgets.QScrollArea(self.tab_ws)
        self.scrollArea_ws.setWidgetResizable(True)
        self.scrollArea_ws.setObjectName("scrollArea_ws")
        self.scrollAreaWidgetContents_ws = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents_ag.setGeometry(QtCore.QRect(0, 0, 641, 252))
        self.scrollAreaWidgetContents_ws.setObjectName("scrollAreaWidgetContents_ws")
        self.gridLayout_scrollA_ws = QtWidgets.QGridLayout(
            self.scrollAreaWidgetContents_ws
        )
        self.gridLayout_scrollA_ws.setObjectName("gridLayout_scrollA_ws")
        self.btn_ws_all = QtWidgets.QPushButton(self.tab_ws)
        self.btn_ws_all.setStyleSheet(
            _fromUtf8("background-color: rgb(240, 240, 240);")
        )
        self.btn_ws_all.setObjectName(_fromUtf8("btn_ws_all"))
        self.gridLayout_scrollA_ws.addWidget(
            self.btn_ws_all, 10, 2, 1, 1, QtCore.Qt.AlignRight
        )
        self.btn_ws_all.setMinimumSize(QtCore.QSize(100, 22))
        # self.btn_ws_all.setMaximumSize(QtCore.QSize(100,22))
        self.tab_widget_gk.addTab(self.tab_ws, _fromUtf8(""))
        self.create_checkbox_gk("ws", ws_beschreibung)
        self.scrollArea_ws.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_ws.setWidget(self.scrollAreaWidgetContents_ws)
        self.gridLayout_ws.addWidget(self.scrollArea_ws, 1, 0, 7, 1)
        ######### Klassenthemen
        ### K5
        self.tab_k5 = QtWidgets.QWidget()
        self.tab_k5.setObjectName(_fromUtf8("tab_k5"))
        self.gridLayout_k5 = QtWidgets.QGridLayout(self.tab_k5)
        self.gridLayout_k5.setObjectName(_fromUtf8("gridLayout_k5"))
        self.tabWidget.addTab(self.tab_k5, _fromUtf8(""))
        self.create_checkbox_klasse("k5", k5_beschreibung)
        ### K6
        self.tab_k6 = QtWidgets.QWidget()
        self.tab_k6.setObjectName(_fromUtf8("tab_k6"))
        self.gridLayout_k6 = QtWidgets.QGridLayout(self.tab_k6)
        self.gridLayout_k6.setObjectName(_fromUtf8("gridLayout_k6"))
        self.tabWidget.addTab(self.tab_k6, _fromUtf8(""))
        self.create_checkbox_klasse("k6", k6_beschreibung)
        ### K7
        self.tab_k7 = QtWidgets.QWidget()
        self.tab_k7.setObjectName(_fromUtf8("tab_k7"))
        self.gridLayout_k7 = QtWidgets.QGridLayout(self.tab_k7)
        self.gridLayout_k7.setObjectName(_fromUtf8("gridLayout_k7"))
        self.create_checkbox_klasse("k7", k7_beschreibung)
        self.tabWidget.addTab(self.tab_k7, _fromUtf8(""))
        ### K8
        self.tab_k8 = QtWidgets.QWidget()
        self.tab_k8.setObjectName(_fromUtf8("tab_k8"))
        self.gridLayout_k8 = QtWidgets.QGridLayout(self.tab_k8)
        self.gridLayout_k8.setObjectName(_fromUtf8("gridLayout_k8"))
        self.tabWidget.addTab(self.tab_k8, _fromUtf8(""))
        self.create_checkbox_klasse("k8", k8_beschreibung)

        #### Warnung ### Hinweis ####
        self.label_warnung = QtWidgets.QLabel(self.centralwidget)
        self.label_warnung.setWordWrap(True)
        self.label_warnung.setObjectName(_fromUtf8("label_warnung"))
        self.label_warnung.setStyleSheet(_fromUtf8("background-color: rgb(255, 80, 80);"))
        self.label_warnung.setText(_translate("MainWindow", "Achtung: Aufgrund neuer hilfreicher Befehle ist es ratsam, ein Update des srdp-mathematik-Pakets so bald wie möglich durchzuführen! Nähere Infos unter lama.schule", None))
        self.gridLayout.addWidget(self.label_warnung, 5,0,1,1)
        ##########################

        ##############################################################
        #####################CREATOR #########################################
        ##########################################################################

        self.groupBox_aufgabentyp = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_aufgabentyp.setObjectName(_fromUtf8("groupBox_aufgabentyp"))
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_aufgabentyp)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))

        self.groupBox_grundkompetenzen_cr = QtWidgets.QGroupBox(self.centralwidget)
        # self.groupBox_grundkompetenzen_cr.setMaximumSize(QtCore.QSize(350, 16777215))
        self.groupBox_grundkompetenzen_cr.setObjectName(
            _fromUtf8("groupBox_grundkompetenzen_cr")
        )
        self.groupBox_grundkompetenzen_cr.setMaximumWidth(500)
        self.gridLayout_11_cr = QtWidgets.QGridLayout(self.groupBox_grundkompetenzen_cr)
        self.gridLayout_11_cr.setObjectName(_fromUtf8("gridLayout_11_cr"))
        self.tab_widget_gk_cr = QtWidgets.QTabWidget(self.groupBox_grundkompetenzen_cr)
        self.tab_widget_gk_cr.setStyleSheet(
            _fromUtf8("background-color: rgb(217, 255, 215);")
        )
        self.tab_widget_gk_cr.setObjectName(_fromUtf8("tab_widget_gk_cr"))
        self.gridLayout_11_cr.addWidget(self.tab_widget_gk_cr, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_grundkompetenzen_cr, 1, 0, 5, 1)
        self.groupBox_grundkompetenzen_cr.setTitle(
            _translate("MainWindow", "Grundkompetenzen", None)
        )
        self.groupBox_grundkompetenzen_cr.hide()

        self.groupBox_ausgew_gk_cr = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_ausgew_gk_cr.setMinimumSize(QtCore.QSize(350, 0))
        self.groupBox_ausgew_gk_cr.setObjectName(_fromUtf8("groupBox_ausgew_gk_cr"))
        self.groupBox_ausgew_gk_cr.setMaximumWidth(500)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_ausgew_gk_cr)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_ausgew_gk = QtWidgets.QLabel(self.groupBox_ausgew_gk_cr)
        self.label_ausgew_gk.setWordWrap(True)
        self.label_ausgew_gk.setObjectName(_fromUtf8("label_ausgew_gk"))
        self.verticalLayout_2.addWidget(self.label_ausgew_gk)
        self.gridLayout.addWidget(self.groupBox_ausgew_gk_cr, 6, 0, 1, 1)
        self.groupBox_ausgew_gk_cr.setTitle(
            _translate("MainWindow", "Ausgewählte Grundkompetenzen", None)
        )
        self.label_ausgew_gk.setText(_translate("MainWindow", "", None))
        self.groupBox_ausgew_gk_cr.hide()

        self.groupBox_bilder = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_bilder.setMaximumSize(QtCore.QSize(16777215, 120))
        self.groupBox_bilder.setObjectName(_fromUtf8("groupBox_bilder"))
        self.groupBox_bilder.setMaximumWidth(500)
        self.gridLayout_13 = QtWidgets.QGridLayout(self.groupBox_bilder)
        self.gridLayout_13.setObjectName(_fromUtf8("gridLayout_13"))
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox_bilder)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollAreaWidgetContents_bilder = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_bilder.setGeometry(QtCore.QRect(0, 0, 320, 40))
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
        self.gridLayout.addWidget(self.groupBox_bilder, 7, 0, 1, 1)
        self.groupBox_bilder.hide()

        #### CREATE CHECKBOXES ####
        ##### AG #####
        self.tab_ag_cr = QtWidgets.QWidget()
        self.tab_ag_cr.setObjectName(_fromUtf8("tab_ag_cr"))
        self.gridLayout_ag_cr = QtWidgets.QGridLayout(self.tab_ag_cr)
        self.gridLayout_ag_cr.setObjectName(_fromUtf8("gridLayout_ag_cr"))
        self.tab_widget_gk_cr.addTab(self.tab_ag_cr, _fromUtf8(""))
        self.scrollArea_ag_cr = QtWidgets.QScrollArea(self.tab_ag_cr)
        self.scrollArea_ag_cr.setWidgetResizable(True)
        self.scrollArea_ag_cr.setObjectName("scrollArea_ag_cr")
        self.scrollAreaWidgetContents_ag_cr = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents_ag.setGeometry(QtCore.QRect(0, 0, 641, 252))
        self.scrollAreaWidgetContents_ag_cr.setObjectName(
            "scrollAreaWidgetContents_ag_cr"
        )
        self.gridLayout_scrollA_ag_cr = QtWidgets.QGridLayout(
            self.scrollAreaWidgetContents_ag_cr
        )
        self.gridLayout_scrollA_ag_cr.setObjectName("gridLayout_scrollA_ag_cr")
        self.create_checkbox_gk("ag_cr", ag_beschreibung)
        self.tab_widget_gk_cr.setTabText(
            self.tab_widget_gk_cr.indexOf(self.tab_ag_cr),
            _translate("MainWindow", "Algebra und Geometrie", None),
        )
        self.scrollArea_ag_cr.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_ag_cr.setWidget(self.scrollAreaWidgetContents_ag_cr)
        self.gridLayout_ag_cr.addWidget(self.scrollArea_ag_cr, 1, 0, 7, 1)

        # # #### FA ####
        self.tab_fa_cr = QtWidgets.QWidget()
        self.tab_fa_cr.setObjectName(_fromUtf8("tab_fa_cr"))
        self.gridLayout_fa_cr = QtWidgets.QGridLayout(self.tab_fa_cr)
        self.gridLayout_fa_cr.setObjectName(_fromUtf8("gridLayout_fa_cr"))
        self.tab_widget_gk_cr.addTab(self.tab_fa_cr, _fromUtf8(""))
        self.scrollArea_fa_cr = QtWidgets.QScrollArea(self.tab_fa_cr)
        self.scrollArea_fa_cr.setWidgetResizable(True)
        self.scrollArea_fa_cr.setObjectName("scrollArea_fa_cr")
        self.scrollAreaWidgetContents_fa_cr = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents_fa.setGeometry(QtCore.QRect(0, 0, 641, 252))
        self.scrollAreaWidgetContents_fa_cr.setObjectName(
            "scrollAreaWidgetContents_fa_cr"
        )
        self.gridLayout_scrollA_fa_cr = QtWidgets.QGridLayout(
            self.scrollAreaWidgetContents_fa_cr
        )
        self.gridLayout_scrollA_fa_cr.setObjectName("gridLayout_scrollA_fa_cr")
        self.create_checkbox_gk("fa_cr", fa_beschreibung)
        self.tab_widget_gk_cr.setTabText(
            self.tab_widget_gk_cr.indexOf(self.tab_fa_cr),
            _translate("MainWindow", "Funktionale Abhängigkeiten", None),
        )
        self.scrollArea_fa_cr.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_fa_cr.setWidget(self.scrollAreaWidgetContents_fa_cr)
        self.gridLayout_fa_cr.addWidget(self.scrollArea_fa_cr, 1, 0, 7, 1)
        # ##### AN ####
        self.tab_an_cr = QtWidgets.QWidget()
        self.tab_an_cr.setObjectName(_fromUtf8("tab_an_cr"))
        self.gridLayout_an_cr = QtWidgets.QGridLayout(self.tab_an_cr)
        self.gridLayout_an_cr.setObjectName(_fromUtf8("gridLayout_an_cr"))
        self.tab_widget_gk_cr.addTab(self.tab_an_cr, _fromUtf8(""))
        self.scrollArea_an_cr = QtWidgets.QScrollArea(self.tab_an_cr)
        self.scrollArea_an_cr.setWidgetResizable(True)
        self.scrollArea_an_cr.setObjectName("scrollArea_an_cr")
        self.scrollAreaWidgetContents_an_cr = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents_an.setGeometry(QtCore.QRect(0, 0, 641, 252))
        self.scrollAreaWidgetContents_an_cr.setObjectName(
            "scrollAreaWidgetContents_an_cr"
        )
        self.gridLayout_scrollA_an_cr = QtWidgets.QGridLayout(
            self.scrollAreaWidgetContents_an_cr
        )
        self.gridLayout_scrollA_an_cr.setObjectName("gridLayout_scrollA_an_cr")
        self.create_checkbox_gk("an_cr", an_beschreibung)
        self.tab_widget_gk_cr.setTabText(
            self.tab_widget_gk_cr.indexOf(self.tab_an_cr),
            _translate("MainWindow", "Analysis", None),
        )
        self.scrollArea_an_cr.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_an_cr.setWidget(self.scrollAreaWidgetContents_an_cr)
        self.gridLayout_an_cr.addWidget(self.scrollArea_an_cr, 1, 0, 7, 1)
        # ### WS ####
        self.tab_ws_cr = QtWidgets.QWidget()
        self.tab_ws_cr.setObjectName(_fromUtf8("tab_ws_cr"))
        self.gridLayout_ws_cr = QtWidgets.QGridLayout(self.tab_ws_cr)
        self.gridLayout_ws_cr.setObjectName(_fromUtf8("gridLayout_ws_cr"))
        self.tab_widget_gk_cr.addTab(self.tab_ws_cr, _fromUtf8(""))
        self.scrollArea_ws_cr = QtWidgets.QScrollArea(self.tab_ws_cr)
        self.scrollArea_ws_cr.setWidgetResizable(True)
        self.scrollArea_ws_cr.setObjectName("scrollArea_ws_cr")
        self.scrollAreaWidgetContents_ws_cr = QtWidgets.QWidget()
        # self.scrollAreaWidgetContents_fa.setGeometry(QtCore.QRect(0, 0, 641, 252))
        self.scrollAreaWidgetContents_ws_cr.setObjectName(
            "scrollAreaWidgetContents_ws_cr"
        )
        self.gridLayout_scrollA_ws_cr = QtWidgets.QGridLayout(
            self.scrollAreaWidgetContents_ws_cr
        )
        self.gridLayout_scrollA_ws_cr.setObjectName("gridLayout_scrollA_ws_cr")
        self.create_checkbox_gk("ws_cr", ws_beschreibung)
        self.tab_widget_gk_cr.setTabText(
            self.tab_widget_gk_cr.indexOf(self.tab_ws_cr),
            _translate("MainWindow", "Wahrscheinlichkeit und Statistik", None),
        )
        self.scrollArea_ws_cr.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_ws_cr.setWidget(self.scrollAreaWidgetContents_ws_cr)
        self.gridLayout_ws_cr.addWidget(self.scrollArea_ws_cr, 1, 0, 7, 1)
        # ### 5. Klasse ###
        self.tab_k5_cr = QtWidgets.QWidget()
        self.tab_k5_cr.setObjectName(_fromUtf8("tab_k5_cr"))
        self.gridLayout_k5_cr = QtWidgets.QGridLayout(self.tab_k5_cr)
        self.gridLayout_k5_cr.setObjectName(_fromUtf8("gridLayout_k5_cr"))
        self.tab_widget_gk_cr.addTab(self.tab_k5_cr, _fromUtf8(""))
        self.create_checkbox_klasse("k5_cr", k5_beschreibung)
        self.tab_widget_gk_cr.setTabText(
            self.tab_widget_gk_cr.indexOf(self.tab_k5_cr),
            _translate("MainWindow", "5. Klasse", None),
        )

        # ### 6. Klasse ###
        self.tab_k6_cr = QtWidgets.QWidget()
        self.tab_k6_cr.setObjectName(_fromUtf8("tab_k6_cr"))
        self.gridLayout_k6_cr = QtWidgets.QGridLayout(self.tab_k6_cr)
        self.gridLayout_k6_cr.setObjectName(_fromUtf8("gridLayout_k6_cr"))
        self.tab_widget_gk_cr.addTab(self.tab_k6_cr, _fromUtf8(""))
        self.create_checkbox_klasse("k6_cr", k6_beschreibung)
        self.tab_widget_gk_cr.setTabText(
            self.tab_widget_gk_cr.indexOf(self.tab_k6_cr),
            _translate("MainWindow", "6. Klasse", None),
        )

        # ### 7. Klasse ###
        self.tab_k7_cr = QtWidgets.QWidget()
        self.tab_k7_cr.setObjectName(_fromUtf8("tab_k7_cr"))
        self.gridLayout_k7_cr = QtWidgets.QGridLayout(self.tab_k7_cr)
        self.gridLayout_k7_cr.setObjectName(_fromUtf8("gridLayout_k7_cr"))
        self.tab_widget_gk_cr.addTab(self.tab_k7_cr, _fromUtf8(""))
        self.create_checkbox_klasse("k7_cr", k7_beschreibung)
        self.tab_widget_gk_cr.setTabText(
            self.tab_widget_gk_cr.indexOf(self.tab_k7_cr),
            _translate("MainWindow", "7. Klasse", None),
        )

        # ### 8. Klasse ###
        self.tab_k8_cr = QtWidgets.QWidget()
        self.tab_k8_cr.setObjectName(_fromUtf8("tab_k8_cr"))
        self.gridLayout_k8_cr = QtWidgets.QGridLayout(self.tab_k8_cr)
        self.gridLayout_k8_cr.setObjectName(_fromUtf8("gridLayout_k8_cr"))
        self.tab_widget_gk_cr.addTab(self.tab_k8_cr, _fromUtf8(""))
        self.create_checkbox_klasse("k8_cr", k8_beschreibung)
        self.tab_widget_gk_cr.setTabText(
            self.tab_widget_gk_cr.indexOf(self.tab_k8_cr),
            _translate("MainWindow", "8. Klasse", None),
        )

        self.groupBox_aufgabentyp.setMaximumSize(100, 60)
        self.comboBox_aufgabentyp_cr = QtWidgets.QComboBox(self.groupBox_aufgabentyp)
        self.comboBox_aufgabentyp_cr.setObjectName(_fromUtf8("comboBox_aufgabentyp_cr"))
        self.comboBox_aufgabentyp_cr.addItem(_fromUtf8(""))
        self.comboBox_aufgabentyp_cr.addItem(_fromUtf8(""))
        self.gridLayout_3.addWidget(self.comboBox_aufgabentyp_cr, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_aufgabentyp, 1, 1, 1, 1)
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
        self.groupBox_punkte.setMaximumSize(80, 60)
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_punkte)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.spinBox_punkte = QtWidgets.QSpinBox(self.groupBox_punkte)
        self.spinBox_punkte.setProperty("value", 1)
        self.spinBox_punkte.setObjectName(_fromUtf8("spinBox_punkte"))
        self.gridLayout_6.addWidget(self.spinBox_punkte, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_punkte, 1, 2, 1, 1)
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
        self.gridLayout.addWidget(self.groupBox_aufgabenformat, 1, 3, 1, 1)
        self.groupBox_aufgabenformat.setTitle(
            _translate("MainWindow", "Aufgabenformat", None)
        )
        self.comboBox_af.setItemText(
            0, _translate("MainWindow", "bitte auswählen", None)
        )
        i = 1
        for all in dict_aufgabenformate:
            self.comboBox_af.setItemText(
                i, _translate("MainWindow", dict_aufgabenformate[all], None)
            )
            i += 1
        self.groupBox_aufgabenformat.hide()
        self.label_keine_auswahl = QtWidgets.QLabel(self.groupBox_aufgabenformat)
        self.label_keine_auswahl.setObjectName(_fromUtf8("label_keine_auswahl"))
        self.label_keine_auswahl.setMinimumSize(QtCore.QSize(139, 0))
        self.gridLayout_7.addWidget(self.label_keine_auswahl)
        self.label_keine_auswahl.setText(
            _translate("MainWindow", "keine Auswahl nötig", None)
        )
        self.label_keine_auswahl.hide()

        self.groupBox_klassen_cr = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_klassen_cr.setObjectName(_fromUtf8("groupBox_klassen_cr"))
        self.groupBox_klassen_cr.setMaximumSize(100, 60)
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
        self.gridLayout.addWidget(self.groupBox_klassen_cr, 1, 4, 1, 1)
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

        self.groupBox_titel_cr = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_titel_cr.setObjectName(_fromUtf8("groupBox_titel_cr"))
        self.groupBox_titel_cr.setMaximumHeight(60)
        self.gridLayout_14 = QtWidgets.QGridLayout(self.groupBox_titel_cr)
        self.gridLayout_14.setObjectName(_fromUtf8("gridLayout_14"))
        self.lineEdit_titel = QtWidgets.QLineEdit(self.groupBox_titel_cr)
        self.lineEdit_titel.setObjectName(_fromUtf8("lineEdit_titel"))
        self.gridLayout_14.addWidget(self.lineEdit_titel, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_titel_cr, 2, 1, 1, 5)
        self.groupBox_titel_cr.setTitle(_translate("MainWindow", "Titel", None))
        self.groupBox_titel_cr.hide()

        self.groupBox_beispieleingabe = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_beispieleingabe.setObjectName(
            _fromUtf8("groupBox_beispieleingabe")
        )
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
        self.gridLayout.addWidget(self.groupBox_beispieleingabe, 3, 1, 4, 5)
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
        self.groupBox_quelle.setMaximumHeight(60)
        self.gridLayout_18 = QtWidgets.QGridLayout(self.groupBox_quelle)
        self.gridLayout_18.setObjectName(_fromUtf8("gridLayout_18"))
        self.lineEdit_quelle = QtWidgets.QLineEdit(self.groupBox_quelle)
        self.lineEdit_quelle.setObjectName(_fromUtf8("lineEdit_quelle"))
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
        ################# LaMA SAGE ####################
        #####################################################

        self.comboBox_at_sage = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_at_sage.setObjectName("comboBox_at_sage")
        self.comboBox_at_sage.addItem("")
        self.comboBox_at_sage.addItem("")
        self.gridLayout.addWidget(self.comboBox_at_sage, 1, 0, 1, 1)
        self.comboBox_at_sage.setItemText(0, _translate("MainWindow", "Typ 1", None))
        self.comboBox_at_sage.setItemText(1, _translate("MainWindow", "Typ 2", None))
        self.comboBox_at_sage.currentIndexChanged.connect(self.comboBox_at_sage_changed)
        self.comboBox_at_sage.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.comboBox_at_sage.hide()

        self.groupBox_alle_aufgaben = QtWidgets.QGroupBox(self.centralwidget)
        # self.groupBox_alle_aufgaben.setMinimumSize(QtCore.QSize(140, 16777215))
        self.groupBox_alle_aufgaben.setMaximumSize(QtCore.QSize(180, 16777215))
        self.groupBox_alle_aufgaben.setObjectName("groupBox_alle_aufgaben")
        self.verticalLayout_sage = QtWidgets.QVBoxLayout(self.groupBox_alle_aufgaben)
        self.verticalLayout_sage.setObjectName("verticalLayout_sage")
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
        self.lineEdit_number = QtWidgets.QLineEdit(self.groupBox_alle_aufgaben)
        self.lineEdit_number.setObjectName("lineEdit_number")
        self.lineEdit_number.textChanged.connect(
            partial(self.lineEdit_number_changed, "sage")
        )
        self.verticalLayout_sage.addWidget(self.lineEdit_number)
        self.listWidget = QtWidgets.QListWidget(self.groupBox_alle_aufgaben)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_sage.addWidget(self.listWidget)
        self.gridLayout.addWidget(self.groupBox_alle_aufgaben, 2, 0, 7, 1)
        self.groupBox_alle_aufgaben.setTitle(_translate("MainWindow", "Aufgaben", None))
        self.groupBox_alle_aufgaben.hide()

        self.groupBox_sage = QtWidgets.QGroupBox(self.centralwidget)
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
        self.comboBox_pruefungstyp.setObjectName("comboBox_pruefungstyp")
        list_comboBox_pruefungstyp = [
            "Schularbeit",
            "Nachschularbeit",
            "Wiederholungsschularbeit",
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
        self.comboBox_pruefungstyp.setMinimumContentsLength(1)
        self.gridLayout_5.addWidget(self.comboBox_pruefungstyp, 2, 4, 1, 2)
        self.comboBox_pruefungstyp.currentIndexChanged.connect(
            self.comboBox_pruefungstyp_changed
        )
        # self.verticalLayout_sage.addWidget(self.comboBox_pruefungstyp)

        self.radioButton_notenschl = QtWidgets.QRadioButton(self.groupBox_sage)
        self.radioButton_notenschl.setChecked(True)
        self.radioButton_notenschl.setObjectName("radioButton_notenschl")
        self.radioButton_notenschl.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.radioButton_notenschl.toggled.connect(self.beurteilungsraster_changed)
        self.gridLayout_5.addWidget(self.radioButton_notenschl, 3, 4, 1, 2)
        self.radioButton_beurteilungsraster = QtWidgets.QRadioButton(self.groupBox_sage)
        self.radioButton_beurteilungsraster.setObjectName(
            "radioButton_beurteilungsraster"
        )
        self.radioButton_beurteilungsraster.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.radioButton_beurteilungsraster.toggled.connect(
            self.beurteilungsraster_changed
        )
        self.gridLayout_5.addWidget(self.radioButton_beurteilungsraster, 4, 4, 1, 2)

        self.pushButton_titlepage = QtWidgets.QPushButton(self.groupBox_sage)
        self.pushButton_titlepage.setObjectName(_fromUtf8("pushButton_titlepage"))
        self.pushButton_titlepage.setText(
            _translate("MainWindow", "Titelblatt anpassen", None)
        )
        self.gridLayout_5.addWidget(self.pushButton_titlepage, 4, 6, 1, 1)

        self.groupBox_default_pkt = QtWidgets.QGroupBox(self.groupBox_sage)
        self.groupBox_default_pkt.setObjectName("groupBox_default_pkt")
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
        self.gridLayout_5.addWidget(self.groupBox_default_pkt, 2, 3, 3, 1)

        self.groupBox_klasse = QtWidgets.QGroupBox(self.groupBox_sage)
        self.groupBox_klasse.setObjectName("groupBox_klasse")
        # self.groupBox_klasse.setMaximumSize(QtCore.QSize(200, 16777215))
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_klasse)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lineEdit_klasse = QtWidgets.QLineEdit(self.groupBox_klasse)
        self.lineEdit_klasse.setObjectName("lineEdit_klasse")
        self.verticalLayout_4.addWidget(self.lineEdit_klasse)
        self.gridLayout_5.addWidget(self.groupBox_klasse, 2, 2, 3, 1)
        # self.groupBox_klasse.setMaximumSize(QtCore.QSize(90, 16777215))
        self.groupBox_datum = QtWidgets.QGroupBox(self.groupBox_sage)
        self.groupBox_datum.setObjectName("groupBox_datum")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_datum)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.dateEdit = QtWidgets.QDateEdit(self.groupBox_datum)
        self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit.setObjectName("dateEdit")
        self.verticalLayout_5.addWidget(self.dateEdit)
        self.gridLayout_5.addWidget(self.groupBox_datum, 2, 1, 3, 1)
        # self.groupBox_datum.setMaximumSize(QtCore.QSize(140, 16777215))
        self.groupBox_nummer = QtWidgets.QGroupBox(self.groupBox_sage)
        self.groupBox_nummer.setObjectName("groupBox_nummer")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_nummer)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.spinBox_nummer = QtWidgets.QSpinBox(self.groupBox_nummer)
        self.spinBox_nummer.setValue(1)
        self.spinBox_nummer.setObjectName("spinBox_nummer")
        # self.groupBox_nummer.setMaximumSize(QtCore.QSize(90, 16777215))
        self.radioButton_notenschl.setText(
            _translate("MainWindow", "Notenschlüssel", None)
        )
        self.radioButton_beurteilungsraster.setText(
            _translate("MainWindow", "Beurteilungsraster", None)
        )
        self.groupBox_klasse.setTitle(_translate("MainWindow", "Klasse", None))
        self.groupBox_datum.setTitle(_translate("MainWindow", "Datum", None))
        self.groupBox_nummer.setTitle(_translate("MainWindow", "Nummer", None))
        self.groupBox_default_pkt.setTitle(
            _translate("MainWindow", "Typ1 Standard", None)
        )
        self.verticalLayout_6.addWidget(self.spinBox_nummer)
        self.gridLayout_5.addWidget(self.groupBox_nummer, 2, 0, 3, 1)
        self.horizontalspacer = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_5.addItem(self.horizontalspacer, 2, 4, 3, 1)
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
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 389, 323))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.gridLayout_8 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.scrollArea_chosen.setWidget(self.scrollAreaWidgetContents_2)
        self.gridLayout_5.addWidget(self.scrollArea_chosen, 5, 0, 1, 7)

        # self.line_seperator = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
        # self.line_seperator.setFrameShape(QtWidgets.QFrame.HLine)
        # self.line_seperator.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.line_seperator.setObjectName("line_seperator")
        # self.line_seperator.setFocusPolicy(QtCore.Qt.NoFocus)
        # self.line_seperator.setLineWidth(3)
        # self.line_seperator.hide()

        self.groupBox_notenschl = QtWidgets.QGroupBox(self.groupBox_sage)
        self.groupBox_notenschl.setObjectName("groupBox_notenschl")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_notenschl)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.spinBox_3 = SpinBox_noWheel(self.groupBox_notenschl)
        self.spinBox_3.setMaximumSize(QtCore.QSize(55, 20))
        self.spinBox_3.setProperty("value", 80)
        self.spinBox_3.setObjectName("spinBox_3")
        self.spinBox_3.valueChanged.connect(self.punkte_changed)
        self.spinBox_3.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.gridLayout_6.addWidget(self.spinBox_3, 0, 4, 1, 1)
        self.label_sg_pkt = QtWidgets.QLabel(self.groupBox_notenschl)
        self.label_sg_pkt.setObjectName("label_sg_pkt")
        self.gridLayout_6.addWidget(self.label_sg_pkt, 0, 2, 1, 1)
        self.label_g_pkt = QtWidgets.QLabel(self.groupBox_notenschl)
        self.label_g_pkt.setObjectName("label_g_pkt")
        self.gridLayout_6.addWidget(self.label_g_pkt, 0, 5, 1, 1)
        self.label_g = QtWidgets.QLabel(self.groupBox_notenschl)
        self.label_g.setMaximumSize(QtCore.QSize(54, 20))
        self.label_g.setObjectName("label_g")
        self.gridLayout_6.addWidget(self.label_g, 0, 3, 1, 1)
        self.label_sg = QtWidgets.QLabel(self.groupBox_notenschl)
        self.label_sg.setMaximumSize(QtCore.QSize(64, 20))
        self.label_sg.setObjectName("label_sg")
        self.gridLayout_6.addWidget(self.label_sg, 0, 0, 1, 1)
        self.spinBox_2 = SpinBox_noWheel(self.groupBox_notenschl)
        self.spinBox_2.setMaximumSize(QtCore.QSize(55, 20))
        self.spinBox_2.setProperty("value", 91)
        self.spinBox_2.setObjectName("spinBox_2")
        self.spinBox_2.valueChanged.connect(self.punkte_changed)
        self.spinBox_2.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.gridLayout_6.addWidget(self.spinBox_2, 0, 1, 1, 1)
        self.label_b = QtWidgets.QLabel(self.groupBox_notenschl)
        self.label_b.setMaximumSize(QtCore.QSize(80, 20))
        self.label_b.setObjectName("label_b")
        self.gridLayout_6.addWidget(self.label_b, 1, 0, 1, 1)
        self.spinBox_4 = SpinBox_noWheel(self.groupBox_notenschl)
        self.spinBox_4.setMaximumSize(QtCore.QSize(55, 20))
        self.spinBox_4.setProperty("value", 64)
        self.spinBox_4.setObjectName("spinBox_4")
        self.spinBox_4.valueChanged.connect(self.punkte_changed)
        self.spinBox_4.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.gridLayout_6.addWidget(self.spinBox_4, 1, 1, 1, 1)
        self.label_b_pkt = QtWidgets.QLabel(self.groupBox_notenschl)
        self.label_b_pkt.setObjectName("label_b_pkt")
        self.gridLayout_6.addWidget(self.label_b_pkt, 1, 2, 1, 1)
        self.label_g_2 = QtWidgets.QLabel(self.groupBox_notenschl)
        self.label_g_2.setMaximumSize(QtCore.QSize(80, 20))
        self.label_g_2.setObjectName("label_g_2")
        self.gridLayout_6.addWidget(self.label_g_2, 1, 3, 1, 1)
        self.label_g_pkt_2 = QtWidgets.QLabel(self.groupBox_notenschl)
        self.label_g_pkt_2.setObjectName("label_g_pkt_2")
        self.gridLayout_6.addWidget(self.label_g_pkt_2, 1, 5, 1, 1)
        self.spinBox_5 = SpinBox_noWheel(self.groupBox_notenschl)
        self.spinBox_5.setMaximumSize(QtCore.QSize(55, 20))
        self.spinBox_5.setProperty("value", 50)
        self.spinBox_5.setObjectName("spinBox_5")
        self.spinBox_5.valueChanged.connect(self.punkte_changed)
        self.spinBox_5.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.gridLayout_6.addWidget(self.spinBox_5, 1, 4, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_notenschl, 6, 0, 1, 7)
        self.groupBox_notenschl.setTitle(
            _translate("MainWindow", "Notenschlüssel", None)
        )
        self.label_sg_pkt.setText(_translate("MainWindow", "% (ab 0)", None))
        self.label_g_pkt.setText(_translate("MainWindow", "% (ab 0)", None))
        self.label_g.setText(_translate("MainWindow", "Gut:", None))
        self.label_sg.setText(_translate("MainWindow", "Sehr Gut:", None))
        self.label_b.setText(_translate("MainWindow", "Befriedigend:", None))
        self.label_b_pkt.setText(_translate("MainWindow", "% (ab 0)", None))
        self.label_g_2.setText(_translate("MainWindow", "Genügend:", None))
        self.label_g_pkt_2.setText(_translate("MainWindow", "% (ab 0)", None))

        ### Groupbox Beurteilungsraster #####

        self.groupBox_beurteilungsra = QtWidgets.QGroupBox(self.groupBox_sage)
        self.groupBox_beurteilungsra.setObjectName("groupBox_beurteilungsra")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_beurteilungsra)
        self.gridLayout_6.setObjectName("gridLayout_6")

        self.label_typ1_pkt = QtWidgets.QLabel(self.groupBox_beurteilungsra)
        self.label_typ1_pkt.setObjectName("label_typ1_pkt")
        self.gridLayout_6.addWidget(self.label_typ1_pkt, 0, 0, 1, 1)
        # self.label_typ1_pkt.setText(_translate("MainWindow", "Punkte Typ 1: 0",None))

        self.label_typ2_pkt = QtWidgets.QLabel(self.groupBox_beurteilungsra)
        self.label_typ2_pkt.setObjectName("label_typ2_pkt")
        self.gridLayout_6.addWidget(self.label_typ2_pkt, 1, 0, 1, 1)

        self.label_ausgleich_pkt = QtWidgets.QLabel(self.groupBox_beurteilungsra)
        self.label_ausgleich_pkt.setObjectName("label_ausgleich_pkt")
        self.gridLayout_6.addWidget(self.label_ausgleich_pkt, 2, 0, 1, 1)
        # self.label_ausgleich_pkt.setText(_translate("MainWindow", "Ausgleichspunkte: 0",None))

        # self.label_typ2_pkt.setText(_translate("MainWindow", "Punkte Typ 2: 0",None))

        self.groupBox_beurteilungsra.setTitle(
            _translate("MainWindow", "Beurteilungsraster", None)
        )
        self.groupBox_beurteilungsra.hide()

        ### Zusammenfassung d. SA ###

        self.label_gesamtbeispiele = QtWidgets.QLabel(self.groupBox_sage)
        self.gridLayout_5.addWidget(self.label_gesamtbeispiele, 7, 0, 1, 3)
        self.label_gesamtbeispiele.setObjectName("label_gesamtbeispiele")
        self.label_gesamtbeispiele.setText(
            _translate(
                "MainWindow", "Anzahl der Aufgaben: 0 (Typ1: 0 / Typ2: 0)	 ", None
            )
        )

        self.label_gesamtpunkte = QtWidgets.QLabel(self.groupBox_sage)
        self.gridLayout_5.addWidget(self.label_gesamtpunkte, 8, 0, 1, 1)
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
        self.cb_solution_sage.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.gridLayout_5.addWidget(
            self.cb_solution_sage, 7, 4, 2, 1, QtCore.Qt.AlignRight
        )

        self.cb_drafts_sage = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_drafts_sage.setObjectName(_fromUtf8("cb_drafts_sage"))
        self.gridLayout_5.addWidget(self.cb_drafts_sage, 8, 4, 2, 1)
        self.cb_drafts_sage.setText(_translate("MainWindow", "Entwürfe anzeigen", None))
        # self.horizontalLayout_2.addWidget(self.cb_drafts_sage)
        self.cb_drafts_sage.toggled.connect(self.cb_drafts_sage_enabled)

        self.pushButton_vorschau = QtWidgets.QPushButton(self.groupBox_sage)
        self.pushButton_vorschau.setMaximumSize(QtCore.QSize(90, 16777215))
        self.pushButton_vorschau.setObjectName("pushButton_vorschau")
        self.pushButton_vorschau.setText(_translate("MainWindow", "Vorschau", None))
        self.pushButton_vorschau.setShortcut(_translate("MainWindow", "Return", None))
        self.gridLayout_5.addWidget(
            self.pushButton_vorschau, 7, 5, 1, 2, QtCore.Qt.AlignRight
        )
        self.pushButton_vorschau.clicked.connect(
            partial(self.pushButton_vorschau_pressed, "vorschau", 0, 0)
        )
        self.pushButton_vorschau.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.gridLayout.addWidget(self.groupBox_sage, 1, 2, 8, 3)

        self.pushButton_erstellen = QtWidgets.QPushButton(self.groupBox_sage)
        self.pushButton_erstellen.setMaximumSize(QtCore.QSize(90, 16777215))
        self.pushButton_erstellen.setObjectName("pushButton_erstellen")
        self.pushButton_erstellen.setText(_translate("MainWindow", "Erstellen", None))
        self.pushButton_erstellen.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.pushButton_erstellen.clicked.connect(self.pushButton_erstellen_pressed)
        self.gridLayout_5.addWidget(
            self.pushButton_erstellen, 8, 5, 1, 2, QtCore.Qt.AlignRight
        )
        self.groupBox_sage.hide()

        ################################################################
        ################################################################
        ########### FEEDBACK #############################################
        #######################################################################
        self.comboBox_at_fb = QtWidgets.QComboBox(self.centralwidget)
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
        self.groupBox_alle_aufgaben_fb.setMinimumSize(QtCore.QSize(140, 16777215))
        self.groupBox_alle_aufgaben_fb.setMaximumSize(QtCore.QSize(180, 16777215))
        self.groupBox_alle_aufgaben_fb.setObjectName("groupBox_alle_aufgaben_fb")
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
        self.gridLayout.addWidget(self.groupBox_alle_aufgaben_fb, 1, 0, 3, 1)
        self.groupBox_alle_aufgaben_fb.setTitle(
            _translate("MainWindow", "Aufgaben", None)
        )
        self.groupBox_alle_aufgaben_fb.hide()

        self.groupBox_fehlertyp = QtWidgets.QGroupBox(self.centralwidget)
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
        self.gridLayout_fb = QtWidgets.QGridLayout(self.groupBox_feedback)
        self.gridLayout_fb.setObjectName(_fromUtf8("gridLayout_fb"))
        self.plainTextEdit_fb = QtWidgets.QPlainTextEdit(self.groupBox_feedback)
        self.plainTextEdit_fb.setObjectName(_fromUtf8("plainTextEdit_fb"))
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
        self.gridLayout.addWidget(self.groupBox_email, 3, 1, 1, 3)
        self.groupBox_email.hide()

        self.pushButton_send = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_send.setObjectName(_fromUtf8("pushButton_send"))
        self.gridLayout.addWidget(
            self.pushButton_send, 4, 3, 1, 1, QtCore.Qt.AlignRight
        )
        self.pushButton_send.setText(_translate("MainWindow", "Senden", None))
        self.pushButton_send.clicked.connect(self.pushButton_send_pressed)
        self.pushButton_send.hide()

        ####################################################################
        #####################################################################
        ######################################################################
        #####################################################################

        self.gridLayout_11.addWidget(self.tab_widget_gk, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_gk, 1, 3, 2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        # self.actionReset = QtWidgets.QAction(MainWindow)
        # self.actionReset.setObjectName(_fromUtf8("actionReset"))

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)

        self.tab_widget_gk_cr.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        ############################################################################
        ############## Commands ####################################################
        ############################################################################

        # self.btn_refreshddb.clicked.connect(self.refresh_ddb)
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
        self.actionFeedback.triggered.connect(self.send_feedback)
        self.actionRefresh_Database.triggered.connect(
            self.refresh_ddb
        )  # self.label_aufgabentyp.text()[-1]
        self.actionReset.triggered.connect(self.suchfenster_reset)
        self.actionReset_sage.triggered.connect(self.reset_sage)
        self.actionLoad.triggered.connect(partial(self.sage_load, False))
        self.actionSave.triggered.connect(partial(self.sage_save, ""))
        self.actionAufgaben_Typ1.triggered.connect(self.chosen_aufgabenformat_typ1)
        self.actionAufgaben_Typ2.triggered.connect(self.chosen_aufgabenformat_typ2)
        self.actionInfo.triggered.connect(self.show_info)
        self.actionNeu.triggered.connect(self.neue_aufgabe_erstellen)
        self.actionSage.triggered.connect(self.neue_schularbeit_erstellen)
        self.actionSuche.triggered.connect(self.aufgaben_suchen)
        self.actionBild_einf_gen.triggered.connect(self.add_picture)
        self.actionBild_konvertieren_jpg_eps.triggered.connect(self.convert_imagetoeps)
        self.comboBox_aufgabentyp_cr.currentIndexChanged.connect(
            self.chosen_aufgabenformat_cr
        )
        self.pushButton_save.clicked.connect(self.save_file)
        self.pushButton_titlepage.clicked.connect(
            partial(self.titlepage_clicked, self.dict_titlepage)
        )

        for all in ag_beschreibung:
            x = eval("self.cb_" + all)
            x.stateChanged.connect(self.cb_checked)

        for all in fa_beschreibung:
            x = eval("self.cb_" + all)
            x.stateChanged.connect(self.cb_checked)

        for all in an_beschreibung:
            x = eval("self.cb_" + all)
            x.stateChanged.connect(self.cb_checked)

        for all in ws_beschreibung:
            x = eval("self.cb_" + all)
            x.stateChanged.connect(self.cb_checked)

        for g in range(5, 9):
            for all in eval("k%s_beschreibung" % g):
                x = eval("self.cb_k%s_" % g + all)
                x.stateChanged.connect(self.cb_rest_checked)

        for all in {
            **ag_beschreibung,
            **fa_beschreibung,
            **an_beschreibung,
            **ws_beschreibung,
        }:
            x = eval("self.cb_" + all + "_cr")
            x.stateChanged.connect(lambda: self.gk_checked_cr("gk"))

        for g in range(5, 9):
            for all in eval("k%s_beschreibung" % g):
                x = eval("self.cb_k%s_cr_" % g + all + "_cr")
                x.stateChanged.connect(lambda: self.gk_checked_cr("klasse"))

        if loaded_lama_file_path != "":
            self.sage_load(True)

        ############################################################################################
        ##############################################################################################

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            _translate(
                "LaMA - LaTeX Mathematik Assistent",
                "LaMA - LaTeX Mathematik Assistent",
                None,
            )
        )
        self.menuDateityp.setTitle(_translate("MainWindow", "Aufgabentyp", None))
        self.menuDatei.setTitle(_translate("MainWindow", "Datei", None))
        self.menuNeu.setTitle(_translate("MainWindow", "Neue Aufgabe", None))
        self.menuSage.setTitle(_translate("MainWindow", "Neue Schularbeit", None))
        self.menuSuche.setTitle(_translate("MainWindow", "Aufgabensuche", None))
        self.menuBild_einf_gen.setTitle(_translate("MainWindow", "Bild einfügen", None))
        self.menuFeedback.setTitle(_translate("MainWindow", "Feedback && Fehler", None))
        self.actionBild_einf_gen.setText(
            _translate("MainWindow", "Durchsuchen...", None)
        )
        self.actionBild_konvertieren_jpg_eps.setText(
            _translate("MainWindow", "Grafik konvertieren (jpg/png zu eps)", None)
        )
        self.menuHelp.setTitle(_translate("MainWindow", "?", None))
        self.actionReset.setText(_translate("MainWindow", "Reset", None))
        self.actionReset_sage.setText(
            _translate("MainWindow", "Reset Schularbeit", None)
        )
        self.actionReset.setShortcut("F4")
        self.actionLoad.setText(_translate("MainWindow", "Öffnen", None))
        self.actionLoad.setShortcut("Ctrl+O")
        self.actionSave.setText(_translate("MainWindow", "Speichern", None))
        self.actionSave.setShortcut("Ctrl+S")
        self.actionFeedback.setText(
            _translate("MainWindow", "Feedback oder Fehler senden ...", None)
        )
        self.actionAufgaben_Typ1.setText(
            _translate("MainWindow", "Typ 1 Aufgaben", None)
        )
        self.actionAufgaben_Typ1.setShortcut("Ctrl+1")
        self.actionAufgaben_Typ2.setText(
            _translate("MainWindow", "Typ 2 Aufgaben", None)
        )
        self.actionAufgaben_Typ2.setShortcut("Ctrl+2")
        self.actionInfo.setText(_translate("MainWindow", "Über LaMA", None))
        self.actionNeu.setText(
            _translate("MainWindow", "Neue Aufgabe erstellen...", None)
        )
        self.actionNeu.setShortcut("F3")
        self.actionSage.setText(
            _translate("MainWindow", "Neue Schularbeit erstellen...", None)
        )
        self.actionSage.setShortcut("F2")
        self.actionSuche.setText(_translate("MainWindow", "Aufgaben suchen...", None))
        self.actionSuche.setShortcut("F1")
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionRefresh_Database.setText(
            _translate("MainWindow", "Refresh Database", None)
        )
        self.actionRefresh_Database.setShortcut("F5")
        self.label_aufgabentyp.setText(
            _translate("MainWindow", "Aufgabentyp: Typ 1", None)
        )
        self.groupBox_ausgew_gk.setTitle(
            _translate("MainWindow", "Ausgewählte Grundkompetenzen", None)
        )
        self.groupBox_titelsuche.setTitle(_translate("MainWindow", "Titelsuche:", None))
        self.groupBox_klassen.setTitle(_translate("MainWindow", "Suchfilter", None))
        self.cb_k7.setText(_translate("MainWindow", "7. Klasse", None))
        self.cb_k5.setText(_translate("MainWindow", "5. Klasse", None))
        self.cb_k6.setText(_translate("MainWindow", "6. Klasse", None))
        self.cb_k8.setText(_translate("MainWindow", "8. Klasse", None))
        self.cb_mat.setText(_translate("MainWindow", "Matura", None))
        self.cb_univie.setText(_translate("MainWindow", "Uni Wien", None))
        self.cb_solution.setText(_translate("MainWindow", "Lösungen anzeigen", None))
        self.cb_drafts.setText(_translate("MainWindow", "Entwürfe anzeigen", None))

        try:
            log_file = os.path.join(path_programm, "Teildokument", "log_file_1")
            self.label_update.setText(
                _translate(
                    "MainWindow",
                    "Letztes Update: "
                    + self.modification_date(log_file).strftime("%d.%m.%y - %H:%M"),
                    None,
                )
            )
        except FileNotFoundError:
            self.label_update.setText(
                _translate("MainWindow", "Letztes Update: ---", None)
            )
        self.btn_suche.setText(_translate("MainWindow", "Suche starten", None))

        # self.btn_refreshddb.setText(_translate("MainWindow", "Refresh Database", None))
        # self.menu_aufgabentyp.setItemText(0, _translate("MainWindow", "Typ 1", None))
        # self.menu_aufgabentyp.setItemText(1, _translate("MainWindow", "Typ 2", None))
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
        self.groupBox_af.setMaximumSize(QtCore.QSize(375, 16777215))
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
        self.gridLayout.addWidget(self.groupBox_af, 4, 0, 1, 1)

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
        #########################

        ### Typ1
        # self.combobox_searchtype.setItemText(1, _translate("MainWindow", "Alle Dateien ausgeben, die alle Suchkriterien enthalten", None))
        ######

        ### Typ2
        self.combobox_searchtype.setItemText(
            1,
            _translate(
                "MainWindow",
                "Alle Dateien ausgeben, die ausschließlich diese Suchkriterien enthalten",
                None,
            ),
        )
        ######

        self.groupBox_themen_klasse.setTitle(
            _translate("MainWindow", "Themen Schulstufe", None)
        )
        # self.name_checkbox_klassen(5)
        # self.name_checkbox_klassen(6)
        # self.name_checkbox_klassen(7)
        # self.name_checkbox_klassen(8)

        self.btn_k5.setText(_translate("MainWindow", "alle auswählen", None))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_k5),
            _translate("MainWindow", "5. Klasse", None),
        )
        self.btn_k6.setText(_translate("MainWindow", "alle auswählen", None))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_k6),
            _translate("MainWindow", "6. Klasse", None),
        )
        self.btn_k7.setText(_translate("MainWindow", "alle auswählen", None))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_k7),
            _translate("MainWindow", "7. Klasse", None),
        )
        self.btn_k8.setText(_translate("MainWindow", "alle auswählen", None))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_k8),
            _translate("MainWindow", "8. Klasse", None),
        )
        self.groupBox_gk.setTitle(_translate("MainWindow", "Grundkompetenzen", None))
        self.btn_suche.setShortcut(_translate("MainWindow", "Return", None))
        # self.btn_refreshddb.setShortcut(_translate("MainWindow", "F5", None))

        ############# Infos for GKs
        self.create_Tooltip(ag_beschreibung)
        self.create_Tooltip(fa_beschreibung)
        self.create_Tooltip(an_beschreibung)
        self.create_Tooltip(ws_beschreibung)
        #############################################

        self.btn_ag_all.setText(_translate("MainWindow", "alle auswählen", None))
        self.tab_widget_gk.setTabText(
            self.tab_widget_gk.indexOf(self.tab_ag),
            _translate("MainWindow", "Algebra und Geometrie", None),
        )
        self.btn_an_all.setText(_translate("MainWindow", "alle auswählen", None))
        self.tab_widget_gk.setTabText(
            self.tab_widget_gk.indexOf(self.tab_an),
            _translate("MainWindow", "Analysis", None),
        )
        self.btn_fa_all.setText(_translate("MainWindow", "alle auswählen", None))
        self.tab_widget_gk.setTabText(
            self.tab_widget_gk.indexOf(self.tab_fa),
            _translate("MainWindow", "Funktionale Abhängigkeiten", None),
        )
        self.btn_fa_all.setText(_translate("MainWindow", "alle auswählen", None))
        self.tab_widget_gk.setTabText(
            self.tab_widget_gk.indexOf(self.tab_fa),
            _translate("MainWindow", "Funktionale Abhängigkeiten", None),
        )
        self.btn_ws_all.setText(_translate("MainWindow", "alle auswählen", None))
        self.tab_widget_gk.setTabText(
            self.tab_widget_gk.indexOf(self.tab_ws),
            _translate("MainWindow", "Wahrscheinlichkeit und Statistik", None),
        )
        self.actionReset.setText(_translate("MainWindow", "Reset", None))
        self.label_gk_rest.setText(_translate("MainWindow", "", None))
        self.label_gk.setText(_translate("MainWindow", "", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))

        print("Done")

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
                    self.warning_window(
                        'Das neue Update von LaMA konnte leider nicht installiert werden! Bitte versuchen Sie es später erneut oder melden Sie den Fehler unter dem Abschnitt "Feedback & Fehler".',
                        'Fehler:\n"{}"'.format(e),
                    )

    def create_Tooltip(self, chosen_dict):
        for all in chosen_dict:
            x = eval("self.cb_" + all)
            x.setToolTip(chosen_dict[all])
            y = eval("self.cb_" + all + "_cr")
            y.setToolTip(chosen_dict[all])

    def suchfenster_reset(self):
        global dict_picture_path
        for all in ag_beschreibung:
            x = eval("self.cb_" + all)
            x.setChecked(False)
            y = eval("self.cb_" + all + "_cr")
            y.setChecked(False)
        for all in an_beschreibung:
            x = eval("self.cb_" + all)
            x.setChecked(False)
            y = eval("self.cb_" + all + "_cr")
            y.setChecked(False)
        for all in fa_beschreibung:
            x = eval("self.cb_" + all)
            x.setChecked(False)
            y = eval("self.cb_" + all + "_cr")
            y.setChecked(False)
        for all in ws_beschreibung:
            x = eval("self.cb_" + all)
            x.setChecked(False)
            y = eval("self.cb_" + all + "_cr")
            y.setChecked(False)
        for r in range(5, 9):
            dict_klasse = eval("k" + str(r) + "_beschreibung")
            for all in dict_klasse:
                x = eval("self.cb_k" + str(r) + "_" + all)
                x.setChecked(False)
                y = eval("self.cb_k" + str(r) + "_cr_" + all + "_cr")
                y.setChecked(False)
        for all in Klassen:
            x = eval("self.cb_" + all)
            x.setChecked(False)
        for all in list(dict_aufgabenformate.keys()):
            x = eval("self.cb_af_" + all)
            x.setChecked(False)
        self.entry_suchbegriffe.setText("")
        self.cb_solution.setChecked(True)
        self.spinBox_punkte.setProperty("value", 1)
        self.comboBox_aufgabentyp_cr.setCurrentIndex(0)
        self.comboBox_af.setCurrentIndex(0)
        self.comboBox_klassen_cr.setCurrentIndex(0)
        self.label_ausgew_gk.setText(_translate("MainWindow", "-", None))
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

    def reset_sage(self):
        global list_sage_examples
        try:
            self.dict_list_input_examples

            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Question)
            msg.setWindowIcon(QtGui.QIcon(logo_path))
            msg.setWindowTitle("Schularbeit löschen?")
            msg.setText(
                "Sind Sie sicher, dass Sie das Fenster zurücksetzen wollen und die erstellte Schularbeit löschen möchten?"
            )
            msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            buttonY = msg.button(QtWidgets.QMessageBox.Yes)
            buttonY.setText("Ja")
            buttonN = msg.button(QtWidgets.QMessageBox.No)
            buttonN.setText("Nein")
            ret = msg.exec_()

            if ret == QtWidgets.QMessageBox.Yes:
                self.spinBox_nummer.setValue(1)
                self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
                self.comboBox_pruefungstyp.setCurrentIndex(0)
                self.lineEdit_klasse.setText("")
                self.spinBox_default_pkt.setValue(1)
                self.radioButton_notenschl.setChecked(True)
                self.spinBox_2.setProperty("value", 91)
                self.spinBox_3.setProperty("value", 80)
                self.spinBox_4.setProperty("value", 64)
                self.spinBox_5.setProperty("value", 50)
                self.comboBox_at_sage.setCurrentIndex(0)
                self.comboBox_gk.setCurrentIndex(0)
                self.comboBox_gk_num.setCurrentIndex(0)
                self.lineEdit_number.setText("")
                self.dict_list_input_examples = {
                    "list_examples": [],
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
                for all in list_sage_examples:
                    if re.search("[A-Z]", all) == None:
                        bsp_string = all
                    else:
                        bsp_string = (
                            all.replace(" ", "").replace(".", "").replace("-", "_")
                        )

                    try:
                        exec("self.groupBox_bsp_{}.setParent(None)".format(bsp_string))
                    except AttributeError:
                        pass
                list_sage_examples = []
                self.sage_aufgabe_create(False)

        except AttributeError:
            pass

    def close_app(self):
        try:
            self.dict_list_input_examples
        except AttributeError:
            sys.exit(0)

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowIcon(QtGui.QIcon(logo_path))
        msg.setText("Möchten Sie vor dem Schließen speichern?")
        msg.setWindowTitle("Schularbeit schon gespeichert?")
        msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        buttonY = msg.button(QtWidgets.QMessageBox.Yes)
        buttonY.setText("Ja")
        buttonN = msg.button(QtWidgets.QMessageBox.No)
        buttonN.setText("Nein")
        ret = msg.exec_()

        if ret == QtWidgets.QMessageBox.Yes:
            self.sage_save("")
            pass
        else:
            sys.exit(0)

    def show_info(self):
        QtWidgets.QApplication.restoreOverrideCursor()

        msg = QtWidgets.QMessageBox()

        # msg.setIcon(QtWidgets.QMessageBox.Information)
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
                    + self.modification_date(log_file).strftime("%d.%m.%y - %H:%M"),
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

    def create_checkbox_gk(self, gk_type, chosen_dict):

        row = 0
        column = 0
        if "cr" in gk_type:
            max_row = 8
        else:
            max_row = 9
        for all in chosen_dict:
            if "cr" in gk_type:
                cb_name = str(all + "_cr")
            else:
                cb_name = all
            exec(
                "self.cb_"
                + cb_name
                + "=QtWidgets.QCheckBox(self.scrollAreaWidgetContents_"
                + gk_type
                + ")"
            )
            exec(
                "self.cb_" + cb_name + '.setObjectName(_fromUtf8("cb_' + cb_name + '"))'
            )
            x = eval("self.cb_" + cb_name)
            x.setText(_translate("MainWindow", dict_gk[all], None))
            grid = eval("self.gridLayout_scrollA_" + gk_type)
            grid.addWidget(x, row, column, 1, 1)

            if row > max_row:
                row = 0
                column += 1
                spacerItem = QtWidgets.QSpacerItem(
                    100, 0, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum
                )
                grid.addItem(spacerItem, row, column, 1, 1)
                column += 1
            else:
                row += 1

        if "cr" in gk_type:
            row += 7
            spacerItem_end_cr = QtWidgets.QSpacerItem(
                0, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
            )
            grid.addItem(spacerItem_end_cr, row, column, 1, 1)

        spacerItem_end = QtWidgets.QSpacerItem(
            40, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        grid.addItem(spacerItem_end, row, column, 1, 1)

    def create_checkbox_klasse(self, klasse, chosen_dict):
        row = 0
        column = 0
        max_row = 9

        for all in chosen_dict:
            if "cr" in klasse:
                cb_name = str(all + "_cr")
                cb_label = chosen_dict[all].replace("\n", " ")
            else:
                cb_name = all
                cb_label = chosen_dict[all]
            exec(
                "self.cb_"
                + klasse
                + "_"
                + cb_name
                + "= QtWidgets.QCheckBox(self.tab_"
                + klasse
                + ")"
            )
            exec(
                "self.cb_"
                + klasse
                + "_"
                + cb_name
                + '.setObjectName(_fromUtf8("cb_'
                + klasse
                + "_"
                + cb_name
                + '"))'
            )
            grid = eval("self.gridLayout_" + klasse)
            x = eval("self.cb_" + klasse + "_" + cb_name)
            # x.setMaximumWidth(25)
            x.setMaximumSize(QtCore.QSize(20, 22))
            exec(
                "self.cb_label_"
                + klasse
                + "_"
                + cb_name
                + "= QtWidgets.QLabel(self.tab_"
                + klasse
                + ")"
            )
            exec(
                "self.cb_label_"
                + klasse
                + "_"
                + cb_name
                + '.setObjectName(_fromUtf8("cb_label_'
                + klasse
                + "_"
                + cb_name
                + '"))'
            )
            x_label = eval("self.cb_label_" + klasse + "_" + cb_name)
            x_label.setWordWrap(True)
            x_label.setText(_translate("MainWindow", cb_label, None))

            # self.label = QtWidgets.QLabel(self.groupBox_beispieleingabe)
            # label_aufgabe=eval('self.label_aufgabe_{}'.format(bsp_string))
            # x_label.setWordWrap(True)
            # label_aufgabe.setObjectName("label_aufgabe_{}".format(bsp_string))
            # self.gridLayout_gB.addWidget(label_aufgabe, 0, 0, 1, 1)

            # x.setText(_translate("MainWindow", cb_label, None))
            grid.addWidget(x, row, column, 1, 1)
            grid.addWidget(x_label, row, column + 1, 1, 1)

            if row > max_row:
                row = 0
                column += 2
            else:
                row += 1

            if "cr" in klasse:
                pass
            else:
                exec(
                    "self.btn_"
                    + klasse
                    + "= QtWidgets.QPushButton(self.tab_"
                    + klasse
                    + ")"
                )
                exec(
                    'self.btn_%s.setStyleSheet(_fromUtf8("background-color: rgb(240, 240, 240);"))'
                    % klasse
                )
                exec(
                    "self.btn_"
                    + klasse
                    + '.setObjectName(_fromUtf8("btn_'
                    + klasse
                    + '"))'
                )
                x_all = eval("self.btn_" + klasse)
                x_all.setMinimumSize(QtCore.QSize(100, 22))
                # x_all.setMaximumSize(QtCore.QSize(100,22))
                exec(
                    "self.gridLayout_"
                    + klasse
                    + ".addWidget(self.btn_"
                    + klasse
                    + ", max_row, column+1, 1, 1, QtCore.Qt.AlignRight)"
                )

    def btn_k5_pressed(self):
        if self.cb_k5_fu.isChecked() == False:
            for all in k5_beschreibung:
                x = eval("self.cb_k5_" + all)
                x.setChecked(True)
        elif self.cb_k5_fu.isChecked() == True:
            for all in k5_beschreibung:
                x = eval("self.cb_k5_" + all)
                x.setChecked(False)

    def btn_k6_pressed(self):
        if self.cb_k6_bsw.isChecked() == False:
            for all in k6_beschreibung:
                x = eval("self.cb_k6_" + all)
                x.setChecked(True)
        elif self.cb_k6_bsw.isChecked() == True:
            for all in k6_beschreibung:
                x = eval("self.cb_k6_" + all)
                x.setChecked(False)

    def btn_k7_pressed(self):
        if self.cb_k7_dr.isChecked() == False:
            for all in k7_beschreibung:
                x = eval("self.cb_k7_" + all)
                x.setChecked(True)
        elif self.cb_k7_dr.isChecked() == True:
            for all in k7_beschreibung:
                x = eval("self.cb_k7_" + all)
                x.setChecked(False)

    def btn_k8_pressed(self):
        if self.cb_k8_ddg.isChecked() == False:
            for all in k8_beschreibung:
                x = eval("self.cb_k8_" + all)
                x.setChecked(True)
        elif self.cb_k8_ddg.isChecked() == True:
            for all in k8_beschreibung:
                x = eval("self.cb_k8_" + all)
                x.setChecked(False)

    def btn_ag_all_pressed(self):
        if self.cb_ag11.isChecked() == False:
            for all in ag_beschreibung:
                x = eval("self.cb_" + all)
                x.setChecked(True)
        elif self.cb_ag11.isChecked() == True:
            for all in ag_beschreibung:
                x = eval("self.cb_" + all)
                x.setChecked(False)

    def btn_an_all_pressed(self):
        if self.cb_an11.isChecked() == False:
            for all in an_beschreibung:
                x = eval("self.cb_" + all)
                x.setChecked(True)
        elif self.cb_an11.isChecked() == True:
            for all in an_beschreibung:
                x = eval("self.cb_" + all)
                x.setChecked(False)

    def btn_fa_all_pressed(self):
        if self.cb_fa11.isChecked() == False:
            for all in fa_beschreibung:
                x = eval("self.cb_" + all)
                x.setChecked(True)
        elif self.cb_fa11.isChecked() == True:
            for all in fa_beschreibung:
                x = eval("self.cb_" + all)
                x.setChecked(False)

    def btn_ws_all_pressed(self):
        if self.cb_ws11.isChecked() == False:
            for all in ws_beschreibung:
                x = eval("self.cb_" + all)
                x.setChecked(True)
        elif self.cb_ws11.isChecked() == True:
            for all in ws_beschreibung:
                x = eval("self.cb_" + all)
                x.setChecked(False)

    # def cb_checked(self):
    # 	set_chosen_gk=set([])

    def cb_checked(self):
        chosen_gk = []

        list_gk = ["ag", "fa", "an", "ws"]

        for thema in list_gk:
            exec("set_chosen_gk_%s=set([])" % thema)
            for all in eval("%s_beschreibung" % thema):
                x = eval("self.cb_" + all)
                if x.isChecked() == True:
                    eval("set_chosen_gk_%s.add(x.text())" % thema)
            eval("chosen_gk.extend(sorted(set_chosen_gk_%s))" % thema)

        x = ", ".join(chosen_gk)

        self.label_gk.setText(_translate("MainWindow", str(x), None))

    def comboBox_pruefungstyp_changed(self):
        if (
            self.comboBox_pruefungstyp.currentText() == "Grundkompetenzcheck"
            or self.comboBox_pruefungstyp.currentText() == "Übungsblatt"
        ):
            self.radioButton_beurteilungsraster.setEnabled(False)
            self.radioButton_notenschl.setEnabled(False)
            self.groupBox_notenschl.setEnabled(False)
            self.groupBox_beurteilungsra.setEnabled(False)
            self.pushButton_titlepage.setEnabled(False)
        else:
            self.radioButton_beurteilungsraster.setEnabled(True)
            self.radioButton_notenschl.setEnabled(True)
            self.groupBox_notenschl.setEnabled(True)
            self.groupBox_beurteilungsra.setEnabled(True)
            self.pushButton_titlepage.setEnabled(True)

    def cb_rest_checked(self):
        set_chosen_gk = set([])
        for all in k5_beschreibung:
            x = eval("self.cb_k5_" + all)
            if x.isChecked() == True:
                set_chosen_gk.add(all.upper() + "(5)")
        for all in k6_beschreibung:
            x = eval("self.cb_k6_" + all)
            if x.isChecked() == True:
                set_chosen_gk.add(all.upper() + "(6)")
        for all in k7_beschreibung:
            x = eval("self.cb_k7_" + all)
            if x.isChecked() == True:
                set_chosen_gk.add(all.upper() + "(7)")
        for all in k8_beschreibung:
            x = eval("self.cb_k8_" + all)
            if x.isChecked() == True:
                set_chosen_gk.add(all.upper() + "(8)")
        if len(set_chosen_gk) > 6:
            x = ", ".join(list(sorted(set_chosen_gk))[:6])
            x = x + ", ..."
        else:
            x = ", ".join(sorted(set_chosen_gk))
        if len(set_chosen_gk) > 0:
            x = "Weitere: " + x
        self.label_gk_rest.setText(_translate("MainWindow", str(x), None))

    ############################################################################
    ############################################################################
    ######### Button REFRESH DATABASE ######################################
    ############################################################################

    def modification_date(self, filename):
        t = os.path.getmtime(filename)
        return datetime.datetime.fromtimestamp(t)

    def refresh_ddb(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowIcon(QtGui.QIcon(logo_path))
        msg.setWindowTitle("Refresh Database")
        msg.setStandardButtons(QtWidgets.QMessageBox.NoButton)
        msg.setText("Datenbank wird aktualisiert. Bitte warten...")

        msg.show()
        QApplication.processEvents()
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        for selected_aufgabentyp in [1, 2]:
            beispieldaten_dateipfad = {}
            beispieldaten = []
            chosen_aufgabenformat = "Typ%sAufgaben" % selected_aufgabentyp
            ########################################################
            ##### Suche offizielle Beispiele ####################
            ##################################################

            for root, dirs, files in os.walk(
                os.path.join(path_programm, "_database", chosen_aufgabenformat)
            ):
                for all in files:
                    if all.endswith(".tex") or all.endswith(".ltx"):
                        if not ("Gesamtdokument" in all) and not (
                            "Teildokument" in all
                        ):
                            file = open(os.path.join(root, all), encoding="utf8")
                            for i, line in enumerate(file):
                                if not line == "\n":
                                    beispieldaten_dateipfad[line] = os.path.join(
                                        root, all
                                    )
                                    beispieldaten.append(line)
                                    break
                            file.close()

            ################################################
            #### Suche inoffizielle Beispiele ######
            #############################################

            for root, dirs, files in os.walk(
                os.path.join(
                    path_programm, "_database_inoffiziell", chosen_aufgabenformat
                )
            ):
                for all in files:
                    if all.endswith(".tex") or all.endswith(".ltx"):
                        if not ("Gesamtdokument" in all) and not (
                            "Teildokument" in all
                        ):
                            file = open(os.path.join(root, all), encoding="utf8")
                            for i, line in enumerate(file):
                                if not line == "\n":
                                    beispieldaten_dateipfad[line] = os.path.join(
                                        root, all
                                    )
                                    beispieldaten.append(line)
                                    break
                            file.close()

            ################################################
            #### Suche lokal gespeicherte Beispiele ######
            #############################################

            for root, dirs, files in os.walk(
                os.path.join(path_programm, "Lokaler_Ordner", chosen_aufgabenformat)
            ):
                for all in files:
                    if all.endswith(".tex") or all.endswith(".ltx"):
                        if not ("Gesamtdokument" in all) and not (
                            "Teildokument" in all
                        ):
                            # print(os.path.join(root,all))
                            file = open(os.path.join(root, all), encoding="utf8")
                            for i, line in enumerate(file):
                                if not line == "\n":
                                    beispieldaten_dateipfad[line] = os.path.join(
                                        root, all
                                    )
                                    beispieldaten.append(line)
                                    break
                            file.close()

            temp_dict_beispieldaten = {}
            temp_list = list(beispieldaten_dateipfad.keys())
            temp_list.sort(key=natural_keys)
            for all in temp_list:
                temp_dict_beispieldaten.update({all: beispieldaten_dateipfad[all]})

            beispieldaten_dateipfad = temp_dict_beispieldaten

            # print(beispieldaten_dateipfad)

            log_file = os.path.join(
                path_programm, "Teildokument", "log_file_%s" % selected_aufgabentyp
            )

            try:
                with open(log_file, "w+", encoding="utf8") as f:
                    json.dump(beispieldaten_dateipfad, f, ensure_ascii=False)
            except FileNotFoundError:
                os.makedirs(os.path.join(path_programm, "Teildokument"))
                with open(log_file, "w+", encoding="utf8") as f:
                    json.dump(beispieldaten_dateipfad, f, ensure_ascii=False)

            self.label_update.setText(
                _translate(
                    "MainWindow",
                    "Last Update: "
                    + self.modification_date(log_file).strftime("%d.%m.%y - %H:%M"),
                    None,
                )
            )
        QtWidgets.QApplication.restoreOverrideCursor()
        self.adapt_choosing_list("sage")
        self.adapt_choosing_list("feedback")
        msg.close()

    ############################################################################
    ############################################################################
    ########################### CREATE PDF ####################################
    ############################################################################

    def cb_drafts_enabled(self):
        if self.cb_drafts.isChecked():
            self.warning_window(
                "Achtung!\nEntwürfe können Fehler enthalten, die das Programm zum Absturz bringen.",
                "\nSpeichern Sie gegebenenfalls eine erstellte Schularbeit vor der Suche!",
                "Here be dragons!",
            )

    def cb_drafts_sage_enabled(self):
        if self.cb_drafts_sage.isChecked():
            self.warning_window(
                "Achtung!\nEntwürfe können Fehler enthalten, die das Programm zum Absturz bringen.",
                "\nSpeichern Sie gegebenenfalls eine erstellte Schularbeit vor dem Erstellen!",
                "Here be dragons!",
            )
        self.adapt_choosing_list("sage")

    def PrepareTeXforPDF(self):
        chosen_aufgabenformat = "Typ%sAufgaben" % self.label_aufgabentyp.text()[-1]

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        if not os.path.isfile(
            os.path.join(
                path_programm,
                "Teildokument",
                "log_file_%s" % self.label_aufgabentyp.text()[-1],
            )
        ):
            self.refresh_ddb()  # self.label_aufgabentyp.text()[-1]
        else:  ##  Automatic update once per month
            log_file = os.path.join(
                path_programm,
                "Teildokument",
                "log_file_%s" % self.label_aufgabentyp.text()[-1],
            )
            month_update_log_file = self.modification_date(log_file).strftime("%m")
            month_today = datetime.date.today().strftime("%m")
            if month_today != month_update_log_file:
                self.refresh_ddb()  # self.label_aufgabentyp.text()[-1]

        suchbegriffe = []

        #### ALGEBRA UND GEOMETRIE
        for all in ag_beschreibung:
            x = eval("self.cb_" + all)
            if x.isChecked() == True:
                suchbegriffe.append(all)

        #### ANALYSIS
        for all in an_beschreibung:
            x = eval("self.cb_" + all)
            if x.isChecked() == True:
                suchbegriffe.append(all)

        #### FUNKTIONALE ABHÄNGIGKEITEN
        for all in fa_beschreibung:
            x = eval("self.cb_" + all)
            if x.isChecked() == True:
                suchbegriffe.append(all)
        #### WAHRSCHEINLICHKEIT UND STATISTIK
        for all in ws_beschreibung:
            x = eval("self.cb_" + all)
            if x.isChecked() == True:
                suchbegriffe.append(all)

        temp_suchbegriffe = []
        for all in suchbegriffe:
            temp_suchbegriffe.append(dict_gk[all])
        suchbegriffe = temp_suchbegriffe

        #### Suche der Schulstufe
        for y in range(5, 9):
            themen_klasse = eval("k%s_beschreibung" % y)
            for all in themen_klasse:
                x = eval("self.cb_k%s_" % y + all)
                grade = "K" + str(y)
                if x.isChecked() == True:
                    # if grade not in suchbegriffe:
                    # suchbegriffe.append('K'+str(y))
                    suchbegriffe.append(all.upper())

        #### typ1 ###
        # log_file=os.path.join(path_programm,'Typ 2 Aufgaben','Teildokument','log_file')
        ######

        log_file = os.path.join(
            path_programm,
            "Teildokument",
            "log_file_%s" % self.label_aufgabentyp.text()[-1],
        )

        with open(log_file, encoding="utf8") as f:
            beispieldaten_dateipfad = json.load(f)
            # beispieldaten_dateipfad=eval(beispieldaten_dateipfad)
            beispieldaten = list(beispieldaten_dateipfad.keys())

        if self.cb_drafts.isChecked():
            # print(beispieldaten_dateipfad)
            QtWidgets.QApplication.restoreOverrideCursor()
            drafts_path = os.path.join(path_programm, "Beispieleinreichung")
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

        path_srdp_pkg = os.path.join(path_programm, "_database", "_config", "srdp-mathematik.sty")
        copy_path_srdp_pkg = os.path.join(path_programm, "Teildokument", "srdp-mathematik.sty")
        if os.path.isfile(copy_path_srdp_pkg):
            pass
        else:
            shutil.copy(path_srdp_pkg, copy_path_srdp_pkg)

        ########################################################

        filename_teildokument = os.path.join(
            path_programm,
            "Teildokument",
            "Teildokument_%s.tex" % self.label_aufgabentyp.text()[-1],
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
            file.write(
                "\\usepackage[solution_off]{srdp-mathematik} % solution_on/off\n"
            )
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

            gesammeltedateien = []
            gesammeltedateien_temporary = []
            for r in range(1, len(liste_kompetenzbereiche) + 1):
                if liste_kompetenzbereiche[r] == []:
                    gesammeltedateien.append(
                        list(beispieldaten_dateipfad.keys())[r - 1]
                    )
            # return
            # for all in gesammeltedateien:
            # 	if entry_suchbegriffe.get().lower() in all.lower():
            # 		gesammeltedateien_temporary.append(all)
            gesammeltedateien = sorted(gesammeltedateien)

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

        # if not len(self.entry_suchbegriffe.text())==0:
        # 	suchbegriffe.append(self.entry_suchbegriffe.text())

        gesammeltedateien.sort(key=natural_keys)

        dict_gesammeltedateien = {}

        for all in gesammeltedateien:
            dict_gesammeltedateien[all] = beispieldaten_dateipfad[all]

        # print(dict_gesammeltedateien)
        # return

        #### typ1 ###
        # ###############################################
        # #### Auswahl der gesuchten Antwortformate ####
        # ###############################################
        if chosen_aufgabenformat == "Typ1Aufgaben":
            if (
                self.cb_af_mc.isChecked()
                or self.cb_af_lt.isChecked()
                or self.cb_af_zo.isChecked()
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
        selected_klassen = []
        if (
            self.cb_k5.isChecked()
            or self.cb_k6.isChecked()
            or self.cb_k7.isChecked()
            or self.cb_k8.isChecked() == True
            or self.cb_mat.isChecked() == True
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
        for all in suchbegriffe:
            if all == suchbegriffe[-1]:
                file.write(all)
            else:
                file.write(all + ", ")
        file.write("\\normalsize \n \n")

        for key, value in dict_gesammeltedateien.items():
            value = value.replace("\\", "/")
            file = open(filename_teildokument, "a", encoding="utf8")

            ### newpage only with typ2 !!
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

            # else:
            # 	if chosen_aufgabenformat=='Typ 1 Aufgaben':
            # 		file.write('\input{".'+value+'"}%\n'
            # 		'\hrule	 \leer\n\n')
            # 	elif chosen_aufgabenformat=='Typ 2 Aufgaben':
            # 		file.write('\input{".'+value+'"}%\n'
            # 		'\\newpage \n')

        file.write('\shorthandoff{"}\n' "\end{document}")

        file.close()

        # print(dict_gesammeltedateien)
        # return

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
            # geometry=MainWindow.geometry()
            # print(geometry)
            # MainWindow.hide()
            typ = self.label_aufgabentyp.text()[-1]
            if sys.platform.startswith("linux"):
                MainWindow.hide()
            create_pdf("Teildokument", 0, 0, typ)
            if sys.platform.startswith("linux"):
                MainWindow.show()
            # MainWindow.show()
            # MainWindow.move(geometry.x(),geometry.y())
            # MainWindow.resize(geometry.width(), geometry.height())

            # sys.exit(0)

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
            # print(head,tail)
            # print(dict_picture_path.keys())
            if tail in dict_picture_path.keys():
                pass
            else:
                head, tail = os.path.split(all)
                dict_picture_path[tail] = all
                x = "self.label_bild_" + str(i)
                # print(dict_picture_path)
                # print(head,tail)
                exec("%s= QtWidgets.QLabel(self.scrollAreaWidgetContents_bilder)" % x)
                eval(x).setObjectName(_fromUtf8("label_bild_%s" % i))

                eval(x).mousePressEvent = functools.partial(
                    self.del_picture, name_of_image=x
                )
                self.verticalLayout.addWidget(eval(x))
                eval(x).setText(_translate("MainWindow", tail, None))
                i += 1

    def del_picture(self, event, name_of_image=None):
        del dict_picture_path[eval(name_of_image).text()]
        eval(name_of_image).hide()
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
                        self.warning_window(
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

    def gk_checked_cr(self, thema):
        global set_chosen_gk
        set_chosen_gk = set([])
        set_chosen_gk_label = set([])
        for all in {
            **ag_beschreibung,
            **fa_beschreibung,
            **an_beschreibung,
            **ws_beschreibung,
        }:  ## merged dictionionaries
            x = eval("self.cb_" + all + "_cr")
            if x.isChecked() == True:
                set_chosen_gk.add(all)
                set_chosen_gk_label.add(x.text())
        for all in k5_beschreibung:
            x = eval("self.cb_k5_cr_" + all + "_cr")
            if x.isChecked() == True:
                set_chosen_gk.add(all)
                set_chosen_gk_label.add(all.upper() + "(5)")
        for all in k6_beschreibung:
            x = eval("self.cb_k6_cr_" + all + "_cr")
            if x.isChecked() == True:
                set_chosen_gk.add(all)
                set_chosen_gk_label.add(all.upper() + "(6)")
        for all in k7_beschreibung:
            x = eval("self.cb_k7_cr_" + all + "_cr")
            if x.isChecked() == True:
                set_chosen_gk.add(all)
                set_chosen_gk_label.add(all.upper() + "(7)")
        for all in k8_beschreibung:
            x = eval("self.cb_k8_cr_" + all + "_cr")
            if x.isChecked() == True:
                set_chosen_gk.add(all)
                set_chosen_gk_label.add(all.upper() + "(8)")

        x = ", ".join(sorted(set_chosen_gk_label))
        self.label_ausgew_gk.setText(_translate("MainWindow", str(x), None))

    def warning_window(self, text, detailed_text="", titel="Warnung"):
        QtWidgets.QApplication.restoreOverrideCursor()
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(titel)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowIcon(QtGui.QIcon(logo_path))
        msg.setText(text)
        msg.setInformativeText(detailed_text)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def save_file(self):
        self.creator_mode = "user"
        local_save = False

        ########################### WARNINGS #####
        ######################################

        if set_chosen_gk == set([]):
            self.warning_window("Es wurden keine Grundkompetenzen zugewiesen.")
            return

        if self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
            if self.comboBox_af.currentText() == "bitte auswählen":
                self.warning_window("Es wurde kein Aufgabenformat ausgewählt.")
                return

            if len(set_chosen_gk) > 1:
                self.warning_window("Es wurden zu viele Grundkompetenzen zugewiesen.")
                return

        if self.lineEdit_titel.text() == "":
            self.warning_window("Bitte geben Sie einen Titel ein.")
            return

        if self.plainTextEdit.toPlainText() == "":
            self.warning_window(
                'Bitte geben Sie den LaTeX-Quelltext der Aufgabe im Bereich "Aufgabeneingabe" ein.'
            )
            return
        if self.lineEdit_quelle.text() == "":
            self.warning_window("Bitte geben Sie die Quelle an.")
            return

        textBox_Entry = self.plainTextEdit.toPlainText()
        list_chosen_gk = list(set_chosen_gk)

        ####### CHECK INCL. & ATTACHED IMAGE RATIO ####

        if textBox_Entry.count("\includegraphics") > len(dict_picture_path):
            self.warning_window(
                "Es sind zu wenige Bilder angehängt ("
                + str(len(dict_picture_path))
                + "/"
                + str(textBox_Entry.count("\includegraphics"))
                + ")."
            )
            return
        if textBox_Entry.count("\includegraphics") < len(dict_picture_path):
            self.warning_window(
                "Es sind zu viele Bilder angehängt ("
                + str(len(dict_picture_path))
                + "/"
                + str(textBox_Entry.count("\includegraphics"))
                + ")."
            )
            return

        ###############################
        ###### Check if Admin Mode is activated ####

        if self.lineEdit_titel.text().startswith("###"):
            try:
                x, y = self.lineEdit_titel.text().split("### ")
            except ValueError:
                x, y = self.lineEdit_titel.text().split("###")
            self.creator_mode = "admin"
            edit_titel = y
        else:
            edit_titel = self.lineEdit_titel.text()
        ################################################

        QtWidgets.QApplication.restoreOverrideCursor()
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowIcon(QtGui.QIcon(logo_path))

        if len(list_chosen_gk) > 1:
            temp_list_chosen_gk = []
            for all in list_chosen_gk:
                if all in {
                    **k5_beschreibung,
                    **k6_beschreibung,
                    **k7_beschreibung,
                    **k8_beschreibung,
                }:
                    temp_list_chosen_gk.append(all.upper())
                else:
                    temp_list_chosen_gk.append(dict_gk[all])
            # print(temp_list_chosen_gk)
            gk = ", ".join(sorted(temp_list_chosen_gk))
        else:
            if list_chosen_gk[0] in {
                **k5_beschreibung,
                **k6_beschreibung,
                **k7_beschreibung,
                **k8_beschreibung,
            }:
                gk = list_chosen_gk[0].upper()

            else:
                gk = dict_gk[list_chosen_gk[0]]

        if dict_picture_path != {}:
            bilder = ", ".join(dict_picture_path)
        else:
            bilder = "-"

        if self.creator_mode == "user":
            local_save = False
            if self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
                aufgabenformat = "Aufgabenformat: %s\n" % self.comboBox_af.currentText()
            else:
                aufgabenformat = ""
            msg.setWindowTitle("Aufgabe speichern")
            msg.setText(
                "Sind Sie sicher, dass Sie die folgendene Aufgabe speichern wollen?\n\n"
                "Aufgabentyp: {0}\n"
                "Titel: {1}\n{2}"
                "Grundkompetenz: {3}\n"
                "Quelle: {4}\n"
                "Bilder: {5}\n".format(
                    self.comboBox_aufgabentyp_cr.currentText(),
                    edit_titel,
                    aufgabenformat,
                    gk,
                    self.lineEdit_quelle.text(),
                    bilder,
                )
            )
            # msg.setInformativeText('Soll die PDF Datei erstellt werden?')
            self.cb_confirm = QtWidgets.QCheckBox(
                "Hiermit bestätige ich, dass ich die eingegebene Aufgabe eigenständig\nund unter Berücksichtigung des Urheberrechtsgesetzes verfasst habe.\n"
                "Ich stelle die eingegebene Aufgabe frei gemäß der Lizenz CC0 1.0 zur Verfügung.\nDie Aufgabe darf daher zu jeder Zeit frei verwendet, kopiert und verändert werden."
            )
            self.cb_confirm.setObjectName(_fromUtf8("cb_confirm"))
            msg.setCheckBox(self.cb_confirm)
            msg.setStandardButtons(
                QtWidgets.QMessageBox.Yes
                | QtWidgets.QMessageBox.Apply
                | QtWidgets.QMessageBox.No
            )
            buttonY = msg.button(QtWidgets.QMessageBox.Yes)
            buttonY.setText("Speichern")
            msg.setDefaultButton(QtWidgets.QMessageBox.Yes)
            button_personal = msg.button(QtWidgets.QMessageBox.Apply)
            button_personal.setText("Lokal speichern")
            buttonN = msg.button(QtWidgets.QMessageBox.No)
            buttonN.setText("Abbrechen")
            ret = msg.exec_()

            if ret == QtWidgets.QMessageBox.Yes:
                while self.cb_confirm.isChecked() == False:
                    if ret == QtWidgets.QMessageBox.No:
                        return
                    else:
                        self.warning_window(
                            "Bitte bestätigen Sie die Eigenständigkeitserklärung und Lizenzvereinbarung."
                        )
                        ret = msg.exec_()
            elif ret == QtWidgets.QMessageBox.Apply:
                msg_personal = QtWidgets.QMessageBox()
                msg_personal.setWindowTitle("Aufgabe lokal speichern")
                msg_personal.setIcon(QtWidgets.QMessageBox.Warning)
                msg_personal.setWindowIcon(QtGui.QIcon(logo_path))
                msg_personal.setText(
                    "Sind Sie sicher, dass Sie diese Aufgabe nur lokal in Ihrer Dropbox speichern wollen?\n"
                )
                msg_personal.setInformativeText(
                    "ACHTUNG: Durch nicht überprüfte Aufgaben können Fehler entstehen, die das Programm zum Absturz bringen!"
                )
                msg_personal.setStandardButtons(
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
                )
                buttonY_personal = msg_personal.button(QtWidgets.QMessageBox.Yes)
                buttonY_personal.setText("Ja")
                buttonN_personal = msg_personal.button(QtWidgets.QMessageBox.No)
                buttonN_personal.setText("Nein")
                msg_personal.setDefaultButton(QtWidgets.QMessageBox.No)
                ret_personal = msg_personal.exec_()

                if ret_personal == QtWidgets.QMessageBox.Yes:
                    local_save = True
                    # self.comboBox_aufgabentyp_cr.currentText()=='Typ 1':

                    # 	if os.path
                    # try:
                    # 	# with open(titlepage_save, 'w+',encoding='utf8') as f:
                    # 	#	json.dump(self.dict_titlepage, f,ensure_ascii=False)
                    # except FileNotFoundError:
                    # 	os.makedirs(os.path.join(path_programm,'Lokaler Ordner'))
                    # 	# with open(titlepage_save, 'w+',encoding='utf8') as f:
                    # 	#	json.dump(self.dict_titlepage, f,ensure_ascii=False)
                if ret_personal == QtWidgets.QMessageBox.No:
                    # ret=msg.exec_()
                    return
            else:
                return

        if self.creator_mode == "admin":
            if self.comboBox_aufgabentyp_cr.currentText() == "Typ 1":
                aufgabenformat = "Aufgabenformat: %s\n" % self.comboBox_af.currentText()
            else:
                aufgabenformat = ""
            msg.setWindowTitle("Admin Modus - Aufgabe speichern")
            msg.setText(
                "Sind Sie sicher, dass Sie die folgendene Aufgabe speichern wollen?\n\n"
                "Aufgabentyp: {0}\n"
                "Titel: {1}\n{2}"
                "Grundkompetenz: {3}\n"
                "Quelle: {4}\n"
                "Bilder: {5}\n".format(
                    self.comboBox_aufgabentyp_cr.currentText(),
                    edit_titel,
                    aufgabenformat,
                    gk,
                    self.lineEdit_quelle.text(),
                    bilder,
                )
            )
            self.cb_save = QtWidgets.QCheckBox("inoffizielle Aufgabe")
            self.cb_save.setObjectName(_fromUtf8("cb_save"))
            self.cb_save.setChecked(True)
            msg.setCheckBox(self.cb_save)

            msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            buttonY = msg.button(QtWidgets.QMessageBox.Yes)
            buttonY.setText("Speichern")
            msg.setDefaultButton(QtWidgets.QMessageBox.Yes)
            buttonN = msg.button(QtWidgets.QMessageBox.No)
            buttonN.setText("Abbrechen")
            ret = msg.exec_()

            if ret == QtWidgets.QMessageBox.Yes:
                pass
            else:
                return

        ##### GET MAX FILENUMBER IN DIR #####
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

        ####### Checks files in 'Beispieleinreichung' #####
        ##################################################

        if local_save == True:
            pass
        else:
            try:
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
            if self.creator_mode == "admin" and self.cb_save.isChecked() == False:
                str_image_path = "../_database/Bilder/"
            if local_save == True:
                str_image_path = "../Lokaler_Ordner/Bilder/"
            else:
                str_image_path = "../Beispieleinreichung/Bilder/"

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

        # copy_image_path=os.path.join(path_programm,'_database','Bilder') ### direct save
        if self.creator_mode == "admin":
            if self.cb_save.isChecked() == False:
                copy_image_path = os.path.join(
                    path_programm, "_database", "Bilder"
                )  ### direct save
            if self.cb_save.isChecked() == True:
                copy_image_path = os.path.join(
                    path_programm, "_database_inoffiziell", "Bilder"
                )  ### direct save

        if local_save == True:
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

        if " - " in edit_titel:
            edit_titel = edit_titel.replace(" - ", "-")

        if " - " in self.lineEdit_quelle.text():
            quelle = self.lineEdit_quelle.text().replace(" - ", "-")
        else:
            quelle = self.lineEdit_quelle.text()

        if local_save == True:
            local = "*Privat* "
        else:
            local = ""
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
            x = ", ".join(dict_picture_path)
        else:
            x = "-"

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
        msg.setWindowTitle("Admin Modus - Aufgabe erfolgreich gespeichert")
        msg.setWindowIcon(QtGui.QIcon(logo_path))
        if local_save == True:
            msg.setText(
                'Die Typ{0}-Aufgabe mit dem Titel\n\n"{1}"\n\nwurde lokal auf ihrem System gespeichert.'.format(
                    chosen_typ, edit_titel
                )
            )
        else:
            msg.setText(
                'Die Typ{0}-Aufgabe mit dem Titel\n\n"{1}"\n\nwurde gespeichert.'.format(
                    chosen_typ, edit_titel
                )
            )

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
                x,
            )
        )
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        retval = msg.exec_()
        self.suchfenster_reset()

    ##################################################################
    ################## Befehle LAMA SAGE################################

    def sage_load(self, external_file_loaded):
        global list_sage_examples
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

        self.neue_schularbeit_erstellen()
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        for example in list_sage_examples:
            self.btn_delete_pressed(example, True)

        with open(self.saved_file_path, "r", encoding="utf8") as loaded_file:
            self.dict_list_input_examples = json.load(loaded_file)

        list_sage_examples = self.dict_list_input_examples["list_examples"]

        for all in list_sage_examples:
            if any(all in s for s in self.beispieldaten_dateipfad_1.values()):
                pass
            else:
                if any(all in s for s in self.beispieldaten_dateipfad_2.values()):
                    pass
                else:
                    self.warning_window(
                        'Die Aufgabe "{}" konnte nicht in der Datenbank gefunden werden. \n\n\n (Tipp: Refresh Database)'.format(
                            all
                        )
                    )
                    return

        for all in list_sage_examples:
            if re.search("[A-Z]", all) == None:
                bsp_string = all
            else:
                bsp_string = all.replace(" ", "").replace(".", "").replace("-", "_")
            # print(bsp_string)
            exec(
                'self.list_input_{0}=self.dict_list_input_examples["self.list_input_{0}"]'.format(
                    bsp_string
                )
            )
        self.spinBox_nummer.setValue(self.dict_list_input_examples["data_gesamt"]["#"])
        self.lineEdit_klasse.setText(
            self.dict_list_input_examples["data_gesamt"]["Klasse"]
        )

        try:
            index = self.comboBox_pruefungstyp.findText(
                self.dict_list_input_examples["data_gesamt"]["Pruefungstyp"],
                QtCore.Qt.MatchFixedString,
            )
        except KeyError:
            index = 0
        if index >= 0:
            self.comboBox_pruefungstyp.setCurrentIndex(index)

        if self.dict_list_input_examples["data_gesamt"]["Beurteilung"] == "ns":
            self.radioButton_notenschl.setChecked(True)
            self.radioButton_beurteilungsraster.setChecked(False)
        if self.dict_list_input_examples["data_gesamt"]["Beurteilung"] == "br":
            self.radioButton_notenschl.setChecked(False)
            self.radioButton_beurteilungsraster.setChecked(True)

        year = self.dict_list_input_examples["data_gesamt"]["Datum"][0]
        month = self.dict_list_input_examples["data_gesamt"]["Datum"][1]
        day = self.dict_list_input_examples["data_gesamt"]["Datum"][2]
        self.dateEdit.setDate(QtCore.QDate(year, month, day))

        self.dict_sage_ausgleichspunkte_chosen = self.dict_list_input_examples[
            "dict_ausgleichspunkte"
        ]

        self.sage_aufgabe_create(True)
        self.spinBox_default_pkt.setValue(
            self.dict_list_input_examples["data_gesamt"]["Typ1 Standard"]
        )
        self.spinBox_2.setValue(
            self.dict_list_input_examples["data_gesamt"]["Notenschluessel"][0]
        )
        self.spinBox_3.setValue(
            self.dict_list_input_examples["data_gesamt"]["Notenschluessel"][1]
        )
        self.spinBox_4.setValue(
            self.dict_list_input_examples["data_gesamt"]["Notenschluessel"][2]
        )
        self.spinBox_5.setValue(
            self.dict_list_input_examples["data_gesamt"]["Notenschluessel"][3]
        )

        QtWidgets.QApplication.restoreOverrideCursor()

    def sage_save(self, path_file):  # path_file
        try:
            self.saved_file_path
        except AttributeError:
            self.saved_file_path = path_programm

        if path_file == "":
            path_backup_file = QtWidgets.QFileDialog.getSaveFileName(
                None,
                "Speichern unter",
                self.saved_file_path,
                "LaMA Datei (*.lama);; Alle Dateien (*.*)",
            )
            if path_backup_file[0] == "":
                return
            self.save_dict_examples_data()
            save_file = path_backup_file[0]

        else:
            name, extension = os.path.splitext(path_file)
            path_file = name + "_autosave.lama"
            save_file = path_file
        try:
            self.neue_schularbeit_erstellen()
        except AttributeError:
            pass

        self.saved_file_path = save_file

        with open(save_file, "w+", encoding="utf8") as saved_file:
            json.dump(self.dict_list_input_examples, saved_file, ensure_ascii=False)

    def titlepage_clicked(self, dict_titlepage):

        self.Dialog = QtWidgets.QDialog(
            None,
            QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint,
        )
        self.ui = Ui_Dialog_titlepage()
        self.ui.setupUi(self.Dialog, dict_titlepage)
        self.Dialog.show()
        self.Dialog.exec_()
        self.dict_titlepage = dict_titlepage

        titlepage_save = os.path.join(path_programm, "Teildokument", "titlepage_save")

        try:
            with open(titlepage_save, "w+", encoding="utf8") as f:
                json.dump(self.dict_titlepage, f, ensure_ascii=False)
        except FileNotFoundError:
            os.makedirs(os.path.join(path_programm, "Teildokument"))
            with open(titlepage_save, "w+", encoding="utf8") as f:
                json.dump(self.dict_titlepage, f, ensure_ascii=False)

        # print(self.dict_titlepage)

        # QtWidgets.QApplication.restoreOverrideCursor()
        # msg = QtWidgets.QMessageBox()
        # msg.setIcon(QtWidgets.QMessageBox.Question)
        # msg.setWindowIcon(QtGui.QIcon(logo_path))
        # msg.setWindowTitle("Titelblatt anpassen")
        # msg.setText('Wählen Sie die gewünschten Punkte für das Titelblatt aus:')
        # self.cb_titlepage_title= QtWidgets.QCheckBox("Titel")
        # self.cb_titlepage_title.setObjectName(_fromUtf8("cb_titlepage_titel"))
        # msg.setCheckBox(self.cb_titlepage_title)
        # self.cb_titlepage_datum= QtWidgets.QCheckBox("Datum")
        # self.cb_titlepage_datum.setObjectName(_fromUtf8("cb_titlepage_datum"))
        # msg.setCheckBox(self.cb_titlepage_datum)

        # msg.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        # buttonY = msg.button(QtWidgets.QMessageBox.Yes)
        # buttonY.setText('Speichern')
        # msg.setDefaultButton(QtWidgets.QMessageBox.Yes)
        # buttonN = msg.button(QtWidgets.QMessageBox.No)
        # buttonN.setText('Standard wieder herstellen')
        # msg.exec_()

    def beurteilungsraster_changed(self):
        if self.radioButton_beurteilungsraster.isChecked():
            self.groupBox_notenschl.hide()
            self.gridLayout_5.addWidget(self.groupBox_beurteilungsra, 6, 0, 1, 7)
            self.save_dict_examples_data()
            self.label_typ1_pkt.setText(
                _translate("MainWindow", "Punkte Typ 1: {}".format(self.pkt_typ1), None)
            )
            self.label_typ2_pkt.setText(
                _translate("MainWindow", "Punkte Typ 2: {}".format(self.pkt_typ2), None)
            )
            self.label_ausgleich_pkt.setText(
                _translate(
                    "MainWindow",
                    "(davon Ausgleichspunkte: {})".format(
                        self.num_ausgleichspkt_gesamt
                    ),
                    None,
                )
            )
            self.groupBox_beurteilungsra.show()

        if self.radioButton_notenschl.isChecked():
            self.gridLayout_5.removeWidget(self.groupBox_beurteilungsra)
            self.groupBox_beurteilungsra.hide()
            self.groupBox_notenschl.show()

    def sage_aufgabe_add(self, typ, aufgabe):
        # print(aufgabe)
        list_sage_examples_typ1 = []
        list_sage_examples_typ2 = []

        for all in list_sage_examples:
            if re.search("[A-Z]", all) == None:
                list_sage_examples_typ2.append(all)
            else:
                list_sage_examples_typ1.append(all)

        if aufgabe not in list_sage_examples:
            if typ == 1:
                list_sage_examples_typ1.append(aufgabe)
            if typ == 2:
                list_sage_examples_typ2.append(aufgabe)

        list_sage_examples.clear()
        list_sage_examples.extend(list_sage_examples_typ1)
        list_sage_examples.extend(list_sage_examples_typ2)
        num_typ1 = len(list_sage_examples_typ1)
        num_typ2 = len(list_sage_examples_typ2)
        num_total = len(list_sage_examples)
        self.label_gesamtbeispiele.setText(
            _translate(
                "MainWindow",
                "Anzahl der Aufgaben: {0} (Typ1: {1} / Typ2: {2})  ".format(
                    num_total, num_typ1, num_typ2
                ),
                None,
            )
        )
        self.sage_aufgabe_create(False)

    def adapt_label_gesamtbeispiele(self):
        list_sage_examples_typ1 = []
        list_sage_examples_typ2 = []

        for all in list_sage_examples:
            if re.search("[A-Z]", all) == None:
                list_sage_examples_typ2.append(all)
            else:
                list_sage_examples_typ1.append(all)

        list_sage_examples.clear()
        list_sage_examples.extend(list_sage_examples_typ1)
        list_sage_examples.extend(list_sage_examples_typ2)
        num_typ1 = len(list_sage_examples_typ1)
        num_typ2 = len(list_sage_examples_typ2)
        num_total = len(list_sage_examples)
        self.label_gesamtbeispiele.setText(
            _translate(
                "MainWindow",
                "Anzahl der Aufgaben: {0} (Typ1: {1} / Typ2: {2})  ".format(
                    num_total, num_typ1, num_typ2
                ),
                None,
            )
        )

    def btn_up_pressed(self, aufgabe):
        self.update_lists_examples()
        temp_aufgabe = aufgabe.replace("_L_", "")
        if re.search("[A-Z]", temp_aufgabe) == None:
            bsp_string = aufgabe
            typ = 2
        else:
            bsp_string = aufgabe.replace(" ", "").replace(".", "").replace("-", "_")
            typ = 1

        list_input = eval("self.list_input_{}".format(bsp_string))
        sb_value = eval("self.spinBox_pkt_{}".format(bsp_string))
        list_input[0] = sb_value.value()

        space_value = eval("self.spinBox_abstand_{}".format(bsp_string))
        list_input[1] = space_value.value()

        # if position!=0:
        a, b = list_sage_examples.index(aufgabe), list_sage_examples.index(aufgabe) - 1
        list_sage_examples[a], list_sage_examples[b] = (
            list_sage_examples[b],
            list_sage_examples[a],
        )

        self.sage_aufgabe_create(False)

    def btn_down_pressed(self, aufgabe):
        self.update_lists_examples()
        temp_aufgabe = aufgabe.replace("_L_", "")
        if re.search("[A-Z]", temp_aufgabe) == None:
            bsp_string = aufgabe
            typ = 2
        else:
            bsp_string = aufgabe.replace(" ", "").replace(".", "").replace("-", "_")

            typ = 1

        # number=list_sage_examples.index(aufgabe)
        list_input = eval("self.list_input_{}".format(bsp_string))
        sb_value = eval("self.spinBox_pkt_{}".format(bsp_string))
        # print(list_input)
        # print(sb_value.value())
        list_input[0] = sb_value.value()

        space_value = eval("self.spinBox_abstand_{}".format(bsp_string))
        list_input[1] = space_value.value()

        # if (typ==1 and position!=len(list_sage_examples_typ1)-1) or (typ==2 and position!=len(list_sage_examples_typ2)-1):
        a, b = list_sage_examples.index(aufgabe), list_sage_examples.index(aufgabe) + 1
        list_sage_examples[a], list_sage_examples[b] = (
            list_sage_examples[b],
            list_sage_examples[a],
        )
        self.sage_aufgabe_create(False)

    def btn_delete_pressed(self, aufgabe, file_loaded):
        temp_aufgabe = aufgabe.replace("_L_", "")
        if re.search("[A-Z]", temp_aufgabe) == None:
            bsp_string = aufgabe
            typ = 2
        else:
            bsp_string = aufgabe.replace(" ", "").replace(".", "").replace("-", "_")
            typ = 1

        exec("self.groupBox_bsp_{}.setParent(None)".format(bsp_string))
        list_input = eval("self.list_input_{}".format(bsp_string))
        spinBox_pkt = eval("self.spinBox_pkt_{}".format(bsp_string))
        if typ == 1:
            list_input[0] = self.spinBox_default_pkt.value()
            spinBox_pkt.setValue(self.spinBox_default_pkt.value())
        if typ == 2:
            list_input[0] = 0
            list_input[3] = ""
            ausgleich_pkt = eval("self.ausgleich_pkt_{}".format(bsp_string))
            self.num_ausgleichspkt_gesamt -= int(ausgleich_pkt.text()[-2])
            spinBox_pkt.setValue(0)
            name = aufgabe + ".tex"
            for path in self.beispieldaten_dateipfad_2.values():
                if name == os.path.basename(path):
                    selected_path = path
            try:
                # del self.dict_sage_ausgleichspunkte_chosen[selected_path]
                del self.dict_sage_ausgleichspunkte_chosen[aufgabe]
            except KeyError:
                pass

        list_input[1] = 0

        spinBox_abstand = eval("self.spinBox_abstand_{}".format(bsp_string))
        spinBox_abstand.setValue(0)

        if file_loaded == False:
            list_sage_examples.remove(aufgabe)
            self.adapt_label_gesamtbeispiele()
            self.sage_aufgabe_create(False)

        ### reset Ausgleichspunkte
        # del self.dict_sage_ausgleichspunkte_chosen[aufgabe]
        # print(self.dict_sage_ausgleichspunkte_chosen)
        # print(aufgabe)

    def punkte_changed(self):
        gesamtpunkte = 0

        for all in list_sage_examples:
            temp_all = all.replace("_L_", "")
            if re.search("[A-Z]", temp_all) == None:
                bsp_string = all
            else:
                bsp_string = all.replace(" ", "").replace(".", "").replace("-", "_")

            spinBox_pkt = eval("self.spinBox_pkt_{}".format(bsp_string))
            punkte = spinBox_pkt.value()
            spinBox_abstand = eval("self.spinBox_abstand_{}".format(bsp_string))
            abstand = spinBox_abstand.value()
            list_input = eval("self.list_input_{}".format(bsp_string))
            list_input[0] = punkte
            list_input[1] = abstand
            gesamtpunkte += punkte

        # gesamtpunkte+=self.num_ausgleichspkt_gesamt
        # ausgleich_pkt = eval('self.ausgleich_pkt_{}'.format(bsp_string))

        # ausgleich_pkt.setText(_translate("MainWindow", '(AP: {})'.format(len(list_sage_ausgleichspunkte_chosen)),None))

        list_punkte = []
        for g in range(2, 6):
            r = 0
            x = eval("self.spinBox_{}.value()".format(g))
            if gesamtpunkte * x / 100 == int(gesamtpunkte * x / 100):
                list_punkte.append(int(gesamtpunkte * (x / 100)))
            else:
                list_punkte.append(int(gesamtpunkte * (x / 100)) + 1)
            r += 1

        self.label_sg_pkt.setText(
            _translate("MainWindow", "% (ab {})".format(list_punkte[0]), None)
        )
        self.label_g_pkt.setText(
            _translate("MainWindow", "% (ab {})".format(list_punkte[1]), None)
        )
        self.label_b_pkt.setText(
            _translate("MainWindow", "% (ab {})".format(list_punkte[2]), None)
        )
        self.label_g_pkt_2.setText(
            _translate("MainWindow", "% (ab {})".format(list_punkte[3]), None)
        )
        # self.label_ng_pkt.setText(_translate("MainWindow",	 "% (<{})".format(pkt_ge),None))

        self.label_gesamtpunkte.setText(
            _translate("MainWindow", "Gesamtpunkte: %i" % gesamtpunkte, None)
        )
        self.beurteilungsraster_changed()

    def update_default_pkt(self):
        for all in list_sage_examples:
            if re.search("[A-Z]", all) == None:
                pass
                # ausgleich_pkt = eval('self.ausgleich_pkt_{}'.format(all))
                # ausgleich_pkt.setText(_translate("MainWindow", '(AP: {})'.format(len(list_sage_ausgleichspunkte_chosen)*self.spinBox_default_pkt.value()),None))
            else:
                bsp_string = all.replace(" ", "").replace(".", "").replace("-", "_")
                sb_value = eval("self.spinBox_pkt_{}".format(bsp_string))
                sb_value.setValue(self.spinBox_default_pkt.value())
                self.beurteilungsraster_changed()

    def update_lists_examples(self):
        for all in list_sage_examples:
            temp_all = all.replace("_L_", "")
            if re.search("[A-Z]", temp_all) == None:
                bsp_string = all
                typ = 2
            else:
                bsp_string = all.replace(" ", "").replace(".", "").replace("-", "_")
                typ = 1

            try:
                list_input = eval("self.list_input_{}".format(bsp_string))
                sb_value = eval("self.spinBox_pkt_{}".format(bsp_string))
                list_input[0] = sb_value.value()
                space_value = eval("self.spinBox_abstand_{}".format(bsp_string))
                list_input[1] = space_value.value()
            except AttributeError:
                if typ == 1:
                    exec(
                        'self.list_input_{0}=[{1},0,"",""]'.format(
                            bsp_string, self.spinBox_default_pkt.value()
                        )
                    )
                if typ == 2:
                    exec('self.list_input_{}=[0,0,"",""]'.format(bsp_string))
                list_input = eval("self.list_input_{}".format(bsp_string))
            # print(list_input)

    def sage_aufgabe_create(self, file_loaded):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.num_ausgleichspkt_gesamt = 0
        r = 0
        scrollBar_position = self.scrollArea_chosen.verticalScrollBar().value()

        for all in list_sage_examples:
            if re.search("[A-Z]", all) == None:
                bsp_string = all
            else:
                bsp_string = all.replace(" ", "").replace(".", "").replace("-", "_")

            try:
                exec("self.groupBox_bsp_{}.setParent(None)".format(bsp_string))
            except AttributeError:
                pass

        if file_loaded == False:
            self.update_lists_examples()

        for example in list_sage_examples:
            temp_example = example.replace("_L_", "")
            if re.search("[A-Z]", temp_example) == None:
                bsp_string = example
            else:
                bsp_string = example.replace(" ", "").replace(".", "").replace("-", "_")
            list_input = eval("self.list_input_{}".format(bsp_string))
            name = example + ".tex"
            for all in self.beispieldaten_dateipfad_1:
                filename = os.path.basename(self.beispieldaten_dateipfad_1[all])
                if name == filename:
                    x = all.split(" - ")
                    # print(x[-2])
                    list_input[2] = x[-3]
                    list_input[3] = x[-2]

            for all in self.beispieldaten_dateipfad_2:
                filename = os.path.basename(self.beispieldaten_dateipfad_2[all])
                if name == filename:
                    x = all.split(" - ")
                    list_input[2] = x[-2]

        if file_loaded == False:
            self.list_copy_images = []
            self.save_dict_examples_data()
        if file_loaded == True:
            try:
                self.list_copy_images
            except AttributeError:
                self.list_copy_images = []
        counter = 0
        num_of_example = 1

        for all in list_sage_examples:
            temp_all = all.replace("_L_", "")
            if re.search("[A-Z]", temp_all) == None:
                bsp_string = all
                typ = 2
            else:
                bsp_string = all.replace(" ", "").replace(".", "").replace("-", "_")
                typ = 1
            list_input = eval("self.list_input_{}".format(bsp_string))
            exec(
                "self.groupBox_bsp_{} = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)".format(
                    bsp_string
                )
            )
            x = eval("self.groupBox_bsp_{}".format(bsp_string))
            # x.setMaximumSize(QtCore.QSize(16777215, 200))
            x.setObjectName("groupBox_bsp_{}".format(bsp_string))
            if (list_sage_examples.index(all) % 2) == 0 and typ == 1:
                x.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
            if typ == 2:
                x.setStyleSheet(_fromUtf8("background-color: rgb(255, 212, 212);"))
            x.setTitle(
                _translate(
                    "MainWindow",
                    "{0}. Aufgabe (Typ{1})".format(str(num_of_example), str(typ)),
                    None,
                )
            )
            self.gridLayout_gB = QtWidgets.QGridLayout(x)
            self.gridLayout_gB.setObjectName("gridLayout_gB")
            self.gridLayout_8.addWidget(x, 0, 0, 1, 2, QtCore.Qt.AlignTop)

            exec("self.label_aufgabe_{} = QtWidgets.QLabel(x)".format(bsp_string))
            label_aufgabe = eval("self.label_aufgabe_{}".format(bsp_string))
            label_aufgabe.setWordWrap(True)
            label_aufgabe.setObjectName("label_aufgabe_{}".format(bsp_string))
            self.gridLayout_gB.addWidget(label_aufgabe, 0, 0, 1, 1)

            if typ == 1:
                try:
                    aufgabenformat = (
                        "(" + dict_aufgabenformate[list_input[3].lower()] + ")"
                    )
                except KeyError:
                    aufgabenformat = ""

                label_aufgabe.setText(
                    _translate(
                        "MainWindow", "{0} {1}".format(all, aufgabenformat), None
                    )
                )
            if typ == 2:
                label_aufgabe.setText(_translate("MainWindow", "{0}".format(all), None))

            exec("self.label_title_{} = QtWidgets.QLabel(x)".format(bsp_string))
            label_title = eval("self.label_title_{}".format(bsp_string))
            label_title.setWordWrap(True)
            label_title.setObjectName("label_title_{}".format(bsp_string))
            self.gridLayout_gB.addWidget(label_title, 1, 0, 1, 1)
            label_title.setText(
                _translate("MainWindow", "Titel: {}".format(list_input[2]), None)
            )  # list_titles[i-1]

            self.groupBox_pkt = QtWidgets.QGroupBox(x)
            # self.groupBox_pkt.setMaximumSize(QtCore.QSize(83, 53))
            self.groupBox_pkt.setObjectName("groupBox_pkt")
            self.groupBox_pkt.setTitle(_translate("MainWindow", "Punkte", None))
            if typ == 1:
                self.groupBox_pkt.setMaximumSize(QtCore.QSize(80, 16777215))
            if typ == 2:
                self.groupBox_pkt.setToolTip(
                    "Die Punkte stehen für die Gesamtpunkte dieser Aufgabe.\nEs müssen daher auch die Ausgleichspunkte berücksichtigt werden."
                )
                self.groupBox_pkt.setMaximumSize(QtCore.QSize(150, 16777215))
            self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_pkt)
            self.gridLayout_3.setObjectName("gridLayout_3")
            self.gridLayout_gB.addWidget(self.groupBox_pkt, 0, 1, 2, 1)

            exec(
                "self.spinBox_pkt_{} = SpinBox_noWheel(self.groupBox_pkt)".format(
                    bsp_string
                )
            )
            spinBox_pkt = eval("self.spinBox_pkt_{}".format(bsp_string))
            spinBox_pkt.setObjectName("spinBox_pkt_{}".format(bsp_string))
            spinBox_pkt.setValue(eval("self.list_input_{}".format(bsp_string))[0])
            spinBox_pkt.valueChanged.connect(self.punkte_changed)
            self.gridLayout_3.addWidget(spinBox_pkt, 0, 0, 1, 1)

            self.pushButton_up = QtWidgets.QPushButton(x)
            self.pushButton_up.setObjectName("pushButton_up")
            self.pushButton_up.setMaximumSize(QtCore.QSize(30, 30))
            self.pushButton_up.setFocusPolicy(QtCore.Qt.ClickFocus)
            self.gridLayout_gB.addWidget(self.pushButton_up, 0, 3, 2, 1)
            self.pushButton_up.setStyleSheet(_fromUtf8("background-color: light gray"))
            self.pushButton_up.setIcon(
                QtWidgets.QApplication.style().standardIcon(QtWidgets.QStyle.SP_ArrowUp)
            )
            if num_of_example == 1:
                self.pushButton_up.setEnabled(False)
            if typ == 2 and counter == 0:
                self.pushButton_up.setEnabled(False)
                counter += 1
            self.pushButton_up.clicked.connect(partial(self.btn_up_pressed, all))

            self.pushButton_down = QtWidgets.QPushButton(x)
            self.pushButton_down.setObjectName("pushButton_down")
            self.pushButton_down.setStyleSheet(
                _fromUtf8("background-color: light gray")
            )
            self.pushButton_down.setMaximumSize(QtCore.QSize(30, 30))
            self.pushButton_down.setFocusPolicy(QtCore.Qt.ClickFocus)
            self.gridLayout_gB.addWidget(self.pushButton_down, 0, 4, 2, 1)
            self.pushButton_down.setIcon(
                QtWidgets.QApplication.style().standardIcon(
                    QtWidgets.QStyle.SP_ArrowDown
                )
            )
            if num_of_example == len(list_sage_examples):
                self.pushButton_down.setEnabled(False)
            if (
                typ == 1
                and self.dict_list_input_examples["data_gesamt"]["num_1"]
                == num_of_example
            ):
                self.pushButton_down.setEnabled(False)
            self.pushButton_down.clicked.connect(partial(self.btn_down_pressed, all))

            self.pushButton_delete = QtWidgets.QPushButton(x)
            self.pushButton_delete.setObjectName("pushButton_delete")
            self.pushButton_delete.setStyleSheet(
                _fromUtf8("background-color: light gray")
            )
            # self.pushButton_delete.setStyleSheet(_fromUtf8("background-color: rgb(255, 153, 153);"))
            self.pushButton_delete.setMaximumSize(QtCore.QSize(30, 30))
            self.pushButton_delete.setFocusPolicy(QtCore.Qt.ClickFocus)
            self.gridLayout_gB.addWidget(self.pushButton_delete, 0, 5, 2, 1)
            self.pushButton_delete.setIcon(
                QtWidgets.QApplication.style().standardIcon(
                    QtWidgets.QStyle.SP_TitleBarCloseButton
                )
            )
            self.pushButton_delete.clicked.connect(
                partial(self.btn_delete_pressed, all, False)
            )

            self.groupBox_abstand = QtWidgets.QGroupBox(x)
            self.groupBox_abstand.setObjectName("groupBox_abstand")
            self.groupBox_abstand.setTitle(
                _translate("MainWindow", "Abstand (cm)", None)
            )
            self.groupBox_abstand.setMaximumSize(QtCore.QSize(100, 16777215))
            self.groupBox_abstand.setToolTip("Neue Seite: Abstand=99")
            self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_abstand)
            # self.groupBox_abstand.setMaximumSize(QtCore.QSize(180, 152))
            if typ == 2:
                self.groupBox_abstand.hide()
            self.verticalLayout_3.setObjectName("verticalLayout_3")

            exec(
                "self.spinBox_abstand_{} = SpinBox_noWheel(self.groupBox_abstand)".format(
                    bsp_string
                )
            )
            spinBox_abstand = eval("self.spinBox_abstand_{}".format(bsp_string))
            spinBox_abstand.setObjectName("spinBox_abstand_{}".format(bsp_string))
            spinBox_abstand.setValue(eval("self.list_input_{}".format(bsp_string))[1])
            spinBox_abstand.valueChanged.connect(self.punkte_changed)
            self.verticalLayout_3.addWidget(spinBox_abstand)
            self.gridLayout_gB.addWidget(self.groupBox_abstand, 0, 2, 2, 1)

            self.pushButton_ausgleich = QtWidgets.QPushButton(x)
            self.pushButton_ausgleich.setObjectName("pushButton_ausgleich")
            self.pushButton_ausgleich.setStyleSheet(
                _fromUtf8("background-color: light gray")
            )
            # self.pushButton_delete.setStyleSheet(_fromUtf8("background-color: rgb(255, 153, 153);"))
            self.pushButton_ausgleich.setMaximumSize(QtCore.QSize(220, 30))
            self.pushButton_ausgleich.setText("Ausgleichspunkte anpassen...")
            self.pushButton_ausgleich.setFocusPolicy(QtCore.Qt.ClickFocus)
            if typ == 1:
                list_path = self.beispieldaten_dateipfad_1.values()
            if typ == 2:
                list_path = self.beispieldaten_dateipfad_2.values()
            name = all + ".tex"
            for path in list_path:
                if name == os.path.basename(path):
                    selected_path = path

            f = open(selected_path, "r", encoding="utf8")
            content = f.read()
            f.close()

            if "\\includegraphics" in content:
                matches = re.findall("/Bilder/(.+.eps)}", content)
                for image in matches:
                    self.list_copy_images.append(image)
            if typ == 2:
                try:
                    num_ausgleichspkt = int(list_input[3])
                except ValueError:
                    num_ausgleichspkt = content.count("\\fbox{A}")

                exec(
                    "self.ausgleich_pkt_{} = QtWidgets.QLabel(self.groupBox_pkt)".format(
                        bsp_string
                    )
                )
                ausgleich_pkt = eval("self.ausgleich_pkt_{}".format(bsp_string))
                ausgleich_pkt.setObjectName("ausgleich_pkt_{}".format(bsp_string))
                self.gridLayout_3.addWidget(ausgleich_pkt, 0, 1, 1, 1)
                list_input[3] = num_ausgleichspkt
                ausgleich_pkt.setText(
                    _translate("MainWindow", "(AP: {})".format(num_ausgleichspkt), None)
                )  ##*self.spinBox_default_pkt.value())
                self.num_ausgleichspkt_gesamt += num_ausgleichspkt
                list_input[3] = num_ausgleichspkt
                self.pushButton_ausgleich.clicked.connect(
                    partial(
                        self.pushButton_ausgleich_pressed, all, selected_path, content
                    )
                )

            self.gridLayout_gB.addWidget(self.pushButton_ausgleich, 0, 2, 2, 1)
            if typ == 1:
                self.pushButton_ausgleich.hide()

            MainWindow.setTabOrder(spinBox_pkt, spinBox_abstand)

            try:
                self.gridLayout_8.removeItem(self.spacerItem)
            except AttributeError:
                pass

            self.gridLayout_8.addWidget(x, r, 0, 1, 2, QtCore.Qt.AlignTop)

            self.spacerItem = QtWidgets.QSpacerItem(
                20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
            )
            self.gridLayout_8.addItem(self.spacerItem, r + 1, 0, 1, 2)

            r += 2

            # print(list_input)
            num_of_example += 1
            self.scrollArea_chosen.verticalScrollBar().setValue(scrollBar_position)
        # self.sum_up_ausgleich()

        self.punkte_changed()
        self.beurteilungsraster_changed()
        self.lineEdit_number.setText("")
        self.lineEdit_number.setFocus()
        QtWidgets.QApplication.restoreOverrideCursor()

    def pushButton_ausgleich_pressed(self, bsp_name, selected_typ2_path, content):

        x = re.split("Aufgabenstellung:}|Lösungserwartung:}", content)
        str_file = x[1].replace("\t", "")
        ausgleichspunkte_split_text = re.split("\n\n|\n\t", str_file)

        temp_list = []
        for all in ausgleichspunkte_split_text:
            x = ausgleichspunkte_split_text[
                ausgleichspunkte_split_text.index(all)
            ].split("\item ")
            for item in x:
                temp_list.append(item)
        ausgleichspunkte_split_text = temp_list
        # print(ausgleichspunkte_split_text)
        for all in ausgleichspunkte_split_text:
            if "\\begin{pspicture*}" in all:
                ausgleichspunkte_split_text[
                    ausgleichspunkte_split_text.index(all)
                ] = "[...] GRAFIK [...]"

        # print(ausgleichspunkte_split_text)
        # return
        for all in ausgleichspunkte_split_text:
            z = all.replace("\t", "")
            z = z.replace("\\leer", "")
            x = [
                line for line in z.split("\n") if line.strip() != ""
            ]  # delete all empty lines
            for item in x[:]:
                if "begin{" in item or "end{" in item:
                    if "tabular" in item or "tabu" in item:
                        pass
                    else:
                        x.remove(item)
            y = "\n".join(x)
            ausgleichspunkte_split_text[ausgleichspunkte_split_text.index(all)] = y

        for all in ausgleichspunkte_split_text[:]:
            if all == "":
                ausgleichspunkte_split_text.remove(all)

        # print(ausgleichspunkte_split_text)
        for all in reversed(ausgleichspunkte_split_text):
            if "\\antwort{" in all:
                index_end = ausgleichspunkte_split_text.index(all)
                break

        try:
            ausgleichspunkte_split_text = ausgleichspunkte_split_text[:index_end]
        except UnboundLocalError:
            self.warning_window(
                "Es ist ein Fehler bei der Auswahl der Ausgleichspunkte von Beispiel {} aufgetreten! (Das Beispiel kann dennoch verwendet und individuell in der TeX-Datei bearbeitet werden.)\n".format(
                    bsp_name
                ),
                'Bitte melden Sie den Fehler unter dem Abschnitt "Feedback & Fehler" an das LaMA-Team.',
            )
            return

        # for all in self.dict_sage_ausgleichspunkte_chosen[selected_typ2_path]:
        # 	print(all)
        # print(self.dict_sage_ausgleichspunkte_chosen)
        if bsp_name in self.dict_sage_ausgleichspunkte_chosen.keys():
            # print(self.dict_sage_ausgleichspunkte_chosen[selected_typ2_path])
            # return
            list_sage_ausgleichspunkte_chosen = self.dict_sage_ausgleichspunkte_chosen[
                bsp_name
            ]
        else:
            list_sage_ausgleichspunkte_chosen = []
            # print(ausgleichspunkte_split_text)
            for all in ausgleichspunkte_split_text:
                if "\\fbox{A}" in all:
                    x = all.replace("\\fbox{A}", "")
                    list_sage_ausgleichspunkte_chosen.append(x)

        self.Dialog = QtWidgets.QDialog(
            None,
            QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint,
        )
        self.ui = Ui_Dialog_ausgleichspunkte()
        self.ui.setupUi(
            self.Dialog, ausgleichspunkte_split_text, list_sage_ausgleichspunkte_chosen
        )
        self.Dialog.show()
        self.Dialog.exec_()
        # print(list_sage_ausgleichspunkte_chosen)
        self.dict_sage_ausgleichspunkte_chosen[
            bsp_name
        ] = list_sage_ausgleichspunkte_chosen
        temp_bsp_name = bsp_name.replace("_L_", "")
        if re.search("[A-Z]", temp_bsp_name) == None:
            bsp_string = bsp_name
        else:
            bsp_string = bsp_name.replace(" ", "").replace(".", "").replace("-", "_")
        list_input = eval("self.list_input_{}".format(bsp_string))
        list_input[3] = len(list_sage_ausgleichspunkte_chosen)

        # print(self.dict_sage_ausgleichspunkte_chosen)
        self.sage_aufgabe_create(False)

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
            index = 0
            for all in list_comboBox_gk:
                self.comboBox_gk.addItem("")
                self.comboBox_gk.setItemText(index, _translate("MainWindow", all, None))
                index += 1
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
        self.sage_aufgabe_add(
            int(self.comboBox_at_sage.currentText()[-1]), item.text().replace("*E-", "")
        )

    def nummer_clicked_fb(self, item):
        # print(item.text())
        self.label_example.setText(
            _translate(
                "MainWindow", "Ausgewählte Aufgabe: {}".format(item.text()), None
            )
        )

    def adapt_choosing_list(self, list_mode):
        if list_mode == "sage":
            listWidget = self.listWidget
        if list_mode == "feedback":
            listWidget = self.listWidget_fb

            if self.comboBox_at_fb.currentText() == "Allgemeine Rückmeldung":
                self.comboBox_fb.clear()
                self.comboBox_fb_num.clear()
                self.lineEdit_number_fb.clear()
                listWidget.clear()
                return

        listWidget.clear()

        log_file_1 = os.path.join(path_programm, "Teildokument", "log_file_1")
        try:
            with open(log_file_1, encoding="utf8") as f:
                beispieldaten_dateipfad_1 = json.load(f)
        except FileNotFoundError:
            self.refresh_ddb()  # 1
            with open(log_file_1, encoding="utf8") as f:
                beispieldaten_dateipfad_1 = json.load(f)

        self.beispieldaten_dateipfad_1 = beispieldaten_dateipfad_1

        log_file_2 = os.path.join(path_programm, "Teildokument", "log_file_2")
        try:
            with open(log_file_2, encoding="utf8") as f:
                beispieldaten_dateipfad_2 = json.load(f)
        except FileNotFoundError:
            self.refresh_ddb()  # 2
            with open(log_file_2, encoding="utf8") as f:
                beispieldaten_dateipfad_2 = json.load(f)

        self.beispieldaten_dateipfad_2 = beispieldaten_dateipfad_2

        if self.cb_drafts_sage.isChecked():
            drafts_path = os.path.join(path_programm, "Beispieleinreichung")
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

        list_beispieldaten = []
        if list_mode == "sage":
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
        if list_mode == "feedback":
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

        # print(list_beispieldaten)
        list_beispieldaten = sorted(list_beispieldaten, key=natural_keys)

        for all in list_beispieldaten:
            if list_mode == "feedback" and all.startswith("_L_"):
                pass
            else:
                listWidget.addItem(all)
                listWidget.setFocusPolicy(QtCore.Qt.ClickFocus)

    def save_dict_examples_data(self):
        self.dict_list_input_examples = {}
        num_typ1 = 0
        num_typ2 = 0
        self.pkt_typ1 = 0
        self.pkt_typ2 = 0

        self.dict_list_input_examples["list_examples"] = list_sage_examples

        ### include data for single examples ###
        for all in list_sage_examples:
            temp_all = all.replace("_L_", "")
            if re.search("[A-Z]", temp_all) == None:
                bsp_string = all
                typ = 2
            else:
                bsp_string = all.replace(" ", "").replace(".", "").replace("-", "_")
                typ = 1
            list_input = eval("self.list_input_{}".format(bsp_string))
            self.dict_list_input_examples[
                "self.list_input_{}".format(bsp_string)
            ] = list_input

            if typ == 1:
                self.pkt_typ1 += list_input[0]
                num_typ1 += 1
            if typ == 2:
                self.pkt_typ2 += list_input[0]
                num_typ2 += 1
        ### end ###

        ### include dictionary of changed 'ausgleichspunkte' ###
        self.dict_list_input_examples[
            "dict_ausgleichspunkte"
        ] = self.dict_sage_ausgleichspunkte_chosen

        ### end ###

        ### include basic data of test ###
        if self.radioButton_beurteilungsraster.isChecked():
            beurteilung = "br"
        else:
            beurteilung = "ns"

        try:
            self.num_ausgleichspkt_gesamt
            self.list_copy_images
        except AttributeError:
            self.num_ausgleichspkt_gesamt = 0
            self.list_copy_images = []

        dict_data_gesamt = {
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

        self.dict_list_input_examples["data_gesamt"] = dict_data_gesamt
        ### end ###


    def pushButton_vorschau_pressed(
        self, ausgabetyp, index, maximum, pdf=True, lama=True
    ):
        if ausgabetyp == "vorschau":
            self.save_dict_examples_data()


        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        dict_gesammeltedateien = {}

        for all in self.beispieldaten_dateipfad_1.values():
            filename_all = os.path.basename(all)
            name, extension = os.path.splitext(filename_all)
            for files in list_sage_examples:
                if files == name:
                    dict_gesammeltedateien[name] = all

        for all in self.beispieldaten_dateipfad_2.values():
            filename_all = os.path.basename(all)
            name, extension = os.path.splitext(filename_all)
            for files in list_sage_examples:
                if files == name:
                    dict_gesammeltedateien[name] = all

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
        raw_date = self.dict_list_input_examples["data_gesamt"]["Datum"]
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
            self.dict_list_input_examples["data_gesamt"]["Pruefungstyp"]
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
            self.dict_list_input_examples["data_gesamt"]["Pruefungstyp"]
            == "Übungsblatt"
        ):
            vorschau.write("\\subsection{Übungsblatt}")
        else:
            vorschau.write("\\begin{titlepage}\n" "\\flushright\n")
            if self.dict_titlepage["logo"] == True:
                logo_name = os.path.basename(self.dict_titlepage["logo_path"])
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
            if self.dict_titlepage["titel"] == True:
                if (
                    self.dict_list_input_examples["data_gesamt"]["Pruefungstyp"]
                    == "Wiederholungsprüfung"
                ):
                    vorschau.write("\\textsc{{\\Huge Wiederholungsprüfung}} \\\ \n")
                else:
                    vorschau.write(
                        "\\textsc{{\\Huge {0}. Mathematikschularbeit}} \\\ \n".format(
                            self.dict_list_input_examples["data_gesamt"]["#"]
                        )
                    )
                    if (
                        self.dict_list_input_examples["data_gesamt"]["Pruefungstyp"]
                        == "Wiederholungsschularbeit"
                    ):
                        vorschau.write("[0.5cm]" "\\textsc{\Large Wiederholung} \\\ \n")
                    if (
                        self.dict_list_input_examples["data_gesamt"]["Pruefungstyp"]
                        == "Nachschularbeit"
                    ):
                        vorschau.write(
                            "[0.5cm]" "\\textsc{\Large Nachschularbeit} \\\ \n"
                        )
                    vorschau.write("[2cm] \n")
            if self.dict_titlepage["datum"] == True:
                vorschau.write("\\textsc{{\Large am {0}}}\\\ [1cm] \n".format(datum))
            if self.dict_titlepage["klasse"] == True:
                vorschau.write(
                    "\\textsc{{\Large Klasse {0}}} \\\ [1cm] \n".format(
                        self.dict_list_input_examples["data_gesamt"]["Klasse"]
                    )
                )

            if ausgabetyp == "schularbeit" and maximum > 2:
                vorschau.write(
                    "\\textsc{{\\Large Gruppe {0}}} \\\ [1cm]\n".format(gruppe)
                )
            # else:
            # 	vorschau.write("\\vphantom{\\textsc{\\Large Gruppe}}\\\ [1cm] \n")
            # vorschau.write("[1cm]")
            if self.dict_titlepage["name"] == True:
                vorschau.write("\\Large Name: \\rule{8cm}{0.4pt} \\\ \n")
            vorschau.write("\\vfil\\vfil\\vfil \n")
            if self.dict_titlepage["note"] == True:
                vorschau.write("\\Large Note: \\rule{8cm}{0.4pt} \\\ [1cm]\n")
            if self.dict_titlepage["unterschrift"] == True:
                vorschau.write("\\Large Unterschrift: \\rule{8cm}{0.4pt} \\\ \n")

            if self.dict_list_input_examples["data_gesamt"]["Beurteilung"] == "br":
                exkl_teil2_pkt = (
                    self.dict_list_input_examples["data_gesamt"]["punkte_2"]
                    - self.dict_list_input_examples["data_gesamt"]["ausgleichspunkte"]
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
                        self.dict_list_input_examples["data_gesamt"]["punkte_1"],
                        self.dict_list_input_examples["data_gesamt"][
                            "ausgleichspunkte"
                        ],
                        exkl_teil2_pkt,
                    )
                )

            vorschau.write("\\end{titlepage}\n\n")
        vorschau.close()

        vorschau = open(filename_vorschau, "a", encoding="utf8")
        # for key, value in dict_gesammeltedateien.items():
        list_chosen_examples = []
        # print(self.dict_list_input_examples)
        control_counter = 0
        # print(list_sage_examples)
        for all in list_sage_examples:
            temp_all = all.replace("_L_", "")
            if re.search("[A-Z]", temp_all) == None:
                bsp_string = all
                typ = 2
            else:
                bsp_string = all.replace(" ", "").replace(".", "").replace("-", "_")
                typ = 1
            list_input = "self.list_input_{}".format(bsp_string)
            spinBox_abstand = self.dict_list_input_examples[list_input][1]
            spinBox_pkt = self.dict_list_input_examples[list_input][0]
            f = open(dict_gesammeltedateien[all], "r", encoding="utf8")
            content = f.readlines()
            f.close()


            ##### adapt content for	 creation ###

            if all in self.dict_list_input_examples["dict_ausgleichspunkte"].keys():
                content = [line.replace("\\fbox{A}", "") for line in content]
                for ausgleichspunkte in self.dict_list_input_examples[
                    "dict_ausgleichspunkte"
                ][all]:
                    content = [
                        line.replace(
                            ausgleichspunkte.partition("\n")[0],
                            "\\fbox{A} " + ausgleichspunkte.partition("\n")[0],
                        )
                        for line in content
                    ]
            ### end ###

            # print(self.dict_list_input_examples['data_gesamt']['copy_images'])

            if ausgabetyp == "schularbeit":
                # print(self.dict_list_input_examples['data_gesamt']['copy_images'])
                if index == 0:
                    if self.dict_titlepage["logo"] == True:
                        logo_name = os.path.basename(self.dict_titlepage["logo_path"])
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

                    # print(self.dict_list_input_examples['data_gesamt']['copy_images'])
                    # return

                    if (
                        self.dict_list_input_examples["data_gesamt"]["copy_images"]
                        == []
                    ):
                        pass
                    else:
                        for image in self.dict_list_input_examples["data_gesamt"][
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


                for image in self.dict_list_input_examples["data_gesamt"][
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

            example = list_chosen_examples[list_sage_examples.index(all)]
            try:
                x, y = example[0].split("[")
                gk, z = y.split("]")
            except ValueError:
                gk = ""

            if (
                self.dict_list_input_examples["data_gesamt"]["Pruefungstyp"]
                == "Grundkompetenzcheck"
                or self.dict_list_input_examples["data_gesamt"]["Pruefungstyp"]
                == "Übungsblatt"
            ):
                header = ""
            else:
                if control_counter == 0 and typ == 1:
                    header = "\\subsubsection{Typ 1 Aufgaben}\n\n"
                    control_counter += 1
                elif control_counter == 1 and typ == 2:
                    header = "\\subsubsection{Typ 2 Aufgaben}\n\n"
                    control_counter += 1
                else:
                    header = ""

            if beispiel_typ == "beispiel":
                if gk == "":
                    vorschau.write(
                        "%s\\begin{beispiel}{" % header
                        + str(spinBox_pkt)
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
                        + str(spinBox_pkt)
                        + "}\n"
                        + example[1]
                        + "\n"
                        + example[2]
                        + "\n\n"
                    )

            if beispiel_typ == "langesbeispiel":
                vorschau.write(
                    "\\newpage\n\n%s\\begin{langesbeispiel} \item[" % header
                    + str(spinBox_pkt)
                    + "]\n"
                    + example[1]
                    + "\n"
                    + example[2]
                    + "\n\n"
                )

            if spinBox_abstand != 0:
                if spinBox_abstand == 99:
                    vorschau.write("\\newpage \n\n")
                else:
                    vorschau.write("\\vspace{" + str(spinBox_abstand) + "cm} \n\n")

        if (
            self.dict_list_input_examples["data_gesamt"]["Pruefungstyp"]
            != "Grundkompetenzcheck"
            and self.dict_list_input_examples["data_gesamt"]["Pruefungstyp"]
            != "Übungsblatt"
        ):
            if self.dict_list_input_examples["data_gesamt"]["Beurteilung"] == "ns":
                notenschluessel = self.dict_list_input_examples["data_gesamt"][
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

        # MainWindow.show()
        QtWidgets.QApplication.restoreOverrideCursor()

        # sys.exit[0]

    #######################################################################
    ########################################################################

    def pushButton_send_pressed(self):
        if self.comboBox_at_fb.currentText() == "Allgemeine Rückmeldung":
            example = "Allgemeiner Bug Report"
            if self.plainTextEdit_fb.toPlainText() == "":
                self.warning_window(
                    "Bitte geben Sie ein Feedback oder beschreiben Sie das Problem im Textfeld."
                )
                return
        else:
            rest, example = self.label_example.text().split(": ")
            if example == "-":
                self.warning_window(
                    'Bitte wählen Sie die Aufgabe, zu der Sie eine Rückmeldung geben möchten oder wählen Sie "Allgemeine Rückmeldung" aus.'
                )
                return

        fehler = self.comboBox_fehlertyp.currentText()
        if fehler == "":
            self.warning_window("Bitte wählen Sie einen Betreff aus.")
            return
        if fehler == "Sonstiges" or fehler == "Feedback":
            if self.plainTextEdit_fb.toPlainText() == "":
                self.warning_window(
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

        content = "Subject: {0}: {1}\n\nProblembeschreibung:\n\n{2}\n\n\nKontakt: {3}".format(
            example, fehler, description, contact
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
            QtWidgets.QApplication.restoreOverrideCursor()

            return
        except:
            QtWidgets.QApplication.restoreOverrideCursor()

            if "smtplib.SMTPAuthenticationError" in str(sys.exc_info()[0]):
                self.warning_window(
                    "Das eingebene Passwort ist nicht korrekt!",
                    "Bitte kontaktieren Sie den Support für nähere Informationen:\n\nlama.helpme@gmail.com",
                )
            else:
                self.warning_window(
                    "Die Meldung konnte leider nicht gesendet werden!",
                    "Überprüfen Sie Ihre Internetverbindung oder versuchen Sie es später erneut.",
                )

    #######################################################################
    ##########################################################################
    ############################################################################

    def pushButton_erstellen_pressed(self):
        self.save_dict_examples_data()
        try:
            self.saved_file_path
        except AttributeError:
            self.saved_file_path = path_programm
        self.open_subwindow(
            self.dict_list_input_examples,
            self.beispieldaten_dateipfad_1,
            self.beispieldaten_dateipfad_2,
            self.dict_titlepage,
            self.saved_file_path,
        )

    def aufgaben_suchen(self):
        lists_delete = widgets_create + widgets_sage + widgets_feedback
        for all in lists_delete:
            if "action" in all:
                exec("self.%s.setVisible(False)" % all)
            elif "menu" in all:
                exec("self.menuBar.removeAction(self.%s.menuAction())" % all)
            else:
                exec("self.%s.hide()" % all)

        for all in widgets_search:
            if "action" in all:
                exec("self.%s.setVisible(True)" % all)
            elif "menu" in all:
                exec("self.menuBar.addAction(self.%s.menuAction())" % all)
            else:
                if all == "combobox_searchtype":
                    if self.label_aufgabentyp.text()[-1] == "2":
                        exec("self.%s.show()" % all)
                else:
                    exec("self.%s.show()" % all)

    def neue_aufgabe_erstellen(self):
        MainWindow.setMenuBar(self.menuBar)
        lists_delete = widgets_search + widgets_sage + widgets_feedback
        for all in lists_delete:
            if "action" in all:
                exec("self.%s.setVisible(False)" % all)
            elif "menu" in all:
                exec("self.menuBar.removeAction(self.%s.menuAction())" % all)
            else:
                exec("self.%s.hide()" % all)

        for all in widgets_create:
            if "action" in all:
                exec("self.%s.setVisible(True)" % all)
            elif "menu" in all:
                exec("self.menuBar.addAction(self.%s.menuAction())" % all)
            else:
                exec("self.%s.show()" % all)

    def neue_schularbeit_erstellen(self):
        MainWindow.setMenuBar(self.menuBar)
        lists_delete = widgets_search + widgets_create + widgets_feedback
        # self.menuBar.removeAction(self.menuDatei.menuAction())

        # self.menuBar.addAction(self.menuDatei.menuAction())
        for all in lists_delete:
            if "action" in all:
                exec("self.%s.setVisible(False)" % all)
            elif "menu" in all:
                exec("self.menuBar.removeAction(self.%s.menuAction())" % all)
            else:
                exec("self.%s.hide()" % all)

        for all in widgets_sage:
            if "action" in all:
                exec("self.%s.setVisible(True)" % all)
            elif "menu" in all:
                exec("self.menuBar.addAction(self.%s.menuAction())" % all)
            else:
                exec("self.%s.show()" % all)

        MainWindow.setTabOrder(self.spinBox_nummer, self.dateEdit)
        MainWindow.setTabOrder(self.dateEdit, self.lineEdit_klasse)

        # self.gridLayout.removeWidget(self.groupBox_alle_aufgaben)
        # self.gridLayout.addWidget(self.groupBox_alle_aufgaben, 2, 0, 7, 1)

        self.adapt_choosing_list("sage")
        self.listWidget.itemClicked.connect(self.nummer_clicked)
        # print(self.listWidget.currentRow())

    def send_feedback(self):

        MainWindow.setMenuBar(self.menuBar)
        lists_delete = widgets_search + widgets_sage + widgets_create
        for all in lists_delete:
            if "action" in all:
                exec("self.%s.setVisible(False)" % all)
            elif "menu" in all:
                exec("self.menuBar.removeAction(self.%s.menuAction())" % all)
            else:
                exec("self.%s.hide()" % all)

        for all in widgets_feedback:
            if "action" in all:
                exec("self.%s.setVisible(True)" % all)
            elif "menu" in all:
                exec("self.menuBar.addAction(self.%s.menuAction())" % all)
            else:
                exec("self.%s.show()" % all)

        self.adapt_choosing_list("feedback")
        self.listWidget_fb.itemClicked.connect(self.nummer_clicked_fb)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    screen_resolution = app.desktop().screenGeometry()
    screen_width, screen_height = screen_resolution.width(), screen_resolution.height()

    MainWindow.setGeometry(30, 30, screen_width * 0.5, screen_height * 0.8)
    MainWindow.move(30, 30)

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()

    sys.exit(app.exec_())
