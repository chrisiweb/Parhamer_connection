import random
import math
import decimal
import re

import os

from numpy import empty
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
    n = str(n).replace('.','')
    return [int(d) for d in n]



def get_all_pixels():
    return re.findall("[A-J][0-9]",content)   


all_nonogramms = {'cat': ["A3", "A6", "A7", "B1", "B2", "B3", "B4", "B6", "B9", "C0", "C1", "C2", "C4",
"C5", "C6", "C7", "C8", "C9", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "E0", "E1", "E2", "E4",
"E5", "E6", "E7", "E8", "E9", "F1", "F2", "F3", "F4", "F6", "F7", "F8", "F9", "G3", "G7", "G8",
"G9", "H8", "H9", "I4", "I5", "I6", "I8", "J3", "J4", "J6", "J7", "J8"],
}


solution_cat = ["A3", "A6", "A7", "B1", "B2", "B3", "B4", "B6", "B9", "C0", "C1", "C2", "C4",
"C5", "C6", "C7", "C8", "C9", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "E0", "E1", "E2", "E4",
"E5", "E6", "E7", "E8", "E9", "F1", "F2", "F3", "F4", "F6", "F7", "F8", "F9", "G3", "G7", "G8",
"G9", "H8", "H9", "I4", "I5", "I6", "I8", "J3", "J4", "J6", "J7", "J8"]

# liste = list(all_nonogramms.keys())
# y = random.choice(liste)
# print(y)
random.shuffle(solution_cat)
print(solution_cat)

content ="""\meinlr{
\\renewcommand{\\arraystretch}{1.2}
\\begin{tabular}{c|p{0,3cm}|p{0,3cm}|p{0,3cm}|p{0,3cm}|p{0,3cm}|p{0,3cm}|p{0,3cm}|p{0,3cm}|p{0,3cm}|p{0,3cm}|}
\multicolumn{1}{l}{}&\multicolumn{1}{c}{A}&\multicolumn{1}{c}{B}&\multicolumn{1}{c}{C}&\multicolumn{1}{c}{D}&\multicolumn{1}{c}{E}&\multicolumn{1}{c}{F}&\multicolumn{1}{c}{G}&\multicolumn{1}{c}{H}&\multicolumn{1}{c}{I}&\multicolumn{1}{c}{J}\\\\ \cline{2-11}
0& A0 & B0 & C0 & D0 & E0 & F0 & G0 & H0 & I0 & J0 \\\\ \cline{2-11}
1& A1 & B1 & C1 & D1 & E1 & F1 & G1 & H1 & I1 & J1 \\\\ \cline{2-11}
2& A2 & B2 & C2 & D2 & E2 & F2 & G2 & H2 & I2 & J2 \\\\ \cline{2-11} 
3& A3 & B3 & C3 & D3 & E3 & F3 & G3 & H3 & I3 & J3 \\\\ \cline{2-11}
4& A4 & B4 & C4 & D4 & E4 & F4 & G4 & H4 & I4 & J4 \\\\ \cline{2-11}
5& A5 & B5 & C5 & D5 & E5 & F5 & G5 & H5 & I5 & J5 \\\\ \cline{2-11}
6& A6 & B6 & C6 & D6 & E6 & F6 & G6 & H6 & I6 & J6 \\\\ \cline{2-11}
7& A7 & B7 & C7 & D7 & E7 & F7 & G7 & H7 & I7 & J7 \\\\ \cline{2-11} 
8& A8 & B8 & C8 & D8 & E8 & F8 & G8 & H8 & I8 & J8 \\\\ \cline{2-11} 
9& A9 & B9 & C9 & D9 & E9 & F9 & G9 & H9 & I9 & J9 \\\\ \cline{2-11}
\end{tabular}}{\scriptsize
\\begin{multicols}{3}
\\begin{enumerate}"""



 
_list = get_all_pixels()

print(_list)

for pixel in _list:
    if pixel in solution_cat:
        content = content.replace(pixel, "\ifthenelse{\\theAntworten=1}{\cellcolor{black}}{}")
    else:
        content = content.replace(pixel, "") 



selection = random.sample(_list, 14)

for pixel in selection:
    content += "\item[\\fbox{{\parbox{{15pt}}{{\centering {}}}}}] 4716,45445\n".format(pixel)


content += """
\end{enumerate}
\end{multicols}}"""
# for coordinate in solution_cat:
#     content = content.replace(coordinate, "\cellcolor{black}")


