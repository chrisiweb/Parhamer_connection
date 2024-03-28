from functools import reduce

import random
from math import floor, ceil
from config import is_empty
# import os
# from config_start import path_localappdata_lama, path_programm
import decimal
import re
from sympy import symbols, gcd_list, lcm_list

from create_nonograms import nonogramm_empty, all_nonogramms, list_all_pixels
from fractions import Fraction
from handle_exceptions import report_exceptions
# import subprocess
# from tex_minimal import tex_preamble, tex_end
# from create_pdf import create_pdf, open_pdf_file, build_pdf_file

dict_themen_wizard = {
    "Arithmetik": {
        "Darstellung von Zahlen": {
            "Stellenwerte" : [
                'self.widget_zahlenbereich_1_combobox',
                'self.widget_zahlenbereich_2_combobox',
                'self.widget_general_direction',               
            ],
            "Römische Zahlen" : [
              'self.widget_zahlenbereich_1_combobox',
              'self.widget_general_direction',  
            ],
            "Zahlengerade": [
                'self.widget_zahlenbereich_startingvalue',
                'self.widget_zahlenbereich_steps',
                'self.widget_zahlenbereich_subticks',
                'self.widget_general_direction_CB',
                'self.widget_coordinatesystem_points',
            ],
        },
        "Teiler && Vielfache":{
            "Primfaktorenzerlegung": [
                'self.widget_zahlenbereich_minimum',
                'self.widget_zahlenbereich_maximum',
                'self.widget_setting_prime',
                'self.comboBox_solution_type_wizard',

            ],
            # "ggT": [
            #     'self.widgetZahlenbereich_anzahl',
            #     'self.widget_zahlenbereich_minimum',
            #     'self.widget_zahlenbereich_maximum',
            #     'self.widget_setting_ggt',                
            # ]        funktioniert noch nicht
        },
        "Positive (Dezimal-)Zahlen": {
            "Addition": [
                'self.widget_ausrichtung_wizard',
                'self.widget_zahlenbereich_minimum',
                'self.widget_zahlenbereich_maximum',
                'self.widget_kommastellen_wizard',
                'self.widgetZahlenbereich_anzahl',                
            ],
            "Subtraktion": [
                'self.widget_ausrichtung_wizard',
                'self.widget_zahlenbereich_minimum',
                'self.widget_zahlenbereich_maximum',
                'self.widget_kommastellen_wizard',
                'self.checkbox_negative_ergebnisse_wizard',
            ],
            "Multiplikation": [
                'self.groupBox_first_number_wizard',
                'self.groupBox_second_number_wizard',
                'self.comboBox_solution_type_wizard',
            ],
            "Division": [
                'self.groupBox_dividend_wizard',
                'self.groupBox_divisor_wizard',
                'self.groupBox_ergebnis_wizard',
                'self.comboBox_solution_type_wizard',
            ],
            "Verbindung der Grundrechnungsarten": [
                'self.widget_zahlenbereich_minimum',
                'self.widget_zahlenbereich_maximum',
                'self.widget_kommastellen_wizard',
                'self.widgetZahlenbereich_anzahl',
                'self.checkbox_allow_brackets_wizard',                  
            ],
        },
        "Negative && Positive (Dezimal-)Zahlen": {
            "Addition && Subtraktion" : [
                'self.widget_zahlenbereich_minimum',
                'self.widget_zahlenbereich_maximum',
                'self.widget_kommastellen_wizard',
                'self.widgetZahlenbereich_anzahl',
                'self.checkbox_allow_brackets_wizard',                  
            ],
            "Multiplikation && Division" : [
                'self.widget_zahlenbereich_minimum',
                'self.widget_zahlenbereich_maximum',
                'self.widget_kommastellen_wizard',
                'self.widgetZahlenbereich_anzahl',                
            ],
            "Verbindung der Grundrechnungsarten" : [
                'self.widget_zahlenbereich_minimum',
                'self.widget_zahlenbereich_maximum',
                'self.widget_kommastellen_wizard',
                'self.widgetZahlenbereich_anzahl',
                'self.checkbox_allow_brackets_wizard', 
            ],
        },
        },
    "Geometrie": {
        "Grundlagen der Geometrie" : {
        "Koordinatensystem" : [
            'self.widget_coordinatesystem_setting',
            'self.widget_coordinatesystem_points',
            'self.widget_general_direction_CB',
        ],
    },
    },
    "Terme": {
        "Binomische Formeln": [
        'self.groupbox_binoms_types',
        'self.widget_binoms_set_variables_factors',
        'self.widget_binoms_set_variables_exponents',
        'self.label_binom_example',
        'self.widget_binom_further_settings',
        ]
    },
}


# STEPS FOR NEW TOPIC
#
# 1. Widgets erstellen -> lama_gui.py
# 2. Notwendige Widgets zur Liste hinzufügen -> worksheet_wizard.py
# 3. Aufgabe berechnen definieren: self.create_list_of_examples_wizard (LaMa.pyw)
# 4. create_list_of_examples_... in worksheet_wizard.py erstellen


dict_wizard_variables = {
    'examples' : 'self.spinBox_number_wizard.value()',
    'anzahl_zahlen' : 'self.spinBox_zahlenbereich_anzahl_wizard.value()',
    'minimum_combobox': 'self.combobox_zahlenbereich_2.currentIndex()',
    'minimum_spinbox' : 'self.spinbox_zahlenbereich_minimum.value()',
    'minimum_spinbox_1' : 'self.spinBox_first_number_min.value()',
    'minimum_spinbox_2' : 'self.spinBox_second_number_min.value()',
    'minimum_division_1' :  'self.spinbox_dividend_min_wizard.value()',
    'minimum_division_2' :  'self.spinbox_divisor_min_wizard.value()',
    'minimum_index' : 'self.combobox_zahlenbereich_2_leq.currentIndex()',
    'maximum_combobox' : 'self.combobox_zahlenbereich_1.currentIndex()',
    'maximum_spinbox' : 'self.spinbox_zahlenbereich_maximum.value()',
    'maximum_spinbox_1' : 'self.spinBox_first_number_max.value()',
    'maximum_spinbox_2' : 'self.spinBox_second_number_max.value()',
    'maximum_division_1' :  'self.spinbox_dividend_max_wizard.value()',
    'maximum_division_2' :  'self.spinbox_divisor_max_wizard.value()',
    'maximum_index' : 'self.combobox_zahlenbereich_1_leq.currentIndex()',
    'general_direction_index' : 'self.pushbutton_general_direction',
    'starting_value' : 'self.spinbox_zahlenbereich_startingvalue.value()',
    'starting_value' : 'self.spinbox_zahlenbereich_startingvalue.value()',
    'steps' : 'self.spinbox_zahlenbereich_steps.value()',
    'subticks' :  'self.spinbox_zahlenbereich_subticks.value()+1',
    'setting_decimal_fraction' : 'self.combobox_decimal_fraction.currentIndex()', 
    'maximum_prime' :  'self.spinbox_maximum_prime.value()',
    'display_as_powers' : 'self.checkbox_prime_powers.isChecked()',
    'ggt_1_checked' :  'self.checkbox_ggT_1.isChecked()',
    'commas' : 'self.spinbox_kommastellen_wizard.value()',
    'commas_1' : 'self.spinBox_first_number_decimal.value()',
    'commas_2' : 'self.spinBox_second_number_decimal.value()',
    'smaller_or_equal' : 'self.combobox_kommastellen_wizard.currentIndex()',
    'smaller_or_equal_1' : 'self.combobox_first_number_decimal.currentIndex()',
    'smaller_or_equal_2' : 'self.combobox_second_number_decimal.currentIndex()',
    'negative_solutions_allowed' : 'self.checkbox_negative_ergebnisse_wizard.isChecked()',
    'commas_div' :  'self.spinBox_divisor_kommastellen_wizard.value()',
    'smaller_or_equal_div' : 'self.combobox_divisor_kommastelle_wizard.currentIndex()',
    'commas_result_div' : 'self.spinbox_ergebnis_kommastellen_wizard.value()',
    'smaller_or_equal_result' : 'self.combobox_ergebnis_kommastellen_wizard.currentIndex()',
    'output_type_division' : 'self.combobox_dividend_wizard',
    'brackets_allowed' : 'self.checkbox_allow_brackets_wizard.isChecked()',
    'enable_addition' : 'self.checkbox_enable_addition.isChecked()',
    'enable_subtraction' : 'self.checkbox_enable_subtraktion.isChecked()',
    'half_allowed_coord' :  'self.checkbox_coordinatesystem_zwischenwerte.isChecked()',
    'negative_allowed_coord' : 'self.checkbox_coordinatesystem_negative_numbers.isChecked()',
    'binomials_type_1' : 'self.cb_binoms_1.isChecked()',
    'binomials_type_2' : 'self.cb_binoms_2.isChecked()',
    'binomials_type_3' : 'self.cb_binoms_3.isChecked()',
    'binomials_checkbox_a' : 'self.checkbox_binoms_a.isChecked()',
    'binomials_checkbox_b' : 'self.checkbox_binoms_b.isChecked()',
    'binomials_checkbox_y' : 'self.checkbox_binoms_y.isChecked()',
    'binomials_minimum_a' : 'self.spinbox_binoms_a_min.value()',
    'binomials_maximum_a' : 'self.spinbox_binoms_a_max.value()',
    'binomials_minimum_b' : 'self.spinbox_binoms_b_min.value()',
    'binomials_maximum_b' : 'self.spinbox_binoms_b_max.value()',
    'binomials_minimum_m' : 'self.spinbox_binoms_m_min.value()',
    'binomials_maximum_m' : 'self.spinbox_binoms_m_max.value()',
    'binomials_minimum_n' : 'self.spinbox_binoms_n_min.value()',
    'binomials_maximum_n' : 'self.spinbox_binoms_n_max.value()',
    'binomials_fractions_allowed' : 'self.checkbox_binoms_enable_fraction.isChecked()',
    'binomials_exponent' : 'self.spinbox_binoms_exponent.value()',
    'binomials_variable_1' : 'self.combobox_choose_variables_1.currentText()',
    'binomials_variable_2' : 'self.combobox_choose_variables_2.currentText()',
    'binomials_direction_index' : 'self.pushbutton_binoms_direction',

}

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
            if switch == True and x!=max and (min>0 or x!=min):
                num = float(f"{str(x)}.5")
                return num
            else:
                return int(x)   
        else:
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

