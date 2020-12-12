from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
import os
import datetime
from datetime import date
import json
from functools import partial
from config import config_file, config_loader, logo_path, path_programm, path_localappdata_lama
from translate import _fromUtf8, _translate
from sort_items import natural_keys, lama_order
from subwindows import Ui_Dialog_processing


list_klassen = config_loader(config_file, "list_klassen")


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


def search_files(dateipfad, beispieldaten_dateipfad={}):
    for root, dirs, files in os.walk(dateipfad):
        for all in files:
            if all.endswith(".tex") or all.endswith(".ltx"):
                if not ("Gesamtdokument" in all) and not ("Teildokument" in all):
                    file = open(os.path.join(root, all), "r", encoding="utf8")
                    for i, line in enumerate(file):
                        if not line == "\n":
                            beispieldaten_dateipfad[line] = os.path.join(root, all)
                            # beispieldaten.append(line)
                            break
                    file.close()
    return beispieldaten_dateipfad  # , beispieldaten


def save_log_file(self, log_file, beispieldaten_dateipfad):
    temp_dict_beispieldaten = {}
    temp_list = list(beispieldaten_dateipfad.keys())
    name_logfile = os.path.basename(log_file)
    if name_logfile == "log_file_2":
        temp_list.sort(key=lama_order)
    else:
        temp_list.sort(key=natural_keys)

    for all in temp_list:
        temp_dict_beispieldaten.update({all: beispieldaten_dateipfad[all]})

    beispieldaten_dateipfad = temp_dict_beispieldaten

    try:
        with open(log_file, "w+", encoding="utf8") as f:
            json.dump(beispieldaten_dateipfad, f, ensure_ascii=False)
    except FileNotFoundError:
        os.makedirs(os.path.join(path_localappdata_lama, "Teildokument"))
        with open(log_file, "w+", encoding="utf8") as f:
            json.dump(beispieldaten_dateipfad, f, ensure_ascii=False)


def collect_all_exisiting_files(self, selected_program):
    if selected_program == "lama":
        for selected_aufgabentyp in [1, 2]:
            beispieldaten_dateipfad = {}
            # beispieldaten = []
            chosen_aufgabenformat = "Typ%sAufgaben" % selected_aufgabentyp
            ########################################################
            ##### Suche offizielle Beispiele ####################
            ##################################################
            dateipfad = os.path.join(path_programm, "_database", chosen_aufgabenformat)
            beispieldaten_dateipfad = search_files(dateipfad, beispieldaten_dateipfad)

            ################################################
            #### Suche inoffizielle Beispiele ######
            #############################################
            dateipfad = os.path.join(
                path_programm, "_database_inoffiziell", chosen_aufgabenformat
            )
            beispieldaten_dateipfad = search_files(dateipfad, beispieldaten_dateipfad)

            ################################################
            #### Suche lokal gespeicherte Beispiele ######
            #############################################
            dateipfad = os.path.join(
                path_programm, "Lokaler_Ordner", chosen_aufgabenformat
            )
            beispieldaten_dateipfad = search_files(dateipfad, beispieldaten_dateipfad)

            #########
            log_file = os.path.join(
                path_localappdata_lama, "Teildokument","log_file_%s" % selected_aufgabentyp
            )

            save_log_file(self, log_file, beispieldaten_dateipfad)

    if selected_program == "cria":
        beispieldaten_dateipfad = {}
        for klasse in list_klassen:
            #### offiziell ####
            dateipfad = os.path.join(path_programm, "_database", klasse)
            search_files(dateipfad, beispieldaten_dateipfad)

            ### inoffiziell ###
            dateipfad = os.path.join(path_programm, "_database_inoffiziell", klasse)
            search_files(dateipfad, beispieldaten_dateipfad)

            ### lokal ###
            dateipfad = os.path.join(path_programm, "Lokaler_Ordner", klasse)
            search_files(dateipfad, beispieldaten_dateipfad)

        log_file = os.path.join(path_localappdata_lama, "Teildokument", "log_file_cria")

        save_log_file(self, log_file, beispieldaten_dateipfad)


class Worker_RefreshDDB(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    @QtCore.pyqtSlot()
    def task(self, Ui_Mainwindow, selected_program):
        collect_all_exisiting_files(Ui_Mainwindow, selected_program)
        # process = build_pdf_file(folder_name, file_name, latex_output_file)
        # process.poll()
        # latex_output_file.close()

        # loading_animation(process)

        # process.wait()

        self.finished.emit()


def refresh_ddb(self, selected_program=False):
    if selected_program == False:
        selected_program = self.chosen_program

    QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

    # msg = QtWidgets.QMessageBox()
    # msg.setWindowIcon(QtGui.QIcon(logo_path))
    # msg.setWindowTitle("Refresh Database")
    # msg.setStandardButtons(QtWidgets.QMessageBox.NoButton)
    # msg.setText("Datenbank wird aktualisiert. Bitte warten...")

    # msg.show()
    # QApplication.processEvents()

    text = "Datenbank wird aktualisiert. Bitte warten..."
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog_processing()
    ui.setupUi(Dialog, text)

    thread = QtCore.QThread(Dialog)
    worker = Worker_RefreshDDB()
    worker.finished.connect(Dialog.close)
    worker.moveToThread(thread)
    thread.started.connect(partial(worker.task, self, selected_program))
    thread.start()
    thread.exit()
    Dialog.exec()

    QtWidgets.QApplication.restoreOverrideCursor()
    # self.adapt_choosing_list("sage")
    # bring_to_front(QMainWindow())
    # self.adapt_choosing_list("feedback")
    # msg.close()
