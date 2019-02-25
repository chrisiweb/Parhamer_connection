#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tkinter.ttk import Progressbar
import time
import threading
import sys
import os 
import os.path
from pathlib import Path
import datetime
import json				   
import subprocess
import tkinter
from tkinter import *
import yaml


hauptfenster = Tk()
hauptfenster.title('Typ 1 LaTeX file assistent')
#hauptfenster.wm_iconbitmap('latex.ico')

hauptfenster.geometry('+50+50')

HUGE_FONT=('Calibri',15)
LARGE_FONT=('Calibri',12)
STANDARD_FONT =('Calibri', 10)
SMALL_FONT =('Calibri',8)

#############################################
################ FARBEN TABELLE ##############
BG_KLASSE='#e6f3ff'
# '#ecffe6'

# Load Config-file
config1 = yaml.safe_load(open("config1.yml")) # for a lack of better name

configNames = [ "ag_kb", "ag_kb_beschreibung", "AG_BB", "an_kb", "an_kb_beschreibung", "AN_BB", "fa_kb", "fa_kb_beschreibung", "FA_BB", "ws_kb", "ws_kb_beschreibung", "WS_BB", "AF_BB", "aufgaben_formate", 
        "Klassen", 
        "themen_klasse_5", "themen_klasse_6", "themen_klasse_7", "themen_klasse_8" ]

ag_kb = config1['ag_kb']
ag_kb_beschreibung = config1['ag_kb_beschreibung']
AG_BB = config1['AG_BB']
an_kb = config1['an_kb']
an_kb_beschreibung = config1['an_kb_beschreibung']
AN_BB = config1['AN_BB']
fa_kb = config1['fa_kb']
fa_kb_beschreibung = config1['fa_kb_beschreibung']
FA_BB = config1['FA_BB']
ws_kb = config1['ws_kb']
ws_kb_beschreibung = config1['ws_kb_beschreibung']
WS_BB = config1['WS_BB']
AF_BB = config1['AF_BB']
aufgaben_formate = config1['aufgaben_formate']
Klassen = config1['Klassen']
themen_klasse_5 = config1['themen_klasse_5']
themen_klasse_6 = config1['themen_klasse_6']
themen_klasse_7 = config1['themen_klasse_7']
themen_klasse_8 = config1['themen_klasse_8']



#########################################################################
############  Skript zu Erstellung der LaTeX Datei ######################
#########################################################################
container=Frame(hauptfenster)
container.grid()
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

frame_klassen=Frame(hauptfenster, bg=BG_KLASSE)
frame_klassen.grid(row=1,column=0, sticky=N+S)
frame_refresh_ddb=Frame(hauptfenster)
frame_refresh_ddb.grid(row=0,column=0)																	  
# frame_k5= Frame(frame_klassen)
# frame_k5.grid(row=0, column=0, sticky=N)
# frame_k6= Frame(frame_klassen)
# frame_k6.grid(row=1, column=0, sticky=N)		
# frame_k7= Frame(frame_klassen)
# frame_k7.grid(row=0, column=1, sticky=N)
# frame_k8= Frame(frame_klassen)
# frame_k8.grid(row=1, column=1, sticky=N)
frame_gk = Frame(hauptfenster)
frame_gk.grid(row=1,column=1,sticky=N+W)	
frame_AG= Frame(frame_gk,bd=2, relief=RIDGE)
frame_AG.grid(row=0, column=0, sticky=W)
frame_AN= Frame(frame_gk,bd=2, relief=RIDGE)
frame_AN.grid(row=0, column=1, sticky=W)
frame_FA= Frame(frame_gk,bd=2, relief=RIDGE)
frame_FA.grid(row=0, column=2, sticky=W)
frame_WS= Frame(frame_gk,bd=2, relief=RIDGE)
frame_WS.grid(row=0, column=3, sticky=W)
frame_infobox = Frame(hauptfenster)
frame_infobox.grid(row=2, column=1, columnspan=4, sticky=N+E+W)
frame_zusatz = Frame(hauptfenster, bd=5, relief=RIDGE)
frame_zusatz.grid(row=2, column=0,rowspan=2,sticky=E+W)
frame_suche =Frame(hauptfenster)
frame_suche.grid(sticky=W+S,row=3, column=1)


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

