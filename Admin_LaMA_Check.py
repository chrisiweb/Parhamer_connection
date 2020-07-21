#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
import os
import sys
import shutil
from config import config_loader 

# from tkinter import *
# from tkinter import filedialog
import yaml

path_programm = os.path.dirname(sys.argv[0])
path_beispieleinreichung = os.path.join(path_programm, "Beispieleinreichung")
logo_path = os.path.join(path_programm, "_database", "_config", "icon", "magnifier.png")


config_file = os.path.join(path_programm, "_database", "_config", "config.yml")

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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(503, 227)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem)
        self.label_task = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_task.setFont(font)
        self.label_task.setObjectName("label_task")
        self.verticalLayout.addWidget(self.label_task, 0, QtCore.Qt.AlignHCenter)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem1)
        self.pushButton_check = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_check.setFont(font)
        self.pushButton_check.setObjectName("pushButton_check")
        self.verticalLayout.addWidget(self.pushButton_check)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem2)
        self.pushButton_move = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_move.setFont(font)
        self.pushButton_move.setObjectName("pushButton_move")
        self.verticalLayout.addWidget(self.pushButton_move)
        spacerItem3 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton_check.clicked.connect(self.btn_check_pressed)
        self.pushButton_move.clicked.connect(self.btn_move_pressed)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LaMA Admin - Check & Move"))
        self.label_task.setText(_translate("MainWindow", "Was möchtest du machen?"))
        self.pushButton_check.setText(_translate("MainWindow", "Aufgaben überprüfen"))
        self.pushButton_move.setText(_translate("MainWindow", "Aufgaben verschieben"))

    def btn_check_pressed(self):
        for file in os.walk(path_beispieleinreichung):
            print(file)
        # QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        # filename_testdokument = os.path.join(
        #     path_programm, "Testdokument", "Testdokument.tex"
        # )
        # folder_items = os.listdir(path_beispieleinreichung)
        # path_folder_items = []
        # for all in folder_items:
        #     path_folder_items.append(os.path.join(path_beispieleinreichung, all))
        # try:
        #     file = open(filename_testdokument, "w+")  # , encoding='ISO-8859-1'

        # except FileNotFoundError:
        #     os.makedirs(os.path.dirname(filename_testdokument))
        #     file = open(filename_testdokument, "w+")

        # file.write(
        #     "\documentclass[a4paper,12pt]{report}\n\n"
        #     "\\usepackage{geometry}\n"
        #     "\geometry{a4paper,left=18mm,right=18mm, top=2cm, bottom=2cm}\n\n"
        #     "\\usepackage{lmodern}\n"
        #     "\\usepackage[T1]{fontenc}\n"
        #     "\\usepackage[utf8]{inputenc}\n"
        #     "\\usepackage[ngerman]{babel}\n"
        #     "\\usepackage[solution_on]{srdp-mathematik} % solution_on/off\n"
        #     "\setcounter{Zufall}{0}\n\n\n"
        #     "\pagestyle{empty} %PAGESTYLE: empty, plain, fancy\n"
        #     "\onehalfspacing %Zeilenabstand\n"
        #     "\setcounter{secnumdepth}{-1} % keine Nummerierung der Ueberschriften\n\n\n\n"
        #     "%\n"
        #     "%\n"
        #     "%%%%%%%%%%%%%%%%%% DOKUMENT - ANFANG %%%%%%%%%%%%%%%%%%%"
        #     "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
        #     "%\n"
        #     "%\n"
        #     "\\begin{document}\n"
        #     '\shorthandoff{"}\n'
        # )
        # file.close()
        # file = open(filename_testdokument, "a")
        # for all in path_folder_items:
        #     if all.endswith(".tex"):
        #         value = all.replace("\\", "/")
        #         file.write('\input{"' + value + '"}%\n' "\\newpage \n")
        # file.write('\shorthandoff{"}\n' "\end{document}")
        # print("Öffne Editor...")
        # os.startfile(filename_testdokument)
        # QtWidgets.QApplication.restoreOverrideCursor()

    def btn_move_pressed(self):
        print('move')
        # filenames_fullpath = QtWidgets.QFileDialog.getOpenFileNames(
        #     None, "Dateien wählen", path_beispieleinreichung, "LaTeX Dateien (*.tex)"
        # )
        # # filenames_fullpath =  filedialog.askopenfilenames(initialdir = path_beispieleinreichung,title = "Durchsuchen...")
        # list_files_move = []
        # for item in filenames_fullpath[0]:
        #     if os.path.isfile(os.path.join(path_beispieleinreichung, item)):
        #         list_files_move.append(os.path.basename(item))

        # # print(list_files_move)
        # for files in list_files_move:
        #     file_path = os.path.join(path_beispieleinreichung, files)

        #     f = open(file_path, "r", encoding="utf8")
        #     content = f.read()
        #     content = content.replace(
        #         "../Beispieleinreichung/Bilder", "../_database/Bilder"
        #     )
        #     f.close()
        #     f = open(file_path, "w", encoding="utf8")
        #     f.write(content)
        #     f.close()

        # if list_files_move == []:
        #     return

        # path_beispieleinreichung_images = os.path.join(
        #     path_beispieleinreichung, "Bilder"
        # )
        # image_folder_items = os.listdir(path_beispieleinreichung_images)
        # image_counter = 0
        # for all in list_files_move:
        #     gk = all.split(" - ")
        #     # print(all)

        #     if len(gk) == 1:
        #         shutil.move(
        #             os.path.join(path_beispieleinreichung, all),
        #             os.path.join(
        #                 path_programm,
        #                 "_database",
        #                 "Typ2Aufgaben",
        #                 "Einzelbeispiele",
        #                 all,
        #             ),
        #         )

        #     if len(gk) == 2:
        #         shutil.move(
        #             os.path.join(path_beispieleinreichung, all),
        #             os.path.join(
        #                 path_programm,
        #                 "_database",
        #                 "Typ1Aufgaben",
        #                 "_Grundkompetenzen",
        #                 gk[0][:2],
        #                 gk[0],
        #                 "Einzelbeispiele",
        #                 all,
        #             ),
        #         )

        #     if len(gk) == 3:
        #         klasse = gk[0][1] + ".Klasse"
        #         thema = gk[1].lower()
        #         shutil.move(
        #             os.path.join(path_beispieleinreichung, all),
        #             os.path.join(
        #                 path_programm,
        #                 "_database",
        #                 "Typ1Aufgaben",
        #                 klasse,
        #                 thema,
        #                 "Einzelbeispiele",
        #                 all,
        #             ),
        #         )

        #     for image in image_folder_items[:]:
        #         # print(gk)
        #         chosen_file, extension = os.path.splitext(all)
        #         chosen_image = (
        #             chosen_file.replace(" ", "").replace(".", "").replace("-", "_")
        #         )
        #         chosen_image = chosen_image + "_"
        #         # print(chosen_image)
        #         # print('Bilder: '+image)
        #         if image.startswith(chosen_image):
        #             image_counter += 1
        #             if image.endswith(".eps"):
        #                 shutil.move(
        #                     os.path.join(path_beispieleinreichung_images, image),
        #                     os.path.join(path_programm, "_database", "Bilder", image),
        #                 )
        #             else:
        #                 image_folder_items.remove(image)
        # msg = QtWidgets.QMessageBox()
        # msg.setIcon(QtWidgets.QMessageBox.Information)
        # msg.setText(
        #     "Erledigt.\nEs wurden "
        #     + str(len(list_files_move))
        #     + " Datei(en) und "
        #     + str(image_counter)
        #     + " Bild(er) verschoben."
        # )
        # msg.setWindowTitle("Dateien kopiert")
        # msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        # ret = msg.exec_()

        # sys.exit(0)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())

