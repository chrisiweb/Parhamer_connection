# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test_2.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

########
### QMessageBox (little info  window)
### QShortcut (key)

from PyQt4 import QtCore, QtGui
import time
import threading
import sys
import os 
import os.path
from pathlib import Path
import datetime
import json
import subprocess
import re

dict_gk={"ag11":'AG 1.1',"ag12":'AG 1.2',"ag13":'AG-L 1.3',"ag14":"AG-L 1.4",
"ag15":"AG-L 1.5","ag21":"AG 2.1","ag22":"AG 2.2","ag23":"AG 2.3","ag24":"AG 2.4",
"ag25":"AG 2.5","ag26":"AG-L 2.6","ag27":"AG-L 2.7","ag28":"AG-L 2.8",
"ag31":"AG 3.1","ag32":"AG 3.2","ag33":"AG 3.3","ag34":"AG 3.4","ag35":"AG 3.5",
"ag36":"AG-L 3.6","ag37":"AG-L 3.7","ag38":"AG-L 3.8","ag39":"AG-L 3.9",
"ag41":"AG 4.1","ag42":"AG 4.2","ag43":"AG-L 4.3","ag44":"AG-L 4.4",
"ag51":"AG-L 5.1","ag52":"AG-L 5.2","ag53":"AG-L 5.3",
"an11":"AN 1.1","an12":"AN 1.2","an13":"AN 1.3","an14":"AN 1.4","an15":"AN-L 1.5",
"an21":"AN 2.1","an22":"AN-L 2.2","an31":"AN 3.1","an32":"AN 3.2","an33":"AN 3.3",
"an34":"AN-L 3.4","an41":"AN 4.1","an42":"AN 4.2","an43":"AN 4.3",
"fa11":"FA 1.1","fa12":"FA 1.2","fa13":"FA 1.3","fa14":"FA 1.4","fa15":"FA 1.5",
"fa16":"FA 1.6","fa17":"FA 1.7","fa18":"FA 1.8","fa19":"FA 1.9",
"fa21":"FA 2.1","fa22":"FA 2.2","fa23":"FA 2.3","fa24":"FA 2.4","fa25":"FA 2.5",
"fa26":"FA 2.6", "fa31":"FA 3.1","fa32":"FA 3.2","fa33":"FA 3.3","fa34":"FA 3.4",
"fa41":"FA 4.1","fa42":"FA 4.2","fa43":"FA 4.3","fa44":"FA 4.4",
"fa51":"FA 5.1","fa52":"FA 5.2","fa53":"FA 5.3","fa54":"FA 5.4","fa55":"FA 5.5",
"fa56":"FA 5.6","fa61":"FA 6.1","fa62":"FA 6.2","fa63":"FA 6.3","fa64":"FA 6.4",
"fa65":"FA 6.5","fa66":"FA 6.6",
"fa71":"FA-L 7.1","fa72":"FA-L 7.2","fa73":"FA-L 7.3","fa74":"FA-L 7.4",
"fa81":"FA-L 8.1","fa82":"FA-L 8.2","fa83":"FA-L 8.3","fa84":"FA-L 8.4",
"ws11":"WS 1.1","ws12":"WS 1.2","ws13":"WS 1.3","ws14":"WS 1.4","ws21":"WS 2.1",
"ws22":"WS 2.2","ws23":"WS 2.3","ws24":"WS 2.4","ws25":"WS-L 2.5","ws26":"WS-L 2.6",
"ws31":"WS 3.1","ws32":"WS 3.2","ws33":"WS 3.3","ws34":"WS 3.4","ws35":"WS-L 3.5",
"ws41":"WS 4.1","ws42":"WS-L 4.2"}


ag_kb_beschreibung={
"ag11":'Wissen über die Zahlenmengen N, Z, Q, R, C verständig einsetzen können',
"ag12":'Wissen über algebraische Begriffe angemessen einsetzen können: \n Variable, Terme, Formeln, (Un-)Gleichungen, Gleichungssysteme;\nÄquivalenz, Umformungen, Lösbarkeit',
"ag13":'Mit Aussagen und Mengen umgehen können',
"ag14":'Zahlen in einem nichtdekadischen Zahlensystem darstellen können',
"ag15":'Komplexe Zahlen in der Gauß’schen Zahlenebene\ndarstellen und mit komplexen Zahlen rechnen können.',
"ag21":'Einfache Terme und Formeln aufstellen, umformen und\nim Kontext deuten können',
"ag22":'Lineare Gleichungen aufstellen, interpretieren, umformen/lösen und\ndie Lösung im Kontext deuten können',
"ag23":'Quadratische Gleichungen in einer Variablen umformen/lösen,\nüber Lösungsfälle Bescheid wissen, Lösungen und Lösungsfälle\n(auch geometrisch) deuten können',
"ag24":'Lineare Ungleichungen aufstellen, interpretieren, umformen/lösen,\nLösungen (auch geometrisch) deuten können',
"ag25":'Lineare Gleichungssysteme in zwei Variablen aufstellen,\ninterpretieren, umformen/lösen, über Lösungsfälle Bescheid wissen,\nLösungen und Lösungsfälle (auch geometrisch) deuten können',
"ag26":'Den Satz von Vieta kennen und anwenden können',
"ag27":'Lineare Gleichungssysteme in drei Variablen lösen können',
"ag28":'Den Fundamentalsatz der Algebra kennen und seine Bedeutung bei der Zahlenbereichserweiterung von R auf C erläutern können',
"ag31":'Vektoren als Zahlentupel verständig einsetzen und im Kontext deuten können',
"ag32":'Vektoren geometrisch (als Punkte bzw. Pfeile) deuten und verständig einsetzen können',
"ag33":'Definition der Rechenoperationen mit Vektoren (Addition, Multiplikation mit einem Skalar, Skalarmultiplikation) kennen,\n Rechenoperationen verständig einsetzen und (auch geometrisch) deuten können',
"ag34":'Geraden durch (Parameter-)Gleichungen in R2 und R3 angeben können; Geradengleichungen interpretieren können;\n Lagebeziehungen (zwischen Geraden und zwischen Punkt und Gerade) analysieren, Schnittpunkte ermitteln können',
"ag35":'Normalvektoren in R2 aufstellen, verständig einsetzen und interpretieren können',
"ag36":'Die geometrische Bedeutung des Skalarprodukts kennen und den Winkel zwischen zwei Vektoren ermitteln können',
"ag37":'Einheitsvektoren ermitteln, verständig einsetzen und interpretieren können',
"ag38":'Definition des vektoriellen Produkts und seine geometrische Bedeutung kennen',
"ag39":'Wissen, wodurch Ebenen festgelegt sind; Ebenen in Parameter- und Normalvektordarstellung aufstellen können',
"ag41":'Definitionen von Sinus, Cosinus, Tangens im rechtwinkligen Dreieck kennen und zur Auflösung rechtwinkliger Dreiecke einsetzen können',
"ag42":'Definitionen von Sinus, Cosinus für Winkel größer als 90° kennen und einsetzen können',
"ag43":'Einfache Berechnungen an allgemeinen Dreiecken, an Figuren und Körpern (auch mittels Sinus- und Cosinussatz) durchführen können',
"ag44":'Polarkoordinaten kennen und einsetzen können',
"ag51":'Kegelschnitte in der Ebene durch Gleichungen beschreiben können; aus einer Kreisgleichung Mittelpunkt und Radius bestimmen können',
"ag52":'Die gegenseitige Lage von Kegelschnitt und Gerade ermitteln können',
"ag53":'Kugeln durch Gleichungen beschreiben können',}
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
"an15":"Einfache Differentialgleichungen, insbesondere f'(x)= k*f(x), lösen können",
"an21":'Einfache Regeln des Differenzierens kennen und anwenden können: Potenzregel, Summenregel, Regeln für k*f(x)′ und f(k*x)′',
"an22":'Kettenregel kennen und anwenden können',
"an31":'Den Begriff Ableitungsfunktion/Stammfunktion kennen und zur Beschreibung von Funktionen einsetzen können',
"an32":'Den Zusammenhang zwischen Funktion und Ableitungsfunktion (bzw. Funktion und Stammfunktion)\n in deren grafischer Darstellung erkennen und beschreiben können',
"an33":'Eigenschaften von Funktionen mithilfe der Ableitung(sfunktion) beschreiben können:\n Monotonie, lokale Extrema, Links- und Rechtskrümmung, Wendestellen',
"an34":'Zielfunktionen in einer Variablen für Optimierungsaufgaben (Extremwertaufgaben) aufstellen und globale Extremstellen ermitteln können',
"an41":'Den Begriff des bestimmten Integrals als Grenzwert einer Summe von Produkten deuten und beschreiben können',
"an42":'Einfache Regeln des Integrierens kennen und anwenden können: Potenzregel, Summenregel, ∫k*f(x)dx, ∫f(k*x)dx;\n bestimmte Integrale von Polynomfunktionen ermitteln können',
"an43":'Das bestimmte Integral in verschiedenen Kontexten deuten und entsprechende Sachverhalte durch Integrale beschreiben können'}
AN_BB=["AN 1.1","AN 1.2","AN 1.3","AN 1.4","AN-L 1.5","AN 2.1","AN-L 2.2",
"AN 3.1","AN 3.2","AN 3.3","AN-L 3.4",
"AN 4.1","AN 4.2","AN 4.3"]
# fa_kb=["fa11","fa12","fa13","fa14","fa15","fa16","fa17","fa18","fa19",
# "fa21","fa22","fa23","fa24","fa25","fa26",
# "fa31","fa32","fa33","fa34",
# "fa41","fa42","fa43","fa44",
# "fa51","fa52","fa53","fa54","fa55","fa56",
# "fa61","fa62","fa63","fa64","fa65","fa66",
# "fa71","fa72","fa73","fa74",
# "fa81","fa82","fa83","fa84"]
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
"fa71":'Zahlenfolgen (insbesondere arithmetische und geometrische Folgen) durch explizite und\nrekursive Bildungsgesetze beschreiben und graphisch darstellen können',
"fa72":'Zahlenfolgen als Funktionen über N bzw. N* auffassen können, insbesondere arithmetische Folgen als lineare Funktionen und\n geometrische Folgen als Exponentialfunktionen',
"fa73":'Definitionen monotoner und beschränkter Folgen kennen und anwenden können',
"fa74":'Grenzwerte von einfachen Folgen ermitteln können',
"fa81":'Endliche arithmetische und geometrische Reihen kennen und ihre Summen berechnen können',
"fa82":'Den Begriff der Summe einer unendlichen Reihe definieren können',
"fa83":'Summen konvergenter geometrischer Reihen berechnen können',
"fa84":'Folgen und Reihen zur Beschreibung diskreter Prozesse in anwendungsorientierten Bereichen einsetzen können',}
FA_BB=["FA 1.1","FA 1.2","FA 1.3","FA 1.4","FA 1.5","FA 1.6","FA 1.7","FA 1.8","FA 1.9",
"FA 2.1","FA 2.2","FA 2.3","FA 2.4","FA 2.5","FA 2.6",
"FA 3.1","FA 3.2","FA 3.3","FA 3.4",
"FA 4.1","FA 4.2","FA 4.3","FA 4.4",
"FA 5.1","FA 5.2","FA 5.3","FA 5.4","FA 5.5","FA 5.6",
"FA 6.1","FA 6.2","FA 6.3","FA 6.4","FA 6.5","FA 6.6",
"FA-L 7.1","FA-L 7.2","FA-L 7.3","FA-L 7.4","FA-L 8.1","FA-L 8.2","FA-L 8.3","FA-L 8.4"]
# ws_kb=["ws11","ws12","ws13","ws14","ws21","ws22","ws23","ws24","wsL25","wsL26","ws31","ws32","ws33","ws34","wsL35","ws41","wsL42"]
ws_kb_beschreibung={
"ws11":'Werte aus tabellarischen und elementaren grafischen Darstellungen ablesen\n(bzw. zusammengesetzte Werte ermitteln) und im jeweiligen Kontext\nangemessen interpretieren können',
"ws12":'Tabellen und einfache statistische Grafiken erstellen, zwischen Darstellungsformen wechseln können',
"ws13":'Statistische Kennzahlen (absolute und relative Häufigkeiten; arithmetisches Mittel, Median, Modus; Quartile; Spannweite, empirische Varianz/\nStandardabweichung) im jeweiligen Kontext interpretieren können; die angeführten Kennzahlen für einfache Datensätze ermitteln können',
"ws14":'Definition und wichtige Eigenschaften des arithmetischen Mittels und des Medians angeben und nutzen,\n Quartile ermitteln und interpretieren können, die Entscheidung für die Verwendung einer bestimmten Kennzahl begründen können',
"ws21":'Grundraum und Ereignisse in angemessenen Situationen verbal bzw. formal angeben können',
"ws22":'Relative Häufigkeit als Schätzwert von Wahrscheinlichkeit verwenden und anwenden können',
"ws23":'Wahrscheinlichkeit unter der Verwendung der Laplace-Annahme (Laplace Wahrscheinlichkeit) berechnen und interpretieren können,\n Additionsregel und Multiplikationsregel anwenden und interpretieren können',
"ws24":'Binomialkoeffizient berechnen und interpretieren können',
"ws25":'Bedingte Wahrscheinlichkeiten kennen, berechnen und interpretieren können',
"ws26":'Entscheiden können, ob ein Ereignis von einem anderen\nEreignis abhängt oder von diesem unabhängig ist',
"ws31":'Die Begriffe Zufallsvariable, (Wahrscheinlichkeits-)Verteilung,\nErwartungswert und Standardabweichung verständig deuten und einsetzen können',
"ws32":'Binomialverteilung als Modell einer diskreten Verteilung kennen –\nErwartungswert & Varianz/Standardabweichung binomialverteilter Zufallsgrößen\nermitteln können, Wahrsch.vert. binomialverteilter Zufallsgrößen angeben können,\nArbeiten mit der Binomialverteilung in anwendungsorientierten Bereichen',
"ws33":'Situationen erkennen und beschreiben können,\nin denen mit Binomialverteilung modelliert werden kann',
"ws34":'Normalapproximation der Binomialverteilung interpretieren und anwenden können',
"ws35":'Mit der Normalverteilung, auch in anwendungsorientierten Bereichen, arbeiten können',
"ws41":'Konfidenzintervalle als Schätzung für eine Wahrscheinlichkeit oder\neinen unbekannten Anteil p interpretieren (frequentistische Deutung) und verwenden\nkönnen, Berechnungen auf Basis der Binomialverteilung oder einer durch die\nNormalverteilung approximierten Binomialverteilung durchführen können',
"ws42":'Einfache Anteilstests durchführen können und ihr Ergebnis erläutern können'}
WS_BB=["WS 1.1","WS 1.2","WS 1.3","WS 1.4","WS 2.1","WS 2.2","WS 2.3","WS 2.4","WS-L 2.5","WS-L 2.6",
"WS 3.1","WS 3.2","WS 3.3","WS 3.4","WS-L 3.5","WS 4.1","WS-L 4.2"]
set_af=["mc","zo","lt","oa"]
aufgaben_formate={"mc":'Multiple Choice',"zo":'Zuordnen',"lt":'Lückentext',"oa":'Offenes Antwortformat'}
Klassen=["k5","k6","k7","k8"]
themen_klasse_5={'fu':'Funktionen', 'gl':'Gleichungen und\nGleichungssysteme',
'mzr':'Mengen, Zahlen,\nRechengesetze','tr':'Trigonometrie',
'vag2':'Vektoren und analytische\nGeometrie'}
themen_klasse_6={'bsw':'Beschreibende Statistik\nund Wahrscheinlichkeit','fo':'Folgen',
'pwlu':'Potenzen, Wurzeln, Logarithmen\nund Ungleichungen','re':'Reihen',
'rf':'Reelle Funktionen','vag3':'Vektoren und analytische\nGeometrie in R3 und Rn'}
themen_klasse_7={'dr':'Differentialrechnung','dwv':'Diskrete Wahrscheinlichkeits-\nverteilungen',
'kkk':'Kreise, Kugeln, Kegelschnittslinien\nund andere Kurven','kz':'Komplexe Zahlen','wm':'Wirtschaftsmathematik','ghg':'Gleichungen höheren Grades als 2'}
themen_klasse_8={'ddg':'Differenzen- und Differential-\ngleichungen; Grundlagen\nder Systemdynamik','ir':'Integralrechnung',
'sws':'Stetgie Wahrscheinlichkeits-\nverteilungen; Beurteilende\nStatistik','wm':'Wirtschaftsmathematik'}

