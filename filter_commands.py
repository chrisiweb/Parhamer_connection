from config import extract_topic_abbr, is_empty
from tinydb import Query
from sort_items import order_gesammeltedateien



def get_filter_string(self, list_mode):
    if self.chosen_program == "cria":
        if list_mode == "sage":
            string_0 = self.comboBox_klassen.currentText()
            string_1 = self.comboBox_kapitel.currentText()
            string_2 = self.comboBox_unterkapitel.currentText()
        elif list_mode == "feedback":
            string_0 = self.comboBox_klassen_fb_cria.currentText()
            string_1 = self.comboBox_kapitel_fb_cria.currentText()
            string_2 = self.comboBox_unterkapitel_fb_cria.currentText()
        filter_string = "k" + string_0[0]

        if not is_empty(string_1):
            filter_string = filter_string + "." + extract_topic_abbr(string_1)
            if not is_empty(string_2):
                filter_string = (
                    filter_string + "." + extract_topic_abbr(string_2)
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
                string_1 = self.comboBox_gk_num.currentText()

        if not is_empty(string_0):
            if string_0 == 'Zusatzthemen':
                filter_string = ""
            else:
                filter_string = string_0
                if not is_empty(string_1):
                    filter_string = filter_string + " " + string_1
            print(filter_string)
            return filter_string
        else:
            return ""

def filter_items(self, table_lama, typ, list_mode, filter_string, line_entry, klasse=None):
    _file_ = Query()
    if typ == "lama_1" or typ == "lama_2":
        def string_included_lama(value):
            print(value)
            
        # string_included_lama = lambda s: (filter_string in s) and (
        #     s.split(" - ")[-1].startswith(line_entry)
        # )
        filtered_items = table_lama.search(_file_.name.test(string_included_lama))
        
    elif typ == "cria":
        if list_mode != "creator":
            klasse = self.get_klasse(list_mode)

        string_included_cria = lambda s: s.split(".")[-1].startswith(line_entry)

        def themen_included_cria(value):
            for all in value:
                return True if filter_string in all else False

        filtered_items = table_lama.search(
            (_file_.name.search("{}\..+".format(klasse)))
            & (_file_.themen.test(themen_included_cria))
            & (_file_.name.test(string_included_cria))
        )

    filtered_items.sort(key=order_gesammeltedateien)

    return filtered_items