def insert_dots(number):
    number = str(number)
    number = number.split(".")
    result = ""
    for i in range(len(number[0])):
        if (len(number[0]) - i) % 3 == 0 and i != 0:
            result += "*"
        result += number[0][i]
    if len(number)>1:
        result = f"{result}.{number[1]}"
    return result


def simplify_numbers(number, num_stellenwerte, minimum_index, maximum_index):
    str_num = [*str(number)]
    number_of_zeros = str_num.count("0")
    erwartungswert = 4-number_of_zeros #4.5-1 if first number must exist


    if erwartungswert<0:
        return number
    
    probability = erwartungswert/num_stellenwerte

    str_new_number = []
    for i, all in enumerate(str_num):
        if str_new_number.count('0')+3>=len(str_num):
            str_new_number.append(str(get_random_number(1,9)))
        elif maximum_index==0 and i==0:
            if all == '0':
                str_new_number.append(str(get_random_number(1,9)))
            else:
                str_new_number.append(all)
        elif minimum_index==0 and i==len(str_num)-1:
            if all == '0':
                str_new_number.append(str(get_random_number(1,9)))
            else:
                str_new_number.append(all)
        elif all != '0' and all!='.':
            if random_switch(probability*100)==False:
                str_new_number.append('0')
            else:
                str_new_number.append(all)
        else:
            str_new_number.append(all)

    if "." in str_new_number:
        number = float("".join(str_new_number))
    else:
        number = int("".join(str_new_number))
    return number


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

dict_of_roman_max = {'I':3, 'V': 8, 'X':39, 'L':89, 'C':399, 'D':899, 'M':3999}

def create_single_example_stellenwert(dict_all_settings_wizard): #minimum, minimum_index, maximum, maximum_index, general_direction_index
    minimum = dict_all_settings_wizard['minimum_combobox']
    minimum_index = dict_all_settings_wizard['minimum_index']
    maximum = dict_all_settings_wizard['maximum_combobox']
    maximum_index = dict_all_settings_wizard['maximum_index']
    general_direction_index = dict_all_settings_wizard['general_direction_index']


    maximum = maximum+2

    maximum_num = int('9'*maximum)
    minimum_num = int('1'+'0'*(maximum-1))


    number = get_random_number(minimum_num,maximum_num, minimum, force_decimals=True)
    number = simplify_numbers(number, maximum+minimum, minimum_index, maximum_index)
    _list_stellenwert = number_to_placevalue(number)

    string_stellenwert = " ".join(_list_stellenwert)

    if general_direction_index == 1:
        index = random.choice([0,2])
    else:
        index = general_direction_index


    number = insert_dots(number)
    if index == 0:
        _string = f"{number} = {string_stellenwert}".replace(".",",")
        _string = _string.replace("*",'.')
        number = number.replace("*",'.')
        return [number, string_stellenwert, _string]
    elif index == 2:
        _string = f"{string_stellenwert} = {number}".replace(".",",")
        _string = _string.replace("*",'.')
        number = number.replace("*",'.')
        return [string_stellenwert,number, _string]
    


def create_single_example_roman_numerals(dict_all_settings_wizard):
    roman_max = dict_all_settings_wizard['maximum_combobox']
    maximum_index =  dict_all_settings_wizard['maximum_index']
    general_direction_index = dict_all_settings_wizard['general_direction_index']
    if maximum_index == 1:
        number = get_random_number(10, dict_of_roman_max[roman_max])
    else:
        chosen_index = list(dict_of_roman_max.keys()).index(roman_max)
        roman_min = list(dict_of_roman_max.keys())[chosen_index-1]
        number = get_random_number(dict_of_roman_max[roman_min]+1, dict_of_roman_max[roman_max])
    
    roman_number = int_to_roman(number)

    if general_direction_index == 1:
        index = random.choice([0,2])
    else:
        index = general_direction_index

    if index == 0:
        _string = f"{number} = {roman_number}"
        return [number, roman_number, _string]
    elif index == 2:
        _string = f"{roman_number} = {number}"
        return [roman_number, number, _string]


def create_single_example_number_line(dict_all_settings_wizard): #starting_value, steps, subticks, setting_decimal_fraction
    starting_value = dict_all_settings_wizard['starting_value']
    steps = dict_all_settings_wizard['steps']
    subticks = dict_all_settings_wizard['subticks']
    setting_decimal_fraction = dict_all_settings_wizard['setting_decmial_fraction']

    maximum = starting_value+14*steps
    factor= subticks/steps
    i=0
    list_of_points = []
    temp_dict_fraction = {}
    while i < 5:
        random_decimal = random.uniform(starting_value, maximum)
        x = round(random_decimal* factor) / factor
        x= float(remove_exponent(D(x)))
        x = formatNumber(x)
        if setting_decimal_fraction == 1:
            num = round(random_decimal * factor)
            dem = round(factor) 
            temp_dict_fraction[x]=[num, dem]      



        if x not in list_of_points:
            list_of_points.append(x)
            i+=1

    list_of_points = sorted(list_of_points, key=float)

    dict_of_points = {}
    for i, all in enumerate(list_of_points):
        dict_of_points[index_to_letter(i).upper()]=(all,0)

    _string = ""
    for all in dict_of_points:
        if _string != "":
            _string += ", "
        value = str(dict_of_points[all][0]).replace(".",",")
        _string += f"{all} = {value}"
    # print([dict_of_points, 0, _string])
    return [dict_of_points, 0, _string]

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

def create_single_example_primenumbers(dict_all_settings_wizard):
    minimum = dict_all_settings_wizard['minimum_spinbox']
    maximum = dict_all_settings_wizard['maximum_spinbox']
    maximum_prime = dict_all_settings_wizard['maximum_prime']
    display_as_powers = dict_all_settings_wizard['display_as_powers']
    
    list_of_primenumbers = get_list_of_primenumbers(maximum_prime)

    product, list_of_factors = create_number_from_primes(list_of_primenumbers,minimum,maximum)

    if display_as_powers == True:
        string_list_of_factors = convert_to_powers(list_of_factors)
    else:
        string_list_of_factors = list_of_factors

    solution = '\cdot '.join(str(x) for x in string_list_of_factors)
    solution = f"${solution}$"
    string_product = '\xb7'.join(str(x) for x in string_list_of_factors)
    _string = f"{product} = {string_product}"
    
    return [product, solution, _string]

