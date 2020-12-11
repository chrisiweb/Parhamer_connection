# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'define_database.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class Ui_DefineDatabaseWindow(object):
    def setupUi(self, DefineDatabaseWindow):
        # self.DefineDatabaseWindow = DefineDatabaseWindow
        DefineDatabaseWindow.setObjectName("DefineDatabaseWindow")
        DefineDatabaseWindow.resize(548, 330)
        self.centralwidget = QtWidgets.QWidget(DefineDatabaseWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_define_database = QtWidgets.QLabel(self.centralwidget)
        self.label_define_database.setObjectName("label_define_database")
        self.verticalLayout_2.addWidget(self.label_define_database)
        self.buttonBox_define_database = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox_define_database.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        buttonS = self.buttonBox_define_database.button(QtWidgets.QDialogButtonBox.Save)
        buttonS.setText('Speichern')
        buttonX = self.buttonBox_define_database.button(QtWidgets.QDialogButtonBox.Cancel)
        buttonX.setText("Abbrechen")
        self.buttonBox_define_database.rejected.connect(self.window_rejected)
        self.buttonBox_define_database.accepted.connect(self.window_accepted)
        self.buttonBox_define_database.setObjectName("buttonBox_define_database")
        self.verticalLayout_2.addWidget(self.buttonBox_define_database)
        DefineDatabaseWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(DefineDatabaseWindow)
        self.statusbar.setObjectName("statusbar")
        DefineDatabaseWindow.setStatusBar(self.statusbar)

        self.retranslateUi(DefineDatabaseWindow)
        QtCore.QMetaObject.connectSlotsByName(DefineDatabaseWindow)
        return True
    def window_rejected(self):
        sys.exit("test")
        # print(self)
        # self.reject()
        # self.DefineDatabaseWindow.reject()
    
    def window_accepted(self):
        print(self)
        self.accept()


    def retranslateUi(self, DefineDatabaseWindow):
        _translate = QtCore.QCoreApplication.translate
        DefineDatabaseWindow.setWindowTitle(_translate("DefineDatabaseWindow", "MainWindow"))
        self.label_define_database.setText(_translate("DefineDatabaseWindow", "TextLabel"))


