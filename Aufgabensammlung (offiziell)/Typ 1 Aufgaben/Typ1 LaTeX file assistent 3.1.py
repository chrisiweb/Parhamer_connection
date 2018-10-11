import sys
import os 
import os.path
import subprocess
import tkinter
from tkinter import *


hauptfenster = Tk()
hauptfenster.title('Typ 1 LaTeX file assistent')
#hauptfenster.wm_iconbitmap('latex.ico')

hauptfenster.geometry('+50+50')


ag_kb=["ag11","ag12","ag21","ag22","ag23","ag24","ag25","ag31","ag32","ag33","ag34","ag35","ag41","ag42"]
ag_kb_beschreibung={
"ag11":'Wissen über die Zahlenmengen N, Z, Q, R, C verständig einsetzen können',
"ag12":'Wissen über algebraische Begriffe angemessen einsetzen können: \n Variable, Terme, Formeln, (Un-)Gleichungen, Gleichungssysteme; Äquivalenz, Umformungen, Lösbarkeit',
"ag21":'Einfache Terme und Formeln aufstellen, umformen und im Kontext deuten können',
"ag22":'Lineare Gleichungen aufstellen, interpretieren, umformen/lösen und die Lösung im Kontext deuten können',
"ag23":'Quadratische Gleichungen in einer Variablen umformen/lösen, über Lösungsfälle Bescheid wissen,\n Lösungen und Lösungsfälle (auch geometrisch) deuten können',
"ag24":'Lineare Ungleichungen aufstellen, interpretieren, umformen/lösen, Lösungen (auch geometrisch) deuten können',
"ag25":'Lineare Gleichungssysteme in zwei Variablen aufstellen, interpretieren, umformen/lösen,\n über Lösungsfälle Bescheid wissen, Lösungen und Lösungsfälle (auch geometrisch) deuten können',
"ag31":'Vektoren als Zahlentupel verständig einsetzen und im Kontext deuten können',
"ag32":'Vektoren geometrisch (als Punkte bzw. Pfeile) deuten und verständig einsetzen können',
"ag33":'Definition der Rechenoperationen mit Vektoren (Addition, Multiplikation mit einem Skalar, Skalarmultiplikation) kennen,\n Rechenoperationen verständig einsetzen und (auch geometrisch) deuten können',
"ag34":'Geraden durch (Parameter-)Gleichungen in R2 und R3 angeben können; Geradengleichungen interpretieren können;\n Lagebeziehungen (zwischen Geraden und zwischen Punkt und Gerade) analysieren, Schnittpunkte ermitteln können',
"ag35":'Normalvektoren in R2 aufstellen, verständig einsetzen und interpretieren können',
"ag41":'Definitionen von Sinus, Cosinus, Tangens im rechtwinkligen Dreieck kennen und zur Auflösung rechtwinkliger Dreiecke einsetzen können',
"ag42":'Definitionen von Sinus, Cosinus für Winkel größer als 90° kennen und einsetzen können'}
AG_BB=["AG 1.1","AG 1.2","AG 2.1","AG 2.2","AG 2.3","AG 2.4","AG 2.5","AG 3.1","AG 3.2","AG 3.3","AG 3.4","AG 3.5","AG 4.1","AG 4.2"]
an_kb=["an11","an12","an13","an14","an21","an31","an32","an33","an41","an42","an43"]
an_kb_beschreibung={"an11":'Absolute und relative (prozentuelle) Änderungsmaße unterscheiden und angemessen verwenden können',
"an12":'Den Zusammenhang Differenzenquotient (mittlere Änderungsrate) – Differentialquotient („momentane“ Änderungsrate) auf der Grundlage \n eines intuitiven Grenzwertbegriffes kennen und damit (verbal und auch in formaler Schreibweise) auch kontextbezogen anwenden können',
"an13":'Den Differenzen- und Differentialquotienten in verschiedenen Kontexten deuten und \n entsprechende Sachverhalte durch den Differenzen- bzw. Differentialquotienten beschreiben können',
"an14":'Das systemdynamische Verhalten von Größen durch Differenzengleichungen beschreiben bzw. diese im Kontext deuten können',
"an21":'Einfache Regeln des Differenzierens kennen und anwenden können: Potenzregel, Summenregel, Regeln für k*f(x)′ und f(k*x)′',
"an31":'Den Begriff Ableitungsfunktion/Stammfunktion kennen und zur Beschreibung von Funktionen einsetzen können',
"an32":'Den Zusammenhang zwischen Funktion und Ableitungsfunktion (bzw. Funktion und Stammfunktion)\n in deren grafischer Darstellung erkennen und beschreiben können',
"an33":'Eigenschaften von Funktionen mithilfe der Ableitung(sfunktion) beschreiben können:\n Monotonie, lokale Extrema, Links- und Rechtskrümmung, Wendestellen',
"an41":'Den Begriff des bestimmten Integrals als Grenzwert einer Summe von Produkten deuten und beschreiben können',
"an42":'Einfache Regeln des Integrierens kennen und anwenden können: Potenzregel, Summenregel, ∫k*f(x)dx, ∫f(k*x)dx;\n bestimmte Integrale von Polynomfunktionen ermitteln können',
"an43":'Das bestimmte Integral in verschiedenen Kontexten deuten und entsprechende Sachverhalte durch Integrale beschreiben können'}
AN_BB=["AN 1.1","AN 1.2","AN 1.3","AN 1.4","AN 2.1","AN 3.1","AN 3.2","AN 3.3","AN 4.1","AN 4.2","AN 4.3"]
fa_kb=["fa11","fa12","fa13","fa14","fa15","fa16","fa17","fa18","fa19","fa21","fa22","fa23","fa24","fa25","fa26","fa31","fa32","fa33","fa34","fa41","fa42","fa43","fa44","fa51","fa52","fa53","fa54","fa55","fa56","fa61","fa62","fa63","fa64","fa65","fa66"]
fa_kb_beschreibung={
"fa11":'Für gegebene Zusammenhänge entscheiden können, ob man sie als Funktionen betrachten kann ',
"fa12":'Formeln als Darstellung von Funktionen interpretieren und den Funktionstyp zuordnen können',
"fa13":'Zwischen tabellarischen und grafischen Darstellungen funktionaler Zusammenhänge wechseln können',
"fa14":'Aus Tabellen, Graphen und Gleichungen von Funktionen Werte(paare) ermitteln und im Kontext deuten können',
"fa15":'Eigenschaften von Funktionen erkennen, benennen, im Kontext deuten und zum Erstellen von Funktionsgraphen einsetzen können:\n Monotonie, Monotoniewechsel (lokale Extrema), Wendepunkte, Periodizität, Achsensymmetrie, asymptotisches Verhalten, Schnittpunkte mit den Achsen',
"fa16":'Schnittpunkte zweier Funktionsgraphen grafisch und rechnerisch ermitteln und im Kontext interpretieren können',
"fa17":'Funktionen als mathematische Modelle verstehen und damit verständig arbeiten können',
"fa18":'Durch Gleichungen (Formeln) gegebene Funktionen mit mehreren Veränderlichen im Kontext deuten können, Funktionswerte ermitteln können',
"fa19":'Einen Überblick über die wichtigsten (unten angeführten) Typen mathematischer Funktionen geben, ihre Eigenschaften vergleichen können',
"fa21":'Verbal, tabellarisch, grafisch oder durch eine Gleichung (Formel) gegebene lineare Zusammenhänge als lineare Funktionen erkennen\n bzw. betrachten können; zwischen diesen Darstellungsformen wechseln können',
"fa22":'Aus Tabellen, Graphen und Gleichungen linearer Funktionen Werte(paare) sowie die Parameter k und d ermitteln und im Kontext deuten können',
"fa23":'Die Wirkung der Parameter k und d kennen und die Parameter in unterschiedlichen Kontexten deuten können',
"fa24":'Charakteristische Eigenschaften von lineare Funktionen kennen und im Kontext deuten können',
"fa25":'Die Angemessenheit einer Beschreibung mittels linearer Funktion bewerten können',
"fa26":'Direkte Proportionalität als lineare Funktion vom Typ f(x) = k*x beschreiben können',
"fa31":'Verbal, tabellarisch, grafisch oder durch eine Gleichung (Formel) gegebene Zusammenhänge dieser Art als entsprechende Potenzfunktionen erkennen\n bzw. betrachten können; zwischen diesen Darstellungsformen wechseln können',
"fa32":'Aus Tabellen, Graphen und Gleichungen von Potenzfunktionen Werte(paare) sowie die Parameter a und b ermitteln und im Kontext deuten können',
"fa33":'Die Wirkung der Parameter a und b bei Potenzfunktionen kennen und die Parameter im Kontext deuten können',
"fa34":'Indirekte Proportionalität als Potenzfunktion vom Typ f(x)=a/x beschreiben können',
"fa41":'Typische Verläufe von Graphen in Abhängigkeit vom Grad der Polynomfunktion (er)kennen',
"fa42":'Zwischen tabellarischen und grafischen Darstellungen von Zusammenhängen dieser Art wechseln können',
"fa43":'Aus Tabellen, Graphen und Gleichungen von Polynomfunktionen Funktionswerte, aus Tabellen und Graphen\n sowie aus einer quadratischen Funktionsgleichung Argumentwerte ermitteln können',
"fa44":'Den Zusammenhang zwischen dem Grad der Polynomfunktion und der Anzahl der Null-, Extrem- und Wendestellen wissen',
"fa51":'Verbal, tabellarisch, grafisch oder durch eine Gleichung (Formel) gegebene exponentielle Zusammenhänge als Exponentialfunktion erkennen\n bzw. betrachten können; zwischen diesen Darstellungsformen wechseln können',
"fa52":'Aus Tabellen, Graphen und Gleichungen von Exponentialfunktionen Werte(paare) ermitteln und im Kontext deuten können',
"fa53":'Die Wirkung der Parameter a und b (bzw. e^λ) kennen und die Parameter in unterschiedlichen Kontexten deuten können',
"fa54":'Charakteristische Eigenschaften von Exponentialfunktionen kennen und im Kontext deuten können',
"fa55":'Die Begriffe „Halbwertszeit“ und „Verdoppelungszeit“ kennen, die entsprechenden Werte berechnen und im Kontext deuten können',
"fa56":'Die Angemessenheit einer Beschreibung mittels Exponentialfunktion bewerten können',
"fa61":'Grafisch oder durch eine Gleichung (Formel) gegebene Zusammenhänge der Art f(x) = a*sin(b*x) als Allgemeine Sinusfunktion erkennen\n bzw. betrachten können; zwischen diesen Darstellungsformen wechseln können',
"fa62":'Aus Graphen und Gleichungen von Allgemeinen Sinusfunktionen Werte(paare) ermitteln und im Kontext deuten können',
"fa63":'Die Wirkung der Parameter a und b bei Winkelfunktionen kennen und die Parameter im Kontext deuten können',
"fa64":'Periodizität als charakteristische Eigenschaft kennen und im Kontext deuten können',
"fa65":'Wissen, dass cos(x)=sin(x+π/2)',
"fa66":'Wissen, dass gilt: sin(x)′=cos(x) und cos(x)′=-sin(x)'}
FA_BB=["FA 1.1","FA 1.2","FA 1.3","FA 1.4","FA 1.5","FA 1.6","FA 1.7","FA 1.8","FA 1.9","FA 2.1","FA 2.2","FA 2.3","FA 2.4","FA 2.5","FA 2.6","FA 3.1","FA 3.2","FA 3.3","FA 3.4","FA 4.1","FA 4.2","FA 4.3","FA 4.4","FA 5.1","FA 5.2","FA 5.3","FA 5.4","FA 5.5","FA 5.6","FA 6.1","FA 6.2","FA 6.3","FA 6.4","FA 6.5","FA 6.6"]
ws_kb=["ws11","ws12","ws13","ws14","ws21","ws22","ws23","ws24","ws31","ws32","ws33","ws34","ws41"]
ws_kb_beschreibung={
"ws11":'Werte aus tabellarischen und elementaren grafischen Darstellungen ablesen (bzw. zusammengesetzte Werte ermitteln)\n und im jeweiligen Kontext angemessen interpretieren können',
"ws12":'Tabellen und einfache statistische Grafiken erstellen, zwischen Darstellungsformen wechseln können',
"ws13":'Statistische Kennzahlen (absolute und relative Häufigkeiten; arithmetisches Mittel, Median, Modus; Quartile; Spannweite, empirische Varianz/\nStandardabweichung) im jeweiligen Kontext interpretieren können; die angeführten Kennzahlen für einfache Datensätze ermitteln können',
"ws14":'Definition und wichtige Eigenschaften des arithmetischen Mittels und des Medians angeben und nutzen,\n Quartile ermitteln und interpretieren können, die Entscheidung für die Verwendung einer bestimmten Kennzahl begründen können',
"ws21":'Grundraum und Ereignisse in angemessenen Situationen verbal bzw. formal angeben können',
"ws22":'Relative Häufigkeit als Schätzwert von Wahrscheinlichkeit verwenden und anwenden können',
"ws23":'Wahrscheinlichkeit unter der Verwendung der Laplace-Annahme (Laplace Wahrscheinlichkeit) berechnen und interpretieren können,\n Additionsregel und Multiplikationsregel anwenden und interpretieren können',
"ws24":'Binomialkoeffizient berechnen und interpretieren können',
"ws31":'Die Begriffe Zufallsvariable, (Wahrscheinlichkeits-)Verteilung, Erwartungswert und Standardabweichung verständig deuten und einsetzen können',
"ws32":'Binomialverteilung als Modell einer diskreten Verteilung kennen – Erwartungswert & Varianz/Standardabweichung binomialverteilter Zufallsgrößen ermitteln\n können, Wahrsch.vert. binomialverteilter Zufallsgrößen angeben können, Arbeiten mit der Binomialverteilung in anwendungsorientierten Bereichen',
"ws33":'Situationen erkennen und beschreiben können, in denen mit Binomialverteilung modelliert werden kann',
"ws34":'Normalapproximation der Binomialverteilung interpretieren und anwenden können',
"ws41":'Konfidenzintervalle als Schätzung für eine Wahrscheinlichkeit oder einen unbekannten Anteil p interpretieren (frequentistische Deutung) und verwenden\n können, Berechnungen auf Basis der Binomialverteilung oder einer durch die Normalverteilung approximierten Binomialverteilung durchführen können'}
WS_BB=["WS 1.1","WS 1.2","WS 1.3","WS 1.4","WS 2.1","WS 2.2","WS 2.3","WS 2.4","WS 3.1","WS 3.2","WS 3.3","WS 3.4","WS 4.1"]
Klassen=["K5","K6","K7","K8"]
AF_BB=["MC","ZO","LT","OA"]
aufgaben_formate={"mc":'Multiple Choice',"zo":'Zuordnen',"lt":'Lückentext',"oa":'Offenes Antwortformat'}
# klassen=['K5','K6','K7','K8']
# klasse_5=['FU', 'GL','MZR','TR','VAG2']
themen_klasse_5={'FU':'Funktionen', 'GL':'Gleichungen und\nGleichungssysteme',
'MZR':'Mengen, Zahlen,\nRechengesetze','TR':'Trigonometrie',
'VAG2':'Vektoren und analytische\nGeometrie'}
themen_klasse_6={'BSW':'Beschreibende Statistik\nund Wahrscheinlichkeit','FO':'Folgen',
'PWLU':'Potenzen, Wurzeln, Logarithmen\nund Ungleichungen','RE':'Reihen',
'RF':'Reelle Funktionen','VAG3':'Vektoren und analytische\nGeometrie in R3 und Rn'}
themen_klasse_7={'DR':'Differentialrechnung','DWV':'Diskrete Wahrscheinlichkeits-\nverteilungen',
'KKK':'Kreise, Kugeln, Kegelschnittslinien\nund andere Kurven','KZ':'Komplexe Zahlen'}
themen_klasse_8={'DDG':'Differenzen- und Differential-\ngleichungen; Grundlagen\nder Systemdynamik','IR':'Integralrechnung',
'SWS':'Stetgie Wahrscheinlichkeits-\nverteilungen; Beurteilende\nStatistik'}



