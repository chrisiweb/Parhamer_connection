from ctypes import alignment
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QCursor, QTextCursor, QPixmap, QRegExpValidator
from PyQt5.QtCore import Qt, QSize, QRect, QMetaObject, QCoreApplication, QThread, QObject, pyqtSignal, pyqtSlot, QRegExp
import os
import shutil
from json import load, dump
import re
import sys
from pathlib import Path
from functools import partial
from config_start import path_programm,path_localappdata_lama, lama_settings_file, lama_developer_credentials, path_home, lama_notenschluessel_file, lama_individual_titlepage, cria_individual_titlepage
from config import (
    config_loader,
    dict_aufgabenformate,
    Klassen,
    config_file,
    colors_ui,
    get_color,
    logo_path,
    logo_cria_button_path,
    is_empty,
    get_icon_path,
    still_to_define,
)
from subprocess import Popen
from handle_exceptions import report_exceptions
from translate import _fromUtf8, _translate
from create_new_widgets import (
    create_new_verticallayout,
    create_new_horizontallayout,
    create_new_gridlayout,
    create_new_button,
    create_new_label,
    create_new_checkbox,
    create_new_combobox,
    create_new_spinbox,
    create_new_lineedit,
    create_new_groupbox,
    add_new_option,
)
from standard_dialog_windows import critical_window, information_window, question_window, warning_window
from predefined_size_policy import SizePolicy_fixed, SizePolicy_fixed_height, SizePolicy_fixed_width, SizePolicy_maximum, SizePolicy_maximum_width, SizePolicy_expanding, SizePolicy_minimum_width
from work_with_content import prepare_content_for_hide_show_items
from lama_stylesheets import (
    StyleSheet_tabWidget,
    StyleSheet_ausgleichspunkte,
    StyleSheet_ausgleichspunkte_dark_mode,
    StyleSheet_subwindow_ausgleichspunkte,
    StyleSheet_subwindow_ausgleichspunkte_dark_mode,
)
from create_pdf import create_tex, create_pdf, check_if_variation, create_info_box
import tex_minimal
from processing_window import Ui_Dialog_processing
import bcrypt
from database_commands import _database, _local_database, _database_addon, get_aufgabe_total, get_aufgabentyp, get_table, update_data, delete_file 
from filter_commands import get_filter_string, filter_items
from sort_items import order_gesammeltedateien
from upload_database import action_push_database
from tinydb import Query
from git_sync import check_branches, git_reset_repo_to_origin, check_internet_connection
from convert_image_to_eps import convert_image_to_eps
from build_titlepage import prepare_individual_titlepage

dict_gk = config_loader(config_file, "dict_gk")
ag_beschreibung = config_loader(config_file, "ag_beschreibung")
an_beschreibung = config_loader(config_file, "an_beschreibung")
fa_beschreibung = config_loader(config_file, "fa_beschreibung")
ws_beschreibung = config_loader(config_file, "ws_beschreibung")
list_klassen = config_loader(config_file, "list_klassen")

zusatzthemen_beschreibung = config_loader(config_file, "zusatzthemen_beschreibung")
for klasse in list_klassen:
    exec('dict_{0} = config_loader(config_file,"dict_{0}")'.format(klasse))
    exec('dict_{0}_name = config_loader(config_file,"dict_{0}_name")'.format(klasse))

dict_unterkapitel = config_loader(config_file, "dict_unterkapitel")

black = colors_ui["black"]
white = colors_ui["white"]
gray = colors_ui["gray"]
blue_1 = colors_ui["blue_1"]
blue_2 = colors_ui["blue_2"]
blue_3 = colors_ui["blue_3"]
blue_4 = colors_ui["blue_4"]
blue_5 = colors_ui["blue_5"]
blue_6 = colors_ui["blue_6"]
blue_7 = colors_ui["blue_7"]
red = colors_ui["red"]


def get_color(color):
    color = "rgb({0}, {1}, {2})".format(color.red(), color.green(), color.blue())
    return color


# StyleSheet_tabWidget = """
# QTabBar::tab:selected {{
# background: {0}; color: {1};
# padding-right: 10px; padding-left: 10px;
# border-top: 2px solid {3};
# border-left: 2px solid {3};
# border-right: 2px solid {3};
# }}

# QWidget {{color: {2};background-color: {3}}}
# """.format(
#     get_color(blue_2), get_color(black), get_color(white), get_color(blue_7)
# )

class Worker_UpdateDatabase(QObject):
    finished = pyqtSignal()

    @pyqtSlot()
    def task(self):
        git_reset_repo_to_origin()
        # print(Ui_MainWindow.reset_successfull)
        self.finished.emit()


def worker_update_database():
    text = "Die Datenbank wird auf den neuesten Stand gebracht ..."
    Dialog_checkchanges = QtWidgets.QDialog()
    ui = Ui_Dialog_processing()
    ui.setupUi(Dialog_checkchanges, text)

    thread = QThread(Dialog_checkchanges)
    worker = Worker_UpdateDatabase()
    worker.finished.connect(Dialog_checkchanges.close)
    worker.moveToThread(thread)
    thread.started.connect(worker.task)
    thread.start()
    thread.exit()
    Dialog_checkchanges.exec()

    # if self.reset_successfull == False:
    #     return False
    # else:
    #     return True


# class Ui_Dialog_Welcome_Window(object):
#     def setupUi(self, Dialog):
#         self.Dialog = Dialog
#         self.Dialog.setObjectName("Dialog")        
#         Dialog.setWindowTitle("Herzlich Willkommen bei LaMA")
#         self.gridLayout = create_new_gridlayout(self.Dialog)

#         self.label_1 = create_new_label(Dialog, """
# Herlich Willkommen!

# Es freut uns sehr, dass Sie sich für das Programm LaMA interessieren!
# Um starten zu können, muss LaMA zu Beginn konfiguriert werden. Dazu muss die Aufgabendatenbank heruntergeladen werden.

# Möchten Sie die Konfiguration beginnen und die Datenbank herunterladen?
#         """)

#         self.gridLayout.addWidget(self.label_1, 0,0,1,1)

#         self.buttonBox_welcome = QtWidgets.QDialogButtonBox(self.Dialog)
#         self.buttonBox_welcome.setStandardButtons(
#             QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
#         )

#         # buttonS = self.buttonBox_titlepage.button(QtWidgets.QDialogButtonBox.Save)
#         # buttonS.setText('Speichern')
#         buttonX = self.buttonBox_welcome.button(QtWidgets.QDialogButtonBox.Cancel)
#         buttonX.setText("Abbrechen")
#         self.buttonBox_welcome.setObjectName("buttonBox_variation")
#         self.buttonBox_welcome.rejected.connect(self.cancel_pressed)
#         self.buttonBox_welcome.accepted.connect(self.start_download)

#         self.gridLayout.addWidget(self.buttonBox_welcome, 1,0,1,1)

#     def cancel_pressed(self):
#         self.Dialog.reject()

#     def start_download(self):
#         self.Dialog.accept()      

class Ui_Dialog_choose_type(object):
    def setupUi(self, Dialog, screen_width, screen_height):
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle(
            _translate("Titelblatt anpassen", "Programm auswählen", None)
        )
        Dialog.setWindowIcon(QIcon(logo_path))

        Dialog.setSizePolicy(SizePolicy_fixed)
        verticalLayout = create_new_verticallayout(Dialog)
        verticalLayout.setContentsMargins(8, 8, 8, 30)

        button_height = 32

        
        label_logo = create_new_label(Dialog, "")
        logo = os.path.join(
            path_programm, "_database", "_config", "icon", "LaMA_logo_full.png"
        )
        label_logo.setPixmap(QPixmap(logo))

        label_logo.setFixedSize(QSize(screen_width*0.1,screen_height*0.07))
        label_logo.setScaledContents(True)

        verticalLayout.addWidget(label_logo, alignment=Qt.AlignCenter)

        verticalLayout.addStretch()

        self.btn_lama_cria = create_new_button(Dialog, "Unterstufe", partial(self.choose_button_pressed, "cria"), "database.svg")

        self.btn_lama_cria.setStyleSheet("QPushButton { text-align: left; padding-left: 8px}")
        self.btn_lama_cria.setAutoDefault(False)
        self.btn_lama_cria.setShortcut("F1")
        self.btn_lama_cria.setFixedHeight(button_height)

        verticalLayout.addWidget(self.btn_lama_cria, alignment=Qt.AlignCenter)

        self.btn_lama = create_new_button(Dialog, "Oberstufe", partial(self.choose_button_pressed, "lama"), "database.svg")

        self.btn_lama.setFixedHeight(button_height)
        self.btn_lama.setStyleSheet("QPushButton { text-align: left; padding-left: 8px}")

        self.btn_lama.setShortcut("F2")
        self.btn_lama.setAutoDefault(False)
        verticalLayout.addWidget(self.btn_lama ,alignment=Qt.AlignCenter)



        self.btn_worksheet = create_new_button(Dialog, "Worksheet Wizard", partial(self.choose_button_pressed, "wizard"), "file-text.svg")
        self.btn_worksheet.setFixedHeight(button_height)
        self.btn_worksheet.setStyleSheet("QPushButton { text-align: left; padding-left: 8px}") #; padding-right:8px}

        self.btn_worksheet.setShortcut("F3")
        self.btn_worksheet.setAutoDefault(False)
        self.btn_worksheet.resize(self.btn_worksheet.sizeHint())

        verticalLayout.addWidget(self.btn_worksheet, alignment=Qt.AlignCenter)

        if label_logo.width()<self.btn_worksheet.size().width()+10:
            width = self.btn_worksheet.size().width()+10
        else:
            width = label_logo.width()
        self.btn_worksheet.setFixedWidth(width)
        self.btn_lama.setFixedWidth(width)
        self.btn_lama_cria.setFixedWidth(width)
        Dialog.setFixedWidth(width+50)
        Dialog.setFixedHeight(260)


        

    def choose_button_pressed(self, chosen_program):
        self.chosen_program = chosen_program
        self.Dialog.accept()



class Ui_Dialog_variation(object):
    def setupUi(self, Dialog, MainWindow, show_variations, mode=None, chosen_file_to_edit= None):
        self.MainWindow = MainWindow
        self.chosen_program = self.MainWindow.chosen_program

        self.show_variations = show_variations
        self.mode = mode
        self.chosen_file_to_edit = chosen_file_to_edit
        # self.beispieldaten_dateipfad_cria = MainWindow.beispieldaten_dateipfad_cria
        # self.beispieldaten_dateipfad_1 = MainWindow.beispieldaten_dateipfad_1
        # self.beispieldaten_dateipfad_2 = MainWindow.beispieldaten_dateipfad_2

        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("Vorhandene Aufgabe auswählen")
        Dialog.setWindowIcon(QIcon(logo_path))
        verticalLayout_variation = create_new_verticallayout(Dialog)

        self.groupBox_alle_aufgaben = QtWidgets.QGroupBox()
        self.groupBox_alle_aufgaben.setMinimumWidth(1)
        self.groupBox_alle_aufgaben.setObjectName("groupBox_alle_aufgaben")

        self.verticalLayout_sage = QtWidgets.QVBoxLayout(self.groupBox_alle_aufgaben)
        self.verticalLayout_sage.setObjectName("verticalLayout_sage")

        ##### ComboBox LaMA ####
        if self.MainWindow.chosen_program == "lama":
            self.comboBox_at_sage = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
            self.comboBox_at_sage.setObjectName("comboBox_at_sage")
            self.comboBox_at_sage.addItem("")
            self.comboBox_at_sage.addItem("")
            self.verticalLayout_sage.addWidget(self.comboBox_at_sage)
            self.comboBox_at_sage.setItemText(
                0, _translate("MainWindow", "Typ 1", None)
            )
            self.comboBox_at_sage.setItemText(
                1, _translate("MainWindow", "Typ 2", None)
            )
            self.comboBox_at_sage.currentIndexChanged.connect(
                self.comboBox_at_sage_changed
            )
            self.comboBox_at_sage.setFocusPolicy(Qt.ClickFocus)

            # self.comboBox_at_sage.hide()

            self.comboBox_gk = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
            self.comboBox_gk.setObjectName("comboBox_gk")
            list_comboBox_gk = ["", "AG", "FA", "AN", "WS", "Zusatzthemen"]
            index = 0
            for all in list_comboBox_gk:
                self.comboBox_gk.addItem("")
                self.comboBox_gk.setItemText(index, _translate("MainWindow", all, None))
                index += 1
            self.comboBox_gk.currentIndexChanged.connect(self.comboBox_gk_changed)
            self.comboBox_gk.setFocusPolicy(Qt.ClickFocus)
            self.verticalLayout_sage.addWidget(self.comboBox_gk)
            self.comboBox_gk_num = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
            self.comboBox_gk_num.setObjectName("comboBox_gk_num")
            self.comboBox_gk_num.currentIndexChanged.connect(self.adapt_choosing_list)
            self.comboBox_gk_num.setFocusPolicy(Qt.ClickFocus)
            self.verticalLayout_sage.addWidget(self.comboBox_gk_num)

        ##### ComboBox LaMA Cria ####
        if self.MainWindow.chosen_program == "cria":
            self.comboBox_klassen = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
            self.comboBox_klassen.setObjectName("comboBox_klassen")
            self.comboBox_klassen.addItem("")
            index = 1
            
            for all in list_klassen:
                self.comboBox_klassen.addItem("")

                self.comboBox_klassen.setItemText(
                    index, _translate("MainWindow", all[1] + ". Klasse", None)
                )
                index += 1

            self.comboBox_klassen.currentIndexChanged.connect(
                self.comboBox_klassen_changed
            )

            self.comboBox_klassen.setFocusPolicy(Qt.ClickFocus)
            self.verticalLayout_sage.addWidget(self.comboBox_klassen)

            self.comboBox_kapitel = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
            self.comboBox_kapitel.setObjectName("comboBox_kapitel")
            self.comboBox_kapitel.currentIndexChanged.connect(
                self.comboBox_kapitel_changed
            )
            self.comboBox_kapitel.setFocusPolicy(Qt.ClickFocus)
            self.verticalLayout_sage.addWidget(self.comboBox_kapitel)

            self.comboBox_unterkapitel = QtWidgets.QComboBox(
                self.groupBox_alle_aufgaben
            )
            self.comboBox_unterkapitel.setObjectName("comboBox_unterkapitel")
            self.comboBox_unterkapitel.currentIndexChanged.connect(
                self.adapt_choosing_list
            )
            self.comboBox_unterkapitel.setFocusPolicy(Qt.ClickFocus)
            self.verticalLayout_sage.addWidget(self.comboBox_unterkapitel)

        self.lineEdit_number = QtWidgets.QLineEdit(self.groupBox_alle_aufgaben)
        self.lineEdit_number.setObjectName("lineEdit_number")
        # self.lineEdit_number.setValidator(QIntValidator())
        self.lineEdit_number.textChanged.connect(self.adapt_choosing_list)
        self.verticalLayout_sage.addWidget(self.lineEdit_number)
        self.listWidget = QtWidgets.QListWidget(self.groupBox_alle_aufgaben)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.itemDoubleClicked.connect(self.choose_example)
        self.verticalLayout_sage.addWidget(self.listWidget)

        self.groupBox_alle_aufgaben.setTitle(_translate("MainWindow", "Aufgaben", None))

        verticalLayout_variation.addWidget(self.groupBox_alle_aufgaben)

        self.buttonBox_variation = QtWidgets.QDialogButtonBox(self.Dialog)
        self.buttonBox_variation.setStandardButtons(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )

        # buttonS = self.buttonBox_titlepage.button(QtWidgets.QDialogButtonBox.Save)
        # buttonS.setText('Speichern')
        buttonX = self.buttonBox_variation.button(QtWidgets.QDialogButtonBox.Cancel)
        buttonX.setText("Abbrechen")
        self.buttonBox_variation.setObjectName("buttonBox_variation")
        self.buttonBox_variation.rejected.connect(self.cancel_pressed)
        self.buttonBox_variation.accepted.connect(self.choose_example)
        verticalLayout_variation.addWidget(self.buttonBox_variation)
        self.adapt_choosing_list()

        if self.MainWindow.chosen_program == "lama":
            self.comboBox_at_sage.setCurrentIndex(
                self.MainWindow.comboBox_aufgabentyp_cr.currentIndex()
            )
        # elif self.MainWindow.chosen_program == "cria":
        #     self.comboBox_klassen.setCurrentIndex(
        #         self.MainWindow.tab_widget_cr_cria.currentIndex()
        #     )

    def cancel_pressed(self):
        self.Dialog.reject()

    def choose_example(self):
        try:
            if self.listWidget.selectedItems()[0].text() == self.no_choice:
                self.chosen_variation = None
            elif self.MainWindow.chosen_program == "cria":
                klasse = list_klassen[self.comboBox_klassen.currentIndex()]
                self.chosen_variation = self.listWidget.selectedItems()[0].text()
                # (
                #     klasse + "." + self.listWidget.selectedItems()[0].text()
                # )
            else:
                self.chosen_variation = self.listWidget.selectedItems()[0].text()

        except IndexError:
            self.chosen_variation = None
        self.Dialog.accept()

    def comboBox_at_sage_changed(self):
        if self.comboBox_at_sage.currentText()[-1] == "1":
            self.comboBox_gk.clear()
            self.lineEdit_number.clear()
            self.comboBox_gk.setEnabled(True)
            self.comboBox_gk_num.setEnabled(True)
            list_comboBox_gk = ["", "AG", "FA", "AN", "WS", "Zusatzthemen"]
            index = 0
            for all in list_comboBox_gk:
                self.comboBox_gk.addItem("")
                self.comboBox_gk.setItemText(index, _translate("MainWindow", all, None))
                index += 1
            self.comboBox_gk_num.clear()

        if self.comboBox_at_sage.currentText()[-1] == "2":
            self.comboBox_gk.setCurrentIndex(0)
            self.comboBox_gk_num.setCurrentIndex(0)
            self.comboBox_gk.setEnabled(False)
            self.comboBox_gk_num.setEnabled(False)

        self.adapt_choosing_list()

    def comboBox_gk_changed(self):
        self.adapt_choosing_list()

        self.comboBox_gk_num.clear()
        if self.comboBox_gk.currentText() == "":
            return
        self.comboBox_gk_num.addItem("")
        self.lineEdit_number.clear()
        # list_klassen = ["k5", "k6", "k7", "k8"]
        if self.comboBox_gk.currentText() == "Zusatzthemen":
            #     x = eval("%s_beschreibung" % self.comboBox_gk.currentText().lower())
            for all in zusatzthemen_beschreibung:
                label = zusatzthemen_beschreibung[all] + " (" + all + ")"
                self.comboBox_gk_num.addItem(label)
        else:
            for all in dict_gk.keys():
                if all.startswith(self.comboBox_gk.currentText().lower()):
                    self.comboBox_gk_num.addItem(dict_gk[all][-3:])

    def comboBox_klassen_changed(self):
        dict_klasse_name = eval(
            "dict_{}_name".format(list_klassen[self.comboBox_klassen.currentIndex()-1])
        )
        self.comboBox_kapitel.clear()
        self.comboBox_unterkapitel.clear()
        self.comboBox_kapitel.addItem("")

        for all in dict_klasse_name.keys():
            self.comboBox_kapitel.addItem(dict_klasse_name[all] + " (" + all + ")")

    def comboBox_kapitel_changed(self):
        dict_klasse = eval(
            "dict_{}".format(list_klassen[self.comboBox_klassen.currentIndex()-1])
        )

        # dict_klasse = eval(
        #     "dict_{}".format(list_klassen[self.comboBox_klassen.currentIndex()-1])
        # )
        self.comboBox_unterkapitel.clear()

        kapitel_shortcut = list(dict_klasse.keys())[
            self.comboBox_kapitel.currentIndex() - 1
        ]

        # self.comboBox_unterkapitel.clear()
        self.comboBox_unterkapitel.addItem("")

        index = 1
        for all in dict_klasse[kapitel_shortcut]:
            self.comboBox_unterkapitel.addItem(
                dict_unterkapitel[all] + " (" + all + ")"
            )

            index += 1

        if self.comboBox_kapitel.currentIndex() == 0:
            self.comboBox_unterkapitel.clear()

        self.adapt_choosing_list()


    def delete_zeros_at_beginning(self, string):
        while string.startswith("0"):
            string = string[1:]
        return string

    def split_section(self, section):
        section = re.split(" - |{|}", section)
        info = [item.strip() for item in section]
        info.pop(0)
        info.pop(-1)

        return info

    def search_for_number(self, list_, line_entry):
        for section in list_[:]:
            info = self.split_section(section)
            if self.MainWindow.chosen_program == "lama":
                combobox_at = self.comboBox_at_sage.currentText()

                if combobox_at == "Typ 1":
                    number = self.delete_zeros_at_beginning(info[1])
                if combobox_at == "Typ 2":
                    number = self.delete_zeros_at_beginning(info[0])

            elif self.MainWindow.chosen_program == "cria":
                number = self.delete_zeros_at_beginning(info[2])
            if not number.startswith(line_entry):
                list_.remove(section)

        return list_


    def add_items_to_listwidget_creator(self, typ, filtered_items, local = False):
        for _file_ in filtered_items:
            if self.mode == 'editor' and _file_['draft'] == True:
                continue
            # if typ == "cria":
            #     name = _file_["name"].split(".", 1)[-1]
            # else:
            name = _file_["name"]

            item = QtWidgets.QListWidgetItem()

            if local == True:
                name = name + " (lokal)"
            #     # item.setBackground(blue_4)
            #     # item.setToolTip("lokal gespeichert")

            # elif _file_["draft"] == True:
            #     item.setBackground(blue_5)
            #     item.setForeground(white)
            #     item.setToolTip("Entwurf")

            item.setText(name)

            if self.show_variations==False and check_if_variation(_file_["name"]) == True:
                continue
            elif self.show_variations==False and self.chosen_file_to_edit == _file_["name"]:
                continue
            else:
                self.listWidget.addItem(item)

    def get_klasse(self, list_mode):
        if self.comboBox_klassen.currentIndex()==0:
            klasse = None
        else:
            klasse = list_klassen[self.comboBox_klassen.currentIndex()-1]
        # elif mode == "feedback":
        #     if self.comboBox_klassen.currentIndex()==0:
        #         klasse = None
        #     else:
        #         klasse = list_klassen[self.comboBox_klassen_fb_cria.currentIndex()]
        # print(klasse)
        return klasse


    def adapt_choosing_list(self):
        QtWidgets.QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        chosen_program = self.MainWindow.chosen_program
        klasse = None
        if chosen_program == "cria":
            typ = "cria"
            klasse = list_klassen[self.comboBox_klassen.currentIndex()-1]
        elif self.comboBox_at_sage.currentIndex()==0:
            typ = "lama_1"

        elif self.comboBox_at_sage.currentIndex()==1:
            typ = "lama_2"

        filter_string = get_filter_string(self, 'sage')        

        line_entry = self.lineEdit_number.text()


        table = "table_" + typ

        self.listWidget.clear()
        self.no_choice = "-- keine Auswahl --"
        self.listWidget.addItem(self.no_choice)
        _list_database = [_local_database, _database]
        if _database_addon != None:
            _list_database.append(_database_addon)
        # print(_list_database)
        # print(len(_list_database))
        all_filtered_items = []
        # print(self.mode)
        for database in _list_database:
            # print(database)
            if database == _database_addon and self.mode == 'creator':
                continue
            elif self.MainWindow.developer_mode_active == False and self.mode != 'creator':
                if database == _database or database == _database_addon:
                    continue

            table_lama = database.table(table)
            if database == _local_database:
                local = True
            else:
                local = False

            filtered_items = filter_items(
                self, table_lama, typ, 'creator', filter_string, line_entry
            )

            
            all_filtered_items = all_filtered_items + filtered_items
        
        # print(all_filtered_items)
        all_filtered_items.sort(key=lambda text: order_gesammeltedateien(text, typ, cria_plain_number_order=True))

        self.add_items_to_listwidget_creator(typ, all_filtered_items, local)
        QtWidgets.QApplication.restoreOverrideCursor()
        


