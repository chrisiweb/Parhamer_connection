from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
import sys

class MainWindow(QMainWindow):

    # def __init__(self) -> None:
    #     super(MainWindow, self).__init__()

    def resizeEvent(self, event: QtGui.QResizeEvent):
        print('test')
        QMainWindow.resizeEvent(self, event)
        # return super().resizeEvent(event)

    def setupUi(self, MainWindow):

        self.label_warnung = QLabel()
        # background-color: rgb(195, 58, 63)
        # self.label_warnung.setMaximumSize(QtCore.QSize(375, 16777215))
        self.label_warnung.setText('text')

   
    

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Resize Event")
    window.setupUi(QMainWindow())

    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()