import sys
import os
from pathlib import Path


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

    path_lama_developer_credentials = os.path.join(os.getenv('LOCALAPPDATA'), "LaMA", "credentials")
    lama_developer_credentials = os.path.join(path_lama_developer_credentials, "developer_credentials.txt")
    # ## OLD VERSION!!
    # path_programm = os.path.dirname(sys.argv[0])
    # path_localappdata_lama = path_programm


elif sys.platform.startswith("darwin"):
    path_programm=os.path.dirname(sys.argv[0])
    if path_programm == "":
        path_programm = "."
    
    path_programm = os.path.join(path_programm, "LaMA_programdata")
    if not os.path.isdir(path_programm):
        os.mkdir(path_programm)
    
    path_localappdata_lama = path_programm

    # path_home=Path.home()

    path_lama_developer_credentials = os.path.join(Path.home(), "Library", "LaMA","credentials")
    if not os.path.isdir(path_lama_developer_credentials):
        os.makedirs(path_lama_developer_credentials)
        
    lama_developer_credentials = os.path.join(path_lama_developer_credentials, "developer_credentials.txt")

lama_user_credentials = 'ghp_PwshmR'
database = os.path.join(path_programm, "_database")

lama_settings_file = os.path.join(
            path_localappdata_lama, "Teildokument", "lama_settings"
        )


