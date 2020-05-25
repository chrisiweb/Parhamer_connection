import re
import os


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split("(\d+)", text)]

def sorted_gks(list_):
    list_ = sorted(list_, key=natural_keys)
    list_ = sorted(list_, key=gk_order)

    return list_


def gk_order(text):
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