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

def get_subitem(string):
    if string.startswith('ITEM'):
        return string
    else:
        return 'SUBitem'+string

def split_aufgaben_content_new_format(content):
    ## mode ='ausgleichspunkte', 'show_hide_items'
    try:
        x = content.split("\\begin{aufgabenstellung}")[1].split("\\end{aufgabenstellung}")
    except IndexError:
        return
 
    aufgabenstellung = x[0].replace("\t", "").replace("%Aufgabentext","")
    # aufgabenstellung_split_text = re.split("\n\n|\n\t", aufgabenstellung)
    # aufgabenstellung = aufgabenstellung.replace('%Aufgabentext','')
    # print(aufgabenstellung)
    aufgabenstellung_split_text = aufgabenstellung.split("\\item")

    aufgabenstellung_split_text = delete_empty_items(aufgabenstellung_split_text)
    # print(aufgabenstellung_split_text)
    # for all in aufgabenstellung_split_text[:]:
    #     if all.isspace()==True:
    #         aufgabenstellung_split_text.remove(all)
    aufgabenstellung_split_text=['ITEM' + string for string in aufgabenstellung_split_text]
    
    
    # if mode == 'show_hide_item':
    #     for all in aufgabenstellung_split_text[:]:
    #         if all.isspace()==True:
    #             aufgabenstellung_split_text.remove(all)
    #     return aufgabenstellung_split_text


   
    # aufgabenstellung_split_text = re.split("\n\n|\n\t", aufgabenstellung)


    aufgabenstellung_split_text = split_all_items_of_list(aufgabenstellung_split_text, "\\Subitem")
    aufgabenstellung_split_text=[get_subitem(string) for string in aufgabenstellung_split_text]

    aufgabenstellung_split_text = split_all_items_of_list(aufgabenstellung_split_text, "\n\n")
    aufgabenstellung_split_text = split_all_items_of_list(aufgabenstellung_split_text, "\n\t")

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


    aufgabenstellung_split_text = delete_empty_items(aufgabenstellung_split_text)

    return aufgabenstellung_split_text


def split_aufgaben_content(content):
    ## mode ='ausgleichspunkte', 'show_hide_items'
    x = re.split("Aufgabenstellung:}|Lösungserwartung:}", content)
    try:
        aufgabenstellung = x[1].replace("\t", "")
    except IndexError:
        return
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

def prepare_content_for_hide_show_items(content):
    # print(content)
    # temp_content = content
    index=0
    temp_list=[]
    temp_content=[]
    for item in content:
        if item.startswith('ITEM') and temp_list!=[]:
            combined_string=''
            for all in temp_list:
                if all.replace('ITEM','').isspace()==True:
                    combined_string = combined_string + all
                else:
                    combined_string = combined_string + all + '\n\n'

            temp_content.append(combined_string)
            temp_list = []
            temp_list.append(item)
        else:
            temp_list.append(item)

    return temp_content