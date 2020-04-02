from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
import os
import datetime
from datetime import date
import json
from config import logo_path, path_programm
from translate import _fromUtf8, _translate
from sort_items import natural_keys

def modification_date(filename):
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
                + modification_date(log_file).strftime("%d.%m.%y - %H:%M"),
                None,
            )
        )
    QtWidgets.QApplication.restoreOverrideCursor()
    self.adapt_choosing_list("sage")
    self.adapt_choosing_list("feedback")
    msg.close()
