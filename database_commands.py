from PyQt5.sip import delete
from tinydb import TinyDB, Query
from tinydb.operations import set
import os
import re
from config_start import path_programm
from config import config_loader, config_file

# from config import database_lama_1, _file_


def get_aufgabentyp(chosen_program , aufgabe):
    # print(aufgabe)
    if chosen_program == "cria":
        typ = None
    elif re.search("[A-Z]", aufgabe) == None:
        typ = 2
    else:
        typ = 1
    return typ

def get_table(aufgabe, typ):
    if typ==None:
        typ = 'cria'
    elif typ == 1:
        typ = 'lama_1'
    elif typ == 2:
        typ = 'lama_2'
    table = "table_" + typ
    
    if " (lokal)" in aufgabe:
        aufgabe = aufgabe.replace(" (lokal)","")
        return _local_database.table(table)
    else:
        return _database.table(table)

def get_aufgabe_total(aufgabe, typ):
    table_lama = get_table(aufgabe, typ)
    # if typ==None:
    #     typ = 'cria'
    # elif typ == 1:
    #     typ = 'lama_1'
    # elif typ == 2:
    #     typ = 'lama_2'
    # table = "table_" + typ
    
    # if " (lokal)" in aufgabe:
    #     aufgabe = aufgabe.replace(" (lokal)","")
    #     table_lama = _local_database.table(table)
    # else:
    #     table_lama = _database.table(table)

    _file_ = Query()

    return table_lama.get(_file_.name == aufgabe) 


def update_data(aufgabe,typ, key, value):
    lama_table = get_table(aufgabe, typ)
    aufgabe = aufgabe.replace(" (lokal)","")
    _file_ = Query()
    lama_table.update(set(key, value), _file_.name == aufgabe)


def delete_file(aufgabe, typ):
    lama_table = get_table(aufgabe, typ)
    aufgabe = aufgabe.replace(" (lokal)","")
    _file_ = Query()
    lama_table.remove(_file_.name == aufgabe)

# def multiple_update_date(aufgabe, typ, _list):


# class WriteFilesToDatabase:
#     def __init__(self):
#         print('test')

# WriteFilesToDatabase()

##################################################################################
##################################################################################
def collect_content(path):
    with open(path, "r", encoding="utf8") as f:
        content = f.read()

    return content


# def config_loader(pathToFile, parameter):
#     config_file = yaml.safe_load(open(pathToFile, encoding="utf8"))
#     return config_file[parameter]


def get_section_from_content(content):
    split_content = content.split("\n")
    for all in split_content:
        if "section" in all:
            section = all
            break
    try:
        return section
    except UnboundLocalError:
        return

def cut_begin_beispiel(content):
    if 'langesbeispiel' in content:
        content = re.split("begin{langesbeispiel}.*\n", content)[-1].lstrip()
    elif 'beispiel' in content:   
        content = re.split("begin{beispiel}.*\n", content)[-1].lstrip()

    return content

def cut_end_beispiel(content):
    if 'langesbeispiel' in content:
        content = content.split("\\end{langesbeispiel}")[0].rstrip()
    elif 'beispiel' in content:
        content = content.split("\\end{beispiel}")[0].rstrip()


    return content


def get_rest_from_content(content):
    rest = content.split("\\begin{", 1)
    rest = "\\begin{" + rest[1]

    # rest = re.split("begin{beispiel}.*{..?}", rest)[-1].lstrip()
    rest = cut_begin_beispiel(rest)

    rest = cut_end_beispiel(rest)

    return rest

def create_list_from_section(section):
	list_collected_data = re.split("{| - |}", section)[1:-1]
	
	return list_collected_data


def add_file(database, name, themen, titel, af, quelle, content, punkte, pagebreak, klasse, info = None, bilder=[], draft = False, abstand = 0):
    database.insert({
        'name' : name,
        'themen' : themen,
        'titel' : titel,
        'af' : af,
        'quelle' : quelle,
        'content' : content,
        'punkte' : punkte,
        'pagebreak' : pagebreak,
        'klasse' : klasse,
        'info' : info,
        'bilder' : bilder,
        'draft' : draft,
        'abstand' : abstand,
    })