try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig)

# class LoadingWindow(QtGui.QDialog):
# 	def __init__(self):
# 		super().__init__()
# 		layout=QtGui.QVBoxLayout()
# 		layout.addWidget(QtGui.QLabel('test'))
# 		self.setLayout(layout)

class Ui_Dialog(object):
	def setupUi(self, Dialog):
		Dialog.setObjectName(_fromUtf8("Dialog"))
		Dialog.resize(557, 231)
		self.gridLayout = QtGui.QGridLayout(Dialog)
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
		spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.gridLayout.addItem(spacerItem, 6, 0, 1, 1)
		self.progressBar = QtGui.QProgressBar(Dialog)

		self.progressBar.setProperty("value", 0)
		self.progressBar.setTextVisible(False)
		self.progressBar.setObjectName(_fromUtf8("progressBar"))
		self.gridLayout.addWidget(self.progressBar, 5, 0, 1, 1)
		self.label = QtGui.QLabel(Dialog)
		self.label.setStyleSheet(_fromUtf8("font: 11pt \"MS Shell Dlg 2\";"))
		self.label.setObjectName(_fromUtf8("label"))
		self.gridLayout.addWidget(self.label, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
		spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.gridLayout.addItem(spacerItem1, 4, 0, 1, 1)
		spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.gridLayout.addItem(spacerItem2, 0, 0, 1, 1)
		spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.gridLayout.addItem(spacerItem3, 2, 0, 1, 1)
		self.label_2 = QtGui.QLabel(Dialog)
		self.label_2.setStyleSheet(_fromUtf8("font: 11pt \"MS Shell Dlg 2\";"))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1, QtCore.Qt.AlignHCenter)

		self.retranslateUi(Dialog)
		QtCore.QMetaObject.connectSlotsByName(Dialog)


	def retranslateUi(self, Dialog):
		Dialog.setWindowTitle(_translate("Dialog", "Erstelle PDF... ", None))
		self.progressBar.setFormat(_translate("Dialog", "%p%", None))
		self.label.setText(_translate("Dialog", "Insegsamt wurden 59 Beispiele gefunden.", None))
		self.label_2.setText(_translate("Dialog", "Lade PDF Datei...", None))
		


