from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
from config import logo_path

def warning_window(text, detailed_text="", titel="Warnung", informative_text=""):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle(titel)
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setWindowIcon(QtGui.QIcon(logo_path))
    msg.setText(text)
    msg.setInformativeText(detailed_text)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()



def question_window(titel, text, informative_text="", detailed_text=""):
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

def critical_window(text, detailed_text="", titel="Fehlermeldung", informative_text=""):
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle(titel)
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setWindowIcon(QtGui.QIcon(logo_path))
    msg.setText(text)
    msg.setInformativeText(detailed_text)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()

