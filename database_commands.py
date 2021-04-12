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

def get_rest_from_content(content):
    rest = content.split("\\begin{", 1)
    rest = "\\begin{" + rest[1]
    
    return rest

def create_list_from_section(section):
	list_collected_data = re.split("{| - |}", section)[1:-1]
	
	return list_collected_data


def add_file(name, gk, titel, af, quelle, content, klasse = 'K?', bilder=None):
    db.insert({
        'name' : name,
        'gk' : gk,
        'titel' : titel,
        'af' : af,
        'quelle' : quelle,
        'content' : content,
        'klasse' : klasse,
        'zusatz' : zusatz,
        'bilder' : bilder,
    })


def write_to_database(folder_path):
    try:
        for all in os.listdir(folder_path):
            name = os.path.splitext(all)[0]
            if os.path.splitext(all)[1] != '.tex':
                print('continued:' +all)
                continue 
            print(all)
            file_path = os.path.join(folder_path, all)
            content = collect_content(file_path)
            rest_content = get_rest_from_content(content)
            section = get_section_from_content(content)
            
            _list = create_list_from_section(section)
            print(_list)
            if len(_list) == 5:
                klasse = None
            # elif         

            print(len(_list))
            # add_file(name, _list[0], _list[-3], _list[-2], _list[-1], rest_content, _list[2])
    except FileNotFoundError:
        print('not found' + folder_path)


path_database = os.path.join(path_programm, "_database", "database_lama_1.json")
db = TinyDB(path_database)

dict_gk = config_loader(config_file, 'dict_gk')


########################################
##### write all files to database - working ###
######################################

# for all in dict_gk.values():
#     gk = all.split(" ")[0].split("-L")[0]
folder_path = os.path.join("D:/", "Dropbox", "_LaMA_Aufgabensammlung", "_database","Typ1Aufgaben", "_Grundkompetenzen","FA", "FA 1.2", "Einzelbeispiele")
# folder_path = os.path.join("D:/", "Dropbox", "_LaMA_Aufgabensammlung", "_database","Typ1Aufgaben", "_Grundkompetenzen",gk, all, "Einzelbeispiele")
write_to_database(folder_path)

print('done')