def get_default_info(content):
    if 'langesbeispiel' in content:
        pagebreak = True
        punkte = int(re.split('begin{langesbeispiel}.*item\[(..?)\]', content)[1])
    elif 'beispiel' in content:
        pagebreak = False
        punkte = int(re.split('begin{beispiel}.*{(..?)}', content)[1])
    
    return pagebreak, punkte

def create_gk_list(string):
    gk_list = string.split(', ')
    return gk_list

def search_for_images(content):
    image_path_list = re.findall('includegraphics.*{(.*.eps)}', content)
    image_list = []
    for all in image_path_list:
        file_name = os.path.basename(all)
        image_list.append(file_name)
    
    return image_list
    # if image != None:
    #     print(image.group())
    # if 'includegraphics' in content:
    #     print(content)


def write_to_database(folder_path, typ,klasse=None):
    try:
        for all in os.listdir(folder_path):
            print(all)
            if os.path.splitext(all)[1] != '.tex':
                continue 

            file_path = os.path.join(folder_path, all)
            content = collect_content(file_path)

            pagebreak, punkte = get_default_info(content)
            rest_content = get_rest_from_content(content)

            section = get_section_from_content(content)
            
            _list = create_list_from_section(section)
                              
            info = None
            if typ == 1:
                name = os.path.splitext(all)[0]
                themen = [_list[0]]
                titel = _list[-3]
                af = _list[-2].lower()
                quelle = _list[-1]
                klasse = None
                if len(_list) != 5:
                    x= re.search('K.',_list[2])
                    if x != None:
                        klasse = x.group().lower()
                    
                    for string in ['MAT', 'UNIVIE']:
                        if len(_list)==6 and string in _list[2]:
                            info = string.lower()
                        elif len(_list)==7 and string in _list[3]:
                            info = string.lower()
            elif typ == 2:
                name = os.path.splitext(all)[0]
                themen = create_gk_list(_list[-3])
                titel = _list[-2]
                quelle = _list[-1]
                af = None
                klasse = None

                if 'MAT' in _list[1]:
                    info = 'mat'
                x= re.search('K.',_list[1])
                if x != None:
                    klasse = x.group().lower()
            elif typ == 0:
                name = klasse + '.' + os.path.splitext(all)[0]
                print(_list)
                themen = create_gk_list(_list[1])
                print(themen)
                themen = [klasse + '.' + x for x in themen]
                print(themen)
                titel = _list[-3]
                af = _list[-2].lower()
                quelle = _list[-1]
 
            image_list = search_for_images(rest_content)
            if image_list != []:
                bilder = image_list
            else:
                bilder = []
            # break
            add_file(table_lama, name, themen, titel, af, quelle, rest_content, punkte, pagebreak, klasse, info, bilder)
    except FileNotFoundError:
        print('not found' + folder_path)


# path_database = os.path.join(path_programm, "_database", "database_lama_1.json")
# database_lama_1 = TinyDB(path_database)

# path_database = os.path.join(path_programm, "_database", "database_lama_2.json")
# database_lama_2 = TinyDB(path_database)

# path_database = os.path.join(path_programm, "_database", "database_cria.json")
# database_cria = TinyDB(path_database)

path_database = os.path.join(path_programm, "_database", "_database.json")
path_local_database = os.path.join(path_programm, "_database", "_local_database.json")
_database = TinyDB(path_database)
_local_database = TinyDB(path_local_database)
# _database.drop_table('table_cria')
# _database.drop_tables()

# table_lama = _database.table('table_lama_1')
# table_lama = _database.table('table_lama_2')
# # table_lama = _database.table('table_cria')

dict_gk = config_loader(config_file, 'dict_gk')






