from PyQt5 import QtCore, QtWidgets, QtGui
import yaml
import sys
import os
import re

path_programm = os.path.dirname(sys.argv[0])
if sys.platform.startswith("darwin"):
    if path_programm is "":
        path_programm = "."

config_file = os.path.join(path_programm, "_database", "_config", "config.yml")


lama_settings_file = os.path.join(
            path_programm, "Teildokument", "lama_settings"
        )
        
colors_ui = {
    "black": QtGui.QColor(0, 0, 0),
    "white": QtGui.QColor(255, 255, 255),
    "dark_gray": QtGui.QColor(53, 53, 53),
    "gray": QtGui.QColor(214, 214, 214),
    "blue_1": QtGui.QColor(245, 245, 255),
    "blue_2": QtGui.QColor(224, 233, 232),
    "blue_3": QtGui.QColor(194, 208, 212),  # 211, 224, 223
    "blue_4": QtGui.QColor(168, 189, 194),
    "blue_5": QtGui.QColor(88, 111, 124),
    "blue_6": QtGui.QColor(47, 69, 80),
    "blue_7": QtGui.QColor(47, 69, 80),
    "red": QtGui.QColor(195, 58, 63),
}


def get_color(color):
    color = "rgb({0}, {1}, {2})".format(color.red(), color.green(), color.blue())
    return color


def config_loader(pathToFile, parameter):
    try:
        config_file = yaml.safe_load(open(pathToFile, encoding="utf8"))
        return config_file[parameter]
    except FileNotFoundError:
        print("File not Found!")
        if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
            root = "."
        else:
            root = ""
            
        config_path = os.path.join(".", "_database", "_config")
        # if not os.path.exists(config_path):
        #     print("No worries, we'll create the structure for you.")
        #     os.makedirs(config_path)
        print('Die Konfigurationsdatei "config.yml" konnte nicht gefunden werden. Stellen Sie sicher, dass sich der Ordner "_database" und das Programm LaMA im selben Ordner befinden.')
        sys.exit()    
    


# if sys.platform.startswith("linux"):
#     workdir = os.path.dirname(os.path.realpath(__file__))
#     path_programm = os.path.join(workdir)

# else:


logo_path = os.path.join(
    path_programm, "_database", "_config", "icon", "LaMA_icon_logo.png"
)

logo_cria_path = os.path.join(
    path_programm, "_database", "_config", "icon", "LaMA_cria_icon_logo.png"
)

logo_cria_button_path = os.path.join(
    path_programm, "_database", "_config", "icon", "LaMA_cria_icon_logo_button.png"
)


class SpinBox_noWheel(QtWidgets.QSpinBox):
    def wheelEvent(self, event):
        event.ignore()


class ClickLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        QtWidgets.QLabel.mousePressEvent(self, event)


def bring_to_front(window):
    window.setWindowFlags(window.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
    window.show()
    window.setWindowFlags(window.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
    window.show()


def is_empty(structure):
    if structure:
        return False
    else:
        return True


def shorten_gk(gk):
    gk = gk.lower().replace(" ", "").replace(".", "").replace("-l", "")
    return gk


def split_section(section, chosen_program):
    section = re.split(" - |{|}", section)
    info = [item.strip() for item in section]
    info.pop(0)
    info.pop(-1)
    if chosen_program == "lama":
        if re.match("K[0-9]", info[1]) or info[1] == "MAT":
            pass
        else:
            info.insert(1, None)

    return info

def still_to_define():
    print('still to define')