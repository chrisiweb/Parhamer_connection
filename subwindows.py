# from Admin_LaMA_Check import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon, QCursor, QTextCursor
from PyQt5.QtCore import Qt, QSize, QRect, QMetaObject, QCoreApplication, QThread
import os
import shutil
from json import load, dump
import re
from string import ascii_lowercase
from functools import partial
from config_start import path_programm,path_localappdata_lama, lama_settings_file, lama_developer_credentials
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
    still_to_define,
)
from subprocess import Popen
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
# from waitingspinnerwidget import QtWaitingSpinner
from predefined_size_policy import SizePolicy_fixed, SizePolicy_fixed_height, SizePolicy_maximum
from work_with_content import prepare_content_for_hide_show_items
from lama_stylesheets import (
    StyleSheet_tabWidget,
    StyleSheet_ausgleichspunkte,
    StyleSheet_ausgleichspunkte_dark_mode,
    StyleSheet_subwindow_ausgleichspunkte,
    StyleSheet_subwindow_ausgleichspunkte_dark_mode,
)
from create_pdf import create_tex, create_pdf, check_if_variation
import tex_minimal
from processing_window import Ui_Dialog_processing
import bcrypt
from database_commands import _database, _local_database, _database_addon, get_table, update_data, delete_file 
from filter_commands import get_filter_string, filter_items
from sort_items import order_gesammeltedateien
from upload_database import action_push_database
from tinydb import Query
from git_sync import check_branches, git_reset_repo_to_origin

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



class Ui_Dialog_Welcome_Window(object):
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")        
        Dialog.setWindowTitle("Herzlich Willkommen bei LaMA")
        self.gridLayout = create_new_gridlayout(self.Dialog)

        self.label_1 = create_new_label(Dialog, """
Herlich Willkommen!

Es freut uns sehr, dass Sie sich für das Programm LaMA interessieren!
Um starten zu können, muss LaMA zu Beginn konfiguriert werden. Dazu muss die Aufgabendatenbank heruntergeladen werden.

Möchten Sie die Konfiguration beginnen und die Datenbank herunterladen?
        """)

        self.gridLayout.addWidget(self.label_1, 0,0,1,1)

        self.buttonBox_welcome = QtWidgets.QDialogButtonBox(self.Dialog)
        self.buttonBox_welcome.setStandardButtons(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )

        # buttonS = self.buttonBox_titlepage.button(QtWidgets.QDialogButtonBox.Save)
        # buttonS.setText('Speichern')
        buttonX = self.buttonBox_welcome.button(QtWidgets.QDialogButtonBox.Cancel)
        buttonX.setText("Abbrechen")
        self.buttonBox_welcome.setObjectName("buttonBox_variation")
        self.buttonBox_welcome.rejected.connect(self.cancel_pressed)
        self.buttonBox_welcome.accepted.connect(self.start_download)

        self.gridLayout.addWidget(self.buttonBox_welcome, 1,0,1,1)

    def cancel_pressed(self):
        self.Dialog.reject()

    def start_download(self):
        self.Dialog.accept()      

