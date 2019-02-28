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
import yaml


hauptfenster = Tk()
hauptfenster.title('LaTeX File Creator')
# hauptfenster.wm_iconbitmap('latex.ico')

hauptfenster.geometry('800x725+10+10')


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


def config_loader(pathToFile):
    config1 = yaml.safe_load(open(pathToFile, encoding='utf8'))

    global dict_aufgabenformat
    global dict_aufgabenformat
    global dict_themen
    global ag_kb
    global AG_BB
    global an_kb
    global AN_BB
    global fa_kb
    global FA_BB
    global ws_kb
    global WS_BB
    global Klassen
    global AF_BB
    global themen_klasse_5
    global themen_klasse_6
    global themen_klasse_7
    global themen_klasse_8
    global Klasse5_BB
    global Klasse6_BB
    global Klasse7_BB
    global Klasse8_BB

    dict_themen = config1['dict_themen']
    ag_kb = config1['ag_kb']
    AG_BB = config1['AG_BB']
    an_kb = config1['an_kb']
    AN_BB = config1['AN_BB']
    fa_kb = config1['fa_kb']
    FA_BB = config1['FA_BB']
    ws_kb = config1['ws_kb']
    WS_BB = config1['WS_BB']
    Klassen = config1['Klassen']
    AF_BB = config1['AF_BB']
    themen_klasse_5 = config1['themen_klasse_5']
    themen_klasse_6 = config1['themen_klasse_6']
    themen_klasse_7 = config1['themen_klasse_7']
    themen_klasse_8 = config1['themen_klasse_8']
    Klasse5_BB = config1['Klasse5_BB']
    Klasse6_BB = config1['Klasse6_BB']
    Klasse7_BB = config1['Klasse7_BB']
    Klasse8_BB = config1['Klasse8_BB']


config_loader('config_creator.yml')




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
	if value=='FA':
		liste_gk = Listbox(frame_gk, width=17, font=("", 7))
	else:
		liste_gk = Listbox(frame_gk,width=14, font=("", 8))
	liste_gk.bind('<<ListboxSelect>>',CurSelect)
	liste_gk.grid(columnspan=2,row=1, sticky=N+S)
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
set_gk_zusatz_info=[]
def add_gk():
	all_items = liste_gk.get(0, END) # tuple with text of all items in Listbox
	sel_idx = liste_gk.curselection() # tuple with indexes of selected items
	sel_list = [all_items[item] for item in sel_idx] # list with text of all selected items
	# print(all_items)
	# print(sel_idx)
	for all in sel_list:
		if all not in set_gk_auswahl and all not in set_gk_zusatz_info:
			liste_gk_auswahl.insert('end', all)
			set_gk_auswahl.append(all)
		
def delete_gk():
	all_items = liste_gk_auswahl.get(0, END) # tuple with text of all items in Listbox
	sel_idx = liste_gk_auswahl.curselection() # tuple with indexes of selected items
	sel_list = [all_items[item] for item in sel_idx] # list with text of all selected items
	# print(sel_list[0])
	try:
		liste_gk_auswahl.delete(sel_idx)
		if sel_list[0] in set_gk_auswahl:
			set_gk_auswahl.remove(sel_list[0])
		if sel_list[0] in set_gk_zusatz_info:
			set_gk_zusatz_info.remove(sel_list[0])
		# print(set_gk_auswahl)
	except TclError:
		pass



def reset_entry():
	global image_path_set, counter_images, dict_button_images, dict_label_images
	selected_gk.set('AG')
	selected_typ.set('Typ 1')
	selected_af.set('bitte auswählen')
	### GK-LISTE zurücksetzen
	liste_gk.delete(0,'end')
	for item in AG_BB:
		liste_gk.insert('end', item)
	##############
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
	for i in range(counter_images):
		dict_button_images[i].destroy()
		dict_label_images[i].destroy()
	counter_images=0
	# picture.destroy()
	# button_cancel.destroy()
	window_height=725
	hauptfenster.geometry("%dx%d" % (800,window_height))
	image_path_set=[]
	dict_button_images={}
	dict_label_images={}

	
def warning_window(warning_text):
	warning =Tk()
	warning.title('Warnung')
	warning.geometry('+150+150')
	def cmd_ok():
		warning.destroy()
	warning_gk_auswahl= Label(warning, text=warning_text, width=50, height=3).grid()
	quit_button = Button(warning, text='OK', command=cmd_ok, width=10).grid(sticky=N, pady=10)		
	