class Ui_Dialog_random_quiz(object):
    def setupUi(self, Dialog, Ui_MainWindow):
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("Zufälliges Quiz")
        Dialog.setWindowIcon(QIcon(logo_path))
        self.gridlayout_random_quiz = QtWidgets.QGridLayout(Dialog)
        self.gridlayout_random_quiz.setObjectName("gridlayout_random_quiz")

        self.groupBox_gk = create_new_groupbox(Dialog, "Grundkompetenzen auswählen")

        self.gridLayout_11 = create_new_gridlayout(self.groupBox_gk)
        self.tab_widget_gk = QtWidgets.QTabWidget(self.groupBox_gk)

        self.tab_widget_gk.setStyleSheet(StyleSheet_tabWidget)
        self.tab_widget_gk.setObjectName(_fromUtf8("tab_widget_gk"))
        self.gridLayout_11.addWidget(self.tab_widget_gk, 0, 0, 1, 1)
        self.gridlayout_random_quiz.addWidget(self.groupBox_gk, 0, 0, 1, 3)

        Ui_MainWindow.create_tab_checkboxes_gk(
            self.tab_widget_gk, "Algebra und Geometrie", ag_beschreibung, "quiz"
        )
        Ui_MainWindow.create_tab_checkboxes_gk(
            self.tab_widget_gk, "Funktionale Abhängigkeiten", fa_beschreibung, "quiz"
        )
        Ui_MainWindow.create_tab_checkboxes_gk(
            self.tab_widget_gk, "Analysis", an_beschreibung, "quiz"
        )
        Ui_MainWindow.create_tab_checkboxes_gk(
            self.tab_widget_gk,
            "Wahrscheinlichkeit und Statistik",
            ws_beschreibung,
            "quiz",
        )

        self.groupBox_aufgaben = create_new_groupbox(Dialog, "Anzahl der Aufgaben")
        self.gridlayout_random_quiz.addWidget(self.groupBox_aufgaben, 1, 0, 2, 1)
        self.spinbox_number_aufgaben = create_new_spinbox(Dialog, 10)
        self.verticalLayout_aufgaben = create_new_verticallayout(self.groupBox_aufgaben)
        self.verticalLayout_aufgaben.addWidget(self.spinbox_number_aufgaben)

        self.button_create_quiz = create_new_button(
            Dialog, "Quiz erstellen", partial(self.create_quiz, Ui_MainWindow)
        )
        self.gridlayout_random_quiz.addWidget(self.button_create_quiz, 1, 2, 1, 1)
        self.button_create_quiz.setFocus()

        self.button_cancel = create_new_button(
            Dialog, "Abbrechen", self.random_quiz_cancel
        )
        self.gridlayout_random_quiz.addWidget(self.button_cancel, 2, 2, 1, 1)

    def random_quiz_cancel(self):
        self.Dialog.reject()

    def create_quiz(self, Ui_MainWindow):
        chosen_gk = []
        for widget in Ui_MainWindow.dict_widget_variables:
            if widget.startswith("checkbox_quiz_"):
                if Ui_MainWindow.dict_widget_variables[widget].isChecked() == True:
                    gk = widget.split("_")[-1]
                    chosen_gk.append(dict_gk[gk])

        self.random_quiz_response = [self.spinbox_number_aufgaben.value(), chosen_gk]
        self.Dialog.accept()



class Ui_Dialog_titlepage(object):
    def setupUi(self, Dialog, dict_titlepage, MainWindow):
        
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle(
            _translate("Titelblatt anpassen", "Titelblatt anpassen", None)
        )
        # self.Dialog.resize(600, 400)
        # self.Dialog.setWindowIcon(QIcon(logo_path))
        # Dialog.setObjectName("Dialog")
        # Dialog.resize(468, 208)
        Dialog.setWindowIcon(QIcon(logo_path))
        self.verticalLayout_titlepage = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_titlepage.setObjectName("verticalLayout_titlepage")

        self.widget_label_logo = QtWidgets.QWidget(Dialog)
        self.verticalLayout_titlepage.addWidget(self.widget_label_logo)
        horizontallayout_label_logo = create_new_horizontallayout(self.widget_label_logo)
        horizontallayout_label_logo.setContentsMargins(0,0,0,0)

        self.label_logo_1 = create_new_label(self.widget_label_logo, "Dateipfad Logo: ")
        horizontallayout_label_logo.addWidget(self.label_logo_1)

        self.label_logo_2 = create_new_label(self.widget_label_logo, "---")
        horizontallayout_label_logo.addWidget(self.label_logo_2)

        if dict_titlepage["logo_path"] != False:
            logo_name = os.path.basename(dict_titlepage["logo_path"])
            self.label_logo_2.setText(logo_name)

        horizontallayout_label_logo.addStretch()


        self.btn_titlepage_logo_path = create_new_button(self.widget_label_logo, "", partial(self.btn_titlepage_logo_path_pressed, dict_titlepage),
                                                         icon = "folder.svg")
        horizontallayout_label_logo.addWidget(self.btn_titlepage_logo_path)


        # self.btn_titlepage_logo_path.setText("Durchsuchen")
        # self.btn_titlepage_logo_path.setIcon(QIcon(get_icon_path('folder.svg')))
        # self.btn_titlepage_logo_path.setMaximumWidth(130)
        # self.btn_titlepage_logo_path.clicked.connect(
            
        # )


        self.groupBox_titlepage = QtWidgets.QGroupBox()
        self.groupBox_titlepage.setObjectName("groupBox_titlepage")
        self.verticalLayout_gBtitlepage = QtWidgets.QVBoxLayout(self.groupBox_titlepage)
        self.verticalLayout_gBtitlepage.setObjectName("verticalLayout_gBtitlepage")
        self.groupBox_titlepage.setTitle(
            _translate("MainWindow", "Gewünschte Anzeige am Titelblatt", None)
        )
        self.verticalLayout_titlepage.addWidget(self.groupBox_titlepage)


        self.widget_individual_titlepage = QtWidgets.QWidget(Dialog)
        horizontallayout_individual_titlepage = create_new_horizontallayout(self.widget_individual_titlepage)
        horizontallayout_individual_titlepage.setContentsMargins(0, 0, 0, 0)


        self.verticalLayout_titlepage.addWidget(self.widget_individual_titlepage)


        self.cb_titlepage_hide_all = QtWidgets.QCheckBox("Kein Titelblatt")
        self.cb_titlepage_hide_all.setObjectName(_fromUtf8("cb_titlepage_hide_all"))
        self.verticalLayout_titlepage.addWidget(self.cb_titlepage_hide_all)
        self.cb_titlepage_hide_all.stateChanged.connect(
            self.cb_titlepage_hide_all_pressed
        )
        try:
            self.cb_titlepage_hide_all.setChecked(dict_titlepage["hide_all"])
        except KeyError:
            dict_titlepage["hide_all"] = False

        self.cb_titlepage_logo = QtWidgets.QCheckBox("Logo")


        self.cb_titlepage_logo.setObjectName(_fromUtf8("cb_titlepage_logo"))
        self.verticalLayout_gBtitlepage.addWidget(self.cb_titlepage_logo)
        self.cb_titlepage_logo.setChecked(dict_titlepage["logo"])


        self.cb_titlepage_titel = QtWidgets.QCheckBox("Titel")
        self.cb_titlepage_titel.setObjectName(_fromUtf8("cb_titlepage_titel"))
        self.verticalLayout_gBtitlepage.addWidget(self.cb_titlepage_titel)
        self.cb_titlepage_titel.setChecked(dict_titlepage["titel"])


        self.widget_titlepage_datum = QtWidgets.QWidget(self.groupBox_titlepage)
        # self.widget_titlepage_datum.setFrameShape(QtWidgets.QFrame.NoFrame)
        horizontallayout_datum = create_new_horizontallayout(self.widget_titlepage_datum)
        horizontallayout_datum.setContentsMargins(0, 0, 0, 0)
        self.cb_titlepage_datum = create_new_checkbox(self.widget_titlepage_datum, "Datum", checked=dict_titlepage["datum"])
        
        horizontallayout_datum.addWidget(self.cb_titlepage_datum)

        

        self.combobox_titlepage_datum = create_new_combobox(self.widget_titlepage_datum)
        add_new_option(self.combobox_titlepage_datum, 0, "Kalender")
        add_new_option(self.combobox_titlepage_datum, 1, "leer")
        horizontallayout_datum.addWidget(self.combobox_titlepage_datum)

        try:
            self.combobox_titlepage_datum.setCurrentIndex(dict_titlepage["datum_combobox"])
        except KeyError:
            self.combobox_titlepage_datum.setCurrentIndex(0)


        def disable_combobox_datum():
            self.combobox_titlepage_datum.setEnabled(self.cb_titlepage_datum.isChecked())
            
        disable_combobox_datum()
        self.cb_titlepage_datum.stateChanged.connect(disable_combobox_datum)
        horizontallayout_datum.addStretch()

        self.verticalLayout_gBtitlepage.addWidget(self.widget_titlepage_datum)

        self.cb_titlepage_klasse = QtWidgets.QCheckBox("Klasse")
        self.cb_titlepage_klasse.setObjectName(_fromUtf8("cb_titlepage_klasse"))
        self.verticalLayout_gBtitlepage.addWidget(self.cb_titlepage_klasse)
        self.cb_titlepage_klasse.setChecked(dict_titlepage["klasse"])

        self.cb_titlepage_name = QtWidgets.QCheckBox("Name")
        self.cb_titlepage_name.setObjectName(_fromUtf8("cb_titlepage_name"))
        self.verticalLayout_gBtitlepage.addWidget(self.cb_titlepage_name)
        self.cb_titlepage_name.setChecked(dict_titlepage["name"])

        self.cb_titlepage_note = QtWidgets.QCheckBox("Note")
        self.cb_titlepage_note.setObjectName(_fromUtf8("cb_titlepage_note"))
        self.verticalLayout_gBtitlepage.addWidget(self.cb_titlepage_note)
        self.cb_titlepage_note.setChecked(dict_titlepage["note"])

        self.cb_titlepage_unterschrift = QtWidgets.QCheckBox("Unterschrift")
        self.cb_titlepage_unterschrift.setObjectName(
            _fromUtf8("cb_titlepage_unterschrift")
        )
        self.verticalLayout_gBtitlepage.addWidget(self.cb_titlepage_unterschrift)
        self.cb_titlepage_unterschrift.setChecked(dict_titlepage["unterschrift"])

        self.cb_titlepage_individual = create_new_checkbox(self.widget_individual_titlepage, "Individuelles Titelblatt")
        horizontallayout_individual_titlepage.addWidget(self.cb_titlepage_individual)


        try:
            self.cb_titlepage_individual.setChecked(dict_titlepage["individual"])
            if self.cb_titlepage_individual.isChecked() == True:
                self.groupBox_titlepage.setEnabled(False)
        except KeyError:
            dict_titlepage["individual"] = False

        self.cb_titlepage_individual.stateChanged.connect(
            partial(self.cb_titlepage_individual_pressed, MainWindow)
        )

        self.btn_individual_titlepage = create_new_button(self.widget_individual_titlepage, "", partial(self.open_individual_titlepage, MainWindow), icon="edit.svg")
        horizontallayout_individual_titlepage.addWidget(self.btn_individual_titlepage)

        horizontallayout_individual_titlepage.addStretch()




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
            partial(self.save_titlepage, dict_titlepage, MainWindow.chosen_program)
        )
        # self.retranslateUi(self.Dialog)

        self.verticalLayout_titlepage.addWidget(self.buttonBox_titlepage)

        return dict_titlepage

    def cb_titlepage_individual_pressed(self, MainWindow):
        print(self.cb_titlepage_individual.isChecked())
        if self.cb_titlepage_individual.isChecked() == True:
            self.groupBox_titlepage.setEnabled(False)
            if MainWindow.chosen_program == 'lama':
                individual_titlepage = lama_individual_titlepage
            elif MainWindow.chosen_program == 'cria':
                individual_titlepage = cria_individual_titlepage

            if not os.path.isfile(individual_titlepage):
                self.open_individual_titlepage(MainWindow)


        if self.cb_titlepage_individual.isChecked() == False:
            self.groupBox_titlepage.setEnabled(True)        

    def cb_titlepage_hide_all_pressed(self):
        if self.cb_titlepage_hide_all.isChecked() == True:
            self.widget_individual_titlepage.setEnabled(False)
            self.groupBox_titlepage.setEnabled(False)
        if self.cb_titlepage_hide_all.isChecked() == False:
            self.widget_individual_titlepage.setEnabled(True)
            if self.cb_titlepage_individual.isChecked() == False:
                self.groupBox_titlepage.setEnabled(True)
            

    def btn_titlepage_logo_path_pressed(self, dict_titlepage):
        logo_titlepage_path = QtWidgets.QFileDialog.getOpenFileNames(
            None, "Grafiken wählen", path_programm, "Grafiken (*.eps)"
        )
        if logo_titlepage_path[0] == []:
            return

        logo_name = os.path.basename(logo_titlepage_path[0][0])

        # self.cb_titlepage_logo.setText("Logo ({})".format(logo_name))
        print(logo_name)
        self.label_logo_2.setText(logo_name)
        dict_titlepage["logo_path"] = "{}".format(logo_titlepage_path[0][0])
        copy_logo_titlepage_path = os.path.join(
            path_localappdata_lama, "Teildokument", logo_name
        )
        try:
            shutil.copy(logo_titlepage_path[0][0], copy_logo_titlepage_path)
        except shutil.SameFileError:
            pass

        return dict_titlepage

    def open_individual_titlepage(self, MainWindow):
        Dialog = QtWidgets.QDialog(
            None,
            Qt.WindowSystemMenuHint
            | Qt.WindowTitleHint
            | Qt.WindowCloseButtonHint,
        )

        Dialog.setWindowTitle("Titelblatt bearbeiten")
        Dialog.setWindowIcon(QIcon(logo_path)) 
        Dialog.resize(700,500)


        verticalLayout = create_new_verticallayout(Dialog)

        widget_titel = QtWidgets.QWidget(Dialog)
        verticalLayout.addWidget(widget_titel)
        self.horizontallayout_titel = create_new_horizontallayout(widget_titel)
        self.horizontallayout_titel.setContentsMargins(0,0,0,0)

        self.plainTextEdit_instructions = QtWidgets.QPlainTextEdit()
        # self.plainTextEdit_instructions.setPlainText(text)

        # dict_titlepage = self.get_dict_titlepage(dict_titlepage)
        # print(dict_titlepage)
        # from build_titlepage import get_titlepage_vorschau()

        if MainWindow.chosen_program == "lama":
            individual_titlepage = lama_individual_titlepage
        elif MainWindow.chosen_program == "cria":
            individual_titlepage = cria_individual_titlepage

        try:
            with open(individual_titlepage, "r", encoding="utf8") as f:
                string_titlepage = load(f)
        except FileNotFoundError:
            string_titlepage = """\\flushright
\\begin{minipage}[t]{0.4\\textwidth}
[[LOGO]]
\end{minipage} \\\\ [1cm] 
\\textsc{\Huge [[TITEL]]}\\\\ [0.5cm] 

\\vspace{0.8cm}

\Large [[DATUM]]\\\\ [0.8cm] 

\\textsc{\Large Klasse [[KLASSE]]} \\\\ [1cm] 

\Large Name: \\rule{8cm}{0.4pt} \\\\ [1cm]

\Large Note: \\rule{8cm}{0.4pt} \\\\ [1cm]

\Large Unterschrift: \\rule{8cm}{0.4pt} \\\\ [1cm]

\\vspace{1cm}

\\vfill

\large[[BEURTEILUNGSRASTER]]"""

        self.plainTextEdit_instructions.setPlainText(string_titlepage)
        verticalLayout.addWidget(self.plainTextEdit_instructions)


        widget_buttons = QtWidgets.QWidget(Dialog)
        verticalLayout.addWidget(widget_buttons)
        horizontallayout_widget_buttons = create_new_horizontallayout(widget_buttons)
        horizontallayout_widget_buttons.setContentsMargins(0,0,0,0)

        self.button_preview = create_new_button(Dialog, "Vorschau", partial(self.button_preview_pressed, MainWindow), icon='eye.svg')
        self.button_preview.setShortcut("Ctrl+Return")
        self.button_preview.setToolTip("Strg+Enter")
        horizontallayout_widget_buttons.addWidget(self.button_preview)

        horizontallayout_widget_buttons.addStretch()

        buttonBox = QtWidgets.QDialogButtonBox(widget_buttons)
        buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        horizontallayout_widget_buttons.addWidget(buttonBox)



        
        # buttonPreview = buttonBox.button(QtWidgets.QDialogButtonBox.Open)
        # buttonPreview.setText("Vorschau")
        # buttonPreview.clicked.connect(still_to_define)

        buttonCancel = buttonBox.button(QtWidgets.QDialogButtonBox.Cancel)
        buttonCancel.setText("Abbrechen")
        
        
        buttonBox.rejected.connect(Dialog.reject)
        buttonBox.accepted.connect(Dialog.accept)

        rsp = Dialog.exec()

        if MainWindow.chosen_program == "lama":
            individual_titlepage = lama_individual_titlepage
        elif MainWindow.chosen_program == "cria":
            individual_titlepage == cria_individual_titlepage

        
        try:
            if rsp == 1:
                with open(individual_titlepage, "w+", encoding="utf8") as f:
                    dump(self.plainTextEdit_instructions.toPlainText(), f, ensure_ascii=False)
            elif rsp == 0 and not os.path.isfile(individual_titlepage):
                self.cb_titlepage_individual.setChecked(False)
                with open(individual_titlepage, "w+", encoding="utf8") as f:
                    dump(self.plainTextEdit_instructions.toPlainText(), f, ensure_ascii=False)
        except FileNotFoundError:
            os.makedirs(individual_titlepage)
            with open(individual_titlepage, "w+", encoding="utf8") as f:
                dump(self.plainTextEdit_instructions.toPlainText(), f, ensure_ascii=False)

      

    def button_preview_pressed(self, MainWindow):
        file_path = os.path.join(
            path_localappdata_lama, "Teildokument", "preview.tex"
            )
        MainWindow.collect_all_infos_for_creating_file()
        titlepage = prepare_individual_titlepage(self.plainTextEdit_instructions.toPlainText(), MainWindow)

        rsp = create_tex(file_path, titlepage, pagebreak=None, solution="solution_off")

        if rsp == True:
            create_pdf("preview")
        else:
            critical_window("Die PDF Datei konnte nicht erstellt werden", detailed_text= rsp)


    def get_dict_titlepage(self, dict_titlepage, chosen_program):
        titlepage_settings = ["logo", "logo_path", "titel", "datum", "datum_combobox", "klasse", "name", "note", "unterschrift", "individual", "hide_all"]
        for all in titlepage_settings:
            if all == "logo_path":
                if self.cb_titlepage_logo.isChecked() and dict_titlepage[all] == False:
                    warning_message = "Bitte geben Sie den Dateipfad eines Logos an oder wählen Sie das Logo auf der Titelseite ab."
                elif self.cb_titlepage_individual.isChecked():
                    if chosen_program == "lama":
                        individual_titlepage = lama_individual_titlepage
                    elif chosen_program == "cria":
                        individual_titlepage = cria_individual_titlepage


                    with open(individual_titlepage, "r", encoding="utf8") as f:
                        string_titlepage = load(f)
                    
                    if string_titlepage.find("[[LOGO]]") == -1:
                        continue
                    warning_message = "Bitte geben Sie den Dateipfad eines Logos an oder entfernen Sie das Logo aus Ihrem Titelblatt."
                else:
                    continue

                critical_window(warning_message, titel="Kein Logo ausgewählt")
                return False

            
            elif all == "datum_combobox":
                dict_titlepage[all] = self.combobox_titlepage_datum.currentIndex()
                continue


            checkbox = eval("self.cb_titlepage_{}".format(all))
            if checkbox.isChecked():
                dict_titlepage[all] = True
            else:
                dict_titlepage[all] = False
            # except AttributeError:
            #     dict_titlepage[all] = False

        return dict_titlepage
    
    def save_titlepage(self, dict_titlepage, chosen_program):
        dict_titlepage = self.get_dict_titlepage(dict_titlepage, chosen_program)
        if dict_titlepage != False:
            self.Dialog.accept()
        return dict_titlepage

    def set_default_titlepage(self, dict_titlepage):
        dict_titlepage = {
            "logo": False,
            "logo_path": False,
            "titel": True,
            "datum": True,
            "datum_combobox": 0,
            "klasse": True,
            "name": True,
            "note": False,
            "unterschrift": False,
            "individual": False,
            "hide_all": False,
        }
        for all in dict_titlepage.keys():
            if all == "logo_path":
                continue
            elif all == "datum_combobox":
                try:
                    self.combobox_titlepage_datum.setCurrentIndex(dict_titlepage[all])
                except KeyError:
                    self.combobox_titlepage_datum.setCurrentIndex(0)
            else:                
                checkbox = eval("self.cb_titlepage_{}".format(all))
                checkbox.setChecked(dict_titlepage[all])

        return dict_titlepage


