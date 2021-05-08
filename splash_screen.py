import sys
from os.path import join
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QMetaObject
from PyQt5.QtGui import QPixmap
from config import path_programm


splash_app = QApplication(sys.argv)
SplashWindow = QMainWindow()

centralwidget = QWidget(SplashWindow)
centralwidget.setObjectName("centralwidget")
verticalLayout = QVBoxLayout(centralwidget)
verticalLayout.setObjectName("verticalLayout")
label = QLabel(centralwidget)
label.setObjectName("label")
label.setText('NEU')
verticalLayout.addWidget(label)

SplashWindow.setCentralWidget(centralwidget)
QMetaObject.connectSlotsByName(SplashWindow)
# SplashWindow.setWindowFlags()
# centralwidget = QWidget(SplashWindow)


# gridLayout = QGridLayout(centralwidget)
# gridLayout.setObjectName("gridLayout")
# verticalLayout = QVBoxLayout(SplashWindow)

# lbl_1 = QLabel('<font color = Green size=12><b> LaMA </b></font>')
# lbl_1.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)

# path = join(
#     path_programm, "_database", "_config", "icon", "LaMA_logo_full.png"
# )
# pixmap = QPixmap(path)
# image = QLabel(SplashWindow)
# image.setObjectName("image")
# # lbl_2 = QLabel('<font color = Green size=12><b> LaMA </b></font>')
# image.setPixmap(pixmap.scaled(500, 500, Qt.KeepAspectRatio)) #
# verticalLayout.addWidget(image)
# lbl = QLabel(SplashWindow)
# lbl.setText('test')
# verticalLayout.addWidget(lbl)


# SplashWindow.setCentralWidget(centralwidget)

# QTimer.singleShot(2000, app.quit)

# lbl_1.show()
# lbl_2.show()
# pixmap.show()
SplashWindow.show()
# label.show()
# splash_app.exec()
# 