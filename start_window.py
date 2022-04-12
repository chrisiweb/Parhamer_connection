import sys
import os
from config_start import database
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QGridLayout, QDialogButtonBox, QDialog, QMessageBox
from waitingspinnerwidget import QtWaitingSpinner
from git_sync import git_clone_repo
# from standard_dialog_windows import information_window, critical_window


class Worker_DownloadDatabase(QObject):
    finished = pyqtSignal()

    @pyqtSlot()
    def task(self):
        self.download_successfull = git_clone_repo()
        self.finished.emit()   

class Ui_Dialog_processing(object):
    def setupUi(self, Dialog, text):
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")

        Dialog.setWindowTitle("Lade...")
        Dialog.setStyleSheet(
            "background-color: {}; color: white".format("rgb(47, 69, 80)")
        )

        Dialog.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        # Dialog.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        horizontalLayout = QHBoxLayout(Dialog)
        horizontalLayout.setObjectName("horizontal")
        horizontalLayout.setSizeConstraint(QHBoxLayout.SetFixedSize)

        # if icon == True:
        #     pixmap = QtGui.QPixmap(logo_cria_button_path)
        #     # Dialog.setPixmap(pixmap.scaled(110, 110, Qt.KeepAspectRatio))
        #     image = QLabel(Dialog)
        #     image.setObjectName("image")
        #     image.setPixmap(pixmap.scaled(30, 30, Qt.KeepAspectRatio))

        self.label = QLabel(Dialog)
        self.label.setObjectName("label")
        self.label.setText(text)
        self.label.setStyleSheet("padding: 20px")
        label_spinner = QLabel(Dialog)
        self.label.setObjectName("label_spinner")
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
        spinner.setColor(Qt.white)
        spinner.start()  # starts spinning
        self.label.setAlignment(Qt.AlignCenter)
        # if icon == True:
        #     horizontalLayout.addWidget(image)
        horizontalLayout.addWidget(self.label)
        horizontalLayout.addWidget(label_spinner)



class Ui_StartWindow(object):
    # def __init__(self):
    #     if os.path.isdir(database):

    def setupUi(self, StartWindow):
        self.StartWindow = StartWindow
        StartWindow.setObjectName("StartWindow")
        StartWindow.setWindowTitle("Herzlich Willkommen bei LaMA!")
        gridlayout = QGridLayout()

        gridlayout.setObjectName("gridlayout")
        # gridlayout = create_new_gridlayout(StartWindow)
#         gridLayout = create_new_gridlayout(self.StartWindow)
        label_1 = QLabel(self.StartWindow)
        label_1.setObjectName("label_1")

        text = """

            **    **
            **    **                                                          Herzlich Willkommen! Es freut uns sehr, dass Sie sich für das Programm LaMA interessieren!
    **********                                                                             
    **********
    **********                                                                                                                             
                ****                                                          LaMA ist eine Open-Source Aufgaben-Datenbank, die Mathematiklehrer\xb7innen bei der    
                ****                            ***                       
                ****                            ***                        Erstellung von Schularbeiten, Grundkompetenzchecks, Übungsblättern usw. unterstützen soll.
                *********************                    
                *********************                                                          
                *********************                        
                ****                          ****                         Um starten zu können, muss LaMA zu Beginn konfiguriert werden. Dazu muss die Aufgabendatenbank heruntergeladen werden.
                ****                          ****                           
                ****                          ****                         Möchten Sie die Konfiguration beginnen und die Datenbank herunterladen?

            """
                
        label_1.setText(text)
        gridlayout.addWidget(label_1, 0,0,1,1)
        StartWindow.setLayout(gridlayout)


        self.buttonBox_welcome = QDialogButtonBox(self.StartWindow)
        self.buttonBox_welcome.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        # buttonS = self.buttonBox_titlepage.button(QDialogButtonBox.Save)
        # buttonS.setText('Speichern')
        buttonX = self.buttonBox_welcome.button(QDialogButtonBox.Cancel)
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
            Dialog_download = QDialog()
            ui = Ui_Dialog_processing()
            ui.setupUi(Dialog_download, text)

            thread = QThread(Dialog_download)
            worker = Worker_DownloadDatabase()
            worker.finished.connect(Dialog_download.close)
            worker.moveToThread(thread)
            rsp = thread.started.connect(worker.task)
            thread.start()
            thread.exit()
            Dialog_download.exec()
            # download_successfull = True

            if worker.download_successfull == True:                
                text = "Die Datenbank wurde erfolgreich heruntergeladen. LaMA kann ab sofort verwendet werden!"
                msg = QMessageBox()
                msg.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
                msg.setWindowTitle("Datenbank heruntergeladen")
                msg.setIcon(QMessageBox.Information)
                # msg.setWindowIcon(QtGui.QIcon(logo_path))
                msg.setText(text)
                # msg.setDetailedText(detailed_text)
                # msg.setInformativeText(informative_text)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

                break
            else:
                text = """
    Datenbank konnte nicht heruntergeladen werden. Stellen Sie sicher, dass eine Verbindung zum Internet besteht und versuchen Sie es erneut.

    Sollte das Problem weiterhin bestehen, melden Sie sich unter lama.helpme@gmail.com
                """
                msg = QMessageBox()
                msg.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
                msg.setWindowTitle("Fehler")
                msg.setIcon(QMessageBox.Critical)
                # msg.setWindowIcon(QtGui.QIcon(logo_path))
                msg.setText(text)
                # msg.setInformativeText(informative_text)
                msg.setDetailedText("Error: {}".format(worker.download_successfull))
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

                buttonRepeat = msg.button(QMessageBox.Ok)
                buttonRepeat.setText("Wiederholen")

                buttonX = msg.button(QMessageBox.Cancel)
                buttonX.setText("Abbrechen")
                
                rsp = msg.exec_()

                if rsp == QMessageBox.Cancel:
                    sys.exit(0)
                else:
                    continue
    #         except Exception as e:
    #             text = """
    # Datenbank konnte nicht heruntergeladen werden. Stellen Sie sicher, dass eine Verbindung zum Internet besteht und versuchen Sie es erneut.

    # Sollte das Problem weiterhin bestehen, melden Sie sich unter lama.helpme@gmail.com
    #             """
    #             msg = QMessageBox()
    #             msg.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
    #             msg.setWindowTitle("Fehler")
    #             msg.setIcon(QMessageBox.Critical)
    #             # msg.setWindowIcon(QtGui.QIcon(logo_path))
    #             msg.setText(text)
    #             # msg.setInformativeText(informative_text)
    #             msg.setDetailedText("Error: {}".format(e))
    #             msg.setStandardButtons(QMessageBox.Ok)
    #             msg.exec_()
    #             continue                       
    
        print("LaMA wird gestartet ...")
        self.StartWindow.accept()


def check_if_database_exists():  
    config_file = os.path.join(database, "_config", "config.yml")

    if not os.path.isfile(config_file):
        app = QApplication(sys.argv)

        Dialog = QDialog(
            None,
            Qt.WindowSystemMenuHint
            | Qt.WindowTitleHint
            | Qt.WindowCloseButtonHint,
        )
        Dialog.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        ui = Ui_StartWindow()
        ui.setupUi(Dialog)
        Dialog.show()

        app.exec()

