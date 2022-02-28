# from __future__ import division
# from distutils.log import fatal
# from pickletools import read_uint1
from functools import partial
from posixpath import split
import random
# from functools import reduce
# import math
import decimal
import re


# from sympy import symbols, init_printing, expand
# import numpy
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
minimum= 0
maximum = 20
anzahl_summanden=10
smaller_or_equal=0
brackets_allowed = True


summanden = []
set_commas=commas
temp_maximum = maximum

def add_summand(s, show_brackets=True):
    if s==0 or show_brackets == False:
        return "{}".format(s)
    elif s>0:
        return "(+{})".format(s)
    else:
        return "({})".format(s)

def random_choice_except(_list, exception):
    return random.choice([x for x in _list if x != exception])

def random_switch(p=50):
    return random.randrange(100) < p

def create_division_pair(factor_1, factor_2, show_brackets = True):
    dividend = factor_1*factor_2
    return "{}:{}".format(add_summand(dividend, show_brackets), add_summand(factor_1, show_brackets))


def get_solution(string):
    return eval(string.replace('[','(').replace(']',')').replace('\xb7','*').replace(':','/'))



# results = set()
# for start in range(len(s)):
#     string = s[start:]
#     _list = re.findall('\(.*?\)', string)
#     print(_list)
    # _list = [x.replace('(','',1) for x in _list]

    # _list = [re.sub('\)$', '',x) for x in _list]
    # for i, all in enumerate(_list):
    #     print(all)
    #     start = all.count('(')
    #     end = all.count('(')
    #     if start != end:
    #         all[i] = re.sub('\)$', '',all)
    #     print(start)
    #     print(end)
    # results.update(_list)

# print(_list)

# print(results)
        #     #stack push
        #     stack.append([])
        # elif char == ')':
        #     yield ''.join(stack.pop())
        # else:
        #     # stack peek
        #     stack[-1].append(char)


def replace_negative_solutions(string):
    # print(string)
    split_string = string.split('-')

    temp_split_string = ['-'+s for s in split_string[1:]]
    # print(temp_split_string)
    # print(split_string[0])

    split_string = [split_string[0]] + temp_split_string
    # print(split_string)
    
    str = '+'.join(split_string)
    split_string = str.split('+')

    temp_split_string = ['+'+s if s[0]!='-' else s for s in split_string[1:]]
    split_string = [split_string[0]] + temp_split_string  

    print(split_string)

    bracket_open = False
    new_split_string = []
    for i, all in enumerate(split_string[:]):
        if all.count('(')>all.count(')'):
            stack = [all]
            bracket_open = True
        elif all.count('(')<all.count(')'):
            stack.append(all)
            new_split_string.append(''.join(stack))
            bracket_open = False
        elif bracket_open == True:
            stack.append(all)
        else:
            new_split_string.append(all)


    split_string = new_split_string
    # print(split_string)

    total_string = ''
    for part in split_string:
        temp_string = total_string + part
        temp_solution = get_solution(temp_string)

        while temp_solution<0:
            temp_string = temp_string.replace("-", "+", 1)
            temp_solution = get_solution(temp_string)
        
        total_string = temp_string


    return total_string

def check_for_negative_solutions(string):
    print(string)

    inner_string_brackets = re.findall(r"\(([0-9+-:\xb7]+)\)", string)
    # print(inner_string_brackets)

    new_inner_string_brackets = [replace_negative_solutions(x) for x in inner_string_brackets]
    for i, item in enumerate(inner_string_brackets):
        if item in string:
            string = string.replace(item, new_inner_string_brackets[i])
    inner_string_brackets = new_inner_string_brackets
    # replace_negative_solutions(inner_string_brackets[0])


    inner_brackets_replacement = {}
    replaced_string = string
    for i, all in enumerate(inner_string_brackets):
        x = '('+all+')'
        inner_brackets_replacement['R{}'.format(i)] = x
        replaced_string = replaced_string.replace(x,'R{}'.format(i))

    outer_string_brackets = re.findall(r"\(([R0-9+-:\xb7]+)\)", replaced_string)

    for i, all in enumerate(outer_string_brackets[:]):
        temp_string = all
        for r in inner_brackets_replacement:
            if r in temp_string:
                temp_string = temp_string.replace(r, inner_brackets_replacement[r])

        outer_string_brackets[i] = temp_string
    

    new_outer_string_brackets = [replace_negative_solutions(x) for x in outer_string_brackets]
    for i, item in enumerate(outer_string_brackets):
        if item in string:
            string = string.replace(item, new_outer_string_brackets[i])
    outer_string_brackets = new_outer_string_brackets

    string = replace_negative_solutions(string)

    solution = get_solution(string)

    return string, solution

