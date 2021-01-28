from PyQt5 import QtCore, QtWidgets, QtGui
# from PyQt5.QtWidgets import QMainWindow, QApplication
from config import (
    colors_ui,
    get_color,
    logo_path,
    logo_cria_button_path,
)
from waitingspinnerwidget import QtWaitingSpinner

blue_7 = colors_ui["blue_7"]

class Ui_Dialog_processing(object):
    def setupUi(self, Dialog, text, icon=True):
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        Dialog.setWindowFlags(
            QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint
        )
        Dialog.setWindowTitle("Lade...")
        Dialog.setStyleSheet(
            "background-color: {}; color: white".format(get_color(blue_7))
        )
        # Dialog.setSizePolicy(SizePolicy_fixed)
        # Dialog.setFixedSize(Dialog.size())
        if icon == True:
            pixmap = QtGui.QPixmap(logo_path)
            Dialog.setWindowIcon(QtGui.QIcon(logo_path))
        # Dialog.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed))
        horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        horizontalLayout.setObjectName("horizontal")
        horizontalLayout.setSizeConstraint(QtWidgets.QHBoxLayout.SetFixedSize)

        if icon == True:
            pixmap = QtGui.QPixmap(logo_cria_button_path)
            # Dialog.setPixmap(pixmap.scaled(110, 110, QtCore.Qt.KeepAspectRatio))
            image = QtWidgets.QLabel(Dialog)
            image.setObjectName("image")
            image.setPixmap(pixmap.scaled(30, 30, QtCore.Qt.KeepAspectRatio))

        label = QtWidgets.QLabel(Dialog)
        label.setObjectName("label")
        label.setText(text)
        label.setStyleSheet("padding: 20px")
        label_spinner = QtWidgets.QLabel(Dialog)
        label.setObjectName("label_spinner")
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
        label.setAlignment(QtCore.Qt.AlignCenter)
        if icon == True:
            horizontalLayout.addWidget(image)
        horizontalLayout.addWidget(label)
        horizontalLayout.addWidget(label_spinner)