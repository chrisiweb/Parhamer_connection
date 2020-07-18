import os
import datetime
from datetime import date
import json
from config import path_programm

def get_datum(self):
    dict_months = {
        1: "Jänner",
        2: "Februar",
        3: "März",
        4: "April",
        5: "Mai",
        6: "Juni",
        7: "Juli",
        8: "August",
        9: "September",
        10: "Oktober",
        11: "November",
        12: "Dezember",
    }
    dict_wochentag = {
        0: "Montag",
        1: "Dienstag",
        2: "Mittwoch",
        3: "Donnerstag",
        4: "Freitag",
        5: "Samstag",
        6: "Sonntag",
    }

    raw_date = self.dict_all_infos_for_file["data_gesamt"]["Datum"]

    year = raw_date[0]
    month = "{:02d}".format(raw_date[1])
    month_word = dict_months[raw_date[1]]
    day = "{:02d}".format(raw_date[2])
    weekday = dict_wochentag[datetime.datetime(raw_date[0], raw_date[1], raw_date[2]).weekday()]

    datum_kurz = "{0}.{1}.{2}".format(day, month, year)

    datum = "{0}, {1}. {2} {3}".format(weekday, day, month_word, year)

    return datum_kurz, datum


def check_if_hide_all_exists(dict_titlepage):
    try:
        dict_titlepage["hide_all"]
    except KeyError:
        dict_titlepage["hide_all"]=False
        titlepage_save = os.path.join(path_programm, "Teildokument", "titlepage_save")
        with open(titlepage_save, "w+", encoding="utf8") as f:
            json.dump(dict_titlepage, f)
    return dict_titlepage

    

