# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'define_database.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
from predefined_size_policy import SizePolicy_fixed

class Ui_define_database(object):
    def setupUi(self, define_database):
        # print(self)
        self.define_database = define_database
        self.define_database.setObjectName("define_database")
        self.define_database.resize(375, 114)
        self.gridLayout = QtWidgets.QGridLayout(define_database)
        self.gridLayout.setObjectName("gridLayout")

        self.label_define_database = QtWidgets.QLabel(define_database)
        self.label_define_database.setObjectName("label_define_database")
        self.gridLayout.addWidget(self.label_define_database, 0,0,1,2)

        # self.lineedit_define_database = QtWidgets.QLineEdit(define_database)
        # self.lineedit_define_database.setObjectName("lineedit_define_database")
        # self.gridLayout.addWidget(self.lineedit_define_database, 1,0,1,1)

        self.button_define_database = QtWidgets.QPushButton(define_database)
        self.button_define_database.setObjectName("button_define_database")
        self.button_define_database.setText("Durchsuchen...")
        self.button_define_database.clicked.connect(self.button_define_database_clicked)
        self.button_define_database.setSizePolicy(SizePolicy_fixed)
        self.gridLayout.addWidget(self.button_define_database, 1,0,1,1)

        self.label_define_database_2 = QtWidgets.QLabel(define_database)
        self.label_define_database_2.setObjectName("label_define_database_2")
        self.gridLayout.addWidget(self.label_define_database_2, 1,1,1,1)

        self.label_define_database_3 = QtWidgets.QLabel(define_database)
        self.label_define_database_3.setObjectName("label_define_database_3")
        self.gridLayout.addWidget(self.label_define_database_3, 2,0,1,2)

        self.buttonBox_define_database = QtWidgets.QDialogButtonBox(define_database)
        self.buttonBox_define_database.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox_define_database.setObjectName("buttonBox_define_database")
        self.gridLayout.addWidget(self.buttonBox_define_database, 3,0,1,2)
        buttonS = self.buttonBox_define_database.button(QtWidgets.QDialogButtonBox.Save)
        buttonS.setText('Speichern')
        buttonS.setEnabled(False)
        buttonX = self.buttonBox_define_database.button(QtWidgets.QDialogButtonBox.Cancel)
        buttonX.setText("Abbrechen")
        self.buttonBox_define_database.rejected.connect(self.window_rejected)
        self.buttonBox_define_database.accepted.connect(self.window_accepted)        
        self.retranslateUi(define_database)
        QtCore.QMetaObject.connectSlotsByName(define_database)

    def retranslateUi(self, define_database):
        # _translate = QtCore.QCoreApplication.translate
        define_database.setWindowTitle("Herzlich Willkommen")
        self.label_define_database.setText("""
Herzlich Willkommen bei LaMA!

Bevor Sie starten können, müssen Sie den Dateipfad zur Datenbank angeben. 
""")

        self.label_define_database_3.setText("""
Sollten Sie noch keinen Zugriff auf die Datenbank erhalten haben, lesen Sie den
Installationsguide auf lama.schule oder wenden Sie sicn an helpme.lama@gmail.com.
        """)

    def button_define_database_clicked(self):
        self.path_database = QtWidgets.QFileDialog.getExistingDirectory(None, "Dateipfad wählen")
        if self.path_database != "":
            self.buttonBox_define_database.button(QtWidgets.QDialogButtonBox.Save).setEnabled(True)
        # QFileDialog.getFolder(
        #     None, "Dateipfad wählen", "", "Alle Dateien (*.*)"
        # ) 
            # print(len(self.path_database))
            self.label_define_database_2.setText(self.path_database)

    def window_rejected(self):
        self.define_database.close()
        # sys.exit(0)
        # print(self)
        # self.buttonBox_define_database.reject()
        # self.DefineDatabaseWindow.reject()
    
    def window_accepted(self):
        path_localappdata = os.getenv('LOCALAPPDATA')
        file_path_database = os.path.join(path_localappdata, "LaMA", "file_path_database.txt")
        with open(file_path_database, "w") as file:
            file.write(self.path_database)

        self.define_database.close()
        # sys.exit(0)    


