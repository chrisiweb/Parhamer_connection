import re

def collect_content(self, aufgabe):
    selected_path = self.get_dateipfad_aufgabe(aufgabe)  

    f = open(selected_path, "r", encoding="utf8")
    content = f.read()
    f.close() 

    return content

def split_all_items_of_list(chosen_list, string):
    temporary_list = []
    for all in chosen_list:
        pieces = all.split(string)
        for item in pieces:
            temporary_list.append(item)
    return temporary_list


def split_content_ausgleichspunkte_new_format(mode, content):
    ## mode ='ausgleichspunkte', 'show_hide_items'
    x = content.split("\\begin{aufgabenstellung}")[1].split("\\end{aufgabenstellung}")
    aufgabenstellung = x[0].replace("\t", "")
    # ausgleichspunkte_split_text = re.split("\n\n|\n\t", aufgabenstellung)

    # print(aufgabenstellung)
    ausgleichspunkte_split_text = aufgabenstellung.split("\\item")
    print(ausgleichspunkte_split_text)
    # if mode == 'show_hide_item':
    #     for all in ausgleichspunkte_split_text[:]:
    #         if all.isspace()==True:
    #             ausgleichspunkte_split_text.remove(all)
    #     return ausgleichspunkte_split_text


    ausgleichspunkte_split_text = split_all_items_of_list(ausgleichspunkte_split_text, "\n\n")
    ausgleichspunkte_split_text = split_all_items_of_list(ausgleichspunkte_split_text, "\n\t")
    # ausgleichspunkte_split_text = re.split("\n\n|\n\t", aufgabenstellung)


    ausgleichspunkte_split_text = split_all_items_of_list(ausgleichspunkte_split_text, "\\Subitem{")



    for all in ausgleichspunkte_split_text:
        if all.startswith(' '):
            x=all[1:]
            ausgleichspunkte_split_text[ausgleichspunkte_split_text.index(all)] = x
            
        if "\\begin{pspicture*}" in all:
            ausgleichspunkte_split_text[
                ausgleichspunkte_split_text.index(all)
            ] = "[...] GRAFIK [...]"

    for all in ausgleichspunkte_split_text:
        z = all.replace("\t", "")
        z = z.replace("\\leer", "")
        x = [
            line for line in z.split("\n") if line.strip() != ""
        ]  # delete all empty lines
        for item in x[:]:
            if "begin{" in item or "end{" in item:
                if "tabular" in item or "tabu" in item:
                    pass
                else:
                    x.remove(item)
        y = "\n".join(x)
        ausgleichspunkte_split_text[ausgleichspunkte_split_text.index(all)] = y        


    for all in ausgleichspunkte_split_text[:]:
        if all == "" or all.startswith('%'):
            ausgleichspunkte_split_text.remove(all)
    return ausgleichspunkte_split_text

def split_content_ausgleichspunkte(mode, content):
    ## mode ='ausgleichspunkte', 'show_hide_items' 
    x = re.split("Aufgabenstellung:}|Lösungserwartung:}", content)
    str_file = x[1].replace("\t", "")
    ausgleichspunkte_split_text = re.split("\n\n|\n\t", str_file)

    temp_list = []
    for all in ausgleichspunkte_split_text:
        x = ausgleichspunkte_split_text[
            ausgleichspunkte_split_text.index(all)
        ].split("\item ")
        for item in x:
            temp_list.append(item)
    ausgleichspunkte_split_text = temp_list

    # print(ausgleichspunkte_split_text)
    for all in ausgleichspunkte_split_text:
        if "\\begin{pspicture*}" in all:
            ausgleichspunkte_split_text[
                ausgleichspunkte_split_text.index(all)
            ] = "[...] GRAFIK [...]"

    for all in ausgleichspunkte_split_text:
        z = all.replace("\t", "")
        z = z.replace("\\leer", "")
        x = [
            line for line in z.split("\n") if line.strip() != ""
        ]  # delete all empty lines
        for item in x[:]:
            if "begin{" in item or "end{" in item:
                if "tabular" in item or "tabu" in item:
                    pass
                else:
                    x.remove(item)
        y = "\n".join(x)
        ausgleichspunkte_split_text[ausgleichspunkte_split_text.index(all)] = y

    for all in ausgleichspunkte_split_text[:]:
        if all == "":
            ausgleichspunkte_split_text.remove(all)

    for all in reversed(ausgleichspunkte_split_text):
        if "\\antwort{" in all:
            index_end = ausgleichspunkte_split_text.index(all)
            break

    return ausgleichspunkte_split_text, index_end