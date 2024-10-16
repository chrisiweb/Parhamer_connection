import os
from re import split, search
import shutil
from config_start import database, path_localappdata_lama, path_programm
from config import is_empty
from work_with_content import collect_content
from standard_dialog_windows import critical_window



def edit_content_individual(self, aufgabe, content):
    for i, line in enumerate(content):
        if "\\begin{beispiel}" in line or "\\begin{langesbeispiel}" in line:
            start_index = i
        elif "\\end{beispiel}" in line or "\\end{langesbeispiel}" in line:
            end_index = i

    text = self.dict_all_infos_for_file["dict_individual_change"][aufgabe]

    content = content[:start_index+1] + text + content[end_index:]

    return content

def edit_content_ausgleichspunkte(self, aufgabe, split_content, full_content):
    split_content = [
        line.replace("\\fbox{A}", "")
        .replace("\\ASubitem", "\\Subitem")
        .replace("\\Aitem", "\\item")
        for line in split_content
    ]

    for all in self.dict_sage_ausgleichspunkte_chosen[aufgabe]:
        line = split_content[all]
        
        if "SUBitem" in line:
            new_line = line.replace("SUBitem", "\\ASubitem")
        elif "ITEM" in line:
            new_line = line.replace("ITEM", "\\Aitem")
        else:
            new_line = "\\fbox{{A}} {}".format(line)

        line = line.replace("ITEM", "\\item").replace("SUBitem", "\\Subitem").strip()

        full_content = full_content.replace(line, new_line)


    return full_content



def edit_content_hide_show_items(self, aufgabe, split_content, full_content):

    list_content = full_content.split("\\item")

    for i, all in enumerate(list_content):
        if "\\end{aufgabenstellung}" in all:
            x, y = all.split("\\end{aufgabenstellung}")
            break
    list_content[i]=x
    list_content.insert(i+1,"\\end{aufgabenstellung}"+y)

    # try:   

    for all in self.dict_sage_hide_show_items_chosen[aufgabe]:
        line = split_content[all]
        line = line.replace("ITEM", "").replace("SUBitem", "")


        _list_to_remove = split("{|}", line)


        line_start = None
        for x in _list_to_remove:
            if x.isspace() == False and len(x)!=0:
                line_start = x.split("\\")[0].strip() #[...] GRAFIK [...]
                line_start = line_start.replace("\n","").replace("\t","")
                break
        
        for x in reversed(_list_to_remove):
            if x.isspace() == False and len(x)!=0:
                line_end = x.split("\\")[0].strip()
                line_end = line_end.replace("\n","").replace("\t","").replace("[...] GRAFIK [...]","")
                break


        index_start=0
        for i, lines in enumerate(list_content):
            if line_start in lines.replace("\n","").replace("\t","").strip():
                index_start=i
                break

        for i, lines in enumerate(list_content[index_start:]):
            if line_end in lines.replace("\n","").replace("\t",""):
                index_end=index_start+i
                break

    try:        
        del list_content[index_start:index_end+1]
    except UnboundLocalError:
        critical_window("Beim automatisierten Ausblenden von einem oder mehreren Aufgabenstellungen in Aufgabe {} ist ein Fehler aufgetreten.".format(aufgabe),
        "Die PDF Datei wird ohne Ausblenden erstellt.")
        

    content = ""
    for i, line in enumerate(list_content):
        if i==0 or "\\end{aufgabenstellung}" in line:
            content = content + line
        else:
            content = content + "\\item" + line

            

    # content = ''.join([("" if "\\end{aufgabenstellung}" in line else "\\item")+ line for line in list_content])

    return content                        



def copy_logo_to_target_path(self, logo_path):
    logo_name = os.path.basename(logo_path)
    logo_titlepage_path = os.path.join(path_localappdata_lama, "Teildokument",logo_name)
    if os.path.isfile(logo_titlepage_path):
        shutil.copy(
            logo_titlepage_path,
            os.path.join(
                os.path.dirname(self.chosen_path_schularbeit_erstellen[0]), logo_name,
            ),
        )
        return True
    else:
        return False


def replace_image_path_in_content(string, content):
    return [line.replace(string, "") for line in content]


def edit_content_image_path(content):
    content = replace_image_path_in_content("../_database/Bilder/", content)
    content = replace_image_path_in_content("../_database_inoffiziell/Bilder/", content)
    content = replace_image_path_in_content("../_database/drafts/Bilder/", content)
    content = replace_image_path_in_content("../Lokaler_Ordner/Bilder/", content)

    return content



def edit_content_vorschau(self, aufgabe, ausgabetyp):

    content = collect_content(self, aufgabe, readlines=True)
    return content


def copy_included_images(self, image):
    path_bilder = [
        "Bilder",
        "Bilder_addon",
        "Bilder_local",
    ]

    for folder in path_bilder:
        path_image = os.path.join(database, folder, image)

        if os.path.isfile(path_image):
            saving_path = os.path.join(
                os.path.dirname(self.chosen_path_schularbeit_erstellen[0]), image
            )
            shutil.copy(path_image, saving_path)
            print(f"DONE {path_image}")
            break
    return
