import sys
import os
from pathlib import Path

#### Version number ###
__version__ = "v4.6.2"

if sys.platform.startswith("win"):
    programdata = os.getenv('PROGRAMDATA')
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
    
    
    path_standard_pdf_reader = os.path.join(os.path.dirname(sys.argv[0]), "SumatraPDF-3.4.6-64.exe")
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
    path_programm=os.path.dirname(sys.argv[0])
    if path_programm == "":
        path_programm = "."
    
    path_programm = os.path.join(path_programm, "LaMA_programdata")
    # path_programm = os.path.join(Path.home(), "Library", "LaMA","LaMA_programdata")
    if not os.path.isdir(path_programm):
        os.mkdir(path_programm)

    path_localappdata_lama = path_programm


    path_lama_developer_credentials = os.path.join(Path.home(), "Library", "LaMA","credentials")
    if not os.path.isdir(path_lama_developer_credentials):
        os.makedirs(path_lama_developer_credentials)
        
    lama_developer_credentials = os.path.join(path_lama_developer_credentials, "developer_credentials.txt")

    lama_settings_file = os.path.join(
                Path.home(), "Library", "LaMA", "lama_settings"
            )

    lama_titlepage_save = os.path.join(
                Path.home(), "Library", "LaMA", "lama_titlepage_save"
            )
    lama_individual_titlepage  = os.path.join(
                Path.home(), "Library", "LaMA", "lama_individual_titlepage"
            )
    cria_titlepage_save  = os.path.join(
                Path.home(), "Library", "LaMA", "cria_titlepage_save"
            )
    cria_individual_titlepage  = os.path.join(
                Path.home(), "Library", "LaMA", "cria_individual_titlepage"
            )

    lama_notenschluessel_file = os.path.join(
                Path.home(), "Library", "LaMA", "lama_notenschluessel.json"
            )

    path_standard_pdf_reader = ""
elif sys.platform.startswith("linux"):
    path_programm = os.path.join(os.path.expanduser('~'), ".LaMA")

    if not os.path.isdir(path_programm):
        os.mkdir(path_programm)
    path_localappdata_lama = path_programm

    path_lama_developer_credentials = os.path.join(path_programm,"credentials")
    if not os.path.isdir(path_lama_developer_credentials):
        os.mkdir(path_lama_developer_credentials)
    lama_developer_credentials = os.path.join(path_lama_developer_credentials, "developer_credentials.txt")

    lama_settings_file = os.path.join(path_programm, "lama_settings"
            )

    lama_notenschluessel_file = os.path.join(
                path_programm, "lama_notenschluessel.json"
            )
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


