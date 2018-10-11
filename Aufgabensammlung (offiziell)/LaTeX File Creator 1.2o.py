import sys
import os 
import os.path
import subprocess
import tkinter
import glob
from tkinter import filedialog
from tkinter import *
import tkinter.scrolledtext as ScrolledText
import shutil


hauptfenster = Tk()
hauptfenster.title('LaTeX File Creator')
# hauptfenster.wm_iconbitmap('latex.ico')

hauptfenster.geometry('800x750+50+30')

# warning =Tk()
# warning.geometry('+100+100')

frame_gk= Frame(hauptfenster)
frame_gk.grid(row=0, column=0)
frame_gk_AG= Frame(hauptfenster)
frame_gk_AG.grid(row=0, column=0)
frame_gk_AN= Frame(hauptfenster)
frame_gk_AN.grid(row=0, column=0)
frame_gk_FA= Frame(hauptfenster)
frame_gk_FA.grid(row=0, column=0)
frame_gk_WS= Frame(hauptfenster)
frame_gk_WS.grid(row=0, column=0)

frame_gk_auswahl= Frame(hauptfenster)
frame_gk_auswahl.grid(row=0, column=2, sticky=S+W)

frame_eingabe = Frame(hauptfenster, bd=2)
frame_eingabe.grid(row=0, column=2, sticky=N+W)



dict_aufgabenformat={'Multiple Choice':'MC', 'Zuordnungsformat':'ZO', 'Lückentext':'LT', 'Offenes Antwortformat':'OA'}	
dict_themen={'AG':'AG - Algebra und Geometrie', 'AN':'AN - Analysis', 'FA':'FA - Funktionale Abhaengigkeiten', 'WS':'WS - Wahrscheinlichkeit und Statistik'}
ag_kb=["ag11","ag12",
# "agL13","agL14","agL15",
"ag21","ag22","ag23","ag24","ag25",
# "agL26","agL27","agL28",
"ag31","ag32","ag33","ag34","ag35",
# "agL36","agL37","agL38","agL39",
"ag41","ag42",
# "agL43","agL44","agL51","agL52","agL53"
]
AG_BB={"AG 1.1":'Wissen über die Zahlenmengen N, Z, Q, R, C verständig einsetzen können',
"AG 1.2":'Wissen über algebraische Begriffe angemessen einsetzen können: \n Variable, Terme, Formeln, (Un-)Gleichungen, Gleichungssysteme;\n Äquivalenz, Umformungen, Lösbarkeit',
# "AG-L 1.3":'Mit Aussagen und Mengen umgehen können',
# "AG-L 1.4":'Zahlen in einem nichtdekadischen Zahlensystem darstellen können',
# "AG-L 1.5":'Komplexe Zahlen in der Gauß’schen Zahlenebene darstellen und\n mit komplexen Zahlen rechnen können.',
"AG 2.1":'Einfache Terme und Formeln aufstellen, umformen und im Kontext deuten können',
"AG 2.2":'Lineare Gleichungen aufstellen, interpretieren, umformen/lösen und\n die Lösung im Kontext deuten können',
"AG 2.3":'Quadratische Gleichungen in einer Variablen umformen/lösen, über Lösungsfälle Bescheid wissen,\n Lösungen und Lösungsfälle (auch geometrisch) deuten können',
"AG 2.4":'Lineare Ungleichungen aufstellen, interpretieren, umformen/lösen,\n Lösungen (auch geometrisch) deuten können',
"AG 2.5":'Lineare Gleichungssysteme in zwei Variablen aufstellen, interpretieren, umformen/lösen,\n über Lösungsfälle Bescheid wissen,\n Lösungen und Lösungsfälle (auch geometrisch) deuten können',
# "AG-L 2.6":'Den Satz von Vieta kennen und anwenden können',
# "AG-L 2.7":'Lineare Gleichungssysteme in drei Variablen lösen können',
# "AG-L 2.8":'Den Fundamentalsatz der Algebra kennen und seine Bedeutung\n bei der Zahlenbereichserweiterung von R auf C erläutern können',
"AG 3.1":'Vektoren als Zahlentupel verständig einsetzen und im Kontext deuten können',
"AG 3.2":'Vektoren geometrisch (als Punkte bzw. Pfeile) deuten und verständig einsetzen können',
"AG 3.3":'Definition der Rechenoperationen mit Vektoren\n (Addition, Multiplikation mit einem Skalar, Skalarmultiplikation) kennen,\n Rechenoperationen verständig einsetzen und (auch geometrisch) deuten können',
"AG 3.4":'Geraden durch (Parameter-)Gleichungen in R2 und R3 angeben können;\n Geradengleichungen interpretieren können;\n Lagebeziehungen (zwischen Geraden und zwischen Punkt und Gerade) analysieren,\n Schnittpunkte ermitteln können',
"AG 3.5":'Normalvektoren in R2 aufstellen, verständig einsetzen und interpretieren können',
# "AG-L 3.6":'Die geometrische Bedeutung des Skalarprodukts kennen und\n den Winkel zwischen zwei Vektoren ermitteln können',
# "AG-L 3.7":'Einheitsvektoren ermitteln, verständig einsetzen und interpretieren können',
# "AG-L 3.8":'Definition des vektoriellen Produkts und seine geometrische Bedeutung kennen',
# "AG-L 3.9":'Wissen, wodurch Ebenen festgelegt sind;\n Ebenen in Parameter- und Normalvektordarstellung aufstellen können',
"AG 4.1":'Definitionen von Sinus, Cosinus, Tangens im rechtwinkligen Dreieck kennen und\n zur Auflösung rechtwinkliger Dreiecke einsetzen können',
"AG 4.2":'Definitionen von Sinus, Cosinus für Winkel größer als 90° kennen und einsetzen können',
# "AG-L 4.3":'Einfache Berechnungen an allgemeinen Dreiecken, an Figuren und Körpern\n (auch mittels Sinus- und Cosinussatz) durchführen können',
# "AG-L 4.4":'Polarkoordinaten kennen und einsetzen können',
# "AG-L 5.1":'Kegelschnitte in der Ebene durch Gleichungen beschreiben können;\n aus einer Kreisgleichung Mittelpunkt und Radius bestimmen können',
# "AG-L 5.2":'Die gegenseitige Lage von Kegelschnitt und Gerade ermitteln können',
# "AG-L 5.3":'Kugeln durch Gleichungen beschreiben können'
}
an_kb=["an11","an12","an13","an14",
# "anL15",
"an21",
# "anL22",
"an31","an32","an33",
# "anL34",
"an41","an42","an43"]
AN_BB={"AN 1.1":'Absolute und relative (prozentuelle) Änderungsmaße unterscheiden und\n angemessen verwenden können',
"AN 1.2":'Den Zusammenhang Differenzenquotient (mittlere Änderungsrate) –\n Differentialquotient („momentane“ Änderungsrate) auf der Grundlage \n eines intuitiven Grenzwertbegriffes kennen und\n damit (verbal und auch in formaler Schreibweise) auch kontextbezogen anwenden können',
"AN 1.3":'Den Differenzen- und Differentialquotienten in verschiedenen Kontexten deuten und \n entsprechende Sachverhalte durch den Differenzen- bzw.\n Differentialquotienten beschreiben können',
"AN 1.4":'Das systemdynamische Verhalten von Größen durch Differenzengleichungen beschreiben bzw.\n diese im Kontext deuten können',
# "AN-L 1.5":"Einfache Differentialgleichungen, insbesondere f'(x)= k*f(x), lösen können",
"AN 2.1":'Einfache Regeln des Differenzierens kennen und anwenden können:\n Potenzregel, Summenregel, Regeln für k*f(x)′ und f(k*x)′',
# "AN-L 2.2":'Kettenregel kennen und anwenden können',
"AN 3.1":'Den Begriff Ableitungsfunktion/Stammfunktion kennen und\n zur Beschreibung von Funktionen einsetzen können',
"AN 3.2":'Den Zusammenhang zwischen Funktion und Ableitungsfunktion\n (bzw. Funktion und Stammfunktion) in deren grafischer Darstellung\n erkennen und beschreiben können',
"AN 3.3":'Eigenschaften von Funktionen mithilfe der Ableitung(sfunktion) beschreiben können:\n Monotonie, lokale Extrema, Links- und Rechtskrümmung, Wendestellen',
# "AN-L 3.4":'Zielfunktionen in einer Variablen für Optimierungsaufgaben (Extremwertaufgaben) aufstellen und\n globale Extremstellen ermitteln können',
"AN 4.1":'Den Begriff des bestimmten Integrals als Grenzwert einer Summe von Produkten\n deuten und beschreiben können',
"AN 4.2":'Einfache Regeln des Integrierens kennen und anwenden können:\n Potenzregel, Summenregel, ∫k*f(x)dx, ∫f(k*x)dx;\n bestimmte Integrale von Polynomfunktionen ermitteln können',
"AN 4.3":'Das bestimmte Integral in verschiedenen Kontexten deuten und\n entsprechende Sachverhalte durch Integrale beschreiben können'}
fa_kb=["fa11","fa12","fa13","fa14","fa15","fa16","fa17","fa18","fa19",
"fa21","fa22","fa23","fa24","fa25","fa26",
"fa31","fa32","fa33","fa34",
"fa41","fa42","fa43","fa44",
"fa51","fa52","fa53","fa54","fa55","fa56",
"fa61","fa62","fa63","fa64","fa65","fa66",
# "faL71","faL72","faL73","faL74","faL81","faL82","faL83","faL84"
]

