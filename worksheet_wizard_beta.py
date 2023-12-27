import random
import decimal
import re
from config import is_empty


from sympy import symbols, init_printing, expand, simplify, apart, Rational
# from sympy import *
from fractions import Fraction


list_of_topics_wizard = ['Addition', 'Subtraktion']

D = decimal.Decimal

def get_random_number(min, max, decimal=0, zero_allowed=False, force_decimals=False, half_allowed = False): #
    if not isinstance(zero_allowed, bool):
        zero_allowed = random_switch(zero_allowed)

    if zero_allowed == False:
        x = 0
        while x == 0:
            x = round(random.uniform(min,max),decimal)
    else:
        x = round(random.uniform(min,max),decimal)

    x = D(f'{x}')

    x = D("{:.{prec}f}".format(x, prec=decimal))

    if force_decimals==True:
        normalized_result = x.normalize()
        if get_number_of_decimals(normalized_result) != decimal:
            integer = random.randint(1,9)
            x = str(x)[:-1] + str(integer)
        
        ## not sure  
        # rand_int = random.randint(0,2)
        # new_decimal = decimal - rand_int
        # test_value = round(x-int(x),new_decimal)
        # last_integer = str(test_value)[-1]

        # if last_integer == "0":
        #     integer = random.randint(1,9)
        #     _str = str(test_value)
        #     _str = _str[:-1] + str(integer)
        #     x = _str
        

    x = D(f'{x}')

    x = D("{:.{prec}f}".format(x, prec=decimal))

    x = x.normalize()
 
    x = remove_exponent(x)

    if decimal == 0:
        if half_allowed == True:
            switch = random_switch()
            if switch == True:
                num = D(f"{str(x)}.5")
                return num
            else:
                return int(x)   
        else:
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


list_stellenwerte = ['ht', 'zt','t','h','z','E', 'Z', 'H', 'T', 'ZT', 'HT', 'M', 'ZM', 'HM', 'Md', 'ZMd', 'HMd', 'B', 'ZB', 'HB']
index_E = 5

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
    number = number.split(".")
    print(number)
    result = ""
    for i in range(len(number[0])):
        if (len(number[0]) - i) % 3 == 0 and i != 0:
            result += "*"
        result += number[0][i]
    print(f"length: {len(number)}")
    if len(number)>1:
        result = f"{result}.{number[1]}"
    return result

def simplify_numbers(number, num_stellenwerte):
    str_num = [*str(number)]
    number_of_zeros = str_num.count("0")
    erwartungswert = 4.5-number_of_zeros #4.5-1 if first number must exist


    if erwartungswert<0:
        return number
    
    probability = erwartungswert/num_stellenwerte
    str_new_number = []
    for i, all in enumerate(str_num):
        # print(random_switch(probability))
        if all != '0' and i!=0 and all!='.' and i!=len(str_num)-1:
            if random_switch(probability*100)==False:
                str_new_number.append('0')
            else:
                str_new_number.append(all)
        else:
            str_new_number.append(all)

    # print(str_new_number)
    if "." in str_new_number:
        number = float("".join(str_new_number))
    else:
        number = int("".join(str_new_number))
    return number

def index_to_letter(index):
    return chr(ord('a') + index)


def primfaktorzerlegung(n):
    faktoren = []
    teiler = 2

    while teiler <= n:
        if n % teiler == 0:
            faktoren.append(teiler)
            n = n // teiler
        else:
            teiler += 1

    return faktoren


minimum = 500
step = 10
subticks = 2
maximum = 1000

def get_list_of_primenumbers(maximum):
    primes = []
    is_prime = [True] * (maximum + 1)
    is_prime[0] = is_prime[1] = False

    for number in range(2, int(maximum**0.5) + 1):
        if is_prime[number]:
            primes.append(number)
            for multiple in range(number * number, maximum + 1, number):
                is_prime[multiple] = False

    for number in range(int(maximum**0.5) + 1, maximum + 1):
        if is_prime[number]:
            primes.append(number)

    return primes

def create_number_from_primes(list_of_primenumbers, minimum, maximum):
    product = 1
    list_of_products = []
    while True:
        x = random.choice(list_of_primenumbers)
        temp_product = product * x
        if temp_product > maximum:
            if product > minimum:
                list_of_products.sort()
                return product, list_of_products
            else:
                continue
        else: 
            product = temp_product
            list_of_products.append(x)

        if product > minimum:
            list_of_products.sort()
            return product, list_of_products

def convert_to_powers(list_of_factors):
    dict_of_occurences = {}
    for all in list_of_factors:
        dict_of_occurences[all]=list_of_factors.count(all)

    list_of_factors_powers = []
    for all in dict_of_occurences.keys():
        if dict_of_occurences[all]>1:
            list_of_factors_powers.append(f"{all}^{dict_of_occurences[all]}")
        else:
            list_of_factors_powers.append(str(all))

    return list_of_factors_powers

list_of_primenumbers = get_list_of_primenumbers(13)

product, list_of_factors = create_number_from_primes(list_of_primenumbers,minimum,maximum)

# print(product)
# print(list_of_factors)
# list_of_factors_powers = convert_to_powers(list_of_factors)

# print(list_of_factors_powers)


def expand_powers(powers):
    result = []
    for all in powers:
        x = all.split("^")
        if len(x)==1:
            result.append(x[0])
        else:
            result.extend(x[0] for i in range(int(x[1])))
    return result

print(expand_powers(['2^2', '5^3', '7^5']))
# factor= subticks/step

# starting_value = 0
# steps = 0.1
# maximum = round(starting_value+14*steps,2)
# print(maximum)
# print(maximum)


# print(primfaktorzerlegung(46456314))
# for i in range(20):
#     x = round(random.uniform(minimum, maximum) * factor) / factor
#     x= remove_exponent(D(x))
#     # x = random.randrange(minimum, maximum, step/subticks)
#     print(x)
#     x = get_random_number(minimum, maximum)

#     print(x)


#     x = add_defined_decimal(x, step, subticks)

#     print(x)

# dict_of_points = {}
# for i in range(5):
#     x = get_random_number(minimum, 5, half_allowed=True)
#     y = get_random_number(minimum, 5, half_allowed=True)
#     dict_of_points[index_to_letter(i).upper()]=[x,y]

# print(dict_of_points)

# _list =list(dict_of_points.values())

# print(_list)

# _string = ""
# for all in dict_of_points:
#     if _string != "":
#         _string += ", "
#     _string += f"{all} = ({dict_of_points[all][0]}|{dict_of_points[all][1]})"

# print(_string)