import os
import shutil
from config import path_programm, is_empty
from work_with_content import collect_content

def edit_content_ausgleichspunkte(self, aufgabe, content):
    content = [line.replace("\\fbox{A}", "") for line in content]
    for ausgleichspunkte in self.dict_all_infos_for_file[
        "dict_ausgleichspunkte"
    ][aufgabe]:
        ausgleichspunkte = ausgleichspunkte.replace('ITEM','').replace('SUBitem','').strip()
        if ausgleichspunkte.startswith('{'):
            ausgleichspunkte = ausgleichspunkte[1:]

        content = [
            line.replace(
                ausgleichspunkte.partition("\n")[0],
                "\\fbox{A} " + ausgleichspunkte.partition("\n")[0],
            )
            for line in content
        ]
    return content

def edit_content_hide_show_items(self,aufgabe, content):
    for item in self.dict_all_infos_for_file["dict_hide_show_items"][aufgabe]:
        hide_item = item.split('\n')[0]
        hide_item = hide_item.replace('ITEM','').replace('SUBitem','').strip()

        start_index=-1
        end_index=-1
        for idx, line in enumerate(content):
            if start_index == -1:
                if hide_item in line:
                    start_index=idx
                    continue
            else:
                if '\\item' in line:
                    end_index=idx
                    break
                if "\\end{aufgabenstellung}" in line:
                    end_index=idx
                    break
                if "Lösungserwartung" in line:
                    break
        if start_index==-1 or end_index==-1:
            warning_window("Das Ein- bzw. Ausblenden von Aufgabenstellungen in Aufgabe {} konnte leider nicht durchgeführt werden.\n"
            "Die Aufgabe wird daher vollständig angezeigt. Bitte bearbeiten sie diese Aufgabe manuell.".format(aufgabe))                
        else:
            for i in reversed(range(start_index+1)):
                if '\\item' in content[i]:         
                    start_index=i
                    break
            for index, line in enumerate(content[start_index:end_index]):
                content[start_index+index]='% '+line

    return content

def copy_logo_to_target_path(self, logo_path):
    logo_name = os.path.basename(logo_path)
    logo_titlepage_path = os.path.join(
        path_programm, "Teildokument", logo_name
    )
    if os.path.isfile(logo_titlepage_path):
        shutil.copy(
            logo_titlepage_path,
            os.path.join(
                os.path.dirname(
                    self.chosen_path_schularbeit_erstellen[0]
                ),
                logo_name,
            ),
        )
        return True
    else:
        return False




def edit_content_vorschau(self):
    for aufgabe in self.list_alle_aufgaben_sage:

        content = collect_content(self, aufgabe)
        

        if self.chosen_program == 'lama':
            typ=self.get_aufgabentyp(aufgabe)


            if aufgabe in self.dict_all_infos_for_file["dict_ausgleichspunkte"].keys():
                content = edit_content_ausgleichspunkte(self, aufgabe, content)


            if aufgabe in self.dict_all_infos_for_file["dict_hide_show_items"].keys():
                content = edit_content_hide_show_items(self, aufgabe, content)

    return content