latest_update=''								
class hoverover(Frame):
	def __init__(self,frame, gk_name, gk_explanation, gk_variable):
		Frame.__init__(self)
		self.gk_explanation=gk_explanation
		if "L" in gk_name:
			cb_phantom=Label(frame,text=" ",width=10).grid(row=r, column=c, pady=5,padx=5, sticky=W)
			self.l1 = Checkbutton(frame, text=gk_name, variable=gk_variable)
			
		else:
			cb_phantom=Label(frame,text=" ",width=10).grid(row=r, column=c, pady=5,padx=5, sticky=W)		
			self.l1 = Checkbutton(frame, text=gk_name, variable=gk_variable,bg="powderblue")
			
		self.l1.grid(row=r, column=c, pady=5,padx=3, sticky=W)
		self.l1.bind("<Enter>",self.on_enter)
		self.l1.bind("<Leave>", self.on_leave)
		
	def on_enter(self,event):
		explanation.configure(text=self.gk_explanation,font=STANDARD_FONT,bg='powderblue',relief=RAISED)

	def on_leave(self, enter):
		explanation.configure(text="",bg='powderblue', relief=FLAT)	
	


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]	
# data_folder=Path('Teildokument')
# log_file= data_folder / 'log_file'
def create_pdf():
	if sys.platform.startswith('linux'):
		subprocess.Popen('cd Teildokument ; latex --synctex=-1 Teildokument.tex ; dvips Teildokument.dvi ; ps2pdf -dNOSAFER Teildokument.ps',shell=True).wait()
		subprocess.run(['xdg-open', 'Teildokument/Teildokument.pdf'])
	elif sys.platform.startswith('darwin'):
		subprocess.Popen('cd Teildokument ; latex --synctex=-1 Teildokument.tex ; dvips Teildokument.dvi ; ps2pdf -dNOSAFER Teildokument.ps',shell=True).wait()
		subprocess.run(['xdg-open', 'Teildokument/Teildokument.pdf'])
	else:
		subprocess.Popen('cd Teildokument & latex --synctex=-1 Teildokument.tex & dvips Teildokument.dvi & ps2pdf -dNOSAFER Teildokument.ps',shell=True).wait()
		subprocess.Popen('cd Teildokument & Teildokument.pdf', shell=True).poll()
	
	cleanupsuffix=['aux', 'dvi', 'log', 'ps']
	for suffixes in cleanupsuffix:
	    filepath='Teildokument/Teildokument.' + suffixes
	    os.unlink(filepath)

def refresh():
	beispieldaten_dateipfad = {}
	beispieldaten = []
	

	for root, dirs, files in os.walk('.'):
		for all in files:
			if all.endswith('.tex') or all.endswith('.ltx'):
				if not ('Gesamtdokument' in all) and not ('Teildokument' in all):
					file=open(os.path.join(root,all), encoding='ISO-8859-1')
					for i, line in enumerate(file):
						if not line == "\n":			
							beispieldaten_dateipfad[line]=os.path.join(root,all)
							beispieldaten.append(line)
							break
					file.close()

	filename= 0
	for root, dirs, files in os.walk(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),"Aufgabensammlung (offiziell)\Typ 1 Aufgaben")):
		for all in files:
			while_cnt=0
			if all.endswith('.tex') or all.endswith('.ltx'):
				if not ('Gesamtdokument' in all) and not ('Teildokument' in all):
					file=open(os.path.join(root,all), encoding='ISO-8859-1')
					dirname, filename= os.path.split(root)
					dirname=root
					while filename != 'Aufgabensammlung (offiziell)':
						dirname, filename= os.path.split(dirname)
						if while_cnt==0:
							rel_path=filename
							while_cnt +=1
						else:		
							rel_path=os.path.join(filename,rel_path)
						os.path.dirname(dirname)
					for i, line in enumerate(file):
						if not line == "\n":			
							beispieldaten_dateipfad[line]=os.path.join(rel_path,all)
							beispieldaten.append(line)
							break
					file.close()
		# print(beispieldaten_dateipfad)
		# print(beispieldaten)
	data_folder=Path('Teildokument')
	log_file=os.path.join(os.path.dirname('__file__'),'Teildokument','log_file')
	#log_file= data_folder / 'log_file'# Works in Windows, doesn't work in linux
	
	with open(log_file, 'w+') as f:
		json.dump(beispieldaten_dateipfad, f,ensure_ascii=False)
	# with open(log_file, 'w') as f:
		# json.dump(beispieldaten_dateipfad, f)
	# print(log_file.read_text())
	label_update.config(text='Last Update: '+modification_date(log_file).strftime('%d.%m.%y - %H:%M'))	

	
