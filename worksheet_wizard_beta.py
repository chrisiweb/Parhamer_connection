from __future__ import division
from distutils.log import fatal
from pickletools import read_uint1
import random
from functools import reduce
import math
import decimal
import re

# import os

# from numpy import empty
# from config_start import path_localappdata_lama, path_programm
# import subprocess
# from tex_minimal import tex_preamble, tex_end
# from create_pdf import  open_pdf_file


list_of_topics_wizard = ['Addition', 'Subtraktion']

D = decimal.Decimal

def get_random_number(min, max, decimal=0, zero_allowed=False):
    if zero_allowed == False:
        x = 0
        while x == 0:
            x = round(random.uniform(min,max),decimal)
    else:
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



def get_all_pixels(content):
    return re.findall("[A-J][0-9]",content)   


def get_quotient_with_rest(dividend,divisor):
    return "{} R{}".format(dividend//divisor, dividend%divisor) 
# for coordinate in solution_cat:
#     content = content.replace(coordinate, "\cellcolor{black}")


commas=0
minimum=-10
maximum = 10
anzahl_summanden=4
smaller_or_equal=0
brackets_allowed = False


summanden = []
set_commas=commas
temp_maximum = maximum

def add_summand(s):
    if s>0:
        return "(+{})".format(s)
    else:
        return "({})".format(s)

def random_switch(p=50):
    return random.randrange(100) < p

def create_division_pair(factor_1, factor_2):

    dividend = factor_1*factor_2

    return "[{}:{}]".format(add_summand(dividend), add_summand(factor_1))



# create_division_pair(minimum, maximum, commas)

factors = []
set_commas=commas
for _ in range(anzahl_summanden):
    if smaller_or_equal == 1:
        commas = random.randint(0,set_commas) 

    num = get_random_number(minimum, maximum, commas)
    factors.append(num)


string  = add_summand(factors[0])

operators = ['\xb7', ':']
division_pair = None

for i, all in enumerate(factors[1:]):
    if division_pair != None:
        string += create_division_pair(division_pair, all)
        division_pair = None
        continue
    operation = random.choice(operators)
    if operation == ':':
        if i < len(factors[1:])-1:
            string += '\xb7'
            division_pair = all
        else:
            string += '\xb7' + add_summand(all)            
    else:
        string += operation

        string += add_summand(all)

print(string)

solution = eval(string.replace('[','(').replace(']',')').replace('\xb7','*').replace(':','/'))
solution = D("{:.{prec}f}".format(solution, prec=set_commas))

print(string)
string = "{0} = {1}".format(string.replace(".",","), str(solution).replace(".",","))

print(string)

#######################################################
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