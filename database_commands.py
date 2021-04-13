from tinydb import TinyDB, Query
import os
import sys
import re
import yaml
from config_start import path_programm
from config import config_loader, config_file
# from config import database_lama_1, _file_




# class WriteFilesToDatabase:
#     def __init__(self):
#         print('test')

# WriteFilesToDatabase()



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


def add_file(database, name, gk, titel, af, quelle, content, klasse = 'K?', info =None, bilder=None):
    database.insert({
        'name' : name,
        'gk' : gk,
        'titel' : titel,
        'af' : af,
        'quelle' : quelle,
        'content' : content,
        'klasse' : klasse,
        'info' : info,
        'bilder' : bilder,
    })

def get_default_info(content):
    if 'langesbeispiel' in content:
        typ = 'langesbeispiel'
        punkte = int(re.split('begin{langesbeispiel}.*item\[(..?)\]', content)[1])
    elif 'beispiel' in content:
        typ = 'beispiel'
        punkte = int(re.split('begin{beispiel}.*{(..?)}', content)[1])
    
    return typ, punkte



def write_to_database(folder_path):
    try:
        for all in os.listdir(folder_path):
            name = os.path.splitext(all)[0]
            if os.path.splitext(all)[1] != '.tex':
                continue 

            file_path = os.path.join(folder_path, all)
            content = collect_content(file_path)

            typ, punkte = get_default_info(content)
            rest_content = get_rest_from_content(content)
            section = get_section_from_content(content)
            
            _list = create_list_from_section(section)
            

            
            klasse = None
            info = None
            if len(_list) != 5:
                x= re.search('K.',_list[2])
                if x != None:
                    klasse = x.group()
                
                for string in ['MAT', 'UNIVIE']:
                    if len(_list)==6 and string in _list[2]:
                        info = string
                    elif len(_list)==7 and string in _list[3]:
                        info = string 



            add_file(database_lama_1, name, _list[0], _list[-3], _list[-2], _list[-1], rest_content, klasse, info)
    except FileNotFoundError:
        print('not found' + folder_path)


path_database = os.path.join(path_programm, "_database", "database_lama_1.json")
database_lama_1 = TinyDB(path_database)

dict_gk = config_loader(config_file, 'dict_gk')






########################################
##### write all files to database - working ###
######################################

# for all in dict_gk.values():
#     gk = all.split(" ")[0].split("-L")[0]
#     ###### Laptop
folder_path = os.path.join("C:/","Users","Christoph", "Dropbox", "_LaMA_Aufgabensammlung", "_database","Typ1Aufgaben", "_Grundkompetenzen","WS", "WS 1.1", "Einzelbeispiele")
#     # folder_path = os.path.join("C:/","Users","Christoph", "Dropbox", "_LaMA_Aufgabensammlung", "_database","Typ1Aufgaben", "_Grundkompetenzen",gk, all, "Einzelbeispiele")
#     ##### PC
#     # folder_path = os.path.join("D:/", "Dropbox", "_LaMA_Aufgabensammlung", "_database","Typ1Aufgaben", "_Grundkompetenzen","FA", "FA 1.2", "Einzelbeispiele")
#     folder_path = os.path.join("D:/", "Dropbox", "_LaMA_Aufgabensammlung", "_database","Typ1Aufgaben", "_Grundkompetenzen",gk, all, "Einzelbeispiele")
#     #######
write_to_database(folder_path)



_file_=Query()

# print(database_lama_1.search(_file_.name == "AG-L 3.6 - 1"))

print('done')