class Ui_Dialog_individual_titlepage(object):
    def setupUi(self, Dialog, text):
        Dialog.setWindowTitle("Titelblatt bearbeiten")
        Dialog.setWindowIcon(QIcon(logo_path)) 
        Dialog.resize(300,50)

        verticalLayout = create_new_verticallayout(Dialog)

        widget_titel = QtWidgets.QWidget(Dialog)
        verticalLayout.addWidget(widget_titel)
        self.horizontallayout_titel = create_new_horizontallayout(widget_titel)
        self.horizontallayout_titel.setContentsMargins(0,0,0,0)

        self.plainTextEdit_instructions = QtWidgets.QPlainTextEdit()
        self.plainTextEdit_instructions.setPlainText(text)

        verticalLayout.addWidget(self.plainTextEdit_instructions)

        buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        verticalLayout.addWidget(buttonBox)

        buttonCancel = buttonBox.button(QtWidgets.QDialogButtonBox.Cancel)
        buttonCancel.setText("Abbrechen")
        
        
        buttonBox.rejected.connect(Dialog.reject)
        buttonBox.accepted.connect(Dialog.accept)


class Ui_Dialog_ausgleichspunkte(object):
    @report_exceptions
    def setupUi(
        self,
        Dialog,
        aufgabe,
        typ,
        content,
        aufgabenstellung_split_text,
        list_sage_hide_show_items_chosen,
        sage_individual_change,
        language,
        display_mode,
        developer_mode_active,
        chosen_program,
    ):

        self.sage_individual_change = sage_individual_change
        self.language = language
        
        self.typ = typ
        self.developer_mode_active = developer_mode_active
        if typ==2:
            self.aufgabenstellung_split_text = aufgabenstellung_split_text
            try:
                self.hide_show_items_split_text = prepare_content_for_hide_show_items(
                    aufgabenstellung_split_text
                )
            except TypeError:
                information_window("Aufgrund einer fehlerhaften Formatierung, kann diese Typ2-Aufgabe nur indivduell bearbeitet werden.")
                self.hide_show_items_split_text = None
            # self.list_sage_ausgleichspunkte_chosen = list_sage_ausgleichspunkte_chosen
            self.list_sage_hide_show_items_chosen = list_sage_hide_show_items_chosen
            # print(sage_individual_change)
            # self.dict_widget_variables_ausgleichspunkte = {}
            self.dict_widget_variables_hide_show_items = {}
        else: 
            self.hide_show_items_split_text = None

        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        self.Dialog.setWindowTitle("Aufgabe bearbeiten")
        self.Dialog.resize(600, 400)
        self.Dialog.setWindowIcon(QIcon(logo_path))

        self.gridlayout_titlepage = create_new_gridlayout(Dialog)
        # self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        # self.gridLayout_2.setObjectName("gridLayout_2")

        self.widgetHeader = QtWidgets.QWidget(Dialog)
        self.widgetHeader.setObjectName(_fromUtf8("widgetHeader"))
        self.horizontalLayoutHeader = create_new_horizontallayout(self.widgetHeader)
        self.horizontalLayoutHeader.setContentsMargins(0,0,0,0)
        self.gridlayout_titlepage.addWidget(self.widgetHeader, 0,0,1,6)

        self.combobox_edit = create_new_combobox(self.widgetHeader)
        self.combobox_edit.setSizePolicy(SizePolicy_fixed)

        self.horizontalLayoutHeader.addWidget(self.combobox_edit)
        # self.gridlayout_titlepage.setColumnStretch(1,0)
        # self.gridlayout_titlepage.addItem(QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum),0,3,1,1)
        if typ == 2 and self.hide_show_items_split_text != None:
            # self.combobox_edit.addItem("Ausgleichspunkte anpassen")
            self.combobox_edit.addItem("Aufgabenstellungen ein-/ausblenden")
        self.combobox_edit.addItem("Individuell bearbeiten")
        if typ !=2 or self.hide_show_items_split_text == None:
            self.combobox_edit.setEnabled(False)
            # self.combobox_edit.setStyleSheet("color: black")

        if typ ==2 and self.hide_show_items_split_text != None:
            # self.combobox_edit.setCurrentIndex(0)
            self.scrollArea = QtWidgets.QScrollArea(Dialog)
            self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
            self.scrollArea.setWidgetResizable(True)
            self.scrollArea.setObjectName("scrollArea")
            self.scrollAreaWidgetContents = QtWidgets.QWidget()
            self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 600, 500))
            self.scrollArea.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")


            self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
            self.gridLayout.setObjectName("gridLayout")
            self.label_einleitung = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.label_einleitung.setWordWrap(True)
            self.label_einleitung.setObjectName("label_einleitung")
            self.label_einleitung.setText(
                "[...] EINFÜHRUNGSTEXT [...] \n\nAufgabenstellung:\n"
            )
            self.gridLayout.addWidget(self.label_einleitung, 0, 1, 1, 3, Qt.AlignTop)

            self.label_solution = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            self.label_solution.setWordWrap(True)
            self.label_solution.setObjectName("label_solution")
            self.label_solution.setText("\nLösungserwartung:\n[...]")

            row = self.build_checkboxes_for_content()

            self.scrollArea.setWidget(self.scrollAreaWidgetContents)
            self.gridlayout_titlepage.addWidget(self.scrollArea, 2,0,1,6)

        # self.scrollArea.hide()

        self.plainTextEdit_content = QtWidgets.QPlainTextEdit()
        if display_mode == 0:
            background_color = StyleSheet_subwindow_ausgleichspunkte
        else:
            background_color = StyleSheet_subwindow_ausgleichspunkte_dark_mode
        self.plainTextEdit_content.setStyleSheet(background_color)
        self.plainTextEdit_content.setObjectName(_fromUtf8("plainTextEdit_content"))
        # self.plainTextEdit_content.textChanged.connect(self.plainTextEdit_content_changed)
        self.plainTextEdit_content.setUndoRedoEnabled(False)

        if language == "DE":
            key = 0
        elif language == "EN":
            key = 1

        if self.sage_individual_change[key] != None:
            # print(self.sage_individual_change)
            self.plainTextEdit_content.insertPlainText(self.sage_individual_change[key])
            self.inital_content = self.sage_individual_change[key]
        else:
            self.plainTextEdit_content.insertPlainText(content)
            self.inital_content = content
        self.plainTextEdit_content.moveCursor(QTextCursor.Start)
        self.plainTextEdit_content.ensureCursorVisible()
        # self.plainTextEdit_content_changed.verticalScrollBar().setValue(0)
        self.gridlayout_titlepage.addWidget(self.plainTextEdit_content, 1,0,1,6)
        self.plainTextEdit_content.setUndoRedoEnabled(True)
        # if typ == 2:
        #     self.plainTextEdit_content.hide()
        #     self.combobox_edit.currentIndexChanged.connect(lambda: self.combobox_edit_changed())


        self.button_preview = create_new_button(Dialog, "Vorschau", self.button_preview_pressed)
        self.button_preview.setIcon(QIcon(get_icon_path('eye.svg')))
        self.button_preview.setSizePolicy(SizePolicy_maximum)
        self.button_preview.setShortcut("Ctrl+Return")
        self.button_preview.setToolTip("Strg+Enter")
        self.gridlayout_titlepage.addWidget(self.button_preview, 3, 0, 1,1)
        # if typ ==2:
        #     self.button_preview.hide()

        self.button_restore_default = create_new_button(Dialog, "Original wiederherstellen", partial(self.button_restore_default_pressed,aufgabe, chosen_program))
        self.button_restore_default.setIcon(QIcon(get_icon_path('archive.svg')))
        self.button_restore_default.setSizePolicy(SizePolicy_maximum)
        self.gridlayout_titlepage.addWidget(self.button_restore_default, 3,1,1,1)
        # if typ ==2:
        #     self.button_restore_default.hide()

        self.button_save_edit = create_new_button(Dialog, "Änderung für alle übernehmen", partial(self.button_save_edit_pressed_individual_changes, aufgabe, chosen_program, language))
        self.button_save_edit.setIcon(QIcon(get_icon_path('save.svg')))
        self.button_save_edit.setSizePolicy(SizePolicy_fixed)
        self.gridlayout_titlepage.addWidget(self.button_save_edit, 3,2,1,1)

        if developer_mode_active == False or (typ ==2 and self.hide_show_items_split_text != None):
            self.button_save_edit.hide()


        # ### Variationsbutton ausblenden, da derzeit nicht funktionsfähig
        self.button_save = create_new_button(Dialog, "Als Variation speichern", self.button_save_pressed)
        self.button_save.setSizePolicy(SizePolicy_maximum)
        self.gridlayout_titlepage.addWidget(self.button_save, 3, 2, 1,1)
        ### Variationsbutton ausblenden, da derzeit nicht funktionsfähig
        self.button_save.hide()
        if typ ==2 and self.hide_show_items_split_text != None:
            self.plainTextEdit_content.hide()
            self.combobox_edit.currentIndexChanged.connect(lambda: self.combobox_edit_changed())
            self.button_preview.hide()
            self.button_restore_default.hide()
            self.button_save.hide()
        ########################################################################


        self.button_OK = create_new_button(Dialog, "OK", partial(self.pushButton_OK_pressed, aufgabe, chosen_program))
        self.button_OK.setSizePolicy(SizePolicy_maximum)
        self.gridlayout_titlepage.addWidget(self.button_OK, 3,4,1,1)

        self.button_cancel = create_new_button(Dialog, "Abbrechen", Dialog.reject)
        self.button_cancel.setSizePolicy(SizePolicy_maximum)
        self.gridlayout_titlepage.addWidget(self.button_cancel, 3,5,1,1)




        self.horizontalLayoutHeader.addStretch()
        # path_undo = os.path.join(path_programm, "_database", "_config", "icon", "undo-arrow.png")
        # self.button_undo = create_standard_button(Dialog, "", still_to_define,QIcon(path_undo))
        self.button_undo = create_new_button(Dialog, "", self.button_undo_pressed)
        self.button_undo.setIcon(QIcon(get_icon_path('rotate-ccw.svg')))
        self.button_undo.setSizePolicy(SizePolicy_maximum)
        self.button_undo.setToolTip("Rückgängig (Strg+Z)")
        self.button_undo.setShortcut("Ctrl+Z")
        self.horizontalLayoutHeader.addWidget(self.button_undo)
        # self.gridlayout_titlepage.addWidget(self.button_undo, 0,4,1,1, Qt.AlignLeft)



        # path_redo = os.path.join(path_programm, "_database", "_config", "icon", "redo-arrow.png")
        # self.button_undo = create_standard_button(Dialog, "", still_to_define,QIcon(path_undo))
        self.button_redo = create_new_button(Dialog, "", self.button_redo_pressed)
        self.button_redo.setIcon(QIcon(get_icon_path('rotate-cw.svg')))
        self.button_redo.setSizePolicy(SizePolicy_maximum)
        self.button_redo.setToolTip("Wiederherstellen (Strg+Y)")
        self.button_redo.setShortcut("Ctrl+Y")
        self.horizontalLayoutHeader.addWidget(self.button_redo)
        # self.button_redo = create_standard_button(Dialog, "", still_to_define,QtWidgets.QStyle.SP_ArrowForward)
        # self.gridlayout_titlepage.addWidget(self.button_redo, 0,4,1,1, Qt.AlignRight)

       

        
        # path_zoom_in = os.path.join(path_programm, "_database", "_config", "icon", "zoom-in.png")
        self.button_zoom_in = create_new_button(Dialog, "", self.plainTextEdit_content.zoomIn)
        self.button_zoom_in.setIcon(QIcon(get_icon_path('zoom-in.svg')))
        self.button_zoom_in.setSizePolicy(SizePolicy_maximum)
        # self.gridlayout_titlepage.addWidget(self.button_zoom_in,0,5,1,1, Qt.AlignLeft)
        self.button_zoom_in.setShortcut("Ctrl++")
        self.horizontalLayoutHeader.addWidget(self.button_zoom_in)

        # path_zoom_out = os.path.join(path_programm, "_database", "_config", "icon", "zoom-out.png")
        self.button_zoom_out = create_new_button(Dialog, "", self.plainTextEdit_content.zoomOut)
        self.button_zoom_out.setIcon(QIcon(get_icon_path('zoom-out.svg')))
        self.button_zoom_out.setSizePolicy(SizePolicy_maximum)
        # self.gridlayout_titlepage.addWidget(self.button_zoom_out,0,5,1,1, Qt.AlignRight)
        self.button_zoom_out.setShortcut("Ctrl+-")
        self.horizontalLayoutHeader.addWidget(self.button_zoom_out)

        if typ==2 and self.hide_show_items_split_text != None:        
            self.button_undo.hide()
            self.button_redo.hide()
            self.button_zoom_in.hide()
            self.button_zoom_out.hide()

        self.change_detected_0 = False

        QMetaObject.connectSlotsByName(self.Dialog)

        # if self.sage_individual_change[key] != None:
        #     self.combobox_edit.setCurrentIndex(1)
        # if typ == 2:
        #     if not is_empty(list_sage_hide_show_items_chosen):
        #         self.combobox_edit.setCurrentIndex(0)
        #     elif sage_individual_change != None:
        #         self.combobox_edit.setCurrentIndex(1)

    # def change_detected_warning(self):
    #     response = question_window("Es wurden bereits nicht gespeicherte Änderungen an der Aufgabe vorgenommen.",
    #     "Sind Sie sicher, dass Sie diese Änderungen verwerfen wollen?","Änderung der Aufgabe")
    #     return response

    def check_for_change(self):
        change_to_index = self.combobox_edit.currentIndex()

        if change_to_index == 1: #change to 1 -> control index 0 
            return self.change_detected_0, 0
        
        elif change_to_index == 0:
            if self.inital_content != self.plainTextEdit_content.toPlainText():
                return True, 1
            else:
                return False, 1

        #####
            
        # for index in [0,1]:
        #     change_detected = eval("self.change_detected_{}".format(index))
        #     if change_detected == True:  
        #         return index

                # rsp = self.change_detected_warning()
                # if rsp == False:
                #     self.combobox_edit.setCurrentIndex(index)
                #     return rsp
                # else:
                #     change_detected = False  
                #     return rsp          
        # _list = [0,1,2]
        # _list.remove(index)

    @report_exceptions
    def combobox_edit_changed(self):
        changes_detected, index = self.check_for_change()

        if changes_detected == True:
            rsp = question_window("Es wurden bereits nicht gespeicherte Änderungen an der Aufgabe vorgenommen.",
                    "Sind Sie sicher, dass Sie diese Änderungen verwerfen wollen?","Änderung der Aufgabe")
            if rsp == False:
                self.combobox_edit.setCurrentIndex(index)
                return
            else:
                self.change_detected_0=False
                if index == 1:
                    self.plainTextEdit_content.clear()
                    self.plainTextEdit_content.insertPlainText(self.inital_content)
                self.inital_content = self.plainTextEdit_content.toPlainText()  
                

        for i in reversed(range(1, self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)
        if self.combobox_edit.currentIndex() == 0:

            self.gridlayout_titlepage.addWidget(self.combobox_edit, 0,0,1,5)
            self.button_undo.hide()
            self.button_redo.hide()
            self.scrollArea.show()
            self.plainTextEdit_content.hide()
            self.build_checkboxes_for_content()
            self.button_save_edit.hide()
            self.button_save.hide()
            self.button_preview.hide()
            self.button_restore_default.hide()
            self.button_zoom_in.hide()
            self.button_zoom_out.hide()

        elif self.combobox_edit.currentIndex() == 1:
            self.gridlayout_titlepage.addWidget(self.combobox_edit, 0,0,1,4)
            # self.gridlayout_titlepage.update()
            self.button_undo.show()
            # self.button_undo.setEnabled(False)
            self.button_redo.show()
            self.scrollArea.hide()
            self.plainTextEdit_content.show()
            # self.build_editable_content()
            # self.button_save.show()
            self.button_preview.show()
            self.button_restore_default.show()
            self.button_zoom_in.show()
            self.button_zoom_out.show()
            if self.developer_mode_active == True:
                self.button_save_edit.show()    

    # def plainTextEdit_content_changed(self):
    #     self.change_detected_2 = True

    def button_restore_default_pressed(self, aufgabe, chosen_program):
        rsp = question_window("Sind Sie sicher, dass sie die originale Aufgabe wiederherstellen wollen?")
        if rsp == True:
            self.plainTextEdit_content.clear()
            typ = get_aufgabentyp(chosen_program, aufgabe)
            aufgabe_total = get_aufgabe_total(aufgabe, typ)
            if self.language == "DE":
                key = 'content'
            elif self.language == "EN":
                key = 'content_translation'
            
            self.plainTextEdit_content.insertPlainText(aufgabe_total[key])
            self.inital_content = aufgabe_total[key]
            information_window("Die originale Aufgabe wurde wiederhergestellt.",titel="Original wiederhergestellt")

    def button_save_edit_pressed_individual_changes(self, aufgabe, chosen_program, language):
        rsp = question_window("Sind Sie sicher, dass Sie originale Aufgabe mit dem geänderten Inhalt überschreiben möchten?")
        if rsp == False:
            return
        
        QtWidgets.QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        
        internet_on = check_internet_connection()
        if internet_on == False:
            QtWidgets.QApplication.restoreOverrideCursor()
            critical_window(
                "Stellen Sie sicher, dass eine Verbindung zum Internet besteht und versuchen Sie es erneut.",
                titel="Keine Internetverbindung",
            )  
            return
        
        rsp = check_branches()
        if rsp == False:
            try:
                worker_update_database()
            except Exception:
                critical_window(
                    "Beim Synchronisieren ist ein Fehler aufgetreten. Bitte stellen Sie sicher, dass eine Internetverbindung beseteht und versuchen Sie es erneut."
                )
                QtWidgets.QApplication.restoreOverrideCursor()
                return

        typ = get_aufgabentyp(chosen_program, aufgabe)
        new_content = self.plainTextEdit_content.toPlainText()

        if language == 'DE':
            entry_key = 'content'
        elif language == 'EN':
            entry_key = 'content_translation'

        update_data(aufgabe, typ, entry_key, new_content)

        QtWidgets.QApplication.restoreOverrideCursor()

        chosen_ddb = ["_database.json"]    
        response = action_push_database(True, 
        chosen_ddb,
        message="Inhalt von {} geändert".format(aufgabe),
        worker_text="Geänderter Inhalt von {} wird gespeichert".format(aufgabe)
        )

        if response == False:
            return
        else:
            information_window("Die Änderung wurde erfolgreich in der Datenbank gespeichert!")

        if typ == 2:
            self.change_detected_2 = False

    def button_undo_pressed(self):
        self.plainTextEdit_content.undo()

        if is_empty(self.plainTextEdit_content.toPlainText()) == True:
            self.plainTextEdit_content.redo()
    

    
    def button_redo_pressed(self):
        self.plainTextEdit_content.redo()


    def button_preview_pressed(self):
        file_path = os.path.join(
            path_localappdata_lama, "Teildokument", "preview.tex"
            )
        
        rsp = create_tex(file_path, self.plainTextEdit_content.toPlainText())

        if rsp == True:
            create_pdf("preview")
        else:
            critical_window("Die PDF Datei konnte nicht erstellt werden", detailed_text= rsp)

        # if typ == 2:
        #     begin_beispiel = "\\begin{langesbeispiel}\item[0]"
        #     end_beispiel = "\\end{langesbeispiel}"
        # else:
        #     begin_beispiel = "\\begin{beispiel}{0}"
        #     end_beispiel = "\\end{beispiel}"
        # filename_preview = os.path.join(
        #         path_programm, "Teildokument", "preview.tex"
        #     )
        # with open(filename_preview, "w+" ,encoding="utf8") as file:
        #     file.write(
        #         "\documentclass[a4paper,12pt]{{report}}\n\n"
        #         "\\usepackage{{geometry}}\n"
        #         "\geometry{{a4paper,left=18mm,right=18mm, top=2cm, bottom=2cm}}\n\n"
        #         "\\usepackage{{lmodern}}\n"
        #         "\\usepackage[T1]{{fontenc}}\n"
        #         "\\usepackage[utf8]{{inputenc}}\n"
        #         "\\usepackage[ngerman]{{babel}}\n"
        #         "\\usepackage[solution_on]{{srdp-mathematik}}% solution_on/off, random=0,1,2,...\n\n"
        #         # "\setcounter{{Zufall}}{{{3}}}\n\n\n"
        #         "\pagestyle{{empty}} %PAGESTYLE: empty, plain\n"
        #         "\onehalfspacing %Zeilenabstand\n"
        #         "\setcounter{{secnumdepth}}{{-1}} % keine Nummerierung der Ueberschriften\n\n\n\n"
        #         "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
        #         "%%%%%%%%%%%%%%%%%% DOKUMENT - ANFANG %%%%%%%%%%%%%%%%%%\n"
        #         "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n"
        #         "\\begin{{document}}\n"
        #         "{0}"
        #         "{1}"
        #         "{2}"
        #         "\n\end{{document}}".format(
        #             begin_beispiel,
        #             self.plainTextEdit_content.toPlainText(),
        #             end_beispiel,
        #             )
                    
        #     )

        # create_pdf("preview",0,0)
        

    def button_save_pressed(self):
        # self.plainTextEdit_content.undo     
        print('save')


    # def build_editable_content(self):
    #     self.plainTextEdit_content.insertPlainText(self.content)

        # for line in conten:
        #     self.plainTextEdit_content.appendPlainText(line)

        # self.label_einleitung.hide()
        # self.label_solution.hide()



    def build_checkboxes_for_content(self):
        row = 1
        # if self.combobox_edit.currentIndex() == 0:
        #     for index, linetext in enumerate(self.aufgabenstellung_split_text):
        #         if (
        #             "GRAFIK" in linetext
        #             or is_empty(linetext.replace("ITEM", "").strip()) == True
        #         ) and self.combobox_edit.currentIndex() == 0:  #
        #             checkbox = None
        #         else:
        #             checkbox, checkbox_label = self.create_checkbox_ausgleich(
        #                 linetext, row, index
        #             )

        #         row += 1
                    
        if self.combobox_edit.currentIndex() == 0:
            for index, linetext in enumerate(self.hide_show_items_split_text):
                if is_empty(linetext.replace("ITEM", "").strip()) == False:


                    self.create_checkbox_ausgleich(
                        linetext, row, index
                    )
                # if checkbox != None:
                #     checkbox.clicked.connect(
                #         partial(self.checkbox_clicked, checkbox, checkbox_label)
                #     )
                    # self.dict_widget_variables_hide_show_items[linetext] = checkbox
                    row += 1

        self.gridLayout.addWidget(self.label_solution, row, 1, 1, 3, Qt.AlignTop)
        row += 1
        self.gridLayout.setRowStretch(row, 1)

    # def checkbox_changed(self):
    #     if self.combobox_edit.currentIndex()==0:
    #         self.change_detected_0 = True
        # elif self.combobox_edit.currentIndex() == 1:
        #     self.change_detected_1 = True
            # self.checkbox_clicked(checkbox, checkbox_label)


    def checkbox_clicked(self, checkbox, checkbox_label):
        self.change_detected_0 = True
        if checkbox.isChecked() == False:
            checkbox_label.setStyleSheet("color: gray")
        else:
            checkbox_label.setStyleSheet("color: black")
        # self.checkbox_changed()
        # try: 
        #     with open(lama_settings_file, "r", encoding="utf8") as f:
        #         self.lama_settings = load(f)
        # except FileNotFoundError:
        #     self.lama_settings = {}
        
        # try:
        #     display_settings = self.lama_settings["display"]
        #     if  display_settings == 1:
        #         stylesheet = StyleSheet_ausgleichspunkte_dark_mode
        #     else:
        #         stylesheet = StyleSheet_ausgleichspunkte
        # except KeyError:
        #     stylesheet = StyleSheet_ausgleichspunkte

        # if checkbox.isChecked() == True:
        #     checkbox_label.setStyleSheet(stylesheet)
        # if self.combobox_edit.currentIndex() == 0:


    def create_checkbox_ausgleich(self, linetext, row, index):
        checkbox_label = create_new_label(self.scrollAreaWidgetContents, "",wordwrap=True, clickable=True)

        checkbox = create_new_checkbox(self.scrollAreaWidgetContents, "")
        checkbox.setStyleSheet("QCheckBox::indicator { width: 20px; height: 20px; padding-right: 10px}")
        checkbox.setSizePolicy(SizePolicy_fixed_width)



        # if self.combobox_edit.currentIndex() == 0:
        #     if index in self.list_sage_ausgleichspunkte_chosen:
        #         checkbox.setChecked(True)
        # if self.combobox_edit.currentIndex() == 1:
        #     if index in self.list_sage_hide_show_items_chosen:
        #         checkbox.setChecked(False)
        #         checkbox_label.setStyleSheet("color: gray")
        #     else:
        #         checkbox.setChecked(True)

        
        # if self.combobox_edit.currentIndex() == 0:
        #     self.dict_widget_variables_ausgleichspunkte[linetext] = checkbox
        #     if index in self.list_sage_ausgleichspunkte_chosen:
        #         checkbox.setChecked(True)

        if self.combobox_edit.currentIndex() == 0:
            self.dict_widget_variables_hide_show_items[linetext] = checkbox
            if index in self.list_sage_hide_show_items_chosen:
                checkbox.setChecked(False)
                checkbox_label.setStyleSheet("color: gray")
            else:
                checkbox.setChecked(True)


        # if "\\fbox{A}" in linetext:
        #     linetext = linetext.replace("\\fbox{A}", "")
        # if "\\ASubitem" in linetext:
        #     linetext = linetext.replace("\\ASubitem", "")

        linetext = (
            linetext.replace("ITEM", "")
            .replace("SUBitem", "")
            .replace("{", "")
            .replace("}", "")
            .replace("\\fbox{A}", "")
            .replace("\\ASubitem", "")
            .strip()
        )
        # if self.combobox_edit.currentIndex() == 1:
        #     linetext = ascii_lowercase[index] + ")\n" + linetext

        checkbox_label.setText(linetext)

        self.gridLayout.addWidget(checkbox, row, 0, 1, 1, Qt.AlignTop)
        self.gridLayout.addWidget(checkbox_label, row, 1, 1, 2, Qt.AlignTop)

        checkbox.stateChanged.connect(partial(self.checkbox_clicked, checkbox, checkbox_label))
        checkbox_label.clicked.connect(
            partial(self.checkbox_label_clicked, checkbox, checkbox_label)
        )
        
        return checkbox, checkbox_label

    def checkbox_label_clicked(self, checkbox, checkbox_label):
        if checkbox.isChecked() == True:
            checkbox.setChecked(False)
        else:
            checkbox.setChecked(True)
        if self.combobox_edit.currentIndex() == 0:
            self.checkbox_clicked(checkbox, checkbox_label)

    def check_if_saved_changes_exist(self):

        # if not is_empty(self.list_sage_ausgleichspunkte_chosen):
        #     for index in self.list_sage_ausgleichspunkte_chosen:
        #         if "\\fbox{A}" in self.aufgabenstellung_split_text[index] or "\\ASubitem" in self.aufgabenstellung_split_text[index]:
        #             continue
        #         else:
        #             return True
        #     # return False
        # if is_empty(self.list_sage_ausgleichspunkte_chosen):
        #     for all in self.aufgabenstellung_split_text:
        #         if "\\fbox{A}" in all or "\\ASubitem" in all:
        #             return True
        
        if not is_empty(self.list_sage_hide_show_items_chosen) and self.combobox_edit.currentIndex()==1:
            return True
        
        if self.language == "DE":
            index =0
        elif self.language == "EN":
            index = 1
        if self.sage_individual_change[index] != None:
            return True

        return False      
    

    def pushButton_OK_pressed(self, aufgabe, chosen_program):
        # self.combobox_edit.currentIndex()
        if self.typ == 2:
            change_detected = self.check_if_saved_changes_exist()
            
            if change_detected == True:
                response = question_window("Es wurden bereits Änderungen an der Aufgabe gespeichert.",
                "Sind Sie sicher, dass Sie diese Änderungen überschreiben möchten?","Änderung der Aufgabe")
                if response == False:
                    return

        # self.list_sage_ausgleichspunkte_chosen = []
        self.list_sage_hide_show_items_chosen = []   
        # self.sage_individual_change = []


        typ = get_aufgabentyp(chosen_program, aufgabe)
        aufgabe_total = get_aufgabe_total(aufgabe, typ)

        if self.combobox_edit.currentIndex() == 1 or self.hide_show_items_split_text==None:
            if self.language == "DE":
                key = 'content'
                index = 0
            elif self.language == "EN":
                key = 'content_translation'
                index = 1

            if aufgabe_total[key] != self.plainTextEdit_content.toPlainText():
                self.sage_individual_change[index] = self.plainTextEdit_content.toPlainText()
            else:
                self.sage_individual_change[index] = None

        # elif self.combobox_edit.currentIndex() == 0:
        #     for index, linetext in enumerate(self.aufgabenstellung_split_text):  #list(self.dict_widget_variables_ausgleichspunkte.keys())
        #         try:
        #             if (
        #                 self.dict_widget_variables_ausgleichspunkte[linetext].isChecked()
        #                 == True
        #             ):
        #                 self.list_sage_ausgleichspunkte_chosen.append(index)
        #         except KeyError:
        #             pass
                #     self.list_sage_ausgleichspunkte_chosen.append(
                #         linetext.replace("\\fbox{A}", "").replace("\\ASubitem", "")
                #     )

        elif self.combobox_edit.currentIndex() == 0:
            for index, linetext in enumerate(self.hide_show_items_split_text): #list(self.dict_widget_variables_hide_show_items.keys())
                try:
                    if (
                        self.dict_widget_variables_hide_show_items[linetext].isChecked()
                        == False
                    ):
                        self.list_sage_hide_show_items_chosen.append(index)
                except KeyError:
                    pass

            # print(self.list_sage_hide_show_items_chosen)               
            if self.language == "DE":
                index = 0
            elif self.language == "EN":
                index = 1
            
            self.sage_individual_change[index] = None
            
                    # self.list_sage_hide_show_items_chosen.append(
                    #     linetext.replace("\\fbox{A}", "")
                    # )

        self.Dialog.reject()


class Ui_Dialog_erstellen(QtWidgets.QDialog):
    def setupUi(
        self,
        Dialog,
        Ui_MainWindow,
        dict_list_input_examples,
        dict_titlepage,
        saved_file_path,
        pruefungstyp,
    ):

        self.dict_list_input_examples = dict_list_input_examples
        self.dict_titlepage = dict_titlepage
        self.data_gesamt = Ui_MainWindow.dict_all_infos_for_file["data_gesamt"]

        self.pkt_gesamt = Ui_MainWindow.get_punkteverteilung()[0]
        self.pkt_typ1 = Ui_MainWindow.get_punkteverteilung()[1]
        self.pkt_typ2 = Ui_MainWindow.get_punkteverteilung()[2]
        self.num_gesamt = len(
            Ui_MainWindow.dict_all_infos_for_file["list_alle_aufgaben"]
        )
        self.num_typ1 = Ui_MainWindow.get_aufgabenverteilung()[0]
        self.num_typ2 = Ui_MainWindow.get_aufgabenverteilung()[1]

        # self.pkt_ausgleich = Ui_MainWindow.get_number_ausgleichspunkte_gesamt()

        # self.dict_list_input_examples["data_gesamt"]

        self.saved_file_path = saved_file_path
        self.Dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(468, 208)
        Dialog.setWindowIcon(QIcon(logo_path))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_sw_save = QtWidgets.QPushButton(Dialog)
        self.pushButton_sw_save.setObjectName("pushButton_sw_save")
        self.pushButton_sw_save.clicked.connect(self.pushButton_sw_save_pressed)
        self.gridLayout.addWidget(self.pushButton_sw_save, 7, 3, 1, 1)
        self.pushButton_sw_back = QtWidgets.QPushButton(Dialog)
        self.pushButton_sw_back.setObjectName("pushButton_sw_back")
        self.pushButton_sw_back.clicked.connect(self.pushButton_sw_back_pressed)
        self.gridLayout.addWidget(self.pushButton_sw_back, 6, 3, 1, 1)


        self.cb_show_pagenumber = create_new_checkbox(Dialog, "Seitennummerierung anzeigen", True)
        self.gridLayout.addWidget(self.cb_show_pagenumber, 4,3,1,1)

        self.cb_single_file = create_new_checkbox(Dialog, "Gesamtausgabe in einer Datei")
        self.gridLayout.addWidget(self.cb_single_file, 5,3,1,1)
        if pruefungstyp != "Grundkompetenzcheck":
            self.cb_single_file.hide()
        self.cb_single_file.toggled.connect(self.cb_create_pdf_checked)
        self.groupBox_sw_data = QtWidgets.QGroupBox(Dialog)
        self.groupBox_sw_data.setObjectName("groupBox_sw_data")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_sw_data)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_sw_num_ges = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_num_ges.setObjectName("label_sw_num_ges")
        self.gridLayout_2.addWidget(self.label_sw_num_ges, 6, 0, 1, 1)
        self.label_sw_num_1 = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_num_1.setLayoutDirection(Qt.LeftToRight)
        self.label_sw_num_1.setObjectName("label_sw_num_1")
        self.gridLayout_2.addWidget(
            self.label_sw_num_1, 3, 0, 1, 1, Qt.AlignLeft
        )
        self.label_sw_num_2 = QtWidgets.QLabel(self.groupBox_sw_data)
        self.label_sw_num_2.setObjectName("label_sw_num_2")
        self.gridLayout_2.addWidget(
            self.label_sw_num_2, 4, 0, 1, 1, Qt.AlignLeft
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
        self.gridLayout.addWidget(self.groupBox_sw_data, 1, 0, 6, 3)
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
        self.gridLayout.addWidget(self.cb_create_tex, 7, 0, 1, 1)
        self.cb_create_pdf = QtWidgets.QCheckBox(Dialog)
        self.cb_create_pdf.setObjectName(_fromUtf8("cb_create_pdf"))
        self.cb_create_pdf.setText(".pdf")
        self.cb_create_pdf.setChecked(True)
        self.cb_create_pdf.toggled.connect(self.cb_create_pdf_checked)
        self.gridLayout.addWidget(self.cb_create_pdf, 7, 1, 1, 1)
        self.cb_create_lama = QtWidgets.QCheckBox(Dialog)
        self.cb_create_lama.setObjectName(_fromUtf8("cb_create_lama"))
        self.cb_create_lama.setText("Autosave (.lama)")
        self.cb_create_lama.setChecked(True)
        self.gridLayout.addWidget(self.cb_create_lama, 7, 2, 1, 1)

        self.retranslateUi(Dialog)

        if Ui_MainWindow.chosen_program == "cria":
            self.label_sw_num_1.hide()
            self.label_sw_num_1_int.hide()
            self.label_sw_pkt_1.hide()
            self.label_sw_pkt_1_int.hide()
            self.label_sw_num_2.hide()
            self.label_sw_num_2_int.hide()
            self.label_sw_pkt_2.hide()
            self.label_sw_pkt_2_int.hide()

        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        datum = (
            str(self.data_gesamt["Datum"][2])
            + "."
            + str(self.data_gesamt["Datum"][1])
            + "."
            + str(self.data_gesamt["Datum"][0])
        )
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Erstellen", "Erstellen"))
        self.radioButton_sw_ns.setText(_translate("Dialog", "Notenschlüssel"))
        self.pushButton_sw_save.setText(_translate("Dialog", "Speichern"))
        self.pushButton_sw_back.setText(_translate("Dialog", "Abbrechen"))
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
        self.label_sw_num_ges_int.setText(str(self.num_gesamt))
        self.label_sw_num_2_int.setText(str(self.num_typ2))
        self.label_sw_num_1_int.setText(str(self.num_typ1))
        self.label_sw_pkt_1_int.setText(str(self.pkt_typ1))
        self.label_sw_pkt_2_int.setText(str(self.pkt_typ2))
        self.label_sw_pkt_ges_int.setText(str(self.pkt_gesamt))
        self.label_sw_klasse.setText(
            _translate("Dialog", "Klasse: %s" % self.data_gesamt["Klasse"])
        )
        self.groupBox_sw_gruppen.setTitle(_translate("Dialog", "Anzahl der Gruppen"))
        self.radioButton_sw_br.setText(_translate("Dialog", "Beurteilungsraster"))

    def cb_create_pdf_checked(self):
        if (self.cb_create_pdf.isChecked() == True or self.cb_single_file.isChecked() == True) and self.data_gesamt["Pruefungstyp"] != "Übungsblatt":
            self.groupBox_sw_gruppen.setEnabled(True)
        else:
            self.groupBox_sw_gruppen.setEnabled(False)

    def pushButton_sw_back_pressed(self):
        self.Dialog.reject()

    def pushButton_sw_save_pressed(self):
        if self.cb_create_pdf.isChecked():
            self.pdf = True
        else:
            self.pdf = False

        if self.cb_create_lama.isChecked():
            self.lama = True
        else:
            self.lama = False

        if self.cb_single_file.isChecked():
            self.single_file_index = 0
        else:
            self.single_file_index = None
        
        if self.cb_show_pagenumber.isChecked():
            self.show_pagenumber = 'plain'
        else:
            self.show_pagenumber = 'empty'
        self.Dialog.accept()


class Ui_Dialog_speichern(QtWidgets.QDialog):
    def setupUi(self, Dialog, developer_mode_active, chosen_variation, save_mode):
 
        self.Dialog = Dialog
        self.developer_mode_active = developer_mode_active
        Dialog.setObjectName("Dialog")
        if self.developer_mode_active == False:
            titel = "Aufgabe speichern"
        if self.developer_mode_active == True:
            titel = "Administrator Modus - Aufgabe speichern"
        Dialog.setWindowTitle(titel)

        Dialog.setStyleSheet(
            "color: white; background-color: {0}".format(get_color(blue_7))
        )
        Dialog.setWindowIcon(QIcon(logo_path))
        gridlayout = create_new_gridlayout(Dialog)
        label_question = create_new_label(
            Dialog,
            "Sind Sie sicher, dass Sie die folgendene Aufgabe speichern wollen?\n\n",
        )
        gridlayout.addWidget(label_question, 0, 0, 1, 2)
        self.label = create_new_label(Dialog, "")
        self.label.setStyleSheet("padding-left: 25px;")
        # self.label.setWordWrap(True)
        gridlayout.addWidget(self.label, 1, 0, 1, 2)

        if self.developer_mode_active==False and save_mode == 'general':
            self.cb_confirm = create_new_checkbox(Dialog, " ")
            # self.cb_confirm.setSizePolicy(SizePolicy_fixed)
            self.cb_confirm.setStyleSheet(f"""
            QCheckBox {{
                spacing: -5px;
                padding-top: 2px;
            }}

            QCheckBox::indicator:unchecked {{ 
                image: url({get_icon_path("square.svg", color="ghostwhite")});
                width: 35px;
            }}

            QCheckBox::indicator:checked {{ 
                image: url({get_icon_path("check-square.svg", color="ghostwhite")});
                width: 35px;
            }}""")

            gridlayout.addWidget(self.cb_confirm, 2, 0, 1, 1, Qt.AlignTop)
            self.label_checkbox = create_new_label(
                Dialog,
                "Hiermit bestätige ich, dass ich die eingegebene Aufgabe eigenständig und\nunter Berücksichtigung des Urheberrechtsgesetzes verfasst habe.\n"
                "Ich stelle die eingegebene Aufgabe frei gemäß der Lizenz CC0 1.0 zur Verfügung.\n"
                "Die Aufgabe darf daher zu jeder Zeit frei verwendet, kopiert und verändert werden.",
                False,
                True,
            )
            # self.label_checkbox.setStyleSheet("padding-bottom: 20px;")
            gridlayout.addWidget(self.label_checkbox, 2, 1, 1, 1, Qt.AlignTop)
            self.label_checkbox.clicked.connect(self.label_checkbox_clicked)


        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        if self.developer_mode_active == False:
            if save_mode == 'local':
                self.buttonBox.setStandardButtons(
                    QtWidgets.QDialogButtonBox.Apply | QtWidgets.QDialogButtonBox.No
                )
            elif chosen_variation == None:
                self.buttonBox.setStandardButtons(
                    QtWidgets.QDialogButtonBox.Yes
                    | QtWidgets.QDialogButtonBox.No
                    | QtWidgets.QDialogButtonBox.Apply
                )
            else:
                self.buttonBox.setStandardButtons(
                    QtWidgets.QDialogButtonBox.Yes | QtWidgets.QDialogButtonBox.No
                )
        elif self.developer_mode_active == True:
            self.buttonBox.setStandardButtons(
                QtWidgets.QDialogButtonBox.Yes | QtWidgets.QDialogButtonBox.No
            )

        buttonN = self.buttonBox.button(QtWidgets.QDialogButtonBox.No)
        buttonN.setText("Abbrechen")
        self.buttonBox.rejected.connect(self.Dialog.reject)

        if save_mode == 'general':
            buttonY = self.buttonBox.button(QtWidgets.QDialogButtonBox.Yes)
            buttonY.setText("Speichern")
            buttonY.clicked.connect(self.yes_pressed)

        if (self.developer_mode_active==False and chosen_variation == None) or save_mode == 'local':
            button_local = self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply)
            button_local.setText("Lokal speichern")
            button_local.clicked.connect(self.local_pressed)

        gridlayout.addWidget(self.buttonBox, 3, 1, 1, 1)

    def local_pressed(self):
        self.confirmed = ["local", None]
        self.Dialog.accept()

    def yes_pressed(self):
        if self.developer_mode_active == True:
            self.confirmed = ["admin", 0]
        else:
            self.confirmed = ["user", self.cb_confirm.isChecked()]

        self.Dialog.accept()
        # return True

    def label_checkbox_clicked(self):
        if self.cb_confirm.isChecked() == True:
            self.cb_confirm.setChecked(False)
        elif self.cb_confirm.isChecked() == False:
            self.cb_confirm.setChecked(True)

    def get_output(self):
        return self.confirmed


