# from __future__ import division
# from distutils.log import fatal
# from pickletools import read_uint1
from functools import partial
from operator import imod
from posixpath import split
import random
# from functools import reduce
# import math
import decimal
import re


from sympy import symbols, init_printing, expand, simplify, apart, Rational
# from sympy import *
from fractions import Fraction
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
    value = eval(string.replace('[','(').replace(']',')').replace('\xb7','*').replace(':','/'))
    value = round(value, 10)
    return value


def get_random_fraction(min, max):
    if min == 0 and max == 1:
        numerator = 1
        denominator = 2
    else:
        numerator = get_random_number(min, max-1)
        denominator = get_random_number(numerator+1, max)

    return Fraction("{0}/{1}".format(numerator, denominator))


## binomische Formel
# v_1 = "a"
# v_2 = "b"
# a, b = symbols("{} {}".format(v_1, v_2))
# C, D = symbols("{} {}".format("C","D"))
# # e = (3*a-1/2*b)**2
# coef_a = [0,3]
# coef_b = [0,3]
# fractions_allowed = True
# exponent = 3

# # if fractions_allowed == True:
# #     coef_1 = get_random_fraction(coef_a[0],coef_a[1])
# #     coef_2 = get_random_fraction(coef_b[0],coef_b[1])
# # else:
# #     coef_1 = get_random_number(coef_a[0],coef_a[1])
# #     coef_2 = get_random_number(coef_b[0],coef_b[1])


# coef_1 = Rational(1,4)
# coef_2 = Rational(1,3)
# print(coef_1)
# print(coef_2)
# # coef_1 = get_random_fraction(1,10)
# # coef_2 = get_random_fraction(1,10)

# print(f'square {coef_1**2}')
# print(f'square {coef_2**2}')
# # if coef_a!=False:
# #     num = get_random_number(coef_a[0],coef_a[1])
# #     if num == 1:
# #         first_string = ""
# #     else:
# #         first_string = f"{num}"
# # else: 
# #     first_string = ""

# # if exp_x!= False and first_string != "":
# #     first_string += f"*{Symbol('A')}"
# # if exp_x!= False:
# #     exponent_x = get_random_number(exp_x[0],exp_x[1])
# #     if exponent_x !=1:
# #         x = f"{v_1}^^{exponent_x}"
# #     else:
# #         x = f"{v_1}"
# # else: 
# #     exponent_x = ""

# # if first_string == "":
# #     first_string = x
# # elif exponent_x != "":
# #     first_string += f"*{x}"


# binome = ['(C*a+D*b)**{0}'.format(exponent), '(C*a-D*b)**{0}'.format(exponent), '(C*a+D*b)*(C*a-D*b)']
# # binome = [f'({first_string}*v_1+{coef_2}*v_2)**{exponent}', '({0}*v_1-{1}*v_2)**{2}'.format(coef_1,coef_2,exponent), '({0}*v_1+{1}*v_2)*({0}*v_1-{1}*v_2)'.format(coef_1,coef_2)]




# random_choice = random.choice(binome)
# print(f"choice: {random_choice}")
# binom = eval(random_choice)

# print(f"binom: {binom}")


# # print(e)

# solution = str(binom.expand())

# print(solution)

# for i in range(2,exponent+1):

#     solution = solution.replace(f"C**{i}",f"{coef_1**i}")
#     solution = solution.replace(f"D**{i}",f"{coef_2**i}")
 
# solution = solution.replace("C",str(coef_1))
# solution = solution.replace("D",str(coef_2))


# print(solution)



# if fractions_allowed == True:
#     _temp = re.findall('[0-9.]+', solution)
#     print(_temp)


#     for all in _temp:
#         frac= Fraction(all)

#         if frac.denominator != 1:
#             solution = solution.replace(all, "\\frac{{{0}}}{{{1}}}".format(frac.numerator, frac.denominator))
#         else:
#             solution = solution.replace(all, str(frac))


# print(solution)
# #####
# # alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# # choices = random.choices(alphabet, k=2)

