from PyQt5 import QtCore, QtWidgets, QtGui
import os
import shutil
import re
from string import ascii_lowercase
from functools import partial
from config import (
    config_loader,
    config_file,
    colors_ui,
    get_color,
    path_programm,
    logo_path,
    logo_cria_button_path,
    is_empty,
)
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
    create_new_groupbox,
    add_new_option,
)
from standard_dialog_windows import critical_window
from waitingspinnerwidget import QtWaitingSpinner
from predefined_size_policy import SizePolicy_fixed
from work_with_content import prepare_content_for_hide_show_items
from sort_items import sorted_gks

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


StyleSheet_tabWidget = """
QTabBar::tab:selected {{
background: {0}; color: {1};
padding-right: 10px; padding-left: 10px;
border-top: 2px solid {3};
border-left: 2px solid {3};
border-right: 2px solid {3};
}}

QWidget {{color: {2};background-color: {3}}}
""".format(
    get_color(blue_2), get_color(black), get_color(white), get_color(blue_7)
)


class Ui_Dialog_choose_type(object):
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle(
            _translate("Titelplatt anpassen", "Programm auswählen", None)
        )
        Dialog.setWindowIcon(QtGui.QIcon(logo_path))

        # Dialog.setStyleSheet("QToolTip { color: white; background-color: rgb(47, 69, 80); border: 0px; }")
        Dialog.setSizePolicy(SizePolicy_fixed)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")

        self.btn_lama_cria = QtWidgets.QPushButton()
        self.btn_lama_cria.setObjectName(_fromUtf8("btn_lama_cria"))
        # self.btn_lama_cria.setText("LaMA Cria (Unterstufe)")
        self.btn_lama_cria.setIcon(QtGui.QIcon(logo_cria_button_path))
        self.btn_lama_cria.setIconSize(QtCore.QSize(120, 120))
        self.btn_lama_cria.setFixedSize(120, 120)
        self.btn_lama_cria.setStyleSheet(
            _fromUtf8("background-color: rgb(63, 169, 245);")
        )
        self.btn_lama_cria.setAutoDefault(False)
        self.btn_lama_cria.setShortcut("F1")
        self.gridLayout.addWidget(self.btn_lama_cria, 0, 0, 1, 1, QtCore.Qt.AlignCenter)
        self.label_lama_cria = QtWidgets.QLabel()
        self.label_lama_cria.setObjectName(_fromUtf8("label_lama_cria"))
        self.label_lama_cria.setText("LaMA Cria (Unterstufe)")
        self.gridLayout.addWidget(
            self.label_lama_cria, 1, 0, 1, 1, QtCore.Qt.AlignCenter
        )
        # self.btn_lama_cria.setMaximumWidth(130)
        self.btn_lama_cria.clicked.connect(partial(self.choose_button_pressed, "cria"))

        self.btn_lama = QtWidgets.QPushButton()
        self.btn_lama.setObjectName(_fromUtf8("btn_lama"))
        # self.btn_lama.setText("LaMA (Oberstufe)")
        self.btn_lama.setIcon(QtGui.QIcon(logo_path))
        self.btn_lama.setIconSize(QtCore.QSize(120, 120))
        self.btn_lama.setShortcut("F2")
        self.btn_lama.setFixedSize(120, 120)
        self.btn_lama.setAutoDefault(False)
        self.gridLayout.addWidget(self.btn_lama, 0, 1, 1, 1, QtCore.Qt.AlignCenter)
        self.btn_lama.clicked.connect(partial(self.choose_button_pressed, "lama"))
        self.label_lama = QtWidgets.QLabel()
        self.label_lama.setObjectName(_fromUtf8("label_lama"))
        self.label_lama.setText("LaMA (Oberstufe)")
        self.gridLayout.addWidget(self.label_lama, 1, 1, 1, 1, QtCore.Qt.AlignCenter)

    def choose_button_pressed(self, chosen_program):
        self.chosen_program = chosen_program
        self.Dialog.accept()