class Ui_Dialog_setup(object):
    def setupUi(self, Dialog, MainWindow):
        self.MainWindow = MainWindow
        standard_settings = {
            'start_program' : 0,
            'pdf_reader' : "",
            'database' : 2,
            'display' : 0,
            'search_output': 0,
            'halfpoints': False,
            'prozente': [87, 75, 61, 50],
            'notenschluessel': [False, False],
            'halfpoints_cria': False,
            'prozente_cria': [91, 80, 64, 50],
            'notenschluessel_cria': [False, False],
            'autosave' : 2,
            'quelle' : '',
            'popup_off': False,
        }
        try: 
            with open(lama_settings_file, "r", encoding="utf8") as f:
                self.lama_settings = load(f)

            for all in standard_settings:
                try:
                    self.lama_settings[all]
                except KeyError:
                    self.lama_settings[all] = standard_settings[all] 
        except FileNotFoundError:
            self.lama_settings = standard_settings

        # Dialog.resize(500, 200)
        # print(self.lama_settings)
        # self.beispieldaten_dateipfad_cria = MainWindow.beispieldaten_dateipfad_cria
        # self.beispieldaten_dateipfad_1 = MainWindow.beispieldaten_dateipfad_1
        # self.beispieldaten_dateipfad_2 = MainWindow.beispieldaten_dateipfad_2

        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("Einstellungen")
        row=0

        # self.Dialog.setMinimumWidth(400)
        Dialog.setWindowIcon(QIcon(logo_path))

        verticallayout = create_new_verticallayout(Dialog)

        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        verticallayout.addWidget(self.tabWidget)

        self.tab_general = QtWidgets.QWidget(self.tabWidget)
        self.tabWidget.addTab(self.tab_general, "Allgemein")

        self.tab_search = QtWidgets.QWidget(self.tabWidget)
        self.tabWidget.addTab(self.tab_search, "Aufgabensuche")

        self.tab_sage = QtWidgets.QWidget(self.tabWidget)
        self.tabWidget.addTab(self.tab_sage, "Prüfungsgenerator")

        self.tab_creator = QtWidgets.QWidget(self.tabWidget)
        self.tabWidget.addTab(self.tab_creator, "Aufgabeneingabe")

        verticallayout_tab_general = create_new_verticallayout(self.tab_general)
        verticallayout_tab_search = create_new_verticallayout(self.tab_search)
        verticallayout_tab_sage = create_new_verticallayout(self.tab_sage)
        verticallayout_tab_creator = create_new_verticallayout(self.tab_creator)

        # gridlayout_setup = create_new_gridlayout(Dialog)

        ################################
        ################### TAB GENERAL
        ################################

        groupbox_start_program = create_new_groupbox(self.tab_general, "Auswahl beim Programmstart")
        groupbox_start_program.setSizePolicy(SizePolicy_fixed_height)
        horizontalLayout_start_program = create_new_horizontallayout(groupbox_start_program)

        # label_start_program = create_new_label(groupbox_start_program, "Auswahl")
        # horizontalLayout_start_program.addWidget(label_start_program)

        self.combobox_start_program = create_new_combobox(groupbox_start_program)
        add_new_option(self.combobox_start_program, 0, "beim Start fragen")
        add_new_option(self.combobox_start_program, 1, "LaMA (Unterstufe)")
        add_new_option(self.combobox_start_program, 2, "LaMA (Oberstufe)")
        add_new_option(self.combobox_start_program, 3, "Worksheet Wizard")
        
        try:
            self.combobox_start_program.setCurrentIndex(self.lama_settings['start_program'])
        except KeyError:
            self.lama_settings['start_program'] = 0
        horizontalLayout_start_program.addWidget(self.combobox_start_program)

        verticallayout_tab_general.addWidget(groupbox_start_program)
        # row +=1

        groupbox_path_pdf = create_new_groupbox(self.tab_general, "Dateipfad PDF Reader")
        groupbox_path_pdf.setSizePolicy(SizePolicy_fixed_height)
        horizontallayout_path_pdf = create_new_horizontallayout(groupbox_path_pdf)

        # label_pdf_reader = create_new_label(Dialog,"Dateipfad:")
        # horizontallayout_path_pdf.addWidget(label_pdf_reader)

        self.lineedit_pdf_reader = create_new_lineedit(groupbox_path_pdf)
        horizontallayout_path_pdf.addWidget(self.lineedit_pdf_reader)
        try:
            self.lineedit_pdf_reader.setText(self.lama_settings['pdf_reader'])
        except KeyError:
            self.lama_settings['pdf_reader'] = ""


        self.button_search_pdf_reader = create_new_button(groupbox_path_pdf, "Durchsuchen", self.search_pdf_reader)
        self.button_search_pdf_reader.setIcon(QIcon(get_icon_path('folder.svg')))
        horizontallayout_path_pdf.addWidget(self.button_search_pdf_reader)

        verticallayout_tab_general.addWidget(groupbox_path_pdf)
        # row +=1

        groupbox_database = create_new_groupbox(self.tab_general, "Automatische Aktualisierung der Datenbank")
        groupbox_database.setSizePolicy(SizePolicy_fixed_height)
        horizontallayout_database = create_new_horizontallayout(groupbox_database)

        # label_database = create_new_label(Dialog, "Datenbank automatisch aktualisieren:")
        # horizontallayout_database.addWidget(label_database)
        self.combobox_database = create_new_combobox(groupbox_database)
        horizontallayout_database.addWidget(self.combobox_database)
        

        add_new_option(self.combobox_database, 0, "jedes Mal beim Öffnen von LaMA")
        add_new_option(self.combobox_database, 1, "täglich")
        add_new_option(self.combobox_database, 2, "wöchentlich")
        add_new_option(self.combobox_database, 3, "monatlich")
        add_new_option(self.combobox_database, 4, "niemals")

        try:
            self.combobox_database.setCurrentIndex(self.lama_settings['database'])
        except KeyError:
            self.lama_settings['database'] = 2
            self.combobox_database.setCurrentIndex(2)
        
        verticallayout_tab_general.addWidget(groupbox_database)
        # row+=1

        groupbox_display = create_new_groupbox(self.tab_general, "Anzeigemodus")
        horizontallayout_display = create_new_horizontallayout(groupbox_display)
    
        # label_display = create_new_label(Dialog, "Darstellung:")
        # horizontallayout_display.addWidget(label_display)
        self.combobox_display = create_new_combobox(Dialog)
        # self.combobox_display.currentIndexChanged.connect(self.combobox_display_changed)
        horizontallayout_display.addWidget(self.combobox_display)

        add_new_option(self.combobox_display, 0, "Standard")
        add_new_option(self.combobox_display, 1, "Dark Mode")

        try:
            self.combobox_display.setCurrentIndex(self.lama_settings['display'])
        except KeyError:
            self.lama_settings['display'] = 0
        
        verticallayout_tab_general.addWidget(groupbox_display)
        groupbox_display.hide()


        ################################
        ################### TAB SEARCH
        ################################

        groupbox_search_output = create_new_groupbox(self.tab_search, "PDF Ausgabe")
        groupbox_search_output.setSizePolicy(SizePolicy_fixed_height)
        verticallayout_tab_search.addWidget(groupbox_search_output)
        horizontalLayout_search_output = create_new_horizontallayout(groupbox_search_output)

        self.combobox_search_output = create_new_combobox(groupbox_search_output)
        horizontalLayout_search_output.addWidget(self.combobox_search_output)

        add_new_option(self.combobox_search_output, 0,"kompakt")
        add_new_option(self.combobox_search_output, 1,"Seitenumbruch nach jeder Aufgabe")

        try:
            self.combobox_search_output.setCurrentIndex(self.lama_settings['search_output'])
        except KeyError:
            self.lama_settings['search_output'] == 0
        

        ################################
        ################### TAB SAGE
        ################################
        
        groupbox_autosave = create_new_groupbox(self.tab_sage, "Autosave Intervall")
        groupbox_autosave.setToolTip("0 = Autosave deaktivieren")
        horizontallayout_autosave = create_new_horizontallayout(groupbox_autosave)

        # label_autosave = create_new_label(Dialog, "Intervall:")
        # horizontallayout_autosave.addWidget(label_autosave)

        self.spinbox_autosave = create_new_spinbox(groupbox_autosave, value=2)
        try:
            self.spinbox_autosave.setValue(self.lama_settings['autosave'])
        except KeyError:
            self.lama_settings['autosave'] = 2
        self.spinbox_autosave.setSizePolicy(SizePolicy_fixed)
        horizontallayout_autosave.addWidget(self.spinbox_autosave)

        label_autosave_2 = create_new_label(groupbox_autosave, "Minuten")
        horizontallayout_autosave.addWidget(label_autosave_2)

        verticallayout_tab_sage.addWidget(groupbox_autosave)


        if MainWindow.chosen_program == 'cria':
            string = 'Unterstufe'
            try:
                self.lama_settings['prozente_cria']
                halfpoints = 'halfpoints_cria'
                key_prozente = 'prozente_cria'
                key_notenschluessel = 'notenschluessel_cria'
            except KeyError:
                key_prozente = 'prozente'
                key_notenschluessel ='notenschluessel'
        else:
            string = 'Oberstufe'
            key_prozente = 'prozente'
            halfpoints = 'halfpoints'
            key_notenschluessel = 'notenschluessel'


        
        groupbox_halfpoints = create_new_groupbox(self.tab_sage, f"Punkte für Aufgaben ({string})")
        horizontallayout_halfpoints = create_new_horizontallayout(groupbox_halfpoints)

        
        self.checkbox_halfpoints = create_new_checkbox(groupbox_halfpoints, "Halbe Punkte für Aufgaben erlauben", checked=self.lama_settings[halfpoints])
        horizontallayout_halfpoints.addWidget(self.checkbox_halfpoints)

        verticallayout_tab_sage.addWidget(groupbox_halfpoints)


        groupbox_prozent = create_new_groupbox(self.tab_sage, "Prozente Beurteilung ({})".format(string))
        gridlayout_prozente = create_new_gridlayout(groupbox_prozent)



        # self.combobox_notenschluessel_typ = create_new_combobox(groupbox_prozent)
        # gridlayout_prozente.addWidget(self.combobox_notenschluessel_typ, 0, 0, 1, 4)
        # add_new_option(self.combobox_notenschluessel_typ, 0, "Standard")
        # add_new_option(self.combobox_notenschluessel_typ, 1, "Individuell")
        # self.combobox_notenschluessel_typ.currentIndexChanged.connect(self.combobox_notenschluessel_typ_changed)

        self.label_prozente_sgu = create_new_label(groupbox_prozent, "Sehr gut:")
        gridlayout_prozente.addWidget(self.label_prozente_sgu, 0, 0, 1, 1)
        try:
            sgu_value = self.lama_settings[key_prozente][0]
        except KeyError:
            sgu_value = 91

        self.spinbox_prozente_sgu = create_new_spinbox(groupbox_prozent, sgu_value)
        gridlayout_prozente.addWidget(self.spinbox_prozente_sgu, 0, 1, 1, 1)


        self.label_prozente_gu = create_new_label(groupbox_prozent, "Gut:")
        gridlayout_prozente.addWidget(self.label_prozente_gu, 0, 2, 1, 1)
        try:
            gu_value = self.lama_settings[key_prozente][1]
        except KeyError:
            gu_value = 80

        self.spinbox_prozente_gu = create_new_spinbox(groupbox_prozent, gu_value)
        gridlayout_prozente.addWidget(self.spinbox_prozente_gu, 0, 3, 1, 1)


        self.label_prozente_be = create_new_label(groupbox_prozent, "Befriedigend:")
        gridlayout_prozente.addWidget(self.label_prozente_be, 1, 0, 1, 1)
        try:
            be_value = self.lama_settings[key_prozente][2]
        except KeyError:
            be_value = 64

        self.spinbox_prozente_be = create_new_spinbox(groupbox_prozent, be_value)
        gridlayout_prozente.addWidget(self.spinbox_prozente_be, 1, 1, 1, 1)


        self.label_prozente_ge = create_new_label(groupbox_prozent, "Genügend:")
        gridlayout_prozente.addWidget(self.label_prozente_ge, 1, 2, 1, 1)
        try:
            ge_value = self.lama_settings[key_prozente][3]
        except KeyError:
            ge_value = 50

        self.spinbox_prozente_ge = create_new_spinbox(groupbox_prozent, ge_value)
        gridlayout_prozente.addWidget(self.spinbox_prozente_ge, 1, 3, 1, 1)
    

        
        widget_notenschluessel_edit = QtWidgets.QWidget(groupbox_prozent)
        gridlayout_prozente.addWidget(widget_notenschluessel_edit, 2,0,1,4)

        horizontallayout_notenschluessel_edit = create_new_horizontallayout(widget_notenschluessel_edit)
        horizontallayout_notenschluessel_edit.setContentsMargins(0, 0, 0, 0)

        try:
            ns_halbe_punkte_checked = self.lama_settings[key_notenschluessel][0]
        except KeyError:
            ns_halbe_punkte_checked = False
        self.cb_ns_halbe_punkte = create_new_checkbox(widget_notenschluessel_edit, "Halbe Punkte", checked= ns_halbe_punkte_checked)
        horizontallayout_notenschluessel_edit.addWidget(self.cb_ns_halbe_punkte)
        # gridlayout_prozente.addWidget(self.cb_ns_halbe_punkte, 3,0,1,2)

        try:
            ns_prozente_checked = self.lama_settings[key_notenschluessel][1]
        except KeyError:
            ns_prozente_checked = False
        self.cb_ns_prozente = create_new_checkbox(widget_notenschluessel_edit, "Prozentangabe", checked= ns_prozente_checked)
        # gridlayout_prozente.addWidget(self.cb_ns_prozente, 3,2,1,2)       
        horizontallayout_notenschluessel_edit.addWidget(self.cb_ns_prozente)


        btn_edit_notenschluessel_individual = create_new_button(groupbox_prozent, "Individuelle Notenschlüssel", self.btn_individual_notenschluessel_clicked, icon="edit-2.svg")
        # horizontallayout_notenschluessel_edit.addWidget(btn_edit_notenschluessel_individual)
        gridlayout_prozente.addWidget(btn_edit_notenschluessel_individual, 3,0,1,4)

        verticallayout_tab_sage.addWidget(groupbox_prozent)
        # row +=1       



        # row+=1
        ################################
        ################### TAB CREATOR
        ################################

        groupbox_quelle = create_new_groupbox(Dialog, "Quelle Standardeingabe")
        horizontallayout_quelle = create_new_horizontallayout(groupbox_quelle)

        self.lineedit_quelle = create_new_lineedit(Dialog)
        try:
            self.lineedit_quelle.setText(self.lama_settings['quelle'])
        except KeyError:
            self.lama_settings['quelle'] = ""        

        horizontallayout_quelle.addWidget(self.lineedit_quelle)

        verticallayout_tab_creator.addWidget(groupbox_quelle)
        # row +=1



        # row +=1


        # gridlayout_setup.setRowStretch(row, 1)
        # row +=1

        verticallayout_tab_general.addStretch()
        verticallayout_tab_search.addStretch()
        verticallayout_tab_sage.addStretch()
        verticallayout_tab_creator.addStretch()


        self.buttonBox_setup = QtWidgets.QDialogButtonBox(self.Dialog)
        self.buttonBox_setup.setStandardButtons(
            QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel
        )


        buttonS = self.buttonBox_setup.button(QtWidgets.QDialogButtonBox.Save)
        buttonS.setText('Speichern')
        buttonS.setIcon(QIcon(get_icon_path('save.svg')))
        buttonX = self.buttonBox_setup.button(QtWidgets.QDialogButtonBox.Cancel)
        buttonX.setText("Abbrechen")
        buttonX.setIcon(QIcon(get_icon_path('x.svg')))
        self.buttonBox_setup.rejected.connect(self.reject_dialog)
        self.buttonBox_setup.accepted.connect(partial(self.save_setting, MainWindow.chosen_program))

        verticallayout.addWidget(self.buttonBox_setup)



    def btn_individual_notenschluessel_clicked(self):
        Dialog = QtWidgets.QDialog(
            None,
            Qt.WindowSystemMenuHint
            | Qt.WindowTitleHint
            | Qt.WindowCloseButtonHint,
        )
        ui = Ui_Dialog_set_individual_ns()
        ui.setupUi(Dialog, self.MainWindow)
        # self.Dialog.show()
        Dialog.exec()
        # screen_resolution = app.desktop().screenGeometry()
        # screen_width = screen_resolution.width()

        # ui = Ui_Dialog_set_individual_ns()
        # ui.setupUi(Dialog)

        # bring_to_front(self.Dialog)

        # self.Dialog.setFixedSize(self.Dialog.size())
        # rsp = Dialog.exec_()
        # list_widgets_notenschluessel = [self.spinbox_prozente_sgu, self.spinbox_prozente_gu, self.spinbox_prozente_be, self.spinbox_prozente_ge]
        # list_widgets_notenschluessel_individual = [self.widget_sg, self.widget_gu, self.widget_be, self.widget_ge]
        # if self.combobox_notenschluessel_typ.currentIndex()==0:
        #     for widget in list_widgets_notenschluessel:
        #         widget.show()
        #     for widget in list_widgets_notenschluessel_individual:
        #         widget.hide()

        # elif self.combobox_notenschluessel_typ.currentIndex()==1:
        #     for widget in list_widgets_notenschluessel:
        #         widget.hide()
        #     for widget in list_widgets_notenschluessel_individual:
        #         widget.show()


    ########################################################################
    ########################################################################





    ############################################################################
    ###########################################################################
        
    # def combobox_display_changed(self):
    #     information_window("Die Darstellung wird erst nach dem Neustart von LaMA übernommen.")
        
    # def combobox_notenschluessel_typ_changed(self):
    #     list_widgets_notenschluessel = [self.spinbox_prozente_sgu, self.spinbox_prozente_gu, self.spinbox_prozente_be, self.spinbox_prozente_ge]
    #     list_widgets_notenschluessel_individual = [self.widget_sg, self.widget_gu, self.widget_be, self.widget_ge]
    #     if self.combobox_notenschluessel_typ.currentIndex()==0:
    #         for widget in list_widgets_notenschluessel:
    #             widget.show()
    #         for widget in list_widgets_notenschluessel_individual:
    #             widget.hide()

    #     elif self.combobox_notenschluessel_typ.currentIndex()==1:
    #         for widget in list_widgets_notenschluessel:
    #             widget.hide()
    #         for widget in list_widgets_notenschluessel_individual:
    #             widget.show()

    def search_pdf_reader(self):
        list_filename = QtWidgets.QFileDialog.getOpenFileName(
            None, "Durchsuchen", self.lama_settings['pdf_reader'], "Alle Dateien (*)"
            )
        if list_filename[0] == '':
            return

        self.lineedit_pdf_reader.setText(list_filename[0])

    def reject_dialog(self):
        self.Dialog.reject()

    def save_settings_to_dict(self, chosen_program):
        # self.lama_settings
        dict_={}
        dict_['start_program'] = self.combobox_start_program.currentIndex()
        dict_['pdf_reader'] = self.lineedit_pdf_reader.text()
        dict_['database'] = self.combobox_database.currentIndex()
        dict_['display'] = self.combobox_display.currentIndex()
        dict_['search_output'] = self.combobox_search_output.currentIndex()
        dict_['autosave'] = self.spinbox_autosave.value()
        dict_['quelle'] = self.lineedit_quelle.text()
        if chosen_program == 'cria':
            key_halfpoints  = 'halfpoints_cria'
            key_prozente = 'prozente_cria'
            key_notenschluessel = 'notenschluessel_cria'

            dict_['halfpoints'] = self.lama_settings['halfpoints']
            dict_['prozente'] = self.lama_settings['prozente']
            dict_['notenschluessel'] = self.lama_settings['notenschluessel']

        else:
            key_halfpoints  = 'halfpoints'
            key_prozente = 'prozente'
            key_notenschluessel = 'notenschluessel'

            try: 
                dict_['halfpoints_cria'] = self.lama_settings['halfpoints_cria']
                dict_['prozente_cria'] = self.lama_settings['prozente_cria']
                dict_['notenschluessel_cria'] = self.lama_settings['notenschluessel_cria']
            except KeyError:
                dict_['halfpoints_cria'] = self.lama_settings['halfpoints']
                dict_['prozente_cria'] = self.lama_settings['prozente']
                dict_['notenschluessel_cria'] = self.lama_settings['notenschluessel']                

        dict_[key_halfpoints] = self.checkbox_halfpoints.isChecked()
        dict_[key_prozente] = [self.spinbox_prozente_sgu.value(), self.spinbox_prozente_gu.value(), self.spinbox_prozente_be.value(), self.spinbox_prozente_ge.value()]
        dict_[key_notenschluessel] = [self.cb_ns_halbe_punkte.isChecked(), self.cb_ns_prozente.isChecked()]

        # if chosen_program == 'cria':
        #     key_notenschluessel_individual = 'notenschluessel_cria_individual'
        # else:
        #     key_notenschluessel_individual = 'notenschluessel_individual'

        # dict_[key_notenschluessel_individual] = [
        #     self.lineedit_sg_lower.text(),
        #     self.lineedit_gu_upper.text(),
        #     self.lineedit_gu_lower.text(),
        #     self.lineedit_be_upper.text(),
        #     self.lineedit_be_lower.text(),
        #     self.lineedit_ge_upper.text(),
        #     self.lineedit_ge_lower.text(),
        #     ]


        try:
            dict_['popup_off'] = self.lama_settings['popup_off']
        except KeyError:
            dict_['popup_off'] = False
        return dict_

    def set_settings_in_sage(self):
        self.MainWindow.lineEdit_quelle.setText(self.lineedit_quelle.text())
        self.MainWindow.spinBox_2.setValue(self.spinbox_prozente_sgu.value())
        self.MainWindow.spinBox_3.setValue(self.spinbox_prozente_gu.value())
        self.MainWindow.spinBox_4.setValue(self.spinbox_prozente_be.value())
        self.MainWindow.spinBox_5.setValue(self.spinbox_prozente_ge.value())
        self.MainWindow.cb_ns_halbe_pkt.setChecked(self.cb_ns_halbe_punkte.isChecked())
        self.MainWindow.cb_ns_prozent.setChecked(self.cb_ns_prozente.isChecked())


        # self.MainWindow.lineedit_sg_lower_limit.setText(self.lineedit_sg_lower.text())
        # self.MainWindow.lineedit_g_upper_limit.setText(self.lineedit_gu_upper.text())
        # self.MainWindow.lineedit_g_lower_limit.setText(self.lineedit_gu_lower.text())
        # self.MainWindow.lineedit_b_upper_limit.setText(self.lineedit_be_upper.text())
        # self.MainWindow.lineedit_b_lower_limit.setText(self.lineedit_be_lower.text())
        # self.MainWindow.lineedit_g2_upper_limit.setText(self.lineedit_ge_upper.text())
        # self.MainWindow.lineedit_g2_lower_limit.setText(self.lineedit_ge_lower.text())

        
    def save_setting(self, chosen_program):
        if self.MainWindow.display_mode != self.combobox_display.currentIndex():
            information_window("Die Änderung der Darstellung wird erst nach dem Neustart von LaMA übernommen.")
        self.lama_settings = self.save_settings_to_dict(chosen_program)

        with open(lama_settings_file, "w+", encoding="utf8") as f:
            dump(self.lama_settings, f, ensure_ascii=False)
    
        self.set_settings_in_sage()
        self.Dialog.accept()
    

