import enum
import re
import os
from config import *


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split("(\d+)", text)]


def get_typ(string):
    if re.match("[A-Z]", string):
        return 'lama_1'
    elif re.match("k[0-9]\.", string):
        return 'cria'
    else:
        return 'lama_2'
    

def sort_variation(num, _list):
    if re.match("[0-9]+\[.+\]", str(num)):
        split_number = re.split("\[|\]", num)
        _list.append(int(split_number[0]))
        _list.append(int(split_number[1]))
    else:
        _list.append(int(num))
    
    return _list

def order_gesammeltedateien(text, typ, cria_plain_number_order=False):
    
    # typ = get_typ(text['name'])
    # print(current_program) #lama_1, lama_2, cria
    name = text['name'].replace('i.','').replace('l.','')
    # print(text)
    # get_typ(text['name'])
    # return 0

    # ###### typ_1 working
    # if re.match
    _list = []
    if typ == 'lama_1':
        for i, gk  in enumerate(dict_gk.values()):
            if gk in name:
                _list.append(i)
                num = name.split(" - ")[-1]
        for i, thema in enumerate(zusatzthemen_beschreibung.keys()):
            if thema.upper() in name.upper():
                index = 1000+i
                _list.append(index)
                num = name.split(" - ")[-1]


    elif typ == 'cria':
        if cria_plain_number_order == True:
            num = name

        else:
            num = name  
            thema = text['themen'][-1]
            temp_list = []
            for klasse in list_klassen:
                dict_klasse_name = eval("dict_{}_name".format(klasse))
                dict_klasse = eval("dict_{}".format(klasse))
                for topic in dict_klasse_name:
                    for subtopic in dict_klasse[topic]:
                        temp_list.append(f"{topic}.{subtopic}")

            # print(temp_list)
            try:
                thema_index = temp_list.index(thema)
            except ValueError:
                thema_index = 0
            # print(num)
            
        # # print(_list)
        # _list = sort_variation(num, _list)
        # print(_list)
        # num = name
        
        
    elif typ == 'lama_2':
        num = name



    if 'l.' in text['name']:
        _list.append(0)
    elif 'i.' in text['name']:
        _list.append(2)
    else:
        _list.append(1)

    if typ == 'cria' and cria_plain_number_order == False:
        _list.append(thema_index)

    # print(_list)
    _list = sort_variation(num, _list)
    #print(_list)
    return _list



def sorted_gks(list_, chosen_program):
    if chosen_program == "lama":
        list_ = sorted(list_, key=natural_keys)
        list_ = sorted(list_, key=lama_order)
    elif chosen_program == "cria":
        list_ = sorted(list_, key=cria_order)

    return list_


def cria_order(text):
    if "*Lokal*" in text.split(" - ")[0]:
        list_ = [0]
    elif "i." in text.split(" - ")[2]:
        list_ = [2]
    else:
        list_ = [1] 
    try:
        number = text.split(" - ")[2]
        number = number.replace("i.","")
        if re.match("[0-9]+\[.+\]", number):
            split_number = re.split("\[|\]", number)
            list_.append(int(split_number[0]))
            list_.append(int(split_number[1]))
        else:
            list_.append(int(number))
        return list_
    except ValueError:
        print("Wrong section format: {}".format(text))
        return []


def lama_order(text):
    if "Lokal" in text.split(" - ")[0]:
        return 0
    elif "AG" in text.split(" - ")[0]:
        return 1
    elif "FA" in text.split(" - ")[0]:
        return 2
    elif "AN" in text.split(" - ")[0]:
        return 3
    elif "WS" in text.split(" - ")[0]:
        return 4
    else:
        return 5


def sortTopics(item):
    # print(item)
    for index_1, klasse in enumerate(list_klassen):
        # print(f"INDEX 1: {index_1}")
        dict_klasse = eval("dict_{}".format(klasse))
        for index_2, topic in enumerate(dict_klasse):
            # print(index_2)
            # print(dict_klasse[topic])

            for index_3, subtopic in enumerate(dict_klasse[topic]):
                if item == f"{topic}.{subtopic}":
                    # print('TRUE')
                    return [index_1, index_2, index_3]


def typ2_order(text):
    number = re.split("section{| - ", text)[1]
    if "*Lokal*" in number:
        number = number.replace("*Lokal* ","")
        list_ = [0]
        # number = str(1) + number
        # return [0,int(number)]

    elif "i." in number:
        number = number.replace("i.","")
        list_ = [2]

    else:
        list_ = [1]

    list_.append(int(number))
    return list_

