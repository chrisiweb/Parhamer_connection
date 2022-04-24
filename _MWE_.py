
## WORKING DRAG & DROP!!!
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QLabel, QMainWindow, QVBoxLayout, QGroupBox
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal
from PyQt5.QtGui import QDrag, QPixmap
from create_new_widgets import create_new_label, create_new_verticallayout


class DragDropGroupBox(QGroupBox):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        # self.setContentsMargins(25, 5, 25, 5)
        # self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.setStyleSheet("border: 1px solid black;")
        # Store data separately from display label, but use label for default.
        # self.data = self.text()

    # def set_data(self, data):
    #     self.data = data

    def mouseMoveEvent(self, e):

        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec_(Qt.MoveAction)


class DragDropWidget(QWidget):
    """
    Generic list sorting handler.
    """

    orderChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

        self.blayout = QVBoxLayout()


        self.setLayout(self.blayout)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        pos = e.pos()
        widget = e.source()
        print(pos)
        
        for n in range(self.blayout.count()):
            # Get the widget at each index in turn.
            # print(n)
            w = self.blayout.itemAt(n).widget()

            drop_here = pos.y() < w.y() +  w.size().height() // 2
            # print(f"drop: {pos.y()}")
            # print(f"widget: {w.y()}")
            # print(f"max  {w.y() + w.size().height() // 2}")
            if pos.y() < w.y() and n == 0:
                # print("FIRST Position")
                self.blayout.insertWidget(0, widget)
                break
            elif drop_here:
                # print("B")
                # We didn't drag past this widget.
                # insert to the left of it.
                self.blayout.insertWidget(n-1, widget)
                # print(f"index: {n}")
                # self.orderChanged.emit()
                break
        if drop_here == False:
            # print("Last Item")
            self.blayout.insertWidget(n, widget)
        e.accept()

    def add_item(self, item):
        self.blayout.addWidget(item)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.drag = DragDropWidget()
        
        for i in range(4):
            item = DragDropGroupBox()
            item.setTitle("NEU")
            verticallayout = create_new_verticallayout(item)
            label = create_new_label(item, f"Das ist ein Test {i}")
            verticallayout.addWidget(label)
            # item.set_data(n)  # Store the data.
            self.drag.add_item(item)

        # Print out the changed order.
        # self.drag.orderChanged.connect(lambda: print('test'))

        container = QWidget()
        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.drag)
        layout.addStretch(1)
        container.setLayout(layout)

        self.setCentralWidget(container)


app = QApplication([])
w = MainWindow()
w.show()

app.exec_()



# ###WORKING ####

# import sys, random
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from matplotlib.figure import Figure
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from create_new_widgets import create_new_groupbox, create_new_label

# class IndicSelectWindow(QDialog):

#     def __init__(self, parent=None):
#         super(IndicSelectWindow, self).__init__(parent=parent)
#         self.resize(1000, 800)

#         self.target = None
#         self.setAcceptDrops(True)
#         self.layout = QHBoxLayout(self)
#         self.scrollArea = QScrollArea(self)
#         self.scrollArea.setWidgetResizable(True)
#         self.scrollAreaWidgetContents = QWidget()
#         self.gridLayout = QGridLayout(self.scrollAreaWidgetContents)
#         self.scrollArea.setWidget(self.scrollAreaWidgetContents)
#         self.layout.addWidget(self.scrollArea)

#         index=1
#         for i in range(3):
#             self.groupBox = create_new_groupbox(self, "Test")

#             self.layout = QHBoxLayout(self.groupBox)

#             self.figure = Figure()  # a figure to plot on
#             self.label = create_new_label(self.groupBox, f"Label {index}")
#             self.canvas = FigureCanvas(self.figure)
#             self.canvas.installEventFilter(self)                
            
#             index += 1


#             self.layout.addWidget(self.canvas)
#             self.layout.addWidget(self.label)

#             Box = QVBoxLayout()

#             Box.addWidget(self.groupBox)

#             self.gridLayout.addLayout(Box, i, 0)


#     def eventFilter(self, watched, event):
#         if event.type() == QEvent.MouseButtonPress:
#             self.mousePressEvent(event)
#         elif event.type() == QEvent.MouseMove:
#             self.mouseMoveEvent(event)
#         elif event.type() == QEvent.MouseButtonRelease:
#             self.mouseReleaseEvent(event)
#         return super().eventFilter(watched, event)

#     def get_index(self, pos):
#         for i in range(self.gridLayout.count()):
#             if self.gridLayout.itemAt(i).geometry().contains(pos) and i != self.target:
#                 return i

#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             self.target = self.get_index(event.windowPos().toPoint())
#         else:
#             self.target = None

#     def mouseMoveEvent(self, event):
#         if event.buttons() & Qt.LeftButton and self.target is not None:
#             drag = QDrag(self.gridLayout.itemAt(self.target))
#             pix = self.gridLayout.itemAt(self.target).itemAt(0).widget().grab()
#             mimedata = QMimeData()
#             mimedata.setImageData(pix)
#             drag.setMimeData(mimedata)
#             drag.setPixmap(pix)
#             drag.setHotSpot(event.pos())
#             drag.exec_()

#     def mouseReleaseEvent(self, event):
#         self.target = None

#     def dragEnterEvent(self, event):
#         if event.mimeData().hasImage():
#             event.accept()
#         else:
#             event.ignore()

#     def dropEvent(self, event):
#         if not event.source().geometry().contains(event.pos()):
#             source = self.get_index(event.pos())
#             if source is None:
#                 return

#             i, j = max(self.target, source), min(self.target, source)
#             p1, p2 = self.gridLayout.getItemPosition(i), self.gridLayout.getItemPosition(j)

#             self.gridLayout.addItem(self.gridLayout.takeAt(i), *p2)
#             self.gridLayout.addItem(self.gridLayout.takeAt(j), *p1)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     w = IndicSelectWindow()
#     w.show()
#     sys.exit(app.exec_())