FA_BB={"FA 1.1":'Für gegebene Zusammenhänge entscheiden können,\n ob man sie als Funktionen betrachten kann ',
"FA 1.2":'Formeln als Darstellung von Funktionen interpretieren und den Funktionstyp zuordnen können',
"FA 1.3":'Zwischen tabellarischen und grafischen Darstellungen\n funktionaler Zusammenhänge wechseln können',
"FA 1.4":'Aus Tabellen, Graphen und Gleichungen von Funktionen Werte(paare) ermitteln und\n im Kontext deuten können',
"FA 1.5":'Eigenschaften von Funktionen erkennen, benennen, im Kontext deuten und\n zum Erstellen von Funktionsgraphen einsetzen können:\n Monotonie, Monotoniewechsel (lokale Extrema), Wendepunkte, Periodizität,\n Achsensymmetrie, asymptotisches Verhalten, Schnittpunkte mit den Achsen',
"FA 1.6":'Schnittpunkte zweier Funktionsgraphen grafisch und rechnerisch ermitteln und\n im Kontext interpretieren können',
"FA 1.7":'Funktionen als mathematische Modelle verstehen und damit verständig arbeiten können',
"FA 1.8":'Durch Gleichungen (Formeln) gegebene Funktionen\n mit mehreren Veränderlichen im Kontext deuten können,\n Funktionswerte ermitteln können',
"FA 1.9":'Einen Überblick über die wichtigsten (unten angeführten) Typen mathematischer Funktionen geben,\n ihre Eigenschaften vergleichen können',
"FA 2.1":'Verbal, tabellarisch, grafisch oder durch eine Gleichung (Formel)\n gegebene lineare Zusammenhänge als lineare Funktionen erkennen\n bzw. betrachten können; zwischen diesen Darstellungsformen wechseln können',
"FA 2.2":'Aus Tabellen, Graphen und Gleichungen linearer Funktionen Werte(paare)\n sowie die Parameter k und d ermitteln und\n im Kontext deuten können',
"FA 2.3":'Die Wirkung der Parameter k und d kennen und die Parameter\n in unterschiedlichen Kontexten deuten können',
"FA 2.4":'Charakteristische Eigenschaften von lineare Funktionen kennen und im Kontext deuten können',
"FA 2.5":'Die Angemessenheit einer Beschreibung mittels linearer Funktion bewerten können',
"FA 2.6":'Direkte Proportionalität als lineare Funktion vom Typ f(x) = k*x beschreiben können',
"FA 3.1":'Verbal, tabellarisch, grafisch oder durch eine Gleichung (Formel)\n gegebene Zusammenhänge dieser Art als entsprechende Potenzfunktionen erkennen\n bzw. betrachten können; zwischen diesen Darstellungsformen wechseln können',
"FA 3.2":'Aus Tabellen, Graphen und Gleichungen von Potenzfunktionen Werte(paare)\n sowie die Parameter a und b ermitteln und im Kontext deuten können',
"FA 3.3":'Die Wirkung der Parameter a und b bei Potenzfunktionen kennen und\n die Parameter im Kontext deuten können',
"FA 3.4":'Indirekte Proportionalität als Potenzfunktion vom Typ f(x)=a/x beschreiben können',
"FA 4.1":'Typische Verläufe von Graphen in Abhängigkeit vom Grad der Polynomfunktion (er)kennen',
"FA 4.2":'Zwischen tabellarischen und grafischen Darstellungen\n von Zusammenhängen dieser Art wechseln können',
"FA 4.3":'Aus Tabellen, Graphen und Gleichungen von Polynomfunktionen Funktionswerte,\n aus Tabellen und Graphen sowie aus einer quadratischen Funktionsgleichung\n Argumentwerte ermitteln können',
"FA 4.4":'Den Zusammenhang zwischen dem Grad der Polynomfunktion und\n der Anzahl der Null-, Extrem- und Wendestellen wissen',
"FA 5.1":'Verbal, tabellarisch, grafisch oder durch eine Gleichung (Formel)\n gegebene exponentielle Zusammenhänge als Exponentialfunktion erkennen\n bzw. betrachten können; zwischen diesen Darstellungsformen wechseln können',
"FA 5.2":'Aus Tabellen, Graphen und Gleichungen von Exponentialfunktionen Werte(paare) ermitteln und\n im Kontext deuten können',
"FA 5.3":'Die Wirkung der Parameter a und b (bzw. e^λ) kennen und\n die Parameter in unterschiedlichen Kontexten deuten können',
"FA 5.4":'Charakteristische Eigenschaften von Exponentialfunktionen kennen und im Kontext deuten können',
"FA 5.5":'Die Begriffe „Halbwertszeit“ und „Verdoppelungszeit“ kennen,\n die entsprechenden Werte berechnen und\n im Kontext deuten können',
"FA 5.6":'Die Angemessenheit einer Beschreibung mittels Exponentialfunktion bewerten können',
"FA 6.1":'Grafisch oder durch eine Gleichung (Formel) gegebene Zusammenhänge\n der Art f(x) = a*sin(b*x) als Allgemeine Sinusfunktion erkennen\n bzw. betrachten können;\n zwischen diesen Darstellungsformen wechseln können',
"FA 6.2":'Aus Graphen und Gleichungen von Allgemeinen Sinusfunktionen Werte(paare) ermitteln und\n im Kontext deuten können',
"FA 6.3":'Die Wirkung der Parameter a und b bei Winkelfunktionen kennen und\n die Parameter im Kontext deuten können',
"FA 6.4":'Periodizität als charakteristische Eigenschaft kennen und im Kontext deuten können',
"FA 6.5":'Wissen, dass cos(x)=sin(x+π/2)',
"FA 6.6":'Wissen, dass gilt: sin(x)′=cos(x) und cos(x)′=-sin(x)',
# "FA-L 7.1":'Zahlenfolgen (insbesondere arithmetische und geometrische Folgen) durch explizite und\n rekursive Bildungsgesetze beschreiben und graphisch darstellen können',
# "FA-L 7.2":'Zahlenfolgen als Funktionen über N bzw. N* auffassen können,\n insbesondere arithmetische Folgen als lineare Funktionen und\n geometrische Folgen als Exponentialfunktionen',
# "FA-L 7.3":'Definitionen monotoner und beschränkter Folgen kennen und anwenden können',
# "FA-L 7.4":'Grenzwerte von einfachen Folgen ermitteln können',
# "FA-L 8.1":'Endliche arithmetische und geometrische Reihen kennen und ihre Summen berechnen können',
# "FA-L 8.2":'Den Begriff der Summe einer unendlichen Reihe definieren können',
# "FA-L 8.3":'Summen konvergenter geometrischer Reihen berechnen können',
# "FA-L 8.4":'Folgen und Reihen zur Beschreibung diskreter Prozesse\n in anwendungsorientierten Bereichen einsetzen können'
}
ws_kb=["ws11","ws12","ws13","ws14","ws21","ws22","ws23","ws24",
# "wsL25","wsL26",
"ws31","ws32","ws33","ws34",
# "wsL35",
"ws41","wsL42"]

