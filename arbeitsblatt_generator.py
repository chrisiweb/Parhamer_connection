import random
import math
import os
from config_start import path_localappdata_lama, path_programm
import decimal
import subprocess
from tex_minimal import tex_preamble, tex_end
from create_pdf import create_pdf, open_pdf_file, build_pdf_file



D = decimal.Decimal

print(D)
# def truncate(number, digits) -> float:
#     stepper = 10.0 ** digits
#     return math.trunc(stepper * number) / stepper

def get_random_number(min, max, decimal=0):
    x = round(random.uniform(min,max),decimal)

    x = D('{}'.format(x))

    x = D("{:.{prec}f}".format(x, prec=2))

    if decimal == 0:
        return int(x)
    else:
        return x

for _ in range(30):
    x = get_random_number(100,700, 2)
    print(x)
    y= get_random_number(100,700, 2)
    print(y)
    solution = x+y
    print(solution)
# print('{0} + {1} = {2}'.format(x,y, x+y))


path_file = os.path.join(
    path_localappdata_lama, "Teildokument", "Arbeitsblatt.tex"
    )


def create_worksheet_subtraction():

    examples = ""
    for _ in range(30):
        x = get_random_number(100,700, 2)
        y = get_random_number(100,700, 2)
    
        if x-y<0:
            x, y = y, x
        
        solution = x-y

        examples += """
        \item \\begin{{tabular}}{{rr}}
        & {0} \\\\
        -& {1} \\\\ \hline
        &\\antwort{{{2}}}
        \end{{tabular}}\n
        """.format(str(x).replace(".",","),str(y).replace(".",","),str(solution).replace(".",","))
        
    content = """
    \section{{Arbeitsblatt -- Addition}}

    \\begin{{multicols}}{{3}}
    \\begin{{enumerate}}[(1)]
    {0}
    \end{{enumerate}}
    \end{{multicols}}
    """.format(examples)

    return content



def create_worksheet_addition():

    examples = ""
    for _ in range(30):
        x = get_random_number(-100,100, 2)
        y= get_random_number(100,700, 2)
        solution = x+y

        examples += """
        \item \\begin{{tabular}}{{rr}}
        & {0} \\\\
        +& {1} \\\\ \hline
        &\\antwort{{{2}}}
        \end{{tabular}}\n
        """.format(str(x).replace(".",","),str(y).replace(".",","),str(solution).replace(".",","))
        
    content = """
    \section{{Arbeitsblatt -- Addition}}

    \\begin{{multicols}}{{3}}
    \\begin{{enumerate}}[(1)]
    {0}
    \end{{enumerate}}
    \end{{multicols}}
    """.format(examples)

    return content

content = create_worksheet_addition()

with open(path_file, "w", encoding="utf8") as file:
    file.write(tex_preamble(solution="solution_on"))

    file.write(content)

    file.write(tex_end)

name = 'Arbeitsblatt'
head, tail = os.path.split(name)
file_name = tail
folder_name = "{0}/Teildokument".format(path_programm)


latex_output_file = open(
    "{0}/Teildokument/temp.txt".format(path_localappdata_lama),
    "w",
    encoding="utf8",
    errors="ignore",
)

drive_programm = os.path.splitdrive(path_programm)[0]
drive_save = os.path.splitdrive(folder_name)[0]

drive = ""

terminal_command = 'cd "{1}" & latex -interaction=nonstopmode --synctex=-1 "{2}.tex" & latex -interaction=nonstopmode --synctex=-1 "{2}.tex" & dvips "{2}.dvi" & ps2pdf -dNOSAFER -dALLOWPSTRANSPARENCY "{2}.ps"'.format(
    drive, folder_name, file_name
)


process = subprocess.Popen(
    terminal_command,
    cwd=os.path.splitdrive(path_programm)[0],
    shell=True,
)

process.wait()


open_pdf_file(folder_name, file_name)