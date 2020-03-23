#!/usr/bin/python3
# -*- coding: utf-8 -*-
#### Version number ###
__version__ = "v1.0.2"
__lastupdate__ = "02/20"
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


try:
    loaded_lama_file_path = sys.argv[1]
except IndexError:
    loaded_lama_file_path = ""

path_programm = os.path.dirname(sys.argv[0])
if sys.platform.startswith("darwin"):
    if path_programm is "":
        path_programm = "."

if sys.platform.startswith("darwin"):
    if path_programm is "":
        path_programm = "."


logo_path = os.path.join(
    path_programm, "_database", "_config", "icon", "LaMa_icon_logo_blau.png"
)

print("Loading...")


def config_loader(pathToFile, parameter):
    for i in range(5):
        try:
            _config = yaml.safe_load(open(pathToFile, encoding="utf8"))
            break
        except FileNotFoundError:
            print("File not Found!")
            if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
                root = "."
            else:
                root = ""
            config_path = os.path.join(".", "_database", "_config")
            if not os.path.exists(config_path):
                print("No worries, we'll create the structure for you.")
                os.makedirs(config_path)
            input(
                "Please place your your config file in '{}' and hit enter. {} tries left!".format(
                    config_path, 5 - i
                )
            )
    return _config[parameter]


config_file = os.path.join(path_programm, "_database", "_config", "_config.yml")

list_klassen = config_loader(config_file, "list_klassen")
dict_aufgabenformate = config_loader(config_file, "dict_aufgabenformate")


for klasse in list_klassen:
    exec('dict_{0} = config_loader(config_file,"dict_{0}")'.format(klasse))
    exec('dict_{0}_name = config_loader(config_file,"dict_{0}_name")'.format(klasse))


# dict_k2 = config_loader(config_file,'dict_k2')
# dict_k2_name = config_loader(config_file,'dict_k2_name')
dict_unterkapitel = config_loader(config_file, "dict_unterkapitel")


class SpinBox_noWheel(QtWidgets.QSpinBox):
    def wheelEvent(self, event):
        event.ignore()


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:

    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8

    def _translate(context, text):
        return QtWidgets.QApplication.translate(context, text, _encoding)


except AttributeError:

    def _translate(context, text):
        return QtWidgets.QApplication.translate(context, text)


widgets_search = [
    "actionRefresh_Database",
    "actionReset",
    "actionLoad",
    "actionSave",
    "menuNeue_Schularbeit",
    "menuNeue_Aufgabe",
    "menuFeedback",
    "menuHelp",
    "label_update",
    "groupBox_ausgew_gk",
    "groupBox_af",
    "groupBox_schulstufe",
    "groupBox_titelsuche",
    "groupBox_unterkapitel",
    "cb_solution",
    "cb_drafts",
    "btn_suche",
    "combobox_searchtype",
]  # ,'label_aufgabentyp','groupBox_gk','groupBox_klassen','groupBox_themen_klasse',

widgets_create = [
    "actionReset",
    "menuBild_einf_gen",
    "menuSuche",
    "menuNeue_Schularbeit",
    "menuFeedback",
    "menuHelp",
    "groupBox_ausgew_gk_cr",
    "groupBox_bilder",
    "groupBox_grundkompetenzen_cr",
    "groupBox_punkte",
    "groupBox_aufgabenformat",
    "groupBox_2",
    "groupBox_beispieleingabe",
    "groupBox_quelle",
    "pushButton_save",
]  # ,'groupBox_aufgabentyp','groupBox_klassen_cr'


widgets_sage = [
    "actionRefresh_Database",
    "menuSuche",
    "actionReset_sage",
    "menuNeue_Aufgabe",
    "menuFeedback",
    "menuHelp",
    "groupBox_alle_aufgaben",
    "groupBox_sage",
    "actionLoad",
    "actionSave",
]


widgets_feedback = [
    "menuSuche",
    "menuNeue_Schularbeit",
    "menuNeue_Aufgabe",
    "menuHelp",
    "comboBox_at_fb",
    "groupBox_alle_aufgaben_fb",
    "label_example",
    "groupBox_fehlertyp",
    "groupBox_feedback",
    "groupBox_email",
    "pushButton_send",
]


dict_picture_path = {}

# dict_sage_examples={}
# for all in list_klassen:
# 	dict_sage_examples[all]=[]
list_sage_examples = []

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [atoi(c) for c in re.split("(\d+)", text)]

class Ui_Dialog_titlepage(object):
    def setupUi(self, Dialog, dict_titlepage):
        # self.dict_titlepage = dict_titlepage
        # print(self.dict_titlepage)

        # self.ausgleichspunkte_split_text=ausgleichspunkte_split_text
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle(_translate("Titelplatt anpassen", "Titelplatt anpassen"))
        # self.Dialog.resize(600, 400)
        # self.Dialog.setWindowIcon(QtGui.QIcon(logo_path))
        # Dialog.setObjectName("Dialog")
        # Dialog.resize(468, 208)
        Dialog.setWindowIcon(QtGui.QIcon(logo_path))
        self.verticalLayout_titlepage = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_titlepage.setObjectName("verticalLayout_titlepage")
        self.label_titlepage = QtWidgets.QLabel()
        # # self.label_gk.setWordWrap(True)
        self.label_titlepage.setObjectName(_fromUtf8("label_titlepage"))
        self.label_titlepage.setText(
            _translate(
                "MainWindow",
                "Wählen Sie die gewünschten Punkte für das Titelblatt aus:\n",
            )
        )
        self.verticalLayout_titlepage.addWidget(self.label_titlepage)

        self.cb_titlepage_logo = QtWidgets.QCheckBox("Logo")
        if dict_titlepage["logo_path"] != False:
            logo_name = os.path.basename(dict_titlepage["logo_path"])
            self.cb_titlepage_logo.setText("Logo ({})".format(logo_name))
        self.cb_titlepage_logo.setObjectName(_fromUtf8("cb_titlepage_logo"))
        self.verticalLayout_titlepage.addWidget(self.cb_titlepage_logo)
        self.cb_titlepage_logo.setChecked(dict_titlepage["logo"])

        self.btn_titlepage_logo_path = QtWidgets.QPushButton()
        self.btn_titlepage_logo_path.setObjectName(_fromUtf8("btn_titlepage_logo_path"))
        self.verticalLayout_titlepage.addWidget(self.btn_titlepage_logo_path)
        self.btn_titlepage_logo_path.setText("Durchsuchen")
        self.btn_titlepage_logo_path.setMaximumWidth(130)
        self.btn_titlepage_logo_path.clicked.connect(
            partial(self.btn_titlepage_logo_path_pressed, dict_titlepage)
        )

        self.cb_titlepage_titel = QtWidgets.QCheckBox("Titel")
        self.cb_titlepage_titel.setObjectName(_fromUtf8("cb_titlepage_titel"))
        self.verticalLayout_titlepage.addWidget(self.cb_titlepage_titel)
        self.cb_titlepage_titel.setChecked(dict_titlepage["titel"])

        self.cb_titlepage_datum = QtWidgets.QCheckBox("Datum")
        self.cb_titlepage_datum.setObjectName(_fromUtf8("cb_titlepage_datum"))
        self.verticalLayout_titlepage.addWidget(self.cb_titlepage_datum)
        self.cb_titlepage_datum.setChecked(dict_titlepage["datum"])

        self.cb_titlepage_klasse = QtWidgets.QCheckBox("Klasse")
        self.cb_titlepage_klasse.setObjectName(_fromUtf8("cb_titlepage_klasse"))
        self.verticalLayout_titlepage.addWidget(self.cb_titlepage_klasse)
        self.cb_titlepage_klasse.setChecked(dict_titlepage["klasse"])

        self.cb_titlepage_name = QtWidgets.QCheckBox("Name")
        self.cb_titlepage_name.setObjectName(_fromUtf8("cb_titlepage_name"))
        self.verticalLayout_titlepage.addWidget(self.cb_titlepage_name)
        self.cb_titlepage_name.setChecked(dict_titlepage["name"])

        self.cb_titlepage_note = QtWidgets.QCheckBox("Note")
        self.cb_titlepage_note.setObjectName(_fromUtf8("cb_titlepage_note"))
        self.verticalLayout_titlepage.addWidget(self.cb_titlepage_note)
        self.cb_titlepage_note.setChecked(dict_titlepage["note"])

        self.cb_titlepage_unterschrift = QtWidgets.QCheckBox("Unterschrift")
        self.cb_titlepage_unterschrift.setObjectName(
            _fromUtf8("cb_titlepage_unterschrift")
        )
        self.verticalLayout_titlepage.addWidget(self.cb_titlepage_unterschrift)
        self.cb_titlepage_unterschrift.setChecked(dict_titlepage["unterschrift"])

        self.buttonBox_titlepage = QtWidgets.QDialogButtonBox(self.Dialog)
        self.buttonBox_titlepage = QtWidgets.QDialogButtonBox(self.Dialog)
        self.buttonBox_titlepage.setStandardButtons(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )

        # buttonS = self.buttonBox_titlepage.button(QtWidgets.QDialogButtonBox.Save)
        # buttonS.setText('Speichern')
        buttonX = self.buttonBox_titlepage.button(QtWidgets.QDialogButtonBox.Cancel)
        buttonX.setText("Standard wiederherstellen")
        self.buttonBox_titlepage.setObjectName("buttonBox")
        self.buttonBox_titlepage.rejected.connect(
            partial(self.set_default_titlepage, dict_titlepage)
        )
        self.buttonBox_titlepage.accepted.connect(
            partial(self.save_titlepage, dict_titlepage)
        )
        # self.retranslateUi(self.Dialog)

        self.verticalLayout_titlepage.addWidget(self.buttonBox_titlepage)

        return dict_titlepage

    def btn_titlepage_logo_path_pressed(self, dict_titlepage):
        logo_titlepage_path = QtWidgets.QFileDialog.getOpenFileNames(
            None, "Grafiken wählen", path_programm, "Grafiken (*.eps)"
        )
        if logo_titlepage_path[0] == []:
            return

        logo_name = os.path.basename(logo_titlepage_path[0][0])
        # print(logo_name)
        self.cb_titlepage_logo.setText("Logo ({})".format(logo_name))
        dict_titlepage["logo_path"] = "{}".format(logo_titlepage_path[0][0])
        copy_logo_titlepage_path = os.path.join(
            path_programm, "Teildokument", logo_name
        )
        shutil.copy(logo_titlepage_path[0][0], copy_logo_titlepage_path)

        # print('browse')
        # print(dict_titlepage)
        return dict_titlepage

    def save_titlepage(self, dict_titlepage):
        for all in dict_titlepage.keys():
            if all == "logo_path":
                if self.cb_titlepage_logo.isChecked() and dict_titlepage[all] == False:
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.setWindowIcon(QtGui.QIcon(logo_path))
                    msg.setText("Es wurde kein Logo ausgewählt")
                    msg.setInformativeText(
                        "Bitte geben Sie den Dateipfad des Logos an oder wählen Sie das Logo ab."
                    )
                    msg.setWindowTitle("Kein Logo ausgewählt")
                    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    msg.exec_()
                    return
                continue

            checkbox = eval("self.cb_titlepage_{}".format(all))
            if checkbox.isChecked():
                dict_titlepage[all] = True
            else:
                dict_titlepage[all] = False

        self.Dialog.reject()
        return dict_titlepage

    def set_default_titlepage(self, dict_titlepage):
        dict_titlepage = {
            "logo": False,
            "logo_path": False,
            "titel": True,
            "datum": True,
            "klasse": True,
            "name": True,
            "note": False,
            "unterschrift": False,
        }
        for all in dict_titlepage.keys():
            if all == "logo_path":
                continue
            checkbox = eval("self.cb_titlepage_{}".format(all))
            checkbox.setChecked(dict_titlepage[all])

        return dict_titlepage