class Ui_Dialog_processing(object):
    def setupUi(self, Dialog, text):
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        Dialog.setWindowFlags(
            QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint
        )
        Dialog.setWindowTitle("Lade...")
        Dialog.setStyleSheet(
            "background-color: {}; color: white".format(get_color(blue_7))
        )
        # Dialog.setSizePolicy(SizePolicy_fixed)
        # Dialog.setFixedSize(Dialog.size())
        pixmap = QtGui.QPixmap(logo_path)
        Dialog.setWindowIcon(QtGui.QIcon(logo_path))
        # Dialog.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        horizontalLayout.setObjectName("horizontal")
        horizontalLayout.setSizeConstraint(QtWidgets.QHBoxLayout.SetFixedSize)

        pixmap = QtGui.QPixmap(logo_cria_button_path)
        # Dialog.setPixmap(pixmap.scaled(110, 110, QtCore.Qt.KeepAspectRatio))
        image = QtWidgets.QLabel(Dialog)
        image.setObjectName("image")
        image.setPixmap(pixmap.scaled(30, 30, QtCore.Qt.KeepAspectRatio))

        label = QtWidgets.QLabel(Dialog)
        label.setObjectName("label")
        label.setText(text)
        label.setStyleSheet("padding: 20px")
        label_spinner = QtWidgets.QLabel(Dialog)
        label.setObjectName("label_spinner")
        label_spinner.setFixedSize(30, 30)
        spinner = QtWaitingSpinner(label_spinner)
        spinner.setRoundness(70.0)
        # spinner.setMinimumTrailOpacity(10.0)
        # spinner.setTrailFadePercentage(60.0)
        spinner.setNumberOfLines(15)
        spinner.setLineLength(8)
        # spinner.setLineWidth(5)
        spinner.setInnerRadius(5)
        # spinner.setRevolutionsPerSecond(2)
        spinner.setColor(QtCore.Qt.white)
        spinner.start()  # starts spinning
        label.setAlignment(QtCore.Qt.AlignCenter)
        horizontalLayout.addWidget(image)
        horizontalLayout.addWidget(label)
        horizontalLayout.addWidget(label_spinner)