# # solution_string = solution.replace("**", "^")
# # solution_string = solution_string.replace("*", "")
# # solution_string = solution_string.replace("a", choices[0])
# # solution_string = solution_string.replace("b", choices[1])

# # binom_string = random_choice.replace("**", "^")
# # binom_string = binom_string.replace("*", "")
# # binom_string = binom_string.replace("a", choices[0])
# # binom_string = binom_string.replace("b", choices[1])

# ##### working 

def convert_to_fractions(string):
    _temp = re.findall('[0-9.]+', string)


    for all in _temp:
        frac= Fraction(all).limit_denominator()

        if frac.denominator != 1:
            string = string.replace(all, f"{frac.numerator}/{frac.denominator}")
        else:
            string = string.replace(all, str(frac))
    
    return string


def get_first_temp_division(dividend, temp_solution):
    end_index =1
    part_divide = str(dividend)[0:end_index]
    print(f"{temp_solution} vs. {eval(part_divide)}")
    while True:
        if temp_solution <= eval(part_divide):
            return part_divide, end_index-1
        
        end_index +=1
        part_divide = str(dividend)[0:end_index]

def get_temp_solution_division(dividend, divisor, solution):
    str_solution = [x for x in solution if x!="."]
    # str_divisor = [x for x in str(divisor) if x!="."]
    list_temp_solutions = []
    # start_index =0

    for i, all in enumerate(str_solution):
        temp_solution = eval(f"{all}*{divisor}")

        if i == 0:
            first_part_divide, end_index = get_first_temp_division(dividend, temp_solution)
            part_divide = first_part_divide
        differenz = eval(part_divide)-temp_solution
        end_index +=1
        try:
            next_digit = str(dividend)[end_index]            
        except IndexError:
            next_digit = ""


        part_divide = f"{differenz}{next_digit}"

        list_temp_solutions.append([f"{differenz}",next_digit])

    return first_part_divide, list_temp_solutions
example = [504,42]
# solution = str(get_solution(f"{example[0]} : {example[1]}"))
solution = "12"
print(example)



first_part_divide, list_temp_solutions = get_temp_solution_division(dividend=example[0], divisor=example[1], solution=solution)


print(first_part_divide)
print(list_temp_solutions)    
content = f"""
$\\begin{{array}}{{l}}
{str(example[0]).replace(".",",")} : {str(example[1]).replace(".",",")} = \\antwort[\\vspace{{1.5cm}}]{{{solution}}} \\\\
"""

previous_num_of_digits  = get_number_of_digits(first_part_divide)
# multiplier = 0
rest = ""
for i, all in enumerate(list_temp_solutions):
    num_of_digits = get_number_of_digits(int(all[0]))
    print(f"pervious_number : {previous_num_of_digits}")
    print(f"num_of_digits: {num_of_digits}")
    print(f"i: {i}")

    if i == 0:
        multiplier = previous_num_of_digits - num_of_digits
    # elif i == len(list_temp_solutions)-1:
    #     diff = previous_num_of_digits - num_of_digits
    #     multiplier += diff
    #     rest = "R"        
    else:
        multiplier += 1
        diff = previous_num_of_digits - num_of_digits
        multiplier += diff

    if i == len(list_temp_solutions)-1:
        rest = "R"
                
    hspace = multiplier*'\enspace'
    content += f"\\antwortzeile {hspace} {all[0]}{all[1]}{rest} \\\\ \n"
    previous_num_of_digits = num_of_digits 
    # print(content)
    print(f"multiplier: {multiplier}")
content += "\end{array}$\n\n"

print(content)

# print(f'end: {temp_solution} vs. {eval(part_divide)}')
#     i=0
#     while temp_solution>eval(part_divide):


##### FRACTION
# w = get_random_fraction(2,10)
# x = get_random_fraction(2,10)
# y= get_random_fraction(2,10)
# z= get_random_fraction(2,10)



# print(x)
# print(y)
# print(z)
# print(x-y)

# print(f"({x}-{y})*({z}+{w}) = {(x-y)*(z+w)}")