class Ui_Dialog_choose_type(object):
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle(
            _translate("Titelplatt anpassen", "Programm auswählen", None)
        )
        Dialog.setWindowIcon(QIcon(logo_path))

        # Dialog.setStyleSheet("QToolTip { color: white; background-color: rgb(47, 69, 80); border: 0px; }")
        Dialog.setSizePolicy(SizePolicy_fixed)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")

        self.btn_lama_cria = QtWidgets.QPushButton()
        self.btn_lama_cria.setObjectName(_fromUtf8("btn_lama_cria"))
        # self.btn_lama_cria.setText("LaMA Cria (Unterstufe)")
        self.btn_lama_cria.setIcon(QIcon(logo_cria_button_path))
        self.btn_lama_cria.setIconSize(QSize(120, 120))
        self.btn_lama_cria.setFixedSize(120, 120)
        self.btn_lama_cria.setStyleSheet(
            _fromUtf8("background-color: rgb(63, 169, 245);")
        )
        self.btn_lama_cria.setAutoDefault(False)
        self.btn_lama_cria.setShortcut("F1")
        self.gridLayout.addWidget(self.btn_lama_cria, 0, 0, 1, 1, Qt.AlignCenter)
        self.label_lama_cria = QtWidgets.QLabel()
        self.label_lama_cria.setObjectName(_fromUtf8("label_lama_cria"))
        self.label_lama_cria.setText("LaMA Cria (Unterstufe)")
        self.gridLayout.addWidget(
            self.label_lama_cria, 1, 0, 1, 1, Qt.AlignCenter
        )
        # self.btn_lama_cria.setMaximumWidth(130)
        self.btn_lama_cria.clicked.connect(partial(self.choose_button_pressed, "cria"))

        self.btn_lama = QtWidgets.QPushButton()
        self.btn_lama.setObjectName(_fromUtf8("btn_lama"))
        # self.btn_lama.setText("LaMA (Oberstufe)")
        self.btn_lama.setIcon(QIcon(logo_path))
        self.btn_lama.setIconSize(QSize(120, 120))
        self.btn_lama.setShortcut("F2")
        self.btn_lama.setFixedSize(120, 120)
        self.btn_lama.setAutoDefault(False)
        self.gridLayout.addWidget(self.btn_lama, 0, 1, 1, 1, Qt.AlignCenter)
        self.btn_lama.clicked.connect(partial(self.choose_button_pressed, "lama"))
        self.label_lama = QtWidgets.QLabel()
        self.label_lama.setObjectName(_fromUtf8("label_lama"))
        self.label_lama.setText("LaMA (Oberstufe)")
        self.gridLayout.addWidget(self.label_lama, 1, 1, 1, 1, Qt.AlignCenter)

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
            # self.comboBox_gk.addItem("")
            index = 0
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
        elif self.MainWindow.chosen_program == "cria":
            self.comboBox_klassen.setCurrentIndex(
                self.MainWindow.tab_widget_cr_cria.currentIndex()
            )

    def cancel_pressed(self):
        self.Dialog.reject()

    def choose_example(self):
        try:
            if self.listWidget.selectedItems()[0].text() == self.no_choice:
                self.chosen_variation = None
            elif self.MainWindow.chosen_program == "cria":
                klasse = list_klassen[self.comboBox_klassen.currentIndex()]
                self.chosen_variation = (
                    klasse + "." + self.listWidget.selectedItems()[0].text()
                )
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
            "dict_{}_name".format(list_klassen[self.comboBox_klassen.currentIndex()])
        )
        self.comboBox_kapitel.clear()
        self.comboBox_unterkapitel.clear()
        self.comboBox_kapitel.addItem("")

        for all in dict_klasse_name.keys():
            self.comboBox_kapitel.addItem(dict_klasse_name[all] + " (" + all + ")")

    def comboBox_kapitel_changed(self):
        dict_klasse = eval(
            "dict_{}".format(list_klassen[self.comboBox_klassen.currentIndex()])
        )

        dict_klasse = eval(
            "dict_{}".format(list_klassen[self.comboBox_klassen.currentIndex()])
        )
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
            if typ == "cria":
                name = _file_["name"].split(".")[-1]
            else:
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

    def adapt_choosing_list(self):
        QtWidgets.QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        chosen_program = self.MainWindow.chosen_program
        klasse = None
        if chosen_program == "cria":
            typ = "cria"
            klasse = list_klassen[self.comboBox_klassen.currentIndex()]
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
        all_filtered_items = []
        for database in _list_database:
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
                self, table_lama, typ, 'creator', filter_string, line_entry,klasse
            )

            all_filtered_items = all_filtered_items + filtered_items
        
        all_filtered_items.sort(key=order_gesammeltedateien)

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
    def setupUi(self, Dialog, dict_titlepage):

        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle(
            _translate("Titelplatt anpassen", "Titelplatt anpassen", None)
        )
        # self.Dialog.resize(600, 400)
        # self.Dialog.setWindowIcon(QIcon(logo_path))
        # Dialog.setObjectName("Dialog")
        # Dialog.resize(468, 208)
        Dialog.setWindowIcon(QIcon(logo_path))
        self.verticalLayout_titlepage = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_titlepage.setObjectName("verticalLayout_titlepage")

        self.groupBox_titlepage = QtWidgets.QGroupBox()
        self.groupBox_titlepage.setObjectName("groupBox_titlepage")
        self.verticalLayout_gBtitlepage = QtWidgets.QVBoxLayout(self.groupBox_titlepage)
        self.verticalLayout_gBtitlepage.setObjectName("verticalLayout_gBtitlepage")
        self.groupBox_titlepage.setTitle(
            _translate("MainWindow", "Gewünschte Anzeige am Titelblatt", None)
        )
        self.verticalLayout_titlepage.addWidget(self.groupBox_titlepage)

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
        if dict_titlepage["logo_path"] != False:
            logo_name = os.path.basename(dict_titlepage["logo_path"])
            self.cb_titlepage_logo.setText("Logo ({})".format(logo_name))
        self.cb_titlepage_logo.setObjectName(_fromUtf8("cb_titlepage_logo"))
        self.verticalLayout_gBtitlepage.addWidget(self.cb_titlepage_logo)
        self.cb_titlepage_logo.setChecked(dict_titlepage["logo"])

        self.btn_titlepage_logo_path = QtWidgets.QPushButton()
        self.btn_titlepage_logo_path.setObjectName(_fromUtf8("btn_titlepage_logo_path"))
        self.verticalLayout_gBtitlepage.addWidget(self.btn_titlepage_logo_path)
        self.btn_titlepage_logo_path.setText("Durchsuchen")
        self.btn_titlepage_logo_path.setMaximumWidth(130)
        self.btn_titlepage_logo_path.clicked.connect(
            partial(self.btn_titlepage_logo_path_pressed, dict_titlepage)
        )

        self.cb_titlepage_titel = QtWidgets.QCheckBox("Titel")
        self.cb_titlepage_titel.setObjectName(_fromUtf8("cb_titlepage_titel"))
        self.verticalLayout_gBtitlepage.addWidget(self.cb_titlepage_titel)
        self.cb_titlepage_titel.setChecked(dict_titlepage["titel"])

        self.cb_titlepage_datum = QtWidgets.QCheckBox("Datum")
        self.cb_titlepage_datum.setObjectName(_fromUtf8("cb_titlepage_datum"))
        self.verticalLayout_gBtitlepage.addWidget(self.cb_titlepage_datum)
        self.cb_titlepage_datum.setChecked(dict_titlepage["datum"])

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

    def cb_titlepage_hide_all_pressed(self):
        if self.cb_titlepage_hide_all.isChecked() == True:
            self.groupBox_titlepage.setEnabled(False)
        if self.cb_titlepage_hide_all.isChecked() == False:
            self.groupBox_titlepage.setEnabled(True)

    def btn_titlepage_logo_path_pressed(self, dict_titlepage):
        logo_titlepage_path = QtWidgets.QFileDialog.getOpenFileNames(
            None, "Grafiken wählen", path_programm, "Grafiken (*.eps)"
        )
        if logo_titlepage_path[0] == []:
            return

        logo_name = os.path.basename(logo_titlepage_path[0][0])

        self.cb_titlepage_logo.setText("Logo ({})".format(logo_name))
        dict_titlepage["logo_path"] = "{}".format(logo_titlepage_path[0][0])
        copy_logo_titlepage_path = os.path.join(
            path_localappdata_lama, "Teildokument", logo_name
        )
        try:
            shutil.copy(logo_titlepage_path[0][0], copy_logo_titlepage_path)
        except shutil.SameFileError:
            pass

        return dict_titlepage

    def save_titlepage(self, dict_titlepage):
        for all in dict_titlepage.keys():
            if all == "logo_path":
                if self.cb_titlepage_logo.isChecked() and dict_titlepage[all] == False:
                    critical_window(
                        "Bitte geben Sie den Dateipfad eines Logos an oder wählen Sie das Logo auf der Titelseite ab.",
                        titel="Kein Logo ausgewählt",
                    )

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
            "hide_all": False,
        }
        for all in dict_titlepage.keys():
            if all == "logo_path":
                continue
            checkbox = eval("self.cb_titlepage_{}".format(all))
            checkbox.setChecked(dict_titlepage[all])

        return dict_titlepage


