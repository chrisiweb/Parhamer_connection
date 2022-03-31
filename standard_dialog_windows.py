from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QWidget, QCheckBox
from config import logo_path
from create_new_widgets import create_new_gridlayout


def warning_window(text, detailed_text="", titel="Warnung", informative_text=""):
    msg = QMessageBox()
    msg.setWindowTitle(titel)
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowIcon(QIcon(logo_path))
    msg.setText(text)
    msg.setInformativeText(detailed_text)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def information_window(
    text, informative_text="", titel="Information", detailed_text=""
):
    msg = QMessageBox()
    msg.setWindowTitle(titel)
    msg.setIcon(QMessageBox.Information)
    msg.setWindowIcon(QIcon(logo_path))
    msg.setText(text)
    msg.setDetailedText(detailed_text)
    msg.setInformativeText(informative_text)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def question_window(
    text, informative_text="", titel="Sind Sie sicher?", detailed_text="", buttontext_yes="Ja", buttontext_no = "Nein", default="yes"
):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)
    msg.setWindowIcon(QIcon(logo_path))
    msg.setWindowTitle(titel)
    msg.setText(text)
    msg.setInformativeText(informative_text)
    msg.setDetailedText(detailed_text)
    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    if default == "no":
        msg.setDefaultButton(QMessageBox.No)
    buttonY = msg.button(QMessageBox.Yes)
    buttonY.setText(buttontext_yes)
    buttonN = msg.button(QMessageBox.No)
    buttonN.setText(buttontext_no)
    response = msg.exec_()
    if response == QMessageBox.No:
        return False
    if response == QMessageBox.Yes:
        return True


def critical_window(text, informative_text="", titel="Fehlermeldung", detailed_text="", sendbutton = False, OKButton_text = None, set_width = None):
    msg = QMessageBox()
    msg.setWindowTitle(titel)
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowIcon(QIcon(logo_path))
    msg.setText(text)
    msg.setInformativeText(informative_text)
    msg.setDetailedText(detailed_text)
    if sendbutton == True:
        msg.setStandardButtons(QMessageBox.Ok| QMessageBox.Apply)
        buttonApply = msg.button(QMessageBox.Apply)
        buttonApply.setText("Fehlerbericht senden")
    else:
        msg.setStandardButtons(QMessageBox.Ok)

    if OKButton_text!=None:
        buttonOK = msg.button(QMessageBox.Ok)
        buttonOK.setText(OKButton_text)



    if set_width != None:
        layout = msg.layout()
        widget = QWidget()
        widget.setFixedWidth(set_width)
        layout.addWidget(widget, 4,1,1,2)
    rsp = msg.exec_()
    if rsp == QMessageBox.Apply: 
        return True



def custom_window(
    text,
    informative_text="",
    titel="LaMA - LaTeX Mathematik Assistent",
    detailed_text="",
    logo=logo_path,
    set_width=None,
    show_checkbox = False,
):
    msg = QMessageBox()

    # msg.setStyleSheet("QLabel{min-width:  400px;}")
    if logo != False:
        pixmap = QPixmap(logo)

        msg.setIconPixmap(pixmap.scaled(110, 110, Qt.KeepAspectRatio))
        msg.setWindowIcon(QIcon(logo_path))
    msg.setText(text)
    msg.setInformativeText(informative_text)
    msg.setWindowTitle(titel)
    msg.setDetailedText(detailed_text)
    cb = QCheckBox()
    if show_checkbox==True:
        msg.setCheckBox(cb)
        cb.setText("Diese Meldung nicht mehr anzeigen")
    msg.setStandardButtons(QMessageBox.Ok)
    if set_width != None:
        layout = msg.layout()
        widget = QWidget()
        widget.setFixedWidth(set_width)
        layout.addWidget(widget, 4,1,1,2)


    # horizontalspacer = QSpacerItem(
    #     500, 0, QSizePolicy.Minimum, QSizePolicy.Expanding
    # )
    # layout = msg.layout()
    # layout.addItem(horizontalspacer)
    msg.exec_()
    return cb.isChecked()

