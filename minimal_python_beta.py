import re
string = "Das ist ein Test.\n\nGegeben ist der Bruch \\variation{$\\frac{3}{4}$}{$\\frac{5}{7}$}. Gib an, ob der Bruch ein echter oder unechter Bruch ist."

def replace_group_variation_aufgabe(string):
    # content = aufgabe_total['content']
    _list = re.findall("\\\\variation\{.*\}\{.*\}", string)
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
    
        replacement_string = all[start_index+2:-1]

        string = re.sub("\\\\variation\{.*\}\{.*\}", replacement_string, string)
    
    # return string
    # content = re.sub("\\variation{.?}{(.?)}", r"\1", content)



string = replace_group_variation_aufgabe(string)
# print(string)