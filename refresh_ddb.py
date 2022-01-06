from PyQt5 import QtCore, QtWidgets, QtGui
import os
import datetime
from config_start import database
from config import config_file, config_loader, is_empty
from processing_window import working_window
from standard_dialog_windows import question_window
from git_sync import git_reset_repo_to_origin, check_for_changes, check_internet_connection
from standard_dialog_windows import warning_window, information_window, question_window, critical_window


list_klassen = config_loader(config_file, "list_klassen")


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)



class Worker_CheckChanges(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    @QtCore.pyqtSlot()
    def task(self, Ui_MainWindow):
        Ui_MainWindow.worker_response = []
        modified_files, new_files = check_for_changes(database)

        if modified_files !=[] or new_files != []:
            modified = b", ".join(modified_files)
            modified = modified.decode()
            new = ", ".join(new_files)

            Ui_MainWindow.worker_response = [modified, new]
        self.finished.emit()


class Worker_RefreshDDB(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    @QtCore.pyqtSlot()
    def task(self, Ui_MainWindow):              
        Ui_MainWindow.reset_successfull = git_reset_repo_to_origin()

        self.finished.emit()



def refresh_ddb(self, auto_update=False):
    QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))

    if self.developer_mode_active == True:
        text = 'Änderungen überprüfen ...'
    elif auto_update == 'mac':
        text = "Datenbank wird vor dem Update aktualisiert ..."
    else:
        text = "Datenbank wird aktualisiert. Bitte warten ..."

    if check_internet_connection()==False:
        QtWidgets.QApplication.restoreOverrideCursor()
        critical_window("""
Stellen Sie sicher, dass eine Verbindung zum Internet besteht und versuchen Sie es erneut.
        """, titel="Keine Internetverbindung")
        return

    if self.developer_mode_active == True:        
        working_window(Worker_CheckChanges(), text, self)
        if not is_empty(self.worker_response):
            QtWidgets.QApplication.restoreOverrideCursor()
            response= question_window("""
        Es befinden sich lokale Änderungen in Ihrer Datenbank. Durch das Aktualisieren der Datenbank werden alle lokalen Änderungen UNWIDERRUFLICH gelöscht!

        Lokale Änderungen können durch "Datei - Datenbank hochladen" online gespeichert werden. 

        Sind Sie sicher, dass Sie die lokalen Änderungen unwiderruflich löschen möchten? 
                    """, titel="Lokale Änderungen löschen?", detailed_text="""
        Geänderte/Gelöschte Dateien: {0} \n\n
        Neu erstellte Dateien: {1}            
                    """.format(self.worker_response[0], self.worker_response[1]), buttontext_yes="Lokale Änderungen löschen", buttontext_no="Abbrechen", default="no")    
            if response == False:
                return
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        text = "Datenbank wird aktualisiert. Bitte warten ..."

    working_window(Worker_RefreshDDB(), text, self)

    QtWidgets.QApplication.restoreOverrideCursor()

    if auto_update != True:
        if self.reset_successfull == False:
            warning_window("Der neueste Stand der Datenbank konnte nicht heruntergeladen werden. Stellen Sie sicher, dass eine Verbindung zum Internet besteht und versuchen Sie es erneut.")
        else:
            information_window("Die Datenbank ist jetzt auf dem neuesten Stand!")