class hoverover(Frame):
	def __init__(self,gk_name, gk_explanation, gk_variable):
		Frame.__init__(self)
		self.gk_explanation=gk_explanation
		self.l1 = Checkbutton(self, text=gk_name, variable=gk_variable)
		self.l1.grid()
		self.l1.bind("<Enter>",self.on_enter)
		self.l1.bind("<Leave>", self.on_leave)
		
	def on_enter(self,event):
		explanation.configure(text=self.gk_explanation,bg='lightsteelblue')

	def on_leave(self, enter):
		explanation.configure(text="",bg='SystemMenu')	
	


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


	
	
	beispieldaten_dateipfad = {}
	beispieldaten = []
	for root, dirs, files in os.walk('.'):
		for all in files:
			if all.endswith('.tex') or all.endswith('.ltx'):
				if not ('Gesamtdokument' in all) and not ('Teildokument' in all):
					file=open(os.path.join(root,all))
					for i, line in enumerate(file):
						if not line == "\n":			
							beispieldaten_dateipfad[os.path.join(root,all)]=line
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

	
	filename_teildokument = os.path.join(os.path.dirname('__file__'),'Teildokument','Teildokument.tex')
	file=open(filename_teildokument,"w")
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
		if not len(entry_suchbegriffe.get()) ==0:
			suchbegriffe.append(entry_suchbegriffe.get())
			for all in beispieldaten:
				if entry_suchbegriffe.get().lower() in all.lower():
					if all not in gesammeltedateien:
						gesammeltedateien.append(all)
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
					file.write('\input{".'+key+'"}%\n'
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
		#subprocess.call(['open', filename_teildokument])
		os.system(filename_teildokument)
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

r=5
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
	beschriftung =  Button(hauptfenster, text= "%s. KLASSE"%x, command=eval('select_all_klasse%s'%x)).grid(column=c, row=r,columnspan=1)
	# beschriftung =  Label(hauptfenster, text= "%s. KLASSE"%x, relief=GROOVE).grid(column=c, row=r,columnspan=1)
	r+=1
	for all in eval('themen_klasse_%s'%x):
		y='K%s_'%x+all
		vars()[y]=IntVar()
		name = eval('themen_klasse_%s[all]'%x) + ' ('+all+')'
		cb_temporary= Checkbutton(hauptfenster, text= name,font=("", 7),justify=(LEFT), variable=vars()[y]).grid(column=c, row=r,sticky=W)
		r+=1



#######  Rahmen #########
frame = Frame(hauptfenster, bd=5, relief=RIDGE)
frame.grid(row=20, column=10, columnspan=9)
###############################  ... Aufgabenformate ##############################
r=0
c=0

Aufgabenformate_header = Label(frame, text="Gewünschte Aufgabenformate:", font=("",11, 'bold')).grid(column=c, row=r, sticky=W, columnspan=3)
r+=1

for all in aufgaben_formate:
	y='af_'+all.upper()
	vars()[y]=IntVar()
	name=aufgaben_formate[all] +' ('+all.upper()+')'
	cb_format= Checkbutton(frame, text=name , variable=vars()[y]).grid(column=c, row=r,sticky=W, columnspan=2)
	c+=2
	

##################### Suche nach Klassen #######################

c=0
r+=1
Aufgabenformate_header = Label(frame, text="Klassen:", font=("",11, 'bold')).grid(column=c, row=r, sticky=W, columnspan=2)
r+=1
for x in range(5,9):
	y='K%s'%x
	vars()[y]=IntVar()
	cb_suche_klasse=Checkbutton(frame, text= "%s. KLASSE"%x, variable=vars()[y]).grid(column=c, row=r,sticky=W, columnspan=2)
	if x!=8:
		c+=2
	

########## ... ALGEBRA UND GEOMETRIE ###############
r=5
c=10
py=5
ag_cb_all=[]
ag_all=IntVar()
Button(hauptfenster, text='Algebra und Geometrie:', command=ag_select_all).grid(column=c, row=r,sticky=W, columnspan=2)

r+=1
for all in ag_kb:
	vars()[all]=IntVar()
	hoverover(AG_BB[ag_kb.index(all)], ag_kb_beschreibung[all], vars()[all]).grid(column=c, row=r, pady=py, sticky=W)
	# cb_ag = Checkbutton(hauptfenster, text=AG_BB[ag_kb.index(all)], variable = vars()[all])
	# cb_ag.grid(column=c, row=r, pady=py, sticky=W)
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
	hoverover(AN_BB[an_kb.index(all)], an_kb_beschreibung[all], vars()[all]).grid(column=c, row=r, pady=py, sticky=W)
	# cb_an = Checkbutton(hauptfenster, text=AN_BB[an_kb.index(all)], variable = vars()[all])
	# cb_an.grid(column=c, row=r, pady=py, sticky=W)
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
	hoverover(FA_BB[fa_kb.index(all)], fa_kb_beschreibung[all], vars()[all]).grid(column=c, row=r, pady=py, sticky=W)
	# cb_fa = Checkbutton(hauptfenster, text=FA_BB[fa_kb.index(all)], variable = vars()[all])
	# cb_fa.grid(column=c, row=r, pady=py, sticky=W)
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
	hoverover(WS_BB[ws_kb.index(all)], ws_kb_beschreibung[all], vars()[all]).grid(column=c, row=r, pady=py, sticky=W)
	# cb_ws = Checkbutton(hauptfenster, text=WS_BB[ws_kb.index(all)], variable = vars()[all])
	# cb_ws.grid(column=c, row=r, pady=py, sticky=W)
	ws_cb_all.append(vars()[all])
	r+=1
	if r>12:
		r-=7
		c+=1	

c+=1
space = Label(hauptfenster, text="          ")
space.grid(column=c, row=5, sticky=E)

# hoverover('Ich teste','Das ist der wahre und lange Test','testl1').grid(row=30)

##########################################################################################

UND='alle Suchkriterien enthalten.'
ODER='zumindest ein Suchkriterium enthalten.'
suchtyp_var = StringVar()
label_suchtyp= Label(hauptfenster, text="Alle Dateien ausgeben, die")
suchtyp = OptionMenu(hauptfenster,suchtyp_var,ODER,UND)
suchtyp_var.set(ODER)
label_suchtyp.grid(row=0, column=10, columnspan=2)
suchtyp.grid(row=0, column=12, columnspan=6,sticky=W)


explanation = Label(hauptfenster,text="",width=118,height=2)	
explanation.grid(row=15,column=10, columnspan=30,sticky=W)


space= Label(hauptfenster, text="").grid(row=1,column=0,columnspan=10)
label_suchbegriffe = Label(hauptfenster, text="Titelsuche:")
entry_suchbegriffe = Entry(hauptfenster, width=80)
label_suchbegriffe.grid(row=16, column=10, columnspan=5, sticky=W)
entry_suchbegriffe.grid(row=17, column=10, columnspan=10,  sticky=W)	
	
	
button_suche = Button(hauptfenster, text="Suche",font=("",13), command=control_cb, width=20,height = 3)
# login.pack(padx=5, pady=10, side=RIGHT)

button_suche.grid(column=20,row=18, columnspan=4, rowspan=3)


hauptfenster.mainloop()