WS_BB={"WS 1.1":'Werte aus tabellarischen und elementaren grafischen Darstellungen ablesen\n (bzw. zusammengesetzte Werte ermitteln)\n und im jeweiligen Kontext angemessen interpretieren können',
"WS 1.2":'Tabellen und einfache statistische Grafiken erstellen,\n zwischen Darstellungsformen wechseln können',
"WS 1.3":'Statistische Kennzahlen (absolute und relative Häufigkeiten;\n arithmetisches Mittel, Median, Modus; Quartile; Spannweite, empirische Varianz/\n Standardabweichung) im jeweiligen Kontext interpretieren können;\n die angeführten Kennzahlen für einfache Datensätze ermitteln können',
"WS 1.4":'Definition und wichtige Eigenschaften des arithmetischen Mittels und des Medians\n angeben und nutzen, Quartile ermitteln und interpretieren können,\n die Entscheidung für die Verwendung einer bestimmten Kennzahl begründen können',
"WS 2.1":'Grundraum und Ereignisse in angemessenen Situationen verbal bzw. formal angeben können',
"WS 2.2":'Relative Häufigkeit als Schätzwert von Wahrscheinlichkeit verwenden und anwenden können',
"WS 2.3":'Wahrscheinlichkeit unter der Verwendung der Laplace-Annahme (Laplace Wahrscheinlichkeit\n berechnen und interpretieren können,\n Additionsregel und Multiplikationsregel anwenden und interpretieren können',
"WS 2.4":'Binomialkoeffizient berechnen und interpretieren können',
# "WS-L 2.5":'Bedingte Wahrscheinlichkeiten kennen, berechnen und interpretieren können',
# "WS-L 2.6":'Entscheiden können, ob ein Ereignis von einem anderen Ereignis abhängt oder\n von diesem unabhängig ist',
"WS 3.1":'Die Begriffe Zufallsvariable, (Wahrscheinlichkeits-)Verteilung, Erwartungswert und\n Standardabweichung verständig deuten und einsetzen können',
"WS 3.2":'Binomialverteilung als Modell einer diskreten Verteilung kennen –\n Erwartungswert & Varianz/Standardabweichung binomialverteilter Zufallsgrößen ermitteln\n können, Wahrsch.vert. binomialverteilter Zufallsgrößen angeben können,\n Arbeiten mit der Binomialverteilung in anwendungsorientierten Bereichen',
"WS 3.3":'Situationen erkennen und beschreiben können,\n in denen mit Binomialverteilung modelliert werden kann',
"WS 3.4":'Normalapproximation der Binomialverteilung interpretieren und anwenden können',
# "WS-L 3.5":'Mit der Normalverteilung, auch in anwendungsorientierten Bereichen, arbeiten können',
"WS 4.1":'Konfidenzintervalle als Schätzung für eine Wahrscheinlichkeit oder\n einen unbekannten Anteil p interpretieren (frequentistische Deutung) und verwenden können,\n Berechnungen auf Basis der Binomialverteilung oder einer durch die\n Normalverteilung approximierten Binomialverteilung durchführen können',
# "WS-L 4.2":'Einfache Anteilstests durchführen können und ihr Ergebnis erläutern können'
}
Klassen=["K5","K6","K7","K8"]
AF_BB=["MC","ZO","LT","OA"]