class Ui_Dialog_variation(object):
    def setupUi(self, Dialog, MainWindow):
        self.MainWindow = MainWindow
        self.beispieldaten_dateipfad_cria = MainWindow.beispieldaten_dateipfad_cria
        self.beispieldaten_dateipfad_1 = MainWindow.beispieldaten_dateipfad_1
        self.beispieldaten_dateipfad_2 = MainWindow.beispieldaten_dateipfad_2

        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("Vorhandene Aufgabe auswählen")
        Dialog.setWindowIcon(QtGui.QIcon(logo_path))
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
            self.comboBox_at_sage.setFocusPolicy(QtCore.Qt.ClickFocus)

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
            self.comboBox_gk.setFocusPolicy(QtCore.Qt.ClickFocus)
            self.verticalLayout_sage.addWidget(self.comboBox_gk)
            self.comboBox_gk_num = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
            self.comboBox_gk_num.setObjectName("comboBox_gk_num")
            self.comboBox_gk_num.currentIndexChanged.connect(self.adapt_choosing_list)
            self.comboBox_gk_num.setFocusPolicy(QtCore.Qt.ClickFocus)
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

            self.comboBox_klassen.setFocusPolicy(QtCore.Qt.ClickFocus)
            self.verticalLayout_sage.addWidget(self.comboBox_klassen)

            self.comboBox_kapitel = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
            self.comboBox_kapitel.setObjectName("comboBox_kapitel")
            self.comboBox_kapitel.currentIndexChanged.connect(
                self.comboBox_kapitel_changed
            )
            self.comboBox_kapitel.setFocusPolicy(QtCore.Qt.ClickFocus)
            self.verticalLayout_sage.addWidget(self.comboBox_kapitel)

            self.comboBox_unterkapitel = QtWidgets.QComboBox(
                self.groupBox_alle_aufgaben
            )
            self.comboBox_unterkapitel.setObjectName("comboBox_unterkapitel")
            self.comboBox_unterkapitel.currentIndexChanged.connect(
                self.adapt_choosing_list
            )
            self.comboBox_unterkapitel.setFocusPolicy(QtCore.Qt.ClickFocus)
            self.verticalLayout_sage.addWidget(self.comboBox_unterkapitel)

        self.lineEdit_number = QtWidgets.QLineEdit(self.groupBox_alle_aufgaben)
        self.lineEdit_number.setObjectName("lineEdit_number")
        self.lineEdit_number.setValidator(QtGui.QIntValidator())
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
                    klasse + "_" + self.listWidget.selectedItems()[0].text()
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

    # def comboBox_unterkapitel_changed(self):
    #     self.adapt_choosing_list()

    def add_items_to_listwidget(
        self, list_beispieldaten_sections, beispieldaten_dateipfad
    ):
        self.no_choice = "-- keine Auswahl --"
        self.listWidget.addItem(self.no_choice)
        for section in list_beispieldaten_sections:
            try:
                path = beispieldaten_dateipfad[section]
            except KeyError:
                drafts_path = os.path.join(path_programm, "Beispieleinreichung")
                beispieldaten_dateipfad_draft = search_files(drafts_path)
                path = beispieldaten_dateipfad_draft[section]

            name, extension = os.path.splitext(os.path.basename(path))
            item = QtWidgets.QListWidgetItem()

            item.setText(name)

            if name.startswith("_L_") or "Beispieleinreichung" in path:
                pass
            elif re.search("\[.+\]", name) != None:
                pass
            else:
                self.listWidget.addItem(item)

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

    def adapt_choosing_list(self):
        self.listWidget.clear()

        if self.MainWindow.chosen_program == "cria":
            typ = None
            beispieldaten_dateipfad = self.beispieldaten_dateipfad_cria
        else:
            if self.comboBox_at_sage.currentText() == "Typ 1":
                typ = 1
                beispieldaten_dateipfad = self.beispieldaten_dateipfad_1
            elif self.comboBox_at_sage.currentText() == "Typ 2":
                typ = 2
                beispieldaten_dateipfad = self.beispieldaten_dateipfad_2

        list_beispieldaten_sections = list(beispieldaten_dateipfad.keys())

        if self.MainWindow.chosen_program == "lama":
            combobox_gk = self.comboBox_gk.currentText()
            result = re.findall("\(([a-z]+)\)", self.comboBox_gk_num.currentText())
            if not is_empty(result):
                combobox_gk_num = result[-1]
            else:
                combobox_gk_num = self.comboBox_gk_num.currentText()

            list_beispieldaten_sections = self.MainWindow.adjust_beispieldaten_combobox_lama(
                list_beispieldaten_sections, combobox_gk, combobox_gk_num,
            )

        if self.MainWindow.chosen_program == "cria":
            combobox_klasse = self.comboBox_klassen.currentText()
            combobox_kapitel = self.comboBox_kapitel.currentText()
            combobox_unterkapitel = self.comboBox_unterkapitel.currentText()

            list_beispieldaten_sections = self.MainWindow.adjust_beispieldaten_combobox_cria(
                list_beispieldaten_sections,
                combobox_klasse,
                combobox_kapitel,
                combobox_unterkapitel,
            )

        line_entry = self.lineEdit_number.text()

        if is_empty(line_entry) == False:
            list_beispieldaten_sections = self.search_for_number(
                list_beispieldaten_sections, line_entry
            )

        list_beispieldaten_sections = sorted_gks(
            list_beispieldaten_sections, self.MainWindow.chosen_program
        )

        self.add_items_to_listwidget(
            list_beispieldaten_sections, beispieldaten_dateipfad
        )


