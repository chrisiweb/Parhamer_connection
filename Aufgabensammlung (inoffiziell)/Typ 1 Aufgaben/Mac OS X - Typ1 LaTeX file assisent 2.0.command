#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-

import os 
import os.path
import codecs
import subprocess
import tkinter
from tkinter import *
import sys


hauptfenster = Tk()
hauptfenster.title('Typ 1 LaTeX file assistent')
#hauptfenster.wm_iconbitmap('latex.ico')

hauptfenster.geometry('+50+50')



ag_kb=["ag11","ag12","ag21","ag22","ag23","ag24","ag25","ag31","ag32","ag33","ag34","ag35","ag41","ag42"]
AG_BB=["AG 1.1","AG 1.2","AG 2.1","AG 2.2","AG 2.3","AG 2.4","AG 2.5","AG 3.1","AG 3.2","AG 3.3","AG 3.4","AG 3.5","AG 4.1","AG 4.2"]
an_kb=["an11","an12","an13","an14","an21","an31","an32","an33","an41","an42","an43"]
AN_BB=["AN 1.1","AN 1.2","AN 1.3","AN 1.4","AN 2.1","AN 3.1","AN 3.2","AN 3.3","AN 4.1","AN 4.2","AN 4.3"]
fa_kb=["fa11","fa12","fa13","fa14","fa15","fa16","fa17","fa18","fa19","fa21","fa22","fa23","fa24","fa25","fa26","fa31","fa32","fa33","fa34","fa41","fa42","fa43","fa44","fa51","fa52","fa53","fa54","fa55","fa56","fa61","fa62","fa63","fa64","fa65","fa66"]
FA_BB=["FA 1.1","FA 1.2","FA 1.3","FA 1.4","FA 1.5","FA 1.6","FA 1.7","FA 1.8","FA 1.9","FA 2.1","FA 2.2","FA 2.3","FA 2.4","FA 2.5","FA 2.6","FA 3.1","FA 3.2","FA 3.3","FA 3.4","FA 4.1","FA 4.2","FA 4.3","FA 4.4","FA 5.1","FA 5.2","FA 5.3","FA 5.4","FA 5.5","FA 5.6","FA 6.1","FA 6.2","FA 6.3","FA 6.4","FA 6.5","FA 6.6"]
ws_kb=["ws11","ws12","ws13","ws14","ws21","ws22","ws23","ws24","ws31","ws32","ws33","ws34","ws41"]
WS_BB=["WS 1.1","WS 1.2","WS 1.3","WS 1.4","WS 2.1","WS 2.2","WS 2.3","WS 2.4","WS 3.1","WS 3.2","WS 3.3","WS 3.4","WS 4.1"]
Klassen=["K5","K6","K7","K8"]
AF_BB=["MC","ZO","LT","OA"]
af_kb=["mc","zo","lt","oa"]


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]

#########################################################################
############  Skript zu Erstellung der LaTeX Datei ######################
#########################################################################


