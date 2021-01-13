import re


def collect_content(self, aufgabe, readlines=False):
    selected_path = self.get_dateipfad_aufgabe(aufgabe)

    with open(selected_path, "r", encoding="utf8") as f:
        if readlines == False:
            content = f.read()
        if readlines == True:
            content = f.readlines()

    return content


def get_section_from_content(content):
    split_content = content.split("\n")
    for all in split_content:
        if "section" in all:
            section = all
            break
    try:
        return section
    except UnboundLocalError:
        return


def split_all_items_of_list(chosen_list, string):
    temporary_list = []
    for all in chosen_list:
        pieces = all.split(string)
        for item in pieces:
            temporary_list.append(item)
    return temporary_list


def delete_empty_items(liste):
    for all in liste[:]:
        if all.isspace() == True or all == "":
            liste.remove(all)

    return liste


def get_subitem(string):
    if string.startswith("ITEM"):
        return string
    else:
        return "SUBitem" + string

def split_content_no_environment(content):
    split_content = content.splitlines()
    # split_content = content.split('\\begin{beispiel}')
    # print(split_content)
    for i, line in enumerate(split_content):
        if '\\begin{langesbeispiel}' in line or '\\begin{beispiel}' in line:
            split_content = split_content[i+1:]
            break

    for i, line in enumerate(split_content):
        if '\\end{langesbeispiel}' in line or '\\end{beispiel}' in line:
            split_content = split_content[:i]
            break
    
    # print(split_content[0])
    split_content[0] = re.sub(r"[\t]*","", split_content[0]) 
    # print(string)
    content_no_environment = merge_list_to_string(split_content)
    # print(content_no_environment)
    return content_no_environment

def split_aufgaben_content_new_format(content):
    ## mode ='ausgleichspunkte', 'show_hide_items'
    try:
        x = content.split("\\begin{aufgabenstellung}")[1].split(
            "\\end{aufgabenstellung}"
        )
    except IndexError:
        return

    aufgabenstellung = x[0].replace("\t", "").replace("%Aufgabentext", "")

    aufgabenstellung_split_text = aufgabenstellung.split("\\item")

    aufgabenstellung_split_text = delete_empty_items(aufgabenstellung_split_text)

    aufgabenstellung_split_text = [
        "ITEM" + string for string in aufgabenstellung_split_text
    ]

    aufgabenstellung_split_text = split_all_items_of_list(
        aufgabenstellung_split_text, "\\Subitem"
    )
    # aufgabenstellung_split_text = split_all_items_of_list(aufgabenstellung_split_text, "\\ASubitem")
    aufgabenstellung_split_text = [
        get_subitem(string) for string in aufgabenstellung_split_text
    ]

    aufgabenstellung_split_text = split_all_items_of_list(
        aufgabenstellung_split_text, "\n\n"
    )
    aufgabenstellung_split_text = split_all_items_of_list(
        aufgabenstellung_split_text, "\n\t"
    )

    for all in aufgabenstellung_split_text:
        if all.startswith(" "):
            x = all[1:]
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
    aufgabenstellung = aufgabenstellung.replace("\\begin{enumerate}", "").replace(
        "\\end{enumerate}", ""
    )
    aufgabenstellung_split_text = aufgabenstellung.split("\\item")

    aufgabenstellung_split_text = delete_empty_items(aufgabenstellung_split_text)

    aufgabenstellung_split_text = [
        "ITEM" + string for string in aufgabenstellung_split_text
    ]

    aufgabenstellung_split_text = split_all_items_of_list(
        aufgabenstellung_split_text, "\n\n"
    )
    aufgabenstellung_split_text = split_all_items_of_list(
        aufgabenstellung_split_text, "\n\t"
    )

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


def merge_list_to_string(list_):
    combined_string = ""
    for all in list_:
        item_short = all.replace("ITEM", "")
        if item_short.isspace() == True or not item_short:
            combined_string = combined_string + all
        else:
            combined_string = combined_string + all + "\n"
    return combined_string


def prepare_content_for_hide_show_items(content):
    index = 0
    temp_list = []
    temp_content = []
    for item in content:
        if item.startswith("ITEM") and temp_list != []:
            combined_string = merge_list_to_string(temp_list)
            temp_content.append(combined_string)
            temp_list = []
            temp_list.append(item)
        else:
            temp_list.append(item)

    combined_string = merge_list_to_string(temp_list)
    temp_content.append(combined_string)

    return temp_content


def split_at_string(content, string):
    if string in content:
        temp_content = content.split(string)
        temp_content = string + temp_content[1]
        if "meinlr{" in content and temp_content.strip().endswith("}}"):
            # temp_content = '}'.join(temp_content.rsplit('}}', 1))
            temp_content = temp_content.strip()[:-1]
        content = temp_content

    return content


def edit_content_quiz(content, solution):
    aufgabenformate = [
        "\multiplechoice",
        "\langmultiplechoice",
        "\lueckentext",
        "\zuordnen",
    ]
    content = content.replace("\onehalfspacing", "")
    if "\\begin{pspicture*}" in content:
        content = content.replace(
            "\\begin{pspicture*}", "\\resizebox{!}{0.7\\textheight}{\\begin{pspicture*}"
        )
        content = content.replace("\end{pspicture*}", "\end{pspicture*}}")

    if "\langmultiplechoice" in content:
        split_content = content.split("\langmultiplechoice")
        temp_content = split_content[1]
        if "\\begin{pspicture*}" in temp_content:
            temp_content = temp_content.replace(
                "\\resizebox{!}{0.7\\textheight}", "\\resizebox{!}{0.25\\textheight}"
            )
        content = content.replace(split_content[1], temp_content)

    if "\zuordnen" in content:
        split_content = content.split("\zuordnen")
        temp_content = split_content[1]
        if "\\begin{pspicture*}" in temp_content:
            temp_content = temp_content.replace(
                "\\resizebox{!}{0.7\\textheight}", "\\resizebox{!}{0.18\\textheight}"
            )
        content = content.replace(split_content[1], temp_content)

    if solution == False:
        for all in aufgabenformate:
            if all in content:
                content = content.replace(all, "\n\\framebreak\n" + all)
    if solution == True:
        for all in aufgabenformate:
            content = split_at_string(content, all)
        # content = split_at_string(content, "\langmultiplechoice")
        # content = split_at_string(content, "\lueckentext")
        # content = split_at_string(content, "\zuordnen")

    return content