class Ui_Dialog_random_quiz(object):
    def setupUi(self, Dialog, Ui_MainWindow):
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("Zufälliges Quiz")
        Dialog.setWindowIcon(QtGui.QIcon(logo_path))
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

        # print(Ui_MainWindow.dict_widget_variables)
        # self.buttonBox_titlepage = QtWidgets.QDialogButtonBox(self.Dialog)
        # self.buttonBox_titlepage = QtWidgets.QDialogButtonBox(self.Dialog)
        # self.buttonBox_titlepage.setStandardButtons(
        #     QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        # )

        # # buttonS = self.buttonBox_titlepage.button(QtWidgets.QDialogButtonBox.Save)
        # # buttonS.setText('Speichern')
        # buttonX = self.buttonBox_titlepage.button(QtWidgets.QDialogButtonBox.Cancel)
        # buttonX.setText("Standard wiederherstellen")
        # self.buttonBox_titlepage.setObjectName("buttonBox")
        # self.buttonBox_titlepage.rejected.connect(
        #     partial(self.set_default_titlepage, dict_titlepage)
        # )
        # self.buttonBox_titlepage.accepted.connect(
        #     partial(self.save_titlepage, dict_titlepage)
        # )
        # # self.retranslateUi(self.Dialog)

        # self.verticalLayout_titlepage.addWidget(self.buttonBox_titlepage)