def prevent_double_multiplication(string):
    operations = ['+','-','\xb7',':']
    multiplication = False
    multiplication_brackets = False
    inside_brackets = False
    for i, all in enumerate(string[:]):
        # print(all)
        if all == '(':
            inside_brackets = True
        elif all == ')':
            inside_brackets = False

        if all in operations:
            if multiplication_brackets==True and all == '\xb7':
               string = string[0:i] + '-' + string[i+1:]
               multiplication_brackets=False
            elif multiplication == True and all == '\xb7':
                string = string[0:i] + '-' + string[i+1:]
                multiplication = False
                if inside_brackets == False:
                    multiplication_brackets=False 
            elif all == '\xb7':
                multiplication =True
                if inside_brackets == False:
                    multiplication_brackets=True   
            else:
                multiplication = False
            # elif inside_brackets==0:
            #     multiplication = False

    
    # split_string = [char for char in string] 
    # # temp_string = re.sub("\([0-9+-:]+\)", "B", string)
    # print(split_string)
    return string


def create_single_example_ganze_zahlen_grundrechnungsarten(minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed, show_brackets):
    numbers = []
    set_commas=commas
    for _ in range(anzahl_summanden):
        if smaller_or_equal == 1:
            commas = random.randint(0,set_commas) 

        num = get_random_number(minimum, maximum, commas, 25)
        numbers.append(num)

    string  = add_summand(numbers[0], show_brackets)

    operators = ['+', '-', '\xb7', ':']
    division_pair = None
    bracket_open = False
    waiter = False

    for i, all in enumerate(numbers[1:]):
        if division_pair == 'done':
            division_pair = None
        elif division_pair != None:
            if division_pair[0] == 0:
                division_pair[0] = get_random_number(minimum, maximum, commas)

            operation = random.choice(operators) # operation after the division

            if division_pair[1] != '\xb7' and operation != '\xb7':
                string += create_division_pair(division_pair[0], all, show_brackets)
            elif show_brackets == False:
                string += "(" + create_division_pair(division_pair[0], all, show_brackets) + ")"
            else:
                string += "[" + create_division_pair(division_pair[0], all, show_brackets) + "]"

                
            division_pair = 'done'
            continue
        else:
            operation = random.choice(operators)

        if operation == ':':
            waiter = False
            rsp = random_switch()
            if i==0 and rsp == True:
                division_pair = [numbers[0], None]
                if division_pair[0] == 0:
                    division_pair[0] = get_random_number(minimum, maximum, commas)
                operation = random.choice(operators)
                if len(numbers)==2:
                    string = create_division_pair(division_pair[0], all, show_brackets)
                elif show_brackets == False:
                    string = "(" + create_division_pair(division_pair[0], all, show_brackets) + ")"
                else: 
                    string = "[" + create_division_pair(division_pair[0], all, show_brackets) + "]"
                
                division_pair = 'done'
                continue
            else:
                if i < len(numbers[1:])-1:
                    operation = random.choice([x for x in operators if x!=':'])
                    string += operation
                    division_pair = [all, operation]
                elif len(numbers)==2:
                    string = create_division_pair(numbers[0], all, show_brackets) 
                else:
                    operation = random.choice([x for x in operators if x!=':'])
                    string += operation + add_summand(all, show_brackets)            
        else:
            if brackets_allowed == True and random_switch(70) == True and waiter==False:
                if bracket_open == False:
                    string +=random.choice(operation)
                    if show_brackets == False:
                        string += '('
                    else:
                        string += '['
                    bracket_open = True
                    waiter = True
                elif bracket_open == True:
                    if show_brackets == False:
                        string += ')'
                    else:
                        string += ']'
                    string += random.choice(operation) 
                    bracket_open = False
                    waiter = False  
            else:
                string += random.choice(operation)
                waiter = False           

            string += add_summand(all, show_brackets)

    if bracket_open == True:
        if waiter == True:
            if show_brackets == True:
                index = string.rfind('[')
            elif show_brackets == False:
                index = string.rfind('(')
            string = string[:index] + string[index+1:]
        elif show_brackets == True:
            string +=']'
        elif show_brackets == False:
            string +=')'

    string = prevent_double_multiplication(string)

    solution = eval(string.replace('[','(').replace(']',')').replace('\xb7','*').replace(':','/'))

    if show_brackets== False: ## check if result ist negative, when natural numbers are chosen         
        string, solution = check_for_negative_solutions(string)
        # while solution < 0:
        #     string = string.replace("-", "+", 1)
        #     solution = eval(string.replace('[','(').replace(']',')').replace('\xb7','*').replace(':','/'))
            


    solution = D("{:.{prec}f}".format(solution, prec=set_commas))

  

    if solution == 0:
        solution = 0
    string = "{0} = {1}".format(string.replace(".",","), str(solution).replace(".",","))

    return [numbers, solution, string] 

rsp = create_single_example_ganze_zahlen_grundrechnungsarten(minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed, show_brackets=False)
print(rsp)


s = '(80:20)\xb7(15-7)\xb715\xb766:6\xb7(10\xb7(60\xb720)\xb73)'
# # # print(s)

# result, solution = check_for_negative_solutions(s)

result = prevent_double_multiplication(s)
print(result)


## binomische Formel
# init_printing()
# a, b = symbols("a b")

# e = (3*a+1/2*b)**2

# print(e)

# print(e.expand())
# sympy.Eq((x^2+x-5, 15))


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