themen_klasse_5={'FU':'Funktionen', 'GL':'Gleichungen und Gleichungssysteme',
'MZR':'Mengen, Zahlen, Rechengesetze','TR':'Trigonometrie',
'VAG2':'Vektoren und analytische Geometrie'}
themen_klasse_6={'BSW':'Beschreibende Statistik und Wahrscheinlichkeit','FO':'Folgen',
'PWLU':'Potenzen, Wurzeln, Logarithmen und Ungleichungen','RE':'Reihen',
'RF':'Reelle Funktionen','VAG3':'Vektoren und analytische Geometrie in R3 und Rn'}
themen_klasse_7={'DR':'Differentialrechnung','DWV':'Diskrete Wahrscheinlichkeitsverteilungen',
'KKK':'Kreise, Kugeln, Kegelschnittslinienund andere Kurven','KZ':'Komplexe Zahlen'}
themen_klasse_8={'DDG':'Differenzen- und Differentialgleichungen; Grundlagen der Systemdynamik','IR':'Integralrechnung',
'SWS':'Stetgie Wahrscheinlichkeitsverteilungen; Beurteilende Statistik'}


Klasse5_BB=['FU', 'GL','MZR','TR','VAG2']
Klasse6_BB=['BSW','FO','PWLU','RE','RF']
Klasse7_BB=['DR','DWV','KKK','KZ']
Klasse8_BB=['DDG','IR','SWS']










set_gk_auswahl=[]
def selected_gk_dropdown(value):
	def CurSelect(evt):
		if liste_gk.curselection() !=():
			while True:
				try:
					explanation = Label(frame_gk_auswahl,text=gk_set[liste_gk.get(liste_gk.curselection())],width=75,height=4,bg="powderblue")	
					explanation.grid(row=1,column=1,columnspan=5,sticky=W)
					# print (gk_set[liste_gk.get(liste_gk.curselection())])
					break
				except KeyError or TclError:
					break
	global liste_gk
	liste_gk = Listbox(frame_gk, height=44, width=13, font=("", 8))
	liste_gk.bind('<<ListboxSelect>>',CurSelect)
	liste_gk.grid(columnspan=2,row=1, sticky=W)
	if value=='5. Klasse':
		gk_set=themen_klasse_5
	elif value=='6. Klasse':
		gk_set=themen_klasse_6
	elif value=='7. Klasse':
		gk_set=themen_klasse_7
	elif value=='8. Klasse':
		gk_set=themen_klasse_8	
	else:	
		gk_set=eval(value+'_BB')
	for item in gk_set:
		liste_gk.insert('end', item)

	
	# print(value)

def add_gk():
	all_items = liste_gk.get(0, END) # tuple with text of all items in Listbox
	sel_idx = liste_gk.curselection() # tuple with indexes of selected items
	sel_list = [all_items[item] for item in sel_idx] # list with text of all selected items
	# print(all_items)
	# print(sel_idx)
	for all in sel_list:
		if all not in set_gk_auswahl:
			liste_gk_auswahl.insert('end', all)
			set_gk_auswahl.append(all)
		
def delete_gk():
	all_items = liste_gk_auswahl.get(0, END) # tuple with text of all items in Listbox
	sel_idx = liste_gk_auswahl.curselection() # tuple with indexes of selected items
	sel_list = [all_items[item] for item in sel_idx] # list with text of all selected items
	try:
		liste_gk_auswahl.delete(sel_idx)
		set_gk_auswahl.remove(sel_list[0])
		# print(set_gk_auswahl)
	except TclError:
		pass