class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName(_fromUtf8("MainWindow"))
		MainWindow.resize(1078, 735)
		MainWindow.setMaximumSize(QtCore.QSize(1078, 16777215))
		MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
		MainWindow.setStyleSheet(_fromUtf8(""))
		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
		self.gridLayout = QtGui.QGridLayout(self.centralwidget)
		self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
		self.groupBox = QtGui.QGroupBox(self.centralwidget)
		self.groupBox.setMaximumSize(QtCore.QSize(367, 16777215))
		self.groupBox.setObjectName(_fromUtf8("groupBox"))
		self.gridLayout_13 = QtGui.QGridLayout(self.groupBox)
		self.gridLayout_13.setObjectName(_fromUtf8("gridLayout_13"))
		self.cb_af_zo = QtGui.QCheckBox(self.groupBox)
		self.cb_af_zo.setObjectName(_fromUtf8("cb_af_zo"))
		self.gridLayout_13.addWidget(self.cb_af_zo, 0, 2, 1, 1)
		self.cb_af_mc = QtGui.QCheckBox(self.groupBox)
		self.cb_af_mc.setObjectName(_fromUtf8("cb_af_mc"))
		self.gridLayout_13.addWidget(self.cb_af_mc, 0, 0, 1, 2)
		self.cb_af_oa = QtGui.QCheckBox(self.groupBox)
		self.cb_af_oa.setObjectName(_fromUtf8("cb_af_oa"))
		self.gridLayout_13.addWidget(self.cb_af_oa, 1, 2, 1, 1)
		self.cb_af_lt = QtGui.QCheckBox(self.groupBox)
		self.cb_af_lt.setObjectName(_fromUtf8("cb_af_lt"))
		self.gridLayout_13.addWidget(self.cb_af_lt, 1, 0, 1, 1)
		self.gridLayout.addWidget(self.groupBox, 3, 0, 1, 1)
		self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
		self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
		self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
		self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
		self.label_gk_ag = QtGui.QLabel(self.groupBox_2)
		self.label_gk_ag.setObjectName(_fromUtf8("label_gk_ag"))
		self.verticalLayout_2.addWidget(self.label_gk_ag)
		self.label_gk_an = QtGui.QLabel(self.groupBox_2)
		self.label_gk_an.setObjectName(_fromUtf8("label_gk_an"))
		self.verticalLayout_2.addWidget(self.label_gk_an)
		self.label_gk_fa = QtGui.QLabel(self.groupBox_2)
		self.label_gk_fa.setObjectName(_fromUtf8("label_gk_fa"))
		self.verticalLayout_2.addWidget(self.label_gk_fa)
		self.label_gk_ws = QtGui.QLabel(self.groupBox_2)
		self.label_gk_ws.setObjectName(_fromUtf8("label_gk_ws"))
		self.verticalLayout_2.addWidget(self.label_gk_ws)
		self.label_gk_rest = QtGui.QLabel(self.groupBox_2)
		self.label_gk_rest.setWordWrap(False)
		self.label_gk_rest.setObjectName(_fromUtf8("label_gk_rest"))
		self.verticalLayout_2.addWidget(self.label_gk_rest)
		self.gridLayout.addWidget(self.groupBox_2, 3, 2, 1, 1)
		self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
		self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
		self.gridLayout_10 = QtGui.QGridLayout(self.groupBox_3)
		self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
		self.entry_suchbegriffe = QtGui.QLineEdit(self.groupBox_3)
									 
		self.entry_suchbegriffe.setObjectName(_fromUtf8("entry_suchbegriffe"))
		self.gridLayout_10.addWidget(self.entry_suchbegriffe, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.groupBox_3, 4, 2, 1, 1)
		self.groupBox_klassen = QtGui.QGroupBox(self.centralwidget)
		self.groupBox_klassen.setMaximumSize(QtCore.QSize(367, 16777215))
		self.groupBox_klassen.setObjectName(_fromUtf8("groupBox_klassen"))
		self.gridLayout_14 = QtGui.QGridLayout(self.groupBox_klassen)
		self.gridLayout_14.setObjectName(_fromUtf8("gridLayout_14"))
		self.cb_k5 = QtGui.QCheckBox(self.groupBox_klassen)
											  
		self.cb_k5.setObjectName(_fromUtf8("cb_k5"))
		self.gridLayout_14.addWidget(self.cb_k5, 0, 0, 1, 1)
		self.cb_k7 = QtGui.QCheckBox(self.groupBox_klassen)
		self.cb_k7.setObjectName(_fromUtf8("cb_k7"))
		self.gridLayout_14.addWidget(self.cb_k7, 0, 1, 1, 1)
		self.cb_k6 = QtGui.QCheckBox(self.groupBox_klassen)
		self.cb_k6.setObjectName(_fromUtf8("cb_k6"))
		self.gridLayout_14.addWidget(self.cb_k6, 1, 0, 1, 1)
		self.cb_k8 = QtGui.QCheckBox(self.groupBox_klassen)
		self.cb_k8.setObjectName(_fromUtf8("cb_k8"))
		self.gridLayout_14.addWidget(self.cb_k8, 1, 1, 1, 1)
		self.gridLayout.addWidget(self.groupBox_klassen, 4, 0, 2, 1)
		self.horizontalLayout_2 = QtGui.QHBoxLayout()
		self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
		self.cb_solution = QtGui.QCheckBox(self.centralwidget)
		self.cb_solution.setObjectName(_fromUtf8("cb_solution"))
		self.horizontalLayout_2.addWidget(self.cb_solution, QtCore.Qt.AlignLeft)
		self.btn_suche = QtGui.QPushButton(self.centralwidget)
		self.btn_suche.setEnabled(True)
		self.btn_suche.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
		self.btn_suche.setAcceptDrops(False)
		self.btn_suche.setObjectName(_fromUtf8("btn_suche"))
		self.horizontalLayout_2.addWidget(self.btn_suche)
		self.gridLayout.addLayout(self.horizontalLayout_2, 5, 2, 1, 1)
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
		self.btn_refreshddb = QtGui.QPushButton(self.centralwidget)
		self.btn_refreshddb.setObjectName(_fromUtf8("btn_refreshddb"))
		self.horizontalLayout.addWidget(self.btn_refreshddb)
		self.label_update = QtGui.QLabel(self.centralwidget)
		self.label_update.setObjectName(_fromUtf8("label_update"))
		self.horizontalLayout.addWidget(self.label_update)
		self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
		self.menu_searchtype = QtGui.QComboBox(self.centralwidget)
		# self.menu_searchtype.setMaximumSize(QtCore.QSize(400, 16777215))
		self.menu_searchtype.setEnabled(True)
		self.menu_searchtype.setObjectName(_fromUtf8("menu_searchtype"))
		self.menu_searchtype.addItem(_fromUtf8(""))
		self.menu_searchtype.addItem(_fromUtf8(""))
		self.menu_searchtype.addItem(_fromUtf8(""))
		self.gridLayout.addWidget(self.menu_searchtype, 0, 2, 1, 1)
		self.groupBox_4 = QtGui.QGroupBox(self.centralwidget)
		self.groupBox_4.setMaximumSize(QtCore.QSize(367, 16777215))
		self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
		self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_4)
		self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
		self.tabWidget = QtGui.QTabWidget(self.groupBox_4)
		self.tabWidget.setStyleSheet(_fromUtf8("background-color: rgb(229, 246, 255);"))
		self.tabWidget.setMovable(False)
		self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
		self.tab_k5 = QtGui.QWidget()
		self.tab_k5.setObjectName(_fromUtf8("tab_k5"))
		self.gridLayout_3 = QtGui.QGridLayout(self.tab_k5)
		self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
		self.cb_k5_fu = QtGui.QCheckBox(self.tab_k5)
		self.cb_k5_fu.setObjectName(_fromUtf8("cb_k5_fu"))
		self.gridLayout_3.addWidget(self.cb_k5_fu, 0, 0, 1, 1)
		self.cb_k5_gl = QtGui.QCheckBox(self.tab_k5)
		self.cb_k5_gl.setStyleSheet(_fromUtf8(""))
		self.cb_k5_gl.setObjectName(_fromUtf8("cb_k5_gl"))
		self.gridLayout_3.addWidget(self.cb_k5_gl, 1, 0, 1, 1)
		self.cb_k5_mzr = QtGui.QCheckBox(self.tab_k5)
		self.cb_k5_mzr.setObjectName(_fromUtf8("cb_k5_mzr"))
		self.gridLayout_3.addWidget(self.cb_k5_mzr, 2, 0, 1, 1)
		self.cb_k5_tr = QtGui.QCheckBox(self.tab_k5)
		self.cb_k5_tr.setObjectName(_fromUtf8("cb_k5_tr"))
		self.gridLayout_3.addWidget(self.cb_k5_tr, 3, 0, 1, 1)
		self.cb_k5_vag2 = QtGui.QCheckBox(self.tab_k5)
		self.cb_k5_vag2.setObjectName(_fromUtf8("cb_k5_vag2"))
		self.gridLayout_3.addWidget(self.cb_k5_vag2, 4, 0, 1, 1)
		self.btn_K5 = QtGui.QPushButton(self.tab_k5)
		self.btn_K5.setStyleSheet(_fromUtf8("background-color: rgb(240, 240, 240);"))
		self.btn_K5.setObjectName(_fromUtf8("btn_K5"))
		self.gridLayout_3.addWidget(self.btn_K5, 5, 0, 1, 1, QtCore.Qt.AlignRight)
		self.tabWidget.addTab(self.tab_k5, _fromUtf8(""))
		self.tab_k6 = QtGui.QWidget()
		self.tab_k6.setObjectName(_fromUtf8("tab_k6"))
		self.gridLayout_6 = QtGui.QGridLayout(self.tab_k6)
		self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
		self.cb_k6_pwlu = QtGui.QCheckBox(self.tab_k6)
		self.cb_k6_pwlu.setObjectName(_fromUtf8("cb_k6_pwlu"))
		self.gridLayout_6.addWidget(self.cb_k6_pwlu, 2, 0, 1, 1)
		self.cb_k6_fo = QtGui.QCheckBox(self.tab_k6)
		self.cb_k6_fo.setObjectName(_fromUtf8("cb_k6_fo"))
		self.gridLayout_6.addWidget(self.cb_k6_fo, 1, 0, 1, 1)
		self.cb_k6_rf = QtGui.QCheckBox(self.tab_k6)
		self.cb_k6_rf.setObjectName(_fromUtf8("cb_k6_rf"))
		self.gridLayout_6.addWidget(self.cb_k6_rf, 4, 0, 1, 1)
		self.cb_k6_vag3 = QtGui.QCheckBox(self.tab_k6)
		self.cb_k6_vag3.setObjectName(_fromUtf8("cb_k6_vag3"))
		self.gridLayout_6.addWidget(self.cb_k6_vag3, 10, 0, 1, 1)
		self.btn_K6 = QtGui.QPushButton(self.tab_k6)
		self.btn_K6.setStyleSheet(_fromUtf8("background-color: rgb(240, 240, 240);"))
		self.btn_K6.setObjectName(_fromUtf8("btn_K6"))
		self.gridLayout_6.addWidget(self.btn_K6, 12, 0, 1, 3, QtCore.Qt.AlignRight)
		self.cb_k6_re = QtGui.QCheckBox(self.tab_k6)
		self.cb_k6_re.setObjectName(_fromUtf8("cb_k6_re"))
		self.gridLayout_6.addWidget(self.cb_k6_re, 3, 0, 1, 1)
		self.cb_k6_bsw = QtGui.QCheckBox(self.tab_k6)
		self.cb_k6_bsw.setObjectName(_fromUtf8("cb_k6_bsw"))
		self.gridLayout_6.addWidget(self.cb_k6_bsw, 0, 0, 1, 1)
		self.tabWidget.addTab(self.tab_k6, _fromUtf8(""))
		self.tab_k7 = QtGui.QWidget()
		self.tab_k7.setObjectName(_fromUtf8("tab_k7"))
		self.gridLayout_7 = QtGui.QGridLayout(self.tab_k7)
		self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
		self.cb_k7_kkk = QtGui.QCheckBox(self.tab_k7)
		self.cb_k7_kkk.setObjectName(_fromUtf8("cb_k7_kkk"))
		self.gridLayout_7.addWidget(self.cb_k7_kkk, 3, 0, 1, 1)
		self.cb_k7_dr = QtGui.QCheckBox(self.tab_k7)
		self.cb_k7_dr.setObjectName(_fromUtf8("cb_k7_dr"))
		self.gridLayout_7.addWidget(self.cb_k7_dr, 0, 0, 1, 1)
		self.cb_k7_dwv = QtGui.QCheckBox(self.tab_k7)
		self.cb_k7_dwv.setObjectName(_fromUtf8("cb_k7_dwv"))
		self.gridLayout_7.addWidget(self.cb_k7_dwv, 1, 0, 1, 1)
		self.cb_k7_kz = QtGui.QCheckBox(self.tab_k7)
		self.cb_k7_kz.setObjectName(_fromUtf8("cb_k7_kz"))
		self.gridLayout_7.addWidget(self.cb_k7_kz, 4, 0, 1, 1)
		self.cb_k7_wm = QtGui.QCheckBox(self.tab_k7)
		self.cb_k7_wm.setObjectName(_fromUtf8("cb_k7_wm"))
		self.gridLayout_7.addWidget(self.cb_k7_wm, 5, 0, 1, 1)
		self.btn_K7 = QtGui.QPushButton(self.tab_k7)
		self.btn_K7.setStyleSheet(_fromUtf8("background-color: rgb(240, 240, 240);"))
		self.btn_K7.setObjectName(_fromUtf8("btn_K7"))
		self.gridLayout_7.addWidget(self.btn_K7, 7, 0, 1, 1, QtCore.Qt.AlignRight)
		self.cb_k7_ghg = QtGui.QCheckBox(self.tab_k7)
		self.cb_k7_ghg.setObjectName(_fromUtf8("cb_k7_ghg"))
		self.gridLayout_7.addWidget(self.cb_k7_ghg, 2, 0, 1, 1)
		self.tabWidget.addTab(self.tab_k7, _fromUtf8(""))
		self.tab_k8 = QtGui.QWidget()
		self.tab_k8.setObjectName(_fromUtf8("tab_k8"))
		self.gridLayout_8 = QtGui.QGridLayout(self.tab_k8)
		self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
		self.cb_k8_ir = QtGui.QCheckBox(self.tab_k8)
		self.cb_k8_ir.setObjectName(_fromUtf8("cb_k8_ir"))
		self.gridLayout_8.addWidget(self.cb_k8_ir, 1, 0, 1, 1)
		self.cb_k8_ddg = QtGui.QCheckBox(self.tab_k8)
		self.cb_k8_ddg.setObjectName(_fromUtf8("cb_k8_ddg"))
		self.gridLayout_8.addWidget(self.cb_k8_ddg, 0, 0, 1, 1)
		self.cb_k8_sws = QtGui.QCheckBox(self.tab_k8)
		self.cb_k8_sws.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
		self.cb_k8_sws.setObjectName(_fromUtf8("cb_k8_sws"))
		self.gridLayout_8.addWidget(self.cb_k8_sws, 2, 0, 1, 1)
		self.cb_k8_wm = QtGui.QCheckBox(self.tab_k8)
		self.cb_k8_wm.setObjectName(_fromUtf8("cb_k8_wm"))
		self.gridLayout_8.addWidget(self.cb_k8_wm, 3, 0, 1, 1)
		self.btn_K8 = QtGui.QPushButton(self.tab_k8)
		self.btn_K8.setStyleSheet(_fromUtf8("background-color: rgb(240, 240, 240);"))
		self.btn_K8.setObjectName(_fromUtf8("btn_K8"))
		self.gridLayout_8.addWidget(self.btn_K8, 4, 0, 1, 1, QtCore.Qt.AlignRight)
		self.tabWidget.addTab(self.tab_k8, _fromUtf8(""))
		self.verticalLayout.addWidget(self.tabWidget)
		self.gridLayout.addWidget(self.groupBox_4, 1, 0, 2, 1)
		self.groupBox_5 = QtGui.QGroupBox(self.centralwidget)
																  
		self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
		self.gridLayout_11 = QtGui.QGridLayout(self.groupBox_5)
		self.gridLayout_11.setObjectName(_fromUtf8("gridLayout_11"))
		self.tab_widget_gk = QtGui.QTabWidget(self.groupBox_5)
		self.tab_widget_gk.setMaximumSize(QtCore.QSize(650, 16777215))
		self.tab_widget_gk.setStyleSheet(_fromUtf8("background-color: rgb(217, 255, 215);"))
		self.tab_widget_gk.setObjectName(_fromUtf8("tab_widget_gk"))
		self.tab_ag = QtGui.QWidget()
		self.tab_ag.setObjectName(_fromUtf8("tab_ag"))
		self.gridLayout_2 = QtGui.QGridLayout(self.tab_ag)
		self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
		self.cb_ag26 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag26.setObjectName(_fromUtf8("cb_ag26"))
		self.gridLayout_2.addWidget(self.cb_ag26, 0, 1, 1, 1)
		self.cb_ag38 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag38.setObjectName(_fromUtf8("cb_ag38"))
		self.gridLayout_2.addWidget(self.cb_ag38, 0, 2, 1, 1)
		self.cb_ag39 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag39.setObjectName(_fromUtf8("cb_ag39"))
		self.gridLayout_2.addWidget(self.cb_ag39, 1, 2, 1, 1)
		self.cb_ag13 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag13.setObjectName(_fromUtf8("cb_ag13"))
		self.gridLayout_2.addWidget(self.cb_ag13, 2, 0, 1, 1)
		self.cb_ag31 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag31.setObjectName(_fromUtf8("cb_ag31"))
		self.gridLayout_2.addWidget(self.cb_ag31, 3, 1, 1, 1)
		self.cb_ag11 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag11.setObjectName(_fromUtf8("cb_ag11"))
		self.gridLayout_2.addWidget(self.cb_ag11, 0, 0, 1, 1)
		self.cb_ag27 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag27.setObjectName(_fromUtf8("cb_ag27"))
		self.gridLayout_2.addWidget(self.cb_ag27, 1, 1, 1, 1)
		self.cb_ag14 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag14.setObjectName(_fromUtf8("cb_ag14"))
		self.gridLayout_2.addWidget(self.cb_ag14, 3, 0, 1, 1)
		self.cb_ag42 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag42.setObjectName(_fromUtf8("cb_ag42"))
		self.gridLayout_2.addWidget(self.cb_ag42, 3, 2, 1, 1)
		self.cb_ag15 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag15.setObjectName(_fromUtf8("cb_ag15"))
		self.gridLayout_2.addWidget(self.cb_ag15, 4, 0, 1, 1)
		self.cb_ag12 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag12.setObjectName(_fromUtf8("cb_ag12"))
		self.gridLayout_2.addWidget(self.cb_ag12, 1, 0, 1, 1)
		self.cb_ag41 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag41.setObjectName(_fromUtf8("cb_ag41"))
		self.gridLayout_2.addWidget(self.cb_ag41, 2, 2, 1, 1)
		self.cb_ag28 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag28.setObjectName(_fromUtf8("cb_ag28"))
		self.gridLayout_2.addWidget(self.cb_ag28, 2, 1, 1, 1)
		self.cb_ag32 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag32.setObjectName(_fromUtf8("cb_ag32"))
		self.gridLayout_2.addWidget(self.cb_ag32, 4, 1, 1, 1)
		self.btn_ag_all = QtGui.QPushButton(self.tab_ag)
		self.btn_ag_all.setStyleSheet(_fromUtf8("background-color: rgb(240, 240, 240);"))
		self.btn_ag_all.setObjectName(_fromUtf8("btn_ag_all"))
		self.gridLayout_2.addWidget(self.btn_ag_all, 9, 2, 1, 1)
		self.cb_ag43 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag43.setObjectName(_fromUtf8("cb_ag43"))
		self.gridLayout_2.addWidget(self.cb_ag43, 4, 2, 1, 1)
		self.cb_ag35 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag35.setObjectName(_fromUtf8("cb_ag35"))
		self.gridLayout_2.addWidget(self.cb_ag35, 7, 1, 1, 1)
		self.cb_ag21 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag21.setObjectName(_fromUtf8("cb_ag21"))
		self.gridLayout_2.addWidget(self.cb_ag21, 5, 0, 1, 1)
		self.cb_ag52 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag52.setObjectName(_fromUtf8("cb_ag52"))
		self.gridLayout_2.addWidget(self.cb_ag52, 7, 2, 1, 1)
		self.cb_ag44 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag44.setObjectName(_fromUtf8("cb_ag44"))
		self.gridLayout_2.addWidget(self.cb_ag44, 5, 2, 1, 1)
		self.cb_ag34 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag34.setObjectName(_fromUtf8("cb_ag34"))
		self.gridLayout_2.addWidget(self.cb_ag34, 6, 1, 1, 1)
		self.cb_ag51 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag51.setObjectName(_fromUtf8("cb_ag51"))
		self.gridLayout_2.addWidget(self.cb_ag51, 6, 2, 1, 1)
		self.cb_ag23 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag23.setObjectName(_fromUtf8("cb_ag23"))
		self.gridLayout_2.addWidget(self.cb_ag23, 7, 0, 1, 1)
		self.cb_ag24 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag24.setObjectName(_fromUtf8("cb_ag24"))
		self.gridLayout_2.addWidget(self.cb_ag24, 8, 0, 1, 1)
		self.cb_ag36 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag36.setObjectName(_fromUtf8("cb_ag36"))
		self.gridLayout_2.addWidget(self.cb_ag36, 8, 1, 1, 1)
		self.cb_ag33 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag33.setObjectName(_fromUtf8("cb_ag33"))
		self.gridLayout_2.addWidget(self.cb_ag33, 5, 1, 1, 1)
		self.cb_ag53 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag53.setObjectName(_fromUtf8("cb_ag53"))
		self.gridLayout_2.addWidget(self.cb_ag53, 8, 2, 1, 1)
		self.cb_ag25 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag25.setObjectName(_fromUtf8("cb_ag25"))
		self.gridLayout_2.addWidget(self.cb_ag25, 9, 0, 1, 1)
		self.cb_ag22 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag22.setObjectName(_fromUtf8("cb_ag22"))
		self.gridLayout_2.addWidget(self.cb_ag22, 6, 0, 1, 1)
		self.cb_ag37 = QtGui.QCheckBox(self.tab_ag)
		self.cb_ag37.setObjectName(_fromUtf8("cb_ag37"))
		self.gridLayout_2.addWidget(self.cb_ag37, 9, 1, 1, 1)
		self.tab_widget_gk.addTab(self.tab_ag, _fromUtf8(""))
		self.tab_an = QtGui.QWidget()
		self.tab_an.setObjectName(_fromUtf8("tab_an"))
		self.gridLayout_4 = QtGui.QGridLayout(self.tab_an)
		self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
		self.cb_an11 = QtGui.QCheckBox(self.tab_an)
		self.cb_an11.setObjectName(_fromUtf8("cb_an11"))
		self.gridLayout_4.addWidget(self.cb_an11, 1, 0, 1, 1)
		self.cb_an12 = QtGui.QCheckBox(self.tab_an)
		self.cb_an12.setObjectName(_fromUtf8("cb_an12"))
		self.gridLayout_4.addWidget(self.cb_an12, 3, 0, 1, 1)
		self.cb_an13 = QtGui.QCheckBox(self.tab_an)
		self.cb_an13.setObjectName(_fromUtf8("cb_an13"))
		self.gridLayout_4.addWidget(self.cb_an13, 4, 0, 1, 1)
		self.cb_an15 = QtGui.QCheckBox(self.tab_an)
		self.cb_an15.setObjectName(_fromUtf8("cb_an15"))
		self.gridLayout_4.addWidget(self.cb_an15, 6, 0, 1, 1)
		self.cb_an14 = QtGui.QCheckBox(self.tab_an)
		self.cb_an14.setObjectName(_fromUtf8("cb_an14"))
		self.gridLayout_4.addWidget(self.cb_an14, 5, 0, 1, 1)
		self.cb_an21 = QtGui.QCheckBox(self.tab_an)
		self.cb_an21.setObjectName(_fromUtf8("cb_an21"))
		self.gridLayout_4.addWidget(self.cb_an21, 7, 0, 1, 1)
		self.cb_an22 = QtGui.QCheckBox(self.tab_an)
		self.cb_an22.setObjectName(_fromUtf8("cb_an22"))
		self.gridLayout_4.addWidget(self.cb_an22, 8, 0, 1, 1)
		self.btn_an_all = QtGui.QPushButton(self.tab_an)
		self.btn_an_all.setStyleSheet(_fromUtf8("background-color: rgb(240, 240, 240);"))
		self.btn_an_all.setObjectName(_fromUtf8("btn_an_all"))
		self.gridLayout_4.addWidget(self.btn_an_all, 11, 3, 1, 1)
		self.cb_an43 = QtGui.QCheckBox(self.tab_an)
		self.cb_an43.setObjectName(_fromUtf8("cb_an43"))
		self.gridLayout_4.addWidget(self.cb_an43, 8, 1, 1, 1)
		self.cb_an42 = QtGui.QCheckBox(self.tab_an)
		self.cb_an42.setObjectName(_fromUtf8("cb_an42"))
		self.gridLayout_4.addWidget(self.cb_an42, 7, 1, 1, 1)
		self.cb_an41 = QtGui.QCheckBox(self.tab_an)
		self.cb_an41.setObjectName(_fromUtf8("cb_an41"))
		self.gridLayout_4.addWidget(self.cb_an41, 6, 1, 1, 1)
		self.cb_an34 = QtGui.QCheckBox(self.tab_an)
		self.cb_an34.setObjectName(_fromUtf8("cb_an34"))
		self.gridLayout_4.addWidget(self.cb_an34, 5, 1, 1, 1)
		self.cb_an33 = QtGui.QCheckBox(self.tab_an)
		self.cb_an33.setObjectName(_fromUtf8("cb_an33"))
		self.gridLayout_4.addWidget(self.cb_an33, 4, 1, 1, 1)
		self.cb_an32 = QtGui.QCheckBox(self.tab_an)
		self.cb_an32.setObjectName(_fromUtf8("cb_an32"))
		self.gridLayout_4.addWidget(self.cb_an32, 3, 1, 1, 1)
		self.cb_an31 = QtGui.QCheckBox(self.tab_an)
		self.cb_an31.setObjectName(_fromUtf8("cb_an31"))
		self.gridLayout_4.addWidget(self.cb_an31, 1, 1, 1, 1)
		self.tab_widget_gk.addTab(self.tab_an, _fromUtf8(""))
		self.tab_fa = QtGui.QWidget()
		self.tab_fa.setObjectName(_fromUtf8("tab_fa"))
		self.gridLayout_5 = QtGui.QGridLayout(self.tab_fa)
		self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
		self.cb_fa66 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa66.setObjectName(_fromUtf8("cb_fa66"))
		self.gridLayout_5.addWidget(self.cb_fa66, 1, 3, 1, 1)
		self.cb_fa51 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa51.setObjectName(_fromUtf8("cb_fa51"))
		self.gridLayout_5.addWidget(self.cb_fa51, 1, 2, 1, 1)
		self.cb_fa24 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa24.setObjectName(_fromUtf8("cb_fa24"))
		self.gridLayout_5.addWidget(self.cb_fa24, 1, 1, 1, 1)
		self.cb_fa73 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa73.setObjectName(_fromUtf8("cb_fa73"))
		self.gridLayout_5.addWidget(self.cb_fa73, 8, 3, 1, 1)
		self.cb_fa44 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa44.setObjectName(_fromUtf8("cb_fa44"))
		self.gridLayout_5.addWidget(self.cb_fa44, 0, 2, 1, 1)
		self.cb_fa65 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa65.setObjectName(_fromUtf8("cb_fa65"))
		self.gridLayout_5.addWidget(self.cb_fa65, 0, 3, 1, 1)
		self.cb_fa23 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa23.setObjectName(_fromUtf8("cb_fa23"))
		self.gridLayout_5.addWidget(self.cb_fa23, 0, 1, 1, 1)
		self.cb_fa71 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa71.setObjectName(_fromUtf8("cb_fa71"))
		self.gridLayout_5.addWidget(self.cb_fa71, 5, 3, 1, 1)
		self.cb_fa25 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa25.setObjectName(_fromUtf8("cb_fa25"))
		self.gridLayout_5.addWidget(self.cb_fa25, 5, 1, 1, 1)
		self.cb_fa72 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa72.setObjectName(_fromUtf8("cb_fa72"))
		self.gridLayout_5.addWidget(self.cb_fa72, 6, 3, 1, 1)
		self.cb_fa52 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa52.setObjectName(_fromUtf8("cb_fa52"))
		self.gridLayout_5.addWidget(self.cb_fa52, 5, 2, 1, 1)
		self.cb_fa54 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa54.setObjectName(_fromUtf8("cb_fa54"))
		self.gridLayout_5.addWidget(self.cb_fa54, 8, 2, 1, 1)
		self.cb_fa53 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa53.setObjectName(_fromUtf8("cb_fa53"))
		self.gridLayout_5.addWidget(self.cb_fa53, 6, 2, 1, 1)
		self.cb_fa11 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa11.setObjectName(_fromUtf8("cb_fa11"))
		self.gridLayout_5.addWidget(self.cb_fa11, 0, 0, 1, 1)
		self.cb_fa12 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa12.setObjectName(_fromUtf8("cb_fa12"))
		self.gridLayout_5.addWidget(self.cb_fa12, 1, 0, 1, 1)
		self.cb_fa13 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa13.setObjectName(_fromUtf8("cb_fa13"))
		self.gridLayout_5.addWidget(self.cb_fa13, 5, 0, 1, 1)
		self.cb_fa14 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa14.setObjectName(_fromUtf8("cb_fa14"))
		self.gridLayout_5.addWidget(self.cb_fa14, 6, 0, 1, 1)
		self.cb_fa15 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa15.setObjectName(_fromUtf8("cb_fa15"))
		self.gridLayout_5.addWidget(self.cb_fa15, 8, 0, 1, 1)
		self.cb_fa16 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa16.setObjectName(_fromUtf8("cb_fa16"))
		self.gridLayout_5.addWidget(self.cb_fa16, 9, 0, 1, 1)
		self.cb_fa17 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa17.setObjectName(_fromUtf8("cb_fa17"))
		self.gridLayout_5.addWidget(self.cb_fa17, 10, 0, 1, 1)
		self.cb_fa18 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa18.setObjectName(_fromUtf8("cb_fa18"))
		self.gridLayout_5.addWidget(self.cb_fa18, 11, 0, 1, 1)
		self.cb_fa19 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa19.setObjectName(_fromUtf8("cb_fa19"))
		self.gridLayout_5.addWidget(self.cb_fa19, 12, 0, 1, 1)
		self.cb_fa21 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa21.setObjectName(_fromUtf8("cb_fa21"))
		self.gridLayout_5.addWidget(self.cb_fa21, 15, 0, 1, 1)
		self.cb_fa26 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa26.setObjectName(_fromUtf8("cb_fa26"))
		self.gridLayout_5.addWidget(self.cb_fa26, 6, 1, 1, 1)
		self.cb_fa31 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa31.setObjectName(_fromUtf8("cb_fa31"))
		self.gridLayout_5.addWidget(self.cb_fa31, 8, 1, 1, 1)
		self.cb_fa32 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa32.setObjectName(_fromUtf8("cb_fa32"))
		self.gridLayout_5.addWidget(self.cb_fa32, 9, 1, 1, 1)
		self.cb_fa33 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa33.setObjectName(_fromUtf8("cb_fa33"))
		self.gridLayout_5.addWidget(self.cb_fa33, 10, 1, 1, 1)
		self.cb_fa34 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa34.setObjectName(_fromUtf8("cb_fa34"))
		self.gridLayout_5.addWidget(self.cb_fa34, 11, 1, 1, 1)
		self.cb_fa41 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa41.setObjectName(_fromUtf8("cb_fa41"))
		self.gridLayout_5.addWidget(self.cb_fa41, 12, 1, 1, 1)
		self.cb_fa42 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa42.setObjectName(_fromUtf8("cb_fa42"))
		self.gridLayout_5.addWidget(self.cb_fa42, 15, 1, 1, 1)
		self.cb_fa55 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa55.setObjectName(_fromUtf8("cb_fa55"))
		self.gridLayout_5.addWidget(self.cb_fa55, 9, 2, 1, 1)
		self.cb_fa56 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa56.setObjectName(_fromUtf8("cb_fa56"))
		self.gridLayout_5.addWidget(self.cb_fa56, 10, 2, 1, 1)
		self.cb_fa61 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa61.setObjectName(_fromUtf8("cb_fa61"))
		self.gridLayout_5.addWidget(self.cb_fa61, 11, 2, 1, 1)
		self.cb_fa62 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa62.setObjectName(_fromUtf8("cb_fa62"))
		self.gridLayout_5.addWidget(self.cb_fa62, 12, 2, 1, 1)
		self.cb_fa63 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa63.setObjectName(_fromUtf8("cb_fa63"))
		self.gridLayout_5.addWidget(self.cb_fa63, 15, 2, 1, 1)
		self.cb_fa74 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa74.setObjectName(_fromUtf8("cb_fa74"))
		self.gridLayout_5.addWidget(self.cb_fa74, 9, 3, 1, 1)
		self.cb_fa81 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa81.setObjectName(_fromUtf8("cb_fa81"))
		self.gridLayout_5.addWidget(self.cb_fa81, 10, 3, 1, 1)
		self.cb_fa82 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa82.setObjectName(_fromUtf8("cb_fa82"))
		self.gridLayout_5.addWidget(self.cb_fa82, 11, 3, 1, 1)
		self.cb_fa83 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa83.setObjectName(_fromUtf8("cb_fa83"))
		self.gridLayout_5.addWidget(self.cb_fa83, 12, 3, 1, 1)
		self.cb_fa84 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa84.setObjectName(_fromUtf8("cb_fa84"))
		self.gridLayout_5.addWidget(self.cb_fa84, 15, 3, 1, 1)
		self.cb_fa22 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa22.setObjectName(_fromUtf8("cb_fa22"))
		self.gridLayout_5.addWidget(self.cb_fa22, 17, 0, 1, 1)
		self.cb_fa43 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa43.setObjectName(_fromUtf8("cb_fa43"))
		self.gridLayout_5.addWidget(self.cb_fa43, 17, 1, 1, 1)
		self.cb_fa64 = QtGui.QCheckBox(self.tab_fa)
		self.cb_fa64.setObjectName(_fromUtf8("cb_fa64"))
		self.gridLayout_5.addWidget(self.cb_fa64, 17, 2, 1, 1)
		self.btn_fa_all = QtGui.QPushButton(self.tab_fa)
		#self.btn_fa_all.setMouseTracking(False)
		self.btn_fa_all.setStyleSheet(_fromUtf8("background-color: rgb(240, 240, 240);"))
		self.btn_fa_all.setObjectName(_fromUtf8("btn_fa_all"))
		self.gridLayout_5.addWidget(self.btn_fa_all, 17, 3, 1, 1)
		self.tab_widget_gk.addTab(self.tab_fa, _fromUtf8(""))
		self.tab_ws = QtGui.QWidget()
		self.tab_ws.setObjectName(_fromUtf8("tab_ws"))
		self.gridLayout_9 = QtGui.QGridLayout(self.tab_ws)
		self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
		self.cb_ws11 = QtGui.QCheckBox(self.tab_ws)
		self.cb_ws11.setObjectName(_fromUtf8("cb_ws11"))
		self.gridLayout_9.addWidget(self.cb_ws11, 0, 0, 1, 1)
		self.cb_ws12 = QtGui.QCheckBox(self.tab_ws)
		self.cb_ws12.setObjectName(_fromUtf8("cb_ws12"))
		self.gridLayout_9.addWidget(self.cb_ws12, 1, 0, 1, 1)
		self.cb_ws13 = QtGui.QCheckBox(self.tab_ws)
		self.cb_ws13.setObjectName(_fromUtf8("cb_ws13"))
		self.gridLayout_9.addWidget(self.cb_ws13, 2, 0, 1, 1)
		self.cb_ws14 = QtGui.QCheckBox(self.tab_ws)
		self.cb_ws14.setObjectName(_fromUtf8("cb_ws14"))
		self.gridLayout_9.addWidget(self.cb_ws14, 3, 0, 1, 1)
		self.cb_ws21 = QtGui.QCheckBox(self.tab_ws)
		self.cb_ws21.setObjectName(_fromUtf8("cb_ws21"))
		self.gridLayout_9.addWidget(self.cb_ws21, 4, 0, 1, 1)
		self.cb_ws22 = QtGui.QCheckBox(self.tab_ws)
		self.cb_ws22.setObjectName(_fromUtf8("cb_ws22"))
		self.gridLayout_9.addWidget(self.cb_ws22, 5, 0, 1, 1)
		self.cb_ws23 = QtGui.QCheckBox(self.tab_ws)
		self.cb_ws23.setObjectName(_fromUtf8("cb_ws23"))
		self.gridLayout_9.addWidget(self.cb_ws23, 6, 0, 1, 1)
		self.cb_ws24 = QtGui.QCheckBox(self.tab_ws)
		self.cb_ws24.setObjectName(_fromUtf8("cb_ws24"))
		self.gridLayout_9.addWidget(self.cb_ws24, 7, 0, 1, 1)
		self.cb_ws25 = QtGui.QCheckBox(self.tab_ws)
		self.cb_ws25.setObjectName(_fromUtf8("cb_ws25"))
		self.gridLayout_9.addWidget(self.cb_ws25, 8, 0, 1, 1)
		
		self.btn_ws_all = QtGui.QPushButton(self.tab_ws)
		self.btn_ws_all.setStyleSheet(_fromUtf8("background-color: rgb(240, 240, 240);"))
		self.btn_ws_all.setObjectName(_fromUtf8("btn_ws_all"))
		self.gridLayout_9.addWidget(self.btn_ws_all, 9, 2, 1, 1)
		self.cb_ws41 = QtGui.QCheckBox(self.tab_ws)
		self.cb_ws41.setObjectName(_fromUtf8("cb_ws41"))
		self.gridLayout_9.addWidget(self.cb_ws41, 6, 1, 1, 1)
		self.cb_ws42 = QtGui.QCheckBox(self.tab_ws)
		self.cb_ws42.setObjectName(_fromUtf8("cb_ws42"))
		self.gridLayout_9.addWidget(self.cb_ws42, 7, 1, 1, 1)
		self.cb_ws35 = QtGui.QCheckBox(self.tab_ws)
		self.cb_ws35.setObjectName(_fromUtf8("cb_ws35"))
		self.gridLayout_9.addWidget(self.cb_ws35, 5, 1, 1, 1)
		self.cb_ws34 = QtGui.QCheckBox(self.tab_ws)
		self.cb_ws34.setObjectName(_fromUtf8("cb_ws34"))
		self.gridLayout_9.addWidget(self.cb_ws34, 4, 1, 1, 1)
		self.cb_ws33 = QtGui.QCheckBox(self.tab_ws)
		self.cb_ws33.setObjectName(_fromUtf8("cb_ws33"))
		self.gridLayout_9.addWidget(self.cb_ws33, 3, 1, 1, 1)
		self.cb_ws32 = QtGui.QCheckBox(self.tab_ws)
		self.cb_ws32.setObjectName(_fromUtf8("cb_ws32"))
		self.gridLayout_9.addWidget(self.cb_ws32, 2, 1, 1, 1)
		self.cb_ws31 = QtGui.QCheckBox(self.tab_ws)
		self.cb_ws31.setObjectName(_fromUtf8("cb_ws31"))
		self.gridLayout_9.addWidget(self.cb_ws31, 1, 1, 1, 1)
		self.cb_ws26 = QtGui.QCheckBox(self.tab_ws)
		self.cb_ws26.setObjectName(_fromUtf8("cb_ws26"))
		self.gridLayout_9.addWidget(self.cb_ws26, 0, 1, 1, 1)
		self.tab_widget_gk.addTab(self.tab_ws, _fromUtf8(""))
		self.gridLayout_11.addWidget(self.tab_widget_gk, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.groupBox_5, 1, 2, 2, 1)
		MainWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtGui.QStatusBar(MainWindow)
		self.statusbar.setObjectName(_fromUtf8("statusbar"))
		MainWindow.setStatusBar(self.statusbar)
		self.actionExit = QtGui.QAction(MainWindow)
		self.actionExit.setObjectName(_fromUtf8("actionExit"))
		self.actionE = QtGui.QAction(MainWindow)
		self.actionE.setObjectName(_fromUtf8("actionE"))
		self.actionNew = QtGui.QAction(MainWindow)
		self.actionNew.setObjectName(_fromUtf8("actionNew"))

		self.retranslateUi(MainWindow)
		self.tabWidget.setCurrentIndex(0)
															   
		self.tab_widget_gk.setCurrentIndex(0)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		
		
		############################################################################
		############## Commands ####################################################
		############################################################################
		self.btn_refreshddb.clicked.connect(self.refresh_ddb)
		self.btn_K5.clicked.connect(self.btn_K5_pressed)
		self.btn_K6.clicked.connect(self.btn_K6_pressed)
		self.btn_K7.clicked.connect(self.btn_K7_pressed)
		self.btn_K8.clicked.connect(self.btn_K8_pressed)
		self.btn_ag_all.clicked.connect(self.btn_ag_all_pressed)
		self.btn_an_all.clicked.connect(self.btn_an_all_pressed)
		self.btn_fa_all.clicked.connect(self.btn_fa_all_pressed)
		self.btn_ws_all.clicked.connect(self.btn_ws_all_pressed)
		self.btn_suche.clicked.connect(self.PrepareTeXforPDF)
		
		
		
		for all in ag_kb_beschreibung:
			x=eval('self.cb_'+all)
			x.stateChanged.connect(self.cb_ag_checked)
		
		for all in an_kb_beschreibung:
			x=eval('self.cb_'+all)
			x.stateChanged.connect(self.cb_an_checked)
			
		for all in fa_kb_beschreibung:
			x=eval('self.cb_'+all)
			x.stateChanged.connect(self.cb_fa_checked)
			
		for all in ws_kb_beschreibung:
			x=eval('self.cb_'+all)
			x.stateChanged.connect(self.cb_ws_checked)
		
		for all in themen_klasse_5:
			x=eval('self.cb_k5_'+all)
			x.stateChanged.connect(self.cb_rest_checked)
		
		for all in themen_klasse_6:
			x=eval('self.cb_k6_'+all)
			x.stateChanged.connect(self.cb_rest_checked)

		for all in themen_klasse_7:
			x=eval('self.cb_k7_'+all)
			x.stateChanged.connect(self.cb_rest_checked)

		for all in themen_klasse_8:
			x=eval('self.cb_k8_'+all)
			x.stateChanged.connect(self.cb_rest_checked)
			
		
		############################################################################################
		##############################################################################################
	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
		self.groupBox.setTitle(_translate("MainWindow", "Gesuchte Aufgabenformate:", None))
		self.cb_af_zo.setText(_translate("MainWindow", "Zuordnungsformat (ZO)", None))
		self.cb_af_mc.setText(_translate("MainWindow", "Multiplechoice (MC)", None))
		self.cb_af_oa.setText(_translate("MainWindow", "Offenes Antwortformat (OA)", None))
		self.cb_af_lt.setText(_translate("MainWindow", "Lückentext (LT)", None))
		self.groupBox_2.setTitle(_translate("MainWindow", "Ausgewählte Grundkompetenzen", None))
		# self.label_gk_ag.setText(_translate("MainWindow", "AG:", None))
		# self.label_gk_an.setText(_translate("MainWindow", "AN:", None))
		# self.label_gk_fa.setText(_translate("MainWindow", "FA:", None))
		# self.label_gk_ws.setText(_translate("MainWindow", "WS:", None))
		# self.label_gk_rest.setText(_translate("MainWindow", "", None))
		self.groupBox_3.setTitle(_translate("MainWindow", "Titelsuche:", None))
		self.groupBox_klassen.setTitle(_translate("MainWindow", "Klassen", None))
		self.cb_k7.setText(_translate("MainWindow", "7. Klasse", None))
		self.cb_k5.setText(_translate("MainWindow", "5. Klasse", None))
		self.cb_k6.setText(_translate("MainWindow", "6. Klasse", None))
		self.cb_k8.setText(_translate("MainWindow", "8. Klasse", None))
		self.cb_solution.setText(_translate("MainWindow", "Lösungen anzeigen", None))
		try:
			log_file=os.path.join(os.path.dirname('__file__'),'Teildokument','log_file')
			self.label_update.setText(_translate("MainWindow", 'Last Update: ' + self.modification_date(log_file).strftime('%d.%m.%y - %H:%M'), None))
		except FileNotFoundError:
			self.label_update.setText(_translate("MainWindow", "Last Update: ---", None))
		self.btn_suche.setText(_translate("MainWindow", "Suche starten!", None))
		self.btn_refreshddb.setText(_translate("MainWindow", "Refresh Database", None))
		self.menu_searchtype.setItemText(0, _translate("MainWindow", "Alle Dateien ausgeben, die zumindest ein Suchkriterium enthalten", None))
		self.menu_searchtype.setItemText(1, _translate("MainWindow", "Alle Dateien ausgeben, die alle Suchkriterien enthalten", None))
		self.groupBox_4.setTitle(_translate("MainWindow", "Themen Schulstufe", None))																					 
		self.cb_k5_fu.setText(_translate("MainWindow", "Funktionen (FU)", None))
		self.cb_k5_gl.setText(_translate("MainWindow", "Gleichungen und\n"
"Gleichungssysteme (GL)", None))
		self.cb_k5_mzr.setText(_translate("MainWindow", "Mengen, Zahlen,\n"
"Rechengesetze (MZR)", None))
		self.cb_k5_tr.setText(_translate("MainWindow", "Trigonometrie (TR)", None))
		self.cb_k5_vag2.setText(_translate("MainWindow", "Vektoren und analytisch\n"
"Geometrie (VAG2)", None))
		self.btn_K5.setText(_translate("MainWindow", "alle auswählen", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_k5), _translate("MainWindow", "5. Klasse", None))
		self.cb_k6_pwlu.setText(_translate("MainWindow", "Potenzen, Wurzeln, Logarithmen\n"
"und Ungleichungen (PWLU)", None))
		self.cb_k6_fo.setText(_translate("MainWindow", "Folgen (FO)", None))
		self.cb_k6_rf.setText(_translate("MainWindow", "Reelle Funktionen (RF)", None))
		self.cb_k6_vag3.setText(_translate("MainWindow", "Vektoren und analytische\n"
"Geometrie in R3 und Rn (VAG3)", None))
		self.btn_K6.setText(_translate("MainWindow", "alle auswählen", None))
		self.cb_k6_re.setText(_translate("MainWindow", "Reihen (RE)", None))
		self.cb_k6_bsw.setText(_translate("MainWindow", "Beschreibende Statistik\n"
"und Wahrscheinlichkeit (BSW)", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_k6), _translate("MainWindow", "6. Klasse", None))
		self.cb_k7_kkk.setText(_translate("MainWindow", "Kreise, Kugeln, Kegelschnittslinien\n"
"und andere Kurven (KKK)", None))
		self.cb_k7_dr.setText(_translate("MainWindow", "Differentialrechnung (DR)", None))
		self.cb_k7_dwv.setText(_translate("MainWindow", "Diskrete Wahrscheinlichkeits-\n"
"verteilungen (DWV)", None))
		self.cb_k7_kz.setText(_translate("MainWindow", "Komplexe Zahlen (KZ)", None))
		self.cb_k7_wm.setText(_translate("MainWindow", "Wirtschaftsmathematik (WM)", None))
		self.btn_K7.setText(_translate("MainWindow", "alle auswählen", None))
		self.cb_k7_ghg.setText(_translate("MainWindow", "Gleichungen höheren Grades als 2 (GHG)", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_k7), _translate("MainWindow", "7. Klasse", None))
		self.cb_k8_ir.setText(_translate("MainWindow", "Integralrechnung (IR)", None))
		self.cb_k8_ddg.setText(_translate("MainWindow", "Differenzen- und Differential-\n"
"gleichungen; Grundlagen\n"
"der Systemdynamik (DDG)", None))
		self.cb_k8_sws.setText(_translate("MainWindow", "Stetgie Wahrscheinlichkeits-\n"
"verteilungen; Beurteilende\n"
"Statistik (SWS)", None))
		self.cb_k8_wm.setText(_translate("MainWindow", "Wirtschaftsmathematik (WM)", None))
		self.btn_K8.setText(_translate("MainWindow", "alle auswählen", None))
		self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_k8), _translate("MainWindow", "8. Klasse", None))
		self.groupBox_5.setTitle(_translate("MainWindow", "Grundkompetenzen", None))
		
