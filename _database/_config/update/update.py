#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from time import sleep
import subprocess

path_programm=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(sys.argv[0]))))

# print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(sys.argv[0])))))

if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    if path_programm is '':
        path_programm = "."

print('Programm wird aktualisiert...')

opened_file=os.path.basename(sys.argv[0])
name, extension=os.path.splitext(opened_file)

updatefile_path=os.path.join(path_programm,'_database','_config','update','update%s'%extension)
newapp_path=os.path.join(path_programm,'_database','_config','update','LaMA%s'%extension)
mainfile_path=os.path.join(path_programm,'LaMA%s'%extension)

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

items = list(range(0, 100))
l = len(items)

# Initial call to print 0% progress
printProgressBar(0, l, prefix = 'Installation:', length = 50)
for i, item in enumerate(items):
    if i==50:
        if sys.platform.startswith('linux'):
            p=subprocess.Popen('cp "{0}" "LaMA{1}"'.format(newapp_path, extension), stdout=subprocess.PIPE,shell=True)
        elif sys.platform.startswith('darwin'):
            p=subprocess.Popen('cp "{0}" "LaMA{1}"'.format(newapp_path, extension), stdout=subprocess.PIPE,shell=True)
        else:
            p=subprocess.Popen('copy "{0}" "LaMA{1}"'.format(newapp_path, extension), stdout=subprocess.PIPE,shell=True)

        (output, err) = p.communicate()
        p_status=p.wait()

    sleep(0.01)
    # Update Progress Bar
    printProgressBar(i + 1, l, prefix = 'Installation:',  length = 50)

if p_status==0:
    print('\nProgramm wurde erfolgreich aktualisiert. Drücken Sie "Enter", um fortzufahren...')
else:
    print(newapp_path)
    print('\nProgramm konnte nicht aktualisiert werden. Bitte versuchen Sie es später erneut.\nFehler: "%s"\n\nDrücken Sie "Enter", um mit der älteren Version fortzufahren...'%str(output)[2:-5]) 
    
input()

if sys.platform.startswith('linux'):
    #print(mainfile_path)
    subprocess.run("python3 " + mainfile_path, shell=True)
elif sys.platform.startswith('darwin'):
    subprocess.run("python3 " + mainfile_path, shell=True)
else:
    os.startfile(mainfile_path)
 