class Ui_Dialog_set_individual_ns(QtWidgets.QDialog):
    def __init__(self):
        try:
            with open(lama_notenschluessel_file, "r", encoding="utf8") as f:
                self.dict_notenschluessel = load(f)
        except FileNotFoundError:
            self.dict_notenschluessel = {}

    def setupUi(self, Dialog, MainWindow):
        self.Dialog = Dialog
        self.MainWindow = MainWindow
        Dialog.setWindowTitle("Individuelle Notenschlüssel")
        Dialog.setWindowIcon(QIcon(logo_path))
        Dialog.setSizePolicy(SizePolicy_fixed)


        verticallayout = create_new_verticallayout(Dialog)


        widget_ns_names = QtWidgets.QWidget(Dialog)
        verticallayout.addWidget(widget_ns_names)

        horizontallayout_widget_ns = create_new_horizontallayout(widget_ns_names)
        horizontallayout_widget_ns.setContentsMargins(0,0,0,0)

        label_ns = create_new_label(widget_ns_names, "Notenschlüssel:")
        horizontallayout_widget_ns.addWidget(label_ns)

        self.combobox_ns = create_new_combobox(Dialog)
        horizontallayout_widget_ns.addWidget(self.combobox_ns)

        horizontallayout_widget_ns.addStretch()

        add_new_option(self.combobox_ns, 0, "Neuer Notenschlüssel")

        index = 1
        for all in self.dict_notenschluessel.keys():
            add_new_option(self.combobox_ns, index, all)
            index +=1            

        self.combobox_ns.setEditable(True)
        self.combobox_ns.currentIndexChanged.connect(lambda: self.combobox_ns_index_changed())

        regexp = QRegExp("[0-9,;/\.]*")
        validator = QRegExpValidator(regexp)

        widget_ns = QtWidgets.QWidget(Dialog)
        verticallayout.addWidget(widget_ns)

        horizontallayout_entry = create_new_horizontallayout(widget_ns)
        horizontallayout_entry.setContentsMargins(0,0,0,0)

        widget_ns_grades = QtWidgets.QWidget(widget_ns)
        horizontallayout_entry.addWidget(widget_ns_grades)

        verticallayout_grades = create_new_verticallayout(widget_ns_grades)
        verticallayout_grades.setContentsMargins(0,0,0,0)

        label_sg = create_new_label(widget_ns_grades,"Sehr gut:")
        verticallayout_grades.addWidget(label_sg)

        label_gu = create_new_label(widget_ns_grades,"Gut:")
        verticallayout_grades.addWidget(label_gu)

        label_be = create_new_label(widget_ns_grades,"Befriedigend:")
        verticallayout_grades.addWidget(label_be)

        label_ge = create_new_label(widget_ns_grades,"Genügend:")
        verticallayout_grades.addWidget(label_ge)


        widget_ns_entry = QtWidgets.QWidget(widget_ns_grades)
        horizontallayout_entry.addWidget(widget_ns_entry)

        verticallayout_entry = create_new_verticallayout(widget_ns_entry)
        verticallayout_entry.setContentsMargins(0,0,0,0)

        widget_sg = QtWidgets.QWidget(widget_ns_entry)
        verticallayout_entry.addWidget(widget_sg)

        horizontallayout_sg = create_new_horizontallayout(widget_sg)
        horizontallayout_sg.setContentsMargins(0,0,0,0)

        label_sg_2 = create_new_label(widget_sg,"Gesamtpunkte -  ")
        horizontallayout_sg.addWidget(label_sg_2)
        
        
        self.lineedit_sg_lower = create_new_lineedit(widget_sg)
        self.lineedit_sg_lower.setValidator(validator)
        horizontallayout_sg.addWidget(self.lineedit_sg_lower)




        widget_gu = QtWidgets.QWidget(widget_ns_entry)
        verticallayout_entry.addWidget(widget_gu)

        horizontallayout_gu = create_new_horizontallayout(widget_gu)
        horizontallayout_gu.setContentsMargins(0,0,0,0)

        self.lineedit_gu_upper = create_new_lineedit(widget_gu)
        horizontallayout_gu.addWidget(self.lineedit_gu_upper)
        self.lineedit_gu_upper.setValidator(validator)

        label_gu_2 = create_new_label(widget_gu, " - ")
        horizontallayout_gu.addWidget(label_gu_2)

        self.lineedit_gu_lower = create_new_lineedit(widget_gu)
        horizontallayout_gu.addWidget(self.lineedit_gu_lower)
        self.lineedit_gu_lower.setValidator(validator)


        widget_be = QtWidgets.QWidget(widget_ns_entry)
        verticallayout_entry.addWidget(widget_be)

        horizontallayout_be = create_new_horizontallayout(widget_be)
        horizontallayout_be.setContentsMargins(0,0,0,0)


        self.lineedit_be_upper = create_new_lineedit(widget_be)
        horizontallayout_be.addWidget(self.lineedit_be_upper)
        self.lineedit_be_upper.setValidator(validator)

        label_be_2 = create_new_label(widget_be, " - ")
        horizontallayout_be.addWidget(label_be_2)

        self.lineedit_be_lower = create_new_lineedit(widget_be)
        horizontallayout_be.addWidget(self.lineedit_be_lower)
        self.lineedit_be_lower.setValidator(validator)


        widget_ge = QtWidgets.QWidget(widget_ns_entry)
        verticallayout_entry.addWidget(widget_ge)

        horizontallayout_ge = create_new_horizontallayout(widget_ge)
        horizontallayout_ge.setContentsMargins(0,0,0,0)


        self.lineedit_ge_upper = create_new_lineedit(widget_ge)
        horizontallayout_ge.addWidget(self.lineedit_ge_upper)
        self.lineedit_ge_upper.setValidator(validator)

        label_ge_2 = create_new_label(widget_ge, " - ")
        horizontallayout_ge.addWidget(label_ge_2)

        self.lineedit_ge_lower = create_new_lineedit(widget_ge)
        horizontallayout_ge.addWidget(self.lineedit_ge_lower)
        self.lineedit_ge_lower.setValidator(validator)


        buttonbox = QtWidgets.QDialogButtonBox(Dialog)
        buttonbox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Discard
        )
        verticallayout.addWidget(buttonbox)


        buttonS = buttonbox.button(QtWidgets.QDialogButtonBox.Save)
        buttonS.setText('Speichern')
        buttonS.setIcon(QIcon(get_icon_path('save.svg')))
        buttonX = buttonbox.button(QtWidgets.QDialogButtonBox.Cancel)
        buttonX.setText("Abbrechen")
        buttonX.setIcon(QIcon(get_icon_path('x.svg')))

        self.button_delete = buttonbox.button(QtWidgets.QDialogButtonBox.Discard)
        self.button_delete.setText('Löschen')
        self.button_delete.setEnabled(False)
        self.button_delete.setIcon(QIcon(get_icon_path('trash-2.svg')))

        buttonS.clicked.connect(lambda: self.save_clicked())
        buttonX.clicked.connect(lambda: self.cancel_clicked())
        self.button_delete.clicked.connect(lambda: self.delete_clicked()) #self.delete_clicked


        # self.buttonBox_setup.rejected.connect(self.reject_dialog)
        # self.buttonBox_setup.accepted.connect(partial(self.save_setting, MainWindow.chosen_program))


    @report_exceptions
    def combobox_ns_index_changed(self):
        if self.combobox_ns.currentIndex()==0:
            self.combobox_ns.setEditable(True)
            self.button_delete.setEnabled(False)
            self.lineedit_sg_lower.clear()
            self.lineedit_gu_upper.clear()
            self.lineedit_gu_lower.clear()
            self.lineedit_be_upper.clear()
            self.lineedit_be_lower.clear()
            self.lineedit_ge_upper.clear()
            self.lineedit_ge_lower.clear()
        elif self.combobox_ns.currentText() in self.dict_notenschluessel:
            grade_limits = self.dict_notenschluessel[self.combobox_ns.currentText()]
            self.combobox_ns.setEditable(False)
            self.lineedit_sg_lower.setText(grade_limits[0])
            self.lineedit_gu_upper.setText(grade_limits[1])
            self.lineedit_gu_lower.setText(grade_limits[2])
            self.lineedit_be_upper.setText(grade_limits[3])
            self.lineedit_be_lower.setText(grade_limits[4])
            self.lineedit_ge_upper.setText(grade_limits[5])
            self.lineedit_ge_lower.setText(grade_limits[6])

            self.button_delete.setEnabled(True)




    def add_to_dictionary(self):
        
        _list_entry = [
            self.lineedit_sg_lower.text(),
            self.lineedit_gu_upper.text(),
            self.lineedit_gu_lower.text(),
            self.lineedit_be_upper.text(),
            self.lineedit_be_lower.text(),
            self.lineedit_ge_upper.text(),
            self.lineedit_ge_lower.text(),
        ]

        # if self.combobox_ns.currentText() in self.dict_notenschluessel:
        #     rsp = information_window("Der Name des Notenschlüssels exisitiert bereits. Wollen sie diesen überschreiben?")
        #     if rsp == False:
        #         return rsp

        self.dict_notenschluessel[self.combobox_ns.currentText()] = _list_entry


    def save_clicked(self):
        rsp = self.add_to_dictionary()
        if rsp == False:
            return


        with open(lama_notenschluessel_file, "w", encoding="utf8") as f:
            dump(self.dict_notenschluessel, f, ensure_ascii=False)

        self.MainWindow.combobox_notenschluessel_saved.addItem(self.combobox_ns.currentText())
        self.Dialog.accept()

    def cancel_clicked(self):
        self.Dialog.reject()

    def reset_combobox(self):
        self.combobox_ns.clear()

        add_new_option(self.combobox_ns, 0, "Neuer Notenschlüssel")

        index = 1
        for all in self.dict_notenschluessel.keys():
            add_new_option(self.combobox_ns, index, all)
            index +=1   


        self.MainWindow.combobox_notenschluessel_saved.clear()

        add_new_option(self.MainWindow.combobox_notenschluessel_saved, 0, "")

        index = 1
        for all in self.dict_notenschluessel.keys():
            add_new_option(self.MainWindow.combobox_notenschluessel_saved, index, all)
            index +=1 



    def delete_clicked(self):
        rsp = information_window(f'Sind Sie sicher, dass die Notenschlüssel "{self.combobox_ns.currentText()}" löschen möchten?')

        if rsp == False:
            return

          

        self.dict_notenschluessel.pop(self.combobox_ns.currentText())

        with open(lama_notenschluessel_file, "w", encoding="utf8") as f:
            dump(self.dict_notenschluessel, f, ensure_ascii=False)

        

        self.reset_combobox()


