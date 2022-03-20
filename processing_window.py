from pydoc import plain
from PyQt5 import QtCore, QtWidgets, QtGui
# from PyQt5.QtWidgets import QMainWindow, QApplication
from config import (
    colors_ui,
    get_color,
    logo_path,
    logo_cria_button_path,
)
from predefined_size_policy import SizePolicy_maximum_height
from waitingspinnerwidget import QtWaitingSpinner
from functools import partial
from create_new_widgets import create_new_verticallayout, create_new_gridlayout, create_new_label

blue_7 = colors_ui["blue_7"]

class Ui_Dialog_processing(object):
    def setupUi(self, Dialog, worker_text, show_output = False, icon=True):
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")

        Dialog.setWindowTitle("Lade...")
        Dialog.setStyleSheet(
            "background-color: {}; color: white".format(get_color(blue_7))
        )
        # Dialog.setSizePolicy(SizePolicy_fixed)
        # Dialog.setFixedSize(Dialog.size())
        # Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        if icon == True:
            pixmap = QtGui.QPixmap(logo_path)
            Dialog.setWindowIcon(QtGui.QIcon(logo_path))
            Dialog.setWindowFlags(
                QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint
            )
        else:
            Dialog.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        # Dialog.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        gridLayout = create_new_gridlayout(Dialog)
        gridLayout.setSizeConstraint(QtWidgets.QHBoxLayout.SetFixedSize)

        if icon == True:
            pixmap = QtGui.QPixmap(logo_cria_button_path)
            # Dialog.setPixmap(pixmap.scaled(110, 110, QtCore.Qt.KeepAspectRatio))
            image = QtWidgets.QLabel(Dialog)
            image.setObjectName("image")
            image.setPixmap(pixmap.scaled(30, 30, QtCore.Qt.KeepAspectRatio))

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.label.setText(worker_text)
        self.label.setStyleSheet("padding: 20px")
        label_spinner = QtWidgets.QLabel(Dialog)
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
        spinner.setColor(QtCore.Qt.white)
        spinner.start()  # starts spinning
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        if icon == True:
            gridLayout.addWidget(image, 0,0,1,1)
        gridLayout.addWidget(self.label, 0,1,1,1)
        gridLayout.addWidget(label_spinner, 0,2,1,1)
        if show_output == True:
            self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
            self.plainTextEdit.setReadOnly(True)
            self.plainTextEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.plainTextEdit.setPlainText("Creating pdf-file ...")
            self.plainTextEdit.setFixedHeight(70)
            gridLayout.addWidget(self.plainTextEdit, 1,0,1,3)



class Ui_ProgressBar(object):
    def setupUi(self, Dialog, max_value):
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")

        Dialog.setWindowTitle("Lade...")
        # Dialog.setStyleSheet(
        #     "background-color: {}; color: white".format(get_color(blue_7))
        # )

        verticallayout = create_new_verticallayout(Dialog)
        # Dialog.setSizePolicy(SizePolicy_fixed)
        # Dialog.setFixedSize(Dialog.size())
        # Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # if icon == True:
        #     pixmap = QtGui.QPixmap(logo_path)
        #     Dialog.setWindowIcon(QtGui.QIcon(logo_path))
        #     Dialog.setWindowFlags(
        #         QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint
        #     )
        # else:
        #     Dialog.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        # # Dialog.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        # horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        # horizontalLayout.setObjectName("horizontal")
        # horizontalLayout.setSizeConstraint(QtWidgets.QHBoxLayout.SetFixedSize)

        # if icon == True:
        #     pixmap = QtGui.QPixmap(logo_cria_button_path)
        #     # Dialog.setPixmap(pixmap.scaled(110, 110, QtCore.Qt.KeepAspectRatio))
        #     image = QtWidgets.QLabel(Dialog)
        #     image.setObjectName("image")
        #     image.setPixmap(pixmap.scaled(30, 30, QtCore.Qt.KeepAspectRatio))

        label = create_new_label(Dialog, "Lade LaMA-Datei ...")
        # self.label = QtWidgets.QLabel(Dialog)
        # self.label.setObjectName("label")
        # self.label.setText("Lade LaMA-Datei ...")
        label.setStyleSheet("padding: 20px")
        verticallayout.addWidget(label)

        self.progressbar = QtWidgets.QProgressBar()
        self.progressbar.setValue(50)
        self.progressbar.setStyleSheet("QProgressBar::chunk {background-color: white}")
        self.progressbar.setMaximum(max_value)
        verticallayout.addWidget(self.progressbar)

        # label_spinner = QtWidgets.QLabel(Dialog)
        # self.label.setObjectName("label_spinner")
        # label_spinner.setFixedSize(30, 30)
        # spinner = QtWaitingSpinner(label_spinner)
        # spinner.setRoundness(70.0)
        # # spinner.setMinimumTrailOpacity(10.0)
        # # spinner.setTrailFadePercentage(60.0)
        # spinner.setNumberOfLines(15)
        # spinner.setLineLength(8)
        # # spinner.setLineWidth(5)
        # spinner.setInnerRadius(5)
        # # spinner.setRevolutionsPerSecond(2)
        # spinner.setColor(QtCore.Qt.white)
        # spinner.start()  # starts spinning
        # self.label.setAlignment(QtCore.Qt.AlignCenter)
        # if icon == True:
        #     horizontalLayout.addWidget(image)
        # horizontalLayout.addWidget(self.label)
        # horizontalLayout.addWidget(label_spinner)


def working_window(worker, text, *args):
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog_processing()
    ui.setupUi(Dialog, text)

    thread = QtCore.QThread(Dialog)
    # worker = Worker_RefreshDDB()
    worker.finished.connect(Dialog.close)
    worker.moveToThread(thread)
    thread.started.connect(partial(worker.task, *args))
    thread.start()
    thread.exit()
    Dialog.exec()




def working_window_latex_output(worker, text, *args):
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog_processing()

    ui.setupUi(Dialog, text, show_output=True)

    ui.latex_error_occured = False
    thread = QtCore.QThread(Dialog)
    # worker = Worker_RefreshDDB()
    worker.signalUpdateOutput.connect(signalUpdateOutput)
    worker.finished.connect(Dialog.close)
    worker.moveToThread(thread)

    thread.started.connect(partial(worker.task,ui, *args)) 
    thread.start()
    thread.exit()
    Dialog.exec()
    
    return ui.latex_error_occured





def signalUpdateOutput(ui, msg):
    ui.plainTextEdit.appendPlainText(msg)