########################################
##### write all files to database - working ###
######################################
# table_lama = _database.table('table_lama_1')
# for all in dict_gk.values():
#     gk = all.split(" ")[0].split("-L")[0]
# #     ###### Laptop
#     # folder_path = os.path.join("C:/","Users","Christoph", "Dropbox", "_LaMA_Aufgabensammlung", "_database","Typ1Aufgaben", "_Grundkompetenzen","WS", "WS 1.1", "Einzelbeispiele")
#     folder_path = os.path.join("C:/","Users","Christoph", "Dropbox", "_LaMA_Aufgabensammlung", "_database","Typ1Aufgaben", "_Grundkompetenzen",gk, all, "Einzelbeispiele")
# #     ##### PC
# # folder_path = os.path.join("D:/", "Dropbox", "_LaMA_Aufgabensammlung", "_database","Typ1Aufgaben", "_Grundkompetenzen","WS", "WS 1.1", "Einzelbeispiele")
# # #     folder_path = os.path.join("D:/", "Dropbox", "_LaMA_Aufgabensammlung", "_database","Typ1Aufgaben", "_Grundkompetenzen",gk, all, "Einzelbeispiele")
# # #     #######
#     write_to_database(folder_path, 1)
# ######## typ 2 ############
# table_lama = _database.table('table_lama_2')
# folder_path = os.path.join("C:/","Users","Christoph", "Dropbox", "_LaMA_Aufgabensammlung", "_database","Typ2Aufgaben", "Einzelbeispiele")
# # # folder_path = os.path.join("D:/", "Dropbox", "_LaMA_Aufgabensammlung", "_database","Typ2Aufgaben", "Einzelbeispiele")
# write_to_database(folder_path, 2)
# #############################

# ######## cria ############
# table_lama = _database.table('table_cria')
# table_lama.truncate()
# for all in ['k1','k2','k3','k4']:
#     # folder_path = os.path.join("C:/","Users","Christoph", "Dropbox", "_LaMA_Aufgabensammlung", "_database",all, "Einzelbeispiele")
#     folder_path = os.path.join("D:/", "Dropbox", "_LaMA_Aufgabensammlung", "_database",all, "Einzelbeispiele")
#     write_to_database(folder_path, 0,all)

# #############################
# ####################################


########################################
##### create dummy local_database - working ###
######################################
# def create_local_database(typ):
#     if typ == 1:
#         folder_path = os.path.join("D:/", "Dropbox", "_LaMA_Aufgabensammlung", "_database","Typ1Aufgaben", "_Grundkompetenzen","WS", "WS 1.1", "Einzelbeispiele")
#     #     # folder_path = os.path.join("C:/","Users","Christoph", "Dropbox", "_LaMA_Aufgabensammlung", "_database","Typ1Aufgaben", "_Grundkompetenzen","WS", "WS 1.1", "Einzelbeispiele")
#         write_to_database(folder_path,1)
#     elif typ == 2:
#         folder_path = os.path.join("D:/", "Dropbox", "_LaMA_Aufgabensammlung", "_database","Typ1Aufgaben", "_Grundkompetenzen","WS", "WS 1.1", "Einzelbeispiele")
#     #     # folder_path = os.path.join("C:/","Users","Christoph", "Dropbox", "_LaMA_Aufgabensammlung", "_database","Typ1Aufgaben", "_Grundkompetenzen","WS", "WS 1.1", "Einzelbeispiele")
#         write_to_database(folder_path,2)
#     elif typ == 0:        
#         for all in ['k3','k4']:
#             # folder_path = os.path.join("C:/","Users","Christoph", "Dropbox", "_LaMA_Aufgabensammlung", "_database",all, "Einzelbeispiele")
#             folder_path = os.path.join("D:/", "Dropbox", "_LaMA_Aufgabensammlung", "_database",all, "Einzelbeispiele")
#             write_to_database(folder_path,0,all)

# path_local_database = os.path.join(path_programm, "_database", "_local_database.json")
# _local_database = TinyDB(path_local_database)


# table_lama = _local_database.table('table_lama_1')
# create_local_database(1)

# # table_lama = _local_database.table('table_lama_2')
# # create_local_database()

# table_lama = _local_database.table('table_cria')
# create_local_database(0)

############################################################
# table_lama = _local_database.table('table_lama_2')
# table_lama.update({'abstand' : 0})
# table_lama = _local_database.table('table_cria')
# # # table_lama.truncate()
# create_local_database()



# print('done')