class Ui_Dialog_ausgleichspunkte(object):
    def setupUi(
        self,
        Dialog,
        aufgabe,
        typ,
        content,
        aufgabenstellung_split_text,
        list_sage_ausgleichspunkte_chosen,
        list_sage_hide_show_items_chosen,
        sage_individual_change,
        display_mode
    ):
        self.content = content
        self.sage_individual_change = sage_individual_change
        self.typ = typ
        if typ==2:
            self.aufgabenstellung_split_text = aufgabenstellung_split_text
            self.hide_show_items_split_text = prepare_content_for_hide_show_items(
                aufgabenstellung_split_text
            )
            self.list_sage_ausgleichspunkte_chosen = list_sage_ausgleichspunkte_chosen
            self.list_sage_hide_show_items_chosen = list_sage_hide_show_items_chosen
            # print(sage_individual_change)
            self.dict_widget_variables_ausgleichspunkte = {}
            self.dict_widget_variables_hide_show_items = {}

        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        self.Dialog.setWindowTitle("Aufgabe bearbeiten")
        self.Dialog.resize(600, 400)
        self.Dialog.setWindowIcon(QIcon(logo_path))

        self.gridlayout_titlepage = create_new_gridlayout(Dialog)
        # self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        # self.gridLayout_2.setObjectName("gridLayout_2")
        self.combobox_edit = create_new_combobox(Dialog)
        self.combobox_edit.setSizePolicy(SizePolicy_fixed)
        if typ == 2:
            self.gridlayout_titlepage.addWidget(self.combobox_edit, 0,0,1,5)
        else:
            self.gridlayout_titlepage.addWidget(self.combobox_edit, 0,0,1,4)

        # self.gridlayout_titlepage.setColumnStretch(1,0)
        # self.gridlayout_titlepage.addItem(QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum),0,3,1,1)
        if typ == 2:
            self.combobox_edit.addItem("Ausgleichspunkte anpassen")
            self.combobox_edit.addItem("Aufgabenstellungen ein-/ausblenden")
        self.combobox_edit.addItem("Individuell bearbeiten")
        if typ !=2:
            self.combobox_edit.setEnabled(False)
            # self.combobox_edit.setStyleSheet("color: black")

        if typ ==2:
            self.combobox_edit.currentIndexChanged.connect(self.combobox_edit_changed)
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
        self.plainTextEdit_content.textChanged.connect(self.plainTextEdit_content_changed)
        self.plainTextEdit_content.setUndoRedoEnabled(False)
        if self.sage_individual_change != None:
            self.plainTextEdit_content.insertPlainText(self.sage_individual_change)
        else:
            self.plainTextEdit_content.insertPlainText(self.content)
        self.plainTextEdit_content.moveCursor(QTextCursor.Start)
        self.plainTextEdit_content.ensureCursorVisible()
        # self.plainTextEdit_content_changed.verticalScrollBar().setValue(0)
        self.gridlayout_titlepage.addWidget(self.plainTextEdit_content, 1,0,1,6)
        self.plainTextEdit_content.setUndoRedoEnabled(True)
        if typ == 2:
            self.plainTextEdit_content.hide()


        self.button_preview = create_new_button(Dialog, "Vorschau", self.button_preview_pressed)
        self.button_preview.setSizePolicy(SizePolicy_maximum)
        self.button_preview.setShortcut("Ctrl+Return")
        self.button_preview.setToolTip("Strg+Enter")
        self.gridlayout_titlepage.addWidget(self.button_preview, 3, 0, 1,1)
        if typ ==2:
            self.button_preview.hide()

        self.button_restore_default = create_new_button(Dialog, "Original wiederherstellen", self.button_restore_default_pressed)
        self.button_restore_default.setSizePolicy(SizePolicy_maximum)
        self.gridlayout_titlepage.addWidget(self.button_restore_default, 3,1,1,1)
        if typ ==2:
            self.button_restore_default.hide()

        self.button_save = create_new_button(Dialog, "Als Variation speichern", self.button_save_pressed)
        self.button_save.setSizePolicy(SizePolicy_maximum)
        self.gridlayout_titlepage.addWidget(self.button_save, 3, 2, 1,1)
        ### Variationsbutton ausblenden, da derzeit nicht funktionsfähig
        self.button_save.hide()
        if typ ==2:
            self.button_save.hide()



        self.button_OK = create_new_button(Dialog, "OK", self.pushButton_OK_pressed)
        self.button_OK.setSizePolicy(SizePolicy_maximum)
        self.gridlayout_titlepage.addWidget(self.button_OK, 3,4,1,1)

        self.button_cancel = create_new_button(Dialog, "Abbrechen", Dialog.reject)
        self.button_cancel.setSizePolicy(SizePolicy_maximum)
        self.gridlayout_titlepage.addWidget(self.button_cancel, 3,5,1,1)



        path_undo = os.path.join(path_programm, "_database", "_config", "icon", "undo-arrow.png")
        # self.button_undo = create_standard_button(Dialog, "", still_to_define,QIcon(path_undo))
        self.button_undo = create_new_button(Dialog, "", self.button_undo_pressed)
        self.button_undo.setIcon(QIcon(path_undo))
        self.button_undo.setSizePolicy(SizePolicy_maximum)
        self.button_undo.setToolTip("Rückgängig (Strg+Z)")
        self.button_undo.setShortcut("Ctrl+Z")
        self.gridlayout_titlepage.addWidget(self.button_undo, 0,4,1,1, Qt.AlignLeft)



        path_redo = os.path.join(path_programm, "_database", "_config", "icon", "redo-arrow.png")
        # self.button_undo = create_standard_button(Dialog, "", still_to_define,QIcon(path_undo))
        self.button_redo = create_new_button(Dialog, "", self.button_redo_pressed)
        self.button_redo.setIcon(QIcon(path_redo))
        self.button_redo.setSizePolicy(SizePolicy_maximum)
        self.button_redo.setToolTip("Wiederherstellen (Strg+Y)")
        self.button_redo.setShortcut("Ctrl+Y")
        # self.button_redo = create_standard_button(Dialog, "", still_to_define,QtWidgets.QStyle.SP_ArrowForward)
        self.gridlayout_titlepage.addWidget(self.button_redo, 0,4,1,1, Qt.AlignRight)

       

        
        path_zoom_in = os.path.join(path_programm, "_database", "_config", "icon", "zoom-in.png")
        self.button_zoom_in = create_new_button(Dialog, "", self.plainTextEdit_content.zoomIn)
        self.button_zoom_in.setIcon(QIcon(path_zoom_in))
        self.button_zoom_in.setSizePolicy(SizePolicy_maximum)
        self.gridlayout_titlepage.addWidget(self.button_zoom_in,0,5,1,1, Qt.AlignLeft)
        self.button_zoom_in.setShortcut("Ctrl++")
        

        path_zoom_out = os.path.join(path_programm, "_database", "_config", "icon", "zoom-out.png")
        self.button_zoom_out = create_new_button(Dialog, "", self.plainTextEdit_content.zoomOut)
        self.button_zoom_out.setIcon(QIcon(path_zoom_out))
        self.button_zoom_out.setSizePolicy(SizePolicy_maximum)
        self.gridlayout_titlepage.addWidget(self.button_zoom_out,0,5,1,1, Qt.AlignRight)
        self.button_zoom_out.setShortcut("Ctrl+-")
        

        if typ==2:        
            self.button_undo.hide()
            self.button_redo.hide()
            self.button_zoom_in.hide()
            self.button_zoom_out.hide()

        self.change_detected_0 = False
        self.change_detected_1 = False
        self.change_detected_2 = False
        QMetaObject.connectSlotsByName(self.Dialog)

        if typ == 2:
            if not is_empty(list_sage_hide_show_items_chosen):
                self.combobox_edit.setCurrentIndex(1)
            elif sage_individual_change != None:
                self.combobox_edit.setCurrentIndex(2)

    def change_detected_warning(self):
        response = question_window("Es wurden bereits nicht gespeicherte Änderungen an der Aufgabe vorgenommen.",
        "Sind Sie sicher, dass Sie diese Änderungen verwerfen wollen?","Änderung der Aufgabe")
        return response

    def check_for_change(self):
        for index in [0,1,2]:
            change_detected = eval("self.change_detected_{}".format(index))
            if change_detected == True:  
                return index

                # rsp = self.change_detected_warning()
                # if rsp == False:
                #     self.combobox_edit.setCurrentIndex(index)
                #     return rsp
                # else:
                #     change_detected = False  
                #     return rsp          
        # _list = [0,1,2]
        # _list.remove(index)
        # print(_list)
        # print(index)

    def combobox_edit_changed(self):
        index = self.check_for_change()
        if index != None:
            if index != self.combobox_edit.currentIndex():
                response = self.change_detected_warning()
                if response == False:
                    self.combobox_edit.setCurrentIndex(index)
                    return
                else:
                    if index == 2:
                        self.plainTextEdit_content.clear()
                        self.plainTextEdit_content.insertPlainText(self.content)  
                    self.change_detected_0=False
                    self.change_detected_1=False
                    self.change_detected_2=False
            else:
                return

        for i in reversed(range(1, self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)
        if self.combobox_edit.currentIndex() == 0 or self.combobox_edit.currentIndex() == 1:

            self.gridlayout_titlepage.addWidget(self.combobox_edit, 0,0,1,5)
            self.button_undo.hide()
            self.button_redo.hide()
            self.scrollArea.show()
            self.plainTextEdit_content.hide()
            self.build_checkboxes_for_content()
            self.button_save.hide()
            self.button_preview.hide()
            self.button_restore_default.hide()
            self.button_zoom_in.hide()
            self.button_zoom_out.hide()

        elif self.combobox_edit.currentIndex() == 2:
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

    def plainTextEdit_content_changed(self):
        self.change_detected_2 = True
    def button_restore_default_pressed(self):
        rsp = question_window("Sind Sie sicher, dass sie die originale Aufgabe wiederherstellen wollen?")
        if rsp == True:
            self.plainTextEdit_content.clear()
            self.plainTextEdit_content.insertPlainText(self.content)
            information_window("Die originale Aufgabe wurde wiederhergestellt.",titel="Original wiederhergestellt")

    def button_undo_pressed(self):
        self.plainTextEdit_content.undo()
        # print(self.plainTextEdit_content.toPlainText())
        # print(is_empty(self.plainTextEdit_content.toPlainText()))
        if is_empty(self.plainTextEdit_content.toPlainText()) == True:
            self.plainTextEdit_content.redo()
    
    # def zoom_in(self):
    #     # value = self.spinbox_font_size.value()
    #     self.plainTextEdit_content.zoomIn()
        # self.plainTextEdit_content.selectAll()
        # self.plainTextEdit_content.setFontPointSize(32)
#         ui->textEdit->selectAll();
# ui->textEdit->setFontPointSize(32);
        # print(self.plainTextEdit_content.styleSheet())
        # self.plainTextEdit_content.setStyleSheet(self.plainTextEdit_content.styleSheet().replace("12", "20"))
        # print(self.plainTextEdit_content.styleSheet())
    
    def button_redo_pressed(self):
        self.plainTextEdit_content.redo()


    def button_preview_pressed(self, typ):
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


    def build_editable_content(self):
        # print(self.aufgabenstellung_split_text)
        self.plainTextEdit_content.insertPlainText(self.content)

        # for line in conten:
        #     self.plainTextEdit_content.appendPlainText(line)

        # self.label_einleitung.hide()
        # self.label_solution.hide()



    def build_checkboxes_for_content(self):
        row = 1
        if self.combobox_edit.currentIndex() == 0:
            for index, linetext in enumerate(self.aufgabenstellung_split_text):
                if (
                    "GRAFIK" in linetext
                    or is_empty(linetext.replace("ITEM", "").strip()) == True
                ) and self.combobox_edit.currentIndex() == 0:  #
                    checkbox = None
                    # print(str(index) + 'empty')
                else:
                    checkbox, checkbox_label = self.create_checkbox_ausgleich(
                        linetext, row, index
                    )
                    # print(checkbox)
                    # if checkbox != None:
                    #     checkbox.clicked.connect(partial(self.checkbox_changed, 0))
                    #     # checkbox_label.clicked.connect(partial(self.checkbox_changed, 0))
                    #     self.dict_widget_variables_ausgleichspunkte[linetext] = checkbox

                        # print(index)
                        # print(self.list_sage_ausgleichspunkte_chosen)
                        # if index in self.list_sage_ausgleichspunkte_chosen:
                        #     print(index)
                        #     print(linetext)
                    #     if index in self.list_sage_ausgleichspunkte_chosen:
                    #         checkbox.setChecked(True) 
                row += 1
                    
        elif self.combobox_edit.currentIndex() == 1:
            for index, linetext in enumerate(self.hide_show_items_split_text):
                if is_empty(linetext.replace("ITEM", "").strip()) == False:

            #     print(linetext)
                    checkbox, checkbox_label = self.create_checkbox_ausgleich(
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

    def checkbox_changed(self, index):
        if index==0:
            self.change_detected_0 = True
        elif index == 1:
            self.change_detected_1 = True

    def checkbox_clicked(self, checkbox, checkbox_label):
        self.checkbox_changed(1)
        try: 
            with open(lama_settings_file, "r", encoding="utf8") as f:
                self.lama_settings = load(f)
        except FileNotFoundError:
            self.lama_settings = {}
        
        try:
            display_settings = self.lama_settings["display"]
            if  display_settings == 1:
                stylesheet = StyleSheet_ausgleichspunkte_dark_mode
            else:
                stylesheet = StyleSheet_ausgleichspunkte
        except KeyError:
            stylesheet = StyleSheet_ausgleichspunkte

        if checkbox.isChecked() == True:
            checkbox_label.setStyleSheet(stylesheet)
        else:
            checkbox_label.setStyleSheet("color: gray")

    def create_checkbox_ausgleich(self, linetext, row, index):
        checkbox_label = create_new_label(self.scrollAreaWidgetContents, "", True, True)

        checkbox = create_new_checkbox(self.scrollAreaWidgetContents, "")
        checkbox.setSizePolicy(SizePolicy_fixed)



        # if self.combobox_edit.currentIndex() == 0:
        #     if index in self.list_sage_ausgleichspunkte_chosen:
        #         checkbox.setChecked(True)
        # if self.combobox_edit.currentIndex() == 1:
        #     if index in self.list_sage_hide_show_items_chosen:
        #         checkbox.setChecked(False)
        #         checkbox_label.setStyleSheet("color: gray")
        #     else:
        #         checkbox.setChecked(True)


        checkbox.clicked.connect(partial(self.checkbox_changed, 0))


        if self.combobox_edit.currentIndex() == 0:
            self.dict_widget_variables_ausgleichspunkte[linetext] = checkbox
            if index in self.list_sage_ausgleichspunkte_chosen:
                checkbox.setChecked(True)

        if self.combobox_edit.currentIndex() == 1:
            self.dict_widget_variables_hide_show_items[linetext] = checkbox
            if index in self.list_sage_hide_show_items_chosen:
                checkbox.setChecked(False)
                checkbox_label.setStyleSheet("color: gray")
            else:
                checkbox.setChecked(True)


        checkbox_label.clicked.connect(
            partial(self.checkbox_label_clicked, checkbox, checkbox_label)
        )

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
        return checkbox, checkbox_label

    def checkbox_label_clicked(self, checkbox, checkbox_label):
        if checkbox.isChecked() == True:
            checkbox.setChecked(False)
        else:
            checkbox.setChecked(True)
        if self.combobox_edit.currentIndex() == 1:
            self.checkbox_clicked(checkbox, checkbox_label)

    def check_if_saved_changes_exist(self):
        # print(self.list_sage_ausgleichspunkte_chosen)
        # print(self.list_sage_hide_show_items_chosen)
        # print(self.sage_individual_change)
        # list_changes = [self.list_sage_ausgleichspunkte_chosen, self.list_sage_hide_show_items_chosen, self.sage_individual_change]

        if not is_empty(self.list_sage_ausgleichspunkte_chosen):
            for index in self.list_sage_ausgleichspunkte_chosen:
                if "\\fbox{A}" in self.aufgabenstellung_split_text[index] or "\\ASubitem" in self.aufgabenstellung_split_text[index]:
                    continue
                else:
                    return True
            # return False
        elif is_empty(self.list_sage_ausgleichspunkte_chosen):
            for all in self.aufgabenstellung_split_text:
                if "\\fbox{A}" in all or "\\ASubitem" in all:
                    return True
        
        if not is_empty(self.list_sage_hide_show_items_chosen):
            return True
        if self.sage_individual_change != None:
            return True

        return False      
    

    def pushButton_OK_pressed(self):
        # self.combobox_edit.currentIndex())
        if self.typ == 2:
            change_detected = self.check_if_saved_changes_exist()
            # print(change_detected)
            
            if change_detected == True:
                response = question_window("Es wurden bereits Änderungen an der Aufgabe gespeichert.",
                "Sind Sie sicher, dass Sie diese Änderungen verwerfen wollen?","Änderung der Aufgabe")
                if response == False:
                    return

        self.list_sage_ausgleichspunkte_chosen = []
        self.list_sage_hide_show_items_chosen = []   
        # self.sage_individual_change = []

        # print(self.plainTextEdit_content.toPlainText())

        if self.combobox_edit.currentIndex() == 2 or self.typ != 2:
            if self.content != self.plainTextEdit_content.toPlainText():
                self.sage_individual_change = self.plainTextEdit_content.toPlainText()

        elif self.combobox_edit.currentIndex() == 0:
            for index, linetext in enumerate(self.aufgabenstellung_split_text):  #list(self.dict_widget_variables_ausgleichspunkte.keys())
                try:
                    if (
                        self.dict_widget_variables_ausgleichspunkte[linetext].isChecked()
                        == True
                    ):
                        self.list_sage_ausgleichspunkte_chosen.append(index)
                except KeyError:
                    pass
                #     self.list_sage_ausgleichspunkte_chosen.append(
                #         linetext.replace("\\fbox{A}", "").replace("\\ASubitem", "")
                #     )

        elif self.combobox_edit.currentIndex() == 1:
            for index, linetext in enumerate(self.hide_show_items_split_text): #list(self.dict_widget_variables_hide_show_items.keys())
                try:
                    if (
                        self.dict_widget_variables_hide_show_items[linetext].isChecked()
                        == False
                    ):
                        self.list_sage_hide_show_items_chosen.append(index)
                except KeyError:
                    pass
                    # self.list_sage_hide_show_items_chosen.append(
                    #     linetext.replace("\\fbox{A}", "")
                    # )

        # print(self.sage_individual_change)

        # list_sage_ausgleichspunkte_chosen = self.list_sage_ausgleichspunkte_chosen
        # list_sage_hide_show_items_chosen = self.list_sage_hide_show_items_chosen
        # sage_individual_change = self.sage_individual_change
        self.Dialog.reject()


class Ui_Dialog_erstellen(QtWidgets.QDialog):
    def setupUi(
        self,
        Dialog,
        Ui_MainWindow,
        dict_list_input_examples,
        dict_titlepage,
        saved_file_path,
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

        self.pkt_ausgleich = Ui_MainWindow.get_number_ausgleichspunkte_gesamt()

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
        self.label_sw_num_ges_int.setText(str(self.num_gesamt))
        self.label_sw_num_2_int.setText(str(self.num_typ2))
        self.label_sw_num_1_int.setText(str(self.num_typ1))
        self.label_sw_pkt_1_int.setText(str(self.pkt_typ1))
        self.label_sw_pkt_2_int.setText(
            "{0} (davon {1} AP)".format(self.pkt_typ2, self.pkt_ausgleich)
        )
        self.label_sw_pkt_ges_int.setText(str(self.pkt_gesamt))
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
        if self.cb_create_pdf.isChecked():
            self.pdf = True
        else:
            self.pdf = False

        if self.cb_create_lama.isChecked():
            self.lama = True
        else:
            self.lama = False

        self.Dialog.accept()


class Ui_Dialog_speichern(QtWidgets.QDialog):
    def setupUi(self, Dialog, creator_mode, chosen_variation):
        self.Dialog = Dialog
        self.creator_mode = creator_mode
        Dialog.setObjectName("Dialog")
        if self.creator_mode == "user":
            titel = "Aufgabe speichern"
        if self.creator_mode == "admin":
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

        if self.creator_mode == "user":
            self.cb_confirm = create_new_checkbox(Dialog, "")
            self.cb_confirm.setSizePolicy(SizePolicy_fixed)
            self.cb_confirm.setStyleSheet("background-color: white; color: black;")
            gridlayout.addWidget(self.cb_confirm, 2, 0, 1, 1, Qt.AlignTop)
            self.label_checkbox = create_new_label(
                Dialog,
                "Hiermit bestätige ich, dass ich die eingegebene Aufgabe eigenständig und\nunter Berücksichtigung des Urheberrechtsgesetzes verfasst habe.\n"
                "Ich stelle die eingegebene Aufgabe frei gemäß der Lizenz CC0 1.0 zur Verfügung.\n"
                "Die Aufgabe darf daher zu jeder Zeit frei verwendet, kopiert und verändert werden.",
                False,
                True,
            )
            self.label_checkbox.setStyleSheet("padding-bottom: 20px;")
            gridlayout.addWidget(self.label_checkbox, 2, 1, 1, 1, Qt.AlignTop)
            self.label_checkbox.clicked.connect(self.label_checkbox_clicked)

        # if self.creator_mode == "admin":
            # self.combobox_in_official = create_new_combobox(Dialog)
            # self.combobox_in_official.setStyleSheet(
            #     """
            # QWidget {{
            #     background-color: white;
            #     color: black;
            #     selection-background-color: {0};
            #     selection-color: white;
            # }}

            # QComboBox::disabled {{
            #    background-color: gray; color: white; 
            # }}
            # """.format(
            #         get_color(blue_7)
            #     )
            # )
            # self.combobox_in_official.addItem("offizielle Aufgabe")
            # self.combobox_in_official.setEnabled(False)
            # self.combobox_in_official.addItem("inoffizelle Aufgabe")
            # if chosen_variation != None:
            #     number = chosen_variation.split(" - ")
            #     number = number[-1].split("_")[-1]
                # if "i" in number:
                #     self.combobox_in_official.setCurrentIndex(1)
                # else:
                # self.combobox_in_official.setCurrentIndex(0)
                # self.combobox_in_official.setEnabled(False)
            # gridlayout.addWidget(self.combobox_in_official, 2, 0, 1, 1)

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        if self.creator_mode == "user":
            if chosen_variation == None:
                self.buttonBox.setStandardButtons(
                    QtWidgets.QDialogButtonBox.Yes
                    | QtWidgets.QDialogButtonBox.No
                    | QtWidgets.QDialogButtonBox.Apply
                )
            else:
                self.buttonBox.setStandardButtons(
                    QtWidgets.QDialogButtonBox.Yes | QtWidgets.QDialogButtonBox.No
                )
        if self.creator_mode == "admin":
            self.buttonBox.setStandardButtons(
                QtWidgets.QDialogButtonBox.Yes | QtWidgets.QDialogButtonBox.No
            )

        buttonN = self.buttonBox.button(QtWidgets.QDialogButtonBox.No)
        buttonN.setText("Abbrechen")
        self.buttonBox.rejected.connect(self.Dialog.reject)

        buttonY = self.buttonBox.button(QtWidgets.QDialogButtonBox.Yes)
        buttonY.setText("Speichern")
        buttonY.clicked.connect(self.yes_pressed)

        if self.creator_mode == "user" and chosen_variation == None:
            button_local = self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply)
            button_local.setText("Lokal speichern")
            button_local.clicked.connect(self.local_pressed)

        gridlayout.addWidget(self.buttonBox, 3, 1, 1, 1)

    def local_pressed(self):
        self.confirmed = ["local", None]
        self.Dialog.accept()

    def yes_pressed(self):
        if self.creator_mode == "admin":
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
        try: 
            with open(lama_settings_file, "r", encoding="utf8") as f:
                self.lama_settings = load(f)
        except FileNotFoundError:
            self.lama_settings = {
                'start_program' : 0,
                'pdf_reader' : "",
                'database' : 2,
                'display' : 0,
                'autosave' : 2,
                'quelle' : '',
            }
        # self.beispieldaten_dateipfad_cria = MainWindow.beispieldaten_dateipfad_cria
        # self.beispieldaten_dateipfad_1 = MainWindow.beispieldaten_dateipfad_1
        # self.beispieldaten_dateipfad_2 = MainWindow.beispieldaten_dateipfad_2

        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("Einstellungen")
        row=0
        # self.Dialog.setMinimumWidth(400)
        Dialog.setWindowIcon(QIcon(logo_path))
        gridlayout_setup = create_new_gridlayout(Dialog)

        groupbox_start_program = create_new_groupbox(Dialog, "Auswahl beim Programmstart")
        groupbox_start_program.setSizePolicy(SizePolicy_fixed_height)
        horizontalLayout_start_program = create_new_horizontallayout(groupbox_start_program)

        # label_start_program = create_new_label(groupbox_start_program, "Auswahl")
        # horizontalLayout_start_program.addWidget(label_start_program)

        self.combobox_start_program = create_new_combobox(groupbox_start_program)
        add_new_option(self.combobox_start_program, 0, "beim Start fragen")
        add_new_option(self.combobox_start_program, 1, "LaMA Cria (Unterstufe)")
        add_new_option(self.combobox_start_program, 2, "LaMA (Oberstufe)")
        try:
            self.combobox_start_program.setCurrentIndex(self.lama_settings['start_program'])
        except KeyError:
            self.lama_settings['start_program'] = 0
        horizontalLayout_start_program.addWidget(self.combobox_start_program)

        gridlayout_setup.addWidget(groupbox_start_program, row,0,1,1)
        row +=1

        groupbox_path_pdf = create_new_groupbox(Dialog, "Dateipfad PDF Reader")
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
        horizontallayout_path_pdf.addWidget(self.button_search_pdf_reader)

        gridlayout_setup.addWidget(groupbox_path_pdf,row,0,1,1)
        row +=1

        groupbox_database = create_new_groupbox(Dialog, "Automatische Aktualisierung der Datenbank")
        groupbox_database.setSizePolicy(SizePolicy_fixed_height)
        horizontallayout_database = create_new_horizontallayout(groupbox_database)

        # label_database = create_new_label(Dialog, "Datenbank automatisch aktualisieren:")
        # horizontallayout_database.addWidget(label_database)
        self.combobox_database = create_new_combobox(groupbox_database)
        horizontallayout_database.addWidget(self.combobox_database)
        

        add_new_option(self.combobox_database, 0, "jedes Mal beim Öffnen von LaMA")
        add_new_option(self.combobox_database, 1, "wöchentlich")
        add_new_option(self.combobox_database, 2, "monatlich")
        add_new_option(self.combobox_database, 3, "niemals")

        try:
            self.combobox_database.setCurrentIndex(self.lama_settings['database'])
        except KeyError:
            self.lama_settings['database'] = 2
            self.combobox_database.setCurrentIndex(2)
        
        gridlayout_setup.addWidget(groupbox_database, row,0,1,1)
        row+=1


        groupbox_autosave = create_new_groupbox(Dialog, "Autosave Intervall")
        groupbox_autosave.setToolTip("0 = Autosave deaktivieren")
        horizontallayout_autosave = create_new_horizontallayout(groupbox_autosave)

        # label_autosave = create_new_label(Dialog, "Intervall:")
        # horizontallayout_autosave.addWidget(label_autosave)

        self.spinbox_autosave = create_new_spinbox(Dialog, value=2)
        try:
            self.spinbox_autosave.setValue(self.lama_settings['autosave'])
        except KeyError:
            self.lama_settings['autosave'] = 2
        self.spinbox_autosave.setSizePolicy(SizePolicy_fixed)
        horizontallayout_autosave.addWidget(self.spinbox_autosave)

        label_autosave_2 = create_new_label(Dialog, "Minuten")
        horizontallayout_autosave.addWidget(label_autosave_2)

        gridlayout_setup.addWidget(groupbox_autosave, row,0,1,1)
        row+=1


        groupbox_quelle = create_new_groupbox(Dialog, "Quelle Standardeingabe")
        horizontallayout_quelle = create_new_horizontallayout(groupbox_quelle)

        self.lineedit_quelle = create_new_lineedit(Dialog)
        try:
            self.lineedit_quelle.setText(self.lama_settings['quelle'])
        except KeyError:
            self.lama_settings['quelle'] = ""        

        horizontallayout_quelle.addWidget(self.lineedit_quelle)

        gridlayout_setup.addWidget(groupbox_quelle, row,0,1,1)
        row +=1


        groupbox_display = create_new_groupbox(Dialog, "Anzeigemodus")
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
        
        gridlayout_setup.addWidget(groupbox_display, row, 0,1,1)
        row +=1


        gridlayout_setup.setRowStretch(row, 1)
        row +=1


        self.buttonBox_setup = QtWidgets.QDialogButtonBox(self.Dialog)
        self.buttonBox_setup.setStandardButtons(
            QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel
        )


        buttonS = self.buttonBox_setup.button(QtWidgets.QDialogButtonBox.Save)
        buttonS.setText('Speichern')
        buttonX = self.buttonBox_setup.button(QtWidgets.QDialogButtonBox.Cancel)
        buttonX.setText("Abbrechen")
        self.buttonBox_setup.rejected.connect(self.reject_dialog)
        self.buttonBox_setup.accepted.connect(self.save_setting)

        gridlayout_setup.addWidget(self.buttonBox_setup,row,0,1,1)

        
    # def combobox_display_changed(self):
    #     information_window("Die Darstellung wird erst nach dem Neustart von LaMA übernommen.")
        

    def search_pdf_reader(self):
        list_filename = QtWidgets.QFileDialog.getOpenFileName(
            None, "Durchsuchen", self.lama_settings['pdf_reader'], "Alle Dateien (*)"
            )
        if list_filename[0] == '':
            return
        # print(list_filename)
        # print(os.path.isfile("-a {}".format(list_filename[0]))
        # print(os.path.isdir("-a {}".format(list_filename[0]))
        self.lineedit_pdf_reader.setText(list_filename[0])

    def reject_dialog(self):
        self.Dialog.reject()

    def save_settings_to_dict(self):
        dict_={}
        dict_['start_program'] = self.combobox_start_program.currentIndex()
        dict_['pdf_reader'] = self.lineedit_pdf_reader.text()
        dict_['database'] = self.combobox_database.currentIndex()
        dict_['display'] = self.combobox_display.currentIndex()
        dict_['autosave'] = self.spinbox_autosave.value()
        dict_['quelle'] = self.lineedit_quelle.text()

        return dict_

    def save_setting(self):
        if self.MainWindow.display_mode != self.combobox_display.currentIndex():
            information_window("Die Änderung der Darstellung wird erst nach dem Neustart von LaMA übernommen.")
        self.lama_settings = self.save_settings_to_dict()
        with open(lama_settings_file, "w+", encoding="utf8") as f:
            dump(self.lama_settings, f, ensure_ascii=False)
        self.MainWindow.lineEdit_quelle.setText(self.lineedit_quelle.text())
        self.Dialog.accept()
    

class Ui_Dialog_developer(object):
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        self.developer_mode_active = False
        Dialog.setWindowTitle("Entwicklermodus aktivieren")
        row=0
        # self.Dialog.setMinimumWidth(400)
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
        buttonS.setText('Speichern')
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
        # print(hashed_pw)
        password = self.lineedit_developer.text().encode('utf-8')
        # print(password)
        if bcrypt.checkpw(password, hashed_pw):
            if self.checkbox_developer.isChecked():
                path_lama_developer_credentials = os.path.join(os.getenv('LOCALAPPDATA'), "LaMA", "credentials")
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
        Dialog.setFixedSize(300, 150)
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
        # print(dict_drafts[typ])
        self.typ = typ
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


        row = 0
        column = 0
        
        for dict_aufgabe in self.dict_drafts[typ]:
            self.add_draft_to_list(dict_aufgabe, self.scrollAreaWidgetContents, row, column)
            if column == 2:
                row += 1
                column = 0
            else:
                column +=1        

        self.spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        self.gridLayout_items.addItem(self.spacerItem, row+1, 0, 1,3)

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
        if self.typ == 'cria':
            self.groupBox_klasse.hide()
        self.horizontalLayout_klasse = create_new_horizontallayout(self.groupBox_klasse)
        self.groupBox_klasse.setEnabled(False)
        
        self.comboBox_klasse = create_new_combobox(self.groupBox_klasse)
        self.horizontalLayout_klasse.addWidget(self.comboBox_klasse)
        add_new_option(self.comboBox_klasse, 0, "")
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
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        buttonSave = self.buttonBox.button(QtWidgets.QDialogButtonBox.Save)
        buttonSave.setText("Änderung speichern")
        buttonSave.clicked.connect(self.save_changes)
        self.gridLayout_2.addWidget(self.buttonBox, 3, 6,1,1)
        self.gridLayout.addWidget(self.groupBox, 5, 0, 1, 5)



        self.comboBox.currentIndexChanged.connect(self.comboBox_index_changed)



        # self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)


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
        # print(self.dict_drafts)
        # name = dict_aufgabe['name']
        # print(name)
        # create_new_checkbox(parent, )

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
            try:
                self.label_themen.setText(str(dict_aufgabe['themen']))
                if re.search("\[.*\]", self.comboBox.currentText()) != None and self.typ == 'lama_1':
                    self.pushButton_themen.setEnabled(False)
                else:
                    self.pushButton_themen.setEnabled(True)

                self.plainTextEdit.setPlainText(dict_aufgabe['content'])
                self.plainText_backup = [self.comboBox.currentIndex(), dict_aufgabe['content']]
                self.spinBox_pkt.setValue(dict_aufgabe['punkte'])
                self.comboBox_af.setCurrentText(dict_aufgabe['af'])
                self.comboBox_klasse.setCurrentText(dict_aufgabe['klasse'])
                if dict_aufgabe['pagebreak'] == False:
                    self.comboBox_pagebreak.setCurrentIndex(0)
                else:
                    self.comboBox_pagebreak.setCurrentIndex(1)

                self.spinBox_abstand.setValue(dict_aufgabe['abstand'])
                self.lineedit_titel.setText(dict_aufgabe['titel'])
                self.lineedit_quelle.setText(dict_aufgabe['quelle'])

            except TypeError:
                pass



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
            file.write(tex_minimal.tex_preamble())
            file.write(content)
            file.write(tex_minimal.tex_end)


        Popen(file_path, shell = True).poll()
        

    def create_content(self, chosen_list):
        content = ""
        for name in chosen_list:
            dict_aufgabe = self.get_dict_aufgabe(name)
            content = content + "\subsubsection{{{0}}}\n".format(name)
            if dict_aufgabe['pagebreak'] == False:
                begin =  tex_minimal.begin_beispiel()
                end = tex_minimal.end_beispiel
            else:
                begin = tex_minimal.begin_beispiel_lang()
                end = tex_minimal.end_beispiel_lang
            
            content = content + begin + dict_aufgabe['content'] +end + "\n\n\\newpage\n\n"

        return content


    def remove_from_list(self):
        chosen_list = self.get_chosen_list()
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


        dict_entries = {
            'themen':eval(self.label_themen.text()),
            'punkte':self.spinBox_pkt.value(),
            'af':self.comboBox_af.currentText(),
            'klasse':self.comboBox_klasse.currentText(),
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


        self.comboBox.clear()
        self.comboBox.addItem("")

        for dict_aufgabe in self.dict_drafts[self.typ]:
            self.comboBox.addItem(dict_aufgabe['name'])
    

    def edit_themen(self):
        Dialog = QtWidgets.QDialog(
            None,
            Qt.WindowSystemMenuHint
            | Qt.WindowTitleHint
            | Qt.WindowCloseButtonHint,
        )
        ui = Ui_Dialog_edit_themen()
        list_themen = eval(self.label_themen.text())
        ui.setupUi(Dialog, list_themen, self.typ)


        rsp = Dialog.exec_()

        if rsp == 1:
            self.label_themen.setText(str(ui.list_themen))



class Ui_Dialog_edit_themen(object):
    def setupUi(self, Dialog, list_themen, typ):
        self.Dialog = Dialog
        self.list_themen = list_themen
        self.typ = typ
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
            #     print(all)
            # self.comboBox_thema.addItem("test")
                # add_new_option(self.comboBox_thema, 0, all)
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
            # print('thema: {}'.format(split))
            dict_themen = eval("dict_{0}".format(klasse))
            # print(dict_themen)
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
        if self.typ == 'cria':
            klasse = self.comboBox_klassen.currentText()
  
        thema = self.comboBox_thema.currentText().split(" (")[0]
        subthema  = self.comboBox_subthema.currentText().split(" (")[0]

        if self.typ == 'cria':
            self.label_themen.setText("{0}.{1}.{2}".format(klasse, thema, subthema))
        else:
            self.label_themen.setText("{0} {1}".format(thema, subthema))

    def add_thema(self):
        gk = self.label_themen.text()

        existing_items = self.listWidget.findItems(gk, Qt.MatchExactly)

        if is_empty(existing_items):
            self.listWidget.addItem(gk)


        

    def remove_thema(self):
        list_selected_items = self.listWidget.selectedItems()
        if not list_selected_items:
            return

        for item in list_selected_items:
            self.listWidget.takeItem(self.listWidget.row(item))
        # self.listWidget.deleteItem(selected_item)??



    def save_changes(self):
        list_themen = []
        for index in range(self.listWidget.count()):
            list_themen.append(self.listWidget.item(index).text())

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