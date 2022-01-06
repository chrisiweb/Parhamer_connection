import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout
from PyQt5.QtCore import QMetaObject


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

SplashWindow.show()