class Ui_Dialog_developer(object):
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        self.developer_mode_active = False
        Dialog.setWindowTitle("Entwicklermodus aktivieren")
        row=0
        Dialog.setWindowIcon(QIcon(logo_path))
        gridlayout_developer = create_new_gridlayout(Dialog)

        label_developer = create_new_label(Dialog, "Bitte geben Sie das Passwort ein, um den Entwicklermodus zu aktivieren")
        gridlayout_developer.addWidget(label_developer, 0, 0, 1,2)

        self.lineedit_developer = create_new_lineedit(Dialog)
        self.lineedit_developer.setEchoMode(QtWidgets.QLineEdit.Password)
        gridlayout_developer.addWidget(self.lineedit_developer, 1,0,1,2)


        self.checkbox_developer = create_new_checkbox(Dialog, "Passwort speichern", True)
        gridlayout_developer.addWidget(self.checkbox_developer, 2,0,1,1)

        self.buttonBox_developer = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox_developer.setStandardButtons(
            QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel
        )


        buttonS = self.buttonBox_developer.button(QtWidgets.QDialogButtonBox.Save)
        buttonS.setText('Aktivieren')
        buttonS.setIcon(QIcon(get_icon_path('unlock.svg')))
        buttonX = self.buttonBox_developer.button(QtWidgets.QDialogButtonBox.Cancel)
        buttonX.setText("Abbrechen")
        self.buttonBox_developer.rejected.connect(self.reject_dialog)
        self.buttonBox_developer.accepted.connect(self.save_password)

        gridlayout_developer.addWidget(self.buttonBox_developer, 2,1,1,1)
    
    def reject_dialog(self):
        self.Dialog.reject()


    def save_password(self):
        QtWidgets.QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))


        hashed_pw = read_credentials()

        password = self.lineedit_developer.text().encode('utf-8')

        if bcrypt.checkpw(password, hashed_pw):
            if self.checkbox_developer.isChecked():
                if sys.platform.startswith("win"):
                    path_lama_developer_credentials = os.path.join(os.getenv('LOCALAPPDATA'), "LaMA", "credentials")
                elif sys.platform.startswith("darwin"):
                    path_lama_developer_credentials = os.path.join(Path.home(), "Library", "LaMA","credentials")
                # lama_developer_credentials = os.path.join(path_lama_developer_credentials, "developer_credentials.txt")
                if not os.path.exists(path_lama_developer_credentials):
                    os.makedirs(path_lama_developer_credentials)

                with open(lama_developer_credentials, "wb") as file:
                    file.write(password)
            
            self.developer_mode_active = True
            QtWidgets.QApplication.restoreOverrideCursor()
            self.Dialog.accept()
        else:
            QtWidgets.QApplication.restoreOverrideCursor()
            critical_window("Das eingegeben Passwort ist nicht korrekt.")
            # self.Dialog.reject() 


def read_credentials():
    #path_programdata = os.getenv('PROGRAMDATA')
    pw_file = os.path.join(path_programm, "_database", "_config" ,"hashed_credentials.txt")
    with open(pw_file, "rb") as file:
        hashed_pw = file.read()
    
    return hashed_pw





class Ui_Dialog_draft_control(object):
    def setupUi(self, Dialog, dict_drafts):
        self.Dialog = Dialog
        self.dict_drafts = dict_drafts
        Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("Entwürfe prüfen")
        Dialog.setSizePolicy(SizePolicy_fixed)
        # Dialog.setFixedSize(300, 150)
        Dialog.setWindowIcon(QIcon(logo_path))


        vertical_layout = create_new_verticallayout(Dialog)

        groupbox = create_new_groupbox(Dialog, "Offene Entwürfe")
        vertical_layout.addWidget(groupbox)

        gridlayout = create_new_gridlayout(groupbox)


        label_cria = create_new_label(groupbox, "Unterstufe:")
        gridlayout.addWidget(label_cria, 0,0,1,1)

        label_cria_num = create_new_label(groupbox, "{}".format(len(dict_drafts['cria'])))
        gridlayout.addWidget(label_cria_num, 0,1,1,1)


        button_cria = create_new_button(groupbox, "Entwürfe prüfen", partial(self.open_edit_draft, 'cria'))
        gridlayout.addWidget(button_cria, 0,2,1,1)
        if len(dict_drafts['cria']) == 0:
            button_cria.setEnabled(False)


        label_typ1 = create_new_label(groupbox, "Typ1 - Aufgaben:")
        gridlayout.addWidget(label_typ1, 1,0,1,1)

        label_typ1_num = create_new_label(groupbox, "{}".format(len(dict_drafts['lama_1'])))
        gridlayout.addWidget(label_typ1_num, 1,1,1,1)

        button_typ1 = create_new_button(groupbox, "Entwürfe prüfen", partial(self.open_edit_draft, 'lama_1'))
        gridlayout.addWidget(button_typ1, 1,2,1,1)
        if len(dict_drafts['lama_1']) == 0:
            button_typ1.setEnabled(False)

        label_typ2 = create_new_label(groupbox, "Typ2 - Aufgaben:")
        gridlayout.addWidget(label_typ2, 2,0,1,1)

        label_typ2_num = create_new_label(groupbox, "{}".format(len(dict_drafts['lama_2'])))
        gridlayout.addWidget(label_typ2_num, 2,1,1,1)


        button_typ2 = create_new_button(groupbox, "Entwürfe prüfen", partial(self.open_edit_draft, 'lama_2'))
        gridlayout.addWidget(button_typ2, 2,2,1,1)
        if len(dict_drafts['lama_2']) == 0:
            button_typ2.setEnabled(False)


    def open_edit_draft(self, typ):
        Dialog = QtWidgets.QDialog(
            None,
            Qt.WindowSystemMenuHint
            | Qt.WindowTitleHint
            | Qt.WindowCloseButtonHint
            | Qt.WindowMaximizeButtonHint
            | Qt.WindowMinimizeButtonHint
        )
        ui = Ui_Dialog_edit_drafts()
        ui.setupUi(Dialog, self.dict_drafts, typ)

        self.Dialog.accept()
        Dialog.exec() 


