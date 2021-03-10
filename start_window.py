import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from create_new_widgets import create_new_gridlayout, create_new_label


class Ui_StartWindow(object):
    def setupUi(self, StartWindow):
        self.StartWindow = StartWindow
        StartWindow.setObjectName("StartWindow")
        StartWindow.setWindowTitle("Herzlich Willkommen bei LaMA")
        gridlayout = QtWidgets.QGridLayout()

        gridlayout.setObjectName("gridlayout")
        # gridlayout = create_new_gridlayout(StartWindow)
#         gridLayout = create_new_gridlayout(self.StartWindow)

        label_1 = create_new_label(self.StartWindow, """
Herlich Willkommen!

Es freut uns sehr, dass Sie sich für das Programm LaMA interessieren!
Um starten zu können, muss LaMA zu Beginn konfiguriert werden. Dazu muss die Aufgabendatenbank heruntergeladen werden.

Möchten Sie die Konfiguration beginnen und die Datenbank herunterladen?
            """)
        gridlayout.addWidget(label_1, 0,0,1,1)
        StartWindow.setLayout(gridlayout)


        self.buttonBox_welcome = QtWidgets.QDialogButtonBox(self.StartWindow)
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

        gridlayout.addWidget(self.buttonBox_welcome, 1,0,1,1)

    def cancel_pressed(self):
        sys.exit()

    def start_download(self):
        self.StartWindow.accept()

app = QApplication(sys.argv)

Dialog = QtWidgets.QDialog(
    None,
    QtCore.Qt.WindowSystemMenuHint
    | QtCore.Qt.WindowTitleHint
    | QtCore.Qt.WindowCloseButtonHint,
)
ui = Ui_StartWindow()
ui.setupUi(Dialog)
Dialog.show()

app.exec()