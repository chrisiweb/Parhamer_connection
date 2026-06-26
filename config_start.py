import sys
import os
from pathlib import Path

#### Version number ###
__version__ = "v5.1.4"

def resource_path(*relative_path):
    """ermittelt den Pfad zu Ressourcen im Entwicklermodus UND im Build"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller Build
        base = sys._MEIPASS
    else:
        # Entwicklungsmodus
        base = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base, *relative_path)



def app_base_dir():
    """
    Liefert das Basisverzeichnis der Anwendung:
    - Entwicklungsmodus: Ordner der .py-Datei
    - PyInstaller: Ordner der EXE
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller / EXE
        return os.path.dirname(sys.executable)
    else:
        # Direkt ausgeführte .py-Datei
        return os.path.dirname(os.path.abspath(__file__))


def portable_path(*parts):
    return os.path.join(app_base_dir(), 'portable', *parts)





def get_running_file_extension() -> str:
    # Wenn es eine PyInstaller-EXE ist → sys.frozen = True
    if getattr(sys, "frozen", False):
        return Path(sys.executable).suffix.lower()

    # Sonst normales Python-Script
    return Path(__file__).suffix.lower()


# def get_install_location():
#     exe_path = sys.executable
#     install_dir = os.path.dirname(exe_path)
#     return install_dir



if sys.platform.startswith("win"):
    extension = get_running_file_extension()
    # programdata = os.getenv('PROGRAMDATA')
    if extension == ".exe":
        exe_dir = os.path.dirname(sys.executable)
        
        if exe_dir.lower().startswith(r"c:\program files") or exe_dir.lower().startswith(r"c:\programme"):
            programdata = os.getenv('PROGRAMDATA')
        else:
            programdata = os.getenv('LOCALAPPDATA')
        path_programm = os.path.join(programdata, "LaMA")
        if not os.path.isdir(path_programm):
            os.mkdir(path_programm)
    else:
        programdata = os.getenv('PROGRAMDATA')
        path_programm = os.path.join(programdata, "LaMA")
        if not os.path.isdir(path_programm):
            programdata = os.getenv('LOCALAPPDATA')
            path_programm = os.path.join(programdata, "LaMA")
            if not os.path.isdir(path_programm):
                os.mkdir(path_programm)


    path_localappdata_lama = path_programm

    path_lama_developer_credentials = os.path.join(os.getenv('LOCALAPPDATA'), "LaMA", "credentials")
    if not os.path.isdir(path_lama_developer_credentials):
        os.makedirs(path_lama_developer_credentials)
    lama_developer_credentials = os.path.join(path_lama_developer_credentials, "developer_credentials.txt")

    lama_settings_file = os.path.join(
                os.getenv('LOCALAPPDATA'), "LaMA", "lama_settings"
            )

    lama_titlepage_save = os.path.join(
                os.getenv('LOCALAPPDATA'), "LaMA", "lama_titlepage_save"
            )
    lama_individual_titlepage  = os.path.join(
                os.getenv('LOCALAPPDATA'), "LaMA", "lama_individual_titlepage"
            )
    cria_titlepage_save  = os.path.join(
                os.getenv('LOCALAPPDATA'), "LaMA", "cria_titlepage_save"
            )
    cria_individual_titlepage  = os.path.join(
                os.getenv('LOCALAPPDATA'), "LaMA", "cria_individual_titlepage"
            )
    lama_notenschluessel_file = os.path.join(
                os.getenv('LOCALAPPDATA'), "LaMA", "lama_notenschluessel.json"
            )
    

    # latex = os.path.join(os.path.dirname(sys.argv[0]), 'portable', 'tinytex', 'bin', 'windows', 'latex.exe')
    # dvips = os.path.join(os.path.dirname(sys.argv[0]), 'portable', 'tinytex', 'bin', 'windows', 'dvips.exe')
    # gs = os.path.join(os.path.dirname(sys.argv[0]), 'portable', 'ghostscript', 'bin', 'gswin64c.exe')    
    
    latex = portable_path('tinytex', 'bin', 'windows', 'latex.exe')
    dvips = portable_path('tinytex', 'bin', 'windows', 'dvips.exe')
    gs = portable_path('ghostscript', 'bin', 'gswin64c.exe')
    # path_standard_pdf_reader = os.path.join(os.path.dirname(sys.argv[0]), "SumatraPDF-3.4.6-64.exe")


    # ## OLD VERSION!!
    # path_programm = os.path.dirname(sys.argv[0])
    # path_localappdata_lama = path_programm

    # everyone, domain, type = win32security.LookupAccountName ("", "Everyone")
    # admins, domain, type = win32security.LookupAccountName ("", "Administrators")
    # user, domain, type = win32security.LookupAccountName ("", win32api.GetUserName())


    # # dacl = sd.GetSecurityDescriptorDacl()
    # dacl = win32security.ACL ()
    # # dacl.AddAccessAllowedAce (win32security.ACL_REVISION, con.FILE_GENERIC_READ, everyone)
    # # dacl.AddAccessAllowedAce (win32security.ACL_REVISION, con.FILE_GENERIC_READ | con.FILE_GENERIC_WRITE, user)
    # dacl.AddAccessAllowedAce (win32security.ACL_REVISION, con.FILE_ALL_ACCESS, None)


