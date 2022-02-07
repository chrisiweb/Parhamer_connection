import random
import math
import decimal
from venv import create

from numpy import isin
import os
from config_start import path_localappdata_lama, path_programm
import subprocess
from tex_minimal import tex_preamble, tex_end
from create_pdf import  open_pdf_file


list_of_topics_wizard = ['Addition', 'Subtraktion']

D = decimal.Decimal


"""\item $\begin{array}{l}
235 \cdot 123 \\ \hline
\antwortzeile \hspace{-0.5em} 1235\\
\antwortzeile \enspace 470\\
\antwortzeile 705 \\ \hline
\antwortzeile 28905 \\
\end{array}$
\antwort[\vspace{2cm}]{}"""

def get_random_number(min, max, decimal=0):
    x = round(random.uniform(min,max),decimal)

    x = D('{}'.format(x))

    x = D("{:.{prec}f}".format(x, prec=2))

    if decimal == 0:
        return int(x)
    else:
        return x


def normalize_decimal(d):
    normalized = d.normalize()
    sign, digit, exponent = normalized.as_tuple()
    return normalized if exponent <= 0 else normalized.quantize(1)

def change_to_integer(n):
    if isinstance(n, int):
        return n
    else:
        n = normalize_decimal(n)
        n = str(n).replace('.','')
        return int(n)



def get_number_of_digits(n):
    return len(str(int(n)))

def split_into_digits(n):
    # print(n)
    n = str(n).replace('.','')
    # print(n)
    # n=int(n)
    return [int(d) for d in n]

# x= get_random_number(235,235,0)
# y= get_random_number(123,123, 0)

# integer = change_to_integer(x)

# _list = split_into_digits(change_to_integer(y))

# result = []
# for digit in _list:
#     result.append(int(x*digit))

# factor_digit_length = get_number_of_digits(x)


def create_single_line_multiplication(digit):
    subresult = str(int(x*digit))

    string = '\\antwortzeile {} \\\\\n'.format(subresult)
    return string


content = ""
for all in range(20):
    x= get_random_number(10,99,0)
    y= get_random_number(10,99, 0)

    integer = change_to_integer(x)

    _list = split_into_digits(change_to_integer(y))

    result = []
    for digit in _list:
        result.append(int(x*digit))

    factor_digit_length = get_number_of_digits(x)

    content += """\item$\\begin{{array}}{{l}}
    {0} \cdot {1} \\\\ \hline
    """.format(str(x).replace('.',','),str(y).replace('.',','))

    for i, digit in enumerate(_list):
        content += create_single_line_multiplication(digit)
    
    content += '\\antwortzeile {} \\\\\n'.format(x*y)
    content += "\end{array}$\n\n"

# print(content)
titel = "Arbeitsblatt"
nummerierung = "(i)"
columns = 2

content = """
\section{{{0}}}

\\begin{{multicols}}{{{1}}}
\\begin{{enumerate}}[{2}]
{3}
\end{{enumerate}}
\end{{multicols}}
""".format(titel, columns, nummerierung, content)


print(content)

# \hspace{-0.5em} 1235 \\
# \enspace 470 \\
# 705 \\ \hline
# 28905\\
# \end{array}$"""

# def create_single_example_subtraction(minimum, maximum, commas, negative_solutions_allowed):
#     x = get_random_number(minimum,maximum, commas)
#     y= get_random_number(minimum,maximum, commas)
#     if x-y<0 and negative_solutions_allowed== False:
#         x, y = y, x

#     string = "{0} - {1} = {2}".format(str(x).replace(".",","),str(y).replace(".",","),str(x-y).replace(".",","))   
#     return [x,y,x-y, string]

# def create_list_of_examples_subtraction(examples, minimum, maximum, commas, negative_solutions_allowed):
#     list_of_examples = []

#     for _ in range(examples):
#         new_example = create_single_example_subtraction(minimum, maximum, commas, negative_solutions_allowed)
#         list_of_examples.append(new_example)

#     return list_of_examples

