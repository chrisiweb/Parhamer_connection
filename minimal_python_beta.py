import re
string = "Löse die folgende lineare Gleichung:\n\n$4x-2=\\variation{14}{22}$\n\n\\antwort{$x=\\variation{4}{6}$}"

def replace_group_variation_aufgabe(content):
    _list = re.findall("\\\\variation\{.*\}\{.*\}", content)

    # for i, all in enumerate(_list):
    #     open_count = all.count("{")
    #     close_count = all.count("}")
    #     print(open_count)
    #     print(close_count)
    #     if open_count < close_count:
    #       string = all.rsplit("}", 2)
    #       _list[i] = string[0] + "}"  

    print(_list)
    for all in _list:
        open_count=0
        close_count=0
        for i, char in enumerate(all):
            if char != "{" and char != "}":
                continue
            elif char == "{":
                open_count +=1
            elif char == "}":
                close_count +=1
            if open_count==close_count:
                start_index = i
                break
        print(start_index)
        replacement_string = all[start_index+2:-1].replace("\\", "\\\\")
        print(replacement_string)
        content = re.sub("\\\\variation\{.*\}\{.*\}", replacement_string, content)



    return content



string = replace_group_variation_aufgabe(string)
print(string)