def confirm_save():
######################################################################################
# Typ 1 - Speichern #######################
######################################################################################
	global image_path_set
	textBox_Entry=str(textBox.get("1.0","end-1c"))
	for all in image_path_set:
		# print(all)
		head, tail=os.path.split(all)
		x = '{'+tail+'}'
		if x in textBox_Entry:
			textBox_Entry=str(textBox_Entry).replace(tail,"../Bilder/"+tail)
	if selected_typ.get()=='Typ 1':
		if len(set_gk_auswahl) > 1:
			warning =Tk()
			warning.title('Warnung')
			warning.geometry('+150+150')
			def cmd_ok():
				warning.destroy()
			warning_gk_auswahl= Label(warning, text='Es wurden zu viele Grundkompetenzen zugewiesen', width=50, height=5).grid()
			quit_button = Button(warning, text='OK', command=cmd_ok, width=10).grid(sticky=N)		
		else:
			set_gk_auswahl_klasse=[]
			if var_cb_klasse_5.get():
				set_gk_auswahl_klasse.append('K5')
			elif var_cb_klasse_6.get():
				set_gk_auswahl_klasse.append('K6')
			elif var_cb_klasse_7.get():
				set_gk_auswahl_klasse.append('K7')
			elif var_cb_klasse_8.get():
				set_gk_auswahl_klasse.append('K8')
				
			# print(set_gk_auswahl_klasse)
			file_list_integer_temp=[]
			def save_file_typ1():
				global image_path_set
				# print(image_path_set)
				copy_image_path_typ_1=os.path.join(os.path.dirname('__file__'),'Typ 1 Aufgaben','Bilder')
				copy_image_path_typ_1_inoff=os.path.join(os.path.dirname(os.path.abspath('.')),'Aufgabensammlung (inoffiziell)','Typ 1 Aufgaben','Bilder')
				for all in image_path_set:
					image_path_temp=all
					head, tail=os.path.split(image_path_temp)
					copy_image_file_typ_1_temp=os.path.join(copy_image_path_typ_1,tail)
					copy_image_file_typ_1_inoff_temp=os.path.join(copy_image_path_typ_1_inoff,tail)
					# print(copy_image_file_typ_1_temp)
					# print(copy_image_file_typ_1_inoff_temp)
					shutil.copy(image_path_temp,copy_image_file_typ_1_temp)
					shutil.copy(image_path_temp, copy_image_file_typ_1_inoff_temp)
				# print(set_gk_auswahl)
				if set_gk_auswahl[0] in themen_klasse_5 or set_gk_auswahl[0] in themen_klasse_6 or set_gk_auswahl[0] in themen_klasse_7 or set_gk_auswahl[0] in themen_klasse_8:
					if set_gk_auswahl[0] in themen_klasse_5:
						path_folder='5. Klasse'
						themen_auswahl=set_gk_auswahl[0]+' - '+themen_klasse_5[set_gk_auswahl[0]]
					elif set_gk_auswahl[0] in themen_klasse_6:
						path_folder='6. Klasse'
						themen_auswahl=set_gk_auswahl[0]+' - '+themen_klasse_6[set_gk_auswahl[0]]
					elif set_gk_auswahl[0] in themen_klasse_7:
						path_folder='7. Klasse'
						themen_auswahl=set_gk_auswahl[0]+' - '+themen_klasse_7[set_gk_auswahl[0]]
					elif set_gk_auswahl[0] in themen_klasse_8:
						path_folder='8. Klasse'
						themen_auswahl=set_gk_auswahl[0]+' - '+themen_klasse_8[set_gk_auswahl[0]]
					gk_path_temp=os.path.join(os.path.dirname('__file__'),'Typ 1 Aufgaben',path_folder,themen_auswahl,'Einzelbeispiele')			
					for all in os.listdir(gk_path_temp):
						if all.endswith('.tex'):
							z=set_gk_auswahl[0]+' - '
							#print(z)
							x, y=all.split(z)
							file_integer, file_extension=y.split('.tex')
							file_list_integer_temp.append(int(file_integer))

				else:
					path_folder='_Grundkompetenzen'
					for all in dict_themen:
						if all in set_gk_auswahl[0]:
							themen_auswahl=dict_themen[all]
					# print(path_folder)		
					# print(themen_auswahl)
					gk_path_temp=os.path.join(os.path.dirname('__file__'),'Typ 1 Aufgaben','_Grundkompetenzen',themen_auswahl,set_gk_auswahl[0],'Einzelbeispiele')	
					# print(gk_path_temp)
					for all in os.listdir(gk_path_temp):
						if all.endswith('.tex'):
							x, y=all.split(' -')
							file_integer, file_extension=y.split('.tex')
							file_list_integer_temp.append(int(file_integer))				

				if file_list_integer_temp==[]:
					max_integer_file_list=0
				else:
					max_integer_file_list= max(file_list_integer_temp)



				# print(max_integer_file_list+1)	
				eingabe_beispiel=textBox_Entry
				# ,'Typ 1 Aufgaben','_Matura',
				
				if set_gk_auswahl[0] in themen_klasse_5 or set_gk_auswahl[0] in themen_klasse_6 or set_gk_auswahl[0] in themen_klasse_7 or set_gk_auswahl[0] in themen_klasse_8:
					if set_gk_auswahl[0] in themen_klasse_5:
						file_name_klasse='K5'
					elif set_gk_auswahl[0] in themen_klasse_6:
						file_name_klasse='K6'
					elif set_gk_auswahl[0] in themen_klasse_7:
						file_name_klasse='K7'
					elif set_gk_auswahl[0] in themen_klasse_8:
						file_name_klasse='K8'				
					file_name=os.path.join(gk_path_temp,file_name_klasse+' - '+set_gk_auswahl[0]+' - '+str(max_integer_file_list+1)+'.tex')
					file=open(file_name,"w")
					file.write('\section{'+file_name_klasse+' - '+set_gk_auswahl[0]+" - "+str(max_integer_file_list+1) +" - "+titel_eingabe.get()+" - "+aufgabenformat_chosen+" - "+quelle_eingabe.get()+"}\n\n"
					"\\begin{beispiel}["+file_name_klasse+' - '+set_gk_auswahl[0]+"]{"+punkte_eingabe.get()+"}\n"+eingabe_beispiel+
					"\n\\end{beispiel}")
					file.close()
				else:
					file_name=os.path.join(os.path.dirname('__file__'),'Typ 1 Aufgaben','_Grundkompetenzen',themen_auswahl,set_gk_auswahl[0],'Einzelbeispiele',set_gk_auswahl[0]+' - '+str(max_integer_file_list+1)+'.tex')
					file=open(file_name,"w")
					if set_gk_auswahl_klasse==[]:
						file.write("\section{"+set_gk_auswahl[0]+" - "+str(max_integer_file_list+1) +" - "+titel_eingabe.get()+" - "+aufgabenformat_chosen+" - "+quelle_eingabe.get()+"}\n\n"
						"\\begin{beispiel}["+set_gk_auswahl[0]+"]{"+punkte_eingabe.get()+"}\n"+eingabe_beispiel+
						"\n\\end{beispiel}")
					else:
						file.write("\section{"+set_gk_auswahl[0]+" - "+str(max_integer_file_list+1) +' - '+set_gk_auswahl_klasse[0]+' - '+titel_eingabe.get()+" - "+aufgabenformat_chosen+" - "+quelle_eingabe.get()+"}\n\n"
						"\\begin{beispiel}["+set_gk_auswahl[0]+' - '+set_gk_auswahl_klasse[0]+"]{"+punkte_eingabe.get()+"}\n"+eingabe_beispiel+
						"\n\\end{beispiel}")
					file.close()
				window_finish =Tk()
				window_finish.title('Bestätigung')
				window_finish.geometry('+150+150')
				def cmd_save_ok():
					global set_gk_auswahl
					global aufgabenformat_chosen
					del aufgabenformat_chosen
					window_finish.destroy()
					selected_gk.set('AG')
					selected_typ.set('Typ 1')
					selected_af.set('bitte auswählen')
					var_cb_klasse_5.set(0)
					var_cb_klasse_6.set(0)
					var_cb_klasse_7.set(0)
					var_cb_klasse_8.set(0)
					titel_eingabe.delete(0,'end')
					punkte_eingabe.delete(0,'end')
					punkte_eingabe.insert(END, 1)
					textBox.delete('1.0','end')
					set_gk_auswahl.clear()
					liste_gk_auswahl.delete(0,'end')
					quelle_eingabe.delete(0,'end')
				gespeichert = Label(window_finish, text= 'Das Typ1-Beispiel "'+titel_eingabe.get()+'" wurde gespeichert!', width=50, height=5).grid()	
				button_ok = Button (window_finish, text= 'OK', width=10, command=cmd_save_ok).grid()	
				window_confirm.destroy()
				# print('Das Typ1-Beispiel "'+titel_eingabe.get()+'" wurde gespeichert!')
			
			try:
				aufgabenformat_chosen
			except NameError:
				warning =Tk()
				warning.title('Warnung')
				warning.geometry('+150+150')
				def cmd_ok():
					warning.destroy()
				warning_gk_auswahl= Label(warning, text='Es wurde kein Aufgabenformat ausgewählt', width=50, height=5).grid()
				quit_button = Button(warning, text='OK', command=cmd_ok, width=10).grid(sticky=N)
			else:
				if not set_gk_auswahl:
					warning =Tk()
					warning.title('Warnung')
					warning.geometry('+150+150')
					def cmd_ok():
						warning.destroy()
					warning_gk_auswahl= Label(warning, text='Es wurde keine Grundkompetenz zugewiesen', width=50, height=5).grid()
					quit_button = Button(warning, text='OK', command=cmd_ok, width=10).grid(sticky=N)
				else: 
					window_confirm =Tk()
					window_confirm.title('Bestätigung')
					window_confirm.geometry('+150+150')
					label_confirm=Label(window_confirm, text='Sind Sie sicher, dass Sie das folgende Beispiel speichern wollen?', height=4, width=60).grid(columnspan=2)
					label_aufgabe_typ=Label(window_confirm, text='Aufgabentyp: '+selected_typ.get(), bg="powderblue").grid(sticky=W,columnspan=2)
					label_confirm_titel=Label(window_confirm, text='Titel: '+titel_eingabe.get(), bg="powderblue").grid(sticky=W,columnspan=2)
					label_confirm_af=Label(window_confirm, text='Aufgabenformat: '+aufgabenformat_chosen_lang, bg="powderblue").grid(sticky=W,columnspan=2)
					label_confirm_gk=Label(window_confirm, text='Grundkompetenz(en): '+set_gk_auswahl[0], bg="powderblue").grid(sticky=W,columnspan=2)
					label_confirm_quelle=Label(window_confirm, text='Quelle: '+quelle_eingabe.get(), bg="powderblue").grid(sticky=W,columnspan=2)
					def cancel():
						window_confirm.destroy()
					button_save_file = Button (window_confirm, text='Speichern', command=save_file_typ1).grid(row=6, column=0, sticky=E)	
					button_cancel = Button(window_confirm, text='Abbrechen', command=cancel).grid(row=6, column=1, sticky=W)
				
