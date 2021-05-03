import os
from config_start import database


# tex_preamble = os.path.join(database, "_config", 'preamble.tex')

# with open(tex_preamble, "r", encoding='utf-8') as f:
#     tex_preamble = f.read()



def tex_preamble(
    solution = "solution_on",
    random = 0,
    info = "info_off",
    bookmark = False,
    beamer_mode = False,
    pagestyle = "plain",
    ):

    if beamer_mode == False:
        start = """
\documentclass[a4paper,12pt]{article}
\\usepackage{geometry}
\geometry{a4paper,left=18mm,right=18mm, top=2cm, bottom=2cm}
"""
        spacing = "\onehalfspacing %Zeilenabstand"

    else:
        start = """
\documentclass[18pt]{beamer}
\let\oldframe\\frame
\\renewcommand\\frame[1][allowframebreaks, c]{\oldframe[#1]}
\\usetheme{Boadilla}
\\usecolortheme{seahorse}
\date{}
"""
        spacing = ""               

    if bookmark == True:
        bookmark_pkg = "\\usepackage{bookmark}"
    else:
        bookmark_pkg = ""

    preamble = """
{0} 

\\usepackage{{lmodern}}
\\usepackage[T1]{{fontenc}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[ngerman]{{babel}}
\\usepackage[{1}, random={2}, {3}]{{srdp-mathematik}} % solution_on/off, random, info_on/off
{4}

\pagestyle{{{5}}} %PAGESTYLE: empty, plain
{6}
\setcounter{{secnumdepth}}{{-1}} % keine Nummerierung der Überschriften
%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%% DOKUMENT - ANFANG %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%

\\begin{{document}}
""".format(
    start,
    solution,
    random,
    info,
    bookmark_pkg,
    pagestyle,
    spacing
)
    return preamble

tex_end = "\end{document}"

def begin_beispiel(themen = None, punkte = 0):
    if themen != None:
        string = "[{}]".format(', '.join(themen))
    else:
        string = ""
    return "\\begin{{beispiel}}{0}{{{1}}}\n".format(string, punkte)

end_beispiel = "\n\end{beispiel}"

def begin_beispiel_lang(punkte = 0):
    return "\\begin{{langesbeispiel}} \item[{0}]\n".format(punkte)

end_beispiel_lang = "\end{langesbeispiel}"