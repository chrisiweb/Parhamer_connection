import re
import os


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split("(\d+)", text)]

def sorted_gks(list_, chosen_program):
    list_ = sorted(list_, key=natural_keys)

    if chosen_program == 'lama':
        list_ = sorted(list_, key=lama_order)
    elif chosen_program == 'cria':
        list_ = sorted(list_, key = cria_order)
    
    return list_

def cria_order(text):
    try:
        return int(text.split(' - ')[2])
    except ValueError:
        print('Wrong section format. "{}"'.format(text))
        return 0
    # print(x)
    #return [atoi(c) for c in text.split(' - ')[2]]


def lama_order(text):
    if 'Lokal' in text.split(' - ')[0]:
        return 0
    elif 'AG' in text.split(' - ')[0]:
        return 1
    elif 'FA' in text.split(' - ')[0]:
        return 2
    elif 'AN' in text.split(' - ')[0]:
        return 3
    elif 'WS' in text.split(' - ')[0]:
        return 4
    else:
        return 5
 
# def atoi_path(text):
#     return int(text) if text.isdigit() else text


# def natural_keys_path(text):
#     return [atoi(c) for c in re.split("(\d+)", os.path.basename(text))]