def control_cb():
	suchbegriffe = []

	##### Suche der Schulstufe 
	# if K5.get():
		# suchbegriffe.append('K5')
	if K5_FU.get():
		suchbegriffe.append('FU')
	if K5_GL.get():
		suchbegriffe.append('GL')
	if K5_MZR.get():
		suchbegriffe.append('MZR')
	if K5_TR.get():
		suchbegriffe.append('TR')
	if K5_VAG2.get():
		suchbegriffe.append('VAG2')		
	# if K6.get():
		# suchbegriffe.append('K6')
	if K6_BSW.get():
		suchbegriffe.append('BSW')	
	if K6_FO.get():
		suchbegriffe.append('FO')
	if K6_PWLU.get():
		suchbegriffe.append('PWLU')
	if K6_RE.get():
		suchbegriffe.append('RE')
	if K6_RF.get():
		suchbegriffe.append('RF')	
	if K6_VAG3.get():
		suchbegriffe.append('VAG3')	
	# if K7.get():
		# suchbegriffe.append('K7')
	if K7_DR.get():
		suchbegriffe.append('DR')
	if K7_DWV.get():
		suchbegriffe.append('DWV')
	if K7_KKK.get():
		suchbegriffe.append('KKK')	
	if K7_KZ.get():
		suchbegriffe.append('KZ')	
	# if K8.get():
		# suchbegriffe.append('K8')
	if K8_DDG.get():
		suchbegriffe.append('DDG')
	if K8_IR.get():
		suchbegriffe.append('IR')
	if K8_SWS.get():
		suchbegriffe.append('SWS')		
	# if MAT.get():
		# suchbegriffe.append('MAT')
	
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


	
	
	beispieldaten_dateipfad = {}
	beispieldaten = []
	for root, dirs, files in os.walk(os.path.relpath(os.path.dirname(__file__))):
		for all in files:
			if all.endswith('.tex') or all.endswith('.ltx'):
				if not ('Gesamtdokument' in all) and not ('Teildokument' in all):
					file=codecs.open(os.path.join(root,all),'r', 'iso-8859-1')
					for i, line in enumerate(file):
						if not line == "\n":			
							beispieldaten_dateipfad[os.path.join(os.path.relpath(root,os.path.relpath(os.path.dirname(__file__))),all)]=line
							beispieldaten.append(line)
							break
					file.close()
	#print(beispieldaten_dateipfad)
	# print(beispieldaten)
		
 #############  Erstellung der Kompetenzbereiche pro Beispiel
	liste_kompetenzbereiche ={}
	gkliste = []
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
		
	#print(liste_kompetenzbereiche)

	
	filename_teildokument = os.path.join(os.path.dirname(__file__),'Teildokument','Teildokument.tex')
	file=codecs.open(filename_teildokument,"w", 'iso-8859-1')
	file.write("\documentclass[a4paper,12pt]{report}\n\n"
	"\\usepackage{geometry}\n"	
	"\geometry{a4paper,left=18mm,right=18mm, top=3cm, bottom=2cm}\n\n" 
	"\\usepackage{lmodern}\n"
	"\\usepackage[T1]{fontenc}\n"
	"\\usepackage{eurosym}\n"
	"\\usepackage{setspace}\n"
	"\\usepackage[latin1]{inputenc}\n"
	"\\usepackage{graphicx}\n"
	"\\usepackage[ngerman]{babel}\n"
	"\\usepackage[solution_on]{mathematik} % solution_on/off\n"
	"\\usepackage{blindtext}\n"
	"\setcounter{Zufall}{0}\n\n\n"
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
		gesammeltedateien=[]
		for r in range(1,len(liste_kompetenzbereiche)+1):
			if liste_kompetenzbereiche[r]==[]:
				del liste_kompetenzbereiche[r]	
		for r in range(1,len(liste_kompetenzbereiche)+1):
			for all in suchbegriffe:
				if r in liste_kompetenzbereiche.keys():
					if all not in liste_kompetenzbereiche[r]:
						del liste_kompetenzbereiche[r]
		# print(liste_kompetenzbereiche)
		
		
		
		for key in liste_kompetenzbereiche.keys():
			gesammeltedateien.append(beispieldaten[key-1])
		
		
		for all in gesammeltedateien[:]:
			if not len(entry_suchbegriffe.get()) ==0:
				if entry_suchbegriffe.get().lower() not in all.lower():
					gesammeltedateien.remove(all)
					
			
	if suchtyp_var.get() == ODER:
		loop_suchbegriffe=0
		#### SUCHBEGRIFFE	
		if not len(entry_suchbegriffe.get()) ==0:
			suchbegriffe.append(entry_suchbegriffe.get())
		gesammeltedateien=[]
		for loop_suchbegriffe in suchbegriffe:  ## Zusammenstellung aller Dateien, die der Suche entsprechen
			loop_ergebnis=0
			while loop_ergebnis <= len(beispieldaten)-1: 
				if loop_suchbegriffe in beispieldaten[loop_ergebnis]:
					if beispieldaten[loop_ergebnis] not in gesammeltedateien:
						gesammeltedateien.append(beispieldaten[loop_ergebnis])
				loop_ergebnis +=1

		gesammeltedateien=sorted(gesammeltedateien)

	loop_dateien=1

###############################################	
#### Auswahl der gesuchten Antwoertformate ####
###############################################

	listen={}
	check_number=1
	if suchbegriffe==[]:
		if af_MC.get() or af_ZO.get() or af_LT.get() or af_OA.get():
			for all_formats in AF_BB:
				gesammeltedateien_temporary=beispieldaten[:]
				x="af_"+all_formats+".get()"
				if eval(x):
					for all in gesammeltedateien_temporary[:]:
						if all_formats not in all: 
							gesammeltedateien_temporary.remove(all)
					listen[check_number]=gesammeltedateien_temporary
				else:
					listen[check_number]=[]
				check_number+=1
			gesammeltedateien = listen[1]+listen[2]+listen[3]+listen[4]	
	
	if af_MC.get() or af_ZO.get() or af_LT.get() or af_OA.get():
		for all_formats in AF_BB:
			gesammeltedateien_temporary=gesammeltedateien[:]
			x="af_"+all_formats+".get()"
			if eval(x):
				for all in gesammeltedateien_temporary[:]:
					if all_formats not in all: 
						gesammeltedateien_temporary.remove(all)
				suchbegriffe.append(all_formats)		
				listen[check_number]=gesammeltedateien_temporary
			else:
				listen[check_number]=[]
			check_number+=1
		gesammeltedateien = listen[1]+listen[2]+listen[3]+listen[4]

###############################################	
#### Auswahl der gesuchten Klassen #########
###############################################
	
	listen={}
	check_number=1
	if suchbegriffe==[]:
		if K5.get() or K6.get() or K7.get() or K8.get():
			for all_formats in Klassen:
				gesammeltedateien_temporary=beispieldaten[:]
				x=all_formats+".get()"
				if eval(x):
					for all in gesammeltedateien_temporary[:]:
						if all_formats not in all: 
							gesammeltedateien_temporary.remove(all)
					listen[check_number]=gesammeltedateien_temporary
				else:
					listen[check_number]=[]
				check_number+=1
			gesammeltedateien = listen[1]+listen[2]+listen[3]+listen[4]
	
	if K5.get() or K6.get() or K7.get() or K8.get():
		for all_formats in Klassen:
			gesammeltedateien_temporary=gesammeltedateien[:]
			x=all_formats+".get()"
			if eval(x):
				for all in gesammeltedateien_temporary[:]:
					if all_formats not in all: 
						gesammeltedateien_temporary.remove(all)
				suchbegriffe.append(all_formats)		
				listen[check_number]=gesammeltedateien_temporary
			else:
				listen[check_number]=[]
			check_number+=1
		gesammeltedateien = listen[1]+listen[2]+listen[3]+listen[4]

		
	print(suchbegriffe)
	# print (listen)
	# print(gesammeltedateien)


	##############################
	beispieldaten.sort(key=natural_keys)
	loop_dateien=1
	check=0
	for dateien in beispieldaten: ## Erstellung der .tex Datei 
		if dateien in gesammeltedateien:
			for key, value in beispieldaten_dateipfad.items():
				key=key.replace('\\','/')
				if dateien in value: 
					file=open(filename_teildokument,"a")
					file.write('\input{"../'+key+'"}%\n'
			'\hrule  \leer\n\n')
					file.close()
		loop_dateien +=1
	file=open(filename_teildokument,"a")
	file.write('\shorthandoff{"}\n'
	"\end{document}")
	file.close()	
	if not gesammeltedateien:
		def okbutton():
			nebenfenster.destroy()
		nebenfenster = Tk()
		nebenfenster.title('Warnung')
		nebenfenster.geometry('400x200+500+200')
		Label(nebenfenster, text="Kein Suchergebnis gefunden. \n\n Das LaTeX Dokument ist leer!", font=("", 12), pady=50).pack()
		Button(nebenfenster, text='OK', width=15, command=okbutton).pack()
		print('Keine LaTeX-Datei ausgeben!')
		
		
	
	else:
		print("Insgesamt wurde(n) " + str(len(gesammeltedateien)) + " Beispiel(e) gefunden. Entsprechende LaTeX-Datei wird ausgegeben...")
		hauptfenster.destroy()
		subprocess.call(['open', filename_teildokument])
		#os.system(filename_teildokument)
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


#########################################
### CHECKBOXEN FÜR... ########################
########################################

######## Schulstufen & Themenbereiche #######

## 5.Klasse ##
r=5
c=0

label_K5 =  Label(hauptfenster, text= "5. KLASSE", relief=GROOVE).grid(column=c, row=r,columnspan=1)
r+=1

K5_FU=IntVar()
cb_K5_FU =  Checkbutton(hauptfenster, text= "Funktionen (FU)",font=("", 7),justify=(LEFT), variable=K5_FU).grid(column=c, row=r,sticky=W,columnspan=1)
r+=1


K5_GL=IntVar()
cb_K5_GL =  Checkbutton(hauptfenster, text= "Gleichungen und\nGleichungssysteme (GL)",font=("", 7),justify=(LEFT), variable=K5_GL).grid(column=c, row=r,sticky=W, columnspan=1)
r+=1


K5_MZR=IntVar()
cb_K5_MZR =  Checkbutton(hauptfenster, text= "Mengen, Zahlen,\nRechengesetze (MZR)",font=("", 7),justify=(LEFT), variable=K5_MZR).grid(column=c, row=r,sticky=W, columnspan=1)
r+=1

K5_TR=IntVar()
cb_K5_TR =  Checkbutton(hauptfenster, text= "Trigonometrie (TR)",font=("", 7),justify=(LEFT), variable=K5_TR).grid(column=c, row=r,sticky=W, columnspan=1)
r+=1

K5_VAG2=IntVar()
cb_K5_VAG2 =  Checkbutton(hauptfenster, text= "Vektoren und analytische\nGeometrie in R2 (VAG2)",font=("", 7),justify=(LEFT), variable=K5_VAG2).grid(column=c, row=r,sticky=W, columnspan=1)
r+=2

## 6.Klasse ##

label_K6 =  Label(hauptfenster, text= "6. KLASSE", relief=GROOVE).grid(column=c, row=r, columnspan=1)
r+=1

K6_BSW=IntVar()
cb_K6_BSW =  Checkbutton(hauptfenster, text= "Beschreibene Statistik\nund Wahrscheinlichkeit (BSW)",font=("", 7),justify=(LEFT), variable=K6_BSW).grid(column=c, row=r,sticky=W, columnspan=1)
r+=1

K6_FO=IntVar()
cb_K6_FO =  Checkbutton(hauptfenster, text= "Folgen (FO)",font=("", 7),justify=(LEFT), variable=K6_FO).grid(column=c, row=r,sticky=W, columnspan=1)
r+=1

K6_PWLU=IntVar()
cb_K6_PWLU =  Checkbutton(hauptfenster, text= "Potenzen, Wurzeln, Logarithmen\nund Ungleichungen (PWLU)",font=("", 7),justify=(LEFT), variable=K6_PWLU).grid(column=c, row=r,sticky=W, columnspan=1)
r+=1

K6_RE=IntVar()
cb_K6_RE =  Checkbutton(hauptfenster, text= "Reihen (RE)",font=("", 7),justify=(LEFT), variable=K6_RE).grid(column=c, row=r,sticky=W, columnspan=1)
r+=1

K6_RF=IntVar()
cb_K6_RF =  Checkbutton(hauptfenster, text= "Reelle Funktionen (RF)",font=("", 7),justify=(LEFT), variable=K6_RF).grid(column=c, row=r,sticky=W, columnspan=1)
r+=1

K6_VAG3=IntVar()
cb_K6_VAG3 =  Checkbutton(hauptfenster, text= "Vektoren und analytische\nGeometrie in R3 und Rn (VAG3)",font=("", 7),justify=(LEFT),variable=K6_VAG3).grid(column=c, row=r,sticky=W, columnspan=1)

r-=13
## 7.Klasse ##

c=1
label_K7 =  Label(hauptfenster, text= "7. KLASSE", relief=GROOVE).grid(column=c, row=r, columnspan=1)
r+=1


K7_DR=IntVar()
cb_K7_DR =  Checkbutton(hauptfenster, text= "Differentialrechnung (DR)",font=("", 7),justify=(LEFT), variable=K7_DR).grid(column=c, row=r,sticky=W, columnspan=1)
#"Courier"
r+=1

K7_DWV=IntVar()
cb_K7_DWV =  Checkbutton(hauptfenster, text= "Diskrete Wahrscheinlichkeits-\nverteilungen (DWV)",font=("", 7),justify=(LEFT), variable=K7_DWV).grid(column=c, row=r,sticky=W, columnspan=1)
r+=1

K7_KKK=IntVar()
cb_K7_KKK =  Checkbutton(hauptfenster, text= "Kreise, Kugeln, Kegelschnittslinien \nund andere Kurven (KKK)",font=("", 7),justify=(LEFT), variable=K7_KKK).grid(column=c, row=r,sticky=W, columnspan=1)
r+=1

K7_KZ=IntVar()
cb_K7_KZ =  Checkbutton(hauptfenster, text= "Komplexe Zahlen (KZ)",font=("", 7),justify=(LEFT), variable=K7_KZ).grid(column=c, row=r,sticky=W, columnspan=1)
r+=3

## 8.Klasse ##

K8=IntVar()
label_K8 =  Label(hauptfenster, text= "8. KLASSE", relief=GROOVE).grid(column=c, row=r, columnspan=1)
r+=1

K8_DDG=IntVar()
cb_K8_DDG =  Checkbutton(hauptfenster, text= "Differenzen- und Differential-\ngleichungen; Grundlagen \nder Systemdynamik (DDG)",font=("", 7),justify=(LEFT), variable=K8_DDG).grid(column=c, row=r,sticky=W, columnspan=1)
r+=1

K8_IR=IntVar()
cb_K8_IR =  Checkbutton(hauptfenster, text= "Integralrechnung (IR)",font=("", 7),justify=(LEFT), variable=K8_IR).grid(column=c, row=r,sticky=W, columnspan=1)
r+=1

K8_SWS=IntVar()
cb_K8_SWS =  Checkbutton(hauptfenster, text= "Stetige Wahrscheinlichkeits-\nverteilungen; Beurteilende \nStatistik (SWS)",font=("", 7),justify=(LEFT), variable=K8_SWS).grid(column=c, row=r,sticky=W, columnspan=1)



#######  Rahmen #########
frame = Frame(hauptfenster, bd=5, relief=RIDGE)
frame.grid(row=19, column=10, columnspan=9)
###############################  ... Aufgabenformate ##############################
r=0
c=0

af_MC=IntVar() #value=0 oder 1
af_ZO=IntVar()
af_LT=IntVar()
af_OA=IntVar()

Aufgabenformate_header = Label(frame, text="Gewünschte Aufgabenformate:", font=("",11, 'bold')).grid(column=c, row=r, sticky=W, columnspan=3)
r+=1

cb_MC = Checkbutton(frame, text= "Multiple Choice (MC)", variable=af_MC).grid(column=c, row=r,sticky=W, columnspan=2) 
c+=2
cb_ZO = Checkbutton(frame, text= "Zuordnen (ZO)", variable=af_ZO).grid(column=c, row=r,sticky=W, columnspan=2) 

c+=2
cb_LT = Checkbutton(frame, text= "Lückentext (LT)", variable=af_LT).grid(column=c, row=r,sticky=W, columnspan=2) 

c+=2
cb_OA = Checkbutton(frame, text= "Offenes Antwortformat (OA)", variable=af_OA).grid(column=c, row=r,sticky=W, columnspan=2) 

##################### Suche nach Klassen #######################
K5=IntVar()
K6=IntVar()
K7=IntVar()
K8=IntVar()
c=0
r+=1
Aufgabenformate_header = Label(frame, text="Klassen:", font=("",11, 'bold')).grid(column=c, row=r, sticky=W, columnspan=2)
r+=1
cb_K5 =  Checkbutton(frame, text= "5. KLASSE", variable=K5).grid(column=c, row=r,sticky=W, columnspan=2)
c+=2
cb_K6 =  Checkbutton(frame, text= "6. KLASSE", variable=K6).grid(column=c, row=r,sticky=W, columnspan=2)
c+=2
cb_K7 =  Checkbutton(frame, text= "7. KLASSE", variable=K7).grid(column=c, row=r,sticky=W, columnspan=2)
c+=2

cb_K8 =  Checkbutton(frame, text= "8. KLASSE", variable=K8).grid(column=c, row=r,sticky=W, columnspan=2)


########## ... ALGEBRA UND GEOMETRIE ###############
r=5
c=10
py=5
ag_cb_all=[]
ag_all=IntVar()
Button(hauptfenster, text='Algebra und Geoemtrie:', command=ag_select_all).grid(column=c, row=r,sticky=W, columnspan=2)

r+=1
for all in ag_kb:
	vars()[all]=IntVar()
	cb_ag = Checkbutton(hauptfenster, text=AG_BB[ag_kb.index(all)], variable = vars()[all])
	cb_ag.grid(column=c, row=r, pady=py, sticky=W)
	ag_cb_all.append(vars()[all])
	r+=1
	if r>12:
		r-=7
		c+=1


				
################# ... ANALYSIS ###############
space = Label(hauptfenster, text="          ")
space.grid(column=c, row=5, sticky=E)
c+=1

r=5
an_cb_all=[]
an_all=IntVar()
Button(hauptfenster, text='Analysis:', command=an_select_all).grid(column=c, row=r,sticky=W, columnspan=2)	
r+=1
for all in an_kb:
	vars()[all]=IntVar()
	cb_an = Checkbutton(hauptfenster, text=AN_BB[an_kb.index(all)], variable = vars()[all])
	cb_an.grid(column=c, row=r, pady=py, sticky=W)
	an_cb_all.append(vars()[all])
	r+=1
	if r>12:
		r-=7
		c+=1
		
c+=1
space = Label(hauptfenster, text="          ")
space.grid(column=c, row=5, sticky=E)
c+=1	

############ ... FUNKTIONALE ABHÄNGIGKEITEN ###############################	
r=5
fa_cb_all=[]
fa_all=IntVar()
Button(hauptfenster, text='Funktionale Abhängigkeiten:', command=fa_select_all).grid(column=c, row=r,sticky=W, columnspan=3)		
r+=1
for all in fa_kb:
	vars()[all]=IntVar()
	cb_fa = Checkbutton(hauptfenster, text=FA_BB[fa_kb.index(all)], variable = vars()[all])
	cb_fa.grid(column=c, row=r, pady=py, sticky=W)
	fa_cb_all.append(vars()[all])
	r+=1
	if r>14:
		r-=9
		c+=1

c+=1
space = Label(hauptfenster, text="          ")
space.grid(column=c, row=5, sticky=E)
c+=1	

################## 	 ... WAHRSCHEINLICHKEIT UND STATISTIK ########################
r=5
ws_cb_all=[]
ws_all=IntVar()
Button(hauptfenster, text='Wahrscheinlichkeit und Statistik:', command=ws_select_all).grid(column=c, row=r,sticky=W, columnspan=2)	
r+=1
for all in ws_kb:
	vars()[all]=IntVar()
	cb_ws = Checkbutton(hauptfenster, text=WS_BB[ws_kb.index(all)], variable = vars()[all])
	cb_ws.grid(column=c, row=r, pady=py, sticky=W)
	ws_cb_all.append(vars()[all])
	r+=1
	if r>12:
		r-=7
		c+=1	

c+=1
space = Label(hauptfenster, text="          ")
space.grid(column=c, row=5, sticky=E)


##########################################################################################

UND='alle Suchkriterien enthalten.'
ODER='zumindest ein Suchkriterium enthalten.'
suchtyp_var = StringVar()
label_suchtyp= Label(hauptfenster, text="Alle Dateien ausgeben, die")
suchtyp = OptionMenu(hauptfenster,suchtyp_var,ODER,UND)
suchtyp_var.set(ODER)
label_suchtyp.grid(row=0, column=10, columnspan=2)
suchtyp.grid(row=0, column=12, columnspan=6,sticky=W)



space= Label(hauptfenster, text="").grid(row=1,column=0,columnspan=10)
label_suchbegriffe = Label(hauptfenster, text="Titelsuche:")
entry_suchbegriffe = Entry(hauptfenster, width=80)
label_suchbegriffe.grid(row=16, column=10, columnspan=5, sticky=W)
entry_suchbegriffe.grid(row=17, column=10, columnspan=10,  sticky=W)	
	
	
login = Button(hauptfenster, text="Suche",font=("",13), command=control_cb, width=20,height = 3)
# login.pack(padx=5, pady=10, side=RIGHT)

login.grid(column=20,row=19, columnspan=4, rowspan=3)
hauptfenster.mainloop()