def control_cb():
	if not os.path.isfile(os.path.join('Teildokument','log_file')):
		refresh()
	suchbegriffe = []

	##### Suche der Schulstufe 

	for y in range(5,9):
		themen_klasse=eval('themen_klasse_%s'%y)
		for all in themen_klasse:
			x='K%s_'%y+all+'.get()'
			if eval(x):
				suchbegriffe.append(all)	
	
	#### ALGEBRA UND GEOMETRIE
	for all in ag_kb:
		x=all+".get()"
		if eval(x):
			suchbegriffe.append(AG_BB[ag_kb.index(all)])
	#### ANALYSIS		
	for all in an_kb:
		x=all+".get()"
		if eval(x):
			suchbegriffe.append(AN_BB[an_kb.index(all)])
	#### FUNKTIONALE ABHÄNGIGKEITEN		
	for all in fa_kb:
		x=all+".get()"
		if eval(x):
			suchbegriffe.append(FA_BB[fa_kb.index(all)])
	#### WAHRSCHEINLICHKEIT UND STATISTIK		
	for all in ws_kb:
		x=all+".get()"
		if eval(x):
			suchbegriffe.append(WS_BB[ws_kb.index(all)])			


	with open(log_file) as f:
		beispieldaten_dateipfad = json.load(f)
		beispieldaten=list(beispieldaten_dateipfad.keys())						  

	

	filename_teildokument = os.path.join(os.path.dirname('__file__'),'Teildokument','Teildokument.tex')
	try:
	    file=open(filename_teildokument,"w", encoding='ISO-8859-1')
	except FileNotFoundError:
		os.makedirs(filename_teildokument) # If dir is not found make it recursivly
	file.write("\documentclass[a4paper,12pt]{report}\n\n"
	"\\usepackage{geometry}\n"	
	"\geometry{a4paper,left=18mm,right=18mm, top=2cm, bottom=2cm}\n\n" 
	"\\usepackage{lmodern}\n"
	"\\usepackage[T1]{fontenc}\n"
	"\\usepackage{eurosym}\n"
	"\\usepackage[latin1]{inputenc}\n"
	"\\usepackage[ngerman]{babel}\n")
	if solution_var.get():
		file.write('\\usepackage[solution_on]{srdp-mathematik} % solution_on/off\n')
	else:
		file.write('\\usepackage[solution_off]{srdp-mathematik} % solution_on/off\n')
	file.write("\setcounter{Zufall}{0}\n\n\n"
	"\pagestyle{empty} %PAGESTYLE: empty, plain, fancy\n"
	"\onehalfspacing %Zeilenabstand\n"
	"\setcounter{secnumdepth}{-1} % keine Nummerierung der Ueberschriften\n\n\n\n"
	"%\n"
	"%\n"
	"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% DOKUMENT - ANFANG %%%%%%%%%%%%%%%%%%%"
	"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
	"%\n"
	"%\n"
	"\\begin{document}\n"
	'\shorthandoff{"}\n')
	file.close()
	

	if suchtyp_var.get() == UND:
	 #############	Erstellung der Kompetenzbereiche pro Beispiel
		liste_kompetenzbereiche ={}
		r=1
		for all in beispieldaten:
			gkliste = []
			for gkbereich in AG_BB:
				if gkbereich in all:
					gkliste.append(gkbereich)
			for gkbereich in AN_BB:
				if gkbereich in all:
					gkliste.append(gkbereich)
			for gkbereich in FA_BB:
				if gkbereich in all:
					gkliste.append(gkbereich)
			for gkbereich in WS_BB:
				if gkbereich in all:
					gkliste.append(gkbereich)
			for klasse in Klassen:
				if klasse in all:
					gkliste.append(klasse)
			liste_kompetenzbereiche.update({r:gkliste})
			r+=1

		
		gesammeltedateien=[]
		for r in range(1,len(liste_kompetenzbereiche)+1):
			if liste_kompetenzbereiche[r]==[]:
				del liste_kompetenzbereiche[r]	
		for r in range(1,len(liste_kompetenzbereiche)+1):
			for all in suchbegriffe:
				if r in liste_kompetenzbereiche.keys():
					if all not in liste_kompetenzbereiche[r]:
						del liste_kompetenzbereiche[r]
	
		
		for key in liste_kompetenzbereiche.keys():
			gesammeltedateien.append(beispieldaten[key-1])
		
		for all in gesammeltedateien[:]:
			if not len(entry_suchbegriffe.get()) ==0:
				if entry_suchbegriffe.get().lower() not in all.lower():
					gesammeltedateien.remove(all)

					
			
	if suchtyp_var.get() == ODER:
	
		gesammeltedateien=[]
		for all in suchbegriffe:
			for element in list(beispieldaten_dateipfad.keys())[:]:
				if all in element:
					gesammeltedateien.append(element)

		gesammeltedateien.sort(key=natural_keys)
		

		for all in gesammeltedateien[:]:
			if not len(entry_suchbegriffe.get()) ==0:
				if entry_suchbegriffe.get().lower() not in all.lower():
					gesammeltedateien.remove(all)

		# if not len(entry_suchbegriffe.get()) ==0:
			# suchbegriffe.append(entry_suchbegriffe.get())
			# for all in list(beispieldaten_dateipfad.keys())[:]:
				# if entry_suchbegriffe.get().lower() in all.lower():
					# if all not in gesammeltedateien:
						# gesammeltedateien.append(all)

	dict_gesammeltedateien={}
	for all in gesammeltedateien:
		dict_gesammeltedateien[all]=beispieldaten_dateipfad[all]

	# print(dict_gesammeltedateien)

	
