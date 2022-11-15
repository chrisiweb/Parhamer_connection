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


from sympy import symbols, init_printing, expand
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
# init_printing()
variable_1 = "a"
variable_2 = "b"
a, b = symbols("{} {}".format(variable_1, variable_2))

e = (3*a-1/2*b)**2

coef_1 = get_random_number(1,10)
coef_2 = get_random_number(1,10)
# coef_1 = get_random_fraction(1,10)
# coef_2 = get_random_fraction(1,10)
print(coef_1)
print(coef_2)

exponent = 5
binome = ['({0}*a+{1}*b)**{2}'.format(coef_1,coef_2,exponent), '({0}*a-{1}*b)**{2}'.format(coef_1,coef_2,exponent), '({0}*a+{1}*b)*({0}*a-{1}*b)'.format(coef_1,coef_2)]


random_choice = random.choice(binome)
print(f"choice: {random_choice}")
binom = eval(random_choice)

print(f"binom: {binom}")
fraction = get_random_fraction(1,10)

# print(e)

calculated = str(binom.expand())
print(binom.expand())
x = re.findall('[0-9.]+', calculated)
print(x)



for i, all in enumerate(x):
    frac= Fraction(all)

    if frac.denominator != 1:
        calculated = calculated.replace(all, "\\frac{{{0}}}{{{1}}}".format(frac.numerator, frac.denominator))
    else:
        calculated = calculated.replace(all, str(frac))

calculated = calculated.replace("**", "^")
calculated = calculated.replace("*", "")
print(calculated)



