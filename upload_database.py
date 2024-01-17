from PyQt5 import QtCore, QtWidgets, QtGui
from git_sync import check_internet_connection, git_push_to_origin
from processing_window import Ui_Dialog_processing
from standard_dialog_windows import critical_window, information_window
from functools import partial


class Worker_PushDatabase(QtCore.QObject):
    finished = QtCore.pyqtSignal()

    @QtCore.pyqtSlot()
    def task(self, ui, admin, file_list, message, worker_text):
        try:
            self.changes_found = git_push_to_origin(ui, admin, file_list, message, worker_text)
        except Exception as e:
            print('Fehler: {}'.format(e))
            self.changes_found = e

        self.finished.emit()


def action_push_database(admin, file_list, message = None, worker_text = "Aufgabe wird hochgeladen ..."):
    QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
    if check_internet_connection() == False:
        critical_window("Stellen Sie sicher, dass eine Verbindung zum Internet besteht und versuchen Sie es erneut.",
        titel="Keine Internetverbindung",
        )
        QtWidgets.QApplication.restoreOverrideCursor()
        return False


    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog_processing()
    ui.setupUi(Dialog, worker_text)

    thread = QtCore.QThread(Dialog)
    worker = Worker_PushDatabase()
    worker.finished.connect(Dialog.close)
    worker.moveToThread(thread)
    thread.started.connect(partial(worker.task, ui, admin, file_list, message, worker_text))
    thread.start()
    thread.exit()
    Dialog.exec()
    QtWidgets.QApplication.restoreOverrideCursor()
    print(worker.changes_found)
    if worker.changes_found == False:
        information_window("Es wurden keine Änderungen gefunden.")
    else:
        critical_window(f"{worker.changes_found}"
            )#"Es ist ein Fehler aufgetreten. Die Datenbank konnte nicht hochgeladen werden. Bitte versuchen Sie es später erneut."
        return False
    # elif admin == True:
    #     information_window("Die Datenbank wurde erfolgreich hochgeladen.")