###############################################	
#### Auswahl der gesuchten Antwortformate ####
###############################################

	if af_MC.get() or af_ZO.get() or af_LT.get() or af_OA.get():
		if suchbegriffe==[]:
			dict_gesammeltedateien=beispieldaten_dateipfad
		for all_formats in AF_BB:
			x="af_"+all_formats+".get()"
			if not eval(x):
				for all in list(dict_gesammeltedateien):
					if all_formats in all:
						del dict_gesammeltedateien[all]
			if eval(x):
				suchbegriffe.append(all_formats)



###############################################	
#### Auswahl der gesuchten Klassen #########
###############################################
	selected_klassen=[]
	if K5.get() or K6.get() or K7.get() or K8.get():
		if suchbegriffe==[]:
			dict_gesammeltedateien=beispieldaten_dateipfad
		for all_formats in list(Klassen):
			x=all_formats+".get()"
			if eval(x):
				selected_klassen.append(all_formats)
				suchbegriffe.append(all_formats)
		for all in list(dict_gesammeltedateien):
			if not any(all_formats in all for all_formats in selected_klassen):
				del dict_gesammeltedateien[all]

	

	
	##############################
	if not dict_gesammeltedateien:
		def okbutton():
			nebenfenster.destroy()
		nebenfenster = Tk()
		nebenfenster.title('Warnung')
		nebenfenster.geometry('400x200+500+200')
		Label(nebenfenster, text="Kein Suchergebnis gefunden. \n\n Das LaTeX Dokument ist leer!", font=("", 12), pady=50).pack()
		Button(nebenfenster, text='OK', width=15, command=okbutton).pack()
		print('Keine LaTeX-Datei ausgeben!')
		return
		
	beispieldaten.sort(key=natural_keys)
	loop_dateien=1
	check=0
	file=open(filename_teildokument,"a", encoding='ISO-8859-1')
	file.write('\n \\scriptsize Suchbegriffe: ')
	for all in suchbegriffe:
		if all == suchbegriffe[-1]:
			file.write(all)
		else:	
			file.write(all + ', ')
	file.write('\\normalsize \n \n')
	file.close()

	
	for key, value in dict_gesammeltedateien.items():
		value=value.replace('\\','/') 
		file=open(filename_teildokument,"a", encoding='ISO-8859-1')
		if 'Aufgabensammlung (offiziell)' in value:
			file.write('\input{"../../../'+value+'"}%\n'
			'\hrule  \leer\n\n')
		else:
			file.write('\input{".'+value+'"}%\n'
			'\hrule  \leer\n\n')
	file.write('\shorthandoff{"}\n'
	"\end{document}")
	file.close()
	
	
	window_loading = Tk()
	window_loading.title('Lade...')
	window_loading.geometry('+300+200')
	def loading_bar():
		def start_loading_bar():
			progress.grid(row=2,column=0)
			progress.start()
			create_pdf()
			progress.stop()
			window_loading.destroy()
		hauptfenster.destroy()
		threading.Thread(target=start_loading_bar).start()
	if len(dict_gesammeltedateien)==1:
		label_output=Label(window_loading, text='Insgesamt wurde '+ str(len(dict_gesammeltedateien)) + ' Beispiel gefunden.\n', font=LARGE_FONT).grid(row=0,column=0)	
	else:
		label_output=Label(window_loading, text='Insgesamt wurden '+ str(len(dict_gesammeltedateien)) + ' Beispiele gefunden.\n', font=LARGE_FONT).grid(row=0,column=0)		
	label_loading = Label(window_loading , text='Lade PDF Datei...', font=LARGE_FONT).grid(row=1,column=0)
	progress = Progressbar(window_loading , orient=HORIZONTAL,length=250,  mode='indeterminate')
	loading_bar()
	window_loading.mainloop()	
	
	# print("Insgesamt wurde(n) " + str(len(dict_gesammeltedateien)) + " Beispiel(e) gefunden. Entsprechende LaTeX-Datei wird ausgegeben...", font=STANDARD_FONT)
	# if sys.platform.startswith('linux'):
		# subprocess.run(['xdg-open', filename_teildokument])
	# elif sys.platform.startswith('darwin'):
		# subprocess.run(['open', filename_teildokument])
	# else:
		# os.system(filename_teildokument)
	sys.exit(0)
		
		
		
