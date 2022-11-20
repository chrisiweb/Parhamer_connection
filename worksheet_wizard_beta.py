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
    return eval(string.replace('[','(').replace(']',')').replace('\xb7','*').replace(':','/'))


def get_random_fraction(min, max):
    nominator = get_random_number(min, max-1)
    denominator = get_random_number(nominator+1, max)
    print(f"nominator {nominator}")
    print(f"denominator: {denominator}")

    return Fraction("{0}/{1}".format(nominator, denominator))


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




A, B = symbols("{} {}".format("A", "B"))

# e = (3*a-1/2*b)**2
coef_a = [0,1]
coef_b = [11,11]
exp
fractions_allowed = False
exponent = 2
binomials_types = [True, True, True]

A, B = symbols("{} {}".format("A", "B"))

if fractions_allowed == True:
    coef_1 = get_random_fraction(coef_a[0],coef_a[1])
    coef_2 = get_random_fraction(coef_b[0],coef_b[1])
else:
    coef_1 = get_random_number(coef_a[0],coef_a[1])
    coef_2 = get_random_number(coef_b[0],coef_b[1])


binome = []

for i, all in enumerate(binomials_types):
    possible_binoms = [f'({coef_1}*A**{exp_x}+{coef_2}*B**{exp_y})**{exponent}', f'({coef_1}*A**{exp_x}-{coef_2}*B**{exp_y})**{exponent}', f'({coef_1}*A**{exp_x}+{coef_2}*B**{exp_y})*({coef_1}*A**{exp_x}-{coef_2}*B**{exp_y})']
    if all == True:
        binome.append(possible_binoms[i])

# binome = ['({0}*A+{1}*B)**{2}'.format(coef_1,coef_2,exponent), '({0}*A-{1}*B)**{2}'.format(coef_1,coef_2,exponent), '({0}*A+{1}*B)*({0}*A-{1}*B)'.format(coef_1,coef_2)]




random_choice = random.choice(binome)
print(f"choice: {random_choice}")
binom = eval(random_choice)

print(f"binom: {binom}")


# print(e)

solution = str(binom.expand())
binom = str(binom)

if fractions_allowed == True:
    solution = convert_to_fractions(solution)
    # binom = convert_to_fractions(binom)

print(f'solution: {solution}')
print(f"binom: {binom}")

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

choice = random.choice(alphabet)
variable_choices = [choice]

alphabet.remove(choice)
choice = random.choice(alphabet)
variable_choices.append(choice) 


solution_string = solution.replace("**", "^")
if fractions_allowed==True:
    replacement = "\xb7"
else:
    replacement = ""
solution_string = solution_string.replace("*", replacement)
solution_string = solution_string.replace("A", variable_choices[0])
solution_string = solution_string.replace("B", variable_choices[1])

binom_string = random_choice.replace("**", "^")
binom_string = binom_string.replace("*", replacement)
binom_string = binom_string.replace("A", variable_choices[0])
binom_string = binom_string.replace("B", variable_choices[1])


print(binom_string)

binom_string = re.sub('([^0-9])1([^0-9])', r"\1\2",binom_string)

print(binom_string)

    # for all in _temp:
    #     frac= Fraction(all).limit_denominator()

    #     if frac.denominator != 1:
    #         solution = solution.replace(all, "\\frac{{{0}}}{{{1}}}".format(frac.numerator, frac.denominator))
    #     else:
    #         solution = solution.replace(all, str(frac))

#####

# if fractions_allowed == True:
#     _temp = re.findall('[0-9.]+', solution)


#     for all in _temp:
#         frac= Fraction(all).limit_denominator()

#         if frac.denominator != 1:
#             solution = solution.replace(all, "\\frac{{{0}}}{{{1}}}".format(frac.numerator, frac.denominator))
#         else:
#             solution = solution.replace(all, str(frac))
