def tex_preamble(
    font_size="12pt",
    documentclass = 'article',
    solution = "solution_on",
    random = 0,
    info = "info_off",
    bookmark = False,
    beamer_mode = False,
    pagestyle = "plain",
    tasks = False,
    ):

    if beamer_mode == False:
        start = f"""\documentclass[a4paper,{font_size}]{{{documentclass}}}
\\usepackage{{geometry}}
\geometry{{a4paper,left=18mm,right=18mm, top=2cm, bottom=2cm}}
"""
        spacing = "\onehalfspacing %Zeilenabstand"

    else:
        start = """\documentclass[18pt]{beamer}
\let\oldframe\\frame
\\renewcommand\\frame[1][allowframebreaks, c]{\oldframe[#1]}
\\usetheme{Boadilla}
\\usecolortheme{seahorse}
\date{}
"""
        spacing = ""               

    if bookmark == False:
        bookmark_pkg = ""
    else:    
        bookmark_pkg = f"\\usepackage{{bookmark}}\n\setcounter{{tocdepth}}{{{bookmark}}}"

    if tasks != False:
        tasks_package =f"""
\\usepackage{{tasks}}
\settasks{{
label-width=4ex,
after-skip = {tasks} , % undo paragraph skip
after-item-skip = {tasks} % undo paragraph skip
}}
"""
    else:
        tasks_package = ""
        
    preamble = f"""
{start} 

\\usepackage{{lmodern}}
\\usepackage[T1]{{fontenc}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[ngerman]{{babel}}
\\usepackage[{solution}, random={random}, {info}]{{srdp-mathematik}} % solution_on/off, random, info_on/off
{bookmark_pkg}
{tasks_package}

\pagestyle{{{pagestyle}}} %PAGESTYLE: empty, plain
{spacing}
\setcounter{{secnumdepth}}{{-1}} % keine Nummerierung der Überschriften
%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%% DOKUMENT - ANFANG %%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%

\\begin{{document}}
"""
    return preamble

tex_end = "\end{document}"

def begin_beispiel(themen = None, punkte = 0, halbe_punkte = False):
    if halbe_punkte == True:
        string = "[1/2]"   
    elif themen != None:
        string = "[{}]".format(', '.join(themen))
    else:
        string = ""
    return f"\\begin{{beispiel}}{string}{{{punkte}}}"

end_beispiel = "\n\end{beispiel}"

def begin_beispiel_lang(punkte = 0):
    return f"\\begin{{langesbeispiel}} \item[{punkte}]"

end_beispiel_lang = "\end{langesbeispiel}"