def create_single_example_ggt(dict_all_settings_wizard): #anzahl_zahlen, minimum, maximum, ggt_1_checked
    # print(dict_all_settings_wizard)
    anzahl_zahlen = dict_all_settings_wizard['anzahl_zahlen']
    minimum = dict_all_settings_wizard['minimum_spinbox']
    maximum = dict_all_settings_wizard['maximum_spinbox']
    ggt_1_checked = dict_all_settings_wizard['ggt_1_checked']

    list_of_numbers = []

    while True:
        while True:
            x = get_random_number(minimum, maximum)
            if x not in list_of_numbers:
                list_of_numbers.append(x)
            
            if len(list_of_numbers)==anzahl_zahlen:
                break

        ggt = gcd_list(list_of_numbers)

        if ggt == 1:
            if ggt_1_checked == False:
                list_of_numbers = []
                continue
            elif random_switch(90):
                list_of_numbers = []
                continue
            else:
                break
        else:
            break

    joined_numbers = ', '.join(str(x) for x in list_of_numbers)
    _string = f"ggT({joined_numbers}) =  {ggt}"
    print([list_of_numbers,ggt,_string])
    return [list_of_numbers,ggt,_string]
        

def create_single_example_addition(dict_all_settings_wizard_wizard):
    minimum = dict_all_settings_wizard_wizard['minimum_spinbox']
    maximum = dict_all_settings_wizard_wizard['maximum_spinbox']
    commas = dict_all_settings_wizard_wizard['commas']
    anzahl_summanden = dict_all_settings_wizard_wizard['anzahl_zahlen']
    smaller_or_equal = dict_all_settings_wizard_wizard['smaller_or_equal']

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

def create_single_example_subtraction(dict_all_settings_wizard):
    minimum = dict_all_settings_wizard['minimum_spinbox']
    maximum = dict_all_settings_wizard['maximum_spinbox']
    commas = dict_all_settings_wizard['commas']
    negative_solutions_allowed = dict_all_settings_wizard['negative_solutions_allowed']
    anzahl_subtrahenden = dict_all_settings_wizard['anzahl_zahlen']
    smaller_or_equal = dict_all_settings_wizard['smaller_or_equal']
    print(dict_all_settings_wizard)

    set_commas=commas
    print(negative_solutions_allowed)
    # if negative_solutions_allowed == False:
    #     subtrahenden_maximum = maximum/anzahl_subtrahenden
    # else:
    #     subtrahenden_maximum = maximum

    # for _ in range(anzahl_subtrahenden):
    if smaller_or_equal == 1:
        commas = random.randint(0,set_commas)
    subtrahend = get_random_number(minimum, maximum, commas)

    if smaller_or_equal == 1:
        commas = random.randint(0,set_commas)
    
    if negative_solutions_allowed == False:   
        minuend = get_random_number(ceil(subtrahend), maximum, commas)
    else:
        minuend = get_random_number(minimum, maximum, commas)


    solution = minuend-subtrahend

    string = str(minuend).replace(".",",")

    string = f"{minuend} - {subtrahend} = {solution}".replace(".",",")    


    return [[minuend, subtrahend],solution, string]


def create_single_example_multiplication(dict_all_settings_wizard): #minimum_1, maximum_1, commas_1, smaller_or_equal_1 ,minimum_2, maximum_2, commas_2, smaller_or_equal_2
    minimum_1 = dict_all_settings_wizard['minimum_spinbox_1']
    maximum_1 = dict_all_settings_wizard['maximum_spinbox_1']
    commas_1 = dict_all_settings_wizard['commas_1']
    smaller_or_equal_1 = dict_all_settings_wizard['smaller_or_equal_1']
    minimum_2 = dict_all_settings_wizard['minimum_spinbox_2']
    maximum_2 = dict_all_settings_wizard['maximum_spinbox_2']
    commas_2 = dict_all_settings_wizard['commas_2']
    smaller_or_equal_2 = dict_all_settings_wizard['smaller_or_equal_2']


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

def create_single_example_division(dict_all_settings_wizard):
    minimum_1 = dict_all_settings_wizard['minimum_division_1']
    maximum_1 = dict_all_settings_wizard['maximum_division_1']
    minimum_2 = dict_all_settings_wizard['minimum_division_2']
    maximum_2 = dict_all_settings_wizard['maximum_division_2']
    commas_div = dict_all_settings_wizard['commas_div']
    smaller_or_equal_div = dict_all_settings_wizard['smaller_or_equal_div']
    commas_result = dict_all_settings_wizard['commas_result']
    smaller_or_equal_result = dict_all_settings_wizard['smaller_or_equal_result']
    output_type_division = dict_all_settings_wizard['output_type_division']

    if smaller_or_equal_div == 1:
        set_commas_div=commas_div
        commas_div = random.randint(0,set_commas_div)
    
    divisor = get_random_number(minimum_2, maximum_2, commas_div)

    if output_type_division == 1:  
        dividend = get_random_number(minimum_1, maximum_1)
        result = str(get_quotient_with_rest(dividend, divisor))

    else:
        result_min = ceil(minimum_1/divisor)
        result_max = floor(maximum_1/divisor)

        if output_type_division == 0:
            commas_result = 0
        else:
            if smaller_or_equal_result == 1:
                set_commas_result=commas_result
                commas_result = random.randint(0,set_commas_result)
        result = get_random_number(result_min, result_max, decimal= commas_result,force_decimals=True)
        dividend = result*divisor
        dividend = D(f'{dividend}').normalize()
        dividend = remove_exponent(dividend)
        
        result = str(result)

    string = "{0} : {1} = {2}".format(str(dividend).replace(".",","),str(divisor).replace(".",","),result.replace(".",","))

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

def create_single_example_ganze_zahlen_strich(dict_all_settings_wizard):
    anzahl_zahlen = dict_all_settings_wizard['anzahl_zahlen']
    minimum = dict_all_settings_wizard['minimum_spinbox']
    maximum = dict_all_settings_wizard['maximum_spinbox']
    commas = dict_all_settings_wizard['commas']
    smaller_or_equal = dict_all_settings_wizard['smaller_or_equal']
    brackets_allowed = dict_all_settings_wizard['brackets_allowed']
    enable_addition = dict_all_settings_wizard['enable_addition']
    enable_subtraction = dict_all_settings_wizard['enable_subtraction']

    #typ, minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed
    summanden = []
    set_commas=commas
    for _ in range(anzahl_zahlen):
        if smaller_or_equal == 1:
            commas = random.randint(0,set_commas) 
        num = 0
        while num == 0:
            num = get_random_number(minimum, maximum, commas)
        summanden.append(num)
    
    string  = add_summand(summanden[0])

    operators = []
    if enable_addition==True:
        operators.append('+')
    if enable_subtraction == True:
        operators.append('-')
    # if typ == "+":
    #     operators =  ['+']
    # elif typ == "-":
    #     operators =  ['-']
    # elif typ == "+-":
    #     operators = ['+', '-']
        
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

def create_single_example_ganze_zahlen_punkt(dict_all_settings_wizard):
    #minimum, maximum, commas, anzahl_summanden, smaller_or_equal
    anzahl_zahlen = dict_all_settings_wizard['anzahl_zahlen']
    minimum = dict_all_settings_wizard['minimum_spinbox']
    maximum = dict_all_settings_wizard['maximum_spinbox']
    commas = dict_all_settings_wizard['commas']
    smaller_or_equal = dict_all_settings_wizard['smaller_or_equal']

    factors = []
    set_commas=commas


    test_commas = commas
    for i in range(anzahl_zahlen):
        if smaller_or_equal == 1 and i+1 == anzahl_zahlen:
            commas = test_commas
            force_decimals = True
        else:
            commas = random.randint(0,test_commas)
            force_decimals = False
            

        #######
        # 
        if anzahl_zahlen==2:
            zero = False
        else:
            zero = 25    
        num = get_random_number(minimum, maximum, commas, zero_allowed=zero, force_decimals=force_decimals)
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
                if anzahl_zahlen > 2:
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

def create_single_example_ganze_zahlen_grundrechnungsarten(dict_all_settings_wizard):
    #minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed, show_brackets
    shorten_topic = dict_all_settings_wizard['dict_all_settings_wizard']
    if shorten_topic == 'ari_pos_ver':
        show_brackets = False
    else:
        show_brackets = True
    anzahl_summanden = dict_all_settings_wizard['anzahl_zahlen']
    minimum = dict_all_settings_wizard['minimum_spinbox']
    maximum = dict_all_settings_wizard['maximum_spinbox']
    commas = dict_all_settings_wizard['commas']
    smaller_or_equal = dict_all_settings_wizard['smaller_or_equal']
    brackets_allowed = dict_all_settings_wizard['brackets_allowed']

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

    return [numbers, solution, string] 

