from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication
from config import logo_path

def warning_window(text, detailed_text="", titel="Warnung"):
    QtWidgets.QApplication.restoreOverrideCursor()
    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle(titel)
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setWindowIcon(QtGui.QIcon(logo_path))
    msg.setText(text)
    msg.setInformativeText(detailed_text)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()