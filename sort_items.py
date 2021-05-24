import re
import os
from config import split_section, dict_gk


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
    

def order_gesammeltedateien(text):
    typ = get_typ(text['name'])
    name = text['name'].replace('i.','')
    # print(text['name'])
    # get_typ(text['name'])
    # return 0

    # ###### typ_1 working
    # if re.match
    if typ == 'lama_1':
        for i, gk  in enumerate(dict_gk.values()):
            if gk in name:
                _list = [i]
                num = name.split(" - ")[-1]
    elif typ == 'cria':
        num = name.split('.')[-1]
        _list = []

    elif typ == 'lama_2':
        num = name
        _list = []

    if re.match("[0-9]+\[.+\]", num):
        split_number = re.split("\[|\]", num)
        _list.append(int(split_number[0]))
        _list.append(int(split_number[1]))
    else:
        _list.append(int(num))
    print(_list)
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