############# Infos for GKs
		for all in ag_kb_beschreibung:
			x=eval('self.cb_'+all)
			x.setToolTip(ag_kb_beschreibung[all])
			
		for all in an_kb_beschreibung:
			x=eval('self.cb_'+all)
			x.setToolTip(an_kb_beschreibung[all])

		for all in fa_kb_beschreibung:
			x=eval('self.cb_'+all)
			x.setToolTip(fa_kb_beschreibung[all])
			
		for all in ws_kb_beschreibung:
			x=eval('self.cb_'+all)
			x.setToolTip(ws_kb_beschreibung[all])
			
#########################################

		self.cb_ag11.setText(_translate("MainWindow", "AG 1.1", None))
		self.cb_ag12.setText(_translate("MainWindow", "AG 1.2", None))
		self.cb_ag13.setText(_translate("MainWindow", "AG-L 1.3", None))
		self.cb_ag14.setText(_translate("MainWindow", "AG-L 1.4", None))
		self.cb_ag15.setText(_translate("MainWindow", "AG-L 1.5", None))
		self.cb_ag21.setText(_translate("MainWindow", "AG 2.1", None))
		self.cb_ag22.setText(_translate("MainWindow", "AG 2.2", None))
		self.cb_ag23.setText(_translate("MainWindow", "AG 2.3", None))
		self.cb_ag24.setText(_translate("MainWindow", "AG 2.4", None))
		self.cb_ag25.setText(_translate("MainWindow", "AG 2.5", None))
		self.cb_ag26.setText(_translate("MainWindow", "AG-L 2.6", None))
		self.cb_ag27.setText(_translate("MainWindow", "AG-L 2.7 ", None))
		self.cb_ag28.setText(_translate("MainWindow", "AG-L 2.8", None))
		self.cb_ag31.setText(_translate("MainWindow", "AG 3.1", None))
		self.cb_ag32.setText(_translate("MainWindow", "AG 3.2", None))
		self.cb_ag33.setText(_translate("MainWindow", "AG 3.3", None))
		self.cb_ag34.setText(_translate("MainWindow", "AG 3.4", None))
		self.cb_ag35.setText(_translate("MainWindow", "AG 3.5", None))
		self.cb_ag36.setText(_translate("MainWindow", "AG-L 3.6", None))
		self.cb_ag37.setText(_translate("MainWindow", "AG-L 3.7", None))
		self.cb_ag38.setText(_translate("MainWindow", "AG-L 3.8", None))
		self.cb_ag39.setText(_translate("MainWindow", "AG-L 3.9", None))
		self.cb_ag41.setText(_translate("MainWindow", "AG 4.1", None))
		self.cb_ag42.setText(_translate("MainWindow", "AG 4.2", None))
		self.cb_ag43.setText(_translate("MainWindow", "AG-L 4.3 ", None))
		self.cb_ag44.setText(_translate("MainWindow", "AG-L 4.4", None))
		self.cb_ag51.setText(_translate("MainWindow", "AG-L 5.1", None))
		self.cb_ag52.setText(_translate("MainWindow", "AG-L 5.2", None))
		self.cb_ag53.setText(_translate("MainWindow", "AG-L 5.3", None))
		self.btn_ag_all.setText(_translate("MainWindow", "alle auswählen", None))
		self.tab_widget_gk.setTabText(self.tab_widget_gk.indexOf(self.tab_ag), _translate("MainWindow", "Algebra und Geometrie", None))
		self.cb_an11.setText(_translate("MainWindow", "AN 1.1", None))
		self.cb_an12.setText(_translate("MainWindow", "AN 1.2", None))
		self.cb_an13.setText(_translate("MainWindow", "AN 1.3", None))
		self.cb_an15.setText(_translate("MainWindow", "AN-L 1.5", None))
		self.cb_an14.setText(_translate("MainWindow", "AN 1.4", None))
		self.cb_an21.setText(_translate("MainWindow", "AN 2.1", None))
		self.cb_an22.setText(_translate("MainWindow", "AN-L 2.2", None))
		self.btn_an_all.setText(_translate("MainWindow", "alle auswählen", None))
		self.cb_an43.setText(_translate("MainWindow", "AN 4.3 ", None))
		self.cb_an42.setText(_translate("MainWindow", "AN 4.2", None))
		self.cb_an41.setText(_translate("MainWindow", "AN 4.1", None))
		self.cb_an34.setText(_translate("MainWindow", "AN-L 3.4", None))
		self.cb_an33.setText(_translate("MainWindow", "AN 3.3", None))
		self.cb_an32.setText(_translate("MainWindow", "AN 3.2", None))
		self.cb_an31.setText(_translate("MainWindow", "AN 3.1", None))
		self.tab_widget_gk.setTabText(self.tab_widget_gk.indexOf(self.tab_an), _translate("MainWindow", "Analysis", None))
		self.cb_fa66.setText(_translate("MainWindow", "FA 6.6", None))
		self.cb_fa51.setText(_translate("MainWindow", "FA 5.1", None))
		self.cb_fa24.setText(_translate("MainWindow", "FA 2.4", None))
		self.cb_fa73.setText(_translate("MainWindow", "FA-L 7.3", None))
		self.cb_fa44.setText(_translate("MainWindow", "FA 4.4", None))
		self.cb_fa65.setText(_translate("MainWindow", "FA 6.5", None))
		self.cb_fa23.setText(_translate("MainWindow", "FA 2.3", None))
		self.cb_fa71.setText(_translate("MainWindow", "FA-L 7.1", None))
		self.cb_fa25.setText(_translate("MainWindow", "FA 2.5", None))
		self.cb_fa72.setText(_translate("MainWindow", "FA-L 7.2", None))
		self.cb_fa52.setText(_translate("MainWindow", "FA 5.2", None))
		self.cb_fa54.setText(_translate("MainWindow", "FA 5.4", None))
		self.cb_fa53.setText(_translate("MainWindow", "FA 5.3", None))
		self.cb_fa11.setText(_translate("MainWindow", "FA 1.1", None))
		self.cb_fa12.setText(_translate("MainWindow", "FA 1.2", None))
		self.cb_fa13.setText(_translate("MainWindow", "FA 1.3", None))
		self.cb_fa14.setText(_translate("MainWindow", "FA 1.4", None))
		self.cb_fa15.setText(_translate("MainWindow", "FA 1.5", None))
		self.cb_fa16.setText(_translate("MainWindow", "FA 1.6", None))
		self.cb_fa17.setText(_translate("MainWindow", "FA 1.7", None))
		self.cb_fa18.setText(_translate("MainWindow", "FA 1.8", None))
		self.cb_fa19.setText(_translate("MainWindow", "FA 1.9", None))
		self.cb_fa21.setText(_translate("MainWindow", "FA 2.1", None))
		self.cb_fa26.setText(_translate("MainWindow", "FA 2.6", None))
		self.cb_fa31.setText(_translate("MainWindow", "FA 3.1", None))
		self.cb_fa32.setText(_translate("MainWindow", "FA 3.2", None))
		self.cb_fa33.setText(_translate("MainWindow", "FA 3.3", None))
		self.cb_fa34.setText(_translate("MainWindow", "FA 3.4", None))
		self.cb_fa41.setText(_translate("MainWindow", "FA 4.1", None))
		self.cb_fa42.setText(_translate("MainWindow", "FA 4.2", None))
		self.cb_fa55.setText(_translate("MainWindow", "FA 5.5", None))
		self.cb_fa56.setText(_translate("MainWindow", "FA 5.6", None))
		self.cb_fa61.setText(_translate("MainWindow", "FA 6.1", None))
		self.cb_fa62.setText(_translate("MainWindow", "FA 6.2", None))
		self.cb_fa63.setText(_translate("MainWindow", "FA 6.3", None))
		self.cb_fa74.setText(_translate("MainWindow", "FA-L 7.4", None))
		self.cb_fa81.setText(_translate("MainWindow", "FA-L 8.1", None))
		self.cb_fa82.setText(_translate("MainWindow", "FA-L 8.2", None))
		self.cb_fa83.setText(_translate("MainWindow", "FA-L 8.3", None))
		self.cb_fa84.setText(_translate("MainWindow", "FA-L 8.4", None))
		self.cb_fa22.setText(_translate("MainWindow", "FA 2.2", None))
		self.cb_fa43.setText(_translate("MainWindow", "FA 4.3", None))
		self.cb_fa64.setText(_translate("MainWindow", "FA 6.4", None))
		self.btn_fa_all.setText(_translate("MainWindow", "alle auswählen", None))
		self.tab_widget_gk.setTabText(self.tab_widget_gk.indexOf(self.tab_fa), _translate("MainWindow", "Funktionale Abhängigkeiten", None))
		self.cb_ws11.setText(_translate("MainWindow", "WS 1.1", None))
		self.cb_ws12.setText(_translate("MainWindow", "WS 1.2", None))
		self.cb_ws13.setText(_translate("MainWindow", "WS 1.3", None))
		self.cb_ws14.setText(_translate("MainWindow", "WS 1.4", None))
		self.cb_ws21.setText(_translate("MainWindow", "WS 2.1", None))
		self.cb_ws22.setText(_translate("MainWindow", "WS 2.2", None))
		self.cb_ws23.setText(_translate("MainWindow", "WS 2.3", None))
		self.cb_ws24.setText(_translate("MainWindow", "WS 2.4", None))
		self.cb_ws25.setText(_translate("MainWindow", "WS-L 2.5", None))
		self.btn_ws_all.setText(_translate("MainWindow", "alle auswählen", None))
		self.cb_ws41.setText(_translate("MainWindow", "WS 4.1", None))
		self.cb_ws42.setText(_translate("MainWindow", "WS-L 4.2", None))
		self.cb_ws35.setText(_translate("MainWindow", "WS-L 3.5", None))
		self.cb_ws34.setText(_translate("MainWindow", "WS 3.4", None))
		self.cb_ws33.setText(_translate("MainWindow", "WS 3.3", None))
		self.cb_ws32.setText(_translate("MainWindow", "WS 3.2", None))
		self.cb_ws31.setText(_translate("MainWindow", "WS 3.1", None))
		self.cb_ws26.setText(_translate("MainWindow", "WS-L 2.6", None))
		self.tab_widget_gk.setTabText(self.tab_widget_gk.indexOf(self.tab_ws), _translate("MainWindow", "Wahrscheinlichkeit und Statistik", None))
		self.actionExit.setText(_translate("MainWindow", "Exit", None))
		self.actionE.setText(_translate("MainWindow", "Exit", None))
		self.actionNew.setText(_translate("MainWindow", "Reset", None))
		self.label_gk_rest.setText(_translate("MainWindow", "", None))
		self.label_gk_ag.setText(_translate("MainWindow", "", None))
		self.label_gk_an.setText(_translate("MainWindow", "", None))
		self.label_gk_fa.setText(_translate("MainWindow", "", None))
		self.label_gk_ws.setText(_translate("MainWindow", "", None))
		self.actionExit.setText(_translate("MainWindow", "Exit", None))
		self.actionE.setText(_translate("MainWindow", "Exit", None))
		
	
	############################################################################
	############################################################################
	############### Buttons Check_ALL ######################################
	############################################################################
	############################################################################


	def btn_K5_pressed(self):
		if self.cb_k5_fu.isChecked()==False:
			for all in themen_klasse_5:
				x=eval('self.cb_k5_'+all)
				x.setChecked(True)
		elif self.cb_k5_fu.isChecked()==True:
			for all in themen_klasse_5:
				x=eval('self.cb_k5_'+all)
				x.setChecked(False)

	def btn_K6_pressed(self):
		if self.cb_k6_bsw.isChecked()==False:
			for all in themen_klasse_6:
				x=eval('self.cb_k6_'+all)
				x.setChecked(True)
		elif self.cb_k6_bsw.isChecked()==True:
			for all in themen_klasse_6:
				x=eval('self.cb_k6_'+all)
				x.setChecked(False)

	def btn_K7_pressed(self):
		if self.cb_k7_dr.isChecked()==False:
			for all in themen_klasse_7:
				x=eval('self.cb_k7_'+all)
				x.setChecked(True)
		elif self.cb_k7_dr.isChecked()==True:
			for all in themen_klasse_7:
				x=eval('self.cb_k7_'+all)
				x.setChecked(False)

	def btn_K8_pressed(self):
		if self.cb_k8_ddg.isChecked()==False:
			for all in themen_klasse_8:
				x=eval('self.cb_k8_'+all)
				x.setChecked(True)
		elif self.cb_k8_ddg.isChecked()==True:
			for all in themen_klasse_8:
				x=eval('self.cb_k8_'+all)
				x.setChecked(False)
				
	def btn_ag_all_pressed(self):
		if self.cb_ag11.isChecked()==False:
			for all in ag_kb_beschreibung:
				x=eval('self.cb_'+all)
				x.setChecked(True)
		elif self.cb_ag11.isChecked()==True:
			for all in ag_kb_beschreibung:
				x=eval('self.cb_'+all)
				x.setChecked(False)
				
	def btn_an_all_pressed(self):
		if self.cb_an11.isChecked()==False:
			for all in an_kb_beschreibung:
				x=eval('self.cb_'+all)
				x.setChecked(True)
		elif self.cb_an11.isChecked()==True:
			for all in an_kb_beschreibung:
				x=eval('self.cb_'+all)
				x.setChecked(False)

	def btn_fa_all_pressed(self):
		if self.cb_fa11.isChecked()==False:
			for all in fa_kb_beschreibung:
				x=eval('self.cb_'+all)
				x.setChecked(True)
		elif self.cb_fa11.isChecked()==True:
			for all in fa_kb_beschreibung:
				x=eval('self.cb_'+all)
				x.setChecked(False)	
				
	def btn_ws_all_pressed(self):
		if self.cb_ws11.isChecked()==False:
			for all in ws_kb_beschreibung:
				x=eval('self.cb_'+all)
				x.setChecked(True)
		elif self.cb_ws11.isChecked()==True:
			for all in ws_kb_beschreibung:
				x=eval('self.cb_'+all)
				x.setChecked(False)	
				
	def cb_ag_checked(self):
		set_chosen_gk=set([])
		for all in ag_kb_beschreibung:
			x=eval('self.cb_'+all)
			if x.isChecked()==True:
				set_chosen_gk.add(x.text())

		if len(set_chosen_gk)>7:
			x= ', '.join(list(sorted(set_chosen_gk))[:7])
			x=x+', ...'
		else:
			x= ', '.join(sorted(set_chosen_gk))
		if len(set_chosen_gk)>0:
			x='AG: '+x
		self.label_gk_ag.setText(_translate("MainWindow", str(x), None))

	def cb_an_checked(self):
		set_chosen_gk=set([])
		for all in an_kb_beschreibung:
			x=eval('self.cb_'+all)
			if x.isChecked()==True:
				set_chosen_gk.add(x.text())
		if len(set_chosen_gk)>6:
			x= ', '.join(list(sorted(set_chosen_gk))[:6])
			x=x+', ...'
		else:
			x= ', '.join(sorted(set_chosen_gk))
		if len(set_chosen_gk)>0:
			x='AN: '+x
		self.label_gk_an.setText(_translate("MainWindow", str(x), None))

	def cb_fa_checked(self):
		set_chosen_gk=set([])
		for all in fa_kb_beschreibung:
			x=eval('self.cb_'+all)
			if x.isChecked()==True:
				set_chosen_gk.add(x.text())
		if len(set_chosen_gk)>6:
			x= ', '.join(list(sorted(set_chosen_gk))[:6])
			x=x+', ...'
		else:
			x= ', '.join(sorted(set_chosen_gk))
		if len(set_chosen_gk)>0:
			x='FA: '+x
		self.label_gk_fa.setText(_translate("MainWindow", str(x), None))
		
	def cb_ws_checked(self):
		set_chosen_gk=set([])
		for all in ws_kb_beschreibung:
			x=eval('self.cb_'+all)
			if x.isChecked()==True:
				set_chosen_gk.add(x.text())
		if len(set_chosen_gk)>6:
			x= ', '.join(list(sorted(set_chosen_gk))[:6])
			x=x+', ...'
		else:
			x= ', '.join(sorted(set_chosen_gk))
		if len(set_chosen_gk)>0:
			x='WS: '+x
		self.label_gk_ws.setText(_translate("MainWindow", str(x), None))
	
	def cb_rest_checked(self):
		set_chosen_gk=set([])
		for all in themen_klasse_5:
			x=eval('self.cb_k5_'+all)
			if x.isChecked()==True:
				set_chosen_gk.add(all.upper()+'(5)')
		for all in themen_klasse_6:
			x=eval('self.cb_k6_'+all)
			if x.isChecked()==True:
				set_chosen_gk.add(all.upper() + '(6)')
		for all in themen_klasse_7:
			x=eval('self.cb_k7_'+all)
			if x.isChecked()==True:
				set_chosen_gk.add(all.upper() + '(7)')
		for all in themen_klasse_8:
			x=eval('self.cb_k8_'+all)
			if x.isChecked()==True:
				set_chosen_gk.add(all.upper() + '(8)')		
		if len(set_chosen_gk)>6:
			x= ', '.join(list(sorted(set_chosen_gk))[:6])
			x=x+', ...'
		else:
			x= ', '.join(sorted(set_chosen_gk))
		if len(set_chosen_gk)>0:
			x='Weitere: '+x
		self.label_gk_rest.setText(_translate("MainWindow", str(x), None))

			

	############################################################################
	############################################################################
	######### Button REFRESH DATABASE ######################################
	############################################################################

	def modification_date(self,filename):
		t = os.path.getmtime(filename)
		return datetime.datetime.fromtimestamp(t)	
		
	def refresh_ddb(self):
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
		#print(beispieldaten_dateipfad)
			# print(beispieldaten)

		data_folder=Path('Teildokument')
		log_file=os.path.join(os.path.dirname('__file__'),'Teildokument','log_file')
		
		with open(log_file, 'w+') as f:
			json.dump(beispieldaten_dateipfad, f,ensure_ascii=False)

		self.label_update.setText(_translate("MainWindow", 'Last Update: ' + self.modification_date(log_file).strftime('%d.%m.%y - %H:%M'), None))

		
		
	############################################################################
	############################################################################
	########################### CREATE PDF ####################################		
	############################################################################
	def atoi(self,text):
		return int(text) if text.isdigit() else text	
	
	def natural_keys(self,text):
		return [ self.atoi(c) for c in re.split('(\d+)', text) ]

	def create_pdf(self):
		if sys.platform.startswith('linux'):
			subprocess.Popen('cd Teildokument ; latex --synctex=-1 Teildokument.tex ; dvips Teildokument.dvi ; ps2pdf -dNOSAFER Teildokument.ps',shell=True).wait()
			subprocess.run(['xdg-open', 'Teildokument/Teildokument.pdf'])
		elif sys.platform.startswith('darwin'):
			subprocess.Popen('cd Teildokument ; latex --synctex=-1 Teildokument.tex ; dvips Teildokument.dvi ; ps2pdf -dNOSAFER Teildokument.ps',shell=True).wait()
			subprocess.run(['xdg-open', 'Teildokument/Teildokument.pdf'])
		else:
			subprocess.Popen('cd Teildokument & latex --synctex=-1 Teildokument.tex& dvips Teildokument.dvi & ps2pdf -dNOSAFER Teildokument.ps',shell=True).wait()
			subprocess.Popen('cd Teildokument & Teildokument.pdf', shell=True).poll()
		
		os.unlink('Teildokument/Teildokument.aux')
		os.unlink('Teildokument/Teildokument.log')
		os.unlink('Teildokument/Teildokument.dvi')
		os.unlink('Teildokument/Teildokument.ps')
	
	def PrepareTeXforPDF(self):


		# r=0
		# while r <100:
		# 	Ui_Dialog.progressBar.setValue(r)
		# 	r+=0.0001

		# window=Ui_Dialog()
		# window.show()
		# print('done')
		# return
		if not os.path.isfile(os.path.join('Teildokument','log_file')):
			self.refresh_ddb()
		suchbegriffe = []
		

					
		#### ALGEBRA UND GEOMETRIE
		for all in ag_kb_beschreibung:
			x=eval('self.cb_'+all)
			if x.isChecked()==True:
				suchbegriffe.append(all)
				
		#### ANALYSIS
		for all in an_kb_beschreibung:
			x=eval('self.cb_'+all)
			if x.isChecked()==True:
				suchbegriffe.append(all)
		
		#### FUNKTIONALE ABHÄNGIGKEITEN	
		for all in fa_kb_beschreibung:
			x=eval('self.cb_'+all)
			if x.isChecked()==True:
				suchbegriffe.append(all)		
		#### WAHRSCHEINLICHKEIT UND STATISTIK
		for all in ws_kb_beschreibung:
			x=eval('self.cb_'+all)
			if x.isChecked()==True:
				suchbegriffe.append(all)
				
		temp_suchbegriffe=[]
		for all in suchbegriffe:
			temp_suchbegriffe.append(dict_gk[all])
		suchbegriffe=temp_suchbegriffe

		#### Suche der Schulstufe 
		for y in range(5,9):
			themen_klasse=eval('themen_klasse_%s'%y)
			for all in themen_klasse:
				x=eval('self.cb_k%s_'%y+all)
				grade='K'+str(y)
				if x.isChecked()==True:
					# if grade not in suchbegriffe:
						# suchbegriffe.append('K'+str(y))
					suchbegriffe.append(all.upper())
					
		
		log_file=os.path.join(os.path.dirname('__file__'),'Teildokument','log_file')

		with open(log_file) as f:
			beispieldaten_dateipfad = json.load(f)
			#beispieldaten_dateipfad=eval(beispieldaten_dateipfad)
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
		if self.cb_solution.isChecked()==True:
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
		

		

					
		if self.menu_searchtype.currentText()=='Alle Dateien ausgeben, die alle Suchkriterien enthalten':
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
			
			# for r in range(1,len(liste_kompetenzbereiche)+1):
				# if liste_kompetenzbereiche[r]==[]:
					# del liste_kompetenzbereiche[r]
			for r in range(1,len(liste_kompetenzbereiche)+1):
				for all in suchbegriffe:
					if r in liste_kompetenzbereiche.keys():
						if all not in liste_kompetenzbereiche[r]:
							del liste_kompetenzbereiche[r]


			for key in liste_kompetenzbereiche.keys():
				gesammeltedateien.append(beispieldaten[key-1])
			
				
			# for all in gesammeltedateien[:]:
				# if not len(self.entry_suchbegriffe.text()) ==0:
					# if self.entry_suchbegriffe.text().lower() not in all.lower():
						# gesammeltedateien.remove(all)

					
		if self.menu_searchtype.currentText()=='Alle Dateien ausgeben, die zumindest ein Suchkriterium enthalten':
		
			gesammeltedateien=[]
			for all in suchbegriffe:
				for element in list(beispieldaten_dateipfad.keys())[:]:
					if all in element:
						gesammeltedateien.append(element)
			
		
			gesammeltedateien.sort(key=self.natural_keys)
			


			# if not len(entry_suchbegriffe.get()) ==0:
				# suchbegriffe.append(entry_suchbegriffe.get())
				# for all in list(beispieldaten_dateipfad.keys())[:]:
					# if entry_suchbegriffe.get().lower() in all.lower():
						# if all not in gesammeltedateien:
							# gesammeltedateien.append(all)

		for all in gesammeltedateien[:]:
			if not len(self.entry_suchbegriffe.text()) ==0:
				if self.entry_suchbegriffe.text().lower() not in all.lower():
					gesammeltedateien.remove(all)
		

		dict_gesammeltedateien={}
		for all in gesammeltedateien:
			dict_gesammeltedateien[all]=beispieldaten_dateipfad[all]
	


		

	###############################################	
	#### Auswahl der gesuchten Antwortformate ####
	###############################################
		if self.cb_af_mc.isChecked() or self.cb_af_lt.isChecked() or self.cb_af_zo.isChecked() or self.cb_af_oa.isChecked()==True:
			if suchbegriffe==[]:
				dict_gesammeltedateien=beispieldaten_dateipfad
			for all_formats in set_af:
				x=eval('self.cb_af_'+all_formats)
				if x.isChecked()==False:
					for all in list(dict_gesammeltedateien):
						if all_formats.upper() in all:
							del dict_gesammeltedateien[all]	
							
						# if all_formats in all:
							# del dict_gesammeltedateien[all]
				if x.isChecked()==True:
					suchbegriffe.append(all_formats)


	###############################################	
	#### Auswahl der gesuchten Klassen #########
	###############################################
		selected_klassen=[]
		if self.cb_k5.isChecked() or self.cb_k6.isChecked() or self.cb_k7.isChecked() or self.cb_k8.isChecked()==True:
			if suchbegriffe==[]:
				dict_gesammeltedateien=beispieldaten_dateipfad
			for all_formats in list(Klassen):
				x=eval('self.cb_'+all_formats)
				if x.isChecked()==True:
					selected_klassen.append(all_formats)
					suchbegriffe.append(all_formats.upper())


			for all in list(dict_gesammeltedateien):
				if not any(all_formats.upper() in all for all_formats in selected_klassen):
					del dict_gesammeltedateien[all]

				

		
		##############################
		if not dict_gesammeltedateien:
			msg = QtGui.QMessageBox()
			msg.setIcon(QtGui.QMessageBox.Information)
			msg.setText("Es wurden keine passenden Beispiele gefunden!")
			msg.setInformativeText('Es wird keine Datei ausgegben.')
			msg.setWindowTitle("Information")
			#msg.setDetailedText("The details are as follows:")
			msg.setStandardButtons(QtGui.QMessageBox.Ok)
			retval = msg.exec_()




		beispieldaten.sort(key=self.natural_keys)
		file=open(filename_teildokument,"a", encoding='ISO-8859-1')
		file.write('\n \\scriptsize Suchbegriffe: ')
		for all in suchbegriffe:
			if all == suchbegriffe[-1]:
				file.write(all)
			else:	
				file.write(all + ', ')
		file.write('\\normalsize \n \n')
		#file.close()


		

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

		MainWindow.close()
		self.create_pdf()
		##################################################
		################################################
		###### Windows Loading Bar ######################
		###############################################

		# LoadingWindow = QtGui.QDialog()
		# ui = Ui_Dialog()
		# ui.setupUi(LoadingWindow)
		# LoadingWindow.exec()
		
		sys.exit(0)
		
		# print('done')
		# return	

		# window_loading = Tk()
		# window_loading.title('Lade...')
		# window_loading.geometry('+300+200')
		# def loading_bar():
		# 	def start_loading_bar():
		# 		progress.grid(row=2,column=0)
		# 		progress.start()
		# 		create_pdf()
		# 		progress.stop()
		# 		window_loading.destroy()
		# 	hauptfenster.destroy()
		# 	threading.Thread(target=start_loading_bar).start()
		# if len(dict_gesammeltedateien)==1:
		# 	label_output=Label(window_loading, text='Insgesamt wurde '+ str(len(dict_gesammeltedateien)) + ' Beispiel gefunden.\n', font=LARGE_FONT).grid(row=0,column=0)	
		# else:
		# 	label_output=Label(window_loading, text='Insgesamt wurden '+ str(len(dict_gesammeltedateien)) + ' Beispiele gefunden.\n', font=LARGE_FONT).grid(row=0,column=0)		
		# label_loading = Label(window_loading , text='Lade PDF Datei...', font=LARGE_FONT).grid(row=1,column=0)
		# progress = Progressbar(window_loading , orient=HORIZONTAL,length=250,  mode='indeterminate')
		# loading_bar()
		# window_loading.mainloop()	
		
		# print("Insgesamt wurde(n) " + str(len(dict_gesammeltedateien)) + " Beispiel(e) gefunden. Entsprechende LaTeX-Datei wird ausgegeben...", font=STANDARD_FONT)
		# if sys.platform.startswith('linux'):
		# 	subprocess.run(['xdg-open', filename_teildokument])
		# elif sys.platform.startswith('darwin'):
		# 	subprocess.run(['open', filename_teildokument])
		# else:
		# 	os.system(filename_teildokument)
		# sys.exit(0)
	
if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	MainWindow = QtGui.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())