# def create_single_example_addition(minimum, maximum, commas):
#     x = get_random_number(minimum,maximum, commas)
#     y= get_random_number(minimum,maximum, commas)
#     string = "{0} + {1} = {2}".format(str(x).replace(".",","),str(y).replace(".",","),str(x+y).replace(".",","))
#     return [x,y,x+y, string]

# def create_list_of_examples_addition(examples, minimum, maximum, commas):
#     list_of_examples = []

#     for _ in range(examples):
#         new_example = create_single_example_addition(minimum, maximum, commas)
#         list_of_examples.append(new_example)

#     return list_of_examples

# def create_latex_string_addition(content, example, ausrichtung):
#     if ausrichtung == 0:
#         content += """
#         \item \\begin{{tabular}}{{rr}}
#         & ${0}$ \\\\
#         & ${1}$ \\\\ \hline
#         &\\antwort{{${2}$}}
#         \end{{tabular}}\n
#         """.format(str(example[0]).replace(".",","),str(example[1]).replace(".",","),str(example[2]).replace(".",","))
#     elif ausrichtung == 1:
#         content += "\item ${0} + {1} = \\antwort{{{2}}}$\n\\vspace{{\\leer}}\n\n".format(str(example[0]).replace(".",","),str(example[1]).replace(".",","),str(example[2]).replace(".",","))
#     return content

# def create_latex_string_subtraction(content, example, ausrichtung):
#     if ausrichtung == 0:
#         content += """
#         \item \\begin{{tabular}}{{rr}}
#         & ${0}$ \\\\
#         & $-{1}$ \\\\ \hline
#         &\\antwort{{${2}$}}
#         \end{{tabular}}\n
#         """.format(str(example[0]).replace(".",","), str(example[1]).replace(".",","),str(example[2]).replace(".",","))
#     elif ausrichtung == 1:
#         content += "\item ${0} - {1} = \\antwort{{{2}}}$\n\\vspace{{\\leer}}\n\n".format(str(example[0]).replace(".",","),str(example[1]).replace(".",","),str(example[2]).replace(".",","))
#     return content



# def create_latex_worksheet(list_of_examples,index, titel, columns, nummerierung, ausrichtung):
#     content = ""
    
#     for example in list_of_examples:
#         if index == 0:
#             content = create_latex_string_addition(content, example, ausrichtung)
#         elif index == 1:
#             content = create_latex_string_subtraction(content, example, ausrichtung)

#     content = """
#     \section{{{0}}}

#     \\begin{{multicols}}{{{1}}}
#     \\begin{{enumerate}}[{2}]
#     {3}
#     \end{{enumerate}}
#     \end{{multicols}}
#     """.format(titel, columns, nummerierung, content)

#     return content





path_file = os.path.join(
    path_localappdata_lama, "Teildokument", "worksheet.tex"
    )



# content = create_latex_worksheet()

with open(path_file, "w", encoding="utf8") as file:
    file.write(tex_preamble(solution="solution_on"))

    file.write(content)

    file.write(tex_end)

name = 'worksheet'
head, tail = os.path.split(name)
file_name = tail
folder_name = "{0}/Teildokument".format(path_programm)


# latex_output_file = open(
#     "{0}/Teildokument/temp.txt".format(path_localappdata_lama),
#     "w",
#     encoding="utf8",
#     errors="ignore",
# )

# drive_programm = os.path.splitdrive(path_programm)[0]
# drive_save = os.path.splitdrive(folder_name)[0]

drive = ""

terminal_command = 'cd "{1}" & latex -interaction=nonstopmode --synctex=-1 "{2}.tex" & latex -interaction=nonstopmode --synctex=-1 "{2}.tex" & dvips "{2}.dvi" & ps2pdf -dNOSAFER -dALLOWPSTRANSPARENCY "{2}.ps"'.format(
    drive, folder_name, file_name
)


process = subprocess.Popen(
    terminal_command,
    cwd=os.path.splitdrive(path_programm)[0],
    shell=True,
)

process.wait()


open_pdf_file(folder_name, file_name)