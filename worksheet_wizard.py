import random
import math
import os
from config_start import path_localappdata_lama, path_programm
import decimal
import subprocess
from tex_minimal import tex_preamble, tex_end
from create_pdf import create_pdf, open_pdf_file, build_pdf_file


list_of_topics_wizard = ['Addition', 'Subtraktion']

D = decimal.Decimal


def get_random_number(min, max, decimal=0):
    x = round(random.uniform(min,max),decimal)

    x = D('{}'.format(x))

    x = D("{:.{prec}f}".format(x, prec=2))

    if decimal == 0:
        return int(x)
    else:
        return x



def create_single_example_subtraction(minimum, maximum, commas, negative_solutions_allowed):
    x = get_random_number(minimum,maximum, commas)
    y= get_random_number(minimum,maximum, commas)
    if x-y<0 and negative_solutions_allowed== False:
        x, y = y, x

    string = "{0} - {1} = {2}".format(str(x).replace(".",","),str(y).replace(".",","),str(x-y).replace(".",","))   
    return [x,y,x-y, string]

def create_list_of_examples_subtraction(examples, minimum, maximum, commas, negative_solutions_allowed):
    list_of_examples = []

    for _ in range(examples):
        new_example = create_single_example_subtraction(minimum, maximum, commas, negative_solutions_allowed)
        list_of_examples.append(new_example)

    return list_of_examples

def create_single_example_addition(minimum, maximum, commas):
    x = get_random_number(minimum,maximum, commas)
    y= get_random_number(minimum,maximum, commas)
    string = "{0} + {1} = {2}".format(str(x).replace(".",","),str(y).replace(".",","),str(x+y).replace(".",","))
    return [x,y,x+y, string]

def create_list_of_examples_addition(examples, minimum, maximum, commas):
    list_of_examples = []

    for _ in range(examples):
        new_example = create_single_example_addition(minimum, maximum, commas)
        list_of_examples.append(new_example)

    return list_of_examples

def create_worksheet_add_subtract(list_of_examples,index, titel, columns, nummerierung, ausrichtung):
    content = ""
    if index == 0:
        operation = "+"
        zusatz = ""
        
    elif index == 1:
        zusatz = "-"
        operation = "-"

    for all in list_of_examples:
        if ausrichtung == 0:
            content += """
            \item \\begin{{tabular}}{{rr}}
            & ${0}$ \\\\
            & ${1}{2}$ \\\\ \hline
            &\\antwort{{${3}$}}
            \end{{tabular}}\n
            """.format(str(all[0]).replace(".",","), zusatz,str(all[1]).replace(".",","),str(all[2]).replace(".",","))
        elif ausrichtung == 1:
            content += "\item ${0} {1} {2} = \\antwort{{{3}}}$\n\\vspace{{\\leer}}\n\n".format(str(all[0]).replace(".",","),operation ,str(all[1]).replace(".",","),str(all[2]).replace(".",","))
    content = """
    \section{{{0}}}

    \\begin{{multicols}}{{{1}}}
    \\begin{{enumerate}}[{2}]
    {3}
    \end{{enumerate}}
    \end{{multicols}}
    """.format(titel, columns, nummerierung, content)

    return content

