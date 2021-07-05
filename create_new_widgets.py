from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from config import SpinBox_noWheel, ClickLabel
from translate import _fromUtf8, _translate
from predefined_size_policy import SizePolicy_fixed


def add_action(parent, menu, text, command):
    new_action = QtWidgets.QAction(parent)
    new_action.setObjectName(_fromUtf8("{}".format(new_action)))
    menu.addAction(new_action)
    new_action.setText(_translate("MainWindow", text, None))
    new_action.triggered.connect(command)

    return new_action


def combine_all_lists_to_one(list_of_lists):
    combined_list = []
    for list in list_of_lists:
        combined_list = combined_list + list
    return combined_list


def create_new_gridlayout(parent=None):
    new_gridlayout = QtWidgets.QGridLayout(parent)
    new_gridlayout.setObjectName(_fromUtf8("{}".format(new_gridlayout)))
    return new_gridlayout


def create_new_verticallayout(parent=None):
    new_verticallayout = QtWidgets.QVBoxLayout(parent)
    new_verticallayout.setObjectName(_fromUtf8("{}".format(new_verticallayout)))
    return new_verticallayout


def create_new_horizontallayout(parent=None):
    new_horizontallayout = QtWidgets.QHBoxLayout(parent)
    new_horizontallayout.setObjectName(_fromUtf8("{}".format(new_horizontallayout)))
    return new_horizontallayout


def create_new_checkbox(parent, text, checked=False):
    new_checkbox = QtWidgets.QCheckBox(parent)
    new_checkbox.setObjectName(_fromUtf8("{}".format(new_checkbox)))
    new_checkbox.setText(_translate("MainWindow", text, None))
    new_checkbox.setChecked(checked)

    return new_checkbox


def create_new_groupbox(parent, name):
    new_groupbox = QtWidgets.QGroupBox(parent)
    new_groupbox.setObjectName("{}".format(new_groupbox))
    new_groupbox.setTitle(_translate("MainWindow", "{}".format(name), None))

    return new_groupbox


def create_new_label(parent, text, wordwrap=False, clickable=False):
    new_label = ClickLabel()
    if clickable == False:
        new_label = QtWidgets.QLabel(parent)
    elif clickable == True:
        new_label = ClickLabel()

    new_label.setObjectName("{}".format(new_label))
    new_label.setText(_translate("MainWindow", text, None))
    new_label.setWordWrap(wordwrap)

    return new_label


def create_new_lineedit(parent):
    new_lineedit = QtWidgets.QLineEdit(parent)
    new_lineedit.setObjectName(_fromUtf8("{}".format(new_lineedit)))

    return new_lineedit


def create_new_button(parent, text, command):
    new_button = QtWidgets.QPushButton(parent)
    new_button.setObjectName("{}".format(new_button))
    new_button.setText(_translate("MainWindow", text, None))
    if command != None:
        new_button.clicked.connect(command)

    return new_button


def create_standard_button(parent, text, command, icon=""):
    new_standard_button = create_new_button(parent, "", command)
    new_standard_button.setSizePolicy(SizePolicy_fixed)
    # new_standard_button.setMaximumSize(QSize(30, 30))
    new_standard_button.setFocusPolicy(Qt.ClickFocus)
    # new_standard_button.setStyleSheet(_fromUtf8("background-color: light gray"))
    new_standard_button.setIcon(QtWidgets.QApplication.style().standardIcon(icon))

    return new_standard_button


def still_to_define():
    print("still to define")


def create_new_spinbox(parent, value=0):
    new_spinbox = SpinBox_noWheel(parent)
    new_spinbox.setObjectName("{}".format(new_spinbox))
    new_spinbox.setValue(value)
    return new_spinbox


def create_new_combobox(parent):
    new_combobox = QtWidgets.QComboBox(parent)
    new_combobox.setObjectName(_fromUtf8("{}".format(new_combobox)))

    return new_combobox


def create_new_radiobutton(parent, text):
    new_radiobutton = QtWidgets.QRadioButton(parent)
    new_radiobutton.setObjectName("{}".format(new_radiobutton))
    new_radiobutton.setFocusPolicy(Qt.ClickFocus)
    new_radiobutton.setText(_translate("MainWindow", text, None))

    return new_radiobutton


def add_new_option(combobox, index, item):
    combobox.addItem("")
    combobox.setItemText(index, item)


def add_new_tab(tabwidget, name):
    new_tab = QtWidgets.QWidget()
    new_tab.setObjectName("{}".format(new_tab))
    tabwidget.addTab(new_tab, name)

    return new_tab
