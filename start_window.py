import sys
import os
from config_start import database
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from create_new_widgets import create_new_gridlayout, create_new_label
from processing_window import Ui_Dialog_processing
from git_sync import git_clone_repo
from standard_dialog_windows import information_window, critical_window


class Worker_DownloadDatabase(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    @QtCore.pyqtSlot()
    def task(self):
        self.download_successfull = git_clone_repo()
        self.finished.emit()   



class Ui_StartWindow(object):
    # def __init__(self):
    #     if os.path.isdir(database):

    def setupUi(self, StartWindow):
        self.StartWindow = StartWindow
        StartWindow.setObjectName("StartWindow")
        StartWindow.setWindowTitle("Herzlich Willkommen bei LaMA!")
        gridlayout = QtWidgets.QGridLayout()

        gridlayout.setObjectName("gridlayout")
        # gridlayout = create_new_gridlayout(StartWindow)
#         gridLayout = create_new_gridlayout(self.StartWindow)

        label_1 = create_new_label(self.StartWindow, """

            **    **
            **    **                                                          Herzlich Willkommen! Es freut uns sehr, dass Sie sich für das Programm LaMA interessieren!
    **********                                                                             
    **********
    **********                                                                                                                             
                ****                                                          LaMA ist eine Open-Source Aufgaben-Datenbank, die Mathematiklehrer_innen bei der    
                ****                            ***                       
                ****                            ***                        Erstellung von Schularbeiten, Grundkompetenzchecks, Übungsblättern usw. unterstützen soll.
                *********************                    
                *********************                                                          
                *********************                        
                ****                          ****                         Um starten zu können, muss LaMA zu Beginn konfiguriert werden. Dazu muss die Aufgabendatenbank heruntergeladen werden.
                ****                          ****                           
                ****                          ****                         Möchten Sie die Konfiguration beginnen und die Datenbank herunterladen?

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
        while True:
            text = "Die Datenbank wird heruntergeladen.\n\nDies kann einige Minuten dauern ..."
            Dialog_download = QtWidgets.QDialog()
            ui = Ui_Dialog_processing()
            ui.setupUi(Dialog_download, text, False)

            thread = QtCore.QThread(Dialog_download)
            worker = Worker_DownloadDatabase()
            worker.finished.connect(Dialog_download.close)
            worker.moveToThread(thread)
            rsp = thread.started.connect(worker.task)
            thread.start()
            thread.exit()
            Dialog_download.exec()
            if worker.download_successfull == False:
                bring_to_front(critical_window("""
    Datenbank konnte nicht heruntergeladen werden. Stellen Sie sicher, dass eine Verbindung zum Internet besteht und versuchen Sie es erneut.

    Sollte das Problem weiterhin bestehen, melden Sie sich unter lama.helpme@gmail.com
    """))
                continue
            elif worker.download_successfull == True:
                information_window(
    """Die Datenbank wurde erfolgreich heruntergeladen. LaMA kann ab sofort verwendet werden!
    """
                )
                break
        print("Loading...")
        self.StartWindow.accept()


if not os.path.isdir(database):
    app = QApplication(sys.argv)

    Dialog = QtWidgets.QDialog(
        None,
        QtCore.Qt.WindowSystemMenuHint
        | QtCore.Qt.WindowTitleHint
        | QtCore.Qt.WindowCloseButtonHint,
    )
    Dialog.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
    ui = Ui_StartWindow()
    ui.setupUi(Dialog)
    Dialog.show()

    app.exec()
else:
    print(True)