def index_to_letter(index):
    return chr(ord('a') + index)

def create_single_example_coordinate_system(dict_all_settings_wizard):
    #half_allowed, negative_allowed
    half_allowed = dict_all_settings_wizard['half_allowed_coord']
    negative_allowed = dict_all_settings_wizard['negative_allowed_coord']
    if negative_allowed == True:
        minimum = -5
    else:
        minimum = 0
    
    dict_of_points = {}

    i=0
    while i < 6:
        x = get_random_number(minimum, 5, zero_allowed=True,half_allowed=half_allowed)
        if x == 0: 
            y = get_random_number(minimum, 4, zero_allowed=True,half_allowed=half_allowed)
        elif x==5:
            y = get_random_number(minimum, 5, zero_allowed=False,half_allowed=half_allowed)
        else:
            y = get_random_number(minimum, 5, zero_allowed=True,half_allowed=half_allowed)
        if (x,y) not in list(dict_of_points.values()):
            dict_of_points[index_to_letter(i).upper()]=(x,y)
            i+=1

    _string = ""
    for all in dict_of_points:
        if _string != "":
            _string += ", "
        _string += f"{all} = ({dict_of_points[all][0]}|{dict_of_points[all][1]})"


    return [dict_of_points,0,_string] 

def convert_to_fractions(string):
    _temp = re.findall('[0-9.]+', string)


    for all in _temp:
        frac= Fraction(all).limit_denominator()

        if frac.denominator != 1:
            string = string.replace(all, f"{frac.numerator}/{frac.denominator}")
        else:
            string = string.replace(all, str(frac))
    
    return string

def create_single_example_binomische_formeln(dict_all_settings_wizard):
    #, coef_a,coef_b,exp_x,exp_y, exponent, binoms_direction_index, fractions_allowed, variable_1, variable_2
    binomials_types = [dict_all_settings_wizard['binomials_type_1'], dict_all_settings_wizard['binomials_type_2'], dict_all_settings_wizard['binomials_type_3']]
    coef_a_checked = dict_all_settings_wizard['binomials_checkbox_a']
    coef_a_min = dict_all_settings_wizard['binomials_minimum_a']
    coef_a_max = dict_all_settings_wizard['binomials_maximum_a']
    coef_b_checked = dict_all_settings_wizard['binomials_checkbox_b']
    coef_b_min = dict_all_settings_wizard['binomials_minimum_b']
    coef_b_max = dict_all_settings_wizard['binomials_maximum_b']
    expo_m_min = dict_all_settings_wizard['binomials_minimum_m']
    expo_m_max = dict_all_settings_wizard['binomials_maximum_m']
    expo_y_checked = dict_all_settings_wizard['binomials_checkbox_y']
    expo_n_min = dict_all_settings_wizard['binomials_minimum_n']
    expo_n_max = dict_all_settings_wizard['binomials_maximum_n']
    fractions_allowed = dict_all_settings_wizard['binomials_fractions_allowed']
    exponent = dict_all_settings_wizard['binomials_exponent']
    binoms_direction_index = dict_all_settings_wizard['binomials_direction_index']
    variable_1 = dict_all_settings_wizard['binomials_variable_1']
    variable_2 = dict_all_settings_wizard['binomials_variable_2']

    A, B = symbols("{} {}".format("A", "B"))

    if fractions_allowed == True:
        if coef_a_checked == False:
            coef_1 = 1
        else:
            coef_1 = get_random_fraction(coef_a_min,coef_a_max)
        
        if coef_b_checked == False:
            coef_2 = 1
        else:
            coef_2 = get_random_fraction(coef_b_min,coef_b_max)
    else:
        if coef_a_checked == False:
            coef_1 = 1
        else:
            coef_1 = get_random_number(coef_a_min,coef_a_max)
        
        if coef_b_checked == False:
            coef_2 = 1
        else:
            coef_2 = get_random_number(coef_b_min,coef_b_max)


    # if exp_x == [0,0]:
    #     exponent_x = 0
    # else:    
    exponent_x = get_random_number(expo_m_min,expo_m_max)
    if exponent_x ==1:
        exponent_x = ""
    else:
        exponent_x = f"**{exponent_x}"

    if expo_y_checked == False:
        exponent_y = 0
    else:
        exponent_y = get_random_number(expo_n_min,expo_n_max)
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

    if index == 3:
        choice = random.choice([0,1]) #edit to 0,1

        string = f"{binom_string} = {solution_string}"

        # if choice == 1:
        #     solution_string = f"{solution_string} = {binom_string}"
        # else:
        #     solution_string = string
        
        split_string = split_binomial_expression(string)
        random_blanks = choose_random_blanks(split_string)

        print(split_string)
        print(random_blanks)

        
        solution_string = []
        for i in random_blanks:
            string = string.replace(split_string[i], "_", 1)
            solution_string.append(split_string[i])

        if choice == 0:
            binom_string = string


        elif choice == 1:
            split_equation = string.split(" = ")

            string = f"{split_equation[1]} = {split_equation[0]}"
            binom_string = string

            if len(split_string)==5:
                first_element = solution_string.pop(0)
                solution_string.append(first_element)

            elif len(split_string)==6:
                solution_string.insert(0, solution_string.pop())

        binom_string = binom_string.replace("_","\\rule{1cm}{0.3pt}")

    else:
        solution_string = re.sub("([0-9]+)/([0-9]+)",r"\\frac{\1}{\2}", solution_string)
        solution_string = solution_string.replace('\xb7', '\cdot ')
        solution_string  = f"${solution_string}$"



    binom_string = re.sub("([0-9]+)/([0-9]+)",r"\\frac{\1}{\2}", binom_string)
    binom_string = binom_string.replace('\xb7', '\cdot ')
    

    return [f"${binom_string}$",solution_string, string]

def split_binomial_expression(expression):
    pattern = r'[+\-()=]'
    segments = re.split(pattern, expression)
    segments = [segment.strip() for segment in segments if segment.strip()]

    filtered_segments = [x for x in segments if not re.fullmatch(r'\^\d+', x)]
    
    # pattern = r'([0-9/a-z]+\^\d+ [+-]|\d*(?:/\d)*[a-z]+ [+-]|^\^\d+(?:/\d)*[a-z]*)'

    # result = re.findall(pattern, expression)

    return filtered_segments

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

def get_random_fraction(min, max):
    numerator = get_random_number(min, max)
    denominator = get_random_number(min, max) 
    # denominator = get_random_number(numerator, max)

    return Fraction("{0}/{1}".format(numerator, abs(denominator)))

def check_for_duplicate(new_example, list_of_examples):
    list_of_solutions = []
    for all in list_of_examples:
        list_of_solutions.append(all[-2])
    # print(list_of_solutions)

    if new_example[-2] in list_of_solutions:
        return True
    else:
        return False

def create_examples_all_topics(spec_function, dict_all_settings_wizard, single_example=False): #spec_function, 
    if single_example == True:
        new_example = spec_function(dict_all_settings_wizard)
        return new_example   
    list_of_examples = []

    i=0
    max_limit_counter =0
    while i<dict_all_settings_wizard['examples']:
        new_example = spec_function(dict_all_settings_wizard) # minimum, minimum_index, maximum, maximum_index, general_direction_index
        duplicate = check_for_duplicate(new_example, list_of_examples)
        
        if duplicate == False:
            list_of_examples.append(new_example)
            i +=1
        else:
            max_limit_counter +=1
            if max_limit_counter > 99:
                list_of_examples.append(new_example)
                i +=1

    return list_of_examples 


# def create_list_of_examples_stellenwert(examples, minimum, minimum_index, maximum, maximum_index, general_direction_index):
#     list_of_examples = []

#     i=0
#     max_limit_counter =0
#     while i<examples:
#         new_example = create_single_example_stellenwert(minimum, minimum_index, maximum, maximum_index, general_direction_index)
#         duplicate = check_for_duplicate(new_example, list_of_examples)
        
#         if duplicate == False:
#             list_of_examples.append(new_example)
#             i +=1
#         else:
#             max_limit_counter +=1
#             if max_limit_counter > 99:
#                 list_of_examples.append(new_example)
#                 i +=1

#     return list_of_examples     


# def create_list_of_examples_roman_numerals(examples, roman_max, maximum_index, general_direction_index):
#     list_of_examples = []


#     i=0
#     max_limit_counter =0
#     while i<examples:
#         new_example = create_single_example_roman_numerals(roman_max, maximum_index, general_direction_index)
#         duplicate = check_for_duplicate(new_example, list_of_examples)
        
