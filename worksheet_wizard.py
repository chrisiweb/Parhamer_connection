from functools import reduce

import random
from math import floor, ceil
from config import is_empty
# import os
# from config_start import path_localappdata_lama, path_programm
import decimal
import re
from sympy import symbols

from create_nonograms import nonogramm_empty, all_nonogramms, list_all_pixels
from fractions import Fraction
from handle_exceptions import report_exceptions
# import subprocess
# from tex_minimal import tex_preamble, tex_end
# from create_pdf import create_pdf, open_pdf_file, build_pdf_file

dict_widgets_wizard = {
    'Addition' : [
        'self.widget_ausrichtung_wizard',
        'self.widget_zahlenbereich_minimum',
        'self.widget_zahlenbereich_maximum',
        'self.widget_kommastellen_wizard',
        'self.widgetZahlenbereich_anzahl',
        ],
    'Subtraktion' : [
        'self.widget_ausrichtung_wizard',
        'self.widget_zahlenbereich_minimum',
        'self.widget_zahlenbereich_maximum',
        'self.widget_kommastellen_wizard',
        'self.checkbox_negative_ergebnisse_wizard',
        # 'self.label_negative_ergebnisse_wizard', 
        ],
    'Multiplikation' : [
        'self.groupBox_first_number_wizard',
        'self.groupBox_second_number_wizard',
        'self.comboBox_solution_type_wizard',
    ],
    'Division' : [
        'self.groupBox_dividend_wizard',
        'self.groupBox_divisor_wizard',
        'self.groupBox_ergebnis_wizard',
        'self.comboBox_solution_type_wizard',
    ],
    'Verbindung der Grundrechnungsarten': [
        'self.widget_zahlenbereich_minimum',
        'self.widget_zahlenbereich_maximum',
        'self.widget_kommastellen_wizard',
        'self.widgetZahlenbereich_anzahl',
        'self.checkbox_allow_brackets_wizard',        
    ],
    'Ganze Zahlen (Addition & Subtraktion)': [
        'self.widget_zahlenbereich_minimum',
        'self.widget_zahlenbereich_maximum',
        'self.widget_kommastellen_wizard',
        'self.widgetZahlenbereich_anzahl',
        'self.checkbox_allow_brackets_wizard',        
    ],
    'Ganze Zahlen (Multiplikation & Division)': [
        'self.widget_zahlenbereich_minimum',
        'self.widget_zahlenbereich_maximum',
        'self.widget_kommastellen_wizard',
        'self.widgetZahlenbereich_anzahl',
        # 'self.checkbox_allow_brackets_wizard',        
    ],
    'Ganze Zahlen (Grundrechnungsarten)': [
        'self.widget_zahlenbereich_minimum',
        'self.widget_zahlenbereich_maximum',
        'self.widget_kommastellen_wizard',
        'self.widgetZahlenbereich_anzahl',
        'self.checkbox_allow_brackets_wizard',        
    ],
    'Binomische Formeln': [
        'self.groupbox_binoms_types',
        'self.widget_binoms_set_variables_factors',
        'self.widget_binoms_set_variables_exponents',
        'self.label_binom_example',
        'self.widget_binom_further_settings',
    ],
}   

themen_worksheet_wizard = list(dict_widgets_wizard.keys())

D = decimal.Decimal

# def add_random_decimal(value):
#     integer = random.randint(1,9)
#     _str = str(value)
#     _str = _str[:-1] + str(integer)
#     print(_str)
#     return  

def get_random_number(min, max, decimal=0, zero_allowed=False, force_decimals=False): #
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
        rand_int = random.randint(0,2)
        new_decimal = decimal - rand_int
        test_value = round(x-int(x),new_decimal)
        last_integer = str(test_value)[-1]

        if last_integer == "0":
            integer = random.randint(1,9)
            _str = str(test_value)
            _str = _str[:-1] + str(integer)
            x = _str
        

    x = D(f'{x}')

    x = D("{:.{prec}f}".format(x, prec=decimal))

    x = x.normalize()
 
    x = remove_exponent(x)

    if decimal == 0:
        return int(x)
    else:
        return x


# def normalize_decimal(d): ### cut off all zeros after deciimals
#     normalized = d.normalize()
#     sign, digit, exponent = normalized.as_tuple()
#     return normalized if exponent <= 0 else normalized.quantize(1)

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





def create_single_example_addition(minimum, maximum, commas, anzahl_summanden, smaller_or_equal):
    summanden = []
    set_commas=commas
    for _ in range(anzahl_summanden):
        if smaller_or_equal == 1:
            commas = random.randint(0,set_commas) 
        x= get_random_number(minimum,maximum, commas)
        summanden.append(x)

    solution = sum(summanden)
    # x = get_random_number(minimum,maximum, commas)
    # y= get_random_number(minimum,maximum, commas)
    # solution = x+y
    string = str(summanden[0]).replace(".",",")
    for x in summanden[1:]:
        string += " + {}".format(str(x).replace(".",","))
    
    string += " = {}".format(str(solution).replace(".",","))

    return [summanden,solution, string]

def create_single_example_subtraction(minimum, maximum, commas, negative_solutions_allowed,anzahl_subtrahenden, smaller_or_equal):
    subtrahenden = []
    set_commas=commas

    if negative_solutions_allowed == False:
        subtrahenden_maximum = maximum/anzahl_subtrahenden
    else:
        subtrahenden_maximum = maximum

    for _ in range(anzahl_subtrahenden):
        if smaller_or_equal == 1:
            commas = random.randint(0,set_commas)
        num = get_random_number(minimum, subtrahenden_maximum, commas)
        subtrahenden.append(num) 

    if smaller_or_equal == 1:
        commas = random.randint(0,set_commas)
    if negative_solutions_allowed == False:   
        minuend = get_random_number(ceil(sum(subtrahenden)), maximum, commas)
    else:
        minuend = get_random_number(minimum, maximum, commas)

    subtrahenden.insert(0, minuend)
    
    solution = reduce(lambda x,y: x-y, subtrahenden)

    string = str(subtrahenden[0]).replace(".",",")


    for x in subtrahenden[1:]:
        string += " - {}".format(str(x).replace(".",","))
    
    string += " = {}".format(str(solution).replace(".",","))

    return [subtrahenden,solution, string]
    # if smaller_or_equal == 1:
    #     commas = random.randint(0,set_commas) 
    # y= get_random_number(minimum,maximum, commas)
    # if x-y<0 and negative_solutions_allowed== False:
    #     x, y = y, x
    # solution = x-y
    # string = "{0} - {1} = {2}".format(str(x).replace(".",","),str(y).replace(".",","),str(solution).replace(".",","))   
    # return [x,y,solution, string]

