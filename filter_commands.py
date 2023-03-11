import re
from config import extract_topic_abbr, is_empty, zusatzthemen_beschreibung
from tinydb import Query
from sort_items import order_gesammeltedateien
from json.decoder import JSONDecodeError
from standard_dialog_windows import critical_window



def get_filter_string(self, list_mode):
    if self.chosen_program == "cria":
        if list_mode == "sage":
            # string_0 = self.comboBox_klassen.currentText()
            string_1 = self.comboBox_kapitel.currentText()
            string_2 = self.comboBox_unterkapitel.currentText()
        elif list_mode == "feedback":
            # string_0 = self.comboBox_klassen_fb_cria.currentText()
            string_1 = self.comboBox_kapitel_fb_cria.currentText()
            string_2 = self.comboBox_unterkapitel_fb_cria.currentText()
        
        filter_string = ""
        # if not is_empty(string_0):
        #     filter_string = "k" + string_0[0] + "."
        

        if not is_empty(string_1):
            filter_string = extract_topic_abbr(string_1)
            if not is_empty(string_2):
                filter_string = (
                    filter_string + "." +extract_topic_abbr(string_2)
                )

        return filter_string

    if self.chosen_program == "lama":
        if list_mode == "sage":
            # if self.comboBox_gk.currentText() == 'Zusatzthemen':
            #     string_0 = ""
            # else:
            string_0 = self.comboBox_gk.currentText()
            topic = extract_topic_abbr(self.comboBox_gk_num.currentText())

            if topic != None:
                string_1 = topic
            else:
                string_1 = self.comboBox_gk_num.currentText()
        elif list_mode == "feedback":
            string_0 = self.comboBox_fb.currentText()
            topic = extract_topic_abbr(self.comboBox_fb_num.currentText())
            if topic != None:
                string_1 = topic
            else:
                string_1 = self.comboBox_fb_num.currentText()
        
        if not is_empty(string_0):
            if string_0 == 'Zusatzthemen':
                filter_string = "zusatz_"+string_1.upper()
            else:
                filter_string = string_0
                if not is_empty(string_1):
                    filter_string = filter_string + " " + string_1
            return filter_string
        else:
            return ""

def filter_number(value, line_entry):
    if line_entry.startswith('l'):
        number = value.split(" - ")[-1].replace("i.","")
    elif line_entry.startswith('i'):
        number = value.split(" - ")[-1].replace("l.","")
    else:
        number = value.split(" - ")[-1].replace("l.","").replace("i.","")
    
    if number.startswith(line_entry):
        return True
    else:
        return False

def filter_items(self, table_lama, typ, list_mode, filter_string, line_entry, klasse=None):
    _file_ = Query()
    if typ == "lama_1" or typ == "lama_2":
        def string_included_lama(value):
            if "zusatz_" in filter_string:
                string = filter_string.replace("zusatz_","")
                if is_empty(string):
                    for all in zusatzthemen_beschreibung.keys():
                        if value.startswith(all.upper()) and (filter_number(value, line_entry)==True):
                            return True
                    return False    
            else:
                string = filter_string
            if (value.replace("-L","").startswith(string)) and (filter_number(value, line_entry)==True):
                return True
            else:
                return False

        try:     
            filtered_items = table_lama.search(_file_.name.test(string_included_lama))
        except JSONDecodeError:
            critical_window("Es ist ein Fehler bei der Aufgabensuche aufgetreten. Es können daher nicht alle Aufgaben angezeigt werden. Bitte starten Sie die Suche erneut.",
            "Sollte der Fehler weiterhin bestehen, melden Sie sich bitte unter lama.helpme@gmail.com",
            detailed_text=f'JSONDecodeError: File "filter_commands.py" in filter_items\n\nError occured in table:\n{table_lama}')
            
            filtered_items = []
  
    elif typ == "cria":

        # if list_mode != "creator":
        klasse = self.get_klasse(list_mode)
        # print(klasse)


        string_included_cria = lambda s: s.split(".")[-1].startswith(line_entry)

        def themen_included_cria(value):
            for all in value:
                return True if filter_string in all else False


        if klasse == None:
            filtered_items = table_lama.search(
                (_file_.themen.test(themen_included_cria))
                & (_file_.name.test(string_included_cria))
            )
        else:
            filtered_items = table_lama.search(
                (_file_.klasse == klasse)
                & (_file_.themen.test(themen_included_cria))
                & (_file_.name.test(string_included_cria))
            )

    filtered_items.sort(key=lambda text: order_gesammeltedateien(text, typ, cria_plain_number_order=True))
    #print(filter_items)
    return filtered_items

def get_drafts(table_lama):
    _file_ = Query()

    return table_lama.search(_file_.draft == True)