def ag_select_all():
	if ag11.get():
		for all in ag_cb_all:
			all.set(0)
	else:
		for all in ag_cb_all:
			all.set(1)
			
def an_select_all():
	if an11.get():
		for all in an_cb_all:
			all.set(0)
	else:
		for all in an_cb_all:
			all.set(1)			

def fa_select_all():
	if fa11.get():
		for all in fa_cb_all:
			all.set(0)
	else:
		for all in fa_cb_all:
			all.set(1)

def ws_select_all():
	if ws11.get():
		for all in ws_cb_all:
			all.set(0)
	else:
		for all in ws_cb_all:
			all.set(1)				

kb = Label(hauptfenster, text="Kompetenzbereiche:")


def select_all_klasse5():
	if K5_FU.get():
		for all in themen_klasse_5:
			eval('K5_'+all).set(0)
	else:
		for all in themen_klasse_5:
			eval('K5_'+all).set(1)	
def select_all_klasse6():
	if K6_BSW.get():
		for all in themen_klasse_6:
			eval('K6_'+all).set(0)
	else:
		for all in themen_klasse_6:
			eval('K6_'+all).set(1)
def select_all_klasse7():
	if K7_DR.get():
		for all in themen_klasse_7:
			eval('K7_'+all).set(0)
	else:
		for all in themen_klasse_7:
			eval('K7_'+all).set(1)
