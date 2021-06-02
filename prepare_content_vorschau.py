import os
from re import split
import shutil
from config_start import database, path_localappdata_lama
from config import is_empty
from work_with_content import collect_content #, split_content_no_environment
from standard_dialog_windows import warning_window


def edit_content_individual(self, aufgabe, content):
    # print(content)
    for i, line in enumerate(content):
        if "\\begin{beispiel}" in line or "\\begin{langesbeispiel}" in line:
            start_index = i
        elif "\\end{beispiel}" in line or "\\end{langesbeispiel}" in line:
            end_index = i
    # print(start_index)
    # print(end_index)
    text = self.dict_all_infos_for_file["dict_individual_change"][aufgabe]
    # print(text)
    # split_text = text.splitlines()
    # print(text)
    # print(split_text)
    # print(content[:start_index+1])
    # print(content[end_index:])
    content = content[:start_index+1] + text + content[end_index:]
    # split_text = split_content_no_environment(text)
    # print(split_text)
    # print(content)
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


    # content[all] = line
    # for i, line in enumerate(content):
    #     ausgleichspunkte = (
    #         ausgleichspunkte.replace("ITEM", "").replace("SUBitem", "").strip()
    #     )

    # return content
    # for ausgleichspunkte in self.dict_all_infos_for_file["dict_ausgleichspunkte"][
    #     aufgabe
    # ]:
    #     for i, line in enumerate(content):
    #         ausgleichspunkte = (
    #             ausgleichspunkte.replace("ITEM", "").replace("SUBitem", "").strip()
    #         )
    #         if ausgleichspunkte.partition("\n")[0] in line:
    #             if "\\Subitem" in line:
    #                 line = line.replace("\\Subitem", "\\ASubitem")
    #             else:
    #                 if ausgleichspunkte.startswith("{"):
    #                     ausgleichspunkte = ausgleichspunkte[1:]

    #                 line = line.replace(
    #                     ausgleichspunkte.partition("\n")[0],
    #                     "\\fbox{A} " + ausgleichspunkte.partition("\n")[0],
    #                 )
    #             content[i] = line
    #             break
    #         if i + 1 == len(content):
    #             warning_window(
    #                 "Leider ist ein Fehler beim Bearbeiten der Ausgleichspunkte augetreten",
    #                 detailed_text="Bitte ändern Sie die Ausgleichspunkte nach dem Erstellen manuell in der LaTeX-Datei.",
    #             )
    #             return content

    # return content


def edit_content_hide_show_items(self, aufgabe, content):
    for item in self.dict_all_infos_for_file["dict_hide_show_items"][aufgabe]:
        hide_item = item.split("\n")[0]
        hide_item = hide_item.replace("ITEM", "").replace("SUBitem", "").strip()

        start_index = -1
        end_index = -1
        for idx, line in enumerate(content):
            if start_index == -1:
                if hide_item in line:
                    start_index = idx
                    continue
            else:
                if "\\item" in line:
                    end_index = idx
                    break
                if "\\end{aufgabenstellung}" in line:
                    end_index = idx
                    break
                if "Lösungserwartung" in line:
                    break
        if start_index == -1 or end_index == -1:
            warning_window(
                "Das Ein- bzw. Ausblenden von Aufgabenstellungen in Aufgabe {} konnte leider nicht durchgeführt werden.\n"
                "Die Aufgabe wird daher vollständig angezeigt. Bitte bearbeiten sie diese Aufgabe manuell.".format(
                    aufgabe
                )
            )
        else:
            for i in reversed(range(start_index + 1)):
                if "\\item" in content[i]:
                    start_index = i
                    break
            for index, line in enumerate(content[start_index:end_index]):
                content[start_index + index] = "% " + line

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
    # print(content)
    if aufgabe in self.dict_all_infos_for_file["dict_individual_change"]:
        if not is_empty(self.dict_all_infos_for_file["dict_individual_change"][aufgabe]):
            # print(aufgabe)
            # print(self.dict_all_infos_for_file["dict_individual_change"])
            content = edit_content_individual(self, aufgabe, content)
            # content = self.dict_all_infos_for_file["dict_individual_change"][aufgabe] 
            # print(content)

    elif self.chosen_program == "lama":
        typ = self.get_aufgabentyp(aufgabe)

        if aufgabe in self.dict_all_infos_for_file["dict_ausgleichspunkte"].keys():
            content = edit_content_ausgleichspunkte(self, aufgabe, content)

        if aufgabe in self.dict_all_infos_for_file["dict_hide_show_items"].keys():
            content = edit_content_hide_show_items(self, aufgabe, content)

        

    if (
        ausgabetyp == "schularbeit"
        and is_empty(self.dict_all_infos_for_file["data_gesamt"]["copy_images"])
        == False
    ):
        content = edit_content_image_path(content)

    return content


def copy_included_images(self, image):
    draft_path = os.path.join("_database", "drafts")
    path_bilder = [
        "_database",
        "_database_inoffiziell",
        draft_path,
        "Lokaler_Ordner",
    ]

    for folder in path_bilder:
        path_image = os.path.join(database, folder, "Bilder", image)
        if os.path.isfile(path_image):
            saving_path = os.path.join(
                os.path.dirname(self.chosen_path_schularbeit_erstellen[0]), image
            )
            shutil.copy(path_image, saving_path)
            break
    return