class Ui_Dialog_edit_drafts(object):
    def setupUi(self, Dialog, dict_drafts, typ):
        self.dict_drafts = dict_drafts
        self.typ = typ
        self.changed_themen = []
        self.dict_widget_variables = {}
        Dialog.setObjectName("Dialog")
        Dialog.setWindowIcon(QIcon(logo_path))
        Dialog.resize(567, 489)
        Dialog.setWindowTitle("Entwürfe prüfen")
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFixedHeight(150)
        # self.scrollArea.setSizePolicy(SizePolicy_fixed_height)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 374, 186))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        # self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        # self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_items = create_new_gridlayout(self.scrollAreaWidgetContents)

        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setTitle("Aufgabe bearbeiten")
        self.gridLayout_2 = create_new_gridlayout(self.groupBox)

        self.groupBox_aufgabe = create_new_groupbox(self.groupBox, "Aufgabe")
        self.gridLayout_2.addWidget(self.groupBox_aufgabe, 0,0,1,1)
        self.horizontalLayout_abstand = create_new_horizontallayout(self.groupBox_aufgabe)

        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")

        self.horizontalLayout_abstand.addWidget(self.comboBox)


        self.create_all_checkboxes_drafts()
        # row = 0
        # column = 0
        
        # for dict_aufgabe in self.dict_drafts[typ]:
        #     self.add_draft_to_list(dict_aufgabe, self.scrollAreaWidgetContents, row, column)
        #     if column == 2:
        #         row += 1
        #         column = 0
        #     else:
        #         column +=1        

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 4, 4)


        self.pushButton_check_all = create_new_button(Dialog,
        "Alle aus-/abwählen",
        self.check_all)  
        self.gridLayout.addWidget(self.pushButton_check_all, 0, 4, 1, 1)


        self.pushButton_open_editor = create_new_button(Dialog,
        "Ausgewählte Aufgabe(n) im\nLaTeX Editor öffnen",
        self.open_editor)
        self.gridLayout.addWidget(self.pushButton_open_editor, 1, 4, 1, 1)
        self.pushButton_open_editor.setEnabled(False)


        self.pushButton_add_to_database = create_new_button(Dialog,
        "Ausgewählte Aufgabe(n) zur\nDatenbank hinzufügen",
        self.add_to_ddb)
        self.gridLayout.addWidget(self.pushButton_add_to_database, 2, 4, 1, 1)
        self.pushButton_add_to_database.setEnabled(False)


        self.pushButton_delete = create_new_button(Dialog,
        "Ausgwählte Aufgabe(n) löschen",
        self.delete_draft)
        self.gridLayout.addWidget(self.pushButton_delete, 3, 4, 1, 1)
        self.pushButton_delete.setEnabled(False)


        # spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.gridLayout.addItem(spacerItem1, 4, 4, 1, 1)


        self.groupBox_pkt = create_new_groupbox(self.groupBox, "Pkte")
        self.gridLayout_2.addWidget(self.groupBox_pkt, 0,1,1,1)
        self.horizontalLayout_pkt = create_new_horizontallayout(self.groupBox_pkt)
        self.groupBox_pkt.setEnabled(False)
        

        self.spinBox_pkt = create_new_spinbox(self.groupBox_pkt)
        self.horizontalLayout_pkt.addWidget(self.spinBox_pkt)
        

        self.groupBox_af = create_new_groupbox(self.groupBox, "AF")
        self.gridLayout_2.addWidget(self.groupBox_af, 0,2,1,1)
        self.horizontalLayout_af = create_new_horizontallayout(self.groupBox_af)
        self.groupBox_af.setEnabled(False)
        
        self.comboBox_af = create_new_combobox(self.groupBox_af)
        self.horizontalLayout_af.addWidget(self.comboBox_af)
        

        if self.typ == 'lama_2':
            self.groupBox_af.hide()

        for i, all in enumerate(dict_aufgabenformate.keys()):
            if self.typ != 'cria' and i>3:
                break

            add_new_option(self.comboBox_af, i, all)


        self.groupBox_klasse = create_new_groupbox(self.groupBox, "Klasse")
        self.gridLayout_2.addWidget(self.groupBox_klasse, 0,3,1,1)
        # if self.typ == 'cria':
        #     self.groupBox_klasse.hide()
        self.horizontalLayout_klasse = create_new_horizontallayout(self.groupBox_klasse)
        self.groupBox_klasse.setEnabled(False)
        
        self.comboBox_klasse = create_new_combobox(self.groupBox_klasse)
        self.horizontalLayout_klasse.addWidget(self.comboBox_klasse)
        if self.typ == 'cria':
            add_new_option(self.comboBox_klasse, 0, "")
            i=1
            for all in list_klassen:
                add_new_option(self.comboBox_klasse, i, all)
                i+=1
            # self.comboBox_klasse.setEnabled(False)
        else:
            add_new_option(self.comboBox_klasse, 0, "")
            i=1
            for i, all in enumerate(Klassen.keys()):
                if i == 4:
                    break
                add_new_option(self.comboBox_klasse, i+1, all)


        self.groupBox_pagebreak = create_new_groupbox(self.groupBox, "Seitenumbr.")
        self.gridLayout_2.addWidget(self.groupBox_pagebreak, 0,4,1,1)
        self.groupBox_pagebreak.setEnabled(False)

        self.horizontalLayout_pagebreak = create_new_horizontallayout(self.groupBox_pagebreak)
        self.comboBox_pagebreak = create_new_combobox(self.groupBox_pagebreak)
        self.horizontalLayout_pagebreak.addWidget(self.comboBox_pagebreak)
        add_new_option(self.comboBox_pagebreak,0,"Nein")
        add_new_option(self.comboBox_pagebreak,1,"Ja")
        


        self.groupBox_abstand = create_new_groupbox(self.groupBox, "Abstand")
        self.gridLayout_2.addWidget(self.groupBox_abstand, 0,5,1,1)
        self.horizontalLayout_abstand = create_new_horizontallayout(self.groupBox_abstand)
        self.groupBox_abstand.setEnabled(False)
        

        self.spinBox_abstand = create_new_spinbox(self.groupBox)
        self.horizontalLayout_abstand.addWidget(self.spinBox_abstand)

        # self.gridLayout_2.setColumnStretch(6,1)

        self.groupBox_titel= create_new_groupbox(self.groupBox, "Titel")
        self.gridLayout_2.addWidget(self.groupBox_titel, 1,0,1,4)
        self.horizontalLayout_titel = create_new_horizontallayout(self.groupBox_titel)
        self.groupBox_titel.setEnabled(False)
        
        self.lineedit_titel = create_new_lineedit(self.groupBox_titel)
        self.horizontalLayout_titel.addWidget(self.lineedit_titel)
        


        self.groupBox_quelle= create_new_groupbox(self.groupBox, "Quelle")
        self.gridLayout_2.addWidget(self.groupBox_quelle, 0,6,1,1)
        self.horizontalLayout_quelle = create_new_horizontallayout(self.groupBox_quelle)
        self.groupBox_quelle.setEnabled(False)
        
        self.lineedit_quelle = create_new_lineedit(self.groupBox_quelle)
        self.horizontalLayout_quelle.addWidget(self.lineedit_quelle)

        self.groupBox_themen= create_new_groupbox(self.groupBox, "Themen")
        self.gridLayout_2.addWidget(self.groupBox_themen, 1,4,1,3)
        self.horizontalLayout_themen = create_new_horizontallayout(self.groupBox_themen)
        self.groupBox_themen.setEnabled(False)


        self.label_themen = create_new_label(self.groupBox_themen, "", wordwrap=True)
        self.horizontalLayout_themen.addWidget(self.label_themen)


        self.pushButton_themen = create_new_button(self.groupBox_themen,"Bearbeiten",self.edit_themen)
        self.pushButton_themen.setSizePolicy(SizePolicy_fixed)
        self.horizontalLayout_themen.addWidget(self.pushButton_themen)

        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.groupBox)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setEnabled(False)
        self.plainText_backup = [0, ""]
        self.reset_combobox = False
        self.gridLayout_2.addWidget(self.plainTextEdit, 2,0,1,7)

        self.buttonBox = QtWidgets.QDialogButtonBox(self.groupBox)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Open|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        buttonSave = self.buttonBox.button(QtWidgets.QDialogButtonBox.Save)
        buttonSave.setText("Änderung speichern")
        buttonSave.clicked.connect(self.save_changes)

        buttonPreview = self.buttonBox.button(QtWidgets.QDialogButtonBox.Open)
        buttonPreview.setText("Vorschau")
        buttonPreview.clicked.connect(self.open_preview)

        self.gridLayout_2.addWidget(self.buttonBox, 3, 6,1,1)
        self.gridLayout.addWidget(self.groupBox, 5, 0, 1, 5)

        self.buttonBox.setEnabled(False)

        self.comboBox.currentIndexChanged.connect(self.comboBox_index_changed)



        # self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def create_all_checkboxes_drafts(self):
        row = 0
        column = 0
        
        for dict_aufgabe in self.dict_drafts[self.typ]:
            self.add_draft_to_list(dict_aufgabe, self.scrollAreaWidgetContents, row, column)
            if column == 2:
                row += 1
                column = 0
            else:
                column +=1

        self.spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        self.gridLayout_items.addItem(self.spacerItem, row+1, 0, 1,3)
 

    def open_preview(self):
        content = self.plainTextEdit.toPlainText()

        if self.comboBox_pagebreak.currentIndex() == 0:
            pagebreak = False
        else:
            pagebreak = True
        
        file_path = os.path.join(path_localappdata_lama, "Teildokument", "preview.tex")

        rsp = create_tex(file_path, content, punkte = self.spinBox_pkt.value(), pagebreak=pagebreak)

        if rsp == True:
            create_pdf("preview")
        else:
            critical_window(
                "Die PDF Datei konnte nicht erstellt werden", detailed_text=rsp
            )

    def checkbox_clicked(self):
        chosen_list = self.get_chosen_list()

        if is_empty(chosen_list):
            on_off = False
        else:
            on_off = True
        self.pushButton_open_editor.setEnabled(on_off)
        self.pushButton_add_to_database.setEnabled(on_off)
        self.pushButton_delete.setEnabled(on_off)


    def add_draft_to_list(self, dict_aufgabe, parent, row, column):
        name = dict_aufgabe['name']

        checkbox = create_new_checkbox(parent, name)
        checkbox.clicked.connect(self.checkbox_clicked)
        # self.verticalLayout.addWidget(checkbox)
        self.gridLayout_items.addWidget(checkbox, row, column, 1,1)

        self.comboBox.addItem(name)

        self.dict_widget_variables[name]=checkbox


    def comboBox_index_changed(self):      
        if self.reset_combobox == True:
            self.reset_combobox = False
            return
        if self.comboBox.currentIndex() == 0:
            self.plainTextEdit.setEnabled(False)
            self.groupBox_pkt.setEnabled(False)
            self.groupBox_af.setEnabled(False)
            self.groupBox_klasse.setEnabled(False)
            self.groupBox_pagebreak.setEnabled(False)
            self.groupBox_abstand.setEnabled(False)
            self.groupBox_titel.setEnabled(False)
            self.groupBox_quelle.setEnabled(False)
            self.groupBox_themen.setEnabled(False)
            self.buttonBox.setEnabled(False)
            self.plainTextEdit.setPlainText("")
            self.plainText_backup = [0, ""]
            self.spinBox_pkt.setValue(0)
            self.comboBox_af.setCurrentIndex(0)
            self.comboBox_klasse.setCurrentIndex(0)
            self.comboBox_pagebreak.setCurrentIndex(0)
            self.spinBox_abstand.setValue(0)
            self.lineedit_titel.setText("")
            self.lineedit_quelle.setText("")
            self.label_themen.setText("")
            
        
        else:
            dict_aufgabe = self.get_dict_aufgabe(self.comboBox.currentText())

            if self.plainTextEdit.toPlainText() != self.plainText_backup[1]:
                rsp = question_window(
                    "Es wurden bereits Änderungen an dieser Aufgabe vorgenommen. Sind Sie sicher, dass Sie diese Änderungen unwiderruflich löschen möchten?",
                    titel="Änderungen löschen?")

                if rsp == False:
                    self.reset_combobox =True
                    self.comboBox.setCurrentIndex(self.plainText_backup[0]) 
                    return
            self.plainTextEdit.setEnabled(True)
            self.groupBox_pkt.setEnabled(True)
            self.groupBox_af.setEnabled(True)
            self.groupBox_klasse.setEnabled(True)
            self.groupBox_pagebreak.setEnabled(True)
            self.groupBox_abstand.setEnabled(True)
            self.groupBox_titel.setEnabled(True)
            self.groupBox_quelle.setEnabled(True)
            self.groupBox_themen.setEnabled(True)
            self.buttonBox.setEnabled(True)
            # try:
            if dict_aufgabe != None:
                self.label_themen.setText(str(dict_aufgabe['themen']))
                if re.search("\[.*\]", self.comboBox.currentText()) != None and self.typ == 'lama_1':
                    self.pushButton_themen.setEnabled(False)
                else:
                    self.pushButton_themen.setEnabled(True)

                self.plainTextEdit.setPlainText(dict_aufgabe['content'])
                self.plainText_backup = [self.comboBox.currentIndex(), dict_aufgabe['content']]
                self.spinBox_pkt.setValue(dict_aufgabe['punkte'])
                self.comboBox_af.setCurrentText(dict_aufgabe['af'])
                if dict_aufgabe['klasse'] == None:
                    self.comboBox_klasse.setCurrentIndex(0)
                    self.saved_klasse = None
                else:
                    self.comboBox_klasse.setCurrentText(dict_aufgabe['klasse'])
                    self.saved_klasse = int(dict_aufgabe['klasse'][1])
                if dict_aufgabe['pagebreak'] == False:
                    self.comboBox_pagebreak.setCurrentIndex(0)
                else:
                    self.comboBox_pagebreak.setCurrentIndex(1)

                self.spinBox_abstand.setValue(dict_aufgabe['abstand'])
                self.lineedit_titel.setText(dict_aufgabe['titel'])
                self.lineedit_quelle.setText(dict_aufgabe['quelle'])

            # except TypeError:
            #     print('error')
            #     pass



    def get_dict_aufgabe(self, name):
        for dict_aufgabe in self.dict_drafts[self.typ]:
            if name == dict_aufgabe['name']:
                return dict_aufgabe
        return

    def check_all(self):
        first_checkbox = list(self.dict_widget_variables.values())[0]
        if first_checkbox.isChecked() == True:
            x = False
        else:
            x = True
        for checkbox in self.dict_widget_variables.values():
            checkbox.setChecked(x)
        self.checkbox_clicked()


    def get_chosen_list(self):
        chosen_list = []
        for checkbox_name in self.dict_widget_variables:
            if self.dict_widget_variables[checkbox_name].isChecked() == True:
                chosen_list.append(checkbox_name)
        return chosen_list

    def open_editor(self):
        chosen_list = self.get_chosen_list()
        
        content = self.create_content(chosen_list)

        file_path = os.path.join(
            path_localappdata_lama, "Teildokument", "draft_preview.tex"
            ) 
        with open(file_path, "w", encoding="utf8") as file:
            file.write(tex_minimal.tex_preamble(info="info_on"))
            file.write(content)
            file.write(tex_minimal.tex_end)


        Popen(file_path, shell = True).poll()
        

    def create_content(self, chosen_list):
        content = ""
        for name in chosen_list:
            dict_aufgabe = self.get_dict_aufgabe(name)
            content = content + "\subsubsection{{{0}}}\n".format(name)
            if dict_aufgabe['pagebreak'] == False:
                begin =  tex_minimal.begin_beispiel() + "\n"
                end = tex_minimal.end_beispiel
            else:
                begin = tex_minimal.begin_beispiel_lang() + "\n"
                end = tex_minimal.end_beispiel_lang
            
            aufgabe_total = get_aufgabe_total(name, self.typ)
            info_box = create_info_box(aufgabe_total)

            content = content + begin + dict_aufgabe['content'] +end + "\n" + info_box + "\n\n\\newpage\n\n"

        return content


    def remove_from_list(self):
        chosen_list = self.get_chosen_list()
        # print(self.dict_widget_variables)
        # print(chosen_list)
        for checkbox in self.dict_widget_variables.values():
            checkbox.setParent(None)
        self.gridLayout_items.removeItem(self.spacerItem)

        self.comboBox.clear()
        self.comboBox.addItem("")

        row=0
        column=0
        for dict_aufgabe in self.dict_drafts[self.typ][:]:
            if dict_aufgabe['name'] not in chosen_list:
                self.add_draft_to_list(dict_aufgabe, self.scrollAreaWidgetContents, row, column)
                if column == 2:
                    row += 1
                    column = 0
                else:
                    column +=1
            else:
                self.dict_drafts[self.typ].remove(dict_aufgabe)
                del self.dict_widget_variables[dict_aufgabe['name']]

        self.spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_items.addItem(self.spacerItem, row+1, 0, 1,3)

    def add_to_ddb(self):
        chosen_list = self.get_chosen_list()

        rsp = question_window("Sind Sie sicher, dass Sie die folgende(n) Aufgabe(n) in die Datenbank aufnehmen möchten?\n\n{}".format("\n".join(chosen_list)))   
        if rsp == False:
            return

        internet_on = check_internet_connection()
        if internet_on == False:
            critical_window(
                "Stellen Sie sicher, dass eine Verbindung zum Internet besteht und versuchen Sie es erneut.",
                titel="Keine Internetverbindung",
            )
            return
        
        print("Checking divergencies ...")
        rsp = check_branches()
        if rsp == False:
            print("Updating database ...")
            git_reset_repo_to_origin()

        for aufgabe in chosen_list:
            update_data(aufgabe, self.typ, 'draft', False)


        self.remove_from_list()


        chosen_ddb = ["_database.json"]    
        action_push_database(True, 
        chosen_ddb,
        message="Entwürfe geprüft ({})".format(", ".join(chosen_list)),
        worker_text="Entwürfe werden in die Datenbank verschoben ..."
        )


        information_window("Die Aufgaben\n{}\nwurden erfolgreich gespeichert.".format("\n".join(chosen_list)))


    def delete_draft(self):
        chosen_list = self.get_chosen_list()
        rsp = question_window("Sind Sie sicher, dass Sie die folgende(n) Aufgabe(n) unwiderruflich löschen möchten?\n\n{}".format("\n".join(chosen_list)))
        if rsp == False:
            return

        internet_on = check_internet_connection()
        if internet_on == False:
            critical_window(
                "Stellen Sie sicher, dass eine Verbindung zum Internet besteht und versuchen Sie es erneut.",
                titel="Keine Internetverbindung",
            )
            return


        print("Checking divergencies ...")
        rsp = check_branches()
        if rsp == False:
            print("Updating database ...")
            git_reset_repo_to_origin()

        for aufgabe in chosen_list:
            delete_file(aufgabe, self.typ)

        self.remove_from_list()

        chosen_ddb = ["_database.json"]    
        action_push_database(True, 
        chosen_ddb,
        message="Entwürfe gelöscht ({})".format(", ".join(chosen_list)),
        worker_text="Entwürfe werden gelöscht ..."
        ) 

        information_window("Die Aufgaben\n{}\nwurden erfolgreich gelöscht.".format("\n".join(chosen_list)))


    def save_changes(self):

        QtWidgets.QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        name = self.comboBox.currentText()

        internet_on = check_internet_connection()
        if internet_on == False:
            QtWidgets.QApplication.restoreOverrideCursor()
            critical_window(
                "Stellen Sie sicher, dass eine Verbindung zum Internet besteht und versuchen Sie es erneut.",
                titel="Keine Internetverbindung",
            )
            return


        print("Checking divergencies ...")
        rsp = check_branches()
        if rsp == False:
            print("Updating database ...")
            git_reset_repo_to_origin()

        self.plainText_backup = [self.comboBox.currentIndex(), self.plainTextEdit.toPlainText()]

        if self.comboBox_pagebreak.currentIndex()==0:
            pagebreak = False
        else:
            pagebreak = True


        gk = name.split(" - ")[0]
        themen_auswahl = eval(self.label_themen.text())[0]

        if self.typ == 'lama_1' and gk != themen_auswahl:

            max_integer = 0
            _file_ = Query()
            table_lama = get_table(name, self.typ)


            all_files = table_lama.search(_file_.name.matches(themen_auswahl))

            for all in all_files:
                temp_name = all["name"].replace('l.','').replace('i.','')
                
                num = temp_name.split(" - ")[-1]
                num = int(num.split("[")[0])

                if num > max_integer:
                    max_integer = num

            new_name = "{0} - {1}".format(themen_auswahl, max_integer+1)
        
        else:
            new_name = name

        if self.comboBox_klasse.currentText() == "":
            klasse = None
        else:
            klasse = self.comboBox_klasse.currentText()
        dict_entries = {
            'themen':eval(self.label_themen.text()),
            'punkte':self.spinBox_pkt.value(),
            'af':self.comboBox_af.currentText(),
            'klasse':klasse,
            'pagebreak':pagebreak,
            'abstand':self.spinBox_abstand.value(),
            'quelle':self.lineedit_quelle.text(),
            'titel':self.lineedit_titel.text(),
            'content': self.plainTextEdit.toPlainText(),
            'name': new_name,
        }


        for index, aufgabe in enumerate(self.dict_drafts[self.typ]):
            if name == aufgabe['name']:
                for all in dict_entries.keys():
                    if self.dict_drafts[self.typ][index][all] != dict_entries[all]:
                        self.dict_drafts[self.typ][index][all] = dict_entries[all]
                        update_data(name, self.typ, all, dict_entries[all])
                break

        QtWidgets.QApplication.restoreOverrideCursor()
        chosen_ddb = ["_database.json"]    
        response = action_push_database(True, 
        chosen_ddb,
        message="Inhalt von {} geändert".format(name),
        worker_text="Geänderter Inhalt von {} wird gespeichert".format(name)
        )

        if response == False:
            return
        else:
            information_window("Der geänderte Inhalt von {} wurde gespeichert.".format(name))

        for all in self.dict_drafts[self.typ]:
            if all['name']==name:
                all['themen']=eval(self.label_themen.text())
                all['name']=new_name

        self.comboBox.setCurrentIndex(0)
        self.dict_widget_variables[name].setText(new_name)

        self.dict_widget_variables[new_name]=self.dict_widget_variables[name]
        del self.dict_widget_variables[name]


        # for dict_aufgabe in self.dict_drafts[self.typ]:
        #     self.comboBox.addItem(dict_aufgabe['name'])

        ### reset checkboxes
        for checkbox in self.dict_widget_variables.values():
            checkbox.setParent(None)
        self.gridLayout_items.removeItem(self.spacerItem)

        self.comboBox.clear()
        self.comboBox.addItem("")

        self.create_all_checkboxes_drafts()


    def edit_themen(self):
        Dialog = QtWidgets.QDialog(
            None,
            Qt.WindowSystemMenuHint
            | Qt.WindowTitleHint
            | Qt.WindowCloseButtonHint,
        )
        ui = Ui_Dialog_edit_themen()
        list_themen = eval(self.label_themen.text())
        try: 
            klasse =  int(self.comboBox_klasse.currentText()[1])
        except IndexError:
            klasse = None
        ui.setupUi(Dialog, list_themen, self.typ, klasse, self.changed_themen)

        rsp = Dialog.exec_()

        

        if rsp == 1:
            self.label_themen.setText(str(ui.list_themen))
            self.changed_themen = ui.changed_themen
            klasse = 1
            for all in self.changed_themen:
                temp_klasse = int(all.split(".")[0][1])
                if temp_klasse > klasse:
                    klasse = temp_klasse
         
            if self.saved_klasse == None:
                str_klasse = None
            else:
                if klasse > self.saved_klasse:
                    str_klasse = "k{}".format(klasse)
                else:
                    str_klasse = "k{}".format(self.saved_klasse)
                self.comboBox_klasse.setCurrentText(str_klasse)