def select_all_klasse8():
	if K8_DDG.get():
		for all in themen_klasse_8:
			eval('K8_'+all).set(0)
	else:
		for all in themen_klasse_8:
			eval('K8_'+all).set(1)

#########################################
### CHECKBOXEN FÜR... ########################
########################################

######## Schulstufen & Themenbereiche #######

r=0
c=0

for x in range(5,9):
	if x==6:
		r+=1
	if x==7:
		c=1
		r-=14
	if x==8:
		r+=2
	beschriftung = 'label_K%s'%x
	beschriftung =	Button(frame_klassen, text= "%s. KLASSE"%x,font=STANDARD_FONT ,command=eval('select_all_klasse%s'%x)).grid(column=c, row=r)
	r+=1
	for all in eval('themen_klasse_%s'%x):
		y='K%s_'%x+all
		vars()[y]=IntVar()
		name = eval('themen_klasse_%s[all]'%x) + ' ('+all+')'
		cb_temporary= Checkbutton(frame_klassen, text= name,font=SMALL_FONT,justify=(LEFT), variable=vars()[y], bg=BG_KLASSE).grid(column=c, row=r, sticky=W)
		r+=1



#######  Rahmen #########

###############################  ... Aufgabenformate ##############################
r=0
c=0

Aufgabenformate_header = Label(frame_zusatz, text="Gesuchte Aufgabenformate:", font=("",11, 'bold')).grid(column=c, row=r, sticky=W, columnspan=2)
r+=1

for all in aufgaben_formate:
	y='af_'+all.upper()
	vars()[y]=IntVar()
	name=aufgaben_formate[all] +' ('+all.upper()+')'
	cb_format= Checkbutton(frame_zusatz, text=name , variable=vars()[y]).grid(column=c, row=r,sticky=W)
	if c==1:
		r+=1
		c=0
	else:
		c+=1
	

##################### Suche nach Klassen #######################

c=0
r+=1
Aufgabenformate_header = Label(frame_zusatz, text="Klassen:", font=("",11, 'bold')).grid(column=c, row=r, sticky=W, columnspan=2)
r+=1
for x in range(5,9):
	y='K%s'%x
	vars()[y]=IntVar()
	cb_suche_klasse=Checkbutton(frame_zusatz, text= "%s. KLASSE"%x, variable=vars()[y]).grid(column=c, row=r,sticky=W)
	if c==1:
		r+=1
		c=0
	else:
		c+=1	
	# if x!=8:
		# c+=2
		
	

########## ... ALGEBRA UND GEOMETRIE ###############
# r=5
# c=10
py=5
c=0
r=0
ag_cb_all=[]
ag_all=IntVar()
Button(frame_AG, text='Algebra und Geometrie:', command=ag_select_all).grid(column=c, row=r, sticky=W, columnspan=2)

r+=1
for all in ag_kb:
	vars()[all]=IntVar()
	hoverover(frame_AG,AG_BB[ag_kb.index(all)], ag_kb_beschreibung[all], vars()[all])
	# .grid(column=0, row=0,sticky=W)	
	ag_cb_all.append(vars()[all])
	r+=1
	if r>11:
		r-=11
		c+=1


				
################# ... ANALYSIS ###############
# c+=1
# space = Label(hauptfenster, text="	      ")
# space.grid(column=c, row=5, sticky=E)
# c+=1

r=0
c=0
an_cb_all=[]
an_all=IntVar()
Button(frame_AN, text='Analysis:', command=an_select_all).grid(column=c, row=r,sticky=W, columnspan=2)	
r+=1
for all in an_kb:
	vars()[all]=IntVar()
	hoverover(frame_AN, AN_BB[an_kb.index(all)], an_kb_beschreibung[all], vars()[all])
	#.grid(column=c, row=r, pady=py, sticky=W)
	an_cb_all.append(vars()[all])
	r+=1
	if r>11:
		r-=11
		c+=1
		