elif sys.platform.startswith("darwin"):
# else:
    # path_programm=os.path.dirname(sys.argv[0])
    # if path_programm == "":
    #     path_programm = "."
    
    path_programm = os.path.join(Path.home(), "Library", "LaMA")
    # path_programm = os.path.join(Path.home(), "Library", "LaMA","LaMA_programdata")
    if not os.path.isdir(path_programm):
        os.makedirs(path_programm)

    path_localappdata_lama = path_programm


    path_lama_developer_credentials = os.path.join(path_programm,"credentials")
    if not os.path.isdir(path_lama_developer_credentials):
        os.mkdir(path_lama_developer_credentials)
        
    lama_developer_credentials = os.path.join(path_lama_developer_credentials, "developer_credentials.txt")

    lama_settings_file = os.path.join(
                path_programm, "lama_settings"
            )

    lama_titlepage_save = os.path.join(
                path_programm, "lama_titlepage_save"
            )
    lama_individual_titlepage  = os.path.join(
                path_programm, "lama_individual_titlepage"
            )
    cria_titlepage_save  = os.path.join(
                path_programm, "cria_titlepage_save"
            )
    cria_individual_titlepage  = os.path.join(
                path_programm, "cria_individual_titlepage"
            )

    lama_notenschluessel_file = os.path.join(
                path_programm, "lama_notenschluessel.json"
            )


    # lama_path = os.path.dirname(sys.argv[0])
    # if lama_path == "":
    #     lama_path = "."
    folder = 'universal-darwin'

    # gs = os.path.join(lama_path, 'portable', 'ghostscript', 'bin', 'gs')

        
    # latex = os.path.join(lama_path, 'portable', 'tinytex', 'bin',folder,'latex')
    # dvips = os.path.join(lama_path, 'portable', 'tinytex', 'bin',folder, 'dvips')

    latex = resource_path('portable', 'tinytex', 'bin', folder , 'latex')
    dvips = resource_path('portable', 'tinytex', 'bin',folder, 'dvips')
    gs = resource_path('portable', 'ghostscript', 'bin', 'gs')


    path_standard_pdf_reader = ""

elif sys.platform.startswith("linux"):
    path_programm = os.path.join(os.path.expanduser('~'), ".local","share","LaMA")

    if not os.path.isdir(path_programm):
        os.mkdir(path_programm)
    path_localappdata_lama = path_programm

    path_lama_developer_credentials = os.path.join(path_programm,"credentials")
    if not os.path.isdir(path_lama_developer_credentials):
        os.mkdir(path_lama_developer_credentials)
    lama_developer_credentials = os.path.join(path_lama_developer_credentials, "developer_credentials.txt")

    lama_settings_file = os.path.join(path_programm, "lama_settings"
            )
    lama_titlepage_save = os.path.join(
                path_programm, "lama_titlepage_save"
            )
    lama_individual_titlepage  = os.path.join(
                path_programm, "lama_individual_titlepage"
            )
    cria_titlepage_save  = os.path.join(
                path_programm, "cria_titlepage_save"
            )
    cria_individual_titlepage  = os.path.join(
                path_programm, "cria_individual_titlepage"
            )

    lama_notenschluessel_file = os.path.join(
                path_programm, "lama_notenschluessel.json"
            )
    

    if getattr(sys, 'frozen', False):
        # Wenn aus AppImage oder PyInstaller gestartet
        lama_path = os.path.dirname(sys.executable)
    else:
        # Normaler Python-Start
        lama_path = os.path.dirname(os.path.abspath(__file__))
    folder = 'x86_64-linux'  
    gs = "gs"
       
    latex = os.path.join(lama_path, 'portable', 'tinytex', 'bin',folder,'latex')
    dvips = os.path.join(lama_path, 'portable', 'tinytex', 'bin',folder, 'dvips')
    path_standard_pdf_reader = ""

path_home = Path.home()

lama_user_credentials = 'ghp_PwshmR'
database = os.path.join(path_programm, "_database")


# if sys.platform.startswith("win"):
#     path_lama_developer_credentials = os.path.join(os.getenv('LOCALAPPDATA'), "LaMA", "credentials")
# elif sys.platform.startswith("darwin"):
#     path_lama_developer_credentials = os.path.join(Path.home(), "Library", "LaMA","credentials")


# lama_developer_credentials = os.path.join(
#     path_lama_developer_credentials, "developer_credentials.txt"
# )

# lama_settings_file = os.path.join(
#             path_localappdata_lama, "Teildokument", "lama_settings"
#         )