class Ui_Dialog_edit_themen(object):
    def setupUi(self, Dialog, list_themen, typ, klasse, changed_themen):
        self.Dialog = Dialog
        self.list_themen = list_themen
        self.typ = typ
        self.changed_themen = changed_themen
        # self.list_klassen = []
        Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("Themen bearbeiten")
        # Dialog.setFixedSize(300, 150)
        Dialog.setWindowIcon(QIcon(logo_path))

        self.gridLayout = create_new_gridlayout(Dialog)

        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.gridLayout.addWidget(self.listWidget, 0,0,5,1)

        for all in list_themen:
            self.listWidget.addItem(all)
        # self.listWidget.itemClicked.connect(self.nummer_clicked)

        row=0
        if self.typ == 'cria':
            self.comboBox_klassen = create_new_combobox(Dialog)
            self.gridLayout.addWidget(self.comboBox_klassen, row,1,1,2)
            if self.typ == 'cria':
                for i, all in enumerate(list_klassen):
                    add_new_option(self.comboBox_klassen, i, all)
            else:
                self.comboBox_klassen.hide()
            row +=1
            

        self.comboBox_thema = create_new_combobox(Dialog)
        self.gridLayout.addWidget(self.comboBox_thema, row,1,1,2)
        
        if self.typ == 'cria':
            klasse = self.comboBox_klassen.currentText()
            dict_themen = eval("dict_{}_name".format(klasse))
            for i, all in enumerate(dict_themen.keys()):
                add_new_option(self.comboBox_thema, i, "{0} ({1})".format(all, dict_themen[all]))
        else:
            list_gk = ['AG', 'FA', 'AN', 'WS']
            for i, all in enumerate(list_gk):
                add_new_option(self.comboBox_thema, i, all)
        row+=1
        # if self.typ == 'cria':


        self.comboBox_subthema = create_new_combobox(Dialog)
        self.gridLayout.addWidget(self.comboBox_subthema, row,1,1,2)

        self.adapt_subthemen()    


        row +=1        

        if self.typ == 'cria':
            self.comboBox_klassen.currentIndexChanged.connect(self.comboBox_klassen_changed)
        self.comboBox_thema.currentIndexChanged.connect(self.comboBox_themen_changed)
        self.comboBox_subthema.currentIndexChanged.connect(self.comoBox_subthemen_changed)

        self.label_themen = create_new_label(Dialog,"")
        self.gridLayout.addWidget(self.label_themen, 3,1,1,2)

        self.pushButton_add = create_new_button(Dialog, "<<", self.add_thema)
        self.gridLayout.addWidget(self.pushButton_add, 4,1,1,1)
        self.pushButton_add.setSizePolicy(SizePolicy_fixed)
        self.pushButton_add.setShortcut("Return")

        self.pushButton_remove = create_new_button(Dialog, ">>", self.remove_thema)
        self.gridLayout.addWidget(self.pushButton_remove, 4,2,1,1)
        self.pushButton_remove.setSizePolicy(SizePolicy_fixed)
        self.pushButton_remove.setShortcut("Del")

        # self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        # self.buttonBox.setStandardButtons(
        #     QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel
        #     )
        # # self.buttonBox.setObjectName("buttonBox")
        # buttonCancel = self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel)
        # buttonCancel.setText("Abbrechen")
        # self.buttonBox.rejected.connect(Dialog.reject())
        # buttonCancel.clicked.connect(Dialog.reject())

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel
        )


        buttonS = self.buttonBox.button(QtWidgets.QDialogButtonBox.Save)
        buttonS.setText('Speichern')
        buttonX = self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel)
        buttonX.setText("Abbrechen")
        self.buttonBox.rejected.connect(self.reject_dialog)
        self.buttonBox.accepted.connect(self.save_changes)


        
        buttonSave = self.buttonBox.button(QtWidgets.QDialogButtonBox.Save)
        buttonSave.setText("Speichern")
        # buttonSave.clicked.connect(self.save_changes)

        self.gridLayout.addWidget(self.buttonBox, 5, 0,1,3)

        self.change_label()


    def comboBox_klassen_changed(self):
        if self.typ == 'cria':
            self.comboBox_thema.clear()
            klasse = self.comboBox_klassen.currentText()
            dict_themen = eval("dict_{}_name".format(klasse))
            for i, all in enumerate(dict_themen.keys()):
                add_new_option(self.comboBox_thema, i, "{0} ({1})".format(all, dict_themen[all]))       

        self.adapt_subthemen()

        self.change_label()

        # self.comboBox_themen_changed()

    def comboBox_themen_changed(self):
        self.adapt_subthemen()
        self.change_label()

    
    def comoBox_subthemen_changed(self):
        # self.label_themen.setText("")
        self.change_label()
    
    def adapt_subthemen(self):
        if is_empty(self.comboBox_thema.currentText()):
            return
        self.comboBox_subthema.clear()
        if self.typ == 'cria':
            klasse = self.comboBox_klassen.currentText()
            split = self.comboBox_thema.currentText().split(" (")
            thema = split[0]
            dict_themen = eval("dict_{0}".format(klasse))
            list_subthemen = dict_themen[thema]
            # self.comboBox_subthema.clear()
            for i, all in enumerate(list_subthemen):
                add_new_option(self.comboBox_subthema, i, "{0} ({1})".format(all, dict_unterkapitel[all]) )
        else:
            gk = self.comboBox_thema.currentText()
            i=0
            for all in dict_gk.values():
                if all.startswith(gk):
                    add_new_option(self.comboBox_subthema, i, all[-3:])
                    i+=1

    def change_label(self):
        thema = self.comboBox_thema.currentText().split(" (")[0]
        subthema  = self.comboBox_subthema.currentText().split(" (")[0]

        if self.typ == 'cria':
            self.label_themen.setText("{0}.{1}".format(thema, subthema))
        else:
            self.label_themen.setText("{0} {1}".format(thema, subthema))

    def add_thema(self):
        gk = self.label_themen.text()

        existing_items = self.listWidget.findItems(gk, Qt.MatchExactly)

        if is_empty(existing_items):
            self.listWidget.addItem(gk)
            if self.typ == 'cria':
                klasse = self.comboBox_klassen.currentText()
                thema = "{0}.{1}".format(klasse, gk)
                self.changed_themen.append(thema)
            # if self.typ == 'cria':
            #     # thema = "{0}.{1}".format(self.comboBox_klassen.currentText(), gk)
            #     # if int(self.comboBox_klassen.currentText()[1]) not in self.list_klassen:
            #     self.list_klassen.append(int(self.comboBox_klassen.currentText()[1]))

    def remove_thema(self):
        list_selected_items = self.listWidget.selectedItems()
        if not list_selected_items:
            return

        for item in list_selected_items:
            self.listWidget.takeItem(self.listWidget.row(item))
            for all in self.changed_themen[:]:
                if item.text() in all:
                    self.changed_themen.remove(all)
        
            # if self.typ == 'cria':
            #     klasse = self.comboBox_klassen.currentText()
            #     thema = "{0}.{1}".format(klasse, gk)
            #     self.changed_themen.append(thema)
        # self.listWidget.deleteItem(selected_item)??
        # self.list_klassen.remove(int(self.comboBox_klassen.currentText()[1]))



    def save_changes(self):
        list_themen = []
        for index in range(self.listWidget.count()):
            list_themen.append(self.listWidget.item(index).text())

        # self.highest_grade = max(self.list_klassen)

        if len(list_themen) == 0:
            warning_window("Es muss zumindest ein Thema/eine Grudkompetenz ausgewählt werden.")
            return
        if len(list_themen) != 1 and self.typ == 'lama_1':
            warning_window("Es kann nur eine Grundkompetenz ausgewählt werden.")
            return
        self.list_themen = list_themen
        self.Dialog.accept()


    def reject_dialog(self):
        self.Dialog.reject()

class DragDropWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
        
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    _, extension = os.path.splitext(str(url.toLocalFile()))
                    if extension.lower() == '.jpg' or extension.lower() == '.jpeg' or extension.lower() == '.png':
                        links.append(str(url.toLocalFile()))
                    else:
                        name = os.path.basename(str(url.toLocalFile()))
                        warning_window('Die Datei {} konnte nicht hinzugefügt werden.'.format(name),'Es können nur ".jpg"- oder ".png"-Dateien konvertiert werden.')

            list_added_items = get_list_of_all_items(self)
            for image in links:
                if image not in list_added_items:
                    self.addItem(image)

            if len(links) != 0:
                self.setCurrentRow(0)
                if self.currentItem().text() == 'hier ablegen ...':
                    self.takeItem(0)       
                self.setCurrentRow(-1)
        else:
            event.ignore()       


def get_list_of_all_items(listWidget):
    _list = []
    for x in range(listWidget.count()):
        _list.append(listWidget.item(x).text())
    
    return _list


class Ui_Dialog_Convert_To_Eps(object):
    def setupUi(self, Dialog, MainWindow):
        self.MainWindow = MainWindow
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        self.Dialog.setWindowIcon(QIcon(logo_path))
        # self.Dialog.resize(600,200)
        self.Dialog.setSizePolicy(SizePolicy_maximum_width)       
        Dialog.setWindowTitle("Grafik(en) konvertieren")
        self.gridLayout = create_new_gridlayout(self.Dialog)

        self.label_1 = create_new_label(Dialog, "Zu konvertierende Grafik(en) auswählen oder hier ablegen:")

        self.gridLayout.addWidget(self.label_1, 0,0,1,4)


        self.listWidget = DragDropWidget(Dialog)
        self.gridLayout.addWidget(self.listWidget, 1,0,1,4)
        self.listWidget.addItem('hier ablegen ...')
        self.listWidget.itemClicked.connect(self.remove_list_item)


        self.label_quality = create_new_label(Dialog, "Bildergrößen:")
        # self.label_quality.setSizePolicy(SizePolicy_fixed)
        self.gridLayout.addWidget(self.label_quality, 2,0,1,1)
        self.comboBox_quality = create_new_combobox(Dialog)
        add_new_option(self.comboBox_quality, 0, 'klein')
        add_new_option(self.comboBox_quality, 1, 'normal')
        add_new_option(self.comboBox_quality, 2, 'groß')
        add_new_option(self.comboBox_quality, 3, 'sehr groß')
        self.comboBox_quality.setCurrentIndex(1)
        self.gridLayout.addWidget(self.comboBox_quality, 2,1,1,1)

        # self.gridLayout.setColumnStretch(3,1)


        self.buttonBox_convert_to_eps = QtWidgets.QDialogButtonBox(self.Dialog)
        self.buttonBox_convert_to_eps.setStandardButtons(
            QtWidgets.QDialogButtonBox.Open | QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel
        )

        button_convert = self.buttonBox_convert_to_eps.button(QtWidgets.QDialogButtonBox.Open)
        button_convert.setText('Konvertieren')
        button_convert.setIcon(QIcon(get_icon_path('repeat.svg')))
        button_search = self.buttonBox_convert_to_eps.button(QtWidgets.QDialogButtonBox.Save)
        button_search.setText('Durchsuchen')
        button_search.setIcon(QIcon(get_icon_path('folder.svg')))
        button_cancel = self.buttonBox_convert_to_eps.button(QtWidgets.QDialogButtonBox.Cancel)
        button_cancel.setText('Abbrechen')
        button_cancel.setIcon(QIcon(get_icon_path('x.svg')))        

        button_search.clicked.connect(lambda: self.search_pressed())
        button_convert.clicked.connect(lambda: self.convert_pressed())
        button_cancel.clicked.connect(self.Dialog.reject)


        self.gridLayout.addWidget(self.buttonBox_convert_to_eps, 2,3,1,1)

    def remove_list_item(self, item):
        if item.text() != 'hier ablegen ...':
            self.listWidget.takeItem(self.listWidget.row(item))

    # def get_list_of_all_items(self, listWidget):
    #     _list = []
    #     for x in range(self.listWidget.count()):
    #         _list.append(self.listWidget.item(x).text())
        
    #     return _list
    @report_exceptions
    def search_pressed(self):
        try:
            os.path.dirname(self.MainWindow.saved_file_path)
        except AttributeError:
            self.MainWindow.saved_file_path = path_home

        filename = QtWidgets.QFileDialog.getOpenFileNames(
            None,
            "Select a folder:",
            os.path.dirname(self.MainWindow.saved_file_path),
            "Bilder (*.jpg; *.jpeg; *.png; *.jfif);; Alle Dateien (*.*)",
        )

        if filename[0] == []:
            return
        else:
            self.listWidget.setCurrentRow(0)
            if self.listWidget.currentItem().text() == 'hier ablegen ...':
                self.listWidget.takeItem(0)
            list_added_items = get_list_of_all_items(self.listWidget)
            for image in filename[0]:
                if image not in list_added_items:
                    self.listWidget.addItem(image)
            # self.listWidget.addItems(filename[0])
            self.listWidget.setCurrentRow(-1)

    @report_exceptions
    def convert_pressed(self):
        item_list = get_list_of_all_items(self.listWidget)

        if item_list[0] == 'hier ablegen ...':
            warning_window('Es wurde keine Grafik zum Konvertieren ausgewählt.')
            return
        # for item in range(self.listWidget.count()):
        #     item_list.append(self.listWidget.item(item).text())

        self.MainWindow.saved_file_path = item_list[0]
        QtWidgets.QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        for image in item_list:
            response = convert_image_to_eps(image, self.comboBox_quality.currentIndex())
            if response != True:
                break
        QtWidgets.QApplication.restoreOverrideCursor()
        if response == True:
            if len(item_list) == 1:
                text = "wurde {} Datei".format(len(item_list))
            else:
                text = "wurden {} Dateien".format(len(item_list))

            information_window(
                "Es {0} erfolgreich konvertiert.".format(text),
                titel="Grafik(en) erfolgreich konvertiert",
                detailed_text="Konvertierte Grafik(en):\n{}".format(
                    "\n".join(item_list)
                ),
            )
        else:
            critical_window(
                "Beim Konvertieren der folgenden Grafik ist ein Fehler aufgetreten:\n\n{}".format(
                    image
                ),
                titel="Fehler beim Konvertieren",
                detailed_text='Fehlermeldung:\n\n"{0}: {1}"'.format(
                    type(response).__name__, response
                ),
            )
        self.listWidget.clear()
        self.listWidget.addItem('hier ablegen ...')
        # self.Dialog.accept()  


class Ui_Dialog_edit_single_instructions(object):
    def setupUi(self, Dialog, text):
        # self.MainWindow = MainWindow
        # self.Dialog = Dialog
        # self.Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("Layout des Arbeitsblatts")
        Dialog.setWindowIcon(QIcon(logo_path)) 
        Dialog.resize(300,50)

        verticalLayout = create_new_verticallayout(Dialog)

        widget_titel = QtWidgets.QWidget(Dialog)
        verticalLayout.addWidget(widget_titel)
        self.horizontallayout_titel = create_new_horizontallayout(widget_titel)
        self.horizontallayout_titel.setContentsMargins(0,0,0,0)

        # if show_titel == False:
        #     check_title = False
        # else:
        #     check_title = True
        # self.checkbox_titel = create_new_checkbox(widget_titel, "Titel:", checked=check_title)
        # self.horizontallayout_titel.addWidget(self.checkbox_titel)
        # self.checkbox_titel.stateChanged.connect(self.enable_title)

        
        # self.lineedit_titel = create_new_lineedit(widget_titel, "")
        # if show_titel != False:
        #     self.lineedit_titel.setText(show_titel)
            
        # self.horizontallayout_titel.addWidget(self.lineedit_titel)


        # self.checkBox_hide_instructions = create_new_checkbox(Dialog, "Arbeitsanweisung anzeigen", show_instructions)
        
        # verticalLayout.addWidget(self.checkBox_hide_instructions)

        self.plainTextEdit_instructions = QtWidgets.QPlainTextEdit()
        self.plainTextEdit_instructions.setPlainText(text)
        # if show_instructions==False: 
        #     self.plainTextEdit_instructions.setEnabled(False)
        verticalLayout.addWidget(self.plainTextEdit_instructions)

        # self.checkBox_hide_instructions.stateChanged.connect(self.enable_instructions)

        # self.checkbox_fortlaufende_nummerierung = create_new_checkbox(Dialog, "Aufgaben fortlaufend nummerieren", checked=fortlaufende_nummerierung)
        # verticalLayout.addWidget(self.checkbox_fortlaufende_nummerierung)

        # self.checkBox_show_pagenumbers = create_new_checkbox(Dialog, "Seitennummerierung anzeigen", show_pagenumbers)
        # verticalLayout.addWidget(self.checkBox_show_pagenumbers)

        # self.widget_number_columns_solution = QtWidgets.QWidget(Dialog)
        # verticalLayout.addWidget(self.widget_number_columns_solution)
        # horizontallayout_number_columns = create_new_horizontallayout(self.widget_number_columns_solution)
        # horizontallayout_number_columns.setContentsMargins(0,0,0,0)

        # label_number_columns = create_new_label(self.widget_number_columns_solution, "Lösungen: Spaltenanzahl")
        # horizontallayout_number_columns.addWidget(label_number_columns)

        # # label_number_columns_icon = create_new_label(self.widget_number_columns_solution, " ")
        # # label_number_columns_icon.setPixmap(QPixmap(get_icon_path("columns.svg")))
        # # label_number_columns_icon.setFixedSize(QSize(20,20))
        # # label_number_columns_icon.setScaledContents(True)
        # # horizontallayout_number_columns.addWidget(label_number_columns_icon)

        # self.spinbox_number_columns = create_new_spinbox(self.widget_number_columns_solution, columns)
        # self.spinbox_number_columns.setRange(1,5)
        # horizontallayout_number_columns.addWidget(self.spinbox_number_columns)

        # horizontallayout_number_columns.addStretch()

        # widget_item_spacing = QtWidgets.QWidget(Dialog)
        # verticalLayout.addWidget(widget_item_spacing)
        # horizontallayout_item_spacing = create_new_horizontallayout(widget_item_spacing)
        # horizontallayout_item_spacing.setContentsMargins(0,0,0,0)

        # label_item_spacing = create_new_label(widget_item_spacing, "Abstand zwischen den Aufgaben:")
        # horizontallayout_item_spacing.addWidget(label_item_spacing)

        # self.spinbox_item_spacing = QtWidgets.QDoubleSpinBox(widget_item_spacing)
        # self.spinbox_item_spacing.setValue(item_spacing)
        # self.spinbox_item_spacing.setSuffix(" cm")
        # horizontallayout_item_spacing.addWidget(self.spinbox_item_spacing)

        # horizontallayout_item_spacing.addStretch()

        buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        verticalLayout.addWidget(buttonBox)
    # self.gridLayout_wizard.addWidget(self.buttonBox_create_worksheet_wizard, 10,1,1,2)
    # self.buttonBox_create_worksheet_wizard.hide()
        # buttonOk.setIcon(QtGui.QIcon(get_icon_path('eye.svg')))
        # button.setText("Vorschau")

        buttonCancel = buttonBox.button(QtWidgets.QDialogButtonBox.Cancel)
        buttonCancel.setText("Abbrechen")
        
        
        buttonBox.rejected.connect(Dialog.reject)
        buttonBox.accepted.connect(Dialog.accept)


class Ui_Dialog_edit_worksheet_instructions(object):
    def setupUi(self, Dialog, text, show_titel, show_instructions,fortlaufende_nummerierung , show_pagenumbers, columns, item_spacing):
        # self.MainWindow = MainWindow
        # self.Dialog = Dialog
        # self.Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("Layout des Arbeitsblatts")
        Dialog.setWindowIcon(QIcon(logo_path)) 
        Dialog.resize(300,50)

        verticalLayout = create_new_verticallayout(Dialog)

        widget_titel = QtWidgets.QWidget(Dialog)
        verticalLayout.addWidget(widget_titel)
        self.horizontallayout_titel = create_new_horizontallayout(widget_titel)
        self.horizontallayout_titel.setContentsMargins(0,0,0,0)

        if show_titel == False:
            check_title = False
        else:
            check_title = True
        self.checkbox_titel = create_new_checkbox(widget_titel, "Titel:", checked=check_title)
        self.horizontallayout_titel.addWidget(self.checkbox_titel)
        self.checkbox_titel.stateChanged.connect(self.enable_title)

        
        self.lineedit_titel = create_new_lineedit(widget_titel, "")
        if show_titel != False:
            self.lineedit_titel.setText(show_titel)
            
        self.horizontallayout_titel.addWidget(self.lineedit_titel)


        self.checkBox_hide_instructions = create_new_checkbox(Dialog, "Arbeitsanweisung am Beginn anzeigen", show_instructions)
        
        verticalLayout.addWidget(self.checkBox_hide_instructions)

        self.plainTextEdit_instructions = QtWidgets.QPlainTextEdit()
        self.plainTextEdit_instructions.setPlainText(text)
        if show_instructions==False: 
            self.plainTextEdit_instructions.setEnabled(False)
        verticalLayout.addWidget(self.plainTextEdit_instructions)

        self.checkBox_hide_instructions.stateChanged.connect(self.enable_instructions)

        self.checkbox_fortlaufende_nummerierung = create_new_checkbox(Dialog, "Aufgaben fortlaufend nummerieren", checked=fortlaufende_nummerierung)
        verticalLayout.addWidget(self.checkbox_fortlaufende_nummerierung)

        self.checkBox_show_pagenumbers = create_new_checkbox(Dialog, "Seitennummerierung anzeigen", show_pagenumbers)
        verticalLayout.addWidget(self.checkBox_show_pagenumbers)

        self.widget_number_columns_solution = QtWidgets.QWidget(Dialog)
        verticalLayout.addWidget(self.widget_number_columns_solution)
        horizontallayout_number_columns = create_new_horizontallayout(self.widget_number_columns_solution)
        horizontallayout_number_columns.setContentsMargins(0,0,0,0)

        label_number_columns = create_new_label(self.widget_number_columns_solution, "Lösungen: Spaltenanzahl")
        horizontallayout_number_columns.addWidget(label_number_columns)

        # label_number_columns_icon = create_new_label(self.widget_number_columns_solution, " ")
        # label_number_columns_icon.setPixmap(QPixmap(get_icon_path("columns.svg")))
        # label_number_columns_icon.setFixedSize(QSize(20,20))
        # label_number_columns_icon.setScaledContents(True)
        # horizontallayout_number_columns.addWidget(label_number_columns_icon)

        self.spinbox_number_columns = create_new_spinbox(self.widget_number_columns_solution, columns)
        self.spinbox_number_columns.setRange(1,5)
        horizontallayout_number_columns.addWidget(self.spinbox_number_columns)

        horizontallayout_number_columns.addStretch()

        widget_item_spacing = QtWidgets.QWidget(Dialog)
        verticalLayout.addWidget(widget_item_spacing)
        horizontallayout_item_spacing = create_new_horizontallayout(widget_item_spacing)
        horizontallayout_item_spacing.setContentsMargins(0,0,0,0)

        label_item_spacing = create_new_label(widget_item_spacing, "Abstand zwischen den Aufgaben:")
        horizontallayout_item_spacing.addWidget(label_item_spacing)

        self.spinbox_item_spacing = QtWidgets.QDoubleSpinBox(widget_item_spacing)
        self.spinbox_item_spacing.setValue(item_spacing)
        self.spinbox_item_spacing.setSuffix(" cm")
        horizontallayout_item_spacing.addWidget(self.spinbox_item_spacing)

        horizontallayout_item_spacing.addStretch()

        buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        verticalLayout.addWidget(buttonBox)
    # self.gridLayout_wizard.addWidget(self.buttonBox_create_worksheet_wizard, 10,1,1,2)
    # self.buttonBox_create_worksheet_wizard.hide()
        # buttonOk.setIcon(QtGui.QIcon(get_icon_path('eye.svg')))
        # button.setText("Vorschau")

        buttonCancel = buttonBox.button(QtWidgets.QDialogButtonBox.Cancel)
        buttonCancel.setText("Abbrechen")
        
        
        buttonBox.rejected.connect(Dialog.reject)
        buttonBox.accepted.connect(Dialog.accept)
    
        # self.buttonBox_setup.accepted.connect(partial(self.save_setting, MainWindow.chosen_program))
        # button_save.setIcon(QtGui.QIcon(get_icon_path('save.svg')))
        # button_save.setText("Speichern")

    def enable_title(self):
        if self.checkbox_titel.isChecked():
            self.lineedit_titel.setEnabled(True)
        else:
            self.lineedit_titel.setEnabled(False)

    def enable_instructions(self):
        if self.checkBox_hide_instructions.isChecked():
            self.plainTextEdit_instructions.setEnabled(True)
        else:
            self.plainTextEdit_instructions.setEnabled(False)      

class Ui_Dialog_import_sage(object):
    def setupUi(self, Dialog):
        Dialog.setWindowTitle("Aufgabenliste importieren")
        Dialog.setWindowIcon(QIcon(logo_path)) 
        Dialog.resize(80,300)
        self.Dialog = Dialog
        verticalLayout = create_new_verticallayout(Dialog)

        # self.tableWidget = QtWidgets.QTableWidget(Dialog)
        # self.tableWidget.setRowCount(4)
        # self.tableWidget.setColumnCount(1)
        # verticalLayout.addWidget(self.tableWidget)
        label = create_new_label(Dialog, "Import der Aufgabenummern")
        verticalLayout.addWidget(label)

        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit.setToolTip("Jede Aufgabenummer muss in eine neue Zeile eingefügt werden")
        verticalLayout.addWidget(self.plainTextEdit)

        btn_import = create_new_button(Dialog, "Importieren", self.btn_import_clicked, icon="plus-square.svg")
        verticalLayout.addWidget(btn_import)

    def btn_import_clicked(self):
       
        self.list_of_tasks = self.plainTextEdit.toPlainText().split('\n')
        self.list_of_tasks = [x for x in self.list_of_tasks if x]
        self.Dialog.accept()
        