#         if duplicate == False:
#             list_of_examples.append(new_example)
#             i +=1
#         else:
#             max_limit_counter +=1
#             if max_limit_counter > 99:
#                 list_of_examples.append(new_example)
#                 i +=1

#     return list_of_examples


# def create_list_of_examples_number_line(examples, starting_value, steps, subticks, setting_decimal_fraction):
#     list_of_examples = []


#     i=0
#     max_limit_counter =0
#     while i<examples:
#         new_example = create_single_example_number_line(starting_value, steps, subticks,setting_decimal_fraction)
#         duplicate = check_for_duplicate(new_example, list_of_examples)
        
#         if duplicate == False:
#             list_of_examples.append(new_example)
#             i +=1
#         else:
#             max_limit_counter +=1
#             if max_limit_counter > 99:
#                 list_of_examples.append(new_example)
#                 i +=1

#     return list_of_examples    

# def create_list_of_examples_primenumbers(dict_all_settings_wizard):
#     list_of_examples = []

#     i=0
#     max_limit_counter =0
#     while i<examples:
#         new_example = create_single_example_primenumbers(minimum, maximum, maximum_prime, display_as_powers)
#         duplicate = check_for_duplicate(new_example, list_of_examples)
        
#         if duplicate == False:
#             list_of_examples.append(new_example)
#             i +=1
#         else:
#             max_limit_counter +=1
#             if max_limit_counter > 99:
#                 list_of_examples.append(new_example)
#                 i +=1

#     return list_of_examples

# def create_list_of_examples_ggt(examples, anzahl_zahlen, minimum, maximum, ggt_1_checked):
#     list_of_examples = []

#     i=0
#     max_limit_counter =0
#     while i<examples:
#         new_example = create_single_example_ggt(anzahl_zahlen, minimum, maximum, ggt_1_checked)
#         duplicate = check_for_duplicate(new_example, list_of_examples)
        
#         if duplicate == False:
#             list_of_examples.append(new_example)
#             i +=1
#         else:
#             max_limit_counter +=1
#             if max_limit_counter > 99:
#                 print('max reached')
#                 list_of_examples.append(new_example)
#                 i +=1

#     return list_of_examples    

# def create_list_of_examples_addition(examples, minimum, maximum, commas, anzahl_summanden, smaller_or_equal):
#     list_of_examples = []

#     i=0
#     max_limit_counter =0
#     while i<examples:
#         new_example = create_single_example_addition(minimum, maximum, commas, anzahl_summanden, smaller_or_equal)
#         duplicate = check_for_duplicate(new_example, list_of_examples)
        
#         if duplicate == False:
#             list_of_examples.append(new_example)
#             i +=1
#         else:
#             max_limit_counter +=1
#             if max_limit_counter > 99:
#                 list_of_examples.append(new_example)
#                 i +=1

#     return list_of_examples

# def create_list_of_examples_subtraction(examples, minimum, maximum, commas, negative_solutions_allowed, anzahl_subtrahenden,smaller_or_equal):
#     list_of_examples = []


#     i=0
#     max_limit_counter =0
#     while i<examples:
#         new_example = create_single_example_subtraction(minimum, maximum, commas, negative_solutions_allowed,anzahl_subtrahenden, smaller_or_equal)
#         duplicate = check_for_duplicate(new_example, list_of_examples)
        
#         if duplicate == False:
#             list_of_examples.append(new_example)
#             i +=1
#         else:
#             max_limit_counter +=1
#             if max_limit_counter > 99:
#                 list_of_examples.append(new_example)
#                 i +=1

#     return list_of_examples

# def create_list_of_examples_multiplication(examples, minimum_1, maximum_1, commas_1, smaller_or_equal_1, minimum_2, maximum_2, commas_2, smaller_or_equal_2):
#     list_of_examples = []

#     i=0
#     max_limit_counter =0
#     while i<examples:
#         new_example = create_single_example_multiplication(minimum_1, maximum_1, commas_1, smaller_or_equal_1,minimum_2, maximum_2, commas_2, smaller_or_equal_2)
#         duplicate = check_for_duplicate(new_example, list_of_examples)
        
#         if duplicate == False:
#             list_of_examples.append(new_example)
#             i +=1
#         else:
#             max_limit_counter +=1
#             if max_limit_counter > 99:
#                 list_of_examples.append(new_example)
#                 i +=1

#     return list_of_examples

# def create_list_of_examples_division(examples, minimum_1, maximum_1, minimum_2, maximum_2, commas_div, smaller_or_equal_div, commas_result, smaller_or_equal_result, output_type):
#     list_of_examples = []

#     i=0
#     max_limit_counter =0
#     while i<examples:
#         new_example = create_single_example_division(minimum_1, maximum_1, minimum_2, maximum_2, commas_div, smaller_or_equal_div, commas_result,smaller_or_equal_result, output_type)
#         duplicate = check_for_duplicate(new_example, list_of_examples)
        
#         if duplicate == False:
#             list_of_examples.append(new_example)
#             i +=1
#         else:
#             max_limit_counter +=1
#             if max_limit_counter > 99:
#                 list_of_examples.append(new_example)
#                 i +=1

#     return list_of_examples


# def create_list_of_examples_ganze_zahlen(typ, examples, minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed, show_brackets):
#     list_of_examples = []


#     i=0
#     max_limit_counter =0
#     while i<examples:
#         if typ == '+' or typ == '-' or typ == '+-':
#             new_example = create_single_example_ganze_zahlen_strich(typ, minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed)
#         elif typ == '*:':
#             new_example = create_single_example_ganze_zahlen_punkt(minimum, maximum, commas, anzahl_summanden, smaller_or_equal)
#         elif typ == '+-*:': 
#             new_example = create_single_example_ganze_zahlen_grundrechnungsarten(minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed, show_brackets)

#         duplicate = check_for_duplicate(new_example, list_of_examples)
        
#         if duplicate == False:
#             list_of_examples.append(new_example)
#             i +=1
#         else:
#             max_limit_counter +=1
#             if max_limit_counter > 99:
#                 list_of_examples.append(new_example)
#                 i +=1


#     return list_of_examples

# def create_list_of_examples_coordinate_system(examples, half_allowed, negative_allowed):
#     list_of_examples = []

#     i=0
#     max_limit_counter =0
#     while i<examples:
#         new_example = create_single_example_coordinate_system(half_allowed, negative_allowed)
#         duplicate = check_for_duplicate(new_example, list_of_examples)
        
#         if duplicate == False:
#             list_of_examples.append(new_example)
#             i +=1
#         else:
#             max_limit_counter +=1
#             if max_limit_counter > 99:
#                 list_of_examples.append(new_example)
#                 i +=1

#     return list_of_examples

# def create_list_of_examples_binomische_formeln(examples, binomials_types, a,b,x,y, exponent, binoms_direction_index, fractions_allowed, variable_1, variable_2):
#     list_of_examples = []

#     i=0
#     max_limit_counter =0
#     while i<examples:
#         new_example = create_single_example_binomische_formeln(binomials_types, a,b,x,y, exponent, binoms_direction_index, fractions_allowed, variable_1, variable_2)
#         duplicate = check_for_duplicate(new_example, list_of_examples)
        
#         if duplicate == False:
#             list_of_examples.append(new_example)
#             i +=1
#         else:
#             max_limit_counter +=1
#             if max_limit_counter > 99:
#                 list_of_examples.append(new_example)
#                 i +=1


#     return list_of_examples


def get_number_of_decimals(x):
    num = D('{}'.format(x)).normalize()
    num = remove_exponent(num)
    num = abs(num.as_tuple().exponent)
    return num


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

def create_latex_string_stellenwert(content, example):
    _string = example[-1]

    _string = _string.split(" = ")

    string_0 = _string[0].replace(".","\,")
    string_1 = _string[1].replace(".","\,")
    content += f"\\task {string_0} = \\antwort{{{string_1}}}"

    return content

def create_latex_string_roman_numerals(content, example):
    _string = example[-1]
    _string = _string.split(" = ")
    content += f"\\task {_string[0]} = \\antwort{{{_string[1]}}}"

    return content

def formatNumber(num):
  if num % 1 == 0:
    return int(num)
  else:
    return num

