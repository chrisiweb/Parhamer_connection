import re
import os


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split("(\d+)", text)]

def sorted_gks(list_, chosen_program):
    list_ = sorted(list_, key=natural_keys)
    # print(list_)
    if chosen_program == 'lama':
        list_ = sorted(list_, key=lama_order)
    elif chosen_program == 'cria':
        list_ = sorted(list_, key = cria_order)

    print(list_)
    return list_

def cria_order(text):
    print(text.split(' - ')[2])
    # print(text.split(' - ')[2])
    return int(text.split(' - ')[2]) if text.isdigit() else text


def lama_order(text):
    if 'AG' in text.split(' - ')[0]:
        return 0
    elif 'FA' in text.split(' - ')[0]:
        return 1
    elif 'AN' in text.split(' - ')[0]:
        return 2
    elif 'WS' in text.split(' - ')[0]:
        return 3
    else:
        return 4
 
# def atoi_path(text):
#     return int(text) if text.isdigit() else text


# def natural_keys_path(text):
#     return [atoi(c) for c in re.split("(\d+)", os.path.basename(text))]