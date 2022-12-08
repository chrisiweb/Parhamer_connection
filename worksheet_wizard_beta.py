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
from config import is_empty


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

def remove_exponent(d):
    return d.quantize(D(1)) if d == d.to_integral() else d.normalize()

def get_number_of_decimals(x):
    num = D('{}'.format(x)).normalize()
    num = remove_exponent(num)
    num = abs(num.as_tuple().exponent)
    return num

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


def extract_parts_of_binom(string):
    _list = string.split("=")
    split_list = []
    for string in _list:
        x= re.split('\(|\)|\+|-|=', string)
        x = [item.strip() for item in x]
        
        for all in x[:]:
            if re.fullmatch(' *\^[0-9] *', all) != None:
                x.remove(all)
            elif is_empty(all):
                x.remove(all) 
        
        split_list.append(x)
    return split_list   

def choose_random_blanks(_list):
    possible_blanks = {1: [[[0],[1,2]], [[0],[0,2]],[[1],[0,1]],[[1],[0,2]]], 2: [[[0,2],[1]], [[1,3],[0]]]}

    if len(_list[0])==2:
        typ_index = 1
    elif len(_list[0])==4:
        typ_index = 2

    return random.choice(possible_blanks[typ_index])

a = '(6f+9u)^2 = 36f^2 + 108fu + 81u^2'
b = '(7y+7e)(7y-7e) = 49y^2 - 49e^2'


binom_parts = re.search("\((.+)[\+-](.+)\)", a)
print(binom_parts.group(1))
print(binom_parts.group(2))

binom_parts = re.search("\((.+)[\+-](.+)\)", b)
print(binom_parts.group(0))
print(binom_parts.group(1))
print(binom_parts.group(2))



# split_list = extract_parts_of_binom(a)
# print(split_list)
# chosen_blanks = choose_random_blanks(split_list)
# print(chosen_blanks)

# for i, all in enumerate(chosen_blanks):
#     for index in all:
#         print(split_list[i][index])
#         a = a.replace(split_list[i][index], "\\rule{1cm}{0.3pt}")

# print(a)

# split_list = extract_parts_of_binom(b)
# print(split_list)
# chosen_blanks = choose_random_blanks(split_list)

# print(chosen_blanks)




# extracted_string = extract_parts_of_binom(a)

# print(extracted_string)
# print(extract_parts_of_binom(b))

# for all in x:
#     print(all)
#     print(re.fullmatch(' *\^[0-9] *', all))

# y= re.split('\(|\)|\+|-|=', b)
# print(y)


#####
# alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# choices = random.choices(alphabet, k=2)

# solution_string = solution.replace("**", "^")
# solution_string = solution_string.replace("*", "")
# solution_string = solution_string.replace("a", choices[0])
# solution_string = solution_string.replace("b", choices[1])

# binom_string = random_choice.replace("**", "^")
# binom_string = binom_string.replace("*", "")
# binom_string = binom_string.replace("a", choices[0])
# binom_string = binom_string.replace("b", choices[1])



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