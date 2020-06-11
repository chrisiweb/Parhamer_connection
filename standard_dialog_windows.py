from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
from config import logo_path

def warning_window(text, informative_text="", titel="Warnung", detailed_text=""):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle(titel)
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setWindowIcon(QtGui.QIcon(logo_path))
    msg.setText(text)
    msg.setInformativeText(detailed_text)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()

def information_window(text, informative_text="", titel="Information", detailed_text=""):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle(titel)
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setWindowIcon(QtGui.QIcon(logo_path))
    msg.setText(text)
    msg.setDetailedText(detailed_text)
    msg.setInformativeText(informative_text)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()

def question_window(text, informative_text="", titel ="Sind sie sicher?", detailed_text=""):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Question)
    msg.setWindowIcon(QtGui.QIcon(logo_path))
    msg.setWindowTitle(titel)
    msg.setText(text)
    msg.setInformativeText(informative_text)
    msg.setDetailedText(detailed_text)
    msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    
    buttonY = msg.button(QtWidgets.QMessageBox.Yes)
    buttonY.setText("Ja")
    buttonN = msg.button(QtWidgets.QMessageBox.No)
    buttonN.setText("Nein")
    response = msg.exec_()
    if response == QtWidgets.QMessageBox.No:
        return False
    if response == QtWidgets.QMessageBox.Yes:
        return True

def critical_window(text, informative_text="", titel="Fehlermeldung", detailed_text=""):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle(titel)
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setWindowIcon(QtGui.QIcon(logo_path))
    msg.setText(text)
    msg.setInformativeText(informative_text)
    msg.setDetailedText(detailed_text)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()

def custom_window(text, informative_text="", titel="LaMA - LaTeX Mathematik Assistent", detailed_text="", logo=logo_path):
    msg = QtWidgets.QMessageBox()

    pixmap = QtGui.QPixmap(logo)

    msg.setIconPixmap(pixmap.scaled(110, 110, QtCore.Qt.KeepAspectRatio))
    msg.setWindowIcon(QtGui.QIcon(logo_path))
    msg.setText(text)
    msg.setInformativeText(informative_text)
    msg.setWindowTitle(titel)
    msg.setDetailedText(detailed_text)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()


