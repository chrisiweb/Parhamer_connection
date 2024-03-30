# import sys

# from PyQt5.QtCore import pyqtSignal
# from PyQt5 import QtWidgets


# class PrimenumberSpinBox(QtWidgets.QSpinBox):
#     # Replaces the valueChanged signal
#     newValueChanged = pyqtSignal(int)

#     def __init__(self, parent=None):
#         super(PrimenumberSpinBox, self).__init__(parent=parent)

#         self.valueChanged.connect(self.onValueChanged)
        
#         # self.newValueChanged.connect(self.slot)

#     def onValueChanged(self, i):
#         print(i)
#         list_of_primenumbers = [2,3,5,7,11,13]

#         current_value = self.value()
        
#         print(current_value)
#         if current_value in list_of_primenumbers:
#             index = list_of_primenumbers.index(current_value)
#             self.setValue(list_of_primenumbers[index])
#             return
#         else:
#             while True:
#                 if current_value >= list_of_primenumbers[-1]:
#                     self.setValue(list_of_primenumbers[-1])
#                     self.previous_value = list_of_primenumbers[-1]
#                     return    
#                 current_value += 1
#                 if current_value in list_of_primenumbers:
#                     index = list_of_primenumbers.index(current_value)
#                     self.setValue(list_of_primenumbers[index])
#                     self.previous_value = list_of_primenumbers[index]
#                     return

#         # try:
#         #     index = list_of_primenumbers.index(current_value)
#         # except ValueError:



#         # print(f"index:{list_of_primenumbers.index(self.before_value)}")

#         # self.setValue(list_of_primenumbers[index])
#         # if not self.isValid(i):
#         #     self.setValue(self.before_value)
#         # else:
#         #     self.newValueChanged.emit(i)
#         #     self.before_value = i

#     # def isValid(self, value):
#     #     if (self.minimum() - value % self.singleStep()) == 0:
#     #         return True
#     #     return False

#     # def slot(self, value):
#     #     print(value)


# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     w = PrimenumberSpinBox()
#     w.setMinimum(2)
#     w.setValue(2)
#     # w.setMaximum(50)
#     w.show()
#     sys.exit(app.exec_())


import re

string = "3+(96:12)+(11:12)\xb73"
x = re.findall(r'\([0-9]+:[0-9]+\)', string)

print(x)

# temp_string = string
for all in x:
    start = string.index(all)
    end = start + len(all)

    if end == len(string):
        following_operation = True
    elif string[end]!='\xb7':
        following_operation = True
    else:
        following_operation = False

    print(start)
    print(end)
    print(len(string))

    # print(string[start-1])
    # print(string[end])
    if string[start-1] != '\xb7' and following_operation==True:
        string = string.replace(all, all[1:-1])

print(string)