def create_latex_string_number_line(content, example, starting_value, steps, subticks, dot_style_index, geometry_direction_index):
    steps = formatNumber(steps)
    # print(example)
    if starting_value==0:
        arrows = "->"
        beginning_picture = starting_value-steps/2
        ending_picture = starting_value+15*steps
        beginning = starting_value
        ending = starting_value+15*steps
        Ox= None
        string_Ox = ""
    elif starting_value<0:
        arrows = "<->"
        beginning_picture = starting_value-steps/2
        ending_picture = starting_value+15*steps
        beginning = starting_value-steps/2
        ending = starting_value+15*steps
        Ox= None
        string_Ox= ""
    elif starting_value>0:
        arrows = "->"
        beginning_picture = -steps/2
        ending_picture = 15*steps
        beginning = 0
        ending = ending_picture
        Ox = starting_value
        string_Ox= f",Ox={formatNumber(starting_value)}"


    pstricks_code_dots = create_pstricks_code_dots(example, dot_style_index, geometry_direction_index, xlabel_padding=-steps/10, ylabel_padding=0.2, Ox=Ox)

    if geometry_direction_index == 1:
        pstricks_code_dots = f"\\antwort{{{pstricks_code_dots}}}" 

    
    pstricks_code = f"""
\psset{{xunit={1/steps}cm,yunit=1.0cm,dotstyle=x,dotsize=6pt 0,linewidth=1pt,arrowsize=3pt 2}}
\\begin{{pspicture*}}({beginning_picture},-1)({ending_picture},1)
\psaxes[labelFontSize=\scriptstyle, comma, yAxis=false {string_Ox},Dx={steps},ticksize=-5pt 0,subticks={subticks}, subtickcolor=black]{{{arrows}}}(0,0)({beginning},-1)({ending},1)
{pstricks_code_dots}
\end{{pspicture*}}
"""
    # print(pstricks_code)
    
    string_coordinates = ""
    for i, all in enumerate(example[0]):
        coordinates = example[0][all]
        if i != 0:
            string_coordinates += " \hfil "

        x_coordinate = str(coordinates[0]).replace(".",",")
        if geometry_direction_index == 0:
            string_coordinates += f"${all} = \\antwort[\\rule{{1cm}}{{0.3pt}}]{{{x_coordinate}}}$"
        else:
            string_coordinates += f"${all} = {x_coordinate}$"


    content += f"\\task\n{pstricks_code}\n{string_coordinates}\n"
#     \psdots(250.,0.)
# \\rput(250,0.4){{$A$}}
# \psdots(370.,0.)
# \\rput(370,0.4){{$B$}}
    return content

def expand_powers(powers):
    result = []
    for all in powers:
        x = all.split("^")
        if len(x)==1:
            result.append(x[0])
        else:
            result.extend(x[0] for i in range(int(x[1])))
    return result

def create_latex_string_primenumbers(content, example, solution_type, powers_enabled):

    solution = example[1].replace("$","")
    content += f"\\task ${example[0]} = "

    content += f'\\antwort{{{solution}}}$'
    
    if solution_type == 1:
        list_of_factors = solution.split("\cdot")
        if powers_enabled == True:
            list_of_factors = expand_powers(list_of_factors)

        content += "\n\n \\antwort{{$\\begin{array}{c|c}\n"
        value = example[0]
        for primefactor in list_of_factors:
            content+= f"{value} & {primefactor} \\\\ \n"
            value = int(value/int(primefactor))
        
        content += "\\end{array}$}}\n"
        
    return content

def create_latex_string_addition(content, example, ausrichtung):
    summanden = example[0]
    
    max_decimal=0
    for all in summanden:
        decimals = get_number_of_decimals(all)
        if decimals > max_decimal:
            max_decimal = decimals    

    if ausrichtung == 0:
        content += "\\task \\begin{tabular}[t]{rr}\n"

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
        content += "\\task ${0}".format(str(summanden[0]).replace(".",","))

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
        \\task \\begin{{tabular}}[t]{{rr}}
        & ${0}{3}$ \\\\
        & $-{1}{4}$ \\\\ \hline
        &\\antwort{{${2}$}}
        \end{{tabular}}\n
        """.format(str(subtrahenden[0]).replace(".",","), str(subtrahenden[1]).replace(".",","),str(example[-2]).replace(".",","), phantom_1, phantom_2)
    elif ausrichtung == 1:
        content += "\\task ${0}".format(str(subtrahenden[0]).replace(".",","))

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
\\task $\\begin{{array}}[t]{{l}}
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

        if part_divide == "":
            part_divide = "0"


        differenz = eval(part_divide)-temp_solution
        differenz = round(differenz, 10)
        end_index +=1

        if i == len(str_solution)-1:
            next_digit = ""
            next_digit_string = next_digit
        else:            
            try:
                if str(dividend)[end_index].isnumeric():
                    next_digit = str(dividend)[end_index]
                    next_digit_string = next_digit
                else:
                    end_index +=1
                    next_digit = str(dividend)[end_index]
                    next_digit_string = f"\;{next_digit}"       
            except IndexError:
                next_digit = "0"
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

    if solution_type == 1:
        content += f"""
        \\task $\\begin{{array}}[t]{{l}}
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

        content += "\end{array}$\n\n"


    else:
        content += "\\task ${0} : {1} = \\antwort[\\vspace{{1.5cm}}]{{{2}}}${3}\n\n".format(str(example[0]).replace(".",","),str(example[1]).replace(".",","),solution, rest)


    return content


def create_latex_string_ganze_zahlen(content, example):
    equation = example[-1]
    
    x,y = equation.split(" = ")
    
    temp_content = "\\task ${0} = \\antwort{{{1}}}$\n\n".format(x.replace(".",","),y.replace(".",","))
    temp_content = temp_content.replace('\xb7', '\cdot')
    content += temp_content
    return content

def create_pstricks_code_dots(example, dot_style_index, coordinates_direction_index, xlabel_padding = 0.1, ylabel_padding = 0.1, Ox=None):
    if dot_style_index==0:
        dot_style = "*"
    elif dot_style_index==1:
        dot_style = "x"

    if coordinates_direction_index==1:
        color = ",linecolor=red"
    else:
        color = ""
    dict_dots = example[0]
    _string = ""

    if Ox != None:
        xcorrection = Ox
    else:
        xcorrection = 0

    for all in dict_dots:
        xcoord = float(dict_dots[all][0])-float(xcorrection)+float(xlabel_padding)
        ycoord = float(dict_dots[all][1])+float(ylabel_padding)
        _string += f"\psdots[dotstyle={dot_style}{color}]({dict_dots[all][0]-float(xcorrection)},{dict_dots[all][1]})\n\\rput[bl]({xcoord},{ycoord}){{${all}$}}\n"        

    return _string

def minimal_coordinate_system(half_allowed, negative_allowed, pstricks_code_dots, coordinates_direction_index):
    if half_allowed == True:
        multips_spacing = "0.5"
    else:
        multips_spacing = "1"

    if negative_allowed == True:
        xyunit = "0.75"
        pspicture_min = "-5.7"
        mulitps_2 = "-5.4"
        mulitps_1 = "-5"
        showorigin = "false"
        if half_allowed == True:
            mulitps_num = "21"
        else:
            mulitps_num = "11"

        
    else:
        xyunit = "0.8"
        pspicture_min = "-0.7"
        mulitps_2 = "0"
        mulitps_1 = "0"
        showorigin= "true"
        if half_allowed == True:
            mulitps_num = "11"
        else:
            mulitps_num = "7"
        

    if coordinates_direction_index == 1:
        pstricks_code_dots = f"\\antwort{{{pstricks_code_dots}}}"        

    pstricks_code = f"""
\psset{{xunit={xyunit}cm,yunit={xyunit}cm,algebraic=true,dimen=middle,dotstyle=o,dotsize=5pt 0,linewidth=1pt,arrowsize=3pt 2,arrowinset=0.25}}
\\begin{{pspicture*}}({pspicture_min},{pspicture_min})(5.5,5.5)
\multips(0,{mulitps_1})(0,{multips_spacing}){{{mulitps_num}}}{{\psline[linestyle=dashed,linecap=1,dash=1.5pt 1.5pt,linewidth=0.4pt,linecolor=darkgray]{{c-c}}({mulitps_2},0)(5.4,0)}}
\multips({mulitps_1},0)({multips_spacing},0){{{mulitps_num}}}{{\psline[linestyle=dashed,linecap=1,dash=1.5pt 1.5pt,linewidth=0.4pt,linecolor=darkgray]{{c-c}}(0,{mulitps_2})(0,5.4)}}
\psaxes[labelFontSize=\scriptstyle,xAxis=true,yAxis=true,Dx=1,Dy=1,ticksize=-2pt 0,subticks=0, showorigin={showorigin}]{{->}}(0,0)({mulitps_2},{mulitps_2})(5.5,5.5)[$x$,140] [$y$,-40]
\\begin{{scriptsize}}
{pstricks_code_dots}
\end{{scriptsize}}
\end{{pspicture*}}
    """
    return pstricks_code

