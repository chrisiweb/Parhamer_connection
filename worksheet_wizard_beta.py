import random
import math
import decimal


import os
from config_start import path_localappdata_lama, path_programm
import subprocess
from tex_minimal import tex_preamble, tex_end
from create_pdf import  open_pdf_file


list_of_topics_wizard = ['Addition', 'Subtraktion']

D = decimal.Decimal

def get_random_number(min, max, decimal=0):
    x = round(random.uniform(min,max),decimal)

    x = D('{}'.format(x))

    x = D("{:.{prec}f}".format(x, prec=decimal))

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
        # n = normalize_decimal(n)
        n = str(n).replace('.','')
        return int(n)



def get_number_of_digits(n):
    return len(str(int(change_to_integer(n))))

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


def create_single_line_multiplication(digit, i, is_integer):
    subresult = int(change_to_integer(x)*digit)
    print(digit)
    print(get_number_of_digits(subresult))
    print(factor_digit_length)
    if get_number_of_digits(subresult) > factor_digit_length:
        dif = get_number_of_digits(subresult)-factor_digit_length
        if i == 0:
            hspace = dif*'\hspace{-0.5em}'
        elif dif > i:
            hspace = (dif-i)*'\hspace{-0.5em}'
        else:
            hspace = (i-dif)*'\enspace'
    else:
        print('smaller')
        print(i)
        dif = factor_digit_length-get_number_of_digits(subresult)  
        hspace = (i+dif)*'\enspace'
        # hspace = i*'\enspace'

    if is_integer==False:
        hspace += "\,"
    string = '\\antwortzeile {0} {1} \\\\\n'.format(hspace, str(subresult))
    return string


content = ""
for all in range(2):
    x= get_random_number(10,99,2)
    y= get_random_number(10,99,1)

    integer = change_to_integer(x)

    _list = split_into_digits(change_to_integer(y))

    result = []
    for digit in _list:
        result.append(int(x*digit))

    factor_digit_length = get_number_of_digits(x)

    content += """
\item$\\begin{{array}}{{l}}
{0} \cdot {1} \\\\ \hline
""".format(str(x).replace('.',','),str(y).replace('.',','))
    
    if isinstance(x,int):
        is_integer = True
    else:
        is_integer = False
    for i, digit in enumerate(_list):
        content += create_single_line_multiplication(digit, i, is_integer=is_integer)

    result = x*y
    if get_number_of_digits(result) > factor_digit_length:
        dif = get_number_of_digits(result)-factor_digit_length
        if i == 0:
            hspace = dif*'\hspace{-0.5em}'
        elif dif > i:
            hspace = (dif-i)*'\hspace{-0.5em}'
        else:
            hspace = (i-dif)*'\enspace'
    else:
        dif = factor_digit_length-get_number_of_digits(result)  
        hspace = (i+dif)*'\enspace'

    # string = '\\antwortzeile {0} {1} \\\\\n'.format(hspace, result)
    content += '\hline\n\\antwortzeile {0} {1}\\\\\n'.format(hspace, str(result).replace('.',','))
    content += "\end{array}$\n\\antwort[\\vspace{2cm}]{}\n\n"

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

# print(x)
# print(y)
# print(result)
# print(content)


path_file = os.path.join(
    path_localappdata_lama, "Teildokument", "worksheet.tex"
    )

with open(path_file, "w", encoding="utf8") as file:
    file.write(tex_preamble(solution="solution_on"))

    file.write(content)

    file.write(tex_end)

name = 'worksheet'
head, tail = os.path.split(name)
file_name = tail
folder_name = "{0}/Teildokument".format(path_programm)


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