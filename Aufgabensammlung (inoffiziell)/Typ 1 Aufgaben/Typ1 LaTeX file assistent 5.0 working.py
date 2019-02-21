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

ag_kb=["ag11","ag12","agL13","agL14","agL15",
"ag21","ag22","ag23","ag24","ag25","agL26","agL27","agL28",
"ag31","ag32","ag33","ag34","ag35","agL36","agL37","agL38","agL39",
"ag41","ag42","agL43","agL44",
"agL51","agL52","agL53"]
ag_kb_beschreibung={
"ag11":'Wissen über die Zahlenmengen N, Z, Q, R, C verständig einsetzen können',
"ag12":'Wissen über algebraische Begriffe angemessen einsetzen können: \n Variable, Terme, Formeln, (Un-)Gleichungen, Gleichungssysteme; Äquivalenz, Umformungen, Lösbarkeit',
"agL13":'Mit Aussagen und Mengen umgehen können',
"agL14":'Zahlen in einem nichtdekadischen Zahlensystem darstellen können',
"agL15":'Komplexe Zahlen in der Gauß’schen Zahlenebene darstellen und mit komplexen Zahlen rechnen können.',
"ag21":'Einfache Terme und Formeln aufstellen, umformen und im Kontext deuten können',
"ag22":'Lineare Gleichungen aufstellen, interpretieren, umformen/lösen und die Lösung im Kontext deuten können',
"ag23":'Quadratische Gleichungen in einer Variablen umformen/lösen, über Lösungsfälle Bescheid wissen,\n Lösungen und Lösungsfälle (auch geometrisch) deuten können',
"ag24":'Lineare Ungleichungen aufstellen, interpretieren, umformen/lösen, Lösungen (auch geometrisch) deuten können',
"ag25":'Lineare Gleichungssysteme in zwei Variablen aufstellen, interpretieren, umformen/lösen,\n über Lösungsfälle Bescheid wissen, Lösungen und Lösungsfälle (auch geometrisch) deuten können',
"agL26":'Den Satz von Vieta kennen und anwenden können',
"agL27":'Lineare Gleichungssysteme in drei Variablen lösen können',
"agL28":'Den Fundamentalsatz der Algebra kennen und seine Bedeutung bei der Zahlenbereichserweiterung von R auf C erläutern können',
"ag31":'Vektoren als Zahlentupel verständig einsetzen und im Kontext deuten können',
"ag32":'Vektoren geometrisch (als Punkte bzw. Pfeile) deuten und verständig einsetzen können',
"ag33":'Definition der Rechenoperationen mit Vektoren (Addition, Multiplikation mit einem Skalar, Skalarmultiplikation) kennen,\n Rechenoperationen verständig einsetzen und (auch geometrisch) deuten können',
"ag34":'Geraden durch (Parameter-)Gleichungen in R2 und R3 angeben können; Geradengleichungen interpretieren können;\n Lagebeziehungen (zwischen Geraden und zwischen Punkt und Gerade) analysieren, Schnittpunkte ermitteln können',
"ag35":'Normalvektoren in R2 aufstellen, verständig einsetzen und interpretieren können',
"agL36":'Die geometrische Bedeutung des Skalarprodukts kennen und den Winkel zwischen zwei Vektoren ermitteln können',
"agL37":'Einheitsvektoren ermitteln, verständig einsetzen und interpretieren können',
"agL38":'Definition des vektoriellen Produkts und seine geometrische Bedeutung kennen',
"agL39":'Wissen, wodurch Ebenen festgelegt sind; Ebenen in Parameter- und Normalvektordarstellung aufstellen können',
"ag41":'Definitionen von Sinus, Cosinus, Tangens im rechtwinkligen Dreieck kennen und zur Auflösung rechtwinkliger Dreiecke einsetzen können',
"ag42":'Definitionen von Sinus, Cosinus für Winkel größer als 90° kennen und einsetzen können',
"agL43":'Einfache Berechnungen an allgemeinen Dreiecken, an Figuren und Körpern (auch mittels Sinus- und Cosinussatz) durchführen können',
"agL44":'Polarkoordinaten kennen und einsetzen können',
"agL51":'Kegelschnitte in der Ebene durch Gleichungen beschreiben können; aus einer Kreisgleichung Mittelpunkt und Radius bestimmen können',
"agL52":'Die gegenseitige Lage von Kegelschnitt und Gerade ermitteln können',
"agL53":'Kugeln durch Gleichungen beschreiben können',}
AG_BB=["AG 1.1","AG 1.2","AG-L 1.3","AG-L 1.4","AG-L 1.5",
"AG 2.1","AG 2.2","AG 2.3","AG 2.4","AG 2.5","AG-L 2.6","AG-L 2.7","AG-L 2.8",
"AG 3.1","AG 3.2","AG 3.3","AG 3.4","AG 3.5","AG-L 3.6","AG-L 3.7","AG-L 3.8","AG-L 3.9",
"AG 4.1","AG 4.2","AG-L 4.3","AG-L 4.4",
"AG-L 5.1","AG-L 5.2","AG-L 5.3"]
an_kb=["an11","an12","an13","an14","anL15","an21","anL22","an31","an32","an33","anL34","an41","an42","an43"]
an_kb_beschreibung={"an11":'Absolute und relative (prozentuelle) Änderungsmaße unterscheiden und angemessen verwenden können',
"an12":'Den Zusammenhang Differenzenquotient (mittlere Änderungsrate) – Differentialquotient („momentane“ Änderungsrate) auf der Grundlage \n eines intuitiven Grenzwertbegriffes kennen und damit (verbal und auch in formaler Schreibweise) auch kontextbezogen anwenden können',
"an13":'Den Differenzen- und Differentialquotienten in verschiedenen Kontexten deuten und \n entsprechende Sachverhalte durch den Differenzen- bzw. Differentialquotienten beschreiben können',
"an14":'Das systemdynamische Verhalten von Größen durch Differenzengleichungen beschreiben bzw. diese im Kontext deuten können',
"anL15":"Einfache Differentialgleichungen, insbesondere f'(x)= k*f(x), lösen können",
"an21":'Einfache Regeln des Differenzierens kennen und anwenden können: Potenzregel, Summenregel, Regeln für k*f(x)′ und f(k*x)′',
"anL22":'Kettenregel kennen und anwenden können',
"an31":'Den Begriff Ableitungsfunktion/Stammfunktion kennen und zur Beschreibung von Funktionen einsetzen können',
"an32":'Den Zusammenhang zwischen Funktion und Ableitungsfunktion (bzw. Funktion und Stammfunktion)\n in deren grafischer Darstellung erkennen und beschreiben können',
"an33":'Eigenschaften von Funktionen mithilfe der Ableitung(sfunktion) beschreiben können:\n Monotonie, lokale Extrema, Links- und Rechtskrümmung, Wendestellen',
"anL34":'Zielfunktionen in einer Variablen für Optimierungsaufgaben (Extremwertaufgaben) aufstellen und globale Extremstellen ermitteln können',
"an41":'Den Begriff des bestimmten Integrals als Grenzwert einer Summe von Produkten deuten und beschreiben können',
"an42":'Einfache Regeln des Integrierens kennen und anwenden können: Potenzregel, Summenregel, ∫k*f(x)dx, ∫f(k*x)dx;\n bestimmte Integrale von Polynomfunktionen ermitteln können',
"an43":'Das bestimmte Integral in verschiedenen Kontexten deuten und entsprechende Sachverhalte durch Integrale beschreiben können'}
AN_BB=["AN 1.1","AN 1.2","AN 1.3","AN 1.4","AN-L 1.5","AN 2.1","AN-L 2.2",
"AN 3.1","AN 3.2","AN 3.3","AN-L 3.4",
"AN 4.1","AN 4.2","AN 4.3"]
fa_kb=["fa11","fa12","fa13","fa14","fa15","fa16","fa17","fa18","fa19",
"fa21","fa22","fa23","fa24","fa25","fa26",
"fa31","fa32","fa33","fa34",
"fa41","fa42","fa43","fa44",
"fa51","fa52","fa53","fa54","fa55","fa56",
"fa61","fa62","fa63","fa64","fa65","fa66",
"faL71","faL72","faL73","faL74",
"faL81","faL82","faL83","faL84"]
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
"fa66":'Wissen, dass gilt: sin(x)′=cos(x) und cos(x)′=-sin(x)',
"faL71":'Zahlenfolgen (insbesondere arithmetische und geometrische Folgen) durch explizite und rekursive Bildungsgesetze beschreiben und\n graphisch darstellen können',
"faL72":'Zahlenfolgen als Funktionen über N bzw. N* auffassen können, insbesondere arithmetische Folgen als lineare Funktionen und\n geometrische Folgen als Exponentialfunktionen',
"faL73":'Definitionen monotoner und beschränkter Folgen kennen und anwenden können',
"faL74":'Grenzwerte von einfachen Folgen ermitteln können',
"faL81":'Endliche arithmetische und geometrische Reihen kennen und ihre Summen berechnen können',
"faL82":'Den Begriff der Summe einer unendlichen Reihe definieren können',
"faL83":'Summen konvergenter geometrischer Reihen berechnen können',
"faL84":'Folgen und Reihen zur Beschreibung diskreter Prozesse in anwendungsorientierten Bereichen einsetzen können',}
FA_BB=["FA 1.1","FA 1.2","FA 1.3","FA 1.4","FA 1.5","FA 1.6","FA 1.7","FA 1.8","FA 1.9",
"FA 2.1","FA 2.2","FA 2.3","FA 2.4","FA 2.5","FA 2.6",
"FA 3.1","FA 3.2","FA 3.3","FA 3.4",
"FA 4.1","FA 4.2","FA 4.3","FA 4.4",
"FA 5.1","FA 5.2","FA 5.3","FA 5.4","FA 5.5","FA 5.6",
"FA 6.1","FA 6.2","FA 6.3","FA 6.4","FA 6.5","FA 6.6",
"FA-L 7.1","FA-L 7.2","FA-L 7.3","FA-L 7.4","FA-L 8.1","FA-L 8.2","FA-L 8.3","FA-L 8.4"]
ws_kb=["ws11","ws12","ws13","ws14","ws21","ws22","ws23","ws24","wsL25","wsL26","ws31","ws32","ws33","ws34","wsL35","ws41","wsL42"]
ws_kb_beschreibung={
"ws11":'Werte aus tabellarischen und elementaren grafischen Darstellungen ablesen (bzw. zusammengesetzte Werte ermitteln)\n und im jeweiligen Kontext angemessen interpretieren können',
"ws12":'Tabellen und einfache statistische Grafiken erstellen, zwischen Darstellungsformen wechseln können',
"ws13":'Statistische Kennzahlen (absolute und relative Häufigkeiten; arithmetisches Mittel, Median, Modus; Quartile; Spannweite, empirische Varianz/\nStandardabweichung) im jeweiligen Kontext interpretieren können; die angeführten Kennzahlen für einfache Datensätze ermitteln können',
"ws14":'Definition und wichtige Eigenschaften des arithmetischen Mittels und des Medians angeben und nutzen,\n Quartile ermitteln und interpretieren können, die Entscheidung für die Verwendung einer bestimmten Kennzahl begründen können',
"ws21":'Grundraum und Ereignisse in angemessenen Situationen verbal bzw. formal angeben können',
"ws22":'Relative Häufigkeit als Schätzwert von Wahrscheinlichkeit verwenden und anwenden können',
"ws23":'Wahrscheinlichkeit unter der Verwendung der Laplace-Annahme (Laplace Wahrscheinlichkeit) berechnen und interpretieren können,\n Additionsregel und Multiplikationsregel anwenden und interpretieren können',
"ws24":'Binomialkoeffizient berechnen und interpretieren können',
"wsL25":'Bedingte Wahrscheinlichkeiten kennen, berechnen und interpretieren können',
"wsL26":'Entscheiden können, ob ein Ereignis von einem anderen Ereignis abhängt oder von diesem unabhängig ist',
"ws31":'Die Begriffe Zufallsvariable, (Wahrscheinlichkeits-)Verteilung, Erwartungswert und Standardabweichung verständig deuten und einsetzen können',
"ws32":'Binomialverteilung als Modell einer diskreten Verteilung kennen – Erwartungswert & Varianz/Standardabweichung binomialverteilter Zufallsgrößen ermitteln\n können, Wahrsch.vert. binomialverteilter Zufallsgrößen angeben können, Arbeiten mit der Binomialverteilung in anwendungsorientierten Bereichen',
"ws33":'Situationen erkennen und beschreiben können, in denen mit Binomialverteilung modelliert werden kann',
"ws34":'Normalapproximation der Binomialverteilung interpretieren und anwenden können',
"wsL35":'Mit der Normalverteilung, auch in anwendungsorientierten Bereichen, arbeiten können',
"ws41":'Konfidenzintervalle als Schätzung für eine Wahrscheinlichkeit oder einen unbekannten Anteil p interpretieren (frequentistische Deutung) und verwenden\n können, Berechnungen auf Basis der Binomialverteilung oder einer durch die Normalverteilung approximierten Binomialverteilung durchführen können',
"wsL42":'Einfache Anteilstests durchführen können und ihr Ergebnis erläutern können'}
WS_BB=["WS 1.1","WS 1.2","WS 1.3","WS 1.4","WS 2.1","WS 2.2","WS 2.3","WS 2.4","WS-L 2.5","WS-L 2.6",
"WS 3.1","WS 3.2","WS 3.3","WS 3.4","WS-L 3.5","WS 4.1","WS-L 4.2"]
AF_BB=["MC","ZO","LT","OA"]
aufgaben_formate={"mc":'Multiple Choice',"zo":'Zuordnen',"lt":'Lückentext',"oa":'Offenes Antwortformat'}
Klassen=["K5","K6","K7","K8"]
themen_klasse_5={'FU':'Funktionen', 'GL':'Gleichungen und\nGleichungssysteme',
'MZR':'Mengen, Zahlen,\nRechengesetze','TR':'Trigonometrie',
'VAG2':'Vektoren und analytische\nGeometrie'}
themen_klasse_6={'BSW':'Beschreibende Statistik\nund Wahrscheinlichkeit','FO':'Folgen',
'PWLU':'Potenzen, Wurzeln, Logarithmen\nund Ungleichungen','RE':'Reihen',
'RF':'Reelle Funktionen','VAG3':'Vektoren und analytische\nGeometrie in R3 und Rn'}
themen_klasse_7={'DR':'Differentialrechnung','DWV':'Diskrete Wahrscheinlichkeits-\nverteilungen',
'KKK':'Kreise, Kugeln, Kegelschnittslinien\nund andere Kurven','KZ':'Komplexe Zahlen','WM':'Wirtschaftsmathematik','GHG':'Gleichungen höheren Grades als 2'}
themen_klasse_8={'DDG':'Differenzen- und Differential-\ngleichungen; Grundlagen\nder Systemdynamik','IR':'Integralrechnung',
'SWS':'Stetgie Wahrscheinlichkeits-\nverteilungen; Beurteilende\nStatistik','WM':'Wirtschaftsmathematik'}



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
	subprocess.Popen('cd Teildokument ; latex --synctex=-1 Teildokument.tex ; dvips Teildokument.dvi ; ps2pdf -dNOSAFER Teildokument.ps',shell=True).wait()
	print('done 1')
	if sys.platform.startswith('linux'):
		subprocess.run(['xdg-open', 'Teildokument/Teildokument.pdf'])
	elif sys.platform.startswith('darwin'):
		subprocess.run(['xdg-open', 'Teildokument/Teildokument.pdf'])
	else:
	    subprocess.Popen('cd Teildokument ; Teildokument.pdf', shell=True).poll()
	os.unlink('Teildokument/Teildokument.aux')
	os.unlink('Teildokument/Teildokument.log')
	os.unlink('Teildokument/Teildokument.dvi')
	os.unlink('Teildokument/Teildokument.ps')


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
	with open(log_file, 'w+') as f:
		json.dump(beispieldaten_dateipfad, f,ensure_ascii=False)
	# print(log_file)		
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


