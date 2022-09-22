import os
import datetime
from datetime import date
import json
from config_start import path_programm, path_localappdata_lama
from config import is_empty
from standard_dialog_windows import warning_window


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
    weekday = dict_wochentag[
        datetime.datetime(raw_date[0], raw_date[1], raw_date[2]).weekday()
    ]

    datum_kurz = "{0}.{1}.{2}".format(day, month, year)

    datum = "{0}, {1}. {2} {3}".format(weekday, day, month_word, year)

    return datum_kurz, datum


def check_if_hide_all_exists(dict_titlepage):
    try:
        dict_titlepage["hide_all"]
    except KeyError:
        dict_titlepage["hide_all"] = False
        titlepage_save = os.path.join(path_localappdata_lama, "Teildokument", "titlepage_save")
        with open(titlepage_save, "w+", encoding="utf8") as f:
            json.dump(dict_titlepage, f)
    return dict_titlepage


def get_titlepage_vorschau(self, dict_titlepage, ausgabetyp, maximum, gruppe):
    datum_kurz, datum = get_datum(self)
    dict_titlepage = check_if_hide_all_exists(dict_titlepage)

    pkt_typ1 = self.get_punkteverteilung()[1]
    pkt_typ2 = self.get_punkteverteilung()[2]


    if (
        self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
        == "Grundkompetenzcheck"
    ):

        if ausgabetyp == "schularbeit" and maximum > 2:
            gruppe_name = " -- " + self.dict_gruppen[gruppe]
        else:
            gruppe_name = ""

        if is_empty(self.dict_all_infos_for_file["data_gesamt"]["Klasse"]):
            klasse = ""
        else:
            klasse = self.dict_all_infos_for_file["data_gesamt"]["Klasse"]

        if self.dict_all_infos_for_file["data_gesamt"]["#"]==0:
            titlepage = (
                "\\textsc{{Grundkompetenzcheck{0}}}  \\hfill {1} \\hfill \\textsc{{Name:}} \\rule{{5cm}}{{0.4pt}} \\hfill {2}"
                "\\normalsize \\\ \\vspace{{\\baselineskip}} \n\n".format(gruppe_name, klasse, datum_kurz)
            )
        else:
            titlepage = (
                "\\textsc{{{0}. Grundkompetenzcheck{1}}} \\hfill {2} \\hfill \\textsc{{Name:}} \\rule{{5cm}}{{0.4pt}} \\hfill {3}"
                "\\normalsize \\\ \\vspace{{\\baselineskip}} \n\n".format(self.dict_all_infos_for_file["data_gesamt"]["#"], gruppe_name, klasse,datum_kurz)
            )

        return titlepage

    elif self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"] == "Übungsblatt":
        titlepage = "Übungsblatt"
        if self.lineEdit_klasse_sage.text().strip() != "":
            titlepage = titlepage + " -- {}".format(self.lineEdit_klasse_sage.text())

        titlepage = "\\subsection{{{0}}}".format(titlepage)

        return titlepage

    # elif self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"] == "Quiz":
    #     titlepage = (
    #         "\\title{{Typ1 - Quiz}} \n"
    #         "\subtitle{{Anzahl der Aufgaben: {0}}} \n"
    #         "\maketitle \n"
    #         "\subtitle{{}} \n"
    #     ).format(len(self.list_alle_aufgaben_sage))

    #     return titlepage

    elif dict_titlepage["hide_all"] == True:

        if (
            self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
            == "Wiederholungsprüfung"
        ):
            subsection = self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
        else:
            if self.widgetNummer.isEnabled() == False:
                subsection = self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
            else:
                if self.dict_all_infos_for_file["data_gesamt"]["#"]==0:
                    subsection = self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
                else:                    
                    subsection = (
                        str(self.dict_all_infos_for_file["data_gesamt"]["#"])
                        + ". "
                        + self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
                    )

        titlepage = "\\subsection{{{0} \\hfill {1}}}".format(subsection, datum_kurz)

        # if self.dict_all_infos_for_file["data_gesamt"]["Beurteilung"] == "br":

        #     beurteilungsraster = (
        #         "\\beurteilung{{0.875}}{{0.75}}{{0.625}}{{1/2}}{{ % Prozentschluessel\n"
        #         "T1={{{0}}}, % Punkte im Teil 1\n"
        #         "T2={{{1}}}, % Punkte im Teil 2\n"
        #         "}}\n\n".format(pkt_typ1, pkt_typ2)
        #     )

        #     titlepage = titlepage + beurteilungsraster
        return titlepage

    else:
        if dict_titlepage["logo"] == True:
            logo_name = os.path.basename(dict_titlepage["logo_path"])
            logo_titlepage_path = os.path.join(path_localappdata_lama, "Teildokument", logo_name)

            if os.path.isfile(logo_titlepage_path):
                logo_input = (
                    "\\begin{{minipage}}[t]{{0.4\\textwidth}} \\vspace{{0pt}}\n"
                    "\\includegraphics[width=1\\textwidth]{{{0}}}\n"
                    "\\end{{minipage}} \\\ [1cm] \n".format(logo_name)
                )
            else:
                warning_window(
                    "Das Logo konnte nicht gefunden werden.",
                    "Bitte suchen Sie ein Logo unter: \n\nTitelblatt anpassen - Durchsuchen",
                    "Kein Logo gefunden",
                )
                logo_input = "\\null\\vspace{3cm}\n\n"
        else:
            logo_input = "\\null\\vspace{3cm}\n\n"
            # logo_input = "~\\vfil \n"

        if dict_titlepage["titel"] == True:
            if (
                self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
                == "Wiederholungsprüfung"
            ):
                title_header = "\\textsc{{\\Huge Wiederholungsprüfung}} \\\ [0.5cm]"
            elif (
                self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
                == "Schularbeit"
                or self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
                == "Wiederholungsschularbeit"
                or self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
                == "Nachschularbeit"
            ):
                if self.dict_all_infos_for_file["data_gesamt"]["#"]==0:
                    title_header = "\\textsc{{\\Huge Mathematikschularbeit}}"    
                else:    
                    title_header = "\\textsc{{\\Huge {0}. Mathematikschularbeit}}".format(
                        self.dict_all_infos_for_file["data_gesamt"]["#"]
                    )

                if (
                    self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
                    == "Wiederholungsschularbeit"
                ):
                    add_on = "Wiederholung"
                elif (
                    self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
                    == "Nachschularbeit"
                ):
                    add_on = "Nachschularbeit"
                else:
                    add_on = None

                if add_on != None:
                    title_header = (
                        title_header
                        + "\\\ [0.5cm] \\textsc{{\Large {0}}}".format(add_on)
                    )

                title_header = title_header + "\\\ [0.5cm] \n\n"

            else:
                title_header = "\\textsc{{\\Huge {0}}} \\\ [2cm]".format(
                    self.dict_all_infos_for_file["data_gesamt"]["Pruefungstyp"]
                )
        else:
            title_header = ""

        if dict_titlepage["datum"] == True:
            datum_text = "\\textsc{{\Large am {0}}}\\\ [1cm] \n\n".format(datum)
        else:
            datum_text = ""

        if dict_titlepage["klasse"] == True:
            klasse = "\\textsc{{\Large Klasse {0}}} \\\ [1cm] \n\n".format(
                self.dict_all_infos_for_file["data_gesamt"]["Klasse"]
            )
        else:
            klasse = ""

        if ausgabetyp == "schularbeit" and maximum > 2:
            gruppe_name = self.dict_gruppen[gruppe]
            gruppe_name = "\\textsc{{\\Large Gruppe {0}}} \\\ [1cm]\n\n".format(gruppe_name)
        else:
            gruppe_name = ""

        if dict_titlepage["name"] == True:
            name = "\\Large Name: \\rule{8cm}{0.4pt} \\\ [1cm]\n\n"
        else:
            name = ""

        if dict_titlepage["note"] == True:
            note = "\\Large Note: \\rule{8cm}{0.4pt} \\\ [1cm]\n\n"
        else:
            note = "\\vspace{1cm}\n\n"

        if dict_titlepage["unterschrift"] == True:
            unterschrift = "\\Large Unterschrift: \\rule{8cm}{0.4pt} \\\ [1cm]\n\n"
        else:
            unterschrift = "\\vspace{1cm}\n\n"

        if self.dict_all_infos_for_file["data_gesamt"]["Beurteilung"] == "br":
            beurteilungsraster = (
                "\large\\beurteilung{{0.875}}{{0.75}}{{0.625}}{{1/2}}{{ % Prozentschluessel\n"
                "T1={{{0}}}, % Punkte im Teil 1\n"
                "T2={{{1}}}, % Punkte im Teil 2\n"
                "}}\n\n".format(pkt_typ1, pkt_typ2)
            )

        else:
            beurteilungsraster = ""

        titlepage = (
            "\\begin{{titlepage}}\n\n"
            "\\flushright\n"
            "{0}"
            "{1}"
            "{2}"
            "{3}"
            "{4}"
            "{5}"
            "{6}"
            "{7}"
            "\\vspace{{1cm}}\n\n{8}"
            "\\end{{titlepage}}\n\n".format(
                logo_input,
                title_header,
                datum_text,
                klasse,
                gruppe_name,
                name,
                note,
                unterschrift,
                beurteilungsraster,
            )
        )

        return titlepage

