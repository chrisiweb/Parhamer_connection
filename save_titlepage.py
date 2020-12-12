import os
import json
from config import path_programm, path_localappdata_lama

def create_file_titlepage(titlepage_save):
    if os.path.isfile(titlepage_save):
        with open(titlepage_save, encoding="utf8") as f:
            titlepage = json.load(f)
    else:
        titlepage = {
            "logo": False,
            "logo_path": False,
            "titel": True,
            "datum": True,
            "klasse": True,
            "name": True,
            "note": False,
            "unterschrift": False,
            "hide_all": False,
        }
    return titlepage


def check_format_titlepage_save(filename):
    path = os.path.join(path_localappdata_lama, "Teildokument", filename)
    try:
        titlepage = create_file_titlepage(path)
    except json.decoder.JSONDecodeError:
        print(
            'The file "{}" has an invalid format. The standard was restored!'.format(
                filename
            )
        )
        titlepage = {
            "logo": False,
            "logo_path": False,
            "titel": True,
            "datum": True,
            "klasse": True,
            "name": True,
            "note": False,
            "unterschrift": False,
            "hide_all": False,
        }
        with open(path, "w+", encoding="utf8") as f:
            json.dump(titlepage, f, ensure_ascii=False)

    return titlepage