# c+=1
# space = Label(hauptfenster, text="	      ")
# space.grid(column=c, row=5, sticky=E)
# c+=1	

############ ... FUNKTIONALE ABHÄNGIGKEITEN ###############################	
r=0
c=0
fa_cb_all=[]
fa_all=IntVar()
Button(frame_FA, text='Funktionale Abhängigkeiten:', command=fa_select_all).grid(column=c, row=r,sticky=W, columnspan=4)		
r+=1
for all in fa_kb:
	vars()[all]=IntVar()
	hoverover(frame_FA,FA_BB[fa_kb.index(all)], fa_kb_beschreibung[all], vars()[all])
	#.grid(column=c, row=r, pady=py, sticky=SW)
	fa_cb_all.append(vars()[all])
	r+=1
	if r>11:
		r-=11
		c+=1

# c+=1		
# space = Label(hauptfenster, text="	     ")
# space.grid(column=c, row=5, sticky=E)
c+=1

##################	 ... WAHRSCHEINLICHKEIT UND STATISTIK ########################
r=0
c=0
ws_cb_all=[]
ws_all=IntVar()
Button(frame_WS, text='Wahrscheinlichkeit und Statistik:', command=ws_select_all).grid(column=c, row=r,sticky=W, columnspan=2)	
r+=1
for all in ws_kb:
	vars()[all]=IntVar()
	hoverover(frame_WS, WS_BB[ws_kb.index(all)], ws_kb_beschreibung[all], vars()[all])
	ws_cb_all.append(vars()[all])
	r+=1
	if r>11:
		r-=11
		c+=1	

# c+=1
# space = Label(hauptfenster, text="	      ")
# space.grid(column=c, row=5, sticky=E)


##########################################################################################

UND='Alle Dateien ausgeben, die alle Suchkriterien enthalten.'
ODER='Alle Dateien ausgeben, die zumindest ein Suchkriterium enthalten.'
suchtyp_var = StringVar()
# label_suchtyp= Label(hauptfenster, text="Alle Dateien ausgeben, die")
suchtyp = OptionMenu(hauptfenster,suchtyp_var,ODER,UND)
suchtyp.config(width=60)
suchtyp_var.set(ODER)
# label_suchtyp.grid(row=0, column=0, sticky=W)
suchtyp.grid(row=0, column=1,columnspan=2, sticky=W)


explanation = Label(frame_infobox,text="",width=138,height=4)	
explanation.grid(row=0,column=0,sticky=W)

button_refresh_ddb=Button(frame_refresh_ddb, text='Refresh Database', command=refresh)
button_refresh_ddb.grid(row=0, column=0, sticky=W)
try:
	log_file=os.path.join(os.path.dirname('__file__'),'Teildokument','log_file')
	label_update=Label(frame_refresh_ddb, text='Last Update: '+modification_date(log_file).strftime('%d.%m.%y - %H:%M'))
except FileNotFoundError:
	label_update=Label(frame_refresh_ddb, text='Last Update: ---')
label_update.grid(row=0, column=1, sticky=E)																					  

# space= Label(hauptfenster, text="").grid(row=1,column=0,columnspan=10)
label_suchbegriffe = Label(frame_suche, text="Titelsuche: ", font=LARGE_FONT)
entry_suchbegriffe = Entry(frame_suche, width=50, font=LARGE_FONT)
label_suchbegriffe.grid(row=0, column=0, sticky=N+W)
entry_suchbegriffe.grid(row=0, column=1,sticky=E+W)
solution_var=IntVar()
cb_solution=Checkbutton(frame_suche, text='Lösung', variable=solution_var, font=HUGE_FONT)
cb_solution.grid(row=0, column=2,padx=170)	
	
	
button_suche = Button(hauptfenster, text="Suche starten!",font=HUGE_FONT,width=20,height=2,bd=5, command=control_cb)

button_suche.grid(column=1,row=3, sticky=E+S)


hauptfenster.mainloop()


