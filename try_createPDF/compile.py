import os, subprocess

# def create_pdf(input_filename, output_filename):
    # process = subprocess.Popen([
        # 'latex',   # Or maybe 'C:\\Program Files\\MikTex\\miktex\\bin\\latex.exe
        # '-output-format=pdf',
        # output_filename, input_filename])
    # process.wait()


# create_pdf("test.tex", "test")
# os.unlink('test.aux')
# print(r'C:\\Users\\Christoph\\Dropbox\\Python\\test.tex')

##### WORKING EXAMPLE !!!! #####
subprocess.Popen('latex --synctex=-1 test_1.tex & dvips test_1.dvi & ps2pdf test_1.ps',shell=True).wait()
subprocess.Popen('test_1.pdf', shell=True).poll()


os.unlink('test_1.aux')
os.unlink('test_1.log')
os.unlink('test_1.dvi')
os.unlink('test_1.ps')

 # ; dvips "C:\Users\Christoph\Dropbox\Python\test.dvi" ;ps2pdf "C:\Users\Christoph\Dropbox\Python\test.ps"'
# subprocess.call('latex test.tex', shell=True)
# subprocess.call('dvips C:\\Users\\Christoph\\Dropbox\\Python\\test.dvi', shell=True)
# subprocess.call('ps2pdf C:\\Users\\Christoph\\Dropbox\\Python\\test.ps', shell=True)
# print(output)



######################

# import os,glob,subprocess

# dictOfSels = {}
# for fname in glob.glob("*.txt"):
    # with open(fname) as f:
        # next(f)
        # sel = fname.split("_yield")[0]
        # dictOfSels[sel] = {}
        # for line in f:
            # line = line.rstrip()
            # dictOfSels[sel][line.split(",")[0]] = [float(line.split(",")[1]),float(line.split(",")[2])]

# header = r'''\documentclass[a4paper,12pt]{report}

# \usepackage{geometry}
# \geometry{a4paper,left=18mm,right=18mm, top=3cm, bottom=2cm}
# \begin{document}
# '''
# footer = r'''\end{document}
# '''

# main = 'test'

# for sel in sorted(dictOfSels.keys()):
    # main = main + '\\begin{tabular}{|c|c|}\hline\multicolumn{2}{|c|}{\\textbf{'+sel+r'''}}\\ \hline
# '''
    # sortedSamples = dictOfSels[sel].keys()
    # if "data" in sortedSamples:
        # sortedSamples.insert(len(sortedSamples)-2,sortedSamples.pop(1))
    # else :
        # sortedSamples.insert(len(sortedSamples)-1,sortedSamples.pop(1))
    # for sample in sortedSamples:
        # if sample == 'MC' or sample == 'data':
            # main = main + '\hline '
        # main = main + sample + ' & $' + "{0:.2f}".format(dictOfSels[sel][sample][0]) + '\pm ' + "{0:.2f}".format(dictOfSels[sel][sample][1]) + r'''$ \\
# '''
    
# main = main + r'''\hline\end{tabular}
# \newline
# \vspace*{1cm}
# \newline
# '''

# content = header + main + footer

# with open('yields.tex','w') as f:
    # f.write(content)

# commandLine = subprocess.Popen(['latex', 'yields.tex'])
# commandLine = subprocess.Popen(['dvips', 'yields.tex'])
# commandLine.communicate()


# os.unlink('yields.tex')
# os.unlink('yields.log')
# os.unlink('yields.aux')