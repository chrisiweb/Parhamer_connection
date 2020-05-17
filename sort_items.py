import re
import os


def atoi(text):
    return int(text) if text.isdigit() else text


def natural_keys(text):
    return [atoi(c) for c in re.split("(\d+)", text)]


def atoi_path(text):
    return int(text) if text.isdigit() else text


def natural_keys_path(text):
    return [atoi(c) for c in re.split("(\d+)", os.path.basename(text))]