######################################################################################
# Typ 2 - Speichern #######################
######################################################################################
	if selected_typ.get()=='Typ 2':
		set_gk_auswahl_klasse=[]
		if var_cb_klasse_5.get():
			set_gk_auswahl_klasse.append('K5')
		elif var_cb_klasse_6.get():
			set_gk_auswahl_klasse.append('K6')
		elif var_cb_klasse_7.get():
			set_gk_auswahl_klasse.append('K7')
		elif var_cb_klasse_8.get():
			set_gk_auswahl_klasse.append('K8')
		# print(set_gk_auswahl)
		def save_file_typ2():
			global image_path_set
			copy_image_path_typ_2=os.path.join(os.path.dirname('__file__'),'Typ 2 Aufgaben','Bilder')
			copy_image_path_typ_2_inoff=os.path.join(os.path.dirname(os.path.abspath('.')),'Aufgabensammlung (inoffiziell)','Typ 2 Aufgaben','Bilder')
			for all in image_path_set:
				image_path_temp=all
				head, tail=os.path.split(image_path_temp)
				copy_image_file_typ_2_temp=os.path.join(copy_image_path_typ_2,tail)
				copy_image_file_typ_2_inoff_temp=os.path.join(copy_image_path_typ_2_inoff,tail)
				shutil.copy(image_path_temp,copy_image_file_typ_2_temp)
				shutil.copy(image_path_temp,copy_image_file_typ_2_inoff_temp)
			file_list_integer_temp=[]
			# print(path_folder)		
			gk_path_temp=os.path.join(os.path.dirname('__file__'),'Typ 2 Aufgaben','Einzelbeispiele')	
			# print(gk_path_temp)
			for all in os.listdir(gk_path_temp):
				if all.endswith('.tex'):
					file_integer, file_extension=all.split('.tex')
					file_list_integer_temp.append(int(file_integer))				
			if file_list_integer_temp==[]:
				max_integer_file_list=0
			else:
				max_integer_file_list= max(file_list_integer_temp)
			# print(max_integer_file_list+1)	
			
			eingabe_beispiel=textBox_Entry
			# ,'Typ 1 Aufgaben','_Matura',
			list_schulstufe=[]
			themen_klasse_auswahl=[]
			gk_auswahl=[]
			# check=0
			for all in set_gk_auswahl:
				if all in themen_klasse_5 or all in themen_klasse_6 or all in themen_klasse_7 or all in themen_klasse_8:
					# check=1
					if all in themen_klasse_5:
						list_schulstufe.append(5)
					elif all in themen_klasse_6:
						list_schulstufe.append(6)
					elif all in themen_klasse_7:
						list_schulstufe.append(7)
					elif all in themen_klasse_8:
						list_schulstufe.append(8)
					themen_klasse_auswahl.append(all)
					# set_gk_auswahl.remove(all)
				if all in AG_BB or all in AN_BB or all in FA_BB or all in WS_BB:
					gk_auswahl.append(all)
					# check=2
			# print(list_schulstufe)
			if list_schulstufe!=[]:
				file_name_klasse='K'+str(max(list_schulstufe))
				# print(file_name_klasse)
			gk_chosen_joined=', '.join(gk_auswahl)
			themen_klasse_joined=', '.join(themen_klasse_auswahl)
			# print(gk_auswahl)
			# print(themen_klasse_auswahl)
			file_name=os.path.join(os.path.dirname('__file__'),'Typ 2 Aufgaben','Einzelbeispiele',str(max_integer_file_list+1)+'.tex')
			file=open(file_name,"w")
			if themen_klasse_auswahl==[]:
				if set_gk_auswahl_klasse==[]:
					file.write("\section{"+str(max_integer_file_list+1)+' - '+gk_chosen_joined+' - '+titel_eingabe.get()+" - "+quelle_eingabe.get()+"}\n\n"
					"\\begin{langesbeispiel} \item["+punkte_eingabe.get()+"] %PUNKTE DES BEISPIELS\n"+eingabe_beispiel+
					"\n\\end{langesbeispiel}")
				else:
					file.write("\section{"+str(max_integer_file_list+1)+' - '+set_gk_auswahl_klasse[0]+' - '+gk_chosen_joined+' - '+titel_eingabe.get()+" - "+quelle_eingabe.get()+"}\n\n"
					"\\begin{langesbeispiel} \item["+punkte_eingabe.get()+"] %PUNKTE DES BEISPIELS\n"+eingabe_beispiel+
					"\n\\end{langesbeispiel}")
			elif gk_auswahl==[]:
				file.write("\section{"+str(max_integer_file_list+1)+' - '+file_name_klasse+' - '+themen_klasse_joined+' - '+titel_eingabe.get()+" - "+quelle_eingabe.get()+"}\n\n"
				"\\begin{langesbeispiel} \item["+punkte_eingabe.get()+"] %PUNKTE DES BEISPIELS\n"+eingabe_beispiel+
				"\n\\end{langesbeispiel}")			
			else:
				file_path_zusatz=file_name_klasse+' - '+ themen_klasse_joined
				file.write("\section{"+str(max_integer_file_list+1)+' - '+file_path_zusatz+' - '+gk_chosen_joined+' - '+titel_eingabe.get()+" - "+quelle_eingabe.get()+"}\n\n"
				"\\begin{langesbeispiel} \item["+punkte_eingabe.get()+"] %PUNKTE DES BEISPIELS\n"+eingabe_beispiel+
				"\n\\end{langesbeispiel}")
			file.close()
			window_finish =Tk()
			window_finish.title('Bestätigung')
			window_finish.geometry('+150+150')
			def cmd_save_ok():
				global set_gk_auswahl
				# global aufgabenformat_chosen
				# del aufgabenformat_chosen
				window_finish.destroy()
				selected_gk.set('AG')
				selected_typ.set('Typ 1')
				selected_af.set('bitte auswählen')
				var_cb_klasse_5.set(0)
				var_cb_klasse_6.set(0)
				var_cb_klasse_7.set(0)
				var_cb_klasse_8.set(0)
				titel_eingabe.delete(0,'end')
				punkte_eingabe.delete(0,'end')
				punkte_eingabe.insert(END, 1)
				textBox.delete('1.0','end')
				set_gk_auswahl.clear()
				liste_gk_auswahl.delete(0,'end')
				quelle_eingabe.delete(0,'end')
			gespeichert = Label(window_finish, text= 'Das Typ1-Beispiel "'+titel_eingabe.get()+'" wurde gespeichert!', width=50, height=5).grid()	
			button_ok = Button (window_finish, text= 'OK', width=10, command=cmd_save_ok).grid()
			window_confirm.destroy()
			# print('Das Typ2-Beispiel "'+titel_eingabe.get()+'" wurde gespeichert!')

		if not set_gk_auswahl:
			warning =Tk()
			warning.title('Warnung')
			warning.geometry('+150+150')
			def cmd_ok():
				warning.destroy()
			warning_gk_auswahl= Label(warning, text='Es wurde keine Grundkompetenz zugewiesen', width=50, height=5).grid()
			quit_button = Button(warning, text='OK', command=cmd_ok, width=10).grid(sticky=N)
		else: 
			window_confirm =Tk()
			window_confirm.title('Bestätigung')
			window_confirm.geometry('+150+150')
			label_confirm=Label(window_confirm, text='Sind Sie sicher, dass Sie das folgende Beispiel speichern wollen?', height=4).grid(columnspan=2)
			label_aufgabe_typ=Label(window_confirm, text='Aufgabentyp: '+selected_typ.get(), bg="powderblue").grid(sticky=W, columnspan=2)
			label_confirm_titel=Label(window_confirm, text='Titel: '+titel_eingabe.get(), bg="powderblue").grid(sticky=W, columnspan=2)
			set_gk_joined=', '.join(set_gk_auswahl)
			label_confirm_gk=Label(window_confirm, text='Themen/Grundkompetenz(en): '+set_gk_joined, bg="powderblue").grid(sticky=W, columnspan=2)
			label_confirm_quelle=Label(window_confirm, text='Quelle: '+quelle_eingabe.get(), bg="powderblue").grid(sticky=W, columnspan=2)
			def cancel():
				window_confirm.destroy()
			button_save_file = Button (window_confirm, text='Speichern', command=save_file_typ2).grid(row=6, column=0, sticky=E)	
			button_cancel = Button(window_confirm, text='Abbrechen', command=cancel).grid(row=6, column=1, sticky=W)
			
			
		# def cancel():
			# window_confirm.destroy()
				
		# window_confirm =Tk()
		# window_confirm.title('Bestätigung')
		# window_confirm.geometry('+150+150')
		# label_confirm=Label(window_confirm, text='Sind Sie sicher, dass Sie das folgende Beispiel speichern wollen?').grid()
		# label_confirm_titel=Label(window_confirm, text='Titel: '+titel_eingabe.get()).grid(sticky=W)
		# label_confirm_gk=Label(window_confirm, text='Grundkompetenz(en): '+', '.join(set_gk_auswahl)).grid(sticky=W)
		# label_confirm_quelle=Label(window_confirm, text='Quelle: '+quelle_eingabe.get()).grid(sticky=W)
		

		# button_cancel = Button(window_confirm, text='Abbrechen', command=cancel).grid()
		# button_save_file = Button (window_confirm, text='Speichern', command=save_file_typ2).grid()


		

	
	