def create_latex_coordinates(example, coordinates_direction_index):
    dict_dots = example[0]

    i = 0
    temp_string = ""
    for all in dict_dots:
        coordinates = dict_dots[all]
        xcoord = str(coordinates[0]).replace('.',',')
        ycoord = str(coordinates[1]).replace('.',',')
        if coordinates_direction_index == 0:
            xcoord = f'\\antwort[\\rule{{0.4cm}}{{0.3pt}}]{{{xcoord}}}'
            ycoord = f'\\antwort[\\rule{{0.4cm}}{{0.3pt}}]{{{ycoord}}}'

        if i==0:
            temp_string += f"${all} = ({xcoord}\mid {ycoord})$ &"
            i +=1
        elif i==1:
            temp_string += f"${all} = ({xcoord}\mid {ycoord})$ \\\\"
            i=0

    return temp_string

def create_latex_string_coordinate_system(content, example, half_allowed, negative_allowed,dot_style_index, coordinates_direction_index):
    pstricks_code_dots = create_pstricks_code_dots(example, dot_style_index, coordinates_direction_index)
    pstricks_code = minimal_coordinate_system(half_allowed, negative_allowed, pstricks_code_dots, coordinates_direction_index)
    latex_coordinates = create_latex_coordinates(example, coordinates_direction_index)

    content += f"""\\task\n{pstricks_code}\n
\centering\\renewcommand{{\\arraystretch}}{{1.2}}
\\begin{{tabular}}{{ll}}
{latex_coordinates}
\end{{tabular}}\n\n  
    """

    # \\begin{{multicols}}{2}
    # \\begin{{enumerate}}[$A$]
    # \item $= (3, 2)$
    # \item $= (3, 2)$
    # \item $= (3, 2)$
    # \item $= (3, 2)$
    # \item $= (3, 2)$
    # \item $= (3, 2)$
    # \end{{enumerate}}
    # \end{{multicols}}

    return content

def create_latex_string_binomische_formeln(content, example, binoms_direction_index):
    print(example)
    if binoms_direction_index==3:
        aufgabe = example[0]

        for _, solution in enumerate(example[1]):
            aufgabe = aufgabe.replace('\\rule{1cm}{0.3pt}', f'\\antwort[RULE]{{{solution}}}', 1)

        aufgabe = aufgabe.replace("RULE", "\\rule{1cm}{0.3pt}")
        aufgabe = re.sub("\^([0-9][0-9]+)",r"^{\1}", aufgabe)
        # for loesung in example[1]:
        #     aufgabe = aufgabe.replace("\\rule{1cm}{0.3pt}", f"\\antwort[\\rule{{1cm}}{{0.3pt}}]{{{loesung}}}",1)
        temp_content = f"\\task {aufgabe}\n\n"

    else:
        example_string = re.sub("([0-9]+)/([0-9]+)",r"\\frac{\1}{\2}", example[2])
        example_string = re.sub("\^([0-9][0-9]+)",r"^{\1}", example_string)

        aufgabe, loesung = example_string.split(" = ")

        temp_content = f"\\task ${aufgabe} = \\antwort{{{loesung}}}$\n\n"

    temp_content = temp_content.replace('\xb7', '\cdot ')

    content += temp_content

    return content


def create_latex_worksheet(
    order_of_examples,
    dict_of_examples,
    titel,
    arbeitsanweisung,
    fortlaufende_nummerierung,
    nummerierung,
    solution_type,
    ):

    if titel != False:
        content = "\section{{{0}}}\n\n".format(titel.replace('&', '\&'))
    else:
        content = ""

    if arbeitsanweisung != False:
        if arbeitsanweisung == True:
            arbeitsanweisung=""
        content += arbeitsanweisung

    for widget in order_of_examples:
        set_of_examples = dict_of_examples[widget]

    # for all in dict_of_examples.values():
        # index = set_of_examples['thema_index']
        shorten_topic = set_of_examples['shorten_topic']
        ausrichtung = set_of_examples['ausrichtung']
        columns = set_of_examples['spalten']
        binoms_direction_index=set_of_examples['binom_direction_index']
        
        if set_of_examples['instruction'] != None:
            content += f"\n\n{set_of_examples['instruction']}\n\n"



        starting_value = set_of_examples['number_line'][0]
        steps = set_of_examples['number_line'][1]
        subticks = set_of_examples['number_line'][2]

        powers_enabled = set_of_examples['primefactors'][0]

        half_allowed = set_of_examples['coordinate_system'][0]
        negative_allowed = set_of_examples['coordinate_system'][1]
        dot_style_index = set_of_examples['dotstyle_index']
        geometry_direction_index = set_of_examples['direction_index']

        content += f"\\begin{{tasks}}[label={nummerierung},resume={fortlaufende_nummerierung}, item-indent=0pt]({columns})\n\n"

        list_of_examples = set_of_examples['list_of_examples']
        # print(shorten_topic)
        for example in list_of_examples:
            if shorten_topic == 'ari_dar_ste':
                content = create_latex_string_stellenwert(content, example)
            elif shorten_topic == 'ari_dar_röm':
                content = create_latex_string_roman_numerals(content, example)
            elif shorten_topic == 'ari_dar_zah':
                content = create_latex_string_number_line(content, example, starting_value, steps, subticks, dot_style_index, geometry_direction_index)
            elif shorten_topic == 'ari_tei_pri':
                content = create_latex_string_primenumbers(content, example, solution_type, powers_enabled)
            # elif shorten_topic == 'ari_tei_ggt':
            #     content = create_latex_string_primenumbers(content, example, solution_type, powers_enabled)
            elif shorten_topic == 'ari_pos_add':
                content = create_latex_string_addition(content, example, ausrichtung)
            elif shorten_topic == 'ari_pos_sub':
                content = create_latex_string_subtraction(content, example, ausrichtung)
            elif shorten_topic == 'ari_pos_mul':
                content = create_latex_string_multiplication(content, example, solution_type)
            elif shorten_topic == 'ari_pos_div':
                content = create_latex_string_division(content, example, solution_type)
            elif (
                shorten_topic == 'ari_pos_ver' or 
                shorten_topic == 'ari_neg_add' or 
                shorten_topic == 'ari_neg_mul' or 
                shorten_topic == 'ari_neg_ver'):
                content = create_latex_string_ganze_zahlen(content, example)
            elif shorten_topic == 'geo_gru_koo':
                content = create_latex_string_coordinate_system(content, example, half_allowed, negative_allowed,dot_style_index, geometry_direction_index)
            elif shorten_topic == 'ter_bin':
                content = create_latex_string_binomische_formeln(content, example, binoms_direction_index)

        content += "\end{tasks}\n"

        # if columns > 1:
        #     content += "\end{multicols}\n"
        
        # content += f"\\vspace{{{item_spacing}cm}}\n\n"
     
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


    try:
        _list = random.sample(all_dummy_solutions, k=10) #choices
    except ValueError:
        _list = []
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


    # coordinates = solution_pixels
    # i=0
    # while i < 10:
    #     distract_pixel = random.choice(list_all_pixels)
    #     if distract_pixel not in solution_pixels.keys():
    #         while True:
    #             distract_result = get_random_solution(self)[-2]
                   
    #             if distract_result not in coordinates.values():
    #                 break

    #         coordinates[distract_pixel] = False
    #         i +=1
    #     # possible_option = False

    # l = list(coordinates.items())
    # random.shuffle(l)
    # shuffled_coordinates = dict(l)

    # return shuffled_coordinates


# def get_random_solution(self):
#     thema = self.get_current_topic_wizard()
#     # thema_index = self.total_list_of_topics_wizard.index(thema)
#     shorten_topic = self.shorten_topic(thema)

#     dict_all_settings_wizard = self.get_all_settings_wizard(shorten_topic)

#     print(dict_all_settings_wizard)

#     if shorten_topic == 'ari_dar_ste':
#         # minimum = self.combobox_zahlenbereich_2.currentIndex()
#         # minimum_index = self.combobox_zahlenbereich_2_leq.currentIndex()
#         # maximum = self.combobox_zahlenbereich_1.currentIndex()
#         # maximum_index = self.combobox_zahlenbereich_1_leq.currentIndex()

