from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
import os
import datetime
from datetime import date
import json
from config import config_loader, logo_path, path_programm
from translate import _fromUtf8, _translate
from sort_items import natural_keys

config_file = os.path.join(path_programm, "_database", "_config", "config1.yml")
list_klassen = config_loader(config_file, "list_klassen")

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def search_files(dateipfad, beispieldaten_dateipfad):
    for root, dirs, files in os.walk(dateipfad):
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
                            #beispieldaten.append(line)
                            break
                    file.close()
    return beispieldaten_dateipfad#, beispieldaten

def save_log_file(self, log_file, beispieldaten_dateipfad):
    temp_dict_beispieldaten = {}
    temp_list = list(beispieldaten_dateipfad.keys())
    temp_list.sort(key=natural_keys)
    for all in temp_list:
        temp_dict_beispieldaten.update({all: beispieldaten_dateipfad[all]})

    beispieldaten_dateipfad = temp_dict_beispieldaten

    # print(beispieldaten_dateipfad)

    # log_file = os.path.join(
    #     path_programm, "Teildokument", "log_file_%s" % selected_aufgabentyp
    # )


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
            + modification_date(log_file).strftime("%d.%m.%y - %H:%M"),
            None,
        )
    )

def refresh_ddb(self):
    msg = QtWidgets.QMessageBox()
    msg.setWindowIcon(QtGui.QIcon(logo_path))
    msg.setWindowTitle("Refresh Database")
    msg.setStandardButtons(QtWidgets.QMessageBox.NoButton)
    msg.setText("Datenbank wird aktualisiert. Bitte warten...")

    msg.show()
    QApplication.processEvents()
    QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
    if self.chosen_program == 'lama':
        for selected_aufgabentyp in [1, 2]:
            beispieldaten_dateipfad = {}
            # beispieldaten = []
            chosen_aufgabenformat = "Typ%sAufgaben" % selected_aufgabentyp
            ########################################################
            ##### Suche offizielle Beispiele ####################
            ##################################################
            dateipfad=os.path.join(path_programm, "_database", chosen_aufgabenformat)
            search_files(dateipfad, beispieldaten_dateipfad)


            ################################################
            #### Suche inoffizielle Beispiele ######
            #############################################
            dateipfad=os.path.join(path_programm, "_database_inoffiziell", chosen_aufgabenformat)
            search_files(dateipfad, beispieldaten_dateipfad)


            ################################################
            #### Suche lokal gespeicherte Beispiele ######
            #############################################
            dateipfad=os.path.join(path_programm, "Lokaler_Ordner", chosen_aufgabenformat)
            search_files(dateipfad, beispieldaten_dateipfad)

            #########
            log_file = os.path.join(path_programm, "Teildokument", "log_file_%s" % selected_aufgabentyp)

            save_log_file(self, log_file, beispieldaten_dateipfad)

    if self.chosen_program == 'cria':
        beispieldaten_dateipfad = {}
        for klasse in list_klassen:
            #### offiziell ####
            dateipfad=os.path.join(path_programm, "_database", klasse)
            search_files(dateipfad, beispieldaten_dateipfad)

            ### inoffiziell ###
            dateipfad=os.path.join(path_programm, "_database_inoffiziell", klasse)
            search_files(dateipfad, beispieldaten_dateipfad)

            ### lokal ###
            dateipfad=os.path.join(path_programm, "Lokaler_Ordner", klasse)
            search_files(dateipfad, beispieldaten_dateipfad)                        

        
        log_file = os.path.join(path_programm, "Teildokument", "log_file_cria")


        save_log_file(self, log_file, beispieldaten_dateipfad)

    QtWidgets.QApplication.restoreOverrideCursor()
    self.adapt_choosing_list("sage")
    # self.adapt_choosing_list("feedback")
    msg.close()