def confirm_save():
######################################################################################
# Typ 1 - Speichern #######################
######################################################################################	
	
	set_gk_auswahl_temp= set_gk_auswahl[:]
	
	textBox_Entry=str(textBox.get("1.0","end-1c"))
	
	if textBox_Entry.count('\includegraphics')>len(image_path_set):
		warning_window('Es sind zu wenige Bilder angehängt! (' + str(len(image_path_set))+'/'+str(textBox_Entry.count('\includegraphics'))+')')
		return
	if textBox_Entry.count('\includegraphics')<len(image_path_set):
		warning_window('Zu viele Bilder angehängt (' + str(len(image_path_set))+'/'+str(textBox_Entry.count('\includegraphics'))+')')
		return
	

	for all in image_path_set:
		head, tail=os.path.split(all)
		x = '{'+tail+'}'
		if x in textBox_Entry:
			textBox_Entry=str(textBox_Entry).replace(tail,"../Bilder/"+tail)
	
	if selected_typ.get()=='Typ 1':
		# print(set_gk_auswahl_temp)
		if len(set_gk_auswahl) > 1:
			for all in set_gk_auswahl: # iterate through copy of list set_gk_auswahl[:]			
				if all in themen_klasse_5 or all in themen_klasse_6 or all in themen_klasse_7 or all in themen_klasse_8:
					# set_gk_auswahl_temp.remove(all)
					if all not in set_gk_zusatz_info:
						set_gk_zusatz_info.append(all)
			

			for all in set_gk_zusatz_info:
				if all in set_gk_auswahl_temp:
					set_gk_auswahl_temp.remove(all)
		
			if not set_gk_auswahl_temp:
				set_gk_auswahl_temp=set_gk_zusatz_info[:]


		if len(set_gk_auswahl_temp)>1:
			warning_window('Es wurden zu viele Grundkompetenzen zugewiesen')
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
				set_gk_auswahl=set_gk_auswahl_temp[:]

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
							# print(x,y)
							file_integer, file_extension=y.split('.tex')
							file_list_integer_temp.append(int(file_integer))				

				if file_list_integer_temp==[]:
					max_integer_file_list=1000
				else:
					max_integer_file_list= max(file_list_integer_temp)

				copy_image_path_typ_1=os.path.join(os.path.dirname('__file__'),'Typ 1 Aufgaben','Bilder')
				for all in image_path_set:
					image_path_temp=all
					head, tail=os.path.split(image_path_temp)
					copy_image_file_typ_1_temp=os.path.join(copy_image_path_typ_1,tail)
					shutil.copy(image_path_temp,copy_image_file_typ_1_temp)
					os.rename(copy_image_file_typ_1_temp,'Typ 1 Aufgaben/Bilder/'+set_gk_auswahl[0][:2]+set_gk_auswahl[0][3]+set_gk_auswahl[0][5]+'_'+str(max_integer_file_list+1)+'_'+tail)
				textBox_Entry=str(textBox.get("1.0","end-1c"))
				for all in image_path_set:
					head, tail=os.path.split(all)
					x = '{'+tail+'}'
					name, ext =os.path.splitext(tail)
					if x in textBox_Entry:
						textBox_Entry=str(textBox_Entry).replace(tail,'{../Bilder/'+set_gk_auswahl[0][:2]+set_gk_auswahl[0][3]+set_gk_auswahl[0][5]+'_'+str(max_integer_file_list+1)+'_'+name+'}'+ext)
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
					if set_gk_auswahl_klasse==[]: ## Klassenauswahl hat Vorrang. Sobald ausgewählt wird diese Klasse eingetragen!
						for all in set_gk_zusatz_info:
							if set_gk_auswahl_klasse==[]:
								if all in themen_klasse_8:
									set_gk_auswahl_klasse.append('K8')
								elif all in themen_klasse_7:
									set_gk_auswahl_klasse.append('K7')
								elif all in themen_klasse_6:
									set_gk_auswahl_klasse.append('K6')
								elif all in themen_klasse_5:
									set_gk_auswahl_klasse.append('K5')
							else:
								if all in themen_klasse_8:
									if 8 > int(re.search(r'\d+', set_gk_auswahl_klasse[0]).group()):
										set_gk_auswahl_klasse[0]='K8'
								elif all in themen_klasse_7:
									if 7 > int(re.search(r'\d+', set_gk_auswahl_klasse[0]).group()):
										set_gk_auswahl_klasse[0]='K7'
								elif all in themen_klasse_6:
									if 6 > int(re.search(r'\d+', set_gk_auswahl_klasse[0]).group()):
										set_gk_auswahl_klasse[0]='K6'
								# elif all in themen_klasse_5:
									# if 5 > int(re.search(r'\d+', set_gk_auswahl_klasse[0]).group()):
										# set_gk_auswahl_klasse[0]='K7'
					
					file_name=os.path.join(os.path.dirname('__file__'),'Typ 1 Aufgaben','_Grundkompetenzen',themen_auswahl,set_gk_auswahl[0],'Einzelbeispiele',set_gk_auswahl[0]+' - '+str(max_integer_file_list+1)+'.tex')
					file=open(file_name,"w")					
					if set_gk_auswahl_klasse==[]:
						if set_gk_zusatz_info==[]:
							file.write("\section{"+set_gk_auswahl[0]+" - "+str(max_integer_file_list+1) +" - "+titel_eingabe.get()+" - "+aufgabenformat_chosen+" - "+quelle_eingabe.get()+"}\n\n"
							"\\begin{beispiel}["+set_gk_auswahl[0]+"]{"+punkte_eingabe.get()+"}\n"+eingabe_beispiel+
							"\n\\end{beispiel}")
						else:

									
							
							set_gk_zusatz_info_joined=', '.join(set_gk_zusatz_info)
							file.write("\section{"+set_gk_auswahl[0]+" - "+str(max_integer_file_list+1) +" - "+ set_gk_auswahl_klasse[0] +" - "+set_gk_zusatz_info_joined+' - '+titel_eingabe.get()+" - "+aufgabenformat_chosen+" - "+quelle_eingabe.get()+"}\n\n"
							"\\begin{beispiel}["+set_gk_auswahl[0]+' - '+set_gk_auswahl_klasse[0]+"]{"+punkte_eingabe.get()+"}\n"+eingabe_beispiel+
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
					global set_gk_auswahl, picture, button_cancel
					global aufgabenformat_chosen
					del aufgabenformat_chosen
					window_finish.destroy()
					reset_entry()

				label_save_1= Label(window_finish, text= 'Das Typ1-Beispiel mit dem Titel', height=2, width=40).grid()
				label_save_2=Label(window_finish, text='"'+titel_eingabe.get()+'"', height=2).grid()
				label_save_3=Label(window_finish, text='wurde gespeichert.', height=2).grid()	
				button_ok = Button (window_finish, text= 'OK', width=10, command=cmd_save_ok).grid()
				window_confirm.destroy()

			
			try:
				aufgabenformat_chosen
			except NameError:
				warning_window('Es wurde kein Aufgabenformat ausgewählt!')

			else:
				if not set_gk_auswahl:
					warning_window('Es wurde keine Grundkompetenz zugewiesen!')
				else: 
					window_confirm =Tk()
					window_confirm.title('Bestätigung')
					window_confirm.geometry('+150+150')
					label_confirm=Label(window_confirm, text='Sind Sie sicher, dass Sie das folgende Beispiel speichern wollen?', height=4, width=60).grid(columnspan=2)
					label_aufgabe_typ=Label(window_confirm, text='Aufgabentyp: '+selected_typ.get(), bg="powderblue").grid(sticky=W,columnspan=2, padx=10)
					label_confirm_titel=Label(window_confirm, text='Titel: '+titel_eingabe.get(), bg="powderblue").grid(sticky=W,columnspan=2, padx=10)
					label_confirm_af=Label(window_confirm, text='Aufgabenformat: '+aufgabenformat_chosen_lang, bg="powderblue").grid(sticky=W,columnspan=2, padx=10)
					label_confirm_gk=Label(window_confirm, text='Grundkompetenz: '+set_gk_auswahl[0], bg="powderblue").grid(sticky=W,columnspan=2, padx=10)
					label_confirm_quelle=Label(window_confirm, text='Quelle: '+quelle_eingabe.get(), bg="powderblue").grid(sticky=W,columnspan=2, padx=10)
					def cancel():
						window_confirm.destroy()
					button_save_file = Button (window_confirm, text='Speichern', command=save_file_typ1).grid(row=6, column=0, sticky=E, pady=10)	
					button_cancel = Button(window_confirm, text='Abbrechen', command=cancel).grid(row=6, column=1, sticky=W, pady=10)
				
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
			for all in image_path_set:
				image_path_temp=all
				head, tail=os.path.split(image_path_temp)
				copy_image_file_typ_2_temp=os.path.join(copy_image_path_typ_2,tail)
				shutil.copy(image_path_temp,copy_image_file_typ_2_temp)

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

			copy_image_path_typ_2=os.path.join(os.path.dirname('__file__'),'Typ 2 Aufgaben','Bilder')
			for all in image_path_set:
				image_path_temp=all
				head, tail=os.path.split(image_path_temp)
				copy_image_file_typ_2_temp=os.path.join(copy_image_path_typ_2,tail)
				shutil.copy(image_path_temp,copy_image_file_typ_2_temp)
				os.rename(copy_image_file_typ_2_temp,'Typ 2 Aufgaben/Bilder/'+str(max_integer_file_list+1)+'_'+tail)
			textBox_Entry=str(textBox.get("1.0","end-1c"))
			for all in image_path_set:
				head, tail=os.path.split(all)
				x = '{'+tail+'}'
				name, ext =os.path.splitext(tail)
				if x in textBox_Entry:
					textBox_Entry=str(textBox_Entry).replace(tail,'{../Bilder/'+str(max_integer_file_list+1)+'_'+name+'}'+ext)
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
				global set_gk_auswahl, picture, button_cancel
				window_finish.destroy()
				reset_entry()

			label_save_1= Label(window_finish, text= 'Das Typ2-Beispiel mit dem Titel', height=2, width=40).grid()
			label_save_2=Label(window_finish, text='"'+titel_eingabe.get()+'"', height=2).grid()
			label_save_3=Label(window_finish, text='wurde gespeichert.', height=2).grid()
			button_ok = Button (window_finish, text= 'OK', width=10, command=cmd_save_ok).grid()
			window_confirm.destroy()
			# print('Das Typ2-Beispiel "'+titel_eingabe.get()+'" wurde gespeichert!')

		if not set_gk_auswahl:
			warning_window('Es wurde keine Grundkompetenz zugewiesen')
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
gk_liste=['AG', 'FA', 'AN', 'WS', '5. Klasse','6. Klasse','7. Klasse','8. Klasse']
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
liste_gk = Listbox(frame_gk, width=14, height=42, font=("", 8)) #, selectmode='multiple', 
liste_gk.bind('<<ListboxSelect>>',CurSelect)
for item in AG_BB:
	liste_gk.insert('end', item)
liste_gk.grid(columnspan=2, row=1, sticky=N+S)



def menu_typ_auswahl(value):
	global aufgabenformat_eingabe, aufgabenformat_inactive
	aufgabenformat_inactive.grid(row=3, column=2, sticky='ew')
	if value=='Typ 1':
		selected_af.set('bitte auswählen')
		aufgabenformat_eingabe=OptionMenu(frame_eingabe, selected_af, *af_liste, command=cmd_aufgabenformat)
		aufgabenformat_eingabe.config(width=1)
		aufgabenformat_eingabe.grid(row=3, column=2, sticky='ew')
		
	if value=='Typ 2':
		aufgabenformat_eingabe.grid_forget()
		aufgabenformat_inactive.config(text='keine Auswahl nötig')
		aufgabenformat_inactive.grid(row=3, column=2, sticky='ew')





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
label_typ = Label(frame_eingabe, text='Aufgabentyp:').grid(row=0, sticky=E)
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
aufgabenformat_inactive=Label(frame_eingabe, text='',height=2, width=7)
aufgabenformat_inactive.grid(row=3, column=2)
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
textBox=ScrolledText.ScrolledText(frame_eingabe, height=24, width=80)
textBox.grid(columnspan=3)
quelle_eingabe_label= Label(frame_eingabe, text='Quelle').grid(sticky=W)
quelle_eingabe=Entry(frame_eingabe, width=107)
quelle_eingabe.grid(sticky=W, columnspan=3)



############## BILDER einfügen ############

global window_height
window_height=725
image_path_set=[]
dict_button_images={}
dict_label_images={}
counter_images=0
def select_image():
	global image_path_set, window_height, var_row,button_cancel, counter_images

	def picture_cancel(*args):
		global window_height
		# print(dict_button_images)
		# print(dict_label_images)
		# print(counter_images_temp)
		dict_button_images[counter_images_temp].destroy()
		dict_label_images[counter_images_temp].destroy()
		# del dict_button_images[counter_images]
		# del dict_label_images[counter_images]

		window_height=window_height-25
		hauptfenster.geometry("%dx%d" % (800,window_height))
		# print(filename)
		image_path_set.remove(filename)
		# print(image_path_set)

		
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
		counter_images_temp=counter_images
		vars()['cancel_button_images_%s'%counter_images_temp]=Button(hauptfenster, text='x', command=lambda: picture_cancel(counter_images), bg='indianred')
		vars()['cancel_button_images_%s'%counter_images_temp].grid(row=var_row, column=2)
		vars()['label_images_%s'%counter_images_temp]=Label(hauptfenster, text=tail)
		vars()['label_images_%s'%counter_images_temp].grid(row=var_row, column=0, columnspan=3, sticky=W)
		
		dict_button_images[counter_images_temp]=vars()['cancel_button_images_%s'%counter_images_temp]
		dict_label_images[counter_images_temp]=vars()['label_images_%s'%counter_images_temp]
		counter_images+=1
	
	


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