def cmd_aufgabenformat(value):
	global aufgabenformat_chosen_lang
	aufgabenformat_chosen_lang=value
	global aufgabenformat_chosen
	aufgabenformat_chosen = dict_aufgabenformat[value]
	

		
	
	

#, 'Klasse5','Klasse6','Klasse7','Klasse8'
gk_liste=['AG', 'FA', 'AN', 'WS',
 # '5. Klasse','6. Klasse','7. Klasse','8. Klasse'
 ]
selected_gk=StringVar()
selected_gk.set('AG')
# liste_gk_label = Label(frame_gk, text='GK:').grid()
liste_gk_dropdown = OptionMenu(frame_gk,selected_gk, *gk_liste, command=selected_gk_dropdown)
liste_gk_dropdown.config(width=6)
liste_gk_dropdown.grid(row=0, column=0)



def CurSelect(evt):
	if liste_gk.curselection() !=():
		while True:
			try:
				explanation = Label(frame_gk_auswahl,text=AG_BB[liste_gk.get(liste_gk.curselection())],width=75,height=4,bg="powderblue")	
				explanation.grid(row=1,column=1,columnspan=5, sticky=W)
				#print (AG_BB[liste_gk.get(liste_gk.curselection())])
				break
			except KeyError:
				break
#AG_BB[liste_gk.get(liste_gk.curselection())]	
liste_gk = Listbox(frame_gk,height=44, width=13, font=("", 8)) #, selectmode='multiple', 
liste_gk.bind('<<ListboxSelect>>',CurSelect)
for item in AG_BB:
	liste_gk.insert('end', item)
liste_gk.grid(columnspan=2, row=1, sticky=W)



def menu_typ_auswahl(value):
	global aufgabenformat_eingabe
	if value=='Typ 1':
		selected_af.set('bitte auswählen')
		
		
		# selected_af=StringVar()
		# aufgabenformat_eingabe=OptionMenu(frame_eingabe, selected_af, *af_liste,command=cmd_aufgabenformat)
		# aufgabenformat_eingabe.config(width=1)
		# aufgabenformat_eingabe.grid(row=3, column=2, sticky='ew')
		# return selected_af
	
	if value=='Typ 2':
		selected_af.set('keine Auswahl nötig')
		# aufgabenformat_eingabe=OptionMenu(frame_eingabe, selected_af, 'keine Auswahl nötig')
		# aufgabenformat_eingabe.config(width=1)
		# aufgabenformat_eingabe.grid(row=3, column=2, sticky='ew')
		# aufgabenformat_eingabe.destroy()
		# aufgabenformat_inactive = Label(frame_eingabe, text='keine Auswahl nötig', width=3, height=1)
		# aufgabenformat_inactive.grid(row=3, column=2, sticky='ew')
		# selected_af_typ.set('keine Auswahl nötig')




