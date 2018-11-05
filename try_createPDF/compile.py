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

subprocess.Popen('cd Teildokument & latex --synctex=-1 test_1.tex & dvips test_1.dvi & ps2pdf test_1.ps',shell=True).wait()
subprocess.Popen('cd Teildokument & test_1.pdf', shell=True).poll()


os.unlink('Teildokument/test_1.aux')
os.unlink('Teildokument/test_1.log')
os.unlink('Teildokument/test_1.dvi')
os.unlink('Teildokument/test_1.ps')

