from functools import reduce
from operator import is_
from pickletools import decimalnl_long
import random
from math import floor, ceil
# import os
# from config_start import path_localappdata_lama, path_programm
import decimal
import re

from create_nonograms import nonogramm_empty, all_nonogramms, list_all_pixels
# import subprocess
# from tex_minimal import tex_preamble, tex_end
# from create_pdf import create_pdf, open_pdf_file, build_pdf_file

dict_widgets_wizard = {
    'Addition' : [
        'self.groupBox_ausrichtung_wizard',
        'self.groupBox_zahlenbereich_minimum',
        'self.groupBox_zahlenbereich_maximum',
        'self.groupBox_kommastellen_wizard',
        'self.groupBox_zahlenbereich_anzahl',
        ],
    'Subtraktion' : [
        'self.groupBox_ausrichtung_wizard',
        'self.groupBox_zahlenbereich_minimum',
        'self.groupBox_zahlenbereich_maximum',
        'self.groupBox_kommastellen_wizard',
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
    ],
    'Verbindung der Grundrechnungsarten': [
        'self.groupBox_zahlenbereich_minimum',
        'self.groupBox_zahlenbereich_maximum',
        # 'self.groupBox_kommastellen_wizard',
        'self.groupBox_zahlenbereich_anzahl',
        'self.checkbox_allow_brackets_wizard',        
    ],
    'Ganze Zahlen (Addition & Subtraktion)': [
        'self.groupBox_zahlenbereich_minimum',
        'self.groupBox_zahlenbereich_maximum',
        'self.groupBox_kommastellen_wizard',
        'self.groupBox_zahlenbereich_anzahl',
        'self.checkbox_allow_brackets_wizard',        
    ],
    'Ganze Zahlen (Multiplikation & Division)': [
        'self.groupBox_zahlenbereich_minimum',
        'self.groupBox_zahlenbereich_maximum',
        'self.groupBox_kommastellen_wizard',
        'self.groupBox_zahlenbereich_anzahl',
        # 'self.checkbox_allow_brackets_wizard',        
    ],
    'Ganze Zahlen (Grundrechnungsarten)': [
        'self.groupBox_zahlenbereich_minimum',
        'self.groupBox_zahlenbereich_maximum',
        'self.groupBox_kommastellen_wizard',
        'self.groupBox_zahlenbereich_anzahl',
        'self.checkbox_allow_brackets_wizard',        
    ],
}   

themen_worksheet_wizard = list(dict_widgets_wizard.keys())

D = decimal.Decimal


def get_random_number(min, max, decimal=0, zero_allowed=False):
    if not isinstance(zero_allowed, bool):
        zero_allowed = random_switch(zero_allowed)

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
        result = get_random_number(result_min, result_max, commas_result)

        dividend = result*divisor

        result = str(result)

    string = "{0} : {1} = {2}".format(str(dividend).replace(".",","),str(divisor).replace(".",","),result.replace(".",","))

    return [dividend,divisor,result, string]

def add_summand(s):
    if s>0:
        return "(+{})".format(s)
    elif s==0:
        return "{}".format(s)
    else:
        return "({})".format(s)

def random_switch(p=50):
    return random.randrange(100) < p

def create_single_example_ganze_zahlen_strich(minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed):
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

    operation = ['+', '-']
    bracket_open = False
    waiter = False

    for all in summanden[1:]:
        if brackets_allowed == True and random_switch(70) == True and waiter==False:
            if bracket_open == False:
                string +=random.choice(operation) + '['
                bracket_open = True
                waiter = True
            elif bracket_open == True:
                string +=']' + random.choice(operation) 
                bracket_open = False
                waiter = False  
        else:
            string += random.choice(operation)
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


def create_division_pair(factor_1, factor_2):
    dividend = factor_1*factor_2
    return "{}:{}".format(add_summand(dividend), add_summand(factor_1))

def create_single_example_ganze_zahlen_punkt(minimum, maximum, commas, anzahl_summanden, smaller_or_equal):
    factors = []
    set_commas=commas
    for _ in range(anzahl_summanden):
        if smaller_or_equal == 1:
            commas = random.randint(0,set_commas) 

        num = get_random_number(minimum, maximum, commas, 25)
        factors.append(num)


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
                string = "[" + create_division_pair(division_pair, all) + "]"
                division_pair = None
                continue
            else:
                if i < len(factors[1:])-1:
                    string += '\xb7'
                    division_pair = all
                elif len(factors)==2:
                    string = create_division_pair(factors[0], all) 
                else:
                    string += '\xb7' + add_summand(all)            
        else:
            string += operation

            string += add_summand(all)

    solution = eval(string.replace('[','(').replace(']',')').replace('\xb7','*').replace(':','/'))
    solution = D("{:.{prec}f}".format(solution, prec=set_commas))

    if solution == 0:
        solution = 0
    string = "{0} = {1}".format(string.replace(".",","), str(solution).replace(".",","))

    return [factors, solution, string]     


def create_single_example_ganze_zahlen_grundrechnungsarten(minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed):
    numbers = []
    set_commas=commas
    for _ in range(anzahl_summanden):
        if smaller_or_equal == 1:
            commas = random.randint(0,set_commas) 

        num = get_random_number(minimum, maximum, commas, 25)
        numbers.append(num)


    string  = add_summand(numbers[0])

    operators = ['+', '-', '\xb7', ':']
    division_pair = None
    bracket_open = False
    waiter = False
    
    for i, all in enumerate(numbers[1:]):
        if division_pair != None:
            if division_pair == 0:
                division_pair = get_random_number(minimum, maximum, commas)    
            string += "[" + create_division_pair(division_pair, all) + "]"
            division_pair = None
            continue
        operation = random.choice(operators)
        if operation == ':':
            waiter = False
            rsp = random_switch()
            if i==0 and rsp == True:
                division_pair = numbers[0]
                if division_pair == 0:
                    division_pair = get_random_number(minimum, maximum, commas)
                string = "[" + create_division_pair(division_pair, all) + "]"
                division_pair = None
                continue
            else:
                if i < len(numbers[1:])-1:
                    string += '\xb7'
                    division_pair = all
                elif len(numbers)==2:
                    string = create_division_pair(numbers[0], all) 
                else:
                    string += '\xb7' + add_summand(all)            
        else:
            if brackets_allowed == True and random_switch(70) == True and waiter==False:
                if bracket_open == False:
                    string +=random.choice(operation) + '['
                    bracket_open = True
                    waiter = True
                elif bracket_open == True:
                    string +=']' + random.choice(operation) 
                    bracket_open = False
                    waiter = False  
            else:
                string += random.choice(operation)
                waiter = False           

            string += add_summand(all)

    if bracket_open == True:
        if waiter == True:
            index = string.rfind('[')
            string = string[:index] + string[index+1:]
        else:
            string +=']'


    solution = eval(string.replace('[','(').replace(']',')').replace('\xb7','*').replace(':','/'))
    solution = D("{:.{prec}f}".format(solution, prec=set_commas))

    if solution == 0:
        solution = 0
    string = "{0} = {1}".format(string.replace(".",","), str(solution).replace(".",","))
    return [numbers, solution, string] 



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

    # print(list_of_examples)
    return list_of_examples


def create_list_of_examples_ganze_zahlen(typ, examples, minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed):
    list_of_examples = []

    for _ in range(examples):
        if typ == 'strich':
            new_example = create_single_example_ganze_zahlen_strich(minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed)
        elif typ == 'punkt':
            new_example = create_single_example_ganze_zahlen_punkt(minimum, maximum, commas, anzahl_summanden, smaller_or_equal)
        elif typ == 'grundrechnungsarten': 
            new_example = create_single_example_ganze_zahlen_grundrechnungsarten(minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed)
        list_of_examples.append(new_example)

    # print(list_of_examples)
    return list_of_examples

def get_number_of_decimals(x):
    return abs(D('{}'.format(x)).as_tuple().exponent)

def create_latex_string_addition(content, example, ausrichtung):
    summanden = example[0]
    
    max_decimal=0
    for all in summanden:
        decimals = get_number_of_decimals(all)
        if decimals > max_decimal:
            max_decimal = decimals    

    if ausrichtung == 0:
        content += "\item \\begin{tabular}{rr}"

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
        

        content += " = \\antwort{{{0}}}$\n\\leer\n\n".format(str(example[-2]).replace(".",","))
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

        content += " = \\antwort{{{0}}}$\n\\leer\n\n".format(str(example[-2]).replace(".",","))
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


def create_latex_string_division(content, example):
    if "R " in str(example[2]):
        solution, rest = example[2].split("R ")
        solution = solution.replace(".",",")
        rest = "\n\n\\antwort{{R {}}}".format(rest)    
    else:
        solution = str(example[2]).replace(".",",")
        rest = ""

    content += "\item ${0} : {1} = \\antwort[\\vspace{{1.5cm}}]{{{2}}}${3}\n\\leer\n\n".format(str(example[0]).replace(".",","),str(example[1]).replace(".",","),solution, rest)
    
    return content


def create_latex_string_ganze_zahlen(content, example):
    equation = example[-1]
    
    x,y = equation.split(" = ")
    
    temp_content = "\item ${0} = \\antwort{{{1}}}$\n\\leer\n\n".format(x.replace(".",","),y.replace(".",","))
    temp_content = temp_content.replace('\xb7', '\cdot')
    content += temp_content
    return content

def create_latex_worksheet(list_of_examples,index, titel, columns, nummerierung, ausrichtung, solution_type=0):
    content = "\section{{{0}}}\n\n".format(titel.replace('&', '\&'))
    if columns > 1:
        content += "\\begin{{multicols}}{{{0}}}\n".format(columns)

    content += "\\begin{{enumerate}}[{0}]\n".format(nummerierung)

    for example in list_of_examples:
        if index == 0:
            content = create_latex_string_addition(content, example, ausrichtung)
        elif index == 1:
            content = create_latex_string_subtraction(content, example, ausrichtung)
        elif index == 2:
            content = create_latex_string_multiplication(content, example, solution_type)
        elif index == 3:
            content = create_latex_string_division(content, example)
        elif index == 5 or index == 6 or index ==7:
            content = create_latex_string_ganze_zahlen(content, example)


    content += "\end{enumerate}"

    if columns > 1:
        content += "\end{multicols}"

    return content


def get_all_pixels(content):
    return re.findall("[A-J][0-9]",content) 


def rechose_nonogramm(list_of_examples, nonogram):
    while len(list_of_examples) > len(all_nonogramms[nonogram]):
        nonogram = random.choice(list(all_nonogramms.keys()))

    return nonogram
        
def get_all_solution_pixels(list_of_examples):
    nonogram = random.choice(list(all_nonogramms.keys()))

    if len(list_of_examples) > len(all_nonogramms[nonogram]):
        nonogram = rechose_nonogramm(list_of_examples, nonogram)


    all_pixels_solution = all_nonogramms[nonogram]
    random.shuffle(all_pixels_solution)
    solution_pixels = {}

   

    for i, pixel in enumerate(all_pixels_solution):
        if i<len(list_of_examples):
            solution_pixels[pixel] =  list_of_examples[i][-2]
        else:
            solution_pixels[pixel] = True


    return nonogram, solution_pixels
    # for num, pixel in enumerate(all_pixels_solution):
    #     if num<examples:
    #         solution_pixels.append([pixel, True])
    #     else:
    #         return solution_pixels  


def replace_correct_pixels(content, coordinates_nonogramm):
    for pixel in list_all_pixels:
        if pixel in coordinates_nonogramm.keys():
            if coordinates_nonogramm[pixel] == False:
                content = content.replace(pixel, "")
            elif coordinates_nonogramm[pixel] == True:
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

def create_coordinates(self, solution_pixels):
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
        possible_option = False

    l = list(coordinates.items())
    random.shuffle(l)
    shuffled_coordinates = dict(l)

    return shuffled_coordinates


