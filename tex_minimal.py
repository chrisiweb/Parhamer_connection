import os
from config_start import database


tex_preamble = os.path.join(database, "_config", 'preamble.tex')

with open(tex_preamble, "r", encoding='utf-8') as f:
    tex_preamble = f.read()

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