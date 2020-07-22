#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
import os
import sys
import shutil
from config import config_loader, is_empty 
import re
import yaml
from standard_dialog_windows import information_window

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

def get_info_from_path(path):
    filename = os.path.basename(path)
    if os.path.basename(os.path.dirname(path)) != "Beispieleinreichung":
        typ=None
        klasse = os.path.basename(os.path.dirname(path))
        thema = None
        nummer, _ = os.path.splitext(filename)
    elif re.search("[A-Z]", filename) == None:
        typ=2
        klasse=None
        thema=None
        nummer, _ =os.path.splitext(os.path.basename(path))
    else:
        filename,_ = os.path.splitext(filename)
        list_filename_split = filename.split(" - ")
        if len(list_filename_split)==2:
            typ=1
            klasse=None
            thema = list_filename_split[0]
            nummer = list_filename_split[1]
        else:
            typ=1
            klasse= list_filename_split[0].lower()
            thema = list_filename_split[1]
            nummer = list_filename_split[2]

    info= [typ, klasse, thema, nummer]

    return info


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
        path_folder_items = []
        for path, subdires, files in os.walk(path_beispieleinreichung):
            for name in files:
                if 'Bilder' not in path:
                    path_folder_items.append(os.path.join(path, name))
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        filename_testdokument = os.path.join(
            path_programm, "Testdokument", "Testdokument.tex"
        )
        # folder_items = os.listdir(path_beispieleinreichung)
        
        # for all in folder_items:
        #     path_folder_items.append(os.path.join(path_beispieleinreichung, all))
        try:
            file = open(filename_testdokument, "w+")  # , encoding='ISO-8859-1'

        except FileNotFoundError:
            os.makedirs(os.path.dirname(filename_testdokument))
            file = open(filename_testdokument, "w+")

        file.write(
            "\documentclass[a4paper,12pt]{report}\n\n"
            "\\usepackage{geometry}\n"
            "\geometry{a4paper,left=18mm,right=18mm, top=2cm, bottom=2cm}\n\n"
            "\\usepackage{lmodern}\n"
            "\\usepackage[T1]{fontenc}\n"
            "\\usepackage[utf8]{inputenc}\n"
            "\\usepackage[ngerman]{babel}\n"
            "\\usepackage[solution_on]{srdp-mathematik} % solution_on/off\n"
            "\setcounter{Zufall}{0}\n\n\n"
            "\pagestyle{empty} %PAGESTYLE: empty, plain, fancy\n"
            "\onehalfspacing %Zeilenabstand\n"
            "\setcounter{secnumdepth}{-1} % keine Nummerierung der Ueberschriften\n\n\n\n"
            "%\n"
            "%\n"
            "%%%%%%%%%%%%%%%%%% DOKUMENT - ANFANG %%%%%%%%%%%%%%%%%%%"
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
            "%\n"
            "%\n"
            "\\begin{document}\n"
            '\shorthandoff{"}\n'
        )
        file.close()

        with open(filename_testdokument, "a", encoding="utf8") as file: 
            for all in path_folder_items:
                value = all.replace("\\", "/")
                file.write('\input{"' + value + '"}%\n' "\\newpage \n")
            file.write('\shorthandoff{"}\n' "\end{document}")
        print("Öffne Editor...")
        os.startfile(filename_testdokument)
        QtWidgets.QApplication.restoreOverrideCursor()

    def btn_move_pressed(self):
        filenames_fullpath = QtWidgets.QFileDialog.getOpenFileNames(
            None, "Dateien wählen", path_beispieleinreichung, "LaTeX Dateien (*.tex)"
        )

        list_files_move = []
        for item in filenames_fullpath[0]:
            if os.path.isfile(os.path.join(path_beispieleinreichung, item)):
                list_files_move.append(item)

        if is_empty(list_files_move) == True:
            return

        for all in list_files_move:
            with open(all, "r", encoding="utf8") as file:
                content = file.read()

                content = content.replace(
                    "../Beispieleinreichung/Bilder", "../_database/Bilder"
                )

            with open(all, "w", encoding="utf8") as file:
                file.write(content)

        number_images = 0
        for all in list_files_move:
            info = get_info_from_path(all)
            filename = os.path.basename(all)
            if info[0]==None:
                new_path = os.path.join(path_programm,"_database",info[1],"Einzelbeispiele",filename)
            elif info[0]==2:
                new_path = os.path.join(path_programm,"_database","Typ2Aufgaben","Einzelbeispiele",filename)
            elif info[0]==1 and info[1]==None:
                gk, gk_num = info[2].split(" ")
                if "-" in gk:
                    gk,_ = gk.split("-")
                new_path = os.path.join(path_programm,"_database","Typ1Aufgaben","_Grundkompetenzen",gk,info[2],"Einzelbeispiele",filename)
            elif info[0]==1 and info[1] != None:
                new_path = os.path.join(path_programm,"_database","Typ1Aufgaben","{}.Klasse".format(info[1][-1]),info[2].lower(),"Einzelbeispiele",filename)                


            if os.path.isdir(os.path.dirname(new_path)) == False:
                os.makedirs(os.path.dirname(new_path))


            with open(all, "r", encoding="utf8") as file:
                content = file.read()


            shutil.move(all, new_path)


            if content.count("includegraphics") != 0:
                path_beispieleinreichung_images = os.path.join(path_programm, "Beispieleinreichung","Bilder")
                split_content = re.split("../_database/Bilder/|.eps",content)
                for i in range(1,len(split_content),2):
                    image_name = split_content[i]
                    image_name = image_name + '.eps'
                    old_image_path = os.path.join(path_beispieleinreichung_images, image_name)
                    new_image_path = os.path.join(path_programm, "_database", "Bilder", image_name)

                    shutil.move(os.path.join(path_beispieleinreichung_images, image_name),
                        os.path.join(path_programm, "_database", "Bilder", image_name)
                        )
                number_images += content.count("includegraphics")


        information_window(
            "Es wurden {0} Aufgaben und {1} Bild(er) in die Datenbank verschoben!".format(len(list_files_move), number_images),
            titel="Erfolgreich verschoben"
        )

        sys.exit(0)
 

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    MainWindow = QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())