def create_single_example_multiplication(minimum_1, maximum_1, commas_1, smaller_or_equal_1 ,minimum_2, maximum_2, commas_2, smaller_or_equal_2):
    if smaller_or_equal_1 == 1:
        set_commas=commas_1
        commas_1 = random.randint(0,set_commas)
    if smaller_or_equal_2 == 1:
        set_commas=commas_2
        commas_2 = random.randint(0,set_commas)

    x = get_random_number(minimum_1, maximum_1, commas_1)
    y= get_random_number(minimum_2, maximum_2, commas_2)
    solution = x*y
    string = "{0} \xb7 {1} = {2}".format(str(x).replace(".",","),str(y).replace(".",","),str(solution).replace(".",","))
    return [x,y,solution, string]

def get_quotient_with_rest(dividend,divisor):
    
    return "{}\nR {}".format(int(dividend//divisor), dividend%divisor) 

def create_single_example_division(minimum_1, maximum_1, minimum_2, maximum_2, commas_div, smaller_or_equal_div, commas_result, smaller_or_equal_result, output_type):
    if smaller_or_equal_div == 1:
        set_commas_div=commas_div
        commas_div = random.randint(0,set_commas_div)
    
    divisor = get_random_number(minimum_2, maximum_2, commas_div)

    if output_type == 1:  
        dividend = get_random_number(minimum_1, maximum_1)
        result = str(get_quotient_with_rest(dividend, divisor))

    else:
        result_min = ceil(minimum_1/divisor)
        result_max = floor(maximum_1/divisor)

        if output_type == 0:
            commas_result = 0
        else:
            if smaller_or_equal_result == 1:
                set_commas_result=commas_result
                commas_result = random.randint(0,set_commas_result)
        result = get_random_number(result_min, result_max, commas_result, force_decimals=True)

        dividend = result*divisor
        dividend = D(f'{dividend}').normalize()
        dividend = remove_exponent(dividend)
        
        result = str(result)

    string = "{0} : {1} = {2}".format(str(dividend).replace(".",","),str(divisor).replace(".",","),result.replace(".",","))
    # print([dividend,divisor,result, string])
    return [dividend,divisor,result, string]

def add_summand(s, show_brackets=True):
    if s==0 or show_brackets == False:
        return "{}".format(s)
    elif s>0:
        return "(+{})".format(s)
    else:
        return "({})".format(s)

def random_switch(p=50):
    return random.randrange(100) < p

def random_choice_except(_list, exception):
    return random.choice([x for x in _list if x != exception])

def create_single_example_ganze_zahlen_strich(typ, minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed):
    summanden = []
    set_commas=commas
    for _ in range(anzahl_summanden):
        if smaller_or_equal == 1:
            commas = random.randint(0,set_commas) 
        num = 0
        while num == 0:
            num = get_random_number(minimum, maximum, commas)
        summanden.append(num)
    
    string  = add_summand(summanden[0])

    if typ == "+":
        operators =  ['+']
    elif typ == "-":
        operators =  ['-']
    elif typ == "+-":
        operators = ['+', '-']
        
    bracket_open = False
    waiter = False

    for all in summanden[1:]:
        if brackets_allowed == True and random_switch(70) == True and waiter==False:
            if bracket_open == False:
                string +=random.choice(operators) + '['
                bracket_open = True
                waiter = True
            elif bracket_open == True:
                string +=']' + random.choice(operators) 
                bracket_open = False
                waiter = False  
        else:
            string += random.choice(operators)
            waiter = False           

        string += add_summand(all)

    if bracket_open == True:
        if waiter == True:
            index = string.rfind('[')
            string = string[:index] + string[index+1:]

        else:
            string +=']'
        
    solution = eval(string.replace('[','(').replace(']',')'))
    solution = D("{:.{prec}f}".format(solution, prec=set_commas))

    string = "{0} = {1}".format(str(string).replace(".",","), str(solution).replace(".",","))

    return [summanden,solution, string]


def create_division_pair(factor_1, factor_2, show_brackets = True):
    dividend = factor_1*factor_2
    return "{}:{}".format(add_summand(dividend, show_brackets), add_summand(factor_1, show_brackets))

def calculate_solution(string, set_commas):
    exact_solution = eval(string.replace('[','(').replace(']',')').replace('\xb7','*').replace(':','/'))
    rounded_solution = round(exact_solution, 2)

    
    test_value = rounded_solution - exact_solution
    test_value = round(test_value, 10)

    if test_value != 0 :
        return False

    solution = D("{:.{prec}f}".format(exact_solution, prec=set_commas)).normalize()



    solution = remove_exponent(solution)

    return solution

def check_decimals(string, number, set_commas, factors):
        temp_solution = get_solution(string)

        if set_commas >= get_number_of_decimals(temp_solution):
            difference = int(set_commas) - int(get_number_of_decimals(temp_solution))
            new_number = round(number, difference)
            index = factors.index(number)
            factors[index] = new_number
        else:
            new_number= number
        
        new_number = D('{}'.format(new_number)).normalize()
        new_number = remove_exponent(new_number)
        return new_number, factors

def remove_exponent(d):
    return d.quantize(D(1)) if d == d.to_integral() else d.normalize()

def create_single_example_ganze_zahlen_punkt(minimum, maximum, commas, anzahl_summanden, smaller_or_equal):
    factors = []
    set_commas=commas


    test_commas = commas
    for i in range(anzahl_summanden):
        if smaller_or_equal == 1 and i+1 == anzahl_summanden:
            commas = test_commas
            force_decimals = True
        else:
            commas = random.randint(0,test_commas)
            force_decimals = False
            

        #######
        #     
        num = get_random_number(minimum, maximum, commas, zero_allowed=25, force_decimals=force_decimals)
        factors.append(num)
        
        if test_commas !=0:
            test_commas = test_commas - commas
        
        if test_commas <0:
            test_commas = 0
        



    string  = add_summand(factors[0])

    operators = ['\xb7', ':']
    division_pair = None

    for i, all in enumerate(factors[1:]):
        if division_pair != None:
            if division_pair == 0:
                division_pair = get_random_number(minimum, maximum, commas)    
            string += "[" + create_division_pair(division_pair, all) + "]"
            division_pair = None
            continue
        operation = random.choice(operators)
        if operation == ':':
            rsp = random_switch()
            if i==0 and rsp == True:
                division_pair = factors[0]
                if division_pair == 0:
                    division_pair = get_random_number(minimum, maximum, commas)
                
                string = create_division_pair(division_pair, all)
                if anzahl_summanden > 2:
                    string = "[" + string + "]"

                
                division_pair = None
                continue
            else:
                if i < len(factors[1:])-1:
                    string += '\xb7'
                    division_pair = all
                elif len(factors)==2:
                    string = create_division_pair(factors[0], all) 
                else:
                    new_number, factors = check_decimals(string, all, set_commas, factors)

                    string += '\xb7' + add_summand(new_number)
        else:
            new_number, factors = check_decimals(string, all, set_commas, factors)

            string += operation

            string += add_summand(new_number)


    solution = calculate_solution(string, set_commas)
    if solution == False:
        factors, solution, string = repair_decimals(factors, solution, string, set_commas, minimum, maximum)

    if smaller_or_equal == 0 and get_number_of_decimals(solution) < set_commas:
        if solution != 0:
            factors, solution, string = repair_decimals(factors, solution, string, set_commas, minimum, maximum)

    
    if solution == 0:
        solution = 0
    string = "{0} = {1}".format(string.replace(".",","), str(solution).replace(".",","))


    return [factors, solution, string]     

def repair_decimals(factors, solution, string, set_commas, minimum, maximum):
    split_string = string.split("\xb7")

    for all in reversed(split_string):
        if ":" not in all:
            number = D("{}".format(all.replace("(","").replace(")","").replace("+",""))).normalize()
            number = remove_exponent(number)

            i=0
            temp_solution = solution
            index = factors.index(number)
            split_string_index = split_string.index(all)


            if solution == False:
                new_number = get_random_number(minimum, maximum,0)
                split_string[split_string_index] = add_summand(new_number)
                string = "\xb7".join(split_string)
                solution = get_solution(string)

                solution = D("{:.{prec}f}".format(solution, prec=set_commas)).normalize()
                solution = remove_exponent(solution)
                
                factors[index] = new_number

                return factors, solution, string

            while i<5:
                temp_split_string = split_string
                comma_difference = set_commas - get_number_of_decimals(temp_solution)

                if comma_difference < 0:
                    break

                new_number = get_random_number(minimum, maximum, comma_difference)

                

                temp_split_string[split_string_index] = add_summand(new_number)
                new_string = "\xb7".join(temp_split_string)



                temp_solution = get_solution(new_string)
                if get_number_of_decimals(temp_solution) == set_commas:
                    factors[index] = new_number
                    solution = temp_solution
                    string = new_string
                    return factors, solution, string
                i +=1

    return factors, solution, string   


def get_solution(string):
    value = eval(string.replace('[','(').replace(']',')').replace('\xb7','*').replace(':','/'))
    value = round(value, 10)
    return value



def replace_negative_solutions(string):
    split_string = string.split('-')

    temp_split_string = ['-'+s for s in split_string[1:]]

    split_string = [split_string[0]] + temp_split_string
    
    str = '+'.join(split_string)
    split_string = str.split('+')

    temp_split_string = ['+'+s if s[0]!='-' else s for s in split_string[1:]]
    split_string = [split_string[0]] + temp_split_string  

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
    inner_string_brackets = re.findall(r"\(([0-9+-:\xb7]+)\)", string)

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

    return string


def avoid_futile_brackets(string):
    character_list = [x for x in string]

    operations_strich = ["+", "-"]
    bracket_open = False
    index_list_to_pop = []

    for i, all in enumerate(character_list):
        if bracket_open == False:
            if all == "[" and i==0:
                bracket_open = True
                starting_index = i            
            elif all == "[" and character_list[i-1] in operations_strich:
                bracket_open = True
                starting_index = i
        elif bracket_open == True:
            try:
                following_operation = character_list[i+1]
            except IndexError:
                following_operation = "+"
            if all == "]" and following_operation in operations_strich:
                index_list_to_pop.append(starting_index)
                index_list_to_pop.append(i)
                bracket_open = False
            elif all == "]":
                bracket_open = False  
    

    for index in reversed(index_list_to_pop):
        character_list.pop(index)

    
    string = "".join(character_list)



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
    reduced_operators = ['+', '-']
    division_pair = None
    bracket_open = False
    waiter_brackets = False
    # multiplication_pair = False
    prevent_division = False


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
                string +=  "[" + create_division_pair(division_pair[0], all, show_brackets) + "]" #create_division_pair(division_pair[0], all, show_brackets)

                
            division_pair = 'done'
            continue
        
        elif prevent_division == True:
            operation = random.choice(reduced_operators)
            prevent_division = False
        else:
            operation = random.choice(operators)

        if operation == ':':
            waiter_brackets = False
            rsp = random_switch()
            if i==0 and rsp == True:
                division_pair = [numbers[0], None]
                if division_pair[0] == 0:
                    division_pair[0] = get_random_number(minimum, maximum, commas)
                operation = random.choice(operators)
                if len(numbers)==2: #operation != '\xb7' or 
                    string = create_division_pair(division_pair[0], all, show_brackets)
                elif show_brackets == False:
                    string = "(" + create_division_pair(division_pair[0], all, show_brackets) + ")"
                else: 
                    string = "[" + create_division_pair(division_pair[0], all, show_brackets) + "]"
                
                division_pair = 'done'
                continue
            else:
                if i < len(numbers[1:])-1:
                    if commas !=0:
                        operation = random.choice([x for x in reduced_operators])
                    else:
                        operation = random.choice([x for x in operators if x!=':'])
                    string += operation
                    division_pair = [all, operation]
                elif len(numbers)==2:
                    string = create_division_pair(numbers[0], all, show_brackets) 
                else:
                    if commas !=0:
                        operation = random.choice([x for x in reduced_operators])
                    else:
                        operation = random.choice([x for x in operators if x!=':'])
                    string += operation + add_summand(all, show_brackets)            
        
        else:
            if operation == '\xb7' and commas != 0:
                string +=operation
            elif brackets_allowed == True and random_switch(70) == True and waiter_brackets==False:
                if bracket_open == False:
                    string +=operation
                    if show_brackets == False:
                        string += '('
                    else:
                        string += '['
                    bracket_open = True
                    waiter_brackets = True
                elif bracket_open == True:
                    if show_brackets == False:
                        string += ')'
                    else:
                        string += ']'
                    string += operation
                    bracket_open = False
                    waiter_brackets = False  
            else:
                string += operation
                waiter_brackets = False

            if operation == '\xb7' and commas != 0:
                integer = get_random_number(minimum, maximum, 0, 25)
                string += add_summand(integer, show_brackets)
                prevent_division = True
            else:
                string += add_summand(all, show_brackets)

            

    if bracket_open == True:
        if waiter_brackets == True:
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

    string = avoid_futile_brackets(string)

    solution = eval(string.replace('[','(').replace(']',')').replace('\xb7','*').replace(':','/'))

    if show_brackets== False: ## check if result ist negative, when natural numbers are chosen          
        string, solution = check_for_negative_solutions(string)


    solution = D("{:.{prec}f}".format(solution, prec=set_commas)) #

  

    if solution == 0:
        solution = 0
    string = "{0} = {1}".format(string.replace(".",","), str(solution).replace(".",","))

    # print([numbers, solution, string])
    return [numbers, solution, string] 

def convert_to_fractions(string):
    _temp = re.findall('[0-9.]+', string)


    for all in _temp:
        frac= Fraction(all).limit_denominator()

        if frac.denominator != 1:
            string = string.replace(all, f"{frac.numerator}/{frac.denominator}")
        else:
            string = string.replace(all, str(frac))
    
    return string

def create_single_example_binomische_formeln(binomials_types, coef_a,coef_b,exp_x,exp_y, exponent, binoms_direction_index, fractions_allowed, variable_1, variable_2):
    A, B = symbols("{} {}".format("A", "B"))

    if fractions_allowed == True:
        if coef_a == False:
            coef_1 = 1
        else:
            coef_1 = get_random_fraction(coef_a[0],coef_a[1])
        
        if coef_b == False:
            coef_2 = 1
        else:
            coef_2 = get_random_fraction(coef_b[0],coef_b[1])
    else:
        if coef_a == False:
            coef_1 = 1
        else:
            coef_1 = get_random_number(coef_a[0],coef_a[1])
        
        if coef_b == False:
            coef_2 = 1
        else:
            coef_2 = get_random_number(coef_b[0],coef_b[1])


    if exp_x == [0,0]:
        exponent_x = 0
    else:    
        exponent_x = get_random_number(exp_x[0],exp_x[1])
    if exponent_x ==1:
        exponent_x = ""
    else:
        exponent_x = f"**{exponent_x}"

    if exp_y == False:
        exponent_y = 0
    else:
        exponent_y = get_random_number(exp_y[0],exp_y[1])
    if exponent_y ==1:
        exponent_y = ""
    else:
        exponent_y = f"**{exponent_y}"


    binome = []
    operation = [['+','-'],['-','+']]
    chosen_operation = random.choice(operation)
    for i, all in enumerate(binomials_types):
        possible_binoms = [
            f'({coef_1}*A{exponent_x}+{coef_2}*B{exponent_y})**{exponent}',
            f'({coef_1}*A{exponent_x}-{coef_2}*B{exponent_y})**{exponent}',
            f'({coef_1}*A{exponent_x}{chosen_operation[0]}{coef_2}*B{exponent_y})*({coef_1}*A{exponent_x}{chosen_operation[1]}{coef_2}*B{exponent_y})'
            ]

        if all == True:
            binome.append(possible_binoms[i])

   
    random_choice = random.choice(binome)

    random_choice = re.sub("\*[AB]\*\*0", "", random_choice)


    binom = eval(random_choice)

    solution = str(binom.expand())
    binom = str(binom)

    if fractions_allowed == True:
        solution = convert_to_fractions(solution)
        # binom = convert_to_fractions(binom)



    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    if variable_1 == "":
        choice = random.choice(alphabet)
    else:
        choice = variable_1
    variable_choices = [choice]
    
    alphabet.remove(choice)

    if variable_2 == "":
        choice = random.choice(alphabet)
    else:
        choice = variable_2
    
    variable_choices.append(choice) 


    solution_string = solution.replace("**", "^")

    if fractions_allowed==True:
        solution_string = re.sub('([AB])\*([AB])', r"\1\2", solution_string)
        solution_string = solution_string.replace("*", "\xb7")
    else:
        solution_string = solution_string.replace("*", "")
    solution_string = solution_string.replace("A", variable_choices[0])
    solution_string = solution_string.replace("B", variable_choices[1])
    

    binom_string = random_choice.replace("**", "^")
    # print(binom_string)
    if fractions_allowed==True:
        binom_string = re.sub('([AB])\*([AB])', r"\1\2", binom_string)
        binom_string = binom_string.replace("*", "\xb7")
    else:
        binom_string = binom_string.replace("*", "")
    binom_string = binom_string.replace("A", variable_choices[0])
    binom_string = binom_string.replace("B", variable_choices[1])


    binom_string = re.sub('([^0-9])1\xb7([^0-9\)/])', r"\1\2",binom_string)
    binom_string = re.sub('([^0-9])1([^0-9\)/])', r"\1\2",binom_string)
    binom_string = re.sub('([^0-9])\xb7([^0-9])', r"\1\2",binom_string)
    binom_string = binom_string.replace("+-", "-")
    binom_string = binom_string.replace("--", "+")


    if binoms_direction_index == 1:
        index = random.choice([0,2])
    else:
        index = binoms_direction_index

    if index == 0:
        string = f"{binom_string} = {solution_string}"
    elif index == 2:
        string = f"{solution_string} = {binom_string}"
        binom_string, solution_string = solution_string, binom_string

    solution_string = re.sub("([0-9]+)/([0-9]+)",r"\\frac{\1}{\2}", solution_string)
    solution_string = solution_string.replace('\xb7', '\cdot ')
    binom_string = re.sub("([0-9]+)/([0-9]+)",r"\\frac{\1}{\2}", binom_string)
    binom_string = binom_string.replace('\xb7', '\cdot ')

    # print(binom_string)
    return [f"${binom_string}$",f"${solution_string}$", string]


def get_random_fraction(min, max):
    # if min == 0 and max == 1:
    #     numerator = 1
    #     denominator = get_random_number(1, 9)
    # else:
    # numerator = get_random_number(min, max-1)
    # denominator = get_random_number(numerator+1, max)
    numerator = get_random_number(min, max)
    denominator = get_random_number(min, max) 
    # denominator = get_random_number(numerator, max)

    return Fraction("{0}/{1}".format(numerator, abs(denominator)))


def create_list_of_examples_addition(examples, minimum, maximum, commas, anzahl_summanden, smaller_or_equal):
    list_of_examples = []

    for _ in range(examples):
        new_example = create_single_example_addition(minimum, maximum, commas, anzahl_summanden, smaller_or_equal)
        list_of_examples.append(new_example)

    return list_of_examples

def create_list_of_examples_subtraction(examples, minimum, maximum, commas, negative_solutions_allowed, anzahl_subtrahenden,smaller_or_equal):
    list_of_examples = []

    for _ in range(examples):
        new_example = create_single_example_subtraction(minimum, maximum, commas, negative_solutions_allowed,anzahl_subtrahenden, smaller_or_equal)
        list_of_examples.append(new_example)

    return list_of_examples

def create_list_of_examples_multiplication(examples, minimum_1, maximum_1, commas_1, smaller_or_equal_1, minimum_2, maximum_2, commas_2, smaller_or_equal_2):
    list_of_examples = []

    for _ in range(examples):
        new_example = create_single_example_multiplication(minimum_1, maximum_1, commas_1, smaller_or_equal_1,minimum_2, maximum_2, commas_2, smaller_or_equal_2)
        list_of_examples.append(new_example)

    return list_of_examples

def create_list_of_examples_division(examples, minimum_1, maximum_1, minimum_2, maximum_2, commas_div, smaller_or_equal_div, commas_result, smaller_or_equal_result, output_type):
    list_of_examples = []

    for _ in range(examples):
        new_example = create_single_example_division(minimum_1, maximum_1, minimum_2, maximum_2, commas_div, smaller_or_equal_div, commas_result,smaller_or_equal_result, output_type)
        list_of_examples.append(new_example)

    return list_of_examples


def create_list_of_examples_ganze_zahlen(typ, examples, minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed, show_brackets):
    list_of_examples = []

    for _ in range(examples):
        if typ == '+' or typ == '-' or typ == '+-':
            new_example = create_single_example_ganze_zahlen_strich(typ, minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed)
        elif typ == '*:':
            new_example = create_single_example_ganze_zahlen_punkt(minimum, maximum, commas, anzahl_summanden, smaller_or_equal)
        elif typ == '+-*:': 
            new_example = create_single_example_ganze_zahlen_grundrechnungsarten(minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed, show_brackets)
        list_of_examples.append(new_example)

    return list_of_examples


def create_list_of_examples_binomische_formeln(examples, binomials_types, a,b,x,y, exponent, binoms_direction_index, fractions_allowed, variable_1, variable_2):
    list_of_examples = []

    for _ in range(examples):
        new_example = create_single_example_binomische_formeln(binomials_types, a,b,x,y, exponent, binoms_direction_index, fractions_allowed, variable_1, variable_2)
        list_of_examples.append(new_example)

    return list_of_examples


def get_number_of_decimals(x):
    num = D('{}'.format(x)).normalize()
    num = remove_exponent(num)
    num = abs(num.as_tuple().exponent)
    return num

def create_latex_string_addition(content, example, ausrichtung):
    summanden = example[0]
    
    max_decimal=0
    for all in summanden:
        decimals = get_number_of_decimals(all)
        if decimals > max_decimal:
            max_decimal = decimals    

    if ausrichtung == 0:
        content += "\item \\begin{tabular}{rr}\n"

        for all in summanden:
            decimals = get_number_of_decimals(all)
            if decimals != max_decimal:
                if decimals == 0:
                    phantom = ","+"0"*max_decimal
                else:
                    phantom = "0"*(max_decimal-decimals)
                
                phantom = "\hphantom{{{0}}}".format(phantom)
            else:
                phantom = ""


            content += "& ${0}{1}$ \\\\ \n".format(str(all).replace(".",","), phantom)

        content += """\hline&\\antwort{{${0}$}}
        \end{{tabular}}\n""".format(str(example[-2]).replace(".",","))
        # .format(str(example[0]).replace(".",","),str(example[1]).replace(".",","),str(example[2]).replace(".",","))
    elif ausrichtung == 1:
        content += "\item ${0}".format(str(summanden[0]).replace(".",","))

        for all in summanden[1:]:
            content += " + {}".format(str(all).replace(".",","))
        

        content += " = \\antwort{{{0}}}$\n\n".format(str(example[-2]).replace(".",","))
    return content

def create_latex_string_subtraction(content, example, ausrichtung):
    subtrahenden = example[0]
    if ausrichtung == 0:
        decimal_1 = get_number_of_decimals(subtrahenden[0])
        decimal_2 = get_number_of_decimals(subtrahenden[1])
        if decimal_1==decimal_2:
            phantom_1 = ""
            phantom_2 = ""
        else:
            if decimal_1>decimal_2:
                diff = decimal_1-decimal_2
                if decimal_2==0:
                    phantom = "," + "0"*diff
                else:
                    phantom = "0"*diff
                phantom_2 = "\hphantom{{{0}}}".format(phantom)
                phantom_1 = ""
            elif decimal_2>decimal_1:
                diff = decimal_2-decimal_1
                if decimal_1 ==0:
                    phantom = "," + "0"*diff
                else:
                    phantom = "0"*diff
                phantom_1 = "\hphantom{{{0}}}".format(phantom)
                phantom_2 = ""
            

        content += """
        \item \\begin{{tabular}}{{rr}}
        & ${0}{3}$ \\\\
        & $-{1}{4}$ \\\\ \hline
        &\\antwort{{${2}$}}
        \end{{tabular}}\n
        """.format(str(subtrahenden[0]).replace(".",","), str(subtrahenden[1]).replace(".",","),str(example[-2]).replace(".",","), phantom_1, phantom_2)
    elif ausrichtung == 1:
        content += "\item ${0}".format(str(subtrahenden[0]).replace(".",","))

        for all in subtrahenden[1:]:
            content += " - {}".format(str(all).replace(".",","))

        content += " = \\antwort{{{0}}}$\n\n".format(str(example[-2]).replace(".",","))
    return content



def create_single_line_multiplication(factor_1, digit, i, is_integer):

    factor_digit_length = get_number_of_digits(factor_1)
    subresult = int(change_to_integer(factor_1)*digit)

    if get_number_of_digits(subresult) > factor_digit_length:
        dif = get_number_of_digits(subresult)-factor_digit_length
        if i == 0:
            hspace = dif*'\hspace{-0.5em}'
        elif dif > i:
            hspace = (dif-i)*'\hspace{-0.5em}'
        else:
            hspace = (i-dif)*'\enspace'
    else:
        dif = factor_digit_length-get_number_of_digits(subresult)  
        hspace = (i+dif)*'\enspace'

    if is_integer==False:
        hspace += "\,"
    string = '\\antwortzeile {0} {1} \\\\\n'.format(hspace, str(subresult))
    return string



def create_latex_string_multiplication(content, example, solution_type):
    factor_1 = example[0]
    factor_2 = example[1]

    _list = split_into_digits(change_to_integer(factor_2))

    result = []
    for digit in _list:
        result.append(int(factor_1*digit))

    factor_digit_length = get_number_of_digits(factor_1)
    
    content += """
\item$\\begin{{array}}{{l}}
{0} \cdot {1} \\\\ \hline
""".format(str(factor_1).replace('.',','),str(factor_2).replace('.',','))

    result = factor_1*factor_2
    if solution_type == 1:
        if isinstance(factor_1,int):
            is_integer = True
        else:
            is_integer = False
        for i, digit in enumerate(_list):
            content += create_single_line_multiplication(factor_1, digit, i, is_integer=is_integer)
        num = len(_list)-1
        if get_number_of_digits(result) > factor_digit_length:
            dif = get_number_of_digits(result)-factor_digit_length
            if dif > num:
                hspace = (dif-num)*'\hspace{-0.5em}'
            else:
                hspace = (num-dif)*'\enspace'
        else:
            dif = factor_digit_length-get_number_of_digits(result)  
            hspace = (num+dif)*'\enspace'

        content += '\hline\n\\antwortzeile {0} {1}\\\\\n'.format(hspace, str(result).replace('.',','))
    else:
        content += '\\antwortzeile {0}\\\\\n'.format(str(result).replace('.',','))
    content += "\end{array}$\n\\antwort[\\vspace{2cm}]{}\n\n"


    # content += """
    #     \item \\begin{{tabular}}{{rrr}}
    #     ${0}$ &$\cdot$ & ${1}$ \\\\ \hline
    #     \multicolumn{{3}}{{r}}{{\\antwort{{${2}$}}}}\\\\
    #     \end{{tabular}}\n
    # """.format(str(example[0]).replace(".",","),str(example[1]).replace(".",","),str(example[2]).replace(".",","))

    return content


def get_first_temp_division(dividend, temp_solution):
    end_index =1
    part_divide = str(dividend)[0:end_index]
    while True:
        if temp_solution <= eval(part_divide):
            return part_divide, end_index-1
        
        end_index +=1
        part_divide = str(dividend)[0:end_index]

def get_temp_solution_division(dividend, divisor, solution):
    str_solution = [x for x in solution if x.isnumeric()]

    list_temp_solutions = []

    for i, all in enumerate(str_solution):
        temp_solution = eval(f"{all}*{divisor}")

        if i == 0:
            first_part_divide, end_index = get_first_temp_division(dividend, temp_solution)
            part_divide = first_part_divide

        if isinstance(part_divide, str):
            part_divide = part_divide.lstrip('0')

        differenz = eval(part_divide)-temp_solution
        differenz = round(differenz, 10)
        end_index +=1
        try:
            if str(dividend)[end_index].isnumeric():
                next_digit = str(dividend)[end_index]
                next_digit_string = next_digit
            else:
                end_index +=1
                next_digit = str(dividend)[end_index]
                next_digit_string = f"\;{next_digit}"       
        except IndexError:
            next_digit = ""
            next_digit_string = next_digit


        part_divide = f"{differenz}{next_digit}"

        list_temp_solutions.append([f"{differenz}",next_digit_string])

    return first_part_divide, list_temp_solutions


def create_latex_string_division(content, example, solution_type):

    if "R " in str(example[2]):
        solution, rest = example[2].split("R ")
        solution = solution.replace(".",",")
        rest = "\n\n\\antwort{{R {}}}".format(rest)    
    else:
        solution = str(example[2]).replace(".",",")
        rest = ""

    content += f"""
    \item $\\begin{{array}}{{l}}
    {str(example[0]).replace(".",",")} : {str(example[1]).replace(".",",")} = \\antwort[\\vspace{{1.5cm}}]{{{solution}}} \\\\
    """

    num_decimal_divisor = get_number_of_decimals(example[1])

    if num_decimal_divisor != 0:
        example[0] = example[0]*10**(num_decimal_divisor)
        example[0] = example[0].normalize()
        example[0] = remove_exponent(example[0])
        example[1] = int(example[1]*10**(num_decimal_divisor))


    first_part_divide, list_temp_solutions = get_temp_solution_division(dividend=example[0], divisor=example[1], solution=solution)


    if num_decimal_divisor != 0:
        content += f"""\\antwortzeile {str(example[0]).replace(".",",")} : {str(example[1]).replace(".",",")} \\\\ """ 



    previous_num_of_digits  = get_number_of_digits(first_part_divide)
    # multiplier = 0
    rest = ""
    komma = False
    for i, all in enumerate(list_temp_solutions):
        num_of_digits = get_number_of_digits(int(all[0]))

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
        if komma == True:
            hspace += "\\;"
        if "\\;" in all[1]:
            komma = True


        content += f"\\antwortzeile {hspace} {all[0]}{all[1]}{rest} \\\\ \n"
        previous_num_of_digits = num_of_digits 
        # print(content)
        # print(f"multiplier: {multiplier}")
    content += "\end{array}$\n\n"





    # content += "\item ${0} : {1} = \\antwort[\\vspace{{1.5cm}}]{{{2}}}${3}\n\n".format(str(example[0]).replace(".",","),str(example[1]).replace(".",","),solution, rest)


    return content


def create_latex_string_ganze_zahlen(content, example):
    equation = example[-1]
    
    x,y = equation.split(" = ")
    
    temp_content = "\item ${0} = \\antwort{{{1}}}$\n\n".format(x.replace(".",","),y.replace(".",","))
    temp_content = temp_content.replace('\xb7', '\cdot')
    content += temp_content
    return content


def create_latex_string_binomische_formeln(content, example):

    example_string = re.sub("([0-9]+)/([0-9]+)",r"\\frac{\1}{\2}", example[2])

    aufgabe, loesung = example_string.split(" = ")
    
    temp_content = f"\item ${aufgabe} = \\antwort{{{loesung}}}$\n\n"

    temp_content = temp_content.replace('\xb7', '\cdot ')

    content += temp_content

    return content


def create_latex_worksheet(order_of_examples, dict_of_examples,total_number_of_examples, index, titel, arbeitsanweisung,nummerierung, item_spacing, solution_type=0):
    if titel != False:
        content = "\section{{{0}}}\n\n".format(titel.replace('&', '\&'))
    else:
        content = ""


    if arbeitsanweisung != False:
        content += arbeitsanweisung

    enumi_counter = 0
    for widget in order_of_examples:
        set_of_examples = dict_of_examples[widget] 
    # for all in dict_of_examples.values():
        index = set_of_examples['index_thema']
        ausrichtung = set_of_examples['ausrichtung']
        columns = set_of_examples['spalten']
        
        if columns > 1:
            content += "\\begin{{multicols}}{{{0}}}\n".format(columns)

        content += f"\\begin{{enumerate}}[{nummerierung}]\setlength\itemsep{{{item_spacing}cm}}\n"

        # if fortlaufende_nummerierung == True:
        #     content += f"\setcounter{{enumi}}{{{enumi_counter}}}"
        #     enumi_counter +=1

        list_of_examples = set_of_examples['list_of_examples']
        for example in list_of_examples:
            if index == 0:
                content = create_latex_string_addition(content, example, ausrichtung)
            elif index == 1:
                content = create_latex_string_subtraction(content, example, ausrichtung)
            elif index == 2:
                content = create_latex_string_multiplication(content, example, solution_type)
            elif index == 3:
                content = create_latex_string_division(content, example, solution_type)
            elif index == 4 or index == 5 or index == 6 or index ==7:
                content = create_latex_string_ganze_zahlen(content, example)
            elif index == 8:
                content = create_latex_string_binomische_formeln(content, example)

        content += "\end{enumerate}\n"

        if columns > 1:
            content += "\end{multicols}\n"
        
        content += f"\\vspace{{{item_spacing}cm}}\n\n"
     
    return content



    for example in list_of_examples:
        if index == 0:
            content = create_latex_string_addition(content, example, ausrichtung)
        elif index == 1:
            content = create_latex_string_subtraction(content, example, ausrichtung)
        elif index == 2:
            content = create_latex_string_multiplication(content, example, solution_type)
        elif index == 3:
            content = create_latex_string_division(content, example)
        elif index == 4 or index == 5 or index == 6 or index ==7:
            content = create_latex_string_ganze_zahlen(content, example)


    content += "\end{enumerate}"

    if columns > 1:
        content += "\end{multicols}"

    return content


def get_all_pixels(content):
    return re.findall("[A-J][0-9]",content) 



def get_max_pixels_nonogram():
    max = 0
    for all in all_nonogramms.values():
        if len(all)>max:
            max = len(all)
    
    return max


def get_all_solution_pixels(list_of_examples, nonogram):
   

    all_pixels_solution = all_nonogramms[nonogram]
    random.shuffle(all_pixels_solution)
    solution_pixels = {}

   

    for i, pixel in enumerate(all_pixels_solution):
        if i<len(list_of_examples):
            solution_pixels[pixel] =  [True, list_of_examples[i][-2]]
        else:
            solution_pixels[pixel] = [True, None]


    return nonogram, solution_pixels
    # for num, pixel in enumerate(all_pixels_solution):
    #     if num<examples:
    #         solution_pixels.append([pixel, True])
    #     else:
    #         return solution_pixels  


def replace_correct_pixels(content, coordinates_nonogramm):
    for pixel in list_all_pixels:
        if pixel in coordinates_nonogramm.keys():
            if coordinates_nonogramm[pixel][0] == False:
                content = content.replace(pixel, "")
            elif coordinates_nonogramm[pixel][0] == True and coordinates_nonogramm[pixel][1] == None:
                content = content.replace(pixel, "\cellcolor{black}")
            else:
                content = content.replace(pixel, "\ifthenelse{\\theAntworten=1}{\cellcolor{black}{}}{}")          
        else:
            content = content.replace(pixel, "")

    return content            


    # for pixel in list_all_pixels:
    #     for coordinate in coordinates_nonogramm:
    #         if pixel == coordinate[0]:
    #             if coordinate[1] == True:
    #                 content = content.replace(pixel, "\ifthenelse{\\theAntworten=1}{\cellcolor{black}}{}")
    #                 break
    #             else:    
    #                 content = content.replace(pixel, "\cellcolor{black}")
    #                 break
    #         else:
    #             content = content.replace(pixel, "")
    #             break    
    
    # return content           
    # for coordinate in coordinates_nonogramm:
    #     if coordinate[1] == True:
            


    #     if pixel in all_nonogramms[nonogram]:
    #         if num<examples:
    #             content = content.replace(pixel, "\ifthenelse{\\theAntworten=1}{\cellcolor{black}}{}")
    #             solution_pixels.append(pixel)
    #             num+=1
    #         else:
    #             content = content.replace(pixel, "\cellcolor{black}")
    #     else:
    #         content = content.replace(pixel, "")

    # return content, solution_pixels


def collect_dummy_solutions(dict_all_examples):
    all_dummy_solutions = []
    for all in dict_all_examples.values():
        all_dummy_solutions.extend(all['dummy_examples'])

    _list = random.choices(all_dummy_solutions, k=10)

    return _list

def create_coordinates(solution_pixels, dict_all_examples):
    list_dummy_solutions = collect_dummy_solutions(dict_all_examples)
    for all in list_dummy_solutions:
        while True:
            distract_pixel = random.choice(list_all_pixels)
            if distract_pixel not in solution_pixels.keys():
                solution_pixels[distract_pixel] = [False, all[-2]]
                break

    l = list(solution_pixels.items())
    random.shuffle(l)
    shuffled_coordinates = dict(l)   

    return shuffled_coordinates


    coordinates = solution_pixels
    i=0
    while i < 10:
        distract_pixel = random.choice(list_all_pixels)
        if distract_pixel not in solution_pixels.keys():
            while True:
                distract_result = get_random_solution(self)[-2]
                   
                if distract_result not in coordinates.values():
                    break

            coordinates[distract_pixel] = False
            i +=1
        # possible_option = False

    l = list(coordinates.items())
    random.shuffle(l)
    shuffled_coordinates = dict(l)

    return shuffled_coordinates


def get_random_solution(self, thema):
    # if thema =
    # thema = random.choice(list(self.dict_all_examples_wizard.keys()))
    # thema = self.comboBox_themen_wizard.currentText()

    if thema == 'Addition':
        minimum = self.spinbox_zahlenbereich_minimum.value()
        maximum = self.spinbox_zahlenbereich_maximum.value()
        commas = self.spinbox_kommastellen_wizard.value()
        anzahl_summanden = self.spinBox_zahlenbereich_anzahl_wizard.value()
        smaller_or_equal = self.combobox_kommastellen_wizard.currentIndex()
        distract_result = create_single_example_addition(minimum, maximum, commas, anzahl_summanden, smaller_or_equal)


    elif thema == 'Subtraktion':
        minimum = self.spinbox_zahlenbereich_minimum.value()
        maximum = self.spinbox_zahlenbereich_maximum.value()
        commas = self.spinbox_kommastellen_wizard.value()
        smaller_or_equal = self.combobox_kommastellen_wizard.currentIndex()
        anzahl_subtrahenden = self.spinBox_zahlenbereich_anzahl_wizard.value()
        distract_result = create_single_example_subtraction(minimum, maximum, commas, self.checkbox_negative_ergebnisse_wizard.isChecked(),anzahl_subtrahenden, smaller_or_equal)

    
    elif thema == 'Multiplikation':
        minimum_1 = self.spinBox_first_number_min.value()
        maximum_1 = self.spinBox_first_number_max.value()
        commas_1 = self.spinBox_first_number_decimal.value()
        smaller_or_equal_1 = self.combobox_first_number_decimal.currentIndex()
        minimum_2 = self.spinBox_second_number_min.value()
        maximum_2 = self.spinBox_second_number_max.value()
        commas_2 = self.spinBox_second_number_decimal.value()
        smaller_or_equal_2 = self.combobox_second_number_decimal.currentIndex()
        distract_result = create_single_example_multiplication(minimum_1, maximum_1, commas_1, smaller_or_equal_1, minimum_2, maximum_2, commas_2, smaller_or_equal_2)
        # self.list_of_examples_wizard = create_list_of_examples_multiplication(examples, minimum_1, maximum_1, commas_1, minimum_2, maximum_2, commas_2)

    elif thema == 'Division':
        minimum_1 = self.spinbox_dividend_min_wizard.value()
        maximum_1 = self.spinbox_dividend_max_wizard.value()
        minimum_2 = self.spinbox_divisor_min_wizard.value()
        maximum_2 = self.spinbox_divisor_max_wizard.value()
        commas_div = self.spinBox_divisor_kommastellen_wizard.value()
        smaller_or_equal_div = self.combobox_divisor_kommastelle_wizard.currentIndex()
        commas_result = self.spinbox_ergebnis_kommastellen_wizard.value()
        smaller_or_equal_result = self.combobox_ergebnis_kommastellen_wizard.currentIndex()
        if self.radioButton_division_ohne_rest.isChecked():
            output_type = 0
        elif self.radioButton_division_rest.isChecked():
            output_type = 1
        elif self.radioButton_division_decimal.isChecked():
            output_type = 2         
        distract_result = create_single_example_division(minimum_1, maximum_1, minimum_2, maximum_2, commas_div,smaller_or_equal_div, commas_result, smaller_or_equal_result, output_type)


    elif thema == themen_worksheet_wizard[4] or thema == themen_worksheet_wizard[5] or thema == themen_worksheet_wizard[6] or thema == themen_worksheet_wizard[7]:
        minimum = self.spinbox_zahlenbereich_minimum.value()
        maximum = self.spinbox_zahlenbereich_maximum.value()
        commas = self.spinbox_kommastellen_wizard.value()
        smaller_or_equal = self.combobox_kommastellen_wizard.currentIndex()
        anzahl_summanden = self.spinBox_zahlenbereich_anzahl_wizard.value()
        brackets_allowed = self.checkbox_allow_brackets_wizard.isChecked()


        if thema == themen_worksheet_wizard[5]:
            if self.checkbox_enable_addition.isChecked():
                typ = "+"
            else:
                typ = ""
            
            if self.checkbox_enable_subtraktion.isChecked():
                typ += "-"

            distract_result = create_single_example_ganze_zahlen_strich(typ, minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed)
        elif thema == themen_worksheet_wizard[6]:
            typ = '*:'
            distract_result = create_single_example_ganze_zahlen_punkt(minimum, maximum, commas, anzahl_summanden, smaller_or_equal)
        elif thema == themen_worksheet_wizard[4] or thema == themen_worksheet_wizard[7]:
            if thema == themen_worksheet_wizard[4]:
                show_brackets = False
            else:
                show_brackets = True
            typ = '+-*:'
            distract_result = create_single_example_ganze_zahlen_grundrechnungsarten(minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed, show_brackets)


    elif thema == themen_worksheet_wizard[8]:
        binomials_types = [self.cb_binoms_1.isChecked(), self.cb_binoms_2.isChecked(), self.cb_binoms_3.isChecked()]
        
        if self.checkbox_binoms_a.isChecked():
            a = [self.spinbox_binoms_a_min.value(), self.spinbox_binoms_a_max.value()]
        else:
            a = False
        
        if self.checkbox_binoms_b.isChecked(): 
            b = [self.spinbox_binoms_b_min.value(), self.spinbox_binoms_b_max.value()]
        else:
            b = False 

        x = [self.spinbox_binoms_m_min.value(), self.spinbox_binoms_m_max.value()]


        if self.checkbox_binoms_y.isChecked():
            y = [self.spinbox_binoms_n_min.value(), self.spinbox_binoms_n_max.value()]
        else:
            y = False

        fractions_allowed = self.checkbox_binoms_enable_fraction.isChecked()
        exponent = self.spinbox_binoms_exponent.value()

        variable_1 = self.combobox_choose_variables_1.currentText()
        variable_2 = self.combobox_choose_variables_2.currentText()


        distract_result = create_single_example_binomische_formeln(binomials_types, a,b,x,y, exponent, self.binoms_direction_index, fractions_allowed, variable_1, variable_2)
    return distract_result

def create_nonogramm(nonogram, coordinates_nonogramm, spalten=3):

    if spalten > 1:
        begin_multicols = f"\\begin{{multicols}}{{{spalten}}}"
        end_multicols = "\end{multicols}"
    else:
        begin_multicols = ""
        end_multicols = ""

    nonogram_name = nonogram.split("_")[0].replace("&","\&").title()
    content = f"""\n\\vfil\n\\fontsize{{12}}{{14}}\selectfont
    \meinlr{{{nonogramm_empty}

    \\antwort{{{nonogram_name}}}}}{{\scriptsize
    {begin_multicols}
    \\begin{{enumerate}}"""

#     # list_all_pixles = get_all_pixels(content)
#     # random.shuffle(list_all_pixles)

    content = replace_correct_pixels(content, coordinates_nonogramm)



    for all in coordinates_nonogramm:
        if coordinates_nonogramm[all][1] == None:
            continue
        
        elif coordinates_nonogramm[all][0] == True:
            result = "\\antwort[{0}]{{{0}}}".format(coordinates_nonogramm[all][1])
        
        elif coordinates_nonogramm[all][0] == False:
            result = coordinates_nonogramm[all][1]
        
        content += "\item[\\fbox{{\parbox{{15pt}}{{\centering {0}}}}}] {1}\n".format(all, result)
    # for all in list_coordinates:
#         result = coordinates_nonogramm[all]
#         if result == True:
#             continue

#         if result == False:
#             while result == False:
#                 distract_result = get_random_solution(MainWindow)[-2]
#                 if distract_result not in coordinates_nonogramm:
#                     result = distract_result
#         else:
#             result = "\\antwort[{0}]{{{0}}}".format(result)

#         content += "\item[\\fbox{{\parbox{{15pt}}{{\centering {0}}}}}] {1}\n".format(all, result)
        
    content += f"""
    \end{{enumerate}}
    {end_multicols}}}"""
    return content


def show_all_nonogramms():
    content = ""
    for nonogramm in all_nonogramms:
        all_pixels_solution = all_nonogramms[nonogramm]

        solution_pixels = {}
   

        for pixel in all_pixels_solution:
            solution_pixels[pixel] = True      


        content += """\n\\vfil\n\\fontsize{{12}}{{14}}\selectfont
    {0}:
    
    {1}""".format(nonogramm.split("_")[0].capitalize(), nonogramm_empty)


        content = replace_correct_pixels(content, solution_pixels)


    return content
