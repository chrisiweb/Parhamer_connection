import sys
import os
from config_start import database, path_programm
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QGridLayout, QDialogButtonBox, QDialog, QMessageBox
from waitingspinnerwidget import QtWaitingSpinner
from git_sync import git_clone_repo
import shutil
import re


phases_translation = {
    "Counting objects":"Objekte werden gezählt",
    "Compressing objects":"Objekte werden komprimiert",
    "copying pack entries":"Einträge werden kopiert",
    "generating index":"Index wird erstellt",
    
}




class QtProgressStream:
    def __init__(self, worker):
        self.worker = worker
        self._buf = b''
        # "(done/total)" in Klammern – z.B. "Counting objects:   3% (1/32)"
        self.RE_PAREN = re.compile(r'\((\d+)\s*/\s*(\d+)\)')

        # "done/total" ohne Klammern – z.B. "generating index: 15812/45533"
        self.RE_SLASH = re.compile(r'(\d+)\s*/\s*(\d+)')

        self.RE_PCT = re.compile(r'(\d+)\s*%')  # optional: Prozent extrahieren

    def parse_progress_line(self, line: str):
        phase = ''
        percent = None
        objects_done = None
        total_objects = None

        s = line.strip()
        parts = s.split(':', 1)
        phase = parts[0].strip() if parts else s
        right = parts[1].strip() if len(parts) > 1 else ''

        # Prozent (falls vorhanden)
        m_pct = self.RE_PCT.search(right or s)
        if m_pct:
            percent = int(m_pct.group(1))

        # Zuerst "(done/total)" versuchen
        m_paren = self.RE_PAREN.search(right)
        if m_paren:
            objects_done = int(m_paren.group(1))
            total_objects = int(m_paren.group(2))
        else:
            # Fallback: "done/total" ohne Klammern
            m_slash = self.RE_SLASH.search(right)
            if m_slash:
                objects_done = int(m_slash.group(1))
                total_objects = int(m_slash.group(2))

        return [phase, percent, objects_done, total_objects]




    def write(self, data):
        if isinstance(data, (bytes, bytearray)):
            text = data.decode(errors='ignore')
        else:
            text = str(data)


        global_percentage=0
        
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            line_output = self.parse_progress_line(line)
            phase = line_output[0]
            objects_done = line_output[-2]
            total_objects = line_output[-1]

            if phase!=None and objects_done!=None and total_objects!=None:
                try:
                    status_part = phases_translation[phase]
                    local_percentage = int(objects_done)/int(total_objects)
                    
                    if phase == "Compressing objects":
                        global_percentage += 1+round(7*local_percentage)
                    elif phase == "copying pack entries":
                        global_percentage += 8+ round(16*local_percentage)
                        objects_done = round(objects_done/10)
                        total_objects = round(total_objects/10)
                    elif phase == "generating index":
                        global_percentage += 24+round(77*local_percentage)
                        objects_done = round(objects_done/10)
                        total_objects = round(total_objects/10)                    

                    new_text = (
                        f"Die Datenbank wird heruntergeladen. ({global_percentage}%)\n\n"
                        f"{status_part} ... ({objects_done}/{total_objects})"
                    )
                    self.worker.progress_text.emit(new_text)
                except Exception:
                    pass
            # m = pattern.search(line)
            # if m:
            #     phase = m.group("phase").strip()
            #     objects_done = m.group("objects_done")
            #     total_objects = m.group("total_objects")
            #     print(phase, objects_done, total_objects)

            #     status_part = phases_translation[phase]

            #     new_text = (
            #         f"Die Datenbank wird heruntergeladen.\n\n"
            #         f"{status_part} ... ({objects_done}/{total_objects})"
            #     )
            #     self.worker.progress_text.emit(new_text)
            # Ausgabe: Counting objects 1 32

            # phase = split_line[0].strip() if split_line else ''
            
            # if len(split_line[1])>1:
            #     match = re.search(r'\((\d+)/(\d+)\)', split_line[1])
            #     # print(match.group(1))
            #     # print(match.group(2))
            #     if match:
            #         objects_done = match.group(1)  # "26"
            #         total_objects = match.group(2) # "32"
                
            #     print(phase)
            #     print(objects_done)
            #     print(total_objects)
            # match = re.search(r'Enumerating objects:\s*(\d+)', line)
            # if match:
            #     number_of_objects = int(match.group(1))
            #     print(f"NUMMER : {number_of_objects}")
            
            # # Prozent extrahieren
            # m = re.search(r'(\d+)%', line)
            # if m:
            #     percent = m.group(1)
            #     # Status aus der Zeile (z. B. "Receiving objects")
            #     # Wir nehmen den Teil vor dem Doppelpunkt, falls vorhanden
            #     status_part = line.split(':')[0]
                
                # Text zusammenbauen
                # new_text = (
                #     f"Die Datenbank wird heruntergeladen.\n\n"
                #     f"{status_part} ... ({percent}%)"
                # )
                # self.worker.progress_text.emit(new_text)
            # else:
            #     # Falls keine Prozentangabe, aber Status vorhanden
            #     self.worker.progress_text.emit(
            #         f"Die Datenbank wird heruntergeladen.\n\n{line}"
            #     )






