from PyQt5 import QtCore, QtWidgets, QtGui
import os
import shutil
from functools import partial
from config import config_loader, path_programm, logo_path, logo_cria_path
from config import logo_path
from translate import _fromUtf8, _translate


class Ui_Dialog_choose_type(object):
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle(
            _translate("Titelplatt anpassen", "Programm auswählen", None)
        )
        Dialog.setWindowIcon(QtGui.QIcon(logo_path))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        # self.label_titlepage = QtWidgets.QLabel()
        # # # self.label_gk.setWordWrap(True)
        # self.label_titlepage.setObjectName(_fromUtf8("label_titlepage"))
        # self.label_titlepage.setText(
        #     _translate(
        #         "MainWindow",
        #         "Wählen Sie das gewünschte Programm aus:\n",
        #         None,
        #     )
        # )
        # self.gridLayout.addWidget(self.label_titlepage, 0,0,1,2)

        self.btn_lama_cria = QtWidgets.QPushButton()
        self.btn_lama_cria.setObjectName(_fromUtf8("btn_lama_cria"))
        # self.btn_lama_cria.setText("LaMA Cria (Unterstufe)")
        self.btn_lama_cria.setIcon(QtGui.QIcon(logo_cria_path))
        self.btn_lama_cria.setIconSize(QtCore.QSize(100,100))
        self.gridLayout.addWidget(self.btn_lama_cria, 0,0,1,1)
        self.label_lama_cria = QtWidgets.QLabel()
        self.label_lama_cria.setObjectName(_fromUtf8("label_lama_cria"))
        self.label_lama_cria.setText("LaMA Cria (Unterstufe)")
        self.gridLayout.addWidget(self.label_lama_cria, 1,0,1,1, QtCore.Qt.AlignCenter)
        # self.btn_lama_cria.setMaximumWidth(130)
        self.btn_lama_cria.clicked.connect(partial(self.choose_button_pressed, 'cria'))

        self.btn_lama = QtWidgets.QPushButton()
        self.btn_lama.setObjectName(_fromUtf8("btn_lama"))
        #self.btn_lama.setText("LaMA (Oberstufe)")
        self.btn_lama.setIcon(QtGui.QIcon(logo_path))
        self.btn_lama.setIconSize(QtCore.QSize(100,100))
        self.gridLayout.addWidget(self.btn_lama, 0,1,1,1)
        self.btn_lama.clicked.connect(partial(self.choose_button_pressed, 'lama'))
        self.label_lama = QtWidgets.QLabel()
        self.label_lama.setObjectName(_fromUtf8("label_lama"))
        self.label_lama.setText("LaMA (Oberstufe)")
        self.gridLayout.addWidget(self.label_lama, 1,1,1,1, QtCore.Qt.AlignCenter)

    def choose_button_pressed(self, chosen_program):
        self.chosen_program=chosen_program
        self.Dialog.accept()


