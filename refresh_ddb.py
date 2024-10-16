from PyQt5 import QtCore, QtWidgets, QtGui
import os
import datetime
from config_start import database, path_programm
from config import config_file, config_loader, is_empty, get_icon_path
from processing_window import working_window
from database_commands import _database_addon
from standard_dialog_windows import question_window
from git_sync import git_reset_repo_to_origin, check_for_changes, check_internet_connection
from standard_dialog_windows import warning_window, information_window, question_window, critical_window, custom_window
import urllib.request
import urllib.error
import requests
import json
import pathlib


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

        Ui_MainWindow.missing_images_addon = []
        if _database_addon != None:
            try:
                download_link = 'https://www.dropbox.com/scl/fi/cw0hfmmo5rjzssiasszha/_database_addon.json?rlkey=cl8d6cczi5ciot9ufr5ii9486&dl=1' #'https://www.dropbox.com/s/nezphxdbqip46cu/_database_addon.json?dl=1'

                saving_path = os.path.join(database, "_database_addon.json")
                    
                urllib.request.urlretrieve(download_link, saving_path)

            except urllib.error.HTTPError:
                print('Die erweiterte Datenbank konnte nicht aktualisiert werden, da der Downloadlink nicht mehr verfügbar ist.')

            try:
                download_link_images = 'https://www.dropbox.com/s/8xgh6p8zgl7xd96/list_of_images.json?dl=1'

                saving_path_images = os.path.join(path_programm, "Teildokument", "list_of_images_addon.txt")

                
                urllib.request.urlretrieve(download_link_images, saving_path_images)


                with open(saving_path_images, "r") as f:
                    new_list_images = json.load(f)

                folder_images_addon = os.path.join(database, "Bilder_addon")

                old_list_images = os.listdir(folder_images_addon)

                Ui_MainWindow.missing_images_addon = []
                for image in new_list_images:
                    if image not in old_list_images:
                        Ui_MainWindow.missing_images_addon.append(image)



            except urllib.error.HTTPError:
                print('BILDER: Die erweiterte Datenbank konnte nicht aktualisiert werden, da der Downloadlink nicht mehr verfügbar ist.')


        self.finished.emit()



def refresh_ddb(self, auto_update=False):
    # QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
    # print(auto_update)
    if self.developer_mode_active == True:
        text = 'Änderungen überprüfen ...'
    elif auto_update == 'mac':
        text = "Datenbank wird vor dem Update aktualisiert ..."
    else:
        link = "https://www.buymeacoffee.com/lama.schule"
        # if self.display_mode == 1:
        #     color = "rgb(88, 111, 124)"
        # else:
        color = "rgb(47, 69, 80)"
        text = "Datenbank wird aktualisiert. Bitte warten ..."

    if check_internet_connection()==False:
        # QtWidgets.QApplication.restoreOverrideCursor()
        
        custom_window(
            "Die Datenbank konnte nicht aktualisiert werden.",
            "Stellen Sie sicher, dass eine Verbindung zum Internet besteht und versuchen Sie es später erneut.",
            titel="Keine Internetverbindung",
            logo=get_icon_path('wifi-off.svg'),
            logo_size=80)
        # critical_window(
        #     "Die Datenbank konnte nicht aktualisiert werden.",
        #     "Stellen Sie sicher, dass eine Verbindung zum Internet besteht und versuchen Sie es später erneut.",
        #     titel="Keine Internetverbindung")
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
            # QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        link = "https://mylama.github.io/lama/"
        # if self.display_mode == 1:
        #     color = "rgb(88, 111, 124)"
        # else:
        color = "rgb(211, 224, 223)"
        text = "Datenbank wird aktualisiert. Bitte warten ..."

    working_window(Worker_RefreshDDB(), text, self,show_donation_notice=True)

    # QtWidgets.QApplication.restoreOverrideCursor()

    if not is_empty(self.missing_images_addon):
        string_missing_images = "\n".join(self.missing_images_addon)
        folder_images_addon = os.path.join(database, "Bilder_addon")
        link = "https://www.dropbox.com/sh/8aaybb7aflx5whj/AAB1ylEA69UbAHjHM1ztwRCga?dl=0"
        color = "rgb(47, 69, 80)"
        warning_window(f'Folgende(s) Bild(er) ist/sind derzeit nicht in der Datenbank vorhanden:\n\n{string_missing_images}',
        f"""Bitte laden Sie das/die fehlende(n) Bild(er) <a href='{link}'style='color:{color};'>manuell herunter</a> und kopieren Sie diese(s) in folgenden Ordner:<br><br>
        
        {folder_images_addon}""")
        # print(database)
        # saving_path = os.path.join(database, "_database_addon.json")

        # with open(saving_path, "wb") as f:
        #     f.write(url.content)

    

    elif auto_update == False or auto_update == 'mac':
        if self.reset_successfull == False:
            warning_window("Der neueste Stand der Datenbank konnte nicht heruntergeladen werden. Stellen Sie sicher, dass eine Verbindung zum Internet besteht und versuchen Sie es erneut.")
        else:           
            information_window("Die Datenbank ist jetzt auf dem neuesten Stand!")