#         # commas = self.spinbox_kommastellen_wizard.value()
#         # smaller_or_equal = self.combobox_kommastellen_wizard.currentIndex()
#         distract_result = create_single_example_stellenwert(dict_all_settings_wizard) #

#     elif shorten_topic == 'ari_dar_röm':
#         # roman_max = self.combobox_zahlenbereich_1.currentText()          
#         # maximum_index = self.combobox_zahlenbereich_1_leq.currentIndex()

#         distract_result = create_single_example_roman_numerals(dict_all_settings_wizard)

#     elif shorten_topic == 'ari_dar_zah':
#         # starting_value = self.spinbox_zahlenbereich_startingvalue.value()
#         # steps = self.spinbox_zahlenbereich_steps.value()
#         # subticks = self.spinbox_zahlenbereich_subticks.value()+1

#         distract_result = create_single_example_number_line(dict_all_settings_wizard)

#     elif shorten_topic == 'ari_tei_pri':
#         # minimum = self.spinbox_zahlenbereich_minimum.value()
#         # maximum = self.spinbox_zahlenbereich_maximum.value()
#         # maximum_prime = self.spinbox_maximum_prime.value()
#         # display_as_powers = self.checkbox_prime_powers.isChecked()

#         distract_result = create_single_example_primenumbers(dict_all_settings_wizard)

#     elif shorten_topic == 'ari_pos_add':
#         # minimum = self.spinbox_zahlenbereich_minimum.value()
#         # maximum = self.spinbox_zahlenbereich_maximum.value()
#         # commas = self.spinbox_kommastellen_wizard.value()
#         # anzahl_summanden = self.spinBox_zahlenbereich_anzahl_wizard.value()
#         # smaller_or_equal = self.combobox_kommastellen_wizard.currentIndex()
#         distract_result = create_single_example_addition(dict_all_settings_wizard)


#     elif shorten_topic == 'ari_pos_sub':
#         # minimum = self.spinbox_zahlenbereich_minimum.value()
#         # maximum = self.spinbox_zahlenbereich_maximum.value()
#         # commas = self.spinbox_kommastellen_wizard.value()
#         # smaller_or_equal = self.combobox_kommastellen_wizard.currentIndex()
#         # anzahl_subtrahenden = self.spinBox_zahlenbereich_anzahl_wizard.value()
#         distract_result = create_single_example_subtraction(dict_all_settings_wizard)

    
#     elif shorten_topic == 'ari_pos_mul':
#         # minimum_1 = self.spinBox_first_number_min.value()
#         # maximum_1 = self.spinBox_first_number_max.value()
#         # commas_1 = self.spinBox_first_number_decimal.value()
#         # smaller_or_equal_1 = self.combobox_first_number_decimal.currentIndex()
#         # minimum_2 = self.spinBox_second_number_min.value()
#         # maximum_2 = self.spinBox_second_number_max.value()
#         # commas_2 = self.spinBox_second_number_decimal.value()
#         # smaller_or_equal_2 = self.combobox_second_number_decimal.currentIndex()
#         distract_result = create_single_example_multiplication(dict_all_settings_wizard)


#     elif shorten_topic == 'ari_pos_div':
#         # minimum_1 = self.spinbox_dividend_min_wizard.value()
#         # maximum_1 = self.spinbox_dividend_max_wizard.value()
#         # minimum_2 = self.spinbox_divisor_min_wizard.value()
#         # maximum_2 = self.spinbox_divisor_max_wizard.value()
#         # commas_div = self.spinBox_divisor_kommastellen_wizard.value()
#         # smaller_or_equal_div = self.combobox_divisor_kommastelle_wizard.currentIndex()
#         # commas_result = self.spinbox_ergebnis_kommastellen_wizard.value()
#         # smaller_or_equal_result = self.combobox_ergebnis_kommastellen_wizard.currentIndex()
#         # if self.combobox_dividend_wizard.currentIndex()==1:
#         #     output_type = 2    
#         # elif self.radioButton_division_ohne_rest.isChecked():
#         #     output_type = 0
#         # elif self.radioButton_division_rest.isChecked():
#         #     output_type = 1       
#         distract_result = create_single_example_division(dict_all_settings_wizard)


#     elif (
#         shorten_topic == 'ari_pos_ver' or 
#         shorten_topic == 'ari_neg_add' or 
#         shorten_topic == 'ari_neg_mul' or 
#         shorten_topic == 'ari_neg_ver'
#         ):
#         minimum = self.spinbox_zahlenbereich_minimum.value()
#         maximum = self.spinbox_zahlenbereich_maximum.value()
#         commas = self.spinbox_kommastellen_wizard.value()
#         smaller_or_equal = self.combobox_kommastellen_wizard.currentIndex()
#         anzahl_summanden = self.spinBox_zahlenbereich_anzahl_wizard.value()
#         brackets_allowed = self.checkbox_allow_brackets_wizard.isChecked()


#         if shorten_topic == 'ari_neg_add':
#             if self.checkbox_enable_addition.isChecked():
#                 typ = "+"
#             else:
#                 typ = ""
            
#             if self.checkbox_enable_subtraktion.isChecked():
#                 typ += "-"

#             distract_result = create_single_example_ganze_zahlen_strich(typ, minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed)
#         elif shorten_topic == 'ari_neg_mul':
#             typ = '*:'
#             distract_result = create_single_example_ganze_zahlen_punkt(minimum, maximum, commas, anzahl_summanden, smaller_or_equal)
#         elif shorten_topic == 'ari_pos_ver' or 'ari_neg_ver':
#             if shorten_topic == 'ari_pos_ver':
#                 show_brackets = False
#             else:
#                 show_brackets = True
#             typ = '+-*:'
#             distract_result = create_single_example_ganze_zahlen_grundrechnungsarten(minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed, show_brackets)

#     elif shorten_topic == 'geo_gru_koo':
#         half_allowed = self.checkbox_coordinatesystem_zwischenwerte.isChecked()
#         negative_allowed = self.checkbox_coordinatesystem_negative_numbers.isChecked()
#         distract_result = create_single_example_coordinate_system(half_allowed, negative_allowed)

#     elif shorten_topic == 'ter_bin':
#         binomials_types = [self.cb_binoms_1.isChecked(), self.cb_binoms_2.isChecked(), self.cb_binoms_3.isChecked()]
        
#         if self.checkbox_binoms_a.isChecked():
#             a = [self.spinbox_binoms_a_min.value(), self.spinbox_binoms_a_max.value()]
#         else:
#             a = False
        
#         if self.checkbox_binoms_b.isChecked(): 
#             b = [self.spinbox_binoms_b_min.value(), self.spinbox_binoms_b_max.value()]
#         else:
#             b = False 

#         x = [self.spinbox_binoms_m_min.value(), self.spinbox_binoms_m_max.value()]


#         if self.checkbox_binoms_y.isChecked():
#             y = [self.spinbox_binoms_n_min.value(), self.spinbox_binoms_n_max.value()]
#         else:
#             y = False

#         fractions_allowed = self.checkbox_binoms_enable_fraction.isChecked()
#         exponent = self.spinbox_binoms_exponent.value()

#         variable_1 = self.combobox_choose_variables_1.currentText()
#         variable_2 = self.combobox_choose_variables_2.currentText()


#         distract_result = create_single_example_binomische_formeln(binomials_types, a,b,x,y, exponent, self.binoms_direction_index, fractions_allowed, variable_1, variable_2)
#     return distract_result

def create_nonogramm(nonogram, coordinates_nonogramm, spalten=3):

    if spalten > 1:
        begin_multicols = f"\\begin{{multicols}}{{{spalten}}}"
        end_multicols = "\end{multicols}"
    else:
        begin_multicols = ""
        end_multicols = ""

    nonogram_name = nonogram.split("_")[0].replace("&","\&").title()
    content = f"""\n\\vfill\n\\fontsize{{12}}{{14}}\selectfont
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
        elif type(coordinates_nonogramm[all][1])==list:
            result = ", ".join(coordinates_nonogramm[all][1])
            result = f"${result}$"
        else:
            result = coordinates_nonogramm[all][1]
        
        if coordinates_nonogramm[all][0] == True:
            result = "\\antwort[{0}]{{{0}}}".format(result)
        
        # elif coordinates_nonogramm[all][0] == False:
        #     result = result
        
        content += f"\item[\\fbox{{\parbox{{15pt}}{{\centering {all}}}}}] {result}\n".replace(".",",") 
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