def copy_included_images(self):
    
    if os.path.isfile(
        os.path.join(
            path_programm, "_database", "Bilder", image
        )
    ):
        shutil.copy(
            os.path.join(
                path_programm, "_database", "Bilder", image
            ),
            os.path.join(
                os.path.dirname(
                    self.chosen_path_schularbeit_erstellen[0]
                ),
                image,
            ),
        )

    elif os.path.isfile(
        os.path.join(
            path_programm,
            "_database_inoffiziell",
            "Bilder",
            image,
        )
    ):
        shutil.copy(
            os.path.join(
                path_programm,
                "_database_inoffiziell",
                "Bilder",
                image,
            ),
            os.path.join(
                os.path.dirname(
                    self.chosen_path_schularbeit_erstellen[0]
                ),
                image,
            ),
        )

    elif os.path.isfile(
        os.path.join(
            path_programm,
            "Beispieleinreichung",
            "Bilder",
            image,
        )
    ):
        shutil.copy(
            os.path.join(
                path_programm,
                "Beispieleinreichung",
                "Bilder",
                image,
            ),
            os.path.join(
                os.path.dirname(
                    self.chosen_path_schularbeit_erstellen[0]
                ),
                image,
            ),
        )


    for image in self.dict_all_infos_for_file["data_gesamt"][
        "copy_images"
    ]:
        content = [
            line.replace("../_database/Bilder/", "") for line in content
        ]
        content = [
            line.replace("../_database_inoffiziell/Bilder/", "")
            for line in content
        ]
        content = [
            line.replace("../Beispieleinreichung/Bilder/", "")
            for line in content
        ]


        # for line in content:
        #     if "begin{beispiel}" in line:
        #         beginning = line
        #         start = content.index(line) + 1
        #         beispiel_typ = "beispiel"
        #     if "begin{langesbeispiel}" in line:
        #         beginning = line
        #         start = content.index(line) + 1
        #         beispiel_typ = "langesbeispiel"

        #     if "end{beispiel}" in line or "end{langesbeispiel}" in line:
        #         ending = line
        #         end = content.index(line)

        # content = content[start:end]
        # joined_content = "".join(content)
        # sub_list = []
        # sub_list.append(beginning)
        # sub_list.append(joined_content)
        # sub_list.append(ending)
        # list_chosen_examples.append(sub_list)

        # example = list_chosen_examples[self.list_alle_aufgaben_sage.index(aufgabe)]
        # try:
        #     x, y = example[0].split("[")
        #     gk, z = y.split("]")
        # except ValueError:
        #     gk = ""

        # if (
        #     self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
        #     == "Grundkompetenzcheck"
        #     or self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
        #     == "Übungsblatt"
        # ):
        #     header = ""
        # else:
        #     if self.chosen_program=='lama' and control_counter == 0 and typ == 1:
        #         header = "\\subsubsection{Typ 1 Aufgaben}\n\n"
        #         control_counter += 1
        #     elif self.chosen_program=='lama' and control_counter == 1 and typ == 2:
        #         header = "\\subsubsection{Typ 2 Aufgaben}\n\n"
        #         control_counter += 1
        #     else:
        #         header = ""

        # if beispiel_typ == "beispiel":
        #     if gk == "":
        #         vorschau.write(
        #             "%s\\begin{beispiel}{" % header
        #             + str(spinbox_pkt)
        #             + "}\n"
        #             + example[1]
        #             + "\n"
        #             + example[2]
        #             + "\n\n"
        #         )

        #     else:
        #         vorschau.write(
        #             "%s\\begin{beispiel}[" % header
        #             + gk
        #             + "]{"
        #             + str(spinbox_pkt)
        #             + "}\n"
        #             + example[1]
        #             + "\n"
        #             + example[2]
        #             + "\n\n"
        #         )

        # elif self.chosen_program=='lama' and beispiel_typ == "langesbeispiel":
        #     vorschau.write(
        #         "\\newpage\n\n%s\\begin{langesbeispiel} \item[" % header
        #         + str(spinbox_pkt)
        #         + "]\n"
        #         + example[1]
        #         + "\n"
        #         + example[2]
        #         + "\n\n"
        #     )

        # elif self.chosen_program=='cria' and beispiel_typ == "langesbeispiel":
        #     vorschau.write(
        #         "\\begin{langesbeispiel} \item["
        #         + str(spinbox_pkt)
        #         + "]\n"
        #         + example[1]
        #         + "\n"
        #         + example[2]
        #         + "\n\n"
        #     )

        # if spinbox_abstand != 0:
        #     if spinbox_abstand == 99:
        #         vorschau.write("\\newpage \n\n")
        #     else:
        #         vorschau.write("\\vspace{" + str(spinbox_abstand) + "cm} \n\n")