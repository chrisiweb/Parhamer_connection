import re
import os
from config import split_section


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split("(\d+)", text)]


def sorted_gks(list_, chosen_program):
    if chosen_program == "lama":
        list_ = sorted(list_, key=natural_keys)
        list_ = sorted(list_, key=lama_order)
    elif chosen_program == "cria":
        list_ = sorted(list_, key=cria_order)

    return list_


def cria_order(text):

    try:
        number = text.split(" - ")[2]
        if re.match("[0-9]+\[.+\]", number):
            split_number = re.split("\[|\]", number)
            number = split_number[0] + "." + split_number[1]
            list_ = [int(split_number[0]), int(split_number[1])]
        else:
            list_ = [int(number)]

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

