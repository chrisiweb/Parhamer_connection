from PyQt5 import QtCore, QtWidgets, QtGui
import yaml
import sys
import os

path_programm = os.path.dirname(sys.argv[0])
if sys.platform.startswith("darwin"):
    if path_programm is "":
        path_programm = "."

config_file = os.path.join(path_programm, "_database", "_config", "config.yml")

colors_ui = {
'black'  : QtGui.QColor(0  , 0, 0),
'white'  : QtGui.QColor(255, 255, 255),
'gray'   : QtGui.QColor(214, 214, 214),
'blue_1' : QtGui.QColor(245, 245, 255),
'blue_2' : QtGui.QColor(225, 240, 240),
'blue_3' : QtGui.QColor(224, 233, 232), #211, 224, 223  
'blue_4' : QtGui.QColor(168, 189, 194),  
'blue_5' : QtGui.QColor(88, 111, 124),
'blue_6' : QtGui.QColor(47, 69, 80),
'blue_7' : QtGui.QColor(47, 69, 80),
'red'    : QtGui.QColor(195, 58, 63),
}
  

def config_loader(pathToFile, parameter):
    for i in range(5):
        try:
            config_file = yaml.safe_load(open(pathToFile, encoding="utf8"))
            break
        except FileNotFoundError:
            print("File not Found!")
            if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
                root = "."
            else:
                root = ""
            config_path = os.path.join(".", "_database", "_config")
            if not os.path.exists(config_path):
                print("No worries, we'll create the structure for you.")
                os.makedirs(config_path)
            input(
                "Please place your config file in '{}' and hit enter. {} tries left!".format(
                    config_path, 5 - i
                )
            )
    return config_file[parameter]


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

class SpinBox_noWheel(QtWidgets.QSpinBox):
    def wheelEvent(self, event):
        event.ignore()