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

def delete_empty_items(liste):
    for all in liste[:]:
        if all.isspace()==True or all == '':
            liste.remove(all)

    return liste    

def split_aufgaben_content_new_format(content):
    ## mode ='ausgleichspunkte', 'show_hide_items'
    x = content.split("\\begin{aufgabenstellung}")[1].split("\\end{aufgabenstellung}")
    aufgabenstellung = x[0].replace("\t", "")
    # aufgabenstellung_split_text = re.split("\n\n|\n\t", aufgabenstellung)

    # print(aufgabenstellung)
    aufgabenstellung_split_text = aufgabenstellung.split("\\item")

    aufgabenstellung_split_text = delete_empty_items(aufgabenstellung_split_text)
    # for all in aufgabenstellung_split_text[:]:
    #     if all.isspace()==True:
    #         aufgabenstellung_split_text.remove(all)

    aufgabenstellung_split_text=['ITEM' + string for string in aufgabenstellung_split_text]

    # print(aufgabenstellung_split_text)
    # if mode == 'show_hide_item':
    #     for all in aufgabenstellung_split_text[:]:
    #         if all.isspace()==True:
    #             aufgabenstellung_split_text.remove(all)
    #     return aufgabenstellung_split_text


    aufgabenstellung_split_text = split_all_items_of_list(aufgabenstellung_split_text, "\n\n")
    aufgabenstellung_split_text = split_all_items_of_list(aufgabenstellung_split_text, "\n\t")
    # aufgabenstellung_split_text = re.split("\n\n|\n\t", aufgabenstellung)


    aufgabenstellung_split_text = split_all_items_of_list(aufgabenstellung_split_text, "\\Subitem{")



    for all in aufgabenstellung_split_text:
        if all.startswith(' '):
            x=all[1:]
            aufgabenstellung_split_text[aufgabenstellung_split_text.index(all)] = x
            
        if "\\begin{pspicture*}" in all:
            aufgabenstellung_split_text[
                aufgabenstellung_split_text.index(all)
            ] = "[...] GRAFIK [...]"

    for all in aufgabenstellung_split_text:
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
        aufgabenstellung_split_text[aufgabenstellung_split_text.index(all)] = y        


    for all in aufgabenstellung_split_text[:]:
        if all == "" or all.startswith('%'):
            aufgabenstellung_split_text.remove(all)
    return aufgabenstellung_split_text


def split_aufgaben_content(content):
    ## mode ='ausgleichspunkte', 'show_hide_items' 
    x = re.split("Aufgabenstellung:}|Lösungserwartung:}", content)
    aufgabenstellung = x[1].replace("\t", "")
    aufgabenstellung = aufgabenstellung.replace("\\begin{enumerate}","").replace("\\end{enumerate}","")
    aufgabenstellung_split_text = aufgabenstellung.split("\\item")

    aufgabenstellung_split_text = delete_empty_items(aufgabenstellung_split_text)
    # for all in aufgabenstellung_split_text[:]:
    #     if all.isspace()==True:
    #         aufgabenstellung_split_text.remove(all)

    aufgabenstellung_split_text=['ITEM' + string for string in aufgabenstellung_split_text]


    aufgabenstellung_split_text = split_all_items_of_list(aufgabenstellung_split_text, "\n\n")
    aufgabenstellung_split_text = split_all_items_of_list(aufgabenstellung_split_text, "\n\t")
    
    # temp_list = []
    # for all in aufgabenstellung_split_text:
    #     x = aufgabenstellung_split_text[
    #         aufgabenstellung_split_text.index(all)
    #     ].split("\item ")
    #     for item in x:
    #         temp_list.append(item)
    # aufgabenstellung_split_text = temp_list

    # print(aufgabenstellung_split_text)

    for all in aufgabenstellung_split_text:
        if "\\begin{pspicture*}" in all:
            aufgabenstellung_split_text[
                aufgabenstellung_split_text.index(all)
            ] = "[...] GRAFIK [...]"

    for all in aufgabenstellung_split_text:
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
        aufgabenstellung_split_text[aufgabenstellung_split_text.index(all)] = y

    # for all in aufgabenstellung_split_text[:]:
    #     if all == "":
    #         aufgabenstellung_split_text.remove(all)
    aufgabenstellung_split_text = delete_empty_items(aufgabenstellung_split_text)

    for all in reversed(aufgabenstellung_split_text):
        if "\\antwort{" in all:
            index_end = aufgabenstellung_split_text.index(all)
            break

    return aufgabenstellung_split_text, index_end