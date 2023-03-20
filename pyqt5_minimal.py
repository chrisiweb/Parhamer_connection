from PyQt5.QtCore import QUrl
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from config import path_programm
import os
# from PyQt5.QtWebKitWidgets import QWebView
import sys

class PDFViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the title and geometry of the main window
        self.setWindowTitle("PDF Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Create a QWebView widget to display the PDF file
        self.web_view = QWebEngineView(self)
        self.web_view.setGeometry(0, 0, 800, 600)
        self.setCentralWidget(self.web_view)

    def open_pdf(self, file_path):
        # Load the PDF file into the QWebView widget
        self.web_view.load(QUrl.fromLocalFile(file_path))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = PDFViewer()
    viewer.show()
    path_teildokument = os.path.join(path_programm, "Teildokument","Teildokument_1.pdf")
    # print(path_programm)
    viewer.open_pdf(path_teildokument)
    sys.exit(app.exec_())