class Ui_Dialog_titlepage(object):
    def setupUi(self, Dialog, dict_titlepage):
        # self.dict_titlepage = dict_titlepage
        # print(self.dict_titlepage)

        # self.aufgabenstellung_split_text=aufgabenstellung_split_text
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle(
            _translate("Titelplatt anpassen", "Titelplatt anpassen", None)
        )
        # self.Dialog.resize(600, 400)
        # self.Dialog.setWindowIcon(QtGui.QIcon(logo_path))
        # Dialog.setObjectName("Dialog")
        # Dialog.resize(468, 208)
        Dialog.setWindowIcon(QtGui.QIcon(logo_path))
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
        # print(logo_name)
        self.cb_titlepage_logo.setText("Logo ({})".format(logo_name))
        dict_titlepage["logo_path"] = "{}".format(logo_titlepage_path[0][0])
        copy_logo_titlepage_path = os.path.join(
            path_programm, "Teildokument", logo_name
        )
        shutil.copy(logo_titlepage_path[0][0], copy_logo_titlepage_path)

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
        aufgabenstellung_split_text,
        list_sage_ausgleichspunkte_chosen,
        list_sage_hide_show_items_chosen,
    ):
        self.aufgabenstellung_split_text = aufgabenstellung_split_text
        self.hide_show_items_split_text = prepare_content_for_hide_show_items(
            aufgabenstellung_split_text
        )
        self.list_sage_ausgleichspunkte_chosen = list_sage_ausgleichspunkte_chosen
        # print(self.list_sage_ausgleichspunkte_chosen)
        self.list_sage_hide_show_items_chosen = list_sage_hide_show_items_chosen
        self.dict_widget_variables_ausgleichspunkte = {}
        self.dict_widget_variables_hide_show_items = {}

        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        self.Dialog.setWindowTitle("Ausgleichspunkte anpassen")
        self.Dialog.resize(600, 400)
        self.Dialog.setWindowIcon(QtGui.QIcon(logo_path))

        verticallayout_titlepage = create_new_verticallayout(Dialog)
        # self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        # self.gridLayout_2.setObjectName("gridLayout_2")
        self.combobox_edit = create_new_combobox(Dialog)
        verticallayout_titlepage.addWidget(self.combobox_edit)
        self.combobox_edit.addItem("Ausgleichspunkte anpassen")
        self.combobox_edit.addItem("Aufgabenstellungen ein-/ausblenden")
        self.combobox_edit.currentIndexChanged.connect(self.combobox_edit_changed)
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 600, 500))
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
        self.gridLayout.addWidget(self.label_einleitung, 0, 1, 1, 3, QtCore.Qt.AlignTop)

        self.label_solution = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_solution.setWordWrap(True)
        self.label_solution.setObjectName("label_solution")
        self.label_solution.setText("\nLösungserwartung:\n[...]")

        row = self.build_checkboxes_for_content()

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        verticallayout_titlepage.addWidget(self.scrollArea)
        # self.buttonBox = QtWidgets.QDialogButtonBox(self.Dialog)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.Dialog)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )

        buttonX = self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel)
        buttonX.setText("Abbrechen")
        self.buttonBox.rejected.connect(self.Dialog.reject)
        verticallayout_titlepage.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(
            partial(self.pushButton_OK_pressed, list_sage_ausgleichspunkte_chosen)
        )
        # # self.retranslateUi(self.Dialog)
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)

    def combobox_edit_changed(self):
        for i in reversed(range(1, self.gridLayout.count())):
            self.gridLayout.itemAt(i).widget().setParent(None)
        if self.combobox_edit.currentIndex() == 0:
            self.build_checkboxes_for_content()
        if self.combobox_edit.currentIndex() == 1:
            self.build_checkboxes_for_content()

    def build_checkboxes_for_content(self):
        row = 1
        if self.combobox_edit.currentIndex() == 0:
            # print(self.aufgabenstellung_split_text)
            for linetext in self.aufgabenstellung_split_text:
                if (
                    "GRAFIK" in linetext
                    or is_empty(linetext.replace("ITEM", "").strip()) == True
                ) and self.combobox_edit.currentIndex() == 0:  #
                    checkbox = None
                else:
                    checkbox, checkbox_label = self.create_checkbox_ausgleich(
                        linetext, row
                    )
                    if checkbox != None:
                        self.dict_widget_variables_ausgleichspunkte[linetext] = checkbox

                    row += 1
        elif self.combobox_edit.currentIndex() == 1:
            item_number = 0
            for linetext in self.hide_show_items_split_text:
                checkbox, checkbox_label = self.create_checkbox_ausgleich(
                    linetext, row, item_number
                )
                if checkbox != None:
                    checkbox.clicked.connect(
                        partial(self.checkbox_clicked, checkbox, checkbox_label)
                    )
                    self.dict_widget_variables_hide_show_items[linetext] = checkbox

                row += 1
                item_number += 1

        self.gridLayout.addWidget(self.label_solution, row, 1, 1, 3, QtCore.Qt.AlignTop)

        self.gridLayout.setRowStretch(row, 1)

    def checkbox_clicked(self, checkbox, checkbox_label):
        if checkbox.isChecked() == True:
            checkbox_label.setStyleSheet("color: black")
        else:
            checkbox_label.setStyleSheet("color: gray")

    def create_checkbox_ausgleich(self, linetext, row, item_number=None):
        checkbox_label = create_new_label(self.scrollAreaWidgetContents, "", True, True)

        checkbox = create_new_checkbox(self.scrollAreaWidgetContents, "")
        checkbox.setSizePolicy(SizePolicy_fixed)
        self.gridLayout.addWidget(checkbox, row, 0, 1, 1, QtCore.Qt.AlignTop)

        if "\\fbox{A}" in linetext:
            linetext = linetext.replace("\\fbox{A}", "")
        if "\\ASubitem" in linetext:
            linetext = linetext.replace("\\ASubitem", "")

        # print(linetext)
        if self.combobox_edit.currentIndex() == 0:
            if linetext in self.list_sage_ausgleichspunkte_chosen:
                checkbox.setChecked(True)
        if self.combobox_edit.currentIndex() == 1:
            # print(self.list_sage_hide_show_items_chosen)
            if linetext in self.list_sage_hide_show_items_chosen:
                checkbox.setChecked(False)
                checkbox_label.setStyleSheet("color: gray")
            else:
                checkbox.setChecked(True)

        checkbox_label.clicked.connect(
            partial(self.checkbox_label_clicked, checkbox, checkbox_label)
        )

        linetext = (
            linetext.replace("ITEM", "")
            .replace("SUBitem", "")
            .replace("{", "")
            .replace("}", "")
            .strip()
        )
        if self.combobox_edit.currentIndex() == 1:
            linetext = ascii_lowercase[item_number] + ")\n" + linetext

        checkbox_label.setText(linetext)

        self.gridLayout.addWidget(checkbox_label, row, 1, 1, 2, QtCore.Qt.AlignTop)
        return checkbox, checkbox_label

    def checkbox_label_clicked(self, checkbox, checkbox_label):
        if checkbox.isChecked() == True:
            checkbox.setChecked(False)
        else:
            checkbox.setChecked(True)
        if self.combobox_edit.currentIndex() == 1:
            self.checkbox_clicked(checkbox, checkbox_label)

    def pushButton_OK_pressed(self, list_sage_ausgleichspunkte_chosen):

        self.list_sage_ausgleichspunkte_chosen = []
        for linetext in list(self.dict_widget_variables_ausgleichspunkte.keys()):
            if (
                self.dict_widget_variables_ausgleichspunkte[linetext].isChecked()
                == True
            ):
                self.list_sage_ausgleichspunkte_chosen.append(
                    linetext.replace("\\fbox{A}", "").replace("\\ASubitem", "")
                )

        self.list_sage_hide_show_items_chosen = []
        for linetext in list(self.dict_widget_variables_hide_show_items.keys()):
            if (
                self.dict_widget_variables_hide_show_items[linetext].isChecked()
                == False
            ):
                self.list_sage_hide_show_items_chosen.append(
                    linetext.replace("\\fbox{A}", "")
                )

        list_sage_ausgleichspunkte_chosen = self.list_sage_ausgleichspunkte_chosen
        list_sage_hide_show_items_chosen = self.list_sage_hide_show_items_chosen

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

        if Ui_MainWindow.chosen_program == "cria":
            self.label_sw_num_1.hide()
            self.label_sw_num_1_int.hide()
            self.label_sw_pkt_1.hide()
            self.label_sw_pkt_1_int.hide()
            self.label_sw_num_2.hide()
            self.label_sw_num_2_int.hide()
            self.label_sw_pkt_2.hide()
            self.label_sw_pkt_2_int.hide()

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
        Dialog.setWindowIcon(QtGui.QIcon(logo_path))
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
            gridlayout.addWidget(self.cb_confirm, 2, 0, 1, 1, QtCore.Qt.AlignTop)
            self.label_checkbox = create_new_label(
                Dialog,
                "Hiermit bestätige ich, dass ich die eingegebene Aufgabe eigenständig und\nunter Berücksichtigung des Urheberrechtsgesetzes verfasst habe.\n"
                "Ich stelle die eingegebene Aufgabe frei gemäß der Lizenz CC0 1.0 zur Verfügung.\n"
                "Die Aufgabe darf daher zu jeder Zeit frei verwendet, kopiert und verändert werden.",
                False,
                True,
            )
            self.label_checkbox.setStyleSheet("padding-bottom: 20px;")
            gridlayout.addWidget(self.label_checkbox, 2, 1, 1, 1, QtCore.Qt.AlignTop)
            self.label_checkbox.clicked.connect(self.label_checkbox_clicked)

        if self.creator_mode == "admin":
            self.combobox_in_official = create_new_combobox(Dialog)
            self.combobox_in_official.setStyleSheet(
                """
            QWidget {{
                background-color: white;
                color: black;
                selection-background-color: {0};
                selection-color: white;
            }}

            QComboBox::disabled {{
               background-color: gray; color: white; 
            }}
            """.format(
                    get_color(blue_7)
                )
            )
            self.combobox_in_official.addItem("offizielle Aufgabe")
            self.combobox_in_official.addItem("inoffizelle Aufgabe")
            if chosen_variation != None:
                number = chosen_variation.split(" - ")
                number = number[-1].split("_")
                if "i." in number:
                    self.combobox_in_official.setCurrentIndex(0)
                else:
                    self.combobox_in_official.setCurrentIndex(1)
                self.combobox_in_official.setEnabled(False)
            gridlayout.addWidget(self.combobox_in_official, 2, 0, 1, 1)

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
            self.confirmed = ["admin", self.combobox_in_official.currentIndex()]
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