class Worker_DownloadDatabase(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress_text = pyqtSignal(str)


    @pyqtSlot()
    def task(self):
        stream = QtProgressStream(self)
        self.download_successfull = git_clone_repo(errstream=stream)
 
        if self.download_successfull is True:
            self.finished.emit()
        else:
            # Falls git_clone_repo einen Fehler zurückgibt
            self.error.emit(str(self.download_successfull))
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

    def setupUi(self, StartWindow, reload_dbb):
        self.StartWindow = StartWindow
        StartWindow.setObjectName("StartWindow")
        gridlayout = QGridLayout()

        gridlayout.setObjectName("gridlayout")
        # gridlayout = create_new_gridlayout(StartWindow)
#         gridLayout = create_new_gridlayout(self.StartWindow)
        label_1 = QLabel(self.StartWindow)
        label_1.setObjectName("label_1")
        if reload_dbb == True:
            StartWindow.setWindowTitle("Datenbank erneuern")
            text = """<b>Augrund einer Änderung der Datenbank muss diese neu heruntergeladen werden.</b><br><br><br>

            Sollten dabei Problem auftreten, melden Sie sich bitte unter: lama.helpme@gmail.com<br>"""
        else:
            StartWindow.setWindowTitle("Herzlich Willkommen bei LaMA!")
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
        if reload_dbb == True:
           self.buttonBox_welcome.setStandardButtons(
                QDialogButtonBox.Ok
            )        
        else:
            self.buttonBox_welcome.setStandardButtons(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            )
            buttonX = self.buttonBox_welcome.button(QDialogButtonBox.Cancel)
            buttonX.setText("Abbrechen")
            self.buttonBox_welcome.rejected.connect(self.cancel_pressed)

        # buttonS = self.buttonBox_titlepage.button(QDialogButtonBox.Save)
        # buttonS.setText('Speichern')

        self.buttonBox_welcome.setObjectName("buttonBox_variation")
        self.buttonBox_welcome.accepted.connect(self.start_download)

        gridlayout.addWidget(self.buttonBox_welcome, 1,0,1,1)

    def cancel_pressed(self):
        sys.exit()

    def start_download(self):
        while True:
            text = (
                "Die Datenbank wird heruntergeladen... (1%)\n\n"
                "Objekte werden gezählt ..."
            )
            Dialog_download = QDialog()
            ui = Ui_Dialog_processing()
            ui.setupUi(Dialog_download, text)

            thread = QThread(Dialog_download)
            worker = Worker_DownloadDatabase()
            worker.finished.connect(Dialog_download.close)
            worker.moveToThread(thread)
            rsp = thread.started.connect(worker.task)
            worker.progress_text.connect(ui.label.setText)
            thread.start()
            thread.exit()
            Dialog_download.exec()

            if worker.download_successfull == True:                
                text = "Die Datenbank wurde erfolgreich heruntergeladen.\n\nLaMA kann ab sofort verwendet werden!"
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
                occured_error = worker.download_successfull
                if hasattr(worker.download_successfull, "winerror") and worker.download_successfull.winerror == 183:

                    defect_git_folder = os.path.join(database, ".git")
                    if os.path.exists(defect_git_folder):
                        try:
                            shutil.rmtree(defect_git_folder, ignore_errors=True)
                            continue
                        except Exception as e:
                            occured_error = f"{occured_error}\n\n{e}"
                
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
                msg.setDetailedText("Error: {}".format(occured_error))
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


def check_if_database_exists(reload_ddb = False):
    config_file = os.path.join(database, "_config", "config.yml")
    if not os.path.isfile(config_file):
        print(f"config in {config_file} does not exist")



    # if not os.path.isfile(config_file):
    #     if sys.platform.startswith("win"):
    #         programdata = os.getenv('PROGRAMDATA')
    #         database_old = os.path.join(programdata, "LaMA", "_database")
    #         config_file_old = os.path.join(database_old, "_config", "config.yml")

    #         if os.path.isfile(config_file_old):
    #             shutil.move(database_old, database)
    #             teildokument_old = os.path.join(programdata, "LaMA", "Teildokument")
    #             shutil.move(teildokument_old, os.path.join(path_programm, "Teildokument"))
    #             if os.path.isfile(config_file):
    #                 return
      


        app = QApplication(sys.argv)

        Dialog = QDialog(
            None,
            Qt.WindowSystemMenuHint
            | Qt.WindowTitleHint
            | Qt.WindowCloseButtonHint,
        )
        Dialog.setWindowFlags(Qt.Dialog | Qt.CustomizeWindowHint | Qt.WindowTitleHint)
        ui = Ui_StartWindow()
        ui.setupUi(Dialog, reload_ddb)
        Dialog.show()

        app.exec()