# print(content)
# x= get_random_number(235,235,0)
# y= get_random_number(123,123, 0)

# integer = change_to_integer(x)

# _list = split_into_digits(change_to_integer(y))

# result = []
# for digit in _list:
#     result.append(int(x*digit))

# factor_digit_length = get_number_of_digits(x)


# def create_single_line_multiplication(digit, i, is_integer):
#     subresult = int(change_to_integer(x)*digit)
#     print(digit)
#     print(get_number_of_digits(subresult))
#     print(factor_digit_length)
#     if get_number_of_digits(subresult) > factor_digit_length:
#         dif = get_number_of_digits(subresult)-factor_digit_length
#         if i == 0:
#             hspace = dif*'\hspace{-0.5em}'
#         elif dif > i:
#             hspace = (dif-i)*'\hspace{-0.5em}'
#         else:
#             hspace = (i-dif)*'\enspace'
#     else:
#         print('smaller')
#         print(i)
#         dif = factor_digit_length-get_number_of_digits(subresult)  
#         hspace = (i+dif)*'\enspace'
#         # hspace = i*'\enspace'

#     if is_integer==False:
#         hspace += "\,"
#     string = '\\antwortzeile {0} {1} \\\\\n'.format(hspace, str(subresult))
#     return string


# for all in range(2):
#     x= get_random_number(10,99,2)
#     y= get_random_number(10,99,1)

    # integer = change_to_integer(x)

#     _list = split_into_digits(change_to_integer(y))

#     result = []
#     for digit in _list:
#         result.append(int(x*digit))

#     factor_digit_length = get_number_of_digits(x)

#     content += """
# \item$\\begin{{array}}{{l}}
# {0} \cdot {1} \\\\ \hline
# """.format(str(x).replace('.',','),str(y).replace('.',','))
    
#     if isinstance(x,int):
#         is_integer = True
#     else:
#         is_integer = False
#     for i, digit in enumerate(_list):
#         content += create_single_line_multiplication(digit, i, is_integer=is_integer)

#     result = x*y
#     if get_number_of_digits(result) > factor_digit_length:
#         dif = get_number_of_digits(result)-factor_digit_length
#         if i == 0:
#             hspace = dif*'\hspace{-0.5em}'
#         elif dif > i:
#             hspace = (dif-i)*'\hspace{-0.5em}'
#         else:
#             hspace = (i-dif)*'\enspace'
#     else:
#         dif = factor_digit_length-get_number_of_digits(result)  
#         hspace = (i+dif)*'\enspace'

#     # string = '\\antwortzeile {0} {1} \\\\\n'.format(hspace, result)
#     content += '\hline\n\\antwortzeile {0} {1}\\\\\n'.format(hspace, str(result).replace('.',','))
#     content += "\end{array}$\n\\antwort[\\vspace{2cm}]{}\n\n"

# print(content)
# titel = "Arbeitsblatt"
# nummerierung = "(i)"
# columns = 2

# content = """
# \section{{{0}}}

# \\begin{{multicols}}{{{1}}}
# \\begin{{enumerate}}[{2}]
# {3}
# \end{{enumerate}}
# \end{{multicols}}
# """.format(titel, columns, nummerierung, content)

# print(x)
# print(y)
# print(result)
# print(content)


########## CREATE LATEX CODE FROM CONTENT
# path_file = os.path.join(
#     path_localappdata_lama, "Teildokument", "worksheet.tex"
#     )

# with open(path_file, "w", encoding="utf8") as file:
#     file.write(tex_preamble(solution="solution_on"))

#     file.write(content)

#     file.write(tex_end)



# ################# CREATE PDF FILE
# name = 'worksheet'
# head, tail = os.path.split(name)
# file_name = tail
# folder_name = "{0}/Teildokument".format(path_programm)


# drive = ""

# terminal_command = 'cd "{1}" & latex -interaction=nonstopmode --synctex=-1 "{2}.tex" & latex -interaction=nonstopmode --synctex=-1 "{2}.tex" & dvips "{2}.dvi" & ps2pdf -dNOSAFER -dALLOWPSTRANSPARENCY "{2}.ps"'.format(
#     drive, folder_name, file_name
# )


# process = subprocess.Popen(
#     terminal_command,
#     cwd=os.path.splitdrive(path_programm)[0],
#     shell=True,
# )

# process.wait()


# open_pdf_file(folder_name, file_name)