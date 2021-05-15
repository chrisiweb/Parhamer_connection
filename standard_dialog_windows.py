from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from config import logo_path


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


def critical_window(text, informative_text="", titel="Fehlermeldung", detailed_text=""):
    msg = QMessageBox()
    msg.setWindowTitle(titel)
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowIcon(QIcon(logo_path))
    msg.setText(text)
    msg.setInformativeText(informative_text)
    msg.setDetailedText(detailed_text)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def custom_window(
    text,
    informative_text="",
    titel="LaMA - LaTeX Mathematik Assistent",
    detailed_text="",
    logo=logo_path,
):
    msg = QMessageBox()

    pixmap = QPixmap(logo)

    msg.setIconPixmap(pixmap.scaled(110, 110, Qt.KeepAspectRatio))
    msg.setWindowIcon(QIcon(logo_path))
    msg.setText(text)
    msg.setInformativeText(informative_text)
    msg.setWindowTitle(titel)
    msg.setDetailedText(detailed_text)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

