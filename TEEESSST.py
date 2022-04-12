# from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QApplication, QWidget
# import sys


# def report_exceptions(f):
#     def wrapped_f(*args, **kwargs):
#         try:
#             f(*args, **kwargs)
#         except Exception as e:
#             print(e)
#             print("ERROR caught")   
#     return wrapped_f


# class Window(QWidget):
#     def __init__(self):
#         super().__init__()
#         b1 = QPushButton('1')
#         b2 = QPushButton('2')
#         b1.clicked.connect(self.f1)
#         b2.clicked.connect(self.f2)
#         layout = QVBoxLayout(self)
#         layout.addWidget(b1)
#         layout.addWidget(b2)
#         self.setLayout(layout)

#     @report_exceptions
#     def f1(self):
#         raise Exception("Error inside f1")

#     @report_exceptions
#     def f2(self,var1, var2):
#         raise Exception("Error inside f2")

# app = QApplication([])
# window = Window()
# window.show()

# sys.exit(app.exec_())




from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QApplication, QWidget
import sys


def report_exceptions(f):
    def wrapped_f(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as e:
            print(f"caught: {e}")   
    return wrapped_f


class Window(QWidget):
    def __init__(self):
        super().__init__()
        b1 = QPushButton('1')
        b1.clicked.connect(self.f1)
        layout = QVBoxLayout(self)
        layout.addWidget(b1)
        self.setLayout(layout)

    @report_exceptions
    def f1(self):
        raise Exception("Error inside f1")


app = QApplication([])
window = Window()
window.show()

sys.exit(app.exec_())