class Ui_Dialog_titlepage(object):
    def setupUi(self, Dialog, dict_titlepage):
        # self.dict_titlepage = dict_titlepage
        # print(self.dict_titlepage)

        # self.ausgleichspunkte_split_text=ausgleichspunkte_split_text
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
        self.label_titlepage = QtWidgets.QLabel()
        # # self.label_gk.setWordWrap(True)
        self.label_titlepage.setObjectName(_fromUtf8("label_titlepage"))
        self.label_titlepage.setText(
            _translate(
                "MainWindow",
                "Wählen Sie die gewünschten Punkte für das Titelblatt aus:\n",
                None,
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


class Ui_Dialog_ausgleichspunkte(object):
    def setupUi(
        self, Dialog, ausgleichspunkte_split_text, list_sage_ausgleichspunkte_chosen
    ):
        # print(list_sage_ausgleichspunkte_chosen)
        self.ausgleichspunkte_split_text = ausgleichspunkte_split_text
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        self.Dialog.resize(600, 400)
        self.Dialog.setWindowIcon(QtGui.QIcon(logo_path))
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
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
        row = 1
        cb_counter = 0

        for all in self.ausgleichspunkte_split_text:
            cb_counter = self.create_checkbox_ausgleich(
                all, row, cb_counter, list_sage_ausgleichspunkte_chosen
            )
            row += 1

        self.label_solution = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_solution.setWordWrap(True)
        self.label_solution.setObjectName("label_solution")
        self.label_solution.setText("\nLösungserwartung:\n[...]")
        self.gridLayout.addWidget(self.label_solution, row, 1, 1, 3, QtCore.Qt.AlignTop)
        row += 1
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.Dialog)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.Dialog)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )

        buttonX = self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel)
        buttonX.setText("Abbrechen")
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.rejected.connect(self.Dialog.reject)
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.buttonBox.accepted.connect(
            partial(self.pushButton_OK_pressed, list_sage_ausgleichspunkte_chosen)
        )
        self.retranslateUi(self.Dialog)
        QtCore.QMetaObject.connectSlotsByName(self.Dialog)

        # return list_sage_ausgleichspunkte_chosen

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(
            _translate("Ausgleichspunkte anpassen", "Ausgleichspunkte anpassen")
        )

    def create_checkbox_ausgleich(
        self, linetext, row, cb_counter, list_sage_ausgleichspunkte_chosen
    ):
        counter = row - 1
        if "GRAFIK" in linetext:
            pass
        else:
            exec(
                "self.checkBox_{} = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)".format(
                    counter
                )
            )
            checkBox = eval("self.checkBox_{}".format(counter))
            checkBox.setMaximumSize(QtCore.QSize(20, 16777215))
            # self.checkBox.setText("")
            checkBox.setObjectName("checkBox_{}".format(counter))
            self.gridLayout.addWidget(checkBox, row, 0, 1, 1, QtCore.Qt.AlignTop)
            cb_counter += 1

        exec(
            "self.label_{} = QtWidgets.QLabel(self.scrollAreaWidgetContents)".format(
                counter
            )
        )
        label = eval("self.label_{}".format(counter))
        label.setWordWrap(True)
        label.setObjectName("label_{}".format(counter))
        if "\\fbox{A}" in linetext:
            linetext = linetext.replace("\\fbox{A}", "")
        if linetext in list_sage_ausgleichspunkte_chosen:
            checkBox.setChecked(True)

        label.setText(linetext)
        self.gridLayout.addWidget(label, row, 1, 1, 2, QtCore.Qt.AlignTop)
        return cb_counter

    def pushButton_OK_pressed(self, list_sage_ausgleichspunkte_chosen):
        # print(len(self.ausgleichspunkte_split_text))
        for i in range(0, len(self.ausgleichspunkte_split_text)):
            try:
                checkBox = eval("self.checkBox_{}".format(i))
                if (
                    eval("self.label_{}".format(i)).text()
                    in list_sage_ausgleichspunkte_chosen
                ):
                    if checkBox.isChecked() == False:
                        list_sage_ausgleichspunkte_chosen.remove(
                            eval("self.label_{}".format(i)).text()
                        )
                else:
                    if checkBox.isChecked() == True:
                        list_sage_ausgleichspunkte_chosen.append(
                            eval("self.label_{}".format(i)).text()
                        )

            except AttributeError:
                pass

        # print(list_sage_ausgleichspunkte_chosen)

        self.Dialog.reject()
        # print(list_sage_ausgleichspunkte_chosen)
        # self.list_sage_ausgleichspunkte_chosen=list_sage_ausgleichspunkte_chosen
        return list_sage_ausgleichspunkte_chosen

class Ui_Dialog_erstellen(QtWidgets.QDialog):
    def setupUi(
        self,
        Dialog,
        dict_list_input_examples,
        beispieldaten_dateipfad_1,
        beispieldaten_dateipfad_2,
        dict_titlepage,
        saved_file_path,
    ):
        self.dict_list_input_examples = dict_list_input_examples
        self.beispieldaten_dateipfad_1 = beispieldaten_dateipfad_1
        self.beispieldaten_dateipfad_2 = beispieldaten_dateipfad_2
        self.dict_titlepage = dict_titlepage
        self.data_gesamt = self.dict_list_input_examples["data_gesamt"]
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
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        # return pdf

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
        if self.cb_create_pdf.isChecked():
            self.pdf = True
        else:
            self.pdf = False

        if self.cb_create_lama.isChecked():
            self.lama = True
        else:
            self.lama = False   

        self.Dialog.accept()

