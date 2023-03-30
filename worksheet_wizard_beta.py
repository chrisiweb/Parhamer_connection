import random
import decimal
import re
from config import is_empty


from sympy import symbols, init_printing, expand, simplify, apart, Rational
# from sympy import *
from fractions import Fraction


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
    # possible_blanks = {
    #     1: [[[0],[1,2]], [[0],[0,2]],[[1],[0,1]],[[1],[0,2]]],
    #     2: [[[0,2],[1]], [[1,3],[0]]]}
    if len(_list)==5:
        possible_blanks = [
            [0,3,4],
            [0,2,4],
            [1,2,3],
            [1,2,4],
        ]
    elif len(_list)==6:
        possible_blanks = [
            [0,2,5],
            [1,3,4],
        ]      

    return random.choice(possible_blanks)


def split_binomial_expression(expression):
    pattern = r'([0-9/a-z]+\^\d+|\d*(?:/\d)*[a-z]+|^\^\d+(?:/\d)*[a-z]*)'
    return re.findall(pattern, expression)

def choose_random_blanks(_list):
    if len(_list)==5:
        possible_blanks = [
            [0,3,4],
            [0,2,4],
            [1,2,3],
            [1,2,4],
        ]
    elif len(_list)==6:
        possible_blanks = [
            [0,2,5],
            [1,3,4],
        ]      

    return random.choice(possible_blanks)


def number_to_placevalue(number):
    list_digits = []
    list_decimals = []
    decimals=False
    for all in str(number):
        if all == ".":
            decimals = True
        elif decimals == False:
            list_digits.append(all)
        elif decimals == True:
            list_decimals.append(all)

    complete_string_list=[]
    for i, all in enumerate(reversed(list_digits)):
        if int(all) != 0:
            string = f"{all}{list_stellenwerte[index_E+i]}"
            complete_string_list.insert(0, string)


    if list_decimals != []:
        for i, all in enumerate(list_decimals):
            if int(all) != 0:
                string = f"{all}{list_stellenwerte[index_E-(i+1)]}"
                complete_string_list.append(string)
    
    return complete_string_list


def insert_dots(number):
    number = str(number)
    result = ""
    for i in range(len(number)):
        if (len(number) - i) % 3 == 0 and i != 0:
            result += "*"
        result += number[i]
    return result

def simplify_numbers(number, num_stellenwerte):
    str_num = [*str(number)]
    number_of_zeros = str_num.count("0")
    erwartungswert = 4.5-number_of_zeros #4.5-1 if first number must exist


    if erwartungswert<0:
        return number
    
    probability = erwartungswert/num_stellenwerte
    print(probability)

    str_new_number = []
    for i, all in enumerate(str_num):
        # print(random_switch(probability))
        if all != '0' and i!=0:
            if random_switch(probability*100)==False:
                str_new_number.append('0')
            else:
                str_new_number.append(all)
        else:
            str_new_number.append(all)

    print(str_new_number)
    if "." in str_new_number:
        number = float("".join(str_new_number))
    else:
        number = int("".join(str_new_number))
    return number

list_stellenwerte = ['ht', 'zt','t','h','z','E', 'Z', 'H', 'T', 'ZT', 'HT', 'M', 'ZM', 'HM', 'Mrd', 'ZMrd', 'HMrd', 'B', 'ZB', 'HB']
index_E = 5


# x= get_random_number(100,999)

# print(x)

# _list = number_to_placevalue(x)

# print(_list)

# # print(complete_string_list)

# print("  ".join(_list))
# list_of_digits = [int(i) for i in str(x)]
# print(list_of_digits)

maximum = 8
minimum = 2
maximum = maximum+2

maximum_num = int('9'*maximum)
minimum_num = int('1'+'0'*(maximum-1))

# print(maximum_num)
# print(minimum_num)
# print(minimum)
number = get_random_number(minimum_num,maximum_num, minimum)

print(number)
number = simplify_numbers(number, maximum+minimum)
print(number)

_list_stellenwert = number_to_placevalue(number)

string_stellenwert = "  ".join(_list_stellenwert)

index = 0

print(string_stellenwert)


# x = '*'.join(reversed(str(number))[i:i+3] for i in range(0, len(str(number)), 3))
# print(x)
number = insert_dots(number)

if index == 0:
    _string = f"{number} = {string_stellenwert}".replace(".",",")
    _string = _string.replace("*",'.')
    # return [number, string_stellenwert, _string]
elif index == 2:
    _string = f"{string_stellenwert} = {number}".replace(".",",")
    _string = _string.replace("*",'.')

print(_string)


### ROMAN NUMBERS WORKING!!!
def int_to_roman(input):
    """ Convert an integer to a Roman numeral. """

    if not isinstance(input, type(1)):
        raise TypeError#, "expected integer, got %s" % type(input)
    if not 0 < input < 4000:
        raise ValueError #, "Argument must be between 1 and 3999"
    ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
    nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
    result = []
    for i in range(len(ints)):
        count = int(input / ints[i])
        result.append(nums[i] * count)
        input -= ints[i] * count
    return ''.join(result)

def roman_to_int(input):
    """ Convert a Roman numeral to an integer. """

    if not isinstance(input, type("")):
        raise TypeError#, "expected string, got %s" % type(input)
    input = input.upper(  )
    nums = {'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'V':5, 'I':1}
    sum = 0
    for i in range(len(input)):
        try:
            value = nums[input[i]]
            # If the next place holds a larger number, this value is negative
            if i+1 < len(input) and nums[input[i+1]] > value:
                sum -= value
            else: sum += value
        except KeyError:
            raise ValueError#, 'input is not a valid Roman numeral: %s' % input
    # easiest test for validity...
    if int_to_roman(sum) == input:
        return sum
    else:
        raise ValueError#, 'input is not a valid Roman numeral: %s' % input
    

# print(f'2029 = {int_to_roman(2029)}')

# print(f"XLII = {roman_to_int('XLII')}")