def get_random_solution(MainWindow):
    thema = MainWindow.comboBox_themen_wizard.currentText()

    if thema == 'Addition':
        minimum = MainWindow.spinbox_zahlenbereich_minimum.value()
        maximum = MainWindow.spinbox_zahlenbereich_maximum.value()
        commas = MainWindow.spinbox_kommastellen_wizard.value()
        anzahl_summanden = MainWindow.spinBox_zahlenbereich_anzahl_wizard.value()
        smaller_or_equal = MainWindow.combobox_kommastellen_wizard.currentIndex()
        distract_result = create_single_example_addition(minimum, maximum, commas, anzahl_summanden, smaller_or_equal)


    elif thema == 'Subtraktion':
        minimum = MainWindow.spinbox_zahlenbereich_minimum.value()
        maximum = MainWindow.spinbox_zahlenbereich_maximum.value()
        commas = MainWindow.spinbox_kommastellen_wizard.value()
        smaller_or_equal = MainWindow.combobox_kommastellen_wizard.currentIndex()
        anzahl_subtrahenden = MainWindow.spinBox_zahlenbereich_anzahl_wizard.value()
        distract_result = create_single_example_subtraction(minimum, maximum, commas, MainWindow.checkbox_negative_ergebnisse_wizard.isChecked(),anzahl_subtrahenden, smaller_or_equal)

    
    elif thema == 'Multiplikation':
        minimum_1 = MainWindow.spinBox_first_number_min.value()
        maximum_1 = MainWindow.spinBox_first_number_max.value()
        commas_1 = MainWindow.spinBox_first_number_decimal.value()
        smaller_or_equal_1 = MainWindow.combobox_first_number_decimal.currentIndex()
        minimum_2 = MainWindow.spinBox_second_number_min.value()
        maximum_2 = MainWindow.spinBox_second_number_max.value()
        commas_2 = MainWindow.spinBox_second_number_decimal.value()
        smaller_or_equal_2 = MainWindow.combobox_second_number_decimal.currentIndex()
        distract_result = create_single_example_multiplication(minimum_1, maximum_1, commas_1, smaller_or_equal_1, minimum_2, maximum_2, commas_2, smaller_or_equal_2)
        # self.list_of_examples_wizard = create_list_of_examples_multiplication(examples, minimum_1, maximum_1, commas_1, minimum_2, maximum_2, commas_2)

    elif thema == 'Division':
        minimum_1 = MainWindow.spinbox_dividend_min_wizard.value()
        maximum_1 = MainWindow.spinbox_dividend_max_wizard.value()
        minimum_2 = MainWindow.spinbox_divisor_min_wizard.value()
        maximum_2 = MainWindow.spinbox_divisor_max_wizard.value()
        commas_div = MainWindow.spinBox_divisor_kommastellen_wizard.value()
        smaller_or_equal_div = MainWindow.combobox_divisor_kommastelle_wizard.currentIndex()
        commas_result = MainWindow.spinbox_ergebnis_kommastellen_wizard.value()
        smaller_or_equal_result = MainWindow.combobox_ergebnis_kommastellen_wizard.currentIndex()
        if MainWindow.radioButton_division_ohne_rest.isChecked():
            output_type = 0
        elif MainWindow.radioButton_division_rest.isChecked():
            output_type = 1
        elif MainWindow.radioButton_division_decimal.isChecked():
            output_type = 2         
        distract_result = create_single_example_division(minimum_1, maximum_1, minimum_2, maximum_2, commas_div,smaller_or_equal_div, commas_result, smaller_or_equal_result, output_type)


    elif thema == themen_worksheet_wizard[5] or thema == themen_worksheet_wizard[6] or thema == themen_worksheet_wizard[7]:
        minimum = MainWindow.spinbox_zahlenbereich_minimum.value()
        maximum = MainWindow.spinbox_zahlenbereich_maximum.value()
        commas = MainWindow.spinbox_kommastellen_wizard.value()
        smaller_or_equal = MainWindow.combobox_kommastellen_wizard.currentIndex()
        anzahl_summanden = MainWindow.spinBox_zahlenbereich_anzahl_wizard.value()
        brackets_allowed = MainWindow.checkbox_allow_brackets_wizard.isChecked()

        if thema == themen_worksheet_wizard[5]:
            distract_result = create_single_example_ganze_zahlen_strich(minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed)
        elif thema == themen_worksheet_wizard[6]:
            distract_result = create_single_example_ganze_zahlen_punkt(minimum, maximum, commas, anzahl_summanden, smaller_or_equal)
        elif thema == themen_worksheet_wizard[7]:
            distract_result = create_single_example_ganze_zahlen_grundrechnungsarten(minimum, maximum, commas, anzahl_summanden, smaller_or_equal, brackets_allowed)


    return distract_result

def create_nonogramm(chosen_nonogram, coordinates_nonogramm, MainWindow):
    content = """\n\\vfil\n\\fontsize{{12}}{{14}}\selectfont
\meinlr{{{0}

\\antwort{{{1}}}}}{{\scriptsize
\\begin{{multicols}}{{3}}
\\begin{{enumerate}}""".format(nonogramm_empty, chosen_nonogram.split("_")[0].capitalize())

    # list_all_pixles = get_all_pixels(content)
    # random.shuffle(list_all_pixles)

    content = replace_correct_pixels(content, coordinates_nonogramm)

    list_coordinates = list(coordinates_nonogramm.keys())
    # random.shuffle(list_coordinates)

    for all in list_coordinates:
        result = coordinates_nonogramm[all]
        if result == True:
            continue

        if result == False:
            while result == False:
                distract_result = get_random_solution(MainWindow)[-2]
                if distract_result not in coordinates_nonogramm:
                    result = distract_result
        else:
            result = "\\antwort[{0}]{{{0}}}".format(result)

        content += "\item[\\fbox{{\parbox{{15pt}}{{\centering {0}}}}}] {1}\n".format(all, result)
        
    content += """
    \end{enumerate}
    \end{multicols}}"""
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