def get_titlepage_vorschau(self, dict_titlepage, ausgabetyp, maximum, index):
    datum_kurz, datum = get_datum(self)
    dict_titlepage = check_if_hide_all_exists(dict_titlepage)

    pkt_gesamt = self.get_punkteverteilung()[0]
    pkt_typ1 = self.get_punkteverteilung()[1]
    pkt_typ2 = self.get_punkteverteilung()[2]
    pkt_ausgleich = self.get_number_ausgleichspunkte_gesamt()



    if self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"] == "Grundkompetenzcheck":        

        if ausgabetyp == "schularbeit" and maximum > 2:
            gruppe = " -- " + self.dict_gruppen[int(index / 2)]
        else:
            gruppe = ""


        titlepage = (
            "\\textsc{{Grundkompetenzcheck{0}}} \\hfill \\textsc{{Name:}} \\rule{{8cm}}{{0.4pt}}"
            "\\normalsize \\\ \\vspace{{\\baselineskip}} \n\n".format(gruppe))
        
        return titlepage


    elif self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"] == "Übungsblatt":
        titlepage = "\\subsection{Übungsblatt}"

        return titlepage         

    elif dict_titlepage["hide_all"] == True:

        if self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"] == "Wiederholungsprüfung":
            subsection = self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
        else:
            if self.groupBox_nummer.isEnabled()==False:
                subsection = self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
            else:    
                subsection = (str(self.dict_all_infos_for_file["data_gesamt"]["#"]) + 
                ". " +
                self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"])
                    

        titlepage = "\\subsection{{{0} \\hfill {1}}}".format(subsection, datum_kurz)

        if self.dict_all_infos_for_file["data_gesamt"]["Beurteilung"] == "br":
            teil2_pkt_ohne_ap = pkt_typ2 - pkt_ausgleich

            beurteilungsraster = (
                "\\flushleft \\normalsize\n"
                "\\thispagestyle{{empty}}\n"
                "\\beurteilungsraster{{0.85}}{{0.68}}{{0.5}}{{1/3}}{{ % Prozentschluessel\n"
                "T1={{{0}}}, % Punkte im Teil 1\n"
                "AP={{{1}}}, % Ausgleichspunkte aus Teil 2\n"
                "T2={{{2}}}, % Punkte im Teil 2\n"
                "}} \n\n"
                "\\newpage\n\n"
                .format(
                pkt_typ2,
                pkt_ausgleich,
                teil2_pkt_ohne_ap,
                ))

            titlepage = titlepage + beurteilungsraster
        return titlepage

    else:
        if dict_titlepage["logo"] == True:
            logo_name = os.path.basename(dict_titlepage["logo_path"])
            logo_titlepage_path = os.path.join(path_programm, "Teildokument", logo_name)

            if os.path.isfile(logo_titlepage_path):
                logo_input = ("\\begin{{minipage}}[t]{{0.4\\textwidth}} \\vspace{{0pt}}\n"
                "\\includegraphics[width=1\\textwidth]{{{0}}}\n"
                "\\end{{minipage}} \\\ \\vfil \n"
                .format(logo_name))
            else:
                warning_window("Das Logo konnte nicht gefunden werden.",
                "Bitte suchen Sie ein Logo unter: \n\nTitelblatt anpassen - Durchsuchen",
                "Kein Logo gefunden"
                )
                logo_input= "~\\vfil \n"
        else:
            logo_input= "~\\vfil \n"        
            # logo_input = "~\\vfil \n"

        if dict_titlepage["titel"] == True:
            if self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"] == "Wiederholungsprüfung":
                title_header = "\\textsc{{\\Huge Wiederholungsprüfung}} \\\ [2cm]"
            elif (
                self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"] == "Schularbeit" or
                self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"] == "Wiederholungsschularbeit" or
                self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"] == "Nachschularbeit"):
                    title_header = "\\textsc{{\\Huge {0}. Mathematikschularbeit}}".format(self.dict_all_infos_for_file["data_gesamt"]["#"])
                    
                    if self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"] == "Wiederholungsschularbeit":
                        add_on = "Wiederholung"
                    elif self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"] == "Nachschularbeit":
                        add_on = "Nachschularbeit"
                    else:
                        add_on = None
                    
                    if add_on != None:
                        title_header = title_header + "\\\ [0.5cm] \\textsc{{\Large {0}}}".format(add_on)
                    
                    title_header = title_header + "\\\ [2cm] \n\n"
                
            else:
                title_header = "\\textsc{{\\Huge {0}}} \\\ [2cm]".format(self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"])    
        else:
            title_header = ''

        if dict_titlepage["datum"] == True:
            datum_text =  "\\textsc{{\Large am {0}}}\\\ [1cm] \n\n".format(datum)
        else:
            datum_text = ''

        if dict_titlepage["klasse"] == True:
            klasse = "\\textsc{{\Large Klasse {0}}} \\\ [1cm] \n\n".format(
                self.dict_all_infos_for_file["data_gesamt"]["Klasse"]
                )
        else:
            klasse = ''

        if ausgabetyp == "schularbeit" and maximum > 2:
            gruppe=self.dict_gruppen[int(index/2)]
            gruppe = "\\textsc{{\\Large Gruppe {0}}} \\\ [1cm]\n\n".format(gruppe)
        else:
            gruppe = ''


        if dict_titlepage["name"] == True:
            name = "\\Large Name: \\rule{8cm}{0.4pt} \\\ \n\n"
        else:
            name = ''
        

        if dict_titlepage["note"] == True:
            note = "\\Large Note: \\rule{8cm}{0.4pt} \\\ [1cm]\n\n"
        else:
            note = ''

        if dict_titlepage["unterschrift"] == True:
            unterschrift = "\\Large Unterschrift: \\rule{8cm}{0.4pt} \\\ \n\n"
        else:
            unterschrift = ''


        if self.dict_all_infos_for_file["data_gesamt"]["Beurteilung"] == "br":
            teil2_pkt_ohne_ap = pkt_typ2 - pkt_ausgleich

            beurteilungsraster = (
                "\\newpage \n\n"
                "\\flushleft \\normalsize\n"
                "\\thispagestyle{{empty}}\n"
                "\\beurteilungsraster{{0.85}}{{0.68}}{{0.5}}{{1/3}}{{ % Prozentschluessel\n"
                "T1={{{0}}}, % Punkte im Teil 1\n"
                "AP={{{1}}}, % Ausgleichspunkte aus Teil 2\n"
                "T2={{{2}}}, % Punkte im Teil 2\n"
                "}} \n\n"
                "\\newpage\n\n"
                .format(
                pkt_typ2,
                pkt_ausgleich,
                teil2_pkt_ohne_ap,
                ))
        else:
            beurteilungsraster = ''
    

        titlepage = (
        "\\begin{{titlepage}}\n\n"
        "\\flushright\n"
        "{0}"
        "{1}"
        "{2}"
        "{3}"
        "{4}"
        "{5}"
        "\\vfil\\vfil\\vfil \n"
        "{6}"
        "{7}"
        "{8}"
        "\\end{{titlepage}}\n\n".format(
        logo_input,
        title_header,
        datum_text,
        klasse,
        gruppe,
        name,
        note,
        unterschrift,
        beurteilungsraster,
        ))

        return titlepage