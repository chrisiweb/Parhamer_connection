import random
# import math
# import os
# from config_start import path_localappdata_lama, path_programm
import decimal
# import subprocess
# from tex_minimal import tex_preamble, tex_end
# from create_pdf import create_pdf, open_pdf_file, build_pdf_file

dict_widgets_wizard = {
    'Addition' : [
        'self.groupBox_zahlenbereich_minimum',
        'self.groupBox_zahlenbereich_maximum',
        'self.groupBox_kommastellen_wizard',
        ],
    'Subtraktion' : [
        'self.groupBox_zahlenbereich_minimum',
        'self.groupBox_zahlenbereich_maximum',
        'self.groupBox_kommastellen_wizard',
        'self.checkbox_negative_ergebnisse_wizard',
        'self.label_negative_ergebnisse_wizard', 
        ],
    'Multiplikation' : [
        'self.groupBox_first_number_wizard',
        'self.groupBox_second_number_wizard',
    ]
}

D = decimal.Decimal


def get_random_number(min, max, decimal=0):
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





def create_single_example_addition(minimum, maximum, commas):
    x = get_random_number(minimum,maximum, commas)
    y= get_random_number(minimum,maximum, commas)
    solution = x+y
    string = "{0} + {1} = {2}".format(str(x).replace(".",","),str(y).replace(".",","),str(solution).replace(".",","))
    return [x,y,solution, string]

def create_single_example_subtraction(minimum, maximum, commas, negative_solutions_allowed):
    x = get_random_number(minimum,maximum, commas)
    y= get_random_number(minimum,maximum, commas)
    if x-y<0 and negative_solutions_allowed== False:
        x, y = y, x
    solution = x-y
    string = "{0} - {1} = {2}".format(str(x).replace(".",","),str(y).replace(".",","),str(solution).replace(".",","))   
    return [x,y,solution, string]

def create_single_example_multiplication(minimum_1, maximum_1, commas_1, minimum_2, maximum_2, commas_2):
    x = get_random_number(minimum_1, maximum_1, commas_1)
    y= get_random_number(minimum_2, maximum_2, commas_2)
    solution = x*y
    string = "{0} \xb7 {1} = {2}".format(str(x).replace(".",","),str(y).replace(".",","),str(solution).replace(".",","))
    return [x,y,solution, string]



def create_list_of_examples_addition(examples, minimum, maximum, commas):
    list_of_examples = []

    for _ in range(examples):
        new_example = create_single_example_addition(minimum, maximum, commas)
        list_of_examples.append(new_example)

    return list_of_examples

def create_list_of_examples_subtraction(examples, minimum, maximum, commas, negative_solutions_allowed):
    list_of_examples = []

    for _ in range(examples):
        new_example = create_single_example_subtraction(minimum, maximum, commas, negative_solutions_allowed)
        list_of_examples.append(new_example)

    return list_of_examples

def create_list_of_examples_multiplication(examples, minimum_1, maximum_1, commas_1, minimum_2, maximum_2, commas_2):
    list_of_examples = []

    for _ in range(examples):
        new_example = create_single_example_multiplication(minimum_1, maximum_1, commas_1, minimum_2, maximum_2, commas_2)
        list_of_examples.append(new_example)

    return list_of_examples

def create_latex_string_addition(content, example, ausrichtung):
    if ausrichtung == 0:
        content += """
        \item \\begin{{tabular}}{{rr}}
        & ${0}$ \\\\
        & ${1}$ \\\\ \hline
        &\\antwort{{${2}$}}
        \end{{tabular}}\n
        """.format(str(example[0]).replace(".",","),str(example[1]).replace(".",","),str(example[2]).replace(".",","))
    elif ausrichtung == 1:
        content += "\item ${0} + {1} = \\antwort{{{2}}}$\n\\vspace{{\\leer}}\n\n".format(str(example[0]).replace(".",","),str(example[1]).replace(".",","),str(example[2]).replace(".",","))
    return content

def create_latex_string_subtraction(content, example, ausrichtung):
    if ausrichtung == 0:
        content += """
        \item \\begin{{tabular}}{{rr}}
        & ${0}$ \\\\
        & $-{1}$ \\\\ \hline
        &\\antwort{{${2}$}}
        \end{{tabular}}\n
        """.format(str(example[0]).replace(".",","), str(example[1]).replace(".",","),str(example[2]).replace(".",","))
    elif ausrichtung == 1:
        content += "\item ${0} - {1} = \\antwort{{{2}}}$\n\\vspace{{\\leer}}\n\n".format(str(example[0]).replace(".",","),str(example[1]).replace(".",","),str(example[2]).replace(".",","))
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

        if get_number_of_digits(result) > factor_digit_length:
            dif = get_number_of_digits(result)-factor_digit_length
            if dif > i:
                hspace = (dif-i)*'\hspace{-0.5em}'
            else:
                hspace = (i-dif)*'\enspace'
        else:
            dif = factor_digit_length-get_number_of_digits(result)  
            hspace = (i+dif)*'\enspace'

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


def create_latex_worksheet(list_of_examples,index, titel, columns, nummerierung, ausrichtung, solution_type=0):
    content = ""

    for example in list_of_examples:
        if index == 0:
            content = create_latex_string_addition(content, example, ausrichtung)
        elif index == 1:
            content = create_latex_string_subtraction(content, example, ausrichtung)
        elif index == 2:
            content = create_latex_string_multiplication(content, example, solution_type)

    content = """
    \section{{{0}}}

    \\begin{{multicols}}{{{1}}}
    \\begin{{enumerate}}[{2}]
    {3}
    \end{{enumerate}}
    \end{{multicols}}
    """.format(titel, columns, nummerierung, content)

    return content

