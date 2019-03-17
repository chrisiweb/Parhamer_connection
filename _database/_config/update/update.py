#!/usr/bin/python3
# -*- coding: utf-8 -*-


from PyQt4 import QtCore, QtGui
import os
import subprocess
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(400, 100)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3, QtCore.Qt.AlignHCenter)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.progressBar.setProperty("value", 0)
        self.verticalLayout.addWidget(self.progressBar)
        self.label = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label, QtCore.Qt.AlignHCenter)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2, QtCore.Qt.AlignHCenter)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.setMaximumWidth(80)
        self.pushButton.hide()
        self.verticalLayout.addWidget(self.pushButton,0, QtCore.Qt.AlignHCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        # self.btn = QtGui.QPushButton(self.centralwidget)
        # self.verticalLayout.addWidget(self.btn, QtCore.Qt.AlignHCenter)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
       

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Update LaTeX File Assistent", None))
        self.label_3.setText(_translate("MainWindow", "Neues Update wird installiert...", None))
        # self.label_2.setText(_translate("MainWindow", "", None))
        #self.label_2.hide()
        self.pushButton.setText(_translate("MainWindow", "OK", None))
        self.pushButton.clicked.connect(self.ok_button)
        #self.btn.setText(_translate("MainWindow","Download", None))


    def install_update(self): 
        counter_progressbar=0
        opened_file=os.path.basename(sys.argv[0])
        name, extension=os.path.splitext(opened_file)
      
        updatefile_path=os.path.join(os.path.dirname('__file__'),'_database','_config','update','update%s'%extension)
        newapp_path=os.path.join(os.path.dirname('__file__'),'_database','_config','update','LaTeX_File_Assistent%s'%extension)
        self.mainfile_path=os.path.join(os.path.dirname('__file__'),'LaTeX_File_Assistent%s'%extension)

        while counter_progressbar<43:
            self.progressBar.setProperty("value", counter_progressbar)
            counter_progressbar+=0.00005
        #shutil.copyfile(newapp_path, "LaTeX File Assistent%s"%extension)
        if sys.platform.startswith('linux'):
            subprocess.call('cp "{0}" "LaTeX_File_Assistent{1}"'.format(newapp_path, extension),shell=True)
        elif sys.platform.startswith('darwin'):
            subprocess.call('cp "{0}" "LaTeX_File_Assistent{1}"'.format(newapp_path, extension),shell=True)
        else:
            subprocess.call('copy "{0}" "LaTeX_File_Assistent{1}"'.format(newapp_path, extension),shell=True)
        while counter_progressbar<100:
            self.progressBar.setProperty("value", counter_progressbar)
            counter_progressbar+=0.0001
        MainWindow.resize(400, 200)
        self.label.setText(_translate("MainWindow", "Das neue Update wurde erfolgreich installiert.", None))
        self.label_2.setText(_translate("MainWindow", "Das Program wird neu gestartet.", None))
        self.pushButton.show()
    
    def ok_button(self):
        if sys.platform.startswith('linux'):
            print(self.mainfile_path)
            subprocess.run("python3 " + self.mainfile_path, shell=True)
        elif sys.platform.startswith('darwin'):
            subprocess.run("python3 " + self.mainfile_path, shell=True)
        else:
            os.startfile(self.mainfile_path)
        sys.exit(0)
  
 
    
   
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.install_update()
    sys.exit(app.exec_())
 