class Ui_Dialog_erstellen(object):
    def setupUi(
        self,
        Dialog,
        dict_list_input_examples,
        beispieldaten_dateipfad,
        dict_titlepage,
        saved_file_path,
    ):
        self.dict_list_input_examples = dict_list_input_examples
        self.beispieldaten_dateipfad = beispieldaten_dateipfad

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
        self.gridLayout.addWidget(self.pushButton_sw_save, 4, 3, 1, 1)
        self.pushButton_sw_back = QtWidgets.QPushButton(Dialog)
        self.pushButton_sw_back.setObjectName("pushButton_sw_back")
        self.pushButton_sw_back.clicked.connect(self.pushButton_sw_back_pressed)
        self.gridLayout.addWidget(self.pushButton_sw_back, 3, 3, 1, 1)
        self.groupBox_sw_data = QtWidgets.QGroupBox(Dialog)
        self.groupBox_sw_data.setObjectName("groupBox_sw_data")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_sw_data)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.label_sw_num_ges = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_num_ges.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_sw_num_ges.setObjectName("label_sw_num_ges")
        self.gridLayout_2.addWidget(
            self.label_sw_num_ges, 3, 0, 1, 1, QtCore.Qt.AlignLeft
        )

        self.label_sw_num_ges_int = QtWidgets.QLabel(self.groupBox_sw_data)

        self.label_sw_num_ges_int.setObjectName("label_sw_num_1_int")
        self.gridLayout_2.addWidget(self.label_sw_num_ges_int, 3, 1, 1, 1)

        self.label_sw_pkt_ges = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_pkt_ges.setObjectName("label_sw_pkt_ges")
        self.gridLayout_2.addWidget(self.label_sw_pkt_ges, 4, 0, 1, 1)

        self.label_sw_pkt_ges_int = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_pkt_ges_int.setObjectName("label_sw_pkt_ges_int")
        self.gridLayout_2.addWidget(self.label_sw_pkt_ges_int, 4, 1, 1, 1)

        self.label_sw_date = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_date.setObjectName("label_sw_date")
        self.gridLayout_2.addWidget(self.label_sw_date, 1, 0, 1, 1)

        self.label_sw_klasse = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_klasse.setObjectName("label_sw_klasse")
        self.gridLayout_2.addWidget(self.label_sw_klasse, 1, 3, 1, 1)
        self.gridLayout.addWidget(self.groupBox_sw_data, 0, 0, 5, 3)
        self.groupBox_sw_gruppen = QtWidgets.QGroupBox(Dialog)
        self.groupBox_sw_gruppen.setObjectName("groupBox_sw_gruppen")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_sw_gruppen)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.spinBox_sw_gruppen = QtWidgets.QSpinBox(self.groupBox_sw_gruppen)
        self.spinBox_sw_gruppen.setMinimum(1)
        self.spinBox_sw_gruppen.setMaximum(5)
        self.spinBox_sw_gruppen.setObjectName("spinBox_sw_gruppen")

        self.gridLayout_3.addWidget(self.spinBox_sw_gruppen, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_sw_gruppen, 0, 3, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        # print(self.data_gesamt)
        datum = (
            str(self.data_gesamt["Datum"][2])
            + "."
            + str(self.data_gesamt["Datum"][1])
            + "."
            + str(self.data_gesamt["Datum"][0])
        )
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Erstellen", "Erstellen"))

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
        self.label_sw_num_ges.setText(_translate("Dialog", "Anzahl der Aufgaben:"))
        self.label_sw_num_ges_int.setText(
            _translate("Dialog", "%s" % str(self.data_gesamt["num_aufgabe"]))
        )

        self.label_sw_pkt_ges.setText(_translate("Dialog", "Gesamtpunkte:"))

        self.label_sw_date.setText(_translate("Dialog", "Datum: %s" % datum))

        self.label_sw_pkt_ges_int.setText(
            _translate("Dialog", "%s" % str(self.data_gesamt["gesamtpunkte"]))
        )  # +self.data_gesamt['ausgleichspunkte']
        self.label_sw_klasse.setText(
            _translate("Dialog", "Klasse: %s" % self.data_gesamt["Klasse"])
        )
        self.groupBox_sw_gruppen.setTitle(_translate("Dialog", "Anzahl der Gruppen"))

    def pushButton_sw_back_pressed(self):
        self.Dialog.reject()

    def pushButton_sw_save_pressed(self):
        self.Dialog.reject()

        # print(self.spinBox_sw_gruppen.value())
        MainWindow.hide()

        for index in range(self.spinBox_sw_gruppen.value() * 2):
            Ui_MainWindow.pushButton_vorschau_pressed(
                self, "schularbeit", index, self.spinBox_sw_gruppen.value() * 2
            )

        MainWindow.show()

        if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
            file_path = os.path.dirname(self.saved_file_path)
            subprocess.Popen('xdg-open "{}"'.format(file_path), shell=True)
        elif sys.platform.startswith("darwin"):
            file_path = os.path.dirname(self.saved_file_path)
            subprocess.Popen('open "{}"'.format(file_path), shell=True)
        else:
            file_path = os.path.dirname(self.saved_file_path).replace("/", "\\")
            subprocess.Popen('explorer "{}"'.format(file_path))


class Ui_MainWindow(object):
    global dict_picture_path, list_sage_examples

    def __init__(self):
        self.dict_chosen_topics = {}
        self.list_creator_topics = []
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

    def open_subwindow_erstellen(
        self,
        dict_list_input_examples,
        beispieldaten_dateipfad,
        dict_titlepage,
        saved_file_path,
    ):  # , dict_gesammeltedateien
        self.Dialog_erstellen = QtWidgets.QDialog(
            None,
            QtCore.Qt.WindowSystemMenuHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint,
        )
        self.ui = Ui_Dialog_erstellen()
        self.ui.setupUi(
            self.Dialog_erstellen,
            dict_list_input_examples,
            beispieldaten_dateipfad,
            dict_titlepage,
            saved_file_path,
        )  # , dict_gesammeltedateien
        self.Dialog_erstellen.show()
        self.Dialog_erstellen.exec_()

    def setupUi(self, MainWindow):

        self.check_for_update()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)

        # MainWindow.setMaximumSize(QtCore.QSize(1078, 16777215))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setStyleSheet("")
        MainWindow.setWindowIcon(QtGui.QIcon(logo_path))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.groupBox_schulstufe = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_schulstufe.setMaximumSize(QtCore.QSize(450, 16777215))
        self.groupBox_schulstufe.setObjectName("groupBox_schulstufe")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_schulstufe)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget_klassen = QtWidgets.QTabWidget(self.groupBox_schulstufe)
        self.tabWidget_klassen.setStyleSheet("background-color: rgb(229, 246, 255);")
        self.tabWidget_klassen.setMovable(False)
        self.tabWidget_klassen.setObjectName("tabWidget_klassen")

        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        for all in list_klassen:
            # print(all)
            exec("self.tab_{} = QtWidgets.QWidget()".format(all))
            exec('self.tab_{}.setObjectName("tab_k1")'.format(all))
            exec(
                "self.gridLayout_{0} = QtWidgets.QGridLayout(self.tab_{0})".format(all)
            )
            exec('self.gridLayout_{0}.setObjectName("gridLayout_{0}")'.format(all))
            exec(
                "self.scrollArea_{0} = QtWidgets.QScrollArea(self.tab_{0})".format(all)
            )
            scrollArea = eval("self.scrollArea_{0}".format(all))
            scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
            scrollArea.setWidgetResizable(True)
            scrollArea.setObjectName("scrollArea")
            exec("self.scrollAreaWidgetContents_{} = QtWidgets.QWidget()".format(all))
            exec(
                "self.scrollAreaWidgetContents_{}.setGeometry(QtCore.QRect(0, 0, 264, 235))".format(
                    all
                )
            )
            exec(
                'self.scrollAreaWidgetContents_{0}.setObjectName("scrollAreaWidgetContents_{0}")'.format(
                    all
                )
            )
            exec(
                "self.verticalLayout_kapitel_{0} = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_{0})".format(
                    all
                )
            )
            verticalLayout = eval("self.verticalLayout_kapitel_{0}".format(all))
            verticalLayout.setObjectName("verticalLayout_kapitel_{0}".format(all))

            dict_klasse_name = eval("dict_{}_name".format(all))
            for kapitel in dict_klasse_name:
                self.create_kapitel(verticalLayout, all[1], kapitel)

            verticalLayout.addItem(spacerItem)
            exec(
                "self.scrollArea_{0}.setWidget(self.scrollAreaWidgetContents_{0})".format(
                    all
                )
            )
            exec(
                "self.gridLayout_{0}.addWidget(self.scrollArea_{0}, 5, 0, 1, 1)".format(
                    all
                )
            )
            exec(
                'self.tabWidget_klassen.addTab(self.tab_{0}, "{1}. Klasse")'.format(
                    all, all[1]
                )
            )

        self.groupBox_unterkapitel = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_unterkapitel.setStyleSheet(
            "background-color: rgb(217, 255, 215);"
        )
        self.groupBox_unterkapitel.setObjectName("groupBox_unterkapitel")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.groupBox_unterkapitel)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.gridLayout.addWidget(self.groupBox_unterkapitel, 1, 2, 2, 1)

        self.verticalLayout.addWidget(self.tabWidget_klassen)
        self.gridLayout.addWidget(self.groupBox_schulstufe, 1, 0, 2, 1)
        self.groupBox_ausgew_gk = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_ausgew_gk.setObjectName("groupBox_ausgew_gk")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_ausgew_gk)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_ausg_themen = QtWidgets.QLabel(self.groupBox_ausgew_gk)
        self.label_ausg_themen.setWordWrap(False)
        self.label_ausg_themen.setObjectName("label_ausg_themen")
        self.label_ausg_themen.setWordWrap(True)
        self.verticalLayout_2.addWidget(self.label_ausg_themen)
        self.gridLayout.addWidget(self.groupBox_ausgew_gk, 3, 2, 1, 1)
        self.groupBox_titelsuche = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_titelsuche.setObjectName("groupBox_titelsuche")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.groupBox_titelsuche)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.entry_suchbegriffe = QtWidgets.QLineEdit(self.groupBox_titelsuche)
        self.entry_suchbegriffe.setObjectName("entry_suchbegriffe")
        self.gridLayout_10.addWidget(self.entry_suchbegriffe, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_titelsuche, 4, 2, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_update = QtWidgets.QLabel(self.centralwidget)
        self.label_update.setObjectName("label_update")
        self.horizontalLayout.addWidget(self.label_update)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_combobox = QtWidgets.QHBoxLayout()
        self.horizontalLayout_combobox.setObjectName("horizontalLayout_combobox")
        self.combobox_searchtype = QtWidgets.QComboBox(self.centralwidget)
        self.combobox_searchtype.setEnabled(True)
        self.combobox_searchtype.setObjectName("combobox_searchtype")
        self.combobox_searchtype.addItem("")
        self.combobox_searchtype.addItem("")
        self.horizontalLayout_combobox.addWidget(self.combobox_searchtype)
        self.gridLayout.addLayout(self.horizontalLayout_combobox, 0, 2, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cb_solution = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_solution.setChecked(True)
        self.cb_solution.setObjectName("cb_solution")
        self.horizontalLayout_2.addWidget(self.cb_solution)
        self.cb_drafts = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_drafts.setObjectName(_fromUtf8("cb_drafts"))
        self.horizontalLayout_2.addWidget(self.cb_drafts)
        self.cb_drafts.toggled.connect(self.cb_drafts_enabled)
        self.btn_suche = QtWidgets.QPushButton(self.centralwidget)
        self.btn_suche.setEnabled(True)
        self.btn_suche.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.btn_suche.setAcceptDrops(False)
        self.btn_suche.setObjectName("btn_suche")
        self.horizontalLayout_2.addWidget(self.btn_suche)
        self.gridLayout.addLayout(self.horizontalLayout_2, 5, 2, 1, 1)
        self.groupBox_af = QtWidgets.QGroupBox(self.centralwidget)
        # self.groupBox_af.setMaximumSize(QtCore.QSize(367, 16777215))
        self.groupBox_af.setObjectName("groupBox_af")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.groupBox_af)
        self.gridLayout_13.setObjectName("gridLayout_13")

        self.cb_af_mc = QtWidgets.QCheckBox(self.groupBox_af)
        self.cb_af_mc.setObjectName("cb_af_mc")
        self.gridLayout_13.addWidget(self.cb_af_mc, 1, 0, 1, 1)

        self.cb_af_lt = QtWidgets.QCheckBox(self.groupBox_af)
        self.cb_af_lt.setObjectName("cb_af_lt")
        self.gridLayout_13.addWidget(self.cb_af_lt, 3, 0, 1, 1)

        self.cb_af_ta = QtWidgets.QCheckBox(self.groupBox_af)
        self.cb_af_ta.setObjectName("cb_af_ta")
        self.gridLayout_13.addWidget(self.cb_af_ta, 5, 0, 1, 1)

        self.cb_af_ko = QtWidgets.QCheckBox(self.groupBox_af)
        self.cb_af_ko.setObjectName("cb_af_rf")
        self.gridLayout_13.addWidget(self.cb_af_ko, 7, 0, 1, 1)

        self.cb_af_rf = QtWidgets.QCheckBox(self.groupBox_af)
        self.cb_af_rf.setObjectName("cb_af_rf")
        self.gridLayout_13.addWidget(self.cb_af_rf, 1, 2, 1, 1)

        self.cb_af_oa = QtWidgets.QCheckBox(self.groupBox_af)
        self.cb_af_oa.setObjectName("cb_af_oa")
        self.gridLayout_13.addWidget(self.cb_af_oa, 5, 2, 1, 1)

        self.cb_af_zo = QtWidgets.QCheckBox(self.groupBox_af)
        self.cb_af_zo.setObjectName("cb_af_zo")
        self.gridLayout_13.addWidget(self.cb_af_zo, 3, 2, 1, 1)

        self.gridLayout.addWidget(self.groupBox_af, 3, 0, 3, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 672, 21))
        self.menuBar.setObjectName("menuBar")

        self.menuDatei = QtWidgets.QMenu(self.menuBar)
        self.menuDatei.setObjectName("menuDatei")
        self.menuNeue_Schularbeit = QtWidgets.QMenu(self.menuBar)
        self.menuNeue_Schularbeit.setObjectName("menuNeue_Schularbeit")
        self.menuNeue_Aufgabe = QtWidgets.QMenu(self.menuBar)
        self.menuNeue_Aufgabe.setObjectName("menuNeue_Aufgabe")

        self.actionBild_konvertieren_jpg_eps = QtWidgets.QAction(MainWindow)
        self.actionBild_konvertieren_jpg_eps.setObjectName(
            _fromUtf8("actionBild_konvertieren_jpg_eps")
        )
        MainWindow.setMenuBar(self.menuBar)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionAufgaben_Typ1 = QtWidgets.QAction(MainWindow)
        self.actionAufgaben_Typ1.setObjectName("actionAufgaben_Typ1")
        self.actionTyp_2_Aufgaben = QtWidgets.QAction(MainWindow)
        self.actionTyp_2_Aufgaben.setObjectName("actionTyp_2_Aufgaben")
        self.actionReset = QtWidgets.QAction(MainWindow)
        self.actionReset.setObjectName("actionReset")
        self.actionReset_sage = QtWidgets.QAction(MainWindow)
        self.actionReset_sage.setObjectName(_fromUtf8("actionReset_sage"))
        self.actionLoad = QtWidgets.QAction(MainWindow)
        self.actionLoad.setObjectName(_fromUtf8("actionLoad"))
        # self.actionLoad.setVisible(False)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        # self.actionSave.setVisible(False)

        self.menuFeedback = QtWidgets.QMenu(self.menuBar)
        self.menuFeedback.setObjectName(_fromUtf8("menuFeedback"))

        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")

        self.actionFeedback = QtWidgets.QAction(MainWindow)
        self.actionFeedback.setObjectName(_fromUtf8("actionFeedback"))

        self.menuFeedback.addAction(self.actionFeedback)

        self.actionRefresh_Database = QtWidgets.QAction(MainWindow)
        self.actionRefresh_Database.setObjectName("actionRefresh_Database")
        self.actionNeue_Schularbeit_erstellen = QtWidgets.QAction(MainWindow)
        self.actionNeue_Schularbeit_erstellen.setObjectName(
            "actionNeue_Schularbeit_erstellen"
        )
        self.actionNeue_Aufgabe_erstellen = QtWidgets.QAction(MainWindow)
        self.actionNeue_Aufgabe_erstellen.setObjectName("actionNeue_Aufgabe_erstellen")
        self.menuDatei.addAction(self.actionRefresh_Database)
        self.menuDatei.addAction(self.actionReset)
        self.menuDatei.addAction(self.actionReset_sage)
        self.actionReset_sage.setVisible(False)        
        self.menuDatei.addAction(self.actionLoad)
        self.menuDatei.addAction(self.actionSave)
        self.menuDatei.addSeparator()
        self.menuDatei.addAction(self.actionBild_konvertieren_jpg_eps)
        self.menuDatei.addSeparator()
        self.menuDatei.addAction(self.actionExit)
        self.menuNeue_Schularbeit.addAction(self.actionNeue_Schularbeit_erstellen)
        self.menuNeue_Aufgabe.addAction(self.actionNeue_Aufgabe_erstellen)

        self.menuBar.addAction(self.menuDatei.menuAction())
        self.menuBar.addAction(self.menuNeue_Schularbeit.menuAction())
        self.menuBar.addAction(self.menuNeue_Aufgabe.menuAction())

        self.menuBar.addAction(self.menuFeedback.menuAction())
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.actionInfo = QtWidgets.QAction(MainWindow)
        self.actionInfo.setObjectName(_fromUtf8("actionInfo"))
        self.menuHelp.addAction(self.actionInfo)
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.actionSuche = QtWidgets.QAction(MainWindow)
        self.actionSuche.setObjectName(_fromUtf8("actionSuche"))
        self.menuSuche = QtWidgets.QMenu(self.menuBar)
        self.menuSuche.setObjectName(_fromUtf8("menuSuche"))
        self.menuSuche.addAction(self.actionSuche)
        self.menuBild_einf_gen = QtWidgets.QMenu(self.menuBar)
        self.menuBild_einf_gen.setObjectName(_fromUtf8("menuBild_einf_gen"))
        self.actionBild_einf_gen = QtWidgets.QAction(MainWindow)
        self.actionBild_einf_gen.setObjectName(_fromUtf8("actionBild_einf_gen"))
        self.menuBild_einf_gen.addAction(self.actionBild_einf_gen)
        self.menuBild_einf_gen.addSeparator()
        # self.menuBild_einf_gen.addAction(self.actionBild_konvertieren_jpg_eps)
        self.actionBild_einf_gen.triggered.connect(self.add_picture)
        self.actionBild_konvertieren_jpg_eps.triggered.connect(self.convert_imagetoeps)
        MainWindow.setMenuBar(self.menuBar)

        self.tabWidget_klassen.setCurrentIndex(0)
        self.tabWidget_klassen.currentChanged.connect(self.tab_changed)

        self.actionExit.triggered.connect(self.close_app)
        self.actionReset.triggered.connect(self.reset_window)
        self.actionReset_sage.triggered.connect(self.reset_sage)
        self.actionRefresh_Database.triggered.connect(self.refresh_ddb)
        self.actionLoad.triggered.connect(partial(self.sage_load, False))
        self.actionSave.triggered.connect(partial(self.sage_save, ""))
        self.actionInfo.triggered.connect(self.show_info)
        self.actionNeue_Aufgabe_erstellen.triggered.connect(self.neue_aufgabe_erstellen)
        self.actionSuche.triggered.connect(self.aufgaben_suchen)
        self.actionNeue_Schularbeit_erstellen.triggered.connect(
            self.neue_schularbeit_erstellen
        )
        self.btn_suche.clicked.connect(self.PrepareTeXforPDF)
        self.actionFeedback.triggered.connect(self.send_feedback)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        ##############################################################
        #####################CREATOR #########################################
        ##########################################################################

        self.groupBox_grundkompetenzen_cr = QtWidgets.QGroupBox(self.centralwidget)

        self.groupBox_grundkompetenzen_cr.setObjectName(
            _fromUtf8("groupBox_grundkompetenzen_cr")
        )
        self.groupBox_grundkompetenzen_cr.setMaximumSize(QtCore.QSize(500, 16777215))
        self.gridLayout_11_cr = QtWidgets.QGridLayout(self.groupBox_grundkompetenzen_cr)
        self.gridLayout_11_cr.setObjectName(_fromUtf8("gridLayout_11_cr"))
        self.tab_widget_gk_cr = QtWidgets.QTabWidget(self.groupBox_grundkompetenzen_cr)
        # self.tab_widget_gk_cr.setStyleSheet(_fromUtf8("background-color: rgb(217, 255, 215);"))
        self.tab_widget_gk_cr.setStyleSheet("background-color: rgb(229, 246, 255);")
        self.tab_widget_gk_cr.setObjectName(_fromUtf8("tab_widget_gk_cr"))
        self.gridLayout_11_cr.addWidget(self.tab_widget_gk_cr, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_grundkompetenzen_cr, 0, 0, 4, 1)
        self.groupBox_grundkompetenzen_cr.setTitle(
            _translate("MainWindow", "Themengebiete")
        )
        self.groupBox_grundkompetenzen_cr.hide()

        self.groupBox_ausgew_gk_cr = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_ausgew_gk_cr.setMinimumSize(QtCore.QSize(350, 0))
        self.groupBox_ausgew_gk_cr.setMaximumSize(QtCore.QSize(500, 16777215))
        self.groupBox_ausgew_gk_cr.setObjectName(_fromUtf8("groupBox_ausgew_gk_cr"))

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_ausgew_gk_cr)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_ausgew_gk = QtWidgets.QLabel(self.groupBox_ausgew_gk_cr)
        self.label_ausgew_gk.setWordWrap(True)
        self.label_ausgew_gk.setObjectName(_fromUtf8("label_ausgew_gk"))
        self.verticalLayout_2.addWidget(self.label_ausgew_gk)
        self.gridLayout.addWidget(self.groupBox_ausgew_gk_cr, 4, 0, 1, 1)
        self.groupBox_ausgew_gk_cr.setTitle(
            _translate("MainWindow", "Ausgewählte Themengebiete")
        )
        self.label_ausgew_gk.setText(_translate("MainWindow", "-"))
        self.groupBox_ausgew_gk_cr.hide()

        self.groupBox_bilder = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_bilder.setMaximumSize(QtCore.QSize(500, 120))
        self.groupBox_bilder.setMaximumSize(QtCore.QSize(500, 16777215))
        self.groupBox_bilder.setObjectName(_fromUtf8("groupBox_bilder"))

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
            _translate("MainWindow", "Bilder (klicken, um Bilder zu entfernen)")
        )

        self.label_bild_leer = QtWidgets.QLabel(self.scrollAreaWidgetContents_bilder)
        self.label_bild_leer.setObjectName(_fromUtf8("label_bild_leer"))
        self.verticalLayout.addWidget(self.label_bild_leer)
        self.label_bild_leer.setText(_translate("MainWindow", "-"))
        self.gridLayout.addWidget(self.groupBox_bilder, 5, 0, 2, 1)
        self.groupBox_bilder.hide()

        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_14 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_14.setObjectName(_fromUtf8("gridLayout_14"))
        self.lineEdit_titel = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_titel.setObjectName(_fromUtf8("lineEdit_titel"))
        self.gridLayout_14.addWidget(self.lineEdit_titel, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 1, 1, 1, 2)
        self.groupBox_2.setTitle(_translate("MainWindow", "Titel"))
        self.groupBox_2.hide()

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
        self.plainTextEdit.setMinimumSize(400, 200)
        # self.plainTextEdit.setSizePolicy(800,500)
        self.gridLayout_10.addWidget(self.plainTextEdit, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_beispieleingabe, 2, 1, 3, 2)
        self.groupBox_beispieleingabe.setTitle(
            _translate("MainWindow", "Beispieleingabe")
        )
        # self.groupBox_beispieleingabe.resize(500, 200)
        self.label.setText(
            _translate(
                "MainWindow",
                "Info: Eingabe des Aufgabentextes zwischen \\begin{beispiel}...\\end{beispiel}",
            )
        )
        self.groupBox_beispieleingabe.hide()

        for all in list_klassen:
            exec("self.tab_cr_{} = QtWidgets.QWidget()".format(all))
            exec('self.tab_cr_{0}.setObjectName("tab_cr_{0}")'.format(all))
            exec(
                "self.gridLayout_cr_{0} = QtWidgets.QGridLayout(self.tab_cr_{0})".format(
                    all
                )
            )
            exec(
                'self.gridLayout_cr_{0}.setObjectName("gridLayout_cr_{0}")'.format(all)
            )
            exec(
                "self.scrollArea_cr_{0} = QtWidgets.QScrollArea(self.tab_cr_{0})".format(
                    all
                )
            )
            scrollArea_cr = eval("self.scrollArea_cr_{0}".format(all))
            scrollArea_cr.setFrameShape(QtWidgets.QFrame.NoFrame)
            scrollArea_cr.setWidgetResizable(True)
            scrollArea_cr.setObjectName("scrollArea_cr")
            exec(
                "self.scrollAreaWidgetContents_cr_{} = QtWidgets.QWidget()".format(all)
            )
            exec(
                "self.scrollAreaWidgetContents_cr_{}.setGeometry(QtCore.QRect(0, 0, 264, 235))".format(
                    all
                )
            )
            exec(
                'self.scrollAreaWidgetContents_cr_{0}.setObjectName("scrollAreaWidgetContents_cr_{0}")'.format(
                    all
                )
            )
            exec(
                "self.verticalLayout_kapitel_cr_{0} = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_cr_{0})".format(
                    all
                )
            )
            verticalLayout_cr = eval("self.verticalLayout_kapitel_cr_{0}".format(all))
            verticalLayout_cr.setObjectName("verticalLayout_kapitel_cr_{0}".format(all))

            dict_klasse_name = eval("dict_{}_name".format(all))

            exec(
                "self.combobox_kapitel_{} = QtWidgets.QComboBox(self.centralwidget)".format(
                    all
                )
            )
            combobox_kapitel = eval("self.combobox_kapitel_{}".format(all))
            # self.combobox_searchtype.setEnabled(True)
            combobox_kapitel.setObjectName("combobox_kapitel_{}".format(all))
            i = 0
            for kapitel in dict_klasse_name:
                dict_klasse_name = eval("dict_k{}_name".format(all[1]))
                combobox_kapitel.addItem("")
                combobox_kapitel.setItemText(
                    i,
                    _translate(
                        "MainWindow", dict_klasse_name[kapitel] + " (" + kapitel + ")"
                    ),
                )
                combobox_kapitel.setMinimumHeight(25)
                combobox_kapitel.setStyleSheet("background-color: rgb(240, 240, 240);")
                i += 1

            spacerItem_unterkapitel = QtWidgets.QSpacerItem(
                20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
            )
            verticalLayout_cr.addWidget(combobox_kapitel)
            combobox_kapitel.currentIndexChanged.connect(
                partial(
                    self.comboBox_kapitel_changed_cr,
                    verticalLayout_cr,
                    combobox_kapitel,
                    all,
                    spacerItem_unterkapitel,
                )
            )
            self.label_linespacer = QtWidgets.QLabel(self.centralwidget)
            self.label_linespacer.setObjectName(_fromUtf8("label_linespacer"))
            self.label_linespacer.setMinimumHeight(10)
            verticalLayout_cr.addWidget(self.label_linespacer)

            exec(
                "self.scrollArea_cr_{0}.setWidget(self.scrollAreaWidgetContents_cr_{0})".format(
                    all
                )
            )
            exec(
                "self.gridLayout_cr_{0}.addWidget(self.scrollArea_cr_{0}, 5, 0, 1, 1)".format(
                    all
                )
            )

            exec(
                'self.tab_widget_gk_cr.addTab(self.tab_cr_{0}, "{1}. Klasse")'.format(
                    all, all[1]
                )
            )

            dict_klasse = eval("dict_{}".format(all))
            first_element = list(dict_klasse.keys())[0]
            for unterkapitel in dict_klasse[first_element]:
                self.create_checkbox_unterkapitel(
                    verticalLayout_cr, all, first_element, unterkapitel
                )

            verticalLayout_cr.addItem(spacerItem_unterkapitel)

        self.groupBox_punkte = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_punkte.setObjectName(_fromUtf8("groupBox_punkte"))
        self.groupBox_punkte.setMaximumSize(100, 60)
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_punkte)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.spinBox_punkte = QtWidgets.QSpinBox(self.groupBox_punkte)
        self.spinBox_punkte.setProperty("value", 1)
        self.spinBox_punkte.setObjectName(_fromUtf8("spinBox_punkte"))
        self.gridLayout_6.addWidget(self.spinBox_punkte, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_punkte, 0, 1, 1, 1)
        self.groupBox_punkte.setTitle(_translate("MainWindow", "Punkte"))
        self.groupBox_punkte.hide()

        self.groupBox_aufgabenformat = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_aufgabenformat.setObjectName(_fromUtf8("groupBox_aufgabenformat"))
        # self.groupBox_aufgabenformat.setMaximumSize(16777215,60)
        self.groupBox_aufgabenformat.setMinimumSize(300, 60)
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_aufgabenformat)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.comboBox_af = QtWidgets.QComboBox(self.groupBox_aufgabenformat)
        self.comboBox_af.setObjectName(_fromUtf8("comboBox_af"))
        i = 0
        self.comboBox_af.addItem(_fromUtf8(""))

        self.comboBox_af.setItemText(i, _translate("MainWindow", "bitte auswählen"))
        i += 1
        for all in dict_aufgabenformate:
            self.comboBox_af.addItem(_fromUtf8(""))
            self.comboBox_af.setItemText(
                i, _translate("MainWindow", dict_aufgabenformate[all])
            )
            i += 1

        self.gridLayout_7.addWidget(self.comboBox_af, 0, 0, 1, 1)
        self.gridLayout.addWidget(
            self.groupBox_aufgabenformat, 0, 2, 1, 1, QtCore.Qt.AlignRight
        )
        self.groupBox_aufgabenformat.setTitle(
            _translate("MainWindow", "Aufgabenformat")
        )

        self.groupBox_aufgabenformat.hide()
        self.label_keine_auswahl = QtWidgets.QLabel(self.groupBox_aufgabenformat)
        self.label_keine_auswahl.setObjectName(_fromUtf8("label_keine_auswahl"))
        # self.label_keine_auswahl.setMinimumSize(QtCore.QSize(139,0))
        self.gridLayout_7.addWidget(self.label_keine_auswahl)
        self.label_keine_auswahl.setText(
            _translate("MainWindow", "keine Auswahl nötig")
        )
        self.label_keine_auswahl.hide()

        self.groupBox_quelle = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_quelle.setObjectName(_fromUtf8("groupBox_quelle"))
        # self.groupBox_quelle.setMaximumSize(QtCore.QSize(16777215, 120))

        self.gridLayout_18 = QtWidgets.QGridLayout(self.groupBox_quelle)
        self.gridLayout_18.setObjectName(_fromUtf8("gridLayout_18"))
        self.lineEdit_quelle = QtWidgets.QLineEdit(self.groupBox_quelle)
        self.lineEdit_quelle.setObjectName(_fromUtf8("lineEdit_quelle"))
        self.gridLayout_18.addWidget(self.lineEdit_quelle, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_quelle, 5, 1, 1, 2)
        self.groupBox_quelle.setTitle(
            _translate(
                "MainWindow", "Quelle oder Autor (Vorname Nachname) - Eingabe: VorNac"
            )
        )
        self.groupBox_quelle.hide()

        self.pushButton_save = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_save.setObjectName(_fromUtf8("pushButton_save"))
        self.gridLayout.addWidget(
            self.pushButton_save, 6, 2, 1, 1, QtCore.Qt.AlignRight
        )  #
        self.pushButton_save.setFixedSize(150, 30)
        self.pushButton_save.setText(_translate("MainWindow", "Speichern"))
        self.pushButton_save.setShortcut(_translate("MainWindow", "Return"))
        self.pushButton_save.clicked.connect(self.save_file)
        self.pushButton_save.hide()

        self.tab_widget_gk_cr.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # MainWindow.setTabOrder(self.comboBox_aufgabentyp_cr, self.spinBox_punkte)
        MainWindow.setTabOrder(self.spinBox_punkte, self.comboBox_af)
        MainWindow.setTabOrder(self.comboBox_af, self.lineEdit_titel)
        # MainWindow.setTabOrder(self.comboBox_klassen_cr, )
        MainWindow.setTabOrder(self.lineEdit_titel, self.plainTextEdit)
        MainWindow.setTabOrder(self.plainTextEdit, self.lineEdit_quelle)
        MainWindow.setTabOrder(self.lineEdit_quelle, self.pushButton_save)

        ####################################################
        #####################################################
        ################# LaMA SAGE ####################
        #####################################################

        self.groupBox_alle_aufgaben = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_alle_aufgaben.setMinimumSize(QtCore.QSize(140, 16777215))
        # self.groupBox_alle_aufgaben.setMaximumSize(QtCore.QSize(180, 16777215))
        self.groupBox_alle_aufgaben.setObjectName("groupBox_alle_aufgaben")
        self.verticalLayout_sage = QtWidgets.QVBoxLayout(self.groupBox_alle_aufgaben)
        self.verticalLayout_sage.setObjectName("verticalLayout_sage")
        self.comboBox_klassen = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
        self.comboBox_klassen.setObjectName("comboBox_klassen")
        # self.comboBox_gk.addItem("")
        index = 0
        for all in list_klassen:
            self.comboBox_klassen.addItem("")

            self.comboBox_klassen.setItemText(
                index, _translate("MainWindow", all[1] + ". Klasse")
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
            partial(self.adapt_choosing_list, "sage")
        )
        self.verticalLayout_sage.addWidget(self.lineEdit_number)

        self.listWidget = QtWidgets.QListWidget(self.groupBox_alle_aufgaben)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_sage.addWidget(self.listWidget)
        self.gridLayout.addWidget(self.groupBox_alle_aufgaben, 0, 0, 7, 1)
        self.groupBox_alle_aufgaben.setTitle(_translate("MainWindow", "Aufgaben"))
        self.groupBox_alle_aufgaben.hide()

        self.groupBox_sage = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_sage.setObjectName("groupBox_sage")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_sage)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.groupBox_sage.setTitle(_translate("MainWindow", "Schularbeitserstellung"))

        # self.checkBox_wiederholung = QtWidgets.QCheckBox(self.groupBox_sage)
        # self.checkBox_wiederholung.setObjectName("checkBox_wiederholung")
        # self.checkBox_wiederholung.setFocusPolicy(QtCore.Qt.ClickFocus)
        # self.gridLayout_5.addWidget(self.checkBox_wiederholung, 2, 4, 1, 2)
        # self.checkBox_wiederholung.setText(_translate("MainWindow", "Wiederholung", None))

        self.comboBox_pruefungstyp = QtWidgets.QComboBox(self.groupBox_sage)
        self.comboBox_pruefungstyp.setObjectName("comboBox_pruefungstyp")
        self.comboBox_pruefungstyp.addItem("")
        self.comboBox_pruefungstyp.addItem("")
        self.comboBox_pruefungstyp.addItem("")
        self.comboBox_pruefungstyp.addItem("")
        self.comboBox_pruefungstyp.addItem("")
        self.comboBox_pruefungstyp.addItem("")
        self.comboBox_pruefungstyp.setItemText(
            0, _translate("MainWindow", "Schularbeit")
        )
        self.comboBox_pruefungstyp.setItemText(
            1, _translate("MainWindow", "Nachschularbeit")
        )
        self.comboBox_pruefungstyp.setItemText(
            2, _translate("MainWindow", "Wiederholungsschularbeit")
        )
        self.comboBox_pruefungstyp.setItemText(
            3, _translate("MainWindow", "Wiederholungsprüfung")
        )
        self.comboBox_pruefungstyp.setItemText(
            4, _translate("MainWindow", "Wiederholung")
        )
        self.comboBox_pruefungstyp.setItemText(
            5, _translate("MainWindow", "Übungsblatt")
        )

        self.comboBox_pruefungstyp.setFocusPolicy(QtCore.Qt.ClickFocus)

        self.gridLayout_5.addWidget(self.comboBox_pruefungstyp, 0, 5, 1, 1)

        # self.verticalLayout_sage.addWidget(self.comboBox_pruefungstyp)

        # self.radioButton_notenschl = QtWidgets.QRadioButton(self.groupBox_sage)
        # self.radioButton_notenschl.setChecked(True)
        # self.radioButton_notenschl.setObjectName("radioButton_notenschl")
        # self.radioButton_notenschl.setFocusPolicy(QtCore.Qt.ClickFocus)
        # #self.radioButton_notenschl.toggled.connect(self.beurteilungsraster_changed)
        # self.gridLayout_5.addWidget(self.radioButton_notenschl, 3, 4, 1, 2)
        # self.radioButton_beurteilungsraster = QtWidgets.QRadioButton(self.groupBox_sage)
        # self.radioButton_beurteilungsraster.setObjectName("radioButton_beurteilungsraster")
        # self.radioButton_beurteilungsraster.setFocusPolicy(QtCore.Qt.ClickFocus)
        # #self.radioButton_beurteilungsraster.toggled.connect(self.beurteilungsraster_changed)
        # self.gridLayout_5.addWidget(self.radioButton_beurteilungsraster, 4, 4, 1, 2)

        self.pushButton_titlepage = QtWidgets.QPushButton(self.groupBox_sage)
        self.pushButton_titlepage.setObjectName(_fromUtf8("pushButton_titlepage"))
        self.pushButton_titlepage.setText(
            _translate("MainWindow", "Titelblatt anpassen")
        )
        self.gridLayout_5.addWidget(self.pushButton_titlepage, 1, 5, 1, 1)
        self.pushButton_titlepage.clicked.connect(
            partial(self.titlepage_clicked, self.dict_titlepage)
        )

        # self.groupBox_default_pkt = QtWidgets.QGroupBox(self.groupBox_sage)
        # self.groupBox_default_pkt.setObjectName("groupBox_default_pkt")
        # self.groupBox_default_pkt.setMaximumSize(QtCore.QSize(120, 16777215))
        # self.verticalLayout_default_pkt = QtWidgets.QVBoxLayout(self.groupBox_default_pkt)
        # self.verticalLayout_default_pkt.setObjectName("verticalLayout_default_pkt")
        # self.spinBox_default_pkt = SpinBox_noWheel(self.groupBox_default_pkt)
        # self.spinBox_default_pkt.setValue(1)
        # self.spinBox_default_pkt.setObjectName("spinBox_default_pkt")
        # self.verticalLayout_default_pkt.addWidget(self.spinBox_default_pkt)
        # #self.spinBox_default_pkt.valueChanged.connect(self.update_default_pkt)
        # self.gridLayout_5.addWidget(self.groupBox_default_pkt, 2, 3, 3, 1)

        self.groupBox_klasse = QtWidgets.QGroupBox(self.groupBox_sage)
        self.groupBox_klasse.setObjectName("groupBox_klasse")

        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_klasse)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lineEdit_klasse = QtWidgets.QLineEdit(self.groupBox_klasse)
        self.lineEdit_klasse.setObjectName("lineEdit_klasse")
        self.verticalLayout_4.addWidget(self.lineEdit_klasse)
        self.gridLayout_5.addWidget(self.groupBox_klasse, 0, 2, 3, 2)
        self.groupBox_klasse.setMaximumSize(QtCore.QSize(90, 100))
        self.groupBox_datum = QtWidgets.QGroupBox(self.groupBox_sage)
        self.groupBox_datum.setObjectName("groupBox_datum")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_datum)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.dateEdit = QtWidgets.QDateEdit(self.groupBox_datum)
        self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit.setObjectName("dateEdit")
        self.verticalLayout_5.addWidget(self.dateEdit)
        self.gridLayout_5.addWidget(self.groupBox_datum, 0, 1, 3, 1)
        self.groupBox_datum.setMaximumSize(QtCore.QSize(140, 100))
        self.groupBox_nummer = QtWidgets.QGroupBox(self.groupBox_sage)
        self.groupBox_nummer.setObjectName("groupBox_nummer")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_nummer)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.spinBox_nummer = QtWidgets.QSpinBox(self.groupBox_nummer)
        self.spinBox_nummer.setValue(1)
        self.spinBox_nummer.setObjectName("spinBox_nummer")
        self.groupBox_nummer.setMaximumSize(QtCore.QSize(90, 100))

        # self.radioButton_notenschl.setText(_translate("MainWindow", "Notenschlüssel"))
        # self.radioButton_beurteilungsraster.setText(_translate("MainWindow", "Beurteilungsraster"))
        self.groupBox_klasse.setTitle(_translate("MainWindow", "Klasse"))
        self.groupBox_datum.setTitle(_translate("MainWindow", "Datum"))
        self.groupBox_nummer.setTitle(_translate("MainWindow", "Nummer"))
        # self.groupBox_default_pkt.setTitle(_translate("MainWindow", "Typ1 Standard"))
        self.verticalLayout_6.addWidget(self.spinBox_nummer)
        self.gridLayout_5.addWidget(self.groupBox_nummer, 0, 0, 3, 2)
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
        self.gridLayout_5.addWidget(self.scrollArea_chosen, 3, 0, 1, 7)

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
        # self.spinBox_3.valueChanged.connect(self.punkte_changed)
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
        # self.spinBox_2.valueChanged.connect(self.punkte_changed)
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
        # self.spinBox_4.valueChanged.connect(self.punkte_changed)
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
        # self.spinBox_5.valueChanged.connect(self.punkte_changed)
        self.spinBox_5.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.gridLayout_6.addWidget(self.spinBox_5, 1, 4, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_notenschl, 6, 0, 1, 7)
        self.groupBox_notenschl.setTitle(_translate("MainWindow", "Notenschlüssel"))
        self.label_sg_pkt.setText(_translate("MainWindow", "% (ab 0)"))
        self.label_g_pkt.setText(_translate("MainWindow", "% (ab 0)"))
        self.label_g.setText(_translate("MainWindow", "Gut:"))
        self.label_sg.setText(_translate("MainWindow", "Sehr Gut:"))
        self.label_b.setText(_translate("MainWindow", "Befriedigend:"))
        self.label_b_pkt.setText(_translate("MainWindow", "% (ab 0)"))
        self.label_g_2.setText(_translate("MainWindow", "Genügend:"))
        self.label_g_pkt_2.setText(_translate("MainWindow", "% (ab 0)"))

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
            _translate("MainWindow", "Beurteilungsraster")
        )
        self.groupBox_beurteilungsra.hide()

        ### Zusammenfassung d. SA ###

        self.label_gesamtbeispiele = QtWidgets.QLabel(self.groupBox_sage)
        self.gridLayout_5.addWidget(self.label_gesamtbeispiele, 7, 0, 1, 3)
        self.label_gesamtbeispiele.setObjectName("label_gesamtbeispiele")
        self.label_gesamtbeispiele.setText(
            _translate("MainWindow", "Anzahl der Aufgaben: 0 (Typ1: 0 / Typ2: 0)	 ")
        )

        self.label_gesamtpunkte = QtWidgets.QLabel(self.groupBox_sage)
        self.gridLayout_5.addWidget(self.label_gesamtpunkte, 8, 0, 1, 1)
        self.label_gesamtpunkte.setObjectName("label_gesamtpunkte")
        self.label_gesamtpunkte.setText(_translate("MainWindow", "Gesamtpunkte: 0"))

        self.cb_solution_sage = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_solution_sage.setObjectName(_fromUtf8("cb_solution"))
        self.cb_solution_sage.setText(_translate("MainWindow", "Lösungen anzeigen"))
        self.cb_solution_sage.setChecked(True)
        self.cb_solution_sage.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.gridLayout_5.addWidget(
            self.cb_solution_sage, 7, 4, 2, 1, QtCore.Qt.AlignRight
        )

        self.cb_drafts_sage = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_drafts_sage.setObjectName(_fromUtf8("cb_drafts_sage"))
        self.gridLayout_5.addWidget(self.cb_drafts_sage, 8, 4, 2, 1)
        self.cb_drafts_sage.setText(_translate("MainWindow", "Entwürfe anzeigen"))
        self.cb_drafts_sage.toggled.connect(self.cb_drafts_sage_enabled)

        self.pushButton_vorschau = QtWidgets.QPushButton(self.groupBox_sage)
        self.pushButton_vorschau.setMaximumSize(QtCore.QSize(90, 16777215))
        self.pushButton_vorschau.setObjectName("pushButton_vorschau")
        self.pushButton_vorschau.setText(_translate("MainWindow", "Vorschau"))
        self.pushButton_vorschau.setShortcut(_translate("MainWindow", "Return"))
        self.gridLayout_5.addWidget(
            self.pushButton_vorschau, 7, 5, 1, 2, QtCore.Qt.AlignRight
        )
        self.pushButton_vorschau.clicked.connect(
            partial(self.pushButton_vorschau_pressed, "vorschau", 0, 0)
        )
        self.pushButton_vorschau.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.gridLayout.addWidget(self.groupBox_sage, 0, 1, 7, 3)

        self.pushButton_erstellen = QtWidgets.QPushButton(self.groupBox_sage)
        self.pushButton_erstellen.setMaximumSize(QtCore.QSize(90, 16777215))
        self.pushButton_erstellen.setObjectName("pushButton_erstellen")
        self.pushButton_erstellen.setText(_translate("MainWindow", "Erstellen"))
        self.pushButton_erstellen.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.pushButton_erstellen.clicked.connect(self.pushButton_erstellen_pressed)
        self.gridLayout_5.addWidget(
            self.pushButton_erstellen, 8, 5, 1, 2, QtCore.Qt.AlignRight
        )
        self.groupBox_sage.hide()

        self.comboBox_klassen_changed("sage")

        # ################################################################
        # ################################################################
        # ########### FEEDBACK #############################################
        # #######################################################################
        self.comboBox_at_fb = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_at_fb.setObjectName("comboBox_at_fb")
        self.comboBox_at_fb.addItem("")
        self.comboBox_at_fb.addItem("")

        self.gridLayout.addWidget(self.comboBox_at_fb, 0, 0, 1, 1)
        self.comboBox_at_fb.setItemText(
            0, _translate("MainWindow", "Aufgaben Rückmeldung")
        )

        self.comboBox_at_fb.setItemText(
            1, _translate("MainWindow", "Allgemeine Rückmeldung")
        )
        self.comboBox_at_fb.currentIndexChanged.connect(self.comboBox_typ_fb_changed)
        self.comboBox_at_fb.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.comboBox_at_fb.hide()

        self.label_example = QtWidgets.QLabel(self.centralwidget)
        self.label_example.setObjectName(_fromUtf8("label_example"))
        # self.label_update.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label_example.setText(_translate("MainWindow", "Ausgewählte Aufgabe: -"))
        self.gridLayout.addWidget(self.label_example, 0, 1, 1, 1)
        self.label_example.hide()

        self.groupBox_alle_aufgaben_fb = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_alle_aufgaben_fb.setMinimumWidth(100)
        # self.groupBox_alle_aufgaben_fb.resize(QtCore.QSize(140, 100))
        # self.groupBox_alle_aufgaben_fb.setMaximumSize(QtCore.QSize(300, 16777215))
        self.groupBox_alle_aufgaben_fb.setObjectName("groupBox_alle_aufgaben_fb")
        self.verticalLayout_fb = QtWidgets.QVBoxLayout(self.groupBox_alle_aufgaben_fb)
        self.verticalLayout_fb.setObjectName("verticalLayout_fb")
        self.comboBox_klassen_fb = QtWidgets.QComboBox(self.groupBox_alle_aufgaben_fb)
        self.comboBox_klassen_fb.setObjectName("self.comboBox_klassen_fb")

        i = 0
        for all in list_klassen:

            self.comboBox_klassen_fb.addItem("")

            self.comboBox_klassen_fb.setItemText(
                i, _translate("MainWindow", all[1] + ". Klasse")
            )
            i += 1

        self.comboBox_klassen_fb.currentIndexChanged.connect(
            partial(self.comboBox_klassen_changed, "feedback")
        )

        self.comboBox_klassen_fb.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.verticalLayout_fb.addWidget(self.comboBox_klassen_fb)
        self.comboBox_kapitel_fb = QtWidgets.QComboBox(self.groupBox_alle_aufgaben_fb)
        self.comboBox_kapitel_fb.setObjectName("self.comboBox_kapitel_fb")

        self.comboBox_kapitel_fb.currentIndexChanged.connect(
            partial(self.comboBox_kapitel_changed, "feedback")
        )
        self.comboBox_kapitel_fb.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.verticalLayout_fb.addWidget(self.comboBox_kapitel_fb)
        # self.comboBox_kapitel_fb.addItem("")
        # self.comboBox_kapitel_fb.setItemText(0, _translate("MainWindow", "Testtest"))

        self.comboBox_unterkapitel_fb = QtWidgets.QComboBox(
            self.groupBox_alle_aufgaben_fb
        )
        self.comboBox_unterkapitel_fb.setObjectName("self.comboBox_unterkapitel_fb")

        self.comboBox_unterkapitel_fb.currentIndexChanged.connect(
            partial(self.comboBox_unterkapitel_changed, "feedback")
        )
        self.comboBox_unterkapitel_fb.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.verticalLayout_fb.addWidget(self.comboBox_unterkapitel_fb)

        self.lineEdit_number_fb = QtWidgets.QLineEdit(self.groupBox_alle_aufgaben_fb)
        self.lineEdit_number_fb.setObjectName("lineEdit_number_fb")

        self.lineEdit_number_fb.textChanged.connect(
            partial(self.adapt_choosing_list, "feedback")
        )
        self.verticalLayout_fb.addWidget(self.lineEdit_number_fb)
        self.listWidget_fb = QtWidgets.QListWidget(self.groupBox_alle_aufgaben)
        self.listWidget_fb.setObjectName("listWidget")
        self.verticalLayout_fb.addWidget(self.listWidget_fb)
        self.gridLayout.addWidget(self.groupBox_alle_aufgaben_fb, 1, 0, 3, 1)
        self.groupBox_alle_aufgaben_fb.setTitle(_translate("MainWindow", "Aufgaben"))
        self.groupBox_alle_aufgaben_fb.hide()

        self.comboBox_klassen_changed("feedback")

        self.groupBox_fehlertyp = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_fehlertyp.setObjectName("groupBox_fehlertyp")
        self.gridLayout_fehlertyp = QtWidgets.QGridLayout(self.groupBox_fehlertyp)
        self.gridLayout_fehlertyp.setObjectName("gridLayout_feedback")
        self.groupBox_fehlertyp.setTitle(_translate("MainWindow", "Betreff"))

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
        self.comboBox_fehlertyp.setItemText(1, _translate("MainWindow", "Feedback"))
        self.comboBox_fehlertyp.setItemText(
            2, _translate("MainWindow", "Fehler in der Angabe")
        )
        self.comboBox_fehlertyp.setItemText(
            3, _translate("MainWindow", "Fehler in der Lösung")
        )
        self.comboBox_fehlertyp.setItemText(
            4, _translate("MainWindow", "Bild wird nicht (richtig) angezeigt")
        )
        self.comboBox_fehlertyp.setItemText(
            5, _translate("MainWindow", "Grafik ist unleserlich/fehlerhaft")
        )
        self.comboBox_fehlertyp.setItemText(
            6, _translate("MainWindow", "Beispiel ist doppelt vorhanden")
        )
        self.comboBox_fehlertyp.setItemText(
            7,
            _translate(
                "MainWindow", "Falsche Kodierung (Themengebiet, Aufgabenformat, ...)"
            ),
        )
        self.comboBox_fehlertyp.setItemText(8, _translate("MainWindow", "Sonstiges"))

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
        self.plainTextEdit_fb.setMinimumWidth(600)
        self.gridLayout_fb.addWidget(self.plainTextEdit_fb, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_feedback, 2, 1, 1, 3)
        self.groupBox_feedback.setTitle(
            _translate("MainWindow", "Feedback bzw. Problembeschreibung")
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
            _translate("MainWindow", "Kontakt (E-Mail) für Nachfragen (optional)")
        )
        self.verticalLayout_email.addWidget(self.lineEdit_email)
        self.gridLayout.addWidget(self.groupBox_email, 3, 1, 1, 3)
        self.groupBox_email.hide()

        self.pushButton_send = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_send.setObjectName(_fromUtf8("pushButton_send"))
        self.gridLayout.addWidget(
            self.pushButton_send, 4, 3, 1, 1, QtCore.Qt.AlignRight
        )
        self.pushButton_send.setText(_translate("MainWindow", "Senden"))
        self.pushButton_send.clicked.connect(self.pushButton_send_pressed)
        self.pushButton_send.hide()

        ###################################################################
        ####################################################################
        #####################################################################
        ####################################################################

        # self.gridLayout_11.addWidget(self.tab_widget_gk, 0, 0, 1, 1)
        # self.gridLayout.addWidget(self.groupBox_gk, 1, 3, 2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        # self.actionReset = QtWidgets.QAction(MainWindow)
        # self.actionReset.setObjectName(_fromUtf8("actionReset"))

        self.retranslateUi(MainWindow)
        # self.tabWidget.setCurrentIndex(0)

        self.tab_widget_gk_cr.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        if loaded_lama_file_path != "":
            self.sage_load(True)

        print("Done")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(
            _translate(
                "LaMA-Cria - LaTeX Mathematik Assistent Unterstufe",
                "LaMA-Cria - LaTeX Mathematik Assistent Unterstufe",
            )
        )
        self.groupBox_unterkapitel.setTitle(_translate("MainWindow", "Unterkapitel"))
        self.groupBox_schulstufe.setTitle(_translate("MainWindow", "Themen Schulstufe"))

        self.groupBox_ausgew_gk.setTitle(_translate("MainWindow", "Ausgewählte Themen"))
        # self.label_ausg_themen.setText(_translate("MainWindow", "-"))
        self.groupBox_titelsuche.setTitle(_translate("MainWindow", "Titelsuche:"))
        try:
            log_file = os.path.join(path_programm, "Teildokument", "log_file")
            self.label_update.setText(
                _translate(
                    "MainWindow",
                    "Letztes Update: "
                    + self.modification_date(log_file).strftime("%d.%m.%y - %H:%M"),
                )
            )
        except FileNotFoundError:
            self.label_update.setText(_translate("MainWindow", "Letztes Update: ---"))
        # self.label_update.setText(_translate("MainWindow", "Letztes Update: ---"))
        self.combobox_searchtype.setItemText(
            0,
            _translate(
                "MainWindow",
                "Alle Dateien ausgeben, die zumindest ein Suchkriterium enthalten",
            ),
        )

        self.combobox_searchtype.setItemText(
            1,
            _translate(
                "MainWindow", "Alle Dateien ausgeben, die alle Suchkriterien enthalten"
            ),
        )
        self.cb_solution.setText(_translate("MainWindow", "Lösungen anzeigen"))
        self.cb_drafts.setText(_translate("MainWindow", "Entwürfe anzeigen"))
        self.btn_suche.setText(_translate("MainWindow", "Suche starten!"))
        self.btn_suche.setShortcut(_translate("MainWindow", "Return"))
        self.menuFeedback.setTitle(_translate("MainWindow", "Feedback && Fehler"))
        self.actionFeedback.setText(
            _translate("MainWindow", "Feedback oder Fehler senden ...")
        )
        self.menuBild_einf_gen.setTitle(_translate("MainWindow", "Bild einfügen"))
        self.actionBild_einf_gen.setText(_translate("MainWindow", "Durchsuchen..."))
        self.menuSuche.setTitle(_translate("MainWindow", "Aufgabensuche"))
        self.actionSuche.setText(_translate("MainWindow", "Aufgaben suchen..."))
        self.actionSuche.setShortcut("F1")
        self.actionBild_konvertieren_jpg_eps.setText(
            _translate("MainWindow", "Bild konvertieren (jpg zu eps)")
        )
        self.groupBox_af.setTitle(_translate("MainWindow", "Gesuchte Aufgabenformate:"))
        self.cb_af_lt.setText(_translate("MainWindow", "Lückentext (LT)"))
        self.cb_af_mc.setText(_translate("MainWindow", "Multiplechoice (MC)"))
        self.cb_af_zo.setText(_translate("MainWindow", "Zuordnungsformat (ZO)"))
        self.cb_af_ta.setText(_translate("MainWindow", "Textaufgaben (TA)"))
        self.cb_af_oa.setText(_translate("MainWindow", "Offenes Antwortformat (OA)"))
        self.cb_af_rf.setText(_translate("MainWindow", "Richtig/Falsch-Format (RF)"))
        self.cb_af_ko.setText(_translate("MainWindow", "Konstruktion (KO)"))
        self.menuDatei.setTitle(_translate("MainWindow", "Datei"))
        self.menuNeue_Schularbeit.setTitle(_translate("MainWindow", "Neue Schularbeit"))
        self.menuNeue_Aufgabe.setTitle(_translate("MainWindow", "Neue Aufgabe"))
        self.actionNew.setText(_translate("MainWindow", "Reset"))
        self.actionAufgaben_Typ1.setText(_translate("MainWindow", "Typ 1 Aufgaben"))
        self.actionTyp_2_Aufgaben.setText(_translate("MainWindow", "Typ 2 Aufgaben"))
        self.actionReset.setText(_translate("MainWindow", "Reset"))
        self.actionReset_sage.setText(_translate("MainWindow", "Reset Schularbeit"))
        self.actionReset.setShortcut(_translate("MainWindow", "F4"))
        self.actionLoad.setText(_translate("MainWindow", "Öffnen"))
        self.actionLoad.setShortcut("Ctrl+O")
        self.actionSave.setText(_translate("MainWindow", "Speichern"))
        self.actionSave.setShortcut("Ctrl+S")

        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionRefresh_Database.setText(
            _translate("MainWindow", "Refresh Database")
        )
        self.actionRefresh_Database.setShortcut(_translate("MainWindow", "F5"))
        self.actionNeue_Schularbeit_erstellen.setText(
            _translate("MainWindow", "Neue Schularbeit erstellen...")
        )

        self.actionNeue_Schularbeit_erstellen.setShortcut(
            _translate("MainWindow", "F2")
        )

        self.actionNeue_Aufgabe_erstellen.setText(
            _translate("MainWindow", "Neue Aufgabe erstellen...")
        )

        self.actionNeue_Aufgabe_erstellen.setShortcut(_translate("MainWindow", "F3"))

        self.menuHelp.setTitle(_translate("MainWindow", "?"))
        self.actionInfo.setText(_translate("MainWindow", "Über LaMA-Cria"))

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

                filename_update = os.path.join(
                    path_programm,
                    "_database",
                    "_config",
                    "update",
                    "update_cria%s" % extension,
                )

                try:
                    if sys.platform.startswith("linux") or sys.platform.startswith(
                        "darwin"
                    ):
                        if extension=='.py':
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

        #msg.setIcon(QtWidgets.QMessageBox.Information)
        pixmap = QtGui.QPixmap(logo_path)


        msg.setIconPixmap(pixmap.scaled(110, 110, QtCore.Qt.KeepAspectRatio))
        msg.setWindowIcon(QtGui.QIcon(logo_path))
        msg.setText("LaMA-Cria - LaTeX Mathematik Assistent Unterstufe %s \n\n"
        "Authors: Christoph Weberndorfer, Matthias Konzett\n\n"
        "License: GNU General Public License v3.0  \n\n"	
        "Credits: David Fischer	"%__version__)
        msg.setInformativeText("Logo & Icon: Lisa Schultz")
        msg.setWindowTitle("Über LaMA - LaTeX Mathematik Assistent Unterstufe")
        #msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def reset_window(self):
        global dict_picture_path
        self.dict_chosen_topics = {}
        for klasse in list_klassen:
            dict_klasse_name = eval("dict_{}_name".format(klasse))
            for all in dict_klasse_name:
                radioButton = eval("self.radioButton_{0}_{1}".format(klasse, all))
                if radioButton.isChecked() == True:
                    radioButton.setAutoExclusive(False)
                    radioButton.setChecked(False)
                    radioButton.setAutoExclusive(True)

        try:
            self.scrollArea_unterkapitel.hide()
        except AttributeError:

            pass
        self.groupBox_unterkapitel.setTitle(_translate("MainWindow", "Unterkapitel"))
        self.label_ausg_themen.setText(_translate("MainWindow", ""))
        self.tabWidget_klassen.setCurrentIndex(0)

        for example in self.list_creator_topics[:]:
            cb_unterkapitel = eval(
                "self.cb_unterkapitel_{0}_{1}".format(example[1], example[2])
            )
            cb_unterkapitel.setChecked(False)

        ### Reset Images ###
        for i in range(len(dict_picture_path)):
            eval("self.label_bild_" + str(i) + ".setParent(None)")
        dict_picture_path = {}
        self.label_bild_leer.show()

        self.spinBox_punkte.setValue(1)
        self.comboBox_af.setCurrentIndex(0)
        if self.lineEdit_titel.text().startswith("###"):
            self.lineEdit_titel.setText(_translate("MainWindow", "###"))
        else:
            self.lineEdit_titel.setText(_translate("MainWindow", ""))
        self.lineEdit_quelle.setText(_translate("MainWindow", ""))
        self.plainTextEdit.setPlainText(_translate("MainWindow", ""))


    def reset_sage(self):
        global list_sage_examples
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
            self.spinBox_2.setProperty("value", 91)
            self.spinBox_3.setProperty("value", 80)
            self.spinBox_4.setProperty("value", 64)
            self.spinBox_5.setProperty("value", 50)
            self.comboBox_klassen.setCurrentIndex(0)
            self.comboBox_kapitel.setCurrentIndex(0)
            self.comboBox_unterkapitel.setCurrentIndex(0)
            self.lineEdit_number.setText("")
            self.dict_list_input_examples = {}
            for all in list_sage_examples:
                exec("self.groupBox_bsp_{}.setParent(None)".format(all))
            list_sage_examples=[]
            #self.sage_aufgabe_create(False)
           


    def tab_changed(self):
        klasse = list_klassen[self.tabWidget_klassen.currentIndex()]
        dict_klasse_name = eval("dict_{}_name".format(klasse))

        for all in dict_klasse_name:
            radioButton = eval("self.radioButton_{0}_{1}".format(klasse, all))
            if radioButton.isChecked() == True:
                self.chosen_radiobutton(klasse[1], all)
                break
            else:
                try:
                    self.scrollArea_unterkapitel.setParent(None)
                    self.groupBox_unterkapitel.setTitle(
                        _translate("MainWindow", "Unterkapitel")
                    )
                except AttributeError:
                    pass

                pass

    def create_kapitel(self, layout, klasse, kapitel):
        dict_klasse_name = eval("dict_k{}_name".format(klasse))
        exec(
            "self.radioButton_k{0}_{1} = QtWidgets.QRadioButton(self.scrollAreaWidgetContents_k{0})".format(
                klasse, kapitel
            )
        )
        radioButton_klasse_kapitel = eval(
            "self.radioButton_k{0}_{1}".format(klasse, kapitel)
        )
        radioButton_klasse_kapitel.setObjectName("radioButton_klasse_kapitel")
        # chosen_layout = eval('{0}_k{1}'.format(layout, klasse))
        layout.addWidget(radioButton_klasse_kapitel)
        radioButton_klasse_kapitel.setText(
            _translate("MainWindow", dict_klasse_name[kapitel] + " (" + kapitel + ")")
        )
        radioButton_klasse_kapitel.toggled.connect(
            partial(self.chosen_radiobutton, klasse, kapitel)
        )

    def chosen_radiobutton(self, klasse, kapitel):
        dict_klasse_name = eval("dict_k{}_name".format(klasse))
        self.groupBox_unterkapitel.setTitle(
            _translate(
                "MainWindow",
                "Unterkapitel - "
                + str(klasse)
                + ". Klasse - "
                + dict_klasse_name[kapitel],
            )
        )

        try:
            self.scrollArea_unterkapitel.setParent(None)
        except AttributeError:
            pass

        self.scrollArea_unterkapitel = QtWidgets.QScrollArea(self.groupBox_unterkapitel)
        self.scrollArea_unterkapitel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_unterkapitel.setWidgetResizable(True)
        self.scrollArea_unterkapitel.setObjectName("scrollArea_unterkapitel")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 320, 279))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        dict_klasse = eval("dict_k{}".format(klasse))
        for all in dict_klasse[kapitel]:
            # print(dict_unterkapitel[all])

            exec(
                "self.checkBox_k{0}_{1}_{2} = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)".format(
                    klasse, kapitel, all
                )
            )
            checkBox = eval("self.checkBox_k{0}_{1}_{2}".format(klasse, kapitel, all))
            checkBox.setObjectName("checkBox_k{0}_{1}_{2}".format(klasse, kapitel, all))
            checkBox.stateChanged.connect(
                partial(self.checkBox_checked, klasse, kapitel, all)
            )

            thema_checked = [klasse, kapitel, all]
            if thema_checked in self.dict_chosen_topics.values():
                checkBox.setChecked(True)

            self.verticalLayout_4.addWidget(checkBox)

            checkBox.setText(_translate("MainWindow", dict_unterkapitel[all]))

        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_4.addItem(spacerItem)

        exec(
            "self.btn_alle_{0}_{1} = QtWidgets.QPushButton(self.scrollAreaWidgetContents)".format(
                klasse, kapitel
            )
        )
        btn_alle = eval("self.btn_alle_{0}_{1}".format(klasse, kapitel))
        btn_alle.setStyleSheet("background-color: rgb(240, 240, 240);")
        btn_alle.setObjectName("btn_alle_{0}_{1}".format(klasse, kapitel))
        btn_alle.setText(_translate("MainWindow", "alle auswählen"))
        btn_alle.clicked.connect(partial(self.btn_alle_clicked, klasse, kapitel))
        self.verticalLayout_4.addWidget(btn_alle, 0, QtCore.Qt.AlignLeft)
        self.scrollArea_unterkapitel.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_11.addWidget(self.scrollArea_unterkapitel, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_unterkapitel, 1, 2, 2, 1)

    def checkBox_checked(self, klasse, kapitel, unterkapitel):
        thema_checked = [klasse, kapitel, unterkapitel]
        thema_label = kapitel + "." + unterkapitel + " (" + klasse + ".)"
        checkBox = eval(
            "self.checkBox_k{0}_{1}_{2}".format(klasse, kapitel, unterkapitel)
        )
        if checkBox.isChecked() == True:
            if thema_label not in self.dict_chosen_topics.keys():
                self.dict_chosen_topics[thema_label] = thema_checked
        if checkBox.isChecked() == False:
            del self.dict_chosen_topics[thema_label]
        x = ", ".join(self.dict_chosen_topics.keys())
        # print(self.dict_chosen_topics)
        self.label_ausg_themen.setText(_translate("MainWindow", x))

    def btn_alle_clicked(self, klasse, kapitel):
        dict_klasse = eval("dict_k{}".format(klasse))
        check = 0
        for all in dict_klasse[kapitel]:
            checkBox = eval("self.checkBox_k{0}_{1}_{2}".format(klasse, kapitel, all))
            if check == 0:
                if checkBox.isChecked():
                    checkBox.setChecked(False)
                    check = 1
                else:
                    checkBox.setChecked(True)
                    check = 2
            else:
                if check == 1:
                    checkBox.setChecked(False)
                elif check == 2:
                    checkBox.setChecked(True)

    def modification_date(self, filename):
        t = os.path.getmtime(filename)
        return datetime.datetime.fromtimestamp(t)

    # def atoi(self, text):
    #     return int(text) if text.isdigit() else text

    # def natural_keys(self, text):
    #     return [self.atoi(c) for c in re.split("(\d+)", text)]

    def refresh_ddb(self):
        msg = QtWidgets.QMessageBox()
        msg.setWindowIcon(QtGui.QIcon(logo_path))
        msg.setWindowTitle("Refresh Database...")
        msg.setStandardButtons(QtWidgets.QMessageBox.NoButton)
        msg.setText("Datenbank wird aktualisiert. Bitte warten...")

        msg.show()
        QApplication.processEvents()
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        beispieldaten_dateipfad = {}
        beispieldaten = []

        ########################################################
        ##### Suche offizielle Beispiele ####################
        ##################################################

        for klasse in list_klassen:
            for root, dirs, files in os.walk(
                os.path.join(path_programm, "_database", klasse)
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

        # 	################################################
        # 	#### Suche inoffizielle Beispiele ######
        # 	#############################################

            for root, dirs, files in os.walk(os.path.join(path_programm,'_database_inoffiziell', klasse)):
                for all in files:
                    if all.endswith('.tex') or all.endswith('.ltx'):
                        if not ('Gesamtdokument' in all) and not ('Teildokument' in all):
                            file=open(os.path.join(root,all),encoding='utf8')
                            for i, line in enumerate(file):
                                if not line == "\n":
                                    beispieldaten_dateipfad[line]=os.path.join(root,all)
                                    beispieldaten.append(line)
                                    break
                            file.close()

        ################################################
        #### Suche lokal gespeicherte Beispiele ######
        #############################################

            for root, dirs, files in os.walk(
                os.path.join(path_programm, "Lokaler_Ordner", klasse)
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

        log_file = os.path.join(path_programm, "Teildokument", "log_file")

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
            )
        )
        QtWidgets.QApplication.restoreOverrideCursor()
        self.adapt_choosing_list("sage")
        self.adapt_choosing_list("feedback")
        msg.close()

    ############################################################################
    ############################################################################


    def create_pdf(self, dateiname, index, maximum):
        if sys.platform.startswith("linux"):
            pass
        else:
            msg = QtWidgets.QMessageBox()
            msg.setWindowIcon(QtGui.QIcon(logo_path))
            msg.setWindowTitle("Lade...")
            msg.setStandardButtons(QtWidgets.QMessageBox.NoButton)
            if dateiname == "Teildokument" or dateiname == "Schularbeit_Vorschau":
                rest = ""
            else:

                rest = " ({0}|{1})".format(index + 1, maximum)
            msg.setText("Die PDF Datei wird erstellt..." + rest)

            msg.show()
            QApplication.processEvents()
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        if dateiname == "Teildokument":
            pass
        # 	dateiname=dateiname+'_'+self.label_aufgabentyp.text()[-1]

        else:
            head, tail = os.path.split(dateiname)
            save_file = head
            dateiname = tail

        if dateiname == "Schularbeit_Vorschau" or dateiname.startswith("Teildokument"):
            if sys.platform.startswith("linux"):
                subprocess.Popen(
                    'cd "{0}/Teildokument" ; latex --synctex=-1 {1}.tex ; dvips {1}.dvi ; ps2pdf -dNOSAFER {1}.ps'.format(
                        path_programm, dateiname
                    ),
                    shell=True,
                ).wait()
                subprocess.run(
                    [   "sudo",
                        "xdg-open",
                        "{0}/Teildokument/{1}.pdf".format(path_programm, dateiname),
                    ]
                )
            elif sys.platform.startswith("darwin"):
                subprocess.Popen(
                    'cd "{0}/Teildokument" ; latex --synctex=-1 {1}.tex ; dvips {1}.dvi ; ps2pdf -dNOSAFER {1}.ps'.format(
                        path_programm, dateiname
                    ),
                    shell=True,
                ).wait()
                subprocess.run(
                    [
                        "open",
                        "{0}/Teildokument/{1}.pdf".format(path_programm, dateiname),
                    ]
                )
            else:
                if os.path.isfile(
                    os.path.join(
                        "C:\\", "Program Files", "SumatraPDF", "SumatraPDF.exe"
                    )
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
                    'cd "{0}/Teildokument" & latex --synctex=-1 "{1}.tex"& dvips "{1}.dvi" & ps2pdf -dNOSAFER "{1}.ps"'.format(
                        path_programm, dateiname
                    ),
                    shell=True,
                ).wait()

                subprocess.Popen(
                    'cd "{0}/Teildokument" &"{1}" "{2}.pdf"'.format(
                        path_programm, sumatrapdf, dateiname
                    ),
                    shell=True,
                ).poll()

            os.unlink("{0}/Teildokument/{1}.aux".format(path_programm, dateiname))
            os.unlink("{0}/Teildokument/{1}.log".format(path_programm, dateiname))
            os.unlink("{0}/Teildokument/{1}.dvi".format(path_programm, dateiname))
            os.unlink("{0}/Teildokument/{1}.ps".format(path_programm, dateiname))

        else:
            if sys.platform.startswith("linux"):
                subprocess.Popen(
                    'cd "{0}" ; latex --synctex=-1 {1}.tex ; dvips {1}.dvi ; ps2pdf -dNOSAFER {1}.ps'.format(
                        save_file, dateiname
                    ),
                    shell=True,
                ).wait()
            elif sys.platform.startswith("darwin"):

                subprocess.Popen(
                    'cd "{0}" ; latex --synctex=-1 {1}.tex ; dvips {1}.dvi ; ps2pdf -dNOSAFER {1}.ps'.format(
                        save_file, dateiname
                    ),
                    shell=True,
                ).wait()
            else:
                subprocess.Popen(
                    'cd "{0}" & latex --synctex=-1 "{1}.tex"& dvips "{1}.dvi" & ps2pdf -dNOSAFER "{1}.ps"'.format(
                        save_file, dateiname
                    ),
                    shell=True,
                ).wait()

            os.unlink("{0}/{1}.aux".format(save_file, dateiname))
            os.unlink("{0}/{1}.log".format(save_file, dateiname))
            os.unlink("{0}/{1}.dvi".format(save_file, dateiname))
            os.unlink("{0}/{1}.ps".format(save_file, dateiname))
            os.unlink("{0}/{1}.synctex".format(save_file, dateiname))

        msg.close()

        QtWidgets.QApplication.restoreOverrideCursor()


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

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        if not os.path.isfile(os.path.join(path_programm, "Teildokument", "log_file")):
            self.refresh_ddb()  # self.label_aufgabentyp.text()[-1]
        else:  ##  Automatic update once per month
            log_file = os.path.join(path_programm, "Teildokument", "log_file")
            month_update_log_file = self.modification_date(log_file).strftime("%m")
            month_today = datetime.date.today().strftime("%m")
            if month_today != month_update_log_file:
                self.refresh_ddb()  # self.label_aufgabentyp.text()[-1]

        log_file = os.path.join(path_programm, "Teildokument", "log_file")

        with open(log_file, encoding="utf8") as f:
            beispieldaten_dateipfad = json.load(f)

            beispieldaten = list(beispieldaten_dateipfad.keys())


        if self.cb_drafts.isChecked():
            #print(beispieldaten_dateipfad)
            QtWidgets.QApplication.restoreOverrideCursor()
            drafts_path = os.path.join(path_programm, "Beispieleinreichung")
            for klasse in list_klassen:
                try:
                    drafts_path = os.path.join(path_programm, "Beispieleinreichung",klasse)
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

        suchbegriffe = []
        # print(self.dict_chosen_topics)
        for all in self.dict_chosen_topics.values():
            suchbegriffe.append(all)

        filename_teildokument = os.path.join(
            path_programm, "Teildokument", "Teildokument.tex"
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

        # print(suchbegriffe)

        gesammeltedateien = []

        if (
            self.combobox_searchtype.currentText()
            == "Alle Dateien ausgeben, die zumindest ein Suchkriterium enthalten"
        ):
            for item in suchbegriffe:
                klasse = "K" + item[0]
                thema = item[1] + "." + item[2]

                for all in list(beispieldaten_dateipfad.keys()):
                    if klasse in all:

                        if thema in all:
                            gesammeltedateien.append(all)

        if (
            self.combobox_searchtype.currentText()
            == "Alle Dateien ausgeben, die alle Suchkriterien enthalten"
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

        gesammeltedateien.sort(key=natural_keys)

        dict_gesammeltedateien = {}

        for all in gesammeltedateien:
            dict_gesammeltedateien[all] = beispieldaten_dateipfad[all]

        # ###############################################
        # #### Auswahl der gesuchten Antwortformate ####
        # ###############################################
        # list_antwortformate=['mc','lt','ta','rf','zo','oa']

        if (
            self.cb_af_mc.isChecked()
            or self.cb_af_lt.isChecked()
            or self.cb_af_zo.isChecked()
            or self.cb_af_oa.isChecked() == True
        ):
            if suchbegriffe == []:
                dict_gesammeltedateien = beispieldaten_dateipfad
            for all_formats in dict_aufgabenformate.keys():
                checkBox_af = eval("self.cb_af_" + all_formats)
                if checkBox_af.isChecked() == False:
                    for all in list(dict_gesammeltedateien):
                        if all_formats.upper() in all:
                            del dict_gesammeltedateien[all]

                if checkBox_af.isChecked() == True:
                    suchbegriffe.append(all_formats)

        # print(dict_gesammeltedateien)

        if not dict_gesammeltedateien:
            QtWidgets.QApplication.restoreOverrideCursor()
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowIcon(QtGui.QIcon(logo_path))
            msg.setText("Es wurden keine passenden Beispiele gefunden!")
            msg.setInformativeText("Es wird keine Datei ausgegeben.")
            msg.setWindowTitle("Warnung")
            # msg.setDetailedText("The details are as follows:")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            return

        beispieldaten.sort(key=natural_keys)
        file = open(filename_teildokument, "a", encoding="utf8")
        file.write("\n \\scriptsize Suchbegriffe: ")
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
            + " Beispiele gefunden.\n "
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

            self.create_pdf("Teildokument", 0, 0)

    ############################################################################
    ######################## BEFEHLE CREATOR ###########################################
    ############################################################################

    def create_checkbox_unterkapitel(self, layout, klasse, kapitel, unterkapitel):
        # exec('self.tab_cr_{} = QtWidgets.QWidget()'.format(all))
        # exec('self.tab_cr_{0}.setObjectName("tab_cr_{0}")'.format(all))
        exec(
            "self.cb_unterkapitel_{0}_{1}= QtWidgets.QCheckBox(self.centralwidget)".format(
                kapitel, unterkapitel
            )
        )
        cb_unterkapitel = eval(
            "self.cb_unterkapitel_{0}_{1}".format(kapitel, unterkapitel)
        )
        # self.cb_thema.setChecked(True)
        cb_unterkapitel.setObjectName(
            "cb_unterkapitel_{0}_{1}".format(kapitel, unterkapitel)
        )
        layout.addWidget(cb_unterkapitel, QtCore.Qt.AlignTop)
        cb_unterkapitel.setText(
            _translate(
                "MainWindow",
                dict_unterkapitel[unterkapitel] + " (" + unterkapitel + ")",
            )
        )
        cb_unterkapitel.stateChanged.connect(
            partial(
                self.checkBox_checked_creator,
                cb_unterkapitel,
                klasse,
                kapitel,
                unterkapitel,
            )
        )
        aufgabe_chosen = [klasse, kapitel, unterkapitel]
        if aufgabe_chosen in self.list_creator_topics:
            cb_unterkapitel.setChecked(True)

    def comboBox_kapitel_changed_cr(
        self, verticalLayout_cr, combobox_kapitel, klasse, spacerItem_unterkapitel
    ):
        # spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        verticalLayout_cr.removeItem(spacerItem_unterkapitel)
        dict_klasse = eval("dict_{}".format(klasse))
        chosen_kapitel = list(dict_klasse.keys())[combobox_kapitel.currentIndex()]

        for i in reversed(range(2, verticalLayout_cr.count())):
            verticalLayout_cr.itemAt(i).widget().close()

        for unterkapitel in dict_klasse[chosen_kapitel]:
            self.create_checkbox_unterkapitel(
                verticalLayout_cr, klasse, chosen_kapitel, unterkapitel
            )

        verticalLayout_cr.addItem(spacerItem_unterkapitel)

    def checkBox_checked_creator(self, cb_unterkapitel, klasse, kapitel, unterkapitel):
        thema_checked = [klasse, kapitel, unterkapitel]
        if cb_unterkapitel.isChecked():
            if thema_checked not in self.list_creator_topics:
                self.list_creator_topics.append(thema_checked)
        if cb_unterkapitel.isChecked() == False:
            self.list_creator_topics.remove(thema_checked)

        list_labels = []
        for all in self.list_creator_topics:
            thema_label = all[1] + "." + all[2] + " (" + all[0][1] + ".)"
            list_labels.append(thema_label)
        x = ", ".join(list_labels)
        self.label_ausgew_gk.setText(_translate("MainWindow", x))

    def add_picture(self):
        try:
            os.path.dirname(self.saved_file_path[0])
        except AttributeError:
            self.saved_file_path = path_programm
        list_filename = QtWidgets.QFileDialog.getOpenFileNames(
            None,
            "Grafiken auswählen",
            os.path.dirname(self.saved_file_path[0]),
            "Grafiken (*.eps)",
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
                eval(x).setText(_translate("MainWindow", tail))
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

        if self.list_creator_topics == []:
            self.warning_window("Es wurden keine Themengebiete zugewiesen.")
            return

        if self.comboBox_af.currentText() == "bitte auswählen":
            self.warning_window("Es wurde kein Aufgabenformat ausgewählt.")

            return

        textBox_Entry = self.plainTextEdit.toPlainText()
        # list_chosen_gk=list(set_chosen_gk)

        # ####### CHECK INCL. & ATTACHED IMAGE RATIO ####

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

        # ###############################
        # ###### Check if Admin Mode is activated ####

        if self.lineEdit_titel.text().startswith("###"):
            try:
                x, y = self.lineEdit_titel.text().split("### ")
            except ValueError:
                x, y = self.lineEdit_titel.text().split("###")
            self.creator_mode = "admin"
            edit_titel = y
        else:
            edit_titel = self.lineEdit_titel.text()
        # ################################################

        QtWidgets.QApplication.restoreOverrideCursor()
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowIcon(QtGui.QIcon(logo_path))

        list_labels = []
        for all in self.list_creator_topics:
            thema_label = all[1] + "." + all[2] + " (" + all[0][1] + ".)"
            list_labels.append(thema_label)
        themen = ", ".join(list_labels)

        if dict_picture_path != {}:
            bilder = ", ".join(dict_picture_path)
        else:
            bilder = "-"

        if self.creator_mode == "user":
            local_save = False
            aufgabenformat = "Aufgabenformat: %s\n" % self.comboBox_af.currentText()

            msg.setWindowTitle("Aufgabe speichern")
            msg.setText(
                "Sind Sie sicher, dass Sie die folgendene Aufgabe speichern wollen?\n\n"
                "Titel: {0}\n{1}"
                "Themengebiet(e): {2}\n"
                "Quelle: {3}\n"
                "Bilder: {4}\n".format(
                    edit_titel,
                    aufgabenformat,
                    themen,
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
            msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Apply| QtWidgets.QMessageBox.No)
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
                if ret_personal == QtWidgets.QMessageBox.No:
                    # ret=msg.exec_()
                    return
            else:
                return

        if self.creator_mode == "admin":

            aufgabenformat = "Aufgabenformat: %s\n" % self.comboBox_af.currentText()

            msg.setWindowTitle("Admin Modus - Aufgabe speichern")
            msg.setText(
                "Sind Sie sicher, dass Sie die folgendene Aufgabe speichern wollen?\n\n"
                "Titel: {0}\n{1}"
                "Themengebiet(e): {2}\n"
                "Quelle: {3}\n"
                "Bilder: {4}\n".format(
                    edit_titel,
                    aufgabenformat,
                    themen,
                    self.lineEdit_quelle.text(),
                    bilder,
                )
            )
            self.cb_save=QtWidgets.QCheckBox("inoffizielle Aufgabe")
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

        # print(list_klassen)
        # print(self.list_creator_topics)
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

        # print(max_integer_file)

        # ####### Checks files in 'Beispieleinreichung' #####
        # ##################################################

        klasse = "k" + str(highest_grade)
        if local_save == True:
            pass
        else:    
            try:
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
                    'Der Ordner "Beispieleinreichung" konnte nicht gefunden werden und muss zuerst für Sie freigegeben werden.'
                )
                msg.setInformativeText(
                    "Derzeit können keine neuen Aufgaben eingegeben werden."
                )
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.exec_()
                return


        # ############################################################################

        for all in dict_picture_path:
            head, tail = os.path.split(all)
            x = "{" + tail + "}"
            #name, ext = os.path.splitext(tail)
            #print(self.creator_mode, self.cb_save.isChecked())
            if self.creator_mode == "admin" and self.cb_save.isChecked() == True:
                str_image_path = "../_database_inoffiziell/Bilder/"
            elif self.creator_mode == "admin" and self.cb_save.isChecked() == False:
                str_image_path = "../_database/Bilder/"
            elif local_save == True:
                str_image_path = "../Lokaler_Ordner/Bilder/"
            else:
                str_image_path = "../Beispieleinreichung/Bilder/"

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


        if self.creator_mode == "admin" and self.cb_save.isChecked() == True:
            copy_image_path = os.path.join(
                path_programm, "_database_inoffiziell", "Bilder"
            )  ### direct inofficial save
        elif self.creator_mode == "admin" and self.cb_save.isChecked() == False:
            copy_image_path = os.path.join(
                path_programm, "_database", "Bilder"
            )  ### direct official save
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
                    msg.exec_()
                    return

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

        if dict_picture_path != {}:
            images = ", ".join(dict_picture_path)
        else:
            images = "-"

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
                'Die Aufgabe mit dem Titel\n\n"{0}"\n\nwurde lokal auf Ihrem System gespeichert.'.format(
                    edit_titel
                )
            )
        else:
            msg.setText(
                'Die Aufgabe mit dem Titel\n\n"{0}"\n\nwurde gespeichert.'.format(
                    edit_titel
                )
            )
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
        msg.exec_()
        self.reset_window()

    ############################################################################
    ######################## BEFEHLE SAGE ###########################################
    ############################################################################

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
                "LaMA-Cria Datei (*.lamacria);; Alle Dateien (*.*)",
            )
            if path_backup_file[0] == "":
                return
            self.saved_file_path = path_backup_file[0]

        if external_file_loaded == True:
            self.saved_file_path = loaded_lama_file_path

        try:
            self.neue_schularbeit_erstellen()
        except AttributeError:
            pass
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        for bsp_string in list_sage_examples:
            self.btn_delete_pressed(bsp_string, True)

        with open(self.saved_file_path, "r", encoding="utf8") as loaded_file:
            self.dict_list_input_examples = json.load(loaded_file)

        # print(self.dict_list_input_examples)
        # print(self.dict_list_input_examples['data_gesamt'])
        list_sage_examples = self.dict_list_input_examples["list_examples"]

        # print(self.beispieldaten_dateipfad)
        # for all in list_sage_examples:
        # 	if any(all in s for s in self.beispieldaten_dateipfad_1.values()):
        # 		pass
        # 	else:
        # 		if any(all in s for s in self.beispieldaten_dateipfad_2.values()):
        # 			pass
        # 		else:
        # 			self.warning_window('Das Beispiel "{}" konnte nicht in der Datenbank gefunden werden. \n\n\n (Tipp: Refresh Database)'.format(all))
        # 			return

        for bsp_string in list_sage_examples:
            exec(
                'self.list_input_{0}=self.dict_list_input_examples["self.list_input_{0}"]'.format(
                    bsp_string
                )
            )

        # self.sage_aufgabe_create(True)

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

        year = self.dict_list_input_examples["data_gesamt"]["Datum"][0]
        month = self.dict_list_input_examples["data_gesamt"]["Datum"][1]
        day = self.dict_list_input_examples["data_gesamt"]["Datum"][2]
        self.dateEdit.setDate(QtCore.QDate(year, month, day))

        self.sage_aufgabe_create(True)

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
        # try:
        if list_sage_examples == []:
            self.warning_window(
                "Die Schularbeit ist leer.\nBitte fügen Sie vor dem Speichern Aufgaben zu Ihrer Schularbeit hinzu."
            )
            return

        try:
            self.saved_file_path
        except AttributeError:
            self.saved_file_path = path_programm

        # print(path_file)
        if path_file == "":
            path_backup_file = QtWidgets.QFileDialog.getSaveFileName(
                None,
                "Speichern unter",
                self.saved_file_path,
                "LaMA-Cria Datei (*.lamacria);; Alle Dateien (*.*)",
            )
            if path_backup_file[0] == "":
                return
            self.save_dict_examples_data()  #
            save_file = path_backup_file[0]

        else:
            name, extension = os.path.splitext(path_file)
            path_file = name + "_autosave.lamacria"
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

    def comboBox_typ_fb_changed(self):
        if self.comboBox_at_fb.currentIndex() == 0:
            QtWidgets.QApplication.setOverrideCursor(
                QtGui.QCursor(QtCore.Qt.WaitCursor)
            )
            self.groupBox_alle_aufgaben_fb.setEnabled(True)
            self.comboBox_klassen_changed("feedback")
            QtWidgets.QApplication.restoreOverrideCursor()

        if self.comboBox_at_fb.currentIndex() == 1:
            self.comboBox_kapitel_fb.clear()
            self.comboBox_unterkapitel_fb.clear()
            self.lineEdit_number_fb.clear()
            self.listWidget_fb.clear()
            self.label_example.setText(
                _translate("MainWindow", "Ausgewählte Aufgabe: -")
            )
            self.groupBox_alle_aufgaben_fb.setEnabled(False)

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
                _translate("MainWindow", "Ausgewählte Aufgabe: -")
            )
            dict_klasse_name = eval(
                "dict_{}_name".format(
                    list_klassen[self.comboBox_klassen_fb.currentIndex()]
                )
            )
            self.listWidget_fb.clear()
            self.comboBox_kapitel_fb.clear()
            self.comboBox_unterkapitel_fb.clear()
            self.comboBox_kapitel_fb.addItem("")

        for all in dict_klasse_name.keys():
            if list_mode == "sage":
                self.comboBox_kapitel.addItem(dict_klasse_name[all] + " (" + all + ")")
            if list_mode == "feedback":
                self.comboBox_kapitel_fb.addItem(
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
                "dict_{}".format(list_klassen[self.comboBox_klassen_fb.currentIndex()])
            )
            self.comboBox_unterkapitel_fb.clear()

            kapitel_shortcut = list(dict_klasse.keys())[
                self.comboBox_kapitel_fb.currentIndex() - 1
            ]
            self.comboBox_unterkapitel_fb.addItem("")

        index = 1
        for all in dict_klasse[kapitel_shortcut]:
            if list_mode == "sage":
                self.comboBox_unterkapitel.addItem(
                    dict_unterkapitel[all] + " (" + all + ")"
                )
                # self.comboBox_unterkapitel.setItemText(index, _translate("MainWindow", dict_unterkapitel[all] + ' ('+all+')'))
            if list_mode == "feedback":
                self.comboBox_unterkapitel_fb.addItem(
                    dict_unterkapitel[all] + " (" + all + ")"
                )
                # self.comboBox_unterkapitel_fb.setItemText(index, _translate("MainWindow", dict_unterkapitel[all] + ' ('+all+')'))
            index += 1

        if list_mode == "sage":
            if self.comboBox_kapitel.currentIndex() == 0:
                self.comboBox_unterkapitel.clear()
        if list_mode == "feedback":
            if self.comboBox_kapitel_fb.currentIndex() == 0:
                self.comboBox_unterkapitel_fb.clear()

        # print(self.comboBox_kapitel.currentIndex())
        self.adapt_choosing_list(list_mode)

    def comboBox_unterkapitel_changed(self, list_mode):

        self.adapt_choosing_list(list_mode)

    def adapt_choosing_list(self, list_mode):
        if list_mode == "sage":
            listWidget = self.listWidget
        if list_mode == "feedback":
            listWidget = self.listWidget_fb

            # if self.comboBox_at_fb.currentText() == "Allgemeine Rückmeldung":
            #     self.comboBox_fb.clear()
            #     self.comboBox_fb_num.clear()
            #     self.lineEdit_number_fb.clear()
            #     listWidget.clear()
            #     return

        listWidget.clear()

        log_file = os.path.join(path_programm, "Teildokument", "log_file")
        try:
            with open(log_file, encoding="utf8") as f:
                beispieldaten_dateipfad = json.load(f)
        except FileNotFoundError:
            self.refresh_ddb()
            with open(log_file, encoding="utf8") as f:
                beispieldaten_dateipfad = json.load(f)

        self.beispieldaten_dateipfad = beispieldaten_dateipfad
        if self.cb_drafts_sage.isChecked():
            QtWidgets.QApplication.restoreOverrideCursor()
            drafts_path = os.path.join(path_programm, "Beispieleinreichung")
            for klasse in list_klassen:
                try:
                    drafts_path = os.path.join(path_programm, "Beispieleinreichung",klasse)
                    for all in os.listdir(drafts_path):
                        file = open(os.path.join(drafts_path, all), encoding="utf8")
                        for i, line in enumerate(file):
                            if not line == "\n":
                                # line=line.replace('\section{', 'section{ENTWURF ')
                                self.beispieldaten_dateipfad[line] = os.path.join(drafts_path, all)
                                break
                        file.close()
                except FileNotFoundError:
                    pass

        list_beispieldaten = []

        if list_mode == "sage":
            klasse='k'+self.comboBox_klassen.currentText()[0]
            for all in self.beispieldaten_dateipfad.values():
                if klasse in all:
                    filename_all = os.path.basename(all)
                    name, extension = os.path.splitext(filename_all)
                    #print(filename_all)
                    if name.startswith(self.lineEdit_number.text()):
                        if "Beispieleinreichung" in all:
                            list_beispieldaten.append("*E-" + name)
                        else:
                            list_beispieldaten.append(name)



        def add_filename_to_list(file_path):
            filename_all = os.path.basename(file_path)
            name, extension = os.path.splitext(filename_all)
            if list_mode == "sage":
                if name.startswith(self.lineEdit_number.text()):
                    list_beispieldaten.append(name)
            if list_mode == "feedback":
                if name.startswith(self.lineEdit_number_fb.text()):
                    list_beispieldaten.append(name)

        list_beispieldaten = []

        if list_mode == "sage":
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

            for all in beispieldaten_dateipfad.keys():
                file_path = beispieldaten_dateipfad[all]
                if str(list_klassen[self.comboBox_klassen.currentIndex()]) in file_path:
                    if kapitel_shortcut == "":
                        add_filename_to_list(file_path)
                    else:
                        if unterkapitel_shortcut == "":
                            if kapitel_shortcut in all:
                                add_filename_to_list(file_path)
                        else:
                            thema_shortcut = (
                                kapitel_shortcut + "." + unterkapitel_shortcut
                            )
                            if thema_shortcut in all:
                                add_filename_to_list(file_path)

        if list_mode == "feedback":
            dict_klasse_name = eval(
                "dict_{}_name".format(
                    list_klassen[self.comboBox_klassen_fb.currentIndex()]
                )
            )
            if self.comboBox_kapitel_fb.currentText() is not "":
                kapitel_shortcut = list(dict_klasse_name.keys())[
                    self.comboBox_kapitel_fb.currentIndex() - 1
                ]
            else:
                kapitel_shortcut = ""

            if self.comboBox_unterkapitel_fb.currentText() is not "":
                shortcut = re.findall(
                    r"\((.*)\)", self.comboBox_unterkapitel_fb.currentText()
                )
                unterkapitel_shortcut = shortcut[-1]
            else:
                unterkapitel_shortcut = ""

            for all in beispieldaten_dateipfad.keys():
                file_path = beispieldaten_dateipfad[all]
                if (
                    str(list_klassen[self.comboBox_klassen_fb.currentIndex()])
                    in file_path
                ):
                    if kapitel_shortcut == "":
                        add_filename_to_list(file_path)
                    else:
                        if unterkapitel_shortcut == "":
                            if kapitel_shortcut in all:
                                add_filename_to_list(file_path)
                        else:
                            thema_shortcut = (
                                kapitel_shortcut + "." + unterkapitel_shortcut
                            )
                            if thema_shortcut in all:
                                add_filename_to_list(file_path)

        list_beispieldaten = sorted(list_beispieldaten, key=natural_keys)

        for all in list_beispieldaten:
            if list_mode == "feedback" and all.startswith("_L_"):
                pass
            else:
                listWidget.addItem(all)
                listWidget.setFocusPolicy(QtCore.Qt.ClickFocus)


    def save_dict_examples_data(self):
        self.dict_list_input_examples = {}
        num_aufgaben = len(list_sage_examples)
        gesamtpunkte = 0

        self.dict_list_input_examples["list_examples"] = list_sage_examples
        for bsp_string in list_sage_examples:
            list_input = eval("self.list_input_{}".format(bsp_string))
            self.dict_list_input_examples[
                "self.list_input_{}".format(bsp_string)
            ] = list_input
            gesamtpunkte += list_input[0]

        try:
            self.list_copy_images
        except AttributeError:
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
            "Notenschluessel": [
                self.spinBox_2.value(),
                self.spinBox_3.value(),
                self.spinBox_4.value(),
                self.spinBox_5.value(),
            ],
            "num_aufgabe": num_aufgaben,
            "gesamtpunkte": gesamtpunkte,
            "copy_images": self.list_copy_images,
        }

        self.dict_list_input_examples["data_gesamt"] = dict_data_gesamt

    def nummer_clicked(self, item):
        self.sage_aufgabe_add(item.text())

    def nummer_clicked_fb(self, item):
        self.label_example.setText(
            _translate(
                "MainWindow",
                "Ausgewählte Aufgabe: {0} ({1})".format(
                    item.text(), self.comboBox_klassen_fb.currentText()
                ),
            )
        )

    def sage_aufgabe_add(self, aufgabe):
        klasse = list_klassen[self.comboBox_klassen.currentIndex()]
        example = klasse + "_" + aufgabe
        if example not in list_sage_examples:
            list_sage_examples.append(example)

        num_total = len(list_sage_examples)
        self.label_gesamtbeispiele.setText(
            _translate("MainWindow", "Anzahl der Aufgaben: {0}".format(num_total))
        )

        self.sage_aufgabe_create()

        # for all in list_sage_examples:
        # 	list_input=eval('self.list_input_{}'.format(all))

        # 	# print(list_input)

    def punkte_changed(self, bsp_string):

        spinBox_pkt = eval("self.spinBox_pkt_{}".format(bsp_string))
        punkte = spinBox_pkt.value()

        list_input = eval("self.list_input_{}".format(bsp_string))
        list_input[0] = punkte

        gesamtpunkte = 0

        for all in list_sage_examples:
            list_input = eval("self.list_input_{}".format(all))
            gesamtpunkte += list_input[0]

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
            _translate("MainWindow", "% (ab {})".format(list_punkte[0]))
        )
        self.label_g_pkt.setText(
            _translate("MainWindow", "% (ab {})".format(list_punkte[1]))
        )
        self.label_b_pkt.setText(
            _translate("MainWindow", "% (ab {})".format(list_punkte[2]))
        )
        self.label_g_pkt_2.setText(
            _translate("MainWindow", "% (ab {})".format(list_punkte[3]))
        )
        # self.label_ng_pkt.setText(_translate("MainWindow",	 "% (<{})".format(pkt_ge),None))

        self.label_gesamtpunkte.setText(
            _translate("MainWindow", "Gesamtpunkte: %i" % gesamtpunkte)
        )
        # self.beurteilungsraster_changed()

    def abstand_changed(self, bsp_string):

        spinBox_abstand = eval("self.spinBox_abstand_{}".format(bsp_string))
        abstand = spinBox_abstand.value()

        list_input = eval("self.list_input_{}".format(bsp_string))
        list_input[1] = abstand

    def move_button_pressed(self, direction, bsp_string):
        self.update_lists_examples()

        list_input = eval("self.list_input_{}".format(bsp_string))
        sb_value = eval("self.spinBox_pkt_{}".format(bsp_string))
        list_input[0] = sb_value.value()

        space_value = eval("self.spinBox_abstand_{}".format(bsp_string))
        list_input[1] = space_value.value()

        if direction == "up":
            a, b = (
                list_sage_examples.index(bsp_string),
                list_sage_examples.index(bsp_string) - 1,
            )
        if direction == "down":
            a, b = (
                list_sage_examples.index(bsp_string),
                list_sage_examples.index(bsp_string) + 1,
            )

        list_sage_examples[a], list_sage_examples[b] = (
            list_sage_examples[b],
            list_sage_examples[a],
        )

        self.sage_aufgabe_create()

    def btn_delete_pressed(self, bsp_string, file_loaded=False):

        exec("self.groupBox_bsp_{}.setParent(None)".format(bsp_string))
        list_input = eval("self.list_input_{}".format(bsp_string))
        spinBox_pkt = eval("self.spinBox_pkt_{}".format(bsp_string))

        list_input[0] = 0
        list_input[3] = ""

        spinBox_pkt.setValue(0)

        list_input[1] = 0

        spinBox_abstand = eval("self.spinBox_abstand_{}".format(bsp_string))
        spinBox_abstand.setValue(0)

        if file_loaded == False:
            list_sage_examples.remove(bsp_string)

            num_total = len(list_sage_examples)
            self.label_gesamtbeispiele.setText(
                _translate("MainWindow", "Anzahl der Aufgaben: {0}".format(num_total))
            )
            self.sage_aufgabe_create()

    def update_lists_examples(self):

        for bsp_string in list_sage_examples:

            try:
                list_input = eval("self.list_input_{}".format(bsp_string))
                sb_value = eval("self.spinBox_pkt_{}".format(bsp_string))
                list_input[0] = sb_value.value()
                space_value = eval("self.spinBox_abstand_{}".format(bsp_string))
                list_input[1] = space_value.value()

            except AttributeError:

                exec('self.list_input_{}=[0,0,"",""]'.format(bsp_string))
                list_input = eval("self.list_input_{}".format(bsp_string))

                # print(list_input)

    def sage_aufgabe_create(self, file_loaded=False):
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        r = 0
        scrollBar_position = self.scrollArea_chosen.verticalScrollBar().value()

        for bsp_string in list_sage_examples:

            try:
                exec("self.groupBox_bsp_{}.setParent(None)".format(bsp_string))
            except AttributeError:
                pass

        if file_loaded == False:
            self.update_lists_examples()

        for bsp_string in list_sage_examples:

            list_input = eval("self.list_input_{}".format(bsp_string))
            klasse, example = bsp_string.split("_")
            name = example + ".tex"

            for all in self.beispieldaten_dateipfad:
                if klasse.upper() in all:

                    filename = os.path.basename(self.beispieldaten_dateipfad[all])
                    if name == filename:
                        chosen_section = all.split(" - ")
                        #print(chosen_section)
                        list_input[2] = chosen_section[-3]

            # print(list_input)

        if file_loaded == False:
            self.list_copy_images = []
            self.save_dict_examples_data()
        # if file_loaded==True:
        # 	try:
        # 		self.list_copy_images
        # 	except AttributeError:
        # 		self.list_copy_images=[]
        # counter=0

        num_of_example = 1

        # for klasse in dict_sage_examples:
        # 	total_num_of_examples+=len(dict_sage_examples[klasse])

        # print(dict_sage_examples)
        # for klasse in dict_sage_examples:
        # 	for all in dict_sage_examples[klasse]:
        # 		bsp_string=klasse+ '_' + all
        self.list_copy_images = []
        for bsp_string in list_sage_examples:
            klasse, example = bsp_string.split("_")

            list_input = eval("self.list_input_{}".format(bsp_string))

            exec(
                "self.groupBox_bsp_{} = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)".format(
                    bsp_string
                )
            )
            x = eval("self.groupBox_bsp_{}".format(bsp_string))
            x.setMaximumSize(QtCore.QSize(16777215, 120))
            x.setObjectName("groupBox_bsp_{}".format(bsp_string))
            if (list_sage_examples.index(bsp_string) % 2) == 0:
                x.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))

            x.setTitle(
                _translate("MainWindow", "{0}. Aufgabe".format(str(num_of_example)))
            )
            self.gridLayout_gB = QtWidgets.QGridLayout(x)
            self.gridLayout_gB.setObjectName("gridLayout_gB")
            self.gridLayout_8.addWidget(x, 0, 0, 1, 2, QtCore.Qt.AlignTop)

            exec("self.label_aufgabe_{} = QtWidgets.QLabel(x)".format(bsp_string))
            label_aufgabe = eval("self.label_aufgabe_{}".format(bsp_string))
            label_aufgabe.setWordWrap(True)
            label_aufgabe.setObjectName("label_aufgabe_{}".format(bsp_string))
            self.gridLayout_gB.addWidget(label_aufgabe, 0, 0, 1, 1)

            label_aufgabe.setText(
                _translate("MainWindow", "{0}. Klasse - {1}".format(klasse[1], example))
            )

            exec("self.label_title_{} = QtWidgets.QLabel(x)".format(bsp_string))
            label_title = eval("self.label_title_{}".format(bsp_string))
            label_title.setWordWrap(True)
            label_title.setObjectName("label_title_{}".format(bsp_string))
            self.gridLayout_gB.addWidget(label_title, 1, 0, 1, 1)
            label_title.setText(
                _translate("MainWindow", "Titel: {}".format(list_input[2]))
            )  # list_titles[i-1]

            self.groupBox_pkt = QtWidgets.QGroupBox(x)
            # self.groupBox_pkt.setMaximumSize(QtCore.QSize(83, 53))
            self.groupBox_pkt.setObjectName("groupBox_pkt")
            self.groupBox_pkt.setTitle(_translate("MainWindow", "Punkte"))

            self.groupBox_pkt.setMaximumSize(QtCore.QSize(80, 16777215))

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
            spinBox_pkt.valueChanged.connect(partial(self.punkte_changed, bsp_string))
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

            self.pushButton_up.clicked.connect(
                partial(self.move_button_pressed, "up", bsp_string)
            )

            # self.pushButton_up.clicked.connect(partial(self.btn_up_pressed,bsp_string))

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
            # self.pushButton_down.clicked.connect(partial(self.btn_down_pressed,bsp_string))

            self.pushButton_down.clicked.connect(
                partial(self.move_button_pressed, "down", bsp_string)
            )

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
                partial(self.btn_delete_pressed, bsp_string)
            )

            self.groupBox_abstand = QtWidgets.QGroupBox(x)
            self.groupBox_abstand.setObjectName("groupBox_abstand")
            self.groupBox_abstand.setTitle(_translate("MainWindow", "Abstand (cm)"))
            self.groupBox_abstand.setMaximumSize(QtCore.QSize(100, 16777215))
            self.groupBox_abstand.setToolTip("Neue Seite: Abstand=99")
            self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_abstand)
            # self.groupBox_abstand.setMaximumSize(QtCore.QSize(180, 152))
            # if typ==2:
            # 	self.groupBox_abstand.hide()
            self.verticalLayout_3.setObjectName("verticalLayout_3")

            exec(
                "self.spinBox_abstand_{} = SpinBox_noWheel(self.groupBox_abstand)".format(
                    bsp_string
                )
            )
            spinBox_abstand = eval("self.spinBox_abstand_{}".format(bsp_string))
            spinBox_abstand.setObjectName("spinBox_abstand_{}".format(bsp_string))
            spinBox_abstand.setValue(eval("self.list_input_{}".format(bsp_string))[1])
            spinBox_abstand.valueChanged.connect(
                partial(self.abstand_changed, bsp_string)
            )
            self.verticalLayout_3.addWidget(spinBox_abstand)
            self.gridLayout_gB.addWidget(self.groupBox_abstand, 0, 2, 2, 1)

            ##### GET included pictures ###

            name = example + ".tex"
            for path in self.beispieldaten_dateipfad.values():
                if klasse in path:
                    if name == os.path.basename(path):
                        selected_path = path

            f = open(selected_path, "r", encoding="utf8")
            content = f.read()
            f.close()

            if "\\includegraphics" in content:
                matches = re.findall("/Bilder/(.+.eps)}", content)
                for image in matches:
                    self.list_copy_images.append(image)

            ### end ###

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

            num_of_example += 1

            #
        self.scrollArea_chosen.verticalScrollBar().setValue(scrollBar_position)
        # # self.sum_up_ausgleich()

        if file_loaded == True:
            for bsp_string in list_sage_examples:
                self.punkte_changed(bsp_string)
        self.lineEdit_number.setText("")
        self.lineEdit_number.setFocus()
        QtWidgets.QApplication.restoreOverrideCursor()

    def pushButton_vorschau_pressed(self, ausgabetyp, index, maximum):
        if ausgabetyp == "vorschau":
            self.save_dict_examples_data()

        # print(self.dict_list_input_examples['data_gesamt']['Datum'])
        # return

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        dict_gesammeltedateien = {}
        # print(list_sage_examples)

        for bsp_string in list_sage_examples:
            klasse, example = bsp_string.split("_")
            name = example + ".tex"
            # print(klasse, example)

            for all in self.beispieldaten_dateipfad:
                if klasse.upper() in all:
                    if name == os.path.basename(self.beispieldaten_dateipfad[all]):
                        dict_gesammeltedateien[
                            bsp_string
                        ] = self.beispieldaten_dateipfad[all]

        # print(dict_gesammeltedateien)

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

        raw_date = self.dict_list_input_examples["data_gesamt"]["Datum"]
        # datum_kurz=str(raw_date[2])+'. '+str(raw_date[1])+'. '+str(raw_date[0])
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
                if sys.platform.startswith("linux") or sys.platform.startswith(
                    "darwin"
                ):
                    filename = filename + ".tex"

                for character in dict_umlaute.keys():
                    if character in filename:
                        filename = filename.replace(character, dict_umlaute[character])
                filename_vorschau = os.path.join(dirname, filename)

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
            == "Wiederholung"
        ):
            if ausgabetyp == "schularbeit" and maximum > 2:
                vorschau.write(
                    "\\textsc{{Wiederholung -- {0}}} \\hfill \\textsc{{Name:}} \\rule{{8cm}}{{0.4pt}} \\normalsize \\\ \\vspace{{\\baselineskip}} \n\n".format(
                        gruppe
                    )
                )
            else:
                vorschau.write(
                    "\\textsc{Wiederholung} \\hfill \\textsc{Name:} \\rule{8cm}{0.4pt} \\normalsize \\\ \\vspace{\\baselineskip} \n\n"
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

            if self.dict_titlepage["name"] == True:
                vorschau.write("\\Large Name: \\rule{8cm}{0.4pt} \\\ \n")
            vorschau.write("\\vfil\\vfil\\vfil \n")
            if self.dict_titlepage["note"] == True:
                vorschau.write("\\Large Note: \\rule{8cm}{0.4pt} \\\ [1cm]\n")
            if self.dict_titlepage["unterschrift"] == True:
                vorschau.write("\\Large Unterschrift: \\rule{8cm}{0.4pt} \\\ \n")

            vorschau.write("\\end{titlepage}\n\n")
        vorschau.close()

        vorschau = open(filename_vorschau, "a", encoding="utf8")

        # list_chosen_examples=[]

        # print(list_sage_examples)
        for bsp_string in list_sage_examples:

            list_input = "self.list_input_{}".format(bsp_string)

            spinBox_abstand = self.dict_list_input_examples[list_input][1]
            spinBox_pkt = self.dict_list_input_examples[list_input][0]
            f = open(dict_gesammeltedateien[bsp_string], "r", encoding="utf8")
            content = f.readlines()
            f.close()

            if ausgabetyp == "schularbeit":

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

                    if (
                        self.dict_list_input_examples["data_gesamt"]["copy_images"]
                        == []
                    ):
                        pass
                    else:
                        for image in self.dict_list_input_examples["data_gesamt"][
                            "copy_images"
                        ]:
                            # if os.path.isfile(os.path.join(path_programm, '_database', 'Bilder', image)):
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

                for image in self.dict_list_input_examples["data_gesamt"][
                    "copy_images"
                ]:
                    content = [
                        line.replace("../_database/Bilder/", "") for line in content
                    ]
                    content=[line.replace('../_database_inoffiziell/Bilder/','') for line in content]

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
            divided_example = []
            divided_example.append(beginning)
            divided_example.append(joined_content)
            divided_example.append(ending)

            if beispiel_typ == "beispiel":

                vorschau.write(
                    "\\begin{beispiel}{"
                    + str(spinBox_pkt)
                    + "}\n"
                    + divided_example[1]
                    + "\n"
                    + divided_example[2]
                    + "\n\n"
                )

            if beispiel_typ == "langesbeispiel":
                vorschau.write(
                    "\\begin{langesbeispiel} \item["
                    + str(spinBox_pkt)
                    + "]\n"
                    + divided_example[1]
                    + "\n"
                    + divided_example[2]
                    + "\n\n"
                )

            if spinBox_abstand != 0:
                if spinBox_abstand == 99:
                    vorschau.write("\\newpage \n\n")
                else:
                    vorschau.write("\\vspace{" + str(spinBox_abstand) + "cm} \n\n")

        if (
            self.dict_list_input_examples["data_gesamt"]["Pruefungstyp"]
            != "Wiederholung"
            and self.dict_list_input_examples["data_gesamt"]["Pruefungstyp"]
            != "Übungsblatt"
        ):

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

        if ausgabetyp == "vorschau":
            self.create_pdf("Schularbeit_Vorschau", 0, 0)

        if ausgabetyp == "schularbeit":
            name, extension = os.path.splitext(filename_vorschau)

            Ui_MainWindow.create_pdf(self, name, index, maximum)

            if maximum > 2:
                if index % 2 == 0:
                    shutil.move(
                        name + ".pdf",
                        name + "_{}_Loesung.pdf".format(dict_gruppen[int(index / 2)]),
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

                text = re.sub(r"setcounter{Zufall}{.}", "setcounter{Zufall}{0}", text)
                text = re.sub(r"Large Gruppe .", "Large Gruppe A", text)

                with open(filename_vorschau, "w", encoding="utf8") as vorschau:
                    vorschau.write(text)

        # MainWindow.show()
        QtWidgets.QApplication.restoreOverrideCursor()

    def pushButton_erstellen_pressed(self):
        self.save_dict_examples_data()
        try:
            self.saved_file_path
        except AttributeError:
            self.saved_file_path = path_programm
        self.open_subwindow_erstellen(
            self.dict_list_input_examples,
            self.beispieldaten_dateipfad,
            self.dict_titlepage,
            self.saved_file_path,
        )

    #############################################################################
    #############################################################################
    #############################################################################

    def pushButton_send_pressed(self):
        gmail_user = "lamabugfix@gmail.com"
        gmail_password = "abcd&1234"

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

        content = "Subject: LaMA-Cria: {0}: {1}\n\nProblembeschreibung:\n\n{2}\n\n\nKontakt: {3}".format(
            example, fehler, description, contact
        )

        # try:
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

        # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        # server.ehlo()
        # server.login(gmail_user, gmail_password)
        # server.sendmail('lamabugfix@gmail.com', 'lama.helpme@gmail.com', content.encode("utf8"))
        # server.close()

        QtWidgets.QApplication.restoreOverrideCursor()

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowIcon(QtGui.QIcon(logo_path))
        msg.setWindowTitle("Meldung gesendet")
        msg.setText("Das Feedback bzw. die Fehlermeldung wurde erfolgreich gesendet!\n")
        msg.setInformativeText("Vielen Dank für die Mithilfe LaMA zu verbessern.")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.plainTextEdit_fb.setPlainText(_translate("MainWindow", ""))

        self.label_example.setText(_translate("MainWindow", "Ausgewählte Aufgabe: -"))
        self.comboBox_fehlertyp.setCurrentIndex(0)
        self.comboBox_at_fb.setCurrentIndex(0)
        self.comboBox_klassen_fb.setCurrentIndex(0)
        self.comboBox_kapitel_fb.setCurrentIndex(0)
        self.comboBox_unterkapitel_fb.setCurrentIndex(0)
        self.lineEdit_number_fb.setText(_translate("MainWindow", ""))
        self.lineEdit_email.setText(_translate("MainWindow", ""))
        QtWidgets.QApplication.restoreOverrideCursor()
        return

        # except:
        # 	msg.close()
        # 	QtWidgets.QApplication.restoreOverrideCursor()

        # 	self.warning_window('Die Meldung konnte leider nicht gesendet werden!', 'Überprüfen Sie Ihre Internetverbindung oder versuchen Sie es später erneut.')

    #######################################################################
    ##########################################################################
    ############################################################################

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

        # MainWindow.setTabOrder(self.spinBox_nummer, self.dateEdit)
        # MainWindow.setTabOrder(self.dateEdit, self.lineEdit_klasse)

        self.adapt_choosing_list("sage")
        self.listWidget.itemClicked.connect(self.nummer_clicked)

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

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()

    sys.exit(app.exec_())

