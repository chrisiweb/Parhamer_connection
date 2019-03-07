import shutil
import sys
import os
import tkinter
from tkinter import *

hauptfenster = Tk()
hauptfenster.geometry('300x120+500+200')
opened_file=os.path.basename(sys.argv[0])
name, extension=os.path.splitext(opened_file)


if extension=='.exe':
    updatefile_path=os.path.join(os.path.dirname('__file__'),'_database','_config','update','update.exe')
    newapp_path=os.path.join(os.path.dirname('__file__'),'_database','_config','update','LaTeX File Assistent.exe')
    mainfile_path=os.path.join(os.path.dirname('__file__'),'LaTeX File Assistent.exe')
    shutil.copyfile(newapp_path,'LaTeX File Assistent.exe')


if extension=='.py':
    updatefile_path=os.path.join(os.path.dirname('__file__'),'_database','_config','update','update.py')
    newapp_path=os.path.join(os.path.dirname('__file__'),'_database','_config','update','LaTeX File Assistent.py')
    mainfile_path=os.path.join(os.path.dirname('__file__'),'LaTeX File Assistent.py')
    shutil.copyfile(newapp_path,'LaTeX File Assistent.py')


def ok_button():
    os.startfile(mainfile_path)
    sys.exit(0)
label_update=Label(hauptfenster,text="Update erfolgreich!\nProgramm wird neu gestartet.").pack(pady=20)    
btn_OK=Button(hauptfenster,text='OK', command=ok_button,width=5).pack(pady=10)

hauptfenster.mainloop()
