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

subprocess.Popen('cd Teildokument & latex --synctex=-1 Teildokument.tex & dvips Teildokument.dvi & ps2pdf Teildokument.ps',shell=True).wait()
subprocess.Popen('cd Teildokument & Teildokument.pdf', shell=True).poll()

os.unlink('Teildokument/Teildokument.aux')
os.unlink('Teildokument/Teildokument.log')
os.unlink('Teildokument/Teildokument.dvi')
os.unlink('Teildokument/Teildokument.ps')