button_hinzufuegen=Button(frame_gk, text='Hinzufügen >>', command=add_gk)
button_hinzufuegen.grid(columnspan=2)


	
liste_gk_auswahl_label=Label(frame_gk_auswahl, text='Ausgewählte GK').grid(sticky=W)
liste_gk_auswahl = Listbox(frame_gk_auswahl,height=4)
# liste_gk_auswahl.bind('<<ListboxSelect>>',CurSelect_auswahl)

scroll = Scrollbar(frame_gk_auswahl, orient=VERTICAL)
liste_gk_auswahl['yscrollcommand']=scroll.set
scroll['command']=liste_gk_auswahl.yview
liste_gk_auswahl.grid(row=1)
scroll.grid(row=1, sticky=E+N+S)

button_entfernen=Button(frame_gk_auswahl, text='<< Entfernen', command=delete_gk)
button_entfernen.grid(sticky=W)


selected_typ=StringVar()
# typ_liste=[]
selected_typ.set('Typ 1')
label_typ = Label(frame_eingabe, text='Aufgbenformat:').grid(row=0, sticky=E)
menu_typ = OptionMenu(frame_eingabe,selected_typ, 'Typ 1','Typ 2', command=menu_typ_auswahl)
menu_typ.grid(row=0, column=1,sticky=W)
titel_eingabe_label= Label(frame_eingabe, text='Titel')
titel_eingabe_label.grid(row=1,sticky=W)
titel_eingabe = Entry(frame_eingabe, width=109)
titel_eingabe.grid(sticky=W,columnspan=3, row=2)
punkte_eingabe_label=Label(frame_eingabe, text='Punkte:')
punkte_eingabe_label.grid(sticky=W,row=3, column=0)
punkte_eingabe = Entry(frame_eingabe, width=3)
punkte_eingabe.grid(row=3, column=0)
punkte_eingabe.insert(END, 1)
aufgabenformat_label=Label(frame_eingabe, text="Aufgabenformat:").grid(row=3, column=1, sticky=E)

check_af=0
af_liste=['Multiple Choice', 'Zuordnungsformat', 'Lückentext', 'Offenes Antwortformat']
selected_af=StringVar()
selected_af.set('bitte auswählen')
aufgabenformat_eingabe=OptionMenu(frame_eingabe, selected_af, *af_liste, command=cmd_aufgabenformat)
aufgabenformat_eingabe.config(width=1)
aufgabenformat_eingabe.grid(row=3, column=2, sticky='ew')
eingabe_label = Label(frame_eingabe, text='Eingabe des Beispiels:')
eingabe_label.grid(sticky=W,row=4, columnspan=2)
eingabe_label_info = Label(frame_eingabe, text='INFO: Eingabe des Aufgabentextes zwischen \\begin{beispiel} ... \end{beispiel}',relief=GROOVE)
eingabe_label_info.grid(sticky=E,row=4,column=1, columnspan=2)
textBox=ScrolledText.ScrolledText(frame_eingabe, height=27, width=80)
textBox.grid(columnspan=3)
quelle_eingabe_label= Label(frame_eingabe, text='Quelle').grid(sticky=W)
quelle_eingabe=Entry(frame_eingabe, width=107)
quelle_eingabe.grid(sticky=W, columnspan=3)



############## BILDER einfügen ############

# global window_height
window_height=750
image_path_set=[]
def select_image():
	global image_path_set
	global window_height
	global var_row
	try:
		picture.destroy()
		button_cancel.destroy()
	except UnboundLocalError:
		pass
	def picture_cancel():
		global window_height
		picture.destroy()
		button_cancel.destroy()
		window_height=window_height-25
		hauptfenster.geometry("%dx%d" % (800,window_height))
		image_path_set.remove(filename)
		# print(image_path_set)
		# picture_delete()
	if 'var_row' in globals():
		pass
	else:
		var_row=5
	var_row+=1
	try:
		last_path=image_path_set[-1]
		# print(image_path_set[-1])
	except IndexError:
		last_path="/"
	filename =  filedialog.askopenfilename(initialdir = last_path,title = "Durchsuchen...",filetypes = (('Grafik Dateien','*.eps;*.jpg;*.gif;*.png'),("Alle Dateien","*.*")))
	if filename!='':
		window_height+=25
		hauptfenster.geometry("%dx%d" % (800,window_height))
		image_path_set.append(filename)
		head,tail=os.path.split(filename)
		picture=Label(hauptfenster, text=tail)
		picture.grid(row=var_row, column=0, columnspan=3, sticky=W)
		button_cancel= Button(hauptfenster, text='x', command=picture_cancel, bg='indianred')
		button_cancel.grid(row=var_row, column=2)
	# print(image_path_set)
		


label_image= Label(hauptfenster, text='Bild hinzufügen').grid(column=0,row=1,sticky=N+W)
button_image= Button(hauptfenster, text="Durchsuchen...", command=select_image).grid(column=2,row=1, sticky=W)

#####################################################
###########################################################


button_speichern=Button(hauptfenster, height=1, width=10, text="Speichern", command=confirm_save)
#command=lambda: retrieve_input() >>> just means do this when i press the button
button_speichern.grid(row=1,column=2, sticky=E)

var_cb_klasse_5=IntVar()
explanation = Label(frame_gk_auswahl,text='',width=75,height=4).grid(row=1,column=1,columnspan=5, sticky=W)
cb_klasse_5 = Checkbutton(frame_gk_auswahl, text='5. Klasse', variable=var_cb_klasse_5)
cb_klasse_5.grid(row=0, column=1, sticky=W) 
var_cb_klasse_6=IntVar()
cb_klasse_6 = Checkbutton(frame_gk_auswahl, text='6. Klasse', variable=var_cb_klasse_6)
cb_klasse_6.grid(row=0, column=2, sticky=W) 
var_cb_klasse_7=IntVar()
cb_klasse_7 = Checkbutton(frame_gk_auswahl, text='7. Klasse', variable=var_cb_klasse_7)
cb_klasse_7.grid(row=0, column=3, sticky=W) 
var_cb_klasse_8=IntVar()
cb_klasse_8 = Checkbutton(frame_gk_auswahl, text='8. Klasse', variable=var_cb_klasse_8)
cb_klasse_8.grid(row=0, column=4, sticky=W) 

hauptfenster.mainloop()