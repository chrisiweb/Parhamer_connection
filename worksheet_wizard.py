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
        'self.groupBox_zahlenbereich_minimum',
        'self.groupBox_zahlenbereich_maximum',
        'self.groupBox_kommastellen_wizard',
        'self.groupBox_zahlenbereich_anzahl',
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
        'self.comboBox_solution_type_wizard',
    ],
    'Division' : [
        'self.groupBox_dividend_wizard',
        'self.groupBox_divisor_wizard',
        'self.groupBox_ergebnis_wizard',
    ],
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





def create_single_example_addition(minimum, maximum, commas, anzahl_summanden):
    summanden = []
    for _ in range(anzahl_summanden):
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

def get_quotient_with_rest(dividend,divisor):
    
    return "{}\nR {}".format(int(dividend//divisor), dividend%divisor) 

def create_single_example_division(minimum_1, maximum_1, minimum_2, maximum_2, commas_div, commas_result, output_type):
    divisor = get_random_number(minimum_2, maximum_2, commas_div)

    if output_type == 1:  
        dividend = get_random_number(minimum_1, maximum_1)
        result = str(get_quotient_with_rest(dividend, divisor))

    else:
        result_min = ceil(minimum_1/divisor)
        result_max = floor(maximum_1/divisor)

        if output_type == 0:
            commas_result = 0
        result = get_random_number(result_min, result_max, commas_result)

        dividend = result*divisor

        result = str(result)

    string = "{0} : {1} = {2}".format(str(dividend).replace(".",","),str(divisor).replace(".",","),result.replace(".",","))

    return [dividend,divisor,result, string]


def create_list_of_examples_addition(examples, minimum, maximum, commas, anzahl_summanden):
    list_of_examples = []

    for _ in range(examples):
        new_example = create_single_example_addition(minimum, maximum, commas, anzahl_summanden)
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

def create_list_of_examples_division(examples, minimum_1, maximum_1, minimum_2, maximum_2, commas_div, commas_result, output_type):
    list_of_examples = []

    for _ in range(examples):
        new_example = create_single_example_division(minimum_1, maximum_1, minimum_2, maximum_2, commas_div, commas_result, output_type)
        list_of_examples.append(new_example)

    # print(list_of_examples)
    return list_of_examples

def create_latex_string_addition(content, example, ausrichtung):
    summanden = example[0]

    if ausrichtung == 0:
        content += "\item \\begin{tabular}{rr}"

        for all in summanden:
            content += "& ${0}$ \\\\ \n".format(str(all).replace(".",","))

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
    if ausrichtung == 0:
        content += """
        \item \\begin{{tabular}}{{rr}}
        & ${0}$ \\\\
        & $-{1}$ \\\\ \hline
        &\\antwort{{${2}$}}
        \end{{tabular}}\n
        """.format(str(example[0]).replace(".",","), str(example[1]).replace(".",","),str(example[2]).replace(".",","))
    elif ausrichtung == 1:
        content += "\item ${0} - {1} = \\antwort{{{2}}}$\n\\leer\n\n".format(str(example[0]).replace(".",","),str(example[1]).replace(".",","),str(example[2]).replace(".",","))
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



def create_latex_worksheet(list_of_examples,index, titel, columns, nummerierung, ausrichtung, solution_type=0):
    content = "\section{{{0}}}\n\n".format(titel)
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
                if distract_result not in coordinates:
                    break
            coordinates[distract_pixel] = False
            i +=1

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
        distract_result = create_single_example_addition(minimum, maximum, commas, anzahl_summanden)


    elif thema == 'Subtraktion':
        minimum = MainWindow.spinbox_zahlenbereich_minimum.value()
        maximum = MainWindow.spinbox_zahlenbereich_maximum.value()
        commas = MainWindow.spinbox_kommastellen_wizard.value()
        distract_result = create_single_example_subtraction(minimum, maximum, commas, MainWindow.checkbox_negative_ergebnisse_wizard.isChecked())

    
    elif thema == 'Multiplikation':
        minimum_1 = MainWindow.spinBox_first_number_min.value()
        maximum_1 = MainWindow.spinBox_first_number_max.value()
        commas_1 = MainWindow.spinBox_first_number_decimal.value()
        minimum_2 = MainWindow.spinBox_second_number_min.value()
        maximum_2 = MainWindow.spinBox_second_number_max.value()
        commas_2 = MainWindow.spinBox_second_number_decimal.value()
        distract_result = create_single_example_multiplication(minimum_1, maximum_1, commas_1, minimum_2, maximum_2, commas_2)
        # self.list_of_examples_wizard = create_list_of_examples_multiplication(examples, minimum_1, maximum_1, commas_1, minimum_2, maximum_2, commas_2)

    elif thema == 'Division':
        minimum_1 = MainWindow.spinbox_dividend_min_wizard.value()
        maximum_1 = MainWindow.spinbox_dividend_max_wizard.value()
        minimum_2 = MainWindow.spinbox_divisor_min_wizard.value()
        maximum_2 = MainWindow.spinbox_divisor_max_wizard.value()
        commas_div = MainWindow.spinBox_divisor_kommastellen_wizard.value()
        commas_result = MainWindow.spinbox_ergebnis_kommastellen_wizard.value()
        if MainWindow.radioButton_division_ohne_rest.isChecked():
            output_type = 0
        elif MainWindow.radioButton_division_rest.isChecked():
            output_type = 1
        elif MainWindow.radioButton_division_decimal.isChecked():
            output_type = 2         
        distract_result = create_single_example_division(minimum_1, maximum_1, minimum_2, maximum_2, commas_div, commas_result, output_type)
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
