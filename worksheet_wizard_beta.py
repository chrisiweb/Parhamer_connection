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



def get_all_pixels(content):
    return re.findall("[A-J][0-9]",content)   


def get_quotient_with_rest(dividend,divisor):
    return "{} R{}".format(dividend//divisor, dividend%divisor) 
# for coordinate in solution_cat:
#     content = content.replace(coordinate, "\cellcolor{black}")


commas=2
minimum=100
maximum = 1000
negative_solutions_allowed=False
anzahl_subtrahenden=2
smaller_or_equal=1

subtrahenden = []
set_commas=commas
temp_maximum = maximum

# dif = maximum-minimum
# step = dif/(anzahl_subtrahenden+2)
# print(dif)
# print(step)
# if negative_solutions_allowed == False:
#     temp_minimum
# if negative_solutions_allowed == False:
#     temp_maximum = minimum+step

if smaller_or_equal == 1:
    commas = random.randint(0,set_commas)

subtrahenden_maximum = maximum/anzahl_subtrahenden
print(subtrahenden_maximum)
for i in range(anzahl_subtrahenden):
    num = get_random_number(minimum, subtrahenden_maximum, commas)
    subtrahenden.append(num)

# print(subtrahenden)  
print(sum(subtrahenden))  


minuend = get_random_number(math.ceil(sum(subtrahenden)), maximum, commas)
subtrahenden.insert(0, minuend)
# for i in range(anzahl_subtrahenden):
#     x= minuend - sum(subtrahenden)
#     print("zwischen {} und {}".format(minimum, x))
#     num = get_random_number(minimum,x, commas)
#     subtrahenden.append(num)
#     print(num)


# subtrahenden.insert(0, minuend)
    # temp_min = maximum-step*(i+1)
    # if negative_solutions_allowed == False:
    #     if i!=0:
    #         temp_maximum = minimum+(num-minimum)/anzahl_subtrahenden
    #         print(temp_maximum)
    # print("zwischen {} und {}".format(minimum, temp_maximum))
    # # print(temp_maximum)
    # if smaller_or_equal == 1:
    #     commas = random.randint(0,set_commas)
    # if i == 0:
    #     num = get_random_number(minimum,maximum, commas)
    # else:
    #     num = get_random_number(minimum,temp_maximum, commas)
    # subtrahenden.append(num)
    # print(num)
    #     if i==0:
    #         temp_maximum = num
    #     else:
    #         temp_maximum -= num
        # print(temp_maximum)
        # print(True)
    #     temp_maximum = temp_maximum-num
    # print(temp_maximum)
    


solution = reduce(lambda x,y: x-y, subtrahenden)

# print(subtrahenden)
string = str(subtrahenden[0]).replace(".",",")
# reduced_list = subtrahenden.pop(0)
# print(subtrahenden)
# random.shuffle(reduced_list)
print(subtrahenden)
for x in subtrahenden[1:]:
    string += " - {}".format(str(x).replace(".",","))

string += " = {}".format(str(solution).replace(".",","))
print(string)

# comma = 1
# # print(content)
# divisor = get_random_number(10,50,comma)
# min = 1000
# max = 10000
# # print(result_min)
# # print(result_max)
# result_min = math.ceil(min/divisor)
# result_max = math.floor(max/divisor)
# # print(result_min)
# # print(result_max)


# result = get_random_number(result_min,result_max, comma)


# print(divisor)
# print(result)

# dividend = result*divisor

# print("{} : {} = {}".format(dividend, divisor, result))

# print(8.395//0.1)
# print(83.95//1)

# result = get_quotient_with_rest(36,6)
# print(result)

# print(max/divisor)
# print(divisor)
# print(result)
# dividend = divisor*result

# print(dividend)


# print(23*22)
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