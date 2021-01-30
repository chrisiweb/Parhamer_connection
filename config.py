from PyQt5 import QtCore, QtWidgets, QtGui
import yaml
import sys
import git
from git import Repo
import os
import re
from pyqt5_minimal import Ui_WelcomeWindow
from define_database import Ui_define_database


if sys.platform.startswith("win"):
    ##### NOT IN USE ! (Working!) - Activate when installer is used!
    # path_localappdata = os.getenv('LOCALAPPDATA')
    # path_localappdata_lama = os.path.join(path_localappdata, "LaMA")
    # file_path_database = os.path.join(path_localappdata_lama ,"file_path_database.txt")
    # try:
    #     with open(file_path_database, "r") as file:
    #         path = file.read()
    # except FileNotFoundError:
    #     path = os.path.dirname(file_path_database)
    #     if os.path.isdir(path) == False:    
    #         os.mkdir(path)

    #     app = QtWidgets.QApplication(sys.argv)
    #     define_database = QtWidgets.QWidget()
    #     ui = Ui_define_database()
    #     ui.setupUi(define_database)
    #     define_database.show()
    #     app.exec_()

    #     with open(file_path_database, "r") as file:
    #         path = file.read()
        
    #     print("Loading LaMA...")


    #####
    programdata = os.getenv('PROGRAMDATA')
    path_programm = os.path.join(programdata, "LaMA")
    if not os.path.isdir(path_programm):
        os.mkdir(path_programm)
    path_localappdata_lama = path_programm

    # ## OLD VERSION!!
    # path_programm = os.path.dirname(sys.argv[0])
    # path_localappdata_lama = path_programm


elif sys.platform.startswith("darwin"):
    path_programm=os.path.dirname(sys.argv[0])
    if path_programm == "":
        path_programm = "."
    path_localappdata_lama = path_programm

# config_file = os.path.join(path_programm, "_database", "_config", "config.yml")
config_file = os.path.join(os.path.dirname(sys.argv[0]), "config.yml")

lama_settings_file = os.path.join(
            path_localappdata_lama, "Teildokument", "lama_settings"
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
    "blue_6": QtGui.QColor(83, 122, 141),
    "blue_7": QtGui.QColor(47, 69, 80),
    "red": QtGui.QColor(195, 58, 63),
}
    # "blue_6": QtGui.QColor(68, 92, 136),

def get_color(color):
    color = "rgb({0}, {1}, {2})".format(color.red(), color.green(), color.blue())
    return color


def config_loader(pathToFile, parameter):
    config_file = yaml.safe_load(open(pathToFile, encoding="utf8"))
    return config_file[parameter]
    #######
    try:
        config_file = yaml.safe_load(open(pathToFile, encoding="utf8"))
        return config_file[parameter]
    except FileNotFoundError:
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_WelcomeWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())

        print("File not Found!")
        print("Downloading database")
        path_programdata = os.getenv('PROGRAMDATA')
        database = os.path.join(path_programdata, "LaMA", "_database")
        # QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        try:
            git.Repo.clone_from("https://github.com/chrisiweb/lama_latest_update.git", database)
        except git.exc.GitCommandError:
            print('Datenbank existiert bereits!')
        print('Download finished')
        # QtWidgets.QApplication.restoreOverrideCursor()
        if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
            root = "."
        else:
            root = ""
            
        config_path = os.path.join(".", "_database", "_config")
        # if not os.path.exists(config_path):
        #     print("No worries, we'll create the structure for you.")
        #     os.makedirs(config_path)
        try:
            config_file = yaml.safe_load(open(pathToFile, encoding="utf8"))
            return config_file[parameter]
        except FileNotFoundError:
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

ag_beschreibung = config_loader(config_file, "ag_beschreibung")
an_beschreibung = config_loader(config_file, "an_beschreibung")
fa_beschreibung = config_loader(config_file, "fa_beschreibung")
ws_beschreibung = config_loader(config_file, "ws_beschreibung")
list_topics = [
    list(ag_beschreibung.keys()),
    list(an_beschreibung.keys()),
    list(fa_beschreibung.keys()),
    list(ws_beschreibung.keys()),
]

zusatzthemen_beschreibung = config_loader(config_file, "zusatzthemen_beschreibung")
k5_beschreibung = config_loader(config_file, "k5_beschreibung")
k6_beschreibung = config_loader(config_file, "k6_beschreibung")
k7_beschreibung = config_loader(config_file, "k7_beschreibung")
k8_beschreibung = config_loader(config_file, "k8_beschreibung")

dict_gk = config_loader(config_file, "dict_gk")
Klassen = config_loader(config_file, "Klassen")
list_klassen = config_loader(config_file, "list_klassen")
dict_aufgabenformate = config_loader(config_file, "dict_aufgabenformate")

for klasse in list_klassen:
    exec('dict_{0} = config_loader(config_file,"dict_{0}")'.format(klasse))
    exec('dict_{0}_name = config_loader(config_file,"dict_{0}_name")'.format(klasse))

dict_unterkapitel = config_loader(config_file, "dict_unterkapitel")