from PyQt5 import QtCore, QtWidgets, QtGui
from create_new_widgets import (
    add_action,
    create_new_label,
    create_new_label_icon,
    create_new_horizontallayout,
    create_new_verticallayout,
    create_new_gridlayout,
    create_new_combobox,
    create_new_checkbox,
    create_new_button,
    create_new_groupbox,
    create_new_lineedit,
    create_new_spinbox,
    create_new_radiobutton,
    add_new_option,
    add_new_tab,
    DragDropWidget,
    )
from predefined_size_policy import SizePolicy_fixed_height, SizePolicy_fixed, SizePolicy_minimum, SizePolicy_minimum_fixed, SizePolicy_maximum_height, SizePolicy_maximum_width, SizePolicy_minimum_height, SizePolicy_expanding, SizePolicy_maximum
from config import *
from config_start import lama_notenschluessel_file
from json import load
from functools import partial
from create_pdf import prepare_tex_for_pdf
from standard_dialog_windows import warning_window
from worksheet_wizard import dict_themen_wizard
from create_nonograms import all_nonogramms




def setup_MenuBar(self):
    MainWindow = self.MainWindow
    self.menuBar = QtWidgets.QMenuBar(self.MainWindow)
    self.menuBar.setGeometry(QtCore.QRect(0, 0, 950, 21))
    self.menuBar.setObjectName("menuBar")

    self.menuDatei = QtWidgets.QMenu(self.menuBar)
    self.menuDatei.setTitle("Datei")
    self.menuNeu = QtWidgets.QMenu(self.menuBar)
    self.menuNeu.setTitle("Aufgabe")
    self.menuChangeProgram = QtWidgets.QMenu(self.menuDatei)
    self.menuChangeProgram.setTitle("Wechseln zu ...")
    self.menuSage = QtWidgets.QMenu(self.menuBar)
    self.menuSage.setTitle("Prüfung")
    self.menuSuche = QtWidgets.QMenu(self.menuBar)
    self.menuSuche.setTitle("Suche")
    self.menuWizard = QtWidgets.QMenu(self.menuBar)
    self.menuWizard.setTitle("Wizard")
    self.menuFeedback = QtWidgets.QMenu(self.menuBar)
    self.menuFeedback.setTitle("Feedback && Fehler")
    self.menuOptionen = QtWidgets.QMenu(self.menuBar)
    self.menuOptionen.setTitle("Optionen")
    self.menuHelp = QtWidgets.QMenu(self.menuBar)
    self.menuHelp.setTitle("?")
    self.menuUpdate = QtWidgets.QMenu(self.menuHelp)
    self.menuUpdate.setTitle("Update...")
    self.menuDeveloper = QtWidgets.QMenu(self.menuBar)
    self.menuDeveloper.setTitle("Entwicklermodus")

    self.MainWindow.setMenuBar(self.menuBar)

    self.actionRefresh_Database = add_action(
        MainWindow,
        self.menuDatei,
        "Datenbank aktualisieren",
        self.action_refreshddb_selected,
    )
    self.actionRefresh_Database.setShortcut("F5")

    # self.menuDatei.addSeparator()

    self.actionPush_Database = add_action(
        MainWindow,
        self.menuDeveloper,
        "Datenbank hochladen",
        self.push_full_database,
    )

    self.actionPush_Database = add_action(
        MainWindow,
        self.menuDeveloper,
        "Entwürfe prüfen",
        self.draft_control,
    )

    self.actionPush_Database = add_action(
        MainWindow,
        self.menuDeveloper,
        "Fehlerbericht erstellen",
        self.database_clean_up,
    )

    self.menuDatei.addSeparator()

    self.actionBild_convert_image_eps = add_action(
        MainWindow,
        self.menuDatei,
        "Grafik zu eps-Datei konvertieren",
        self.convert_image_eps_clicked,
    )

    self.menuDatei.addSeparator()

    self.action_cria = add_action(
            MainWindow,
            self.menuChangeProgram,
            "Unterstufe",
            partial(self.change_program, "cria"), #
        )

    self.action_lama = add_action(
            MainWindow,
            self.menuChangeProgram,
            "Oberstufe",
            partial(self.change_program, "lama"), #
        )

    self.action_wizard = add_action(
            MainWindow,
            self.menuChangeProgram,
            "Worksheet Wizard",
            partial(self.change_program, "wizard"), #
        )

    self.menuDatei.addAction(self.menuChangeProgram.menuAction())
    self.actionExit = add_action(MainWindow, self.menuDatei, "Exit", self.exit_pressed)


    self.actionSuche = add_action(
        MainWindow,
        self.menuSuche,
        "Aufgaben suchen...",
        partial(self.update_gui, "widgets_search"),
    )
    # self.actionSuche.setVisible(False)
    self.actionSuche.setEnabled(False)
    self.actionSuche.setShortcut("F1")

    self.menuSuche.addSeparator()

    self.actionReset_wizard = add_action(
        MainWindow, self.menuWizard, "Reset", self.worksheet_wizard_reset
    )

    self.actionReset = add_action(
        MainWindow, self.menuSuche, "Reset", self.suchfenster_reset
    )
    self.actionReset.setShortcut("F4")

    self.actionSage = add_action(
        MainWindow,
        self.menuSage,
        "Prüfung erstellen...",
        partial(self.update_gui, "widgets_sage"),
    )
    self.actionSage.setShortcut("F2")

    self.menuSage.addSeparator()

    self.actionSave = add_action(
        MainWindow, self.menuSage, "Prüfung speichern", self.sage_save
    )
    self.actionSave.setEnabled(False)
    self.actionSave.setShortcut("Ctrl+S")

    self.actionLoad = add_action(
        MainWindow, self.menuSage, "Prüfung laden", self.sage_load
    )
    # self.actionLoad.setEnabled(False)
    self.actionLoad.setShortcut("Ctrl+O")

    self.menuSage.addSeparator()

    self.actionRestore_sage = add_action(
        MainWindow, self.menuSage, "", partial(self.sage_load, autosave=True)
    )


    self.actionReset_sage = add_action(
        MainWindow, self.menuSage, "Reset Prüfung", partial(self.reset_sage, True)
    )
    self.actionReset_sage.setEnabled(False)
    # self.actionReset_sage.setVisible(False)

    self.actionNeu = add_action(
        MainWindow,
        self.menuNeu,
        "Neue Aufgabe zur Datenbank hinzufügen...",
        self.action_add_file,
    )
    self.actionNeu.setShortcut("F3")


    if self.developer_mode_active == True:
        label_action_edit = "Aufgabe bearbeiten"
    else:
        label_action_edit = "Lokal gespeicherte Aufgabe bearbeiten"
    self.actionEdit_Files = add_action(
        MainWindow, self.menuNeu, label_action_edit, self.action_edit_files
    )
    # self.actionBild_einbinden = add_action(
    #     MainWindow, self.menuBild_einbinden, "Durchsuchen...", self.btn_add_image_pressed
    # )

    self.actionFeedback = add_action(
        MainWindow,
        self.menuFeedback,
        "Feedback oder Fehler senden...",
        partial(self.update_gui, "widgets_feedback"),
    )

    self.actionEinstellungen = add_action(
        MainWindow, self.menuOptionen, "LaMA konfigurieren ...", self.open_setup
    )

    self.actionUpdate_srdpmathematik = add_action(
        MainWindow,
        self.menuUpdate,
        '"srdp-mathematik.sty" aktualisieren',
        self.update_style_package,
    )

    # self.actionUpdate_tabu = add_action(
    #     MainWindow,
    #     self.menuUpdate,
    #     '"tabu.sty" aktualisieren',
    #     partial(self.update_style_package, "tabu.sty"),
    # )

    self.menuOptionen.addAction(self.menuUpdate.menuAction())

    self.actionGKcatalogue = add_action(MainWindow, self.menuHelp, "Grundkompetenzkatalog anzeigen", self.show_gk_catalogue)

    self.actionShowPopupWindow = add_action(
        MainWindow, self.menuHelp, "Letzes Infofenster anzeigen", partial(self.show_popup_window, False)
    )


    self.actionInfo = add_action(
        MainWindow, self.menuHelp, "Über LaMA", self.show_info
    )
    self.actionSupport = add_action(
        MainWindow, self.menuHelp, "LaMA unterstützen", self.show_support
    )



    if self.developer_mode_active == True:
        label = "Entwicklermodus (aktiv)"
    else:
        label = "Entwicklermodus"

    self.actionDeveloper = add_action(
        MainWindow, self.menuOptionen, label, self.activate_developermode
    )

    # self.menuOptionen.addSeparator()

    # self.actionComplete_reset = add_action(MainWindow, self.menuOptionen, "LaMA vollständig zurücksetzen", self.complete_reset)

    self.menuBar.addAction(self.menuDatei.menuAction())
    self.menuBar.addAction(self.menuSuche.menuAction())
    # self.menuBar.addAction(self.menuDateityp.menuAction())
    self.menuBar.addAction(self.menuSage.menuAction())
    self.menuBar.addAction(self.menuNeu.menuAction())
    self.menuBar.addAction(self.menuFeedback.menuAction())
    self.menuBar.addAction(self.menuOptionen.menuAction())

    if self.developer_mode_active == True:
        self.menuBar.addAction(self.menuDeveloper.menuAction())

    self.menuBar.addAction(self.menuHelp.menuAction())

def setup_stackSearch(self):
    self.gridLayout_stackSearch = create_new_gridlayout(self.stackSearch)

    self.widget_headMenu = QtWidgets.QWidget(self.stackSearch)
    self.widget_headMenu.setObjectName("widget_headMenu")
    self.horizontalLayout_headMenu = create_new_horizontallayout(self.widget_headMenu)
    self.horizontalLayout_headMenu.setContentsMargins(0,0,0,0)

    self.label_aufgabentyp = create_new_label(self.widget_headMenu, "")
    self.label_aufgabentyp.setPixmap(QtGui.QPixmap(get_icon_path("database.svg")))
    # self.label_lamaLogo.setFixedHeight(30)
    self.label_aufgabentyp.setFixedSize(QtCore.QSize(30,30))
    self.label_aufgabentyp.setScaledContents(True)
    
    # self.gridLayout.addLayout(self.horizontalLayout_headMenu, 0, 0, 1, 2)
    self.combobox_aufgabentyp = create_new_combobox(self.widget_headMenu)
    # self.combobox_aufgabentyp.setSizePolicy(SizePolicy_fixed)
    add_new_option(self.combobox_aufgabentyp, 0, "Typ1")
    add_new_option(self.combobox_aufgabentyp, 1, "Typ2")
    self.combobox_aufgabentyp.currentIndexChanged.connect(
        self.chosen_aufgabenformat_typ
    )
    
    self.horizontalLayout_headMenu.addWidget(self.label_aufgabentyp)
    self.horizontalLayout_headMenu.addWidget(self.combobox_aufgabentyp)


    self.combobox_searchtype = create_new_combobox(self.widget_headMenu, "combobox_searchtype")
    # self.combobox_searchtype.setMinimumContentsLength(1)

    # self.horizontalLayout_combobox = create_new_horizontallayout()
    add_new_option(
        self.combobox_searchtype,
        0,
        "Alle Dateien ausgeben, die zumindest ein Themengebiet enthalten",
    )

    label = None
    if self.chosen_program == "lama":
        label = "Alle Dateien ausgeben, die ausschließlich diese Themengebiete enthalten"
    elif self.chosen_program == "cria":
        label = "Alle Dateien ausgeben, die alle Themengebiete enthalten"
        

    add_new_option(self.combobox_searchtype, 1, label)
    # self.combobox_searchtype.setSizePolicy(SizePolicy_minimum_width)
    self.horizontalLayout_headMenu.addWidget(self.combobox_searchtype)

    # self.gridLayout.addLayout(self.horizontalLayout_combobox, 0, 1, 1, 1)

    self.combobox_searchtype.hide()
    self.horizontalLayout_headMenu.addStretch()

    self.gridLayout_stackSearch.addWidget(self.widget_headMenu, 0,0,1,2)

    self.frame_tab_widget_gk = QtWidgets.QFrame(self.stackSearch)
    self.frame_tab_widget_gk.setObjectName("frame_tab_widget_gk")
    self.verticalLayout_frame_gk = create_new_verticallayout(self.frame_tab_widget_gk)
    # # self.verticalLayout_frame_gk.setContentsMargins(1,1,1,1)

    self.tab_widget_gk = QtWidgets.QTabWidget(self.frame_tab_widget_gk)


    self.tab_widget_gk.setObjectName("tab_widget_gk")
    self.verticalLayout_frame_gk.addWidget(self.tab_widget_gk)
    self.gridLayout_stackSearch.addWidget(self.frame_tab_widget_gk, 1, 0, 1, 1)

    # #### AG #####
    self.create_tab_checkboxes_gk(
        self.tab_widget_gk, "Algebra und Geometrie", ag_beschreibung, "search"
    )

    ### FA ###
    self.create_tab_checkboxes_gk(
        self.tab_widget_gk, "Funktionale Abhängigkeiten", fa_beschreibung, "search"
    )

    ### AN ###
    self.create_tab_checkboxes_gk(
        self.tab_widget_gk, "Analysis", an_beschreibung, "search"
    )

    ### WS ###
    self.create_tab_checkboxes_gk(
        self.tab_widget_gk,
        "Wahrscheinlichkeit und Statistik",
        ws_beschreibung,
        "search",
    )

    ######### Klassenthemen
    self.create_tab_checkboxes_themen(self.tab_widget_gk, "search")

    # self.gridLayout_stackSearch.addWidget(self.widget_headMenu, 0,0,1,2)



    # self.frame_tab_widget_gk = QtWidgets.QFrame(self.stackSearch)
    # self.frame_tab_widget_gk.setObjectName("frame_tab_widget_gk")
    # self.verticalLayout_frame_gk = create_new_verticallayout(self.frame_tab_widget_gk)
    # # self.verticalLayout_frame_gk.setContentsMargins(1,1,1,1)

    # self.tab_widget_gk = QtWidgets.QTabWidget(self.frame_tab_widget_gk)

    # self.tab_widget_gk.setObjectName("tab_widget_gk")
    # self.verticalLayout_frame_gk.addWidget(self.tab_widget_gk)
    # self.gridLayout_stackSearch.addWidget(self.frame_tab_widget_gk, 1, 0, 1, 1)

    # # #### AG #####
    # self.create_tab_checkboxes_gk(
    #     self.tab_widget_gk, "Algebra und Geometrie", ag_beschreibung, "search"
    # )

    # ### FA ###
    # self.create_tab_checkboxes_gk(
    #     self.tab_widget_gk, "Funktionale Abhängigkeiten", fa_beschreibung, "search"
    # )

    # ### AN ###
    # self.create_tab_checkboxes_gk(
    #     self.tab_widget_gk, "Analysis", an_beschreibung, "search"
    # )

    # ### WS ###
    # self.create_tab_checkboxes_gk(
    #     self.tab_widget_gk,
    #     "Wahrscheinlichkeit und Statistik",
    #     ws_beschreibung,
    #     "search",
    # )

    # ######### Klassenthemen
    # self.create_tab_checkboxes_themen(self.tab_widget_gk, "search")





    # ##################################################################
    # ################ LAMA CRIA SEARCH #################################
    # ###################################################################


    self.tab_widget_search_cria = QtWidgets.QTabWidget(self.frame_tab_widget_gk)

    self.tab_widget_search_cria.setObjectName("tab_widget_search_cria")
    self.tab_widget_search_cria.setFocusPolicy(QtCore.Qt.NoFocus)
    self.verticalLayout_frame_gk.addWidget(self.tab_widget_search_cria)
    self.tab_widget_search_cria.hide()


    for klasse in list_klassen:
        new_tab = add_new_tab(
            self.tab_widget_search_cria, "{}. Klasse".format(klasse[1])
        )

        new_gridlayout = QtWidgets.QGridLayout(new_tab)
        new_gridlayout.setObjectName("{}".format(new_gridlayout))

        new_scrollarea = QtWidgets.QScrollArea(new_tab)
        new_scrollarea.setObjectName("{}".format(new_scrollarea))
        new_scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
        new_scrollarea.setFocusPolicy(QtCore.Qt.NoFocus)
        new_scrollarea.setWidgetResizable(True)

        new_scrollareacontent = QtWidgets.QWidget()

        new_scrollareacontent.setObjectName("{}".format(new_scrollareacontent))

        new_verticallayout = QtWidgets.QVBoxLayout(new_scrollareacontent)
        new_verticallayout.setObjectName("{}".format(new_verticallayout))

        combobox_kapitel = create_new_combobox(new_scrollareacontent)

        self.dict_widget_variables[
            "combobox_kapitel_search_cria_{}".format(klasse)
        ] = combobox_kapitel
        dict_klasse_name = eval("dict_{}_name".format(klasse))
        index = 0
        for kapitel in dict_klasse_name:
            add_new_option(
                combobox_kapitel,
                index,
                dict_klasse_name[kapitel] + " (" + kapitel + ")",
            )
            index += 1
        combobox_kapitel.currentIndexChanged.connect(
            partial(
                self.comboBox_kapitel_changed_cr,
                new_scrollareacontent,
                new_verticallayout,
                klasse,
                'search',
            )
        )

        new_verticallayout.addWidget(combobox_kapitel)

        dict_klasse_name = eval("dict_{}_name".format(klasse))
        kapitel = list(dict_klasse_name.keys())[0]
        dict_klasse = eval("dict_{}".format(klasse))

        for unterkapitel in dict_klasse[kapitel]:
            new_checkbox = create_new_checkbox(
                new_scrollareacontent,
                dict_unterkapitel[unterkapitel] + " (" + unterkapitel + ")"
            )
            new_checkbox.setToolTip(dict_unterkapitel[unterkapitel])

            self.dict_widget_variables[
                "checkbox_unterkapitel_{0}_{1}_{2}".format(
                    klasse, kapitel, unterkapitel
                )
            ] = new_checkbox
            new_checkbox.stateChanged.connect(
                partial(
                    self.checkBox_checked_cria,
                    klasse,
                    kapitel,
                    unterkapitel))


            new_verticallayout.addWidget(new_checkbox)
            new_checkbox.setFocusPolicy(QtCore.Qt.NoFocus)

        

        new_verticallayout.addStretch()

        btn_alle_unterkapitel = create_new_button(
            new_scrollareacontent,
            "alle Unterkapitel auswählen",
            partial(self.btn_alle_unterkapitel_clicked_cria, klasse)
        )
        self.dict_widget_variables[f"btn_alle_unterkapitel_{klasse}"] = btn_alle_unterkapitel
        new_verticallayout.addWidget(btn_alle_unterkapitel)

        btn_alle_kapitel = create_new_button(
            new_scrollareacontent,
            "alle Kapitel der {}. Klasse auswählen".format(klasse[1]),
            partial(self.btn_alle_kapitel_clicked_cria, klasse),
        )
        self.dict_widget_variables[f"btn_alle_kapitel_{klasse}"] = btn_alle_kapitel

        new_verticallayout.addWidget(btn_alle_kapitel)

        new_scrollarea.setWidget(new_scrollareacontent)

        new_gridlayout.addWidget(new_scrollarea, 5, 0, 1, 1)




    self.groupBox_ausgew_gk = create_new_groupbox(
        self.stackSearch, "Auswahl"
    )
  
    self.groupBox_ausgew_gk.setMaximumHeight(115)

    self.verticalLayout_2 = create_new_verticallayout(self.groupBox_ausgew_gk)

    # QtWidgets.QVBoxLayout(self.groupBox_ausgew_gk)
    # self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))

    self.scrollArea_ausgew_gk = QtWidgets.QScrollArea(self.groupBox_ausgew_gk)
    self.scrollArea_ausgew_gk.setWidgetResizable(True)
    self.scrollArea_ausgew_gk.setObjectName("scrollArea_ausgew_gk")
    self.scrollAreaWidgetContents_ausgew_gk = QtWidgets.QWidget()
    self.scrollAreaWidgetContents_ausgew_gk.setObjectName(
        "scrollAreaWidgetContents_ausgew_gk"
    )

    self.verticalLayout_scrollA_ausgew_gk = create_new_verticallayout(
        self.scrollAreaWidgetContents_ausgew_gk
    )
    self.verticalLayout_scrollA_ausgew_gk.setContentsMargins(0,0,0,0)


    # self.horizontalLayout_ausgew_gk.addWidget(self.groupBox_ausgew_gk)
    self.gridLayout_stackSearch.addWidget(self.groupBox_ausgew_gk, 2, 0, 1, 1)


    self.widget_searchMenu = QtWidgets.QWidget(self.stackSearch)
    self.widget_searchMenu.setObjectName("widget_searchMenu")
    self.widget_searchMenu.setMinimumWidth(1)
    # self.widget_searchMenu.setContentsMargins(0,0,0,0)
    self.gridLayout_stackSearch.addWidget(self.widget_searchMenu, 1 , 1,2,1)

    self.verticalLayout_searchMenu = create_new_verticallayout(self.widget_searchMenu)
    self.verticalLayout_searchMenu.setContentsMargins(0,0,0,0)

    self.groupBox_af = QtWidgets.QGroupBox(self.widget_searchMenu)
    self.groupBox_af.setSizePolicy(SizePolicy_fixed_height)
    self.groupBox_af.setTitle("Aufgabenformate")
    self.groupBox_af.setObjectName("groupBox_af")
    # self.groupBox_af.setMaximumHeight(80)
    self.gridLayout_af = QtWidgets.QGridLayout(self.groupBox_af)
    self.gridLayout_af.setObjectName("gridLayout_af")
    self.gridLayout_af.setContentsMargins(0,15,5,10)

    self.cb_af_mc = QtWidgets.QCheckBox(self.groupBox_af)
    self.cb_af_mc.setObjectName("cb_af_mc")
    self.cb_af_mc.setText("Multiplechoice")
    self.gridLayout_af.addWidget(self.cb_af_mc, 0, 0, 1, 1)
        
    self.cb_af_zo = QtWidgets.QCheckBox(self.groupBox_af)        
    self.cb_af_zo.setObjectName("cb_af_zo")
    self.cb_af_zo.setText("Zuordnungsformat")
    self.gridLayout_af.addWidget(self.cb_af_zo, 1, 0, 1, 1)

    self.cb_af_lt = QtWidgets.QCheckBox(self.groupBox_af)
    self.cb_af_lt.setObjectName("cb_af_lt")
    self.cb_af_lt.setText("Lückentext")
    self.gridLayout_af.addWidget(self.cb_af_lt, 2, 0, 1, 1)        
    
    self.cb_af_oa = QtWidgets.QCheckBox(self.groupBox_af)
    self.cb_af_oa.setObjectName("cb_af_oa")
    self.cb_af_oa.setText("Offenes Format")
    self.gridLayout_af.addWidget(self.cb_af_oa, 3, 0, 1, 1)


    self.cb_af_ta = QtWidgets.QCheckBox(self.groupBox_af)
    self.cb_af_ta.setObjectName("cb_af_ta")
    self.cb_af_ta.setText("Textaufgaben")
    self.gridLayout_af.addWidget(self.cb_af_ta, 0, 1, 1, 1)

    self.cb_af_rf = QtWidgets.QCheckBox(self.groupBox_af)
    self.cb_af_rf.setObjectName("cb_af_rf")
    self.cb_af_rf.setText("Richtig/Falsch-Format")
    self.gridLayout_af.addWidget(self.cb_af_rf, 1, 1, 1, 1)

    self.cb_af_ko = QtWidgets.QCheckBox(self.groupBox_af)
    self.cb_af_ko.setObjectName("cb_af_ko")
    self.cb_af_ko.setText("Konstruktion")
    self.gridLayout_af.addWidget(self.cb_af_ko, 2, 1, 1, 1)

    self.gridLayout_af.setRowStretch(4,1)

    if self.chosen_program != "cria":
        self.cb_af_ko.hide()
        self.cb_af_rf.hide()
        self.cb_af_ta.hide()


    self.verticalLayout_searchMenu.addWidget(self.groupBox_af)


    self.groupBox_klassen = create_new_groupbox(
        self.widget_searchMenu, "Suchfilter"
    )
    self.groupBox_klassen.setSizePolicy(SizePolicy_fixed_height)
    self.gridLayout_14 = create_new_gridlayout(self.groupBox_klassen)

    self.cb_k5 = create_new_checkbox(self.groupBox_klassen, "5. Klasse")
    self.gridLayout_14.addWidget(self.cb_k5, 0, 0, 1, 1)

    self.cb_k6 = create_new_checkbox(self.groupBox_klassen, "6. Klasse")
    self.gridLayout_14.addWidget(self.cb_k6, 1, 0, 1, 1)

    self.cb_k7 = create_new_checkbox(self.groupBox_klassen, "7. Klasse")
    self.gridLayout_14.addWidget(self.cb_k7, 2, 0, 1, 1)

    self.cb_k8 = create_new_checkbox(self.groupBox_klassen, "8. Klasse")
    self.gridLayout_14.addWidget(self.cb_k8, 3, 0, 1, 1)

    self.cb_mat = create_new_checkbox(self.groupBox_klassen, "Matura")
    self.gridLayout_14.addWidget(self.cb_mat, 4, 0, 1, 1)

    self.cb_univie = create_new_checkbox(self.groupBox_klassen, "Uni Wien")
    self.cb_univie.setToolTip(
        "Aufgaben mit dieser Kennzeichnung wurden im Rahmen einer Lehrveranstaltung auf der\nUniverstität Wien von Studierenden erstellt und von den Lehrveranstaltungsleitern evaluiert."
    )
    self.gridLayout_14.addWidget(self.cb_univie, 1, 2, 1, 1)
    self.gridLayout_14.setContentsMargins(0,10,0,10)
    self.cb_univie.hide()

    self.verticalLayout_searchMenu.addWidget(self.groupBox_klassen)
    # self.gridLayout.addWidget(self.groupBox_klassen, 2, 1, 1, 1)


    self.label_ausgew_gk = create_new_label(self.scrollArea_ausgew_gk, "", True)
    self.verticalLayout_scrollA_ausgew_gk.addWidget(self.label_ausgew_gk)

    self.label_ausgew_gk_rest = create_new_label(self.scrollArea_ausgew_gk, "")

    self.verticalLayout_scrollA_ausgew_gk.addWidget(self.label_ausgew_gk_rest)
    self.label_ausgew_gk_rest.hide()
    self.scrollArea_ausgew_gk.setFrameShape(QtWidgets.QFrame.NoFrame)
    self.scrollArea_ausgew_gk.setWidget(self.scrollAreaWidgetContents_ausgew_gk)
    self.verticalLayout_2.addWidget(self.scrollArea_ausgew_gk)


    self.frame_advanced_search = QtWidgets.QFrame(self.stackSearch)
    self.frame_advanced_search.setObjectName("frame_advanced_search")

    self.frame_advanced_search.setSizePolicy(SizePolicy_fixed_height)

    self.horizontalLayout_advanced_search = create_new_horizontallayout(self.frame_advanced_search)
    # self.gridLayout_10 = create_new_gridlayout(self.groupBox_advanced_search)

    # self.comboBox_suchbegriffe = create_new_combobox(self.frame_advanced_search)
    # self.gridLayout_10.addWidget(self.comboBox_suchbegriffe, 0, 0, 1, 1)
    self.iconlabel_search = create_new_label(self.frame_advanced_search, "")
    self.iconlabel_search.setPixmap(QtGui.QPixmap(get_icon_path("search.svg")))
    self.iconlabel_search.setFixedSize(QtCore.QSize(22,22))
    self.iconlabel_search.setScaledContents(True)
    self.horizontalLayout_advanced_search.addWidget(self.iconlabel_search)
    self.horizontalLayout_advanced_search.setContentsMargins(0,0,0,0)


    self.entry_suchbegriffe = create_new_lineedit(self.frame_advanced_search, ObjectName="entry_suchbegriffe")
    self.horizontalLayout_advanced_search.addWidget(self.entry_suchbegriffe)

    self.filter_search = QtWidgets.QPushButton(self.frame_advanced_search)
    self.filter_search.setObjectName("filter_search")
    self.filter_search.setIcon(QtGui.QIcon(get_icon_path('filter.svg')))
    filterMenu = QtWidgets.QMenu(self.frame_advanced_search)
    # ag = QtGui.QActionGroup(self.filter_search, exclusive=False)

    action_titel = QtWidgets.QAction("Titel", filterMenu)
    filterMenu.addAction(action_titel)
    action_titel.setCheckable(True)
    action_titel.setChecked(True)

    action_inhalt = QtWidgets.QAction("Inhalt", filterMenu)
    filterMenu.addAction(action_inhalt)
    action_inhalt.setCheckable(True)
    action_inhalt.setChecked(True)

    action_quelle = QtWidgets.QAction("Quelle", filterMenu)
    filterMenu.addAction(action_quelle)
    action_quelle.setCheckable(True)
    action_quelle.setChecked(True)

    action_bilder = QtWidgets.QAction("Bilder", filterMenu)
    filterMenu.addAction(action_bilder)
    action_bilder.setCheckable(True)
    action_bilder.setChecked(True)

    action_id = QtWidgets.QAction("Aufgaben-ID", filterMenu)
    filterMenu.addAction(action_id)
    action_id.setCheckable(True)
    action_id.setChecked(True)
    # action_inhalt = filterMenu.addAction(QtWidgets.QAction("Inhalt", filterMenu, checkable=True))
    # action_titel.setChecked(True)
    # action_inhalt.setChecked(True)
    # filterMenu.addAction(QtWidgets.QAction("Quelle", filterMenu, checkable=True))
    # filterMenu.addAction(QtWidgets.QAction("Bilder", filterMenu, checkable=True))
    # filterMenu.addAction(QtWidgets.QAction("Aufgaben-ID", filterMenu, checkable=True))
    self.set_filters = {"Titel", "Inhalt", "Quelle", "Bilder", "Aufgaben-ID"}
    def filterMenu_opened(action):
        if action.isChecked():
            self.set_filters.add(action.text())
        else:
            self.set_filters.remove(action.text())
            if len(self.set_filters)==0:
                warning_window("Es muss mindestens ein Suchkriterium ausgewählt werden.")
                self.set_filters.add(action.text())
                action.setChecked(True)
        filterMenu.show()


    filterMenu.triggered.connect(filterMenu_opened)
    self.filter_search.setMenu(filterMenu)
    self.horizontalLayout_advanced_search.addWidget(self.filter_search)
    # self.entry_suchbegriffe.setEnabled(False)

    self.verticalLayout_searchMenu.addWidget(self.frame_advanced_search)

    self.verticalLayout_searchMenu.addStretch()

    self.groupBox_pdf_output = create_new_groupbox(self.stackSearch, "PDF Anzeige")
    self.groupBox_pdf_output.setSizePolicy(SizePolicy_fixed_height)
    # self.gridLayout.addWidget(self.groupBox_pdf_output, 4,1,2,1, QtCore.Qt.AlignTop)

    self.verticalLayout_pdf_output = create_new_verticallayout(self.groupBox_pdf_output)
    self.verticalLayout_pdf_output.setContentsMargins(0,10,2,10)


    self.cb_solution = create_new_checkbox(self.groupBox_pdf_output, "Lösungen", True)
    self.verticalLayout_pdf_output.addWidget(self.cb_solution)
    # self.horizontalLayout_2.addWidget(self.cb_solution)
    self.cb_solution.setToolTip(
        "Die gesuchten Aufgaben werden inklusive der Lösungen angezeigt."
    )

    self.cb_infos = create_new_checkbox(self.groupBox_pdf_output, "Aufgabeninfos")
    self.verticalLayout_pdf_output.addWidget(self.cb_infos)


    self.cb_show_variation = create_new_checkbox(
        self.groupBox_pdf_output, "Aufgabenvariationen"
    )
    self.verticalLayout_pdf_output.addWidget(self.cb_show_variation)
    self.cb_show_variation.setToolTip(
        "Es werden alle Aufgabenvariationen angezeigt."
    )

    self.cb_drafts = create_new_checkbox(self.groupBox_pdf_output, "Entwürfe")
    self.verticalLayout_pdf_output.addWidget(self.cb_drafts)
    self.cb_drafts.setToolTip(
        "Es werden auch eingereichte Aufgaben durchsucht, die bisher noch nicht auf Fehler überprüft\nund in die Datenbank aufgenommen wurden."
    )
    self.cb_drafts.toggled.connect(self.cb_drafts_enabled)


    self.widget_translation = QtWidgets.QWidget(self.groupBox_pdf_output)
    

    self.horizontalLayout_translation = create_new_horizontallayout(self.widget_translation)
    self.horizontalLayout_translation.setContentsMargins(10,0,0,0)

    self.label_translation = create_new_label(self.widget_translation, "")
    self.label_translation.setPixmap(QtGui.QPixmap(get_icon_path("globe.svg")))
    self.label_translation.setFixedSize(QtCore.QSize(20,20))
    self.label_translation.setScaledContents(True)
    self.horizontalLayout_translation.addWidget(self.label_translation)


    self.combobox_translation = create_new_combobox(self.widget_translation)
    add_new_option(self.combobox_translation, 0, "Deutsch")
    add_new_option(self.combobox_translation, 1, "Deutsch & Englisch")
    add_new_option(self.combobox_translation, 2, "Englisch")

    self.combobox_translation.currentIndexChanged.connect(lambda: self.combobox_translation_changed())

    self.horizontalLayout_translation.addWidget(self.combobox_translation)
    self.widget_translation.setToolTip("Alle Aufgaben in Deutsch anzeigen")

    self.horizontalLayout_translation.addStretch()

    self.verticalLayout_pdf_output.addWidget(self.widget_translation)

    self.verticalLayout_searchMenu.addWidget(self.groupBox_pdf_output)


    # self.verticalLayout_searchMenu.addStretch()
    # self.gridLayout.addWidget(self.cb_show_variaton,5, 1,1,1)

    self.btn_suche = create_new_button(
        self.stackSearch, "Suche starten", partial(prepare_tex_for_pdf, self)
    )
    self.btn_suche.setIcon(QtGui.QIcon(get_icon_path('search.svg')))
    self.btn_suche.setShortcut("Return")

    
    self.gridLayout_stackSearch.addWidget(self.btn_suche, 3, 1, 1, 1, QtCore.Qt.AlignRight)

def setup_stackSage(self):
    self.gridLayout_stackSage = create_new_gridlayout(self.stackSage)
    self.splitter_sage = QtWidgets.QSplitter(self.stackSage)
    self.splitter_sage.setOrientation(QtCore.Qt.Horizontal)
    self.splitter_sage.setObjectName("splitter_sage")
    # self.splitter_sage.splitterMoved.connect(self.splitter_sage_moved)

    self.groupBox_alle_aufgaben = QtWidgets.QGroupBox(self.splitter_sage)
    self.groupBox_alle_aufgaben.setMinimumWidth(1)
    self.groupBox_alle_aufgaben.setObjectName("groupBox_alle_aufgaben")

    self.verticalLayout_sage = QtWidgets.QVBoxLayout(self.groupBox_alle_aufgaben)
    self.verticalLayout_sage.setObjectName("verticalLayout_sage")

    self.comboBox_at_sage = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
    self.comboBox_at_sage.setObjectName("comboBox_at_sage")
    self.comboBox_at_sage.addItem("")
    self.comboBox_at_sage.addItem("")
    self.verticalLayout_sage.addWidget(self.comboBox_at_sage)
    self.comboBox_at_sage.setItemText(0, "Typ 1")
    self.comboBox_at_sage.setItemText(1, "Typ 2")
    self.comboBox_at_sage.currentIndexChanged.connect(self.comboBox_at_sage_changed)
    self.comboBox_at_sage.setFocusPolicy(QtCore.Qt.ClickFocus)

    self.comboBox_gk = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
    self.comboBox_gk.setObjectName("comboBox_gk")
    list_comboBox_gk = ["", "AG", "FA", "AN", "WS", "Zusatzthemen"]
    index = 0
    for all in list_comboBox_gk:
        self.comboBox_gk.addItem("")
        self.comboBox_gk.setItemText(index, all)
        index += 1
    self.comboBox_gk.currentIndexChanged.connect(
        partial(self.comboBox_gk_changed, "sage")
    )
    self.comboBox_gk.setFocusPolicy(QtCore.Qt.ClickFocus)
    self.verticalLayout_sage.addWidget(self.comboBox_gk)
    self.comboBox_gk_num = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
    self.comboBox_gk_num.setObjectName("comboBox_gk_num")
    self.comboBox_gk_num.currentIndexChanged.connect(
        partial(self.comboBox_gk_num_changed, "sage")
    )
    self.comboBox_gk_num.setFocusPolicy(QtCore.Qt.ClickFocus)
    self.verticalLayout_sage.addWidget(self.comboBox_gk_num)


    self.lineEdit_number = QtWidgets.QLineEdit(self.groupBox_alle_aufgaben)
    self.lineEdit_number.setObjectName("lineEdit_number")
    self.lineEdit_number.textChanged.connect(
        partial(self.lineEdit_number_changed, "sage")
    )
    
    self.listWidget = QtWidgets.QListWidget(self.groupBox_alle_aufgaben)
    self.listWidget.setObjectName("listWidget")
    self.listWidget.itemClicked.connect(self.nummer_clicked)
  

    ##### Sage ComboBoxes LaMA Cria ####
    self.comboBox_klassen = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
    self.comboBox_klassen.setObjectName("comboBox_klassen")

    self.comboBox_klassen.addItem("Alle Klassen")
    index = 1
    for all in list_klassen:
        add_new_option(self.comboBox_klassen, index, all[1] + ". Klasse")
        index += 1

    self.comboBox_klassen.currentIndexChanged.connect(
        partial(self.comboBox_klassen_changed, "sage")
    )

    self.comboBox_klassen.setFocusPolicy(QtCore.Qt.ClickFocus)
    self.verticalLayout_sage.addWidget(self.comboBox_klassen)

    self.comboBox_kapitel = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
    self.comboBox_kapitel.setObjectName("comboBox_kapitel")

    self.comboBox_kapitel.setFocusPolicy(QtCore.Qt.ClickFocus)
    self.verticalLayout_sage.addWidget(self.comboBox_kapitel)

    self.comboBox_unterkapitel = QtWidgets.QComboBox(self.groupBox_alle_aufgaben)
    self.comboBox_unterkapitel.setObjectName("comboBox_unterkapitel")

    self.comboBox_unterkapitel.setFocusPolicy(QtCore.Qt.ClickFocus)
    self.verticalLayout_sage.addWidget(self.comboBox_unterkapitel)
    

    self.comboBox_kapitel.currentIndexChanged.connect(
        partial(self.comboBox_kapitel_changed, "sage")
    )

    self.comboBox_unterkapitel.currentIndexChanged.connect(
        partial(self.comboBox_unterkapitel_changed, "sage")
    )


    self.buttonImport_sage = create_new_button(self.stackSage, "Aufgabenliste hinzufügen",self.buttonImport_sage_clicked, icon= "upload.svg")
    
    ####################
    self.verticalLayout_sage.addWidget(self.lineEdit_number)
    self.verticalLayout_sage.addWidget(self.listWidget)
    self.verticalLayout_sage.addWidget(self.buttonImport_sage)

    self.groupBox_sage = QtWidgets.QGroupBox(self.splitter_sage)
    self.groupBox_sage.setMinimumWidth(1)
    self.groupBox_sage.setObjectName("groupBox_sage")
    self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_sage)
    self.gridLayout_5.setObjectName("gridLayout_5")



    self.widget_SageMenu2 = QtWidgets.QWidget(self.groupBox_sage)
    self.widget_SageMenu2.setSizePolicy(SizePolicy_fixed)
    self.gridLayout_5.addWidget(self.widget_SageMenu2, 0,1,1,1)
    self.verticalLayout_SageMenu2 = create_new_verticallayout(self.widget_SageMenu2)
    self.verticalLayout_SageMenu2.setContentsMargins(0,0,0,0)
    self.comboBox_pruefungstyp = QtWidgets.QComboBox(self.groupBox_sage)
    # self.comboBox_pruefungstyp.setMinimumContentsLength(1)
    self.comboBox_pruefungstyp.setObjectName("comboBox_pruefungstyp")
    list_comboBox_pruefungstyp = [
        "Schularbeit",
        "Nachschularbeit",
        "Wiederholungsschularbeit",
        "Wiederholungsprüfung",
        "Grundkompetenzcheck",
        "Übungsblatt",
    ]
    # self.comboBox_pruefungstyp.setEditable(True)

    # if self.chosen_program == "lama":
    #     list_comboBox_pruefungstyp.append("Quiz")

    list_comboBox_pruefungstyp.append("Benutzerdefiniert")

    index = 0
    for all in list_comboBox_pruefungstyp:
        self.comboBox_pruefungstyp.addItem("")
        self.comboBox_pruefungstyp.setItemText(
            index, all
        )
        index += 1
    self.comboBox_pruefungstyp.setFocusPolicy(QtCore.Qt.ClickFocus)
    # self.comboBox_pruefungstyp.setMinimumContentsLength()
    self.verticalLayout_SageMenu2.addWidget(self.comboBox_pruefungstyp)
    # self.gridLayout_5.addWidget(self.comboBox_pruefungstyp, 0, 1, 1, 1)
    self.comboBox_pruefungstyp.currentIndexChanged.connect(
        self.comboBox_pruefungstyp_changed
    )
    # self.verticalLayout_sage.addWidget(self.comboBox_pruefungstyp)

    self.combobox_beurteilung = create_new_combobox(self.groupBox_sage)
    add_new_option(self.combobox_beurteilung, 0, "Notenschlüssel")

    add_new_option(self.combobox_beurteilung, 1, "Beurteilungsraster")

    add_new_option(self.combobox_beurteilung, 2, "keine Auswahl")

    if self.chosen_program == "cria":
        self.combobox_beurteilung.removeItem(self.combobox_beurteilung.findText("Beurteilungsraster"))

    try:
        if self.dict_titlepage['hide_all'] == True:
            self.combobox_beurteilung.model().item(1).setEnabled(False)
            self.combobox_beurteilung.model().item(1).setForeground(QtGui.QColor('gray'))
            self.combobox_beurteilung.setItemText(1, "Beurteilungsraster (Titelblatt deaktiviert)")
            # self.combobox_beurteilung.removeItem(self.combobox_beurteilung.findText("Beurteilungsraster"))
    except KeyError:
        pass

    self.combobox_beurteilung.currentIndexChanged.connect(self.notenanzeige_changed)
    # self.combobox_beurteilung.setMinimumContentsLength(1)
    self.verticalLayout_SageMenu2.addWidget(self.combobox_beurteilung)

    self.pushButton_titlepage = QtWidgets.QPushButton(self.groupBox_sage)
    self.pushButton_titlepage.setObjectName("pushButton_titlepage")
    self.pushButton_titlepage.setText("Titelblatt")
    self.pushButton_titlepage.setIcon(QtGui.QIcon(get_icon_path('edit.svg')))
    self.pushButton_titlepage.clicked.connect(lambda: self.define_titlepage())
    self.verticalLayout_SageMenu2.addWidget(self.pushButton_titlepage)


    self.widget_SageMenu = QtWidgets.QWidget(self.groupBox_sage)
    self.gridLayout_5.addWidget(self.widget_SageMenu, 0,0,1,1)
    self.gridLayout_SageMenu = create_new_gridlayout(self.widget_SageMenu)
    self.gridLayout_SageMenu.setContentsMargins(0,0,0,0)


    self.widgetNummer = QtWidgets.QWidget(self.widget_SageMenu)
    self.widgetNummer.setObjectName("widgetNummer")
    


    self.horizontalLayout_widgetNummer = create_new_horizontallayout(self.widgetNummer)
    self.horizontalLayout_widgetNummer.setContentsMargins(0,0,0,0)

    self.labelNummer = create_new_label(self.widgetNummer,"")
    self.labelNummer.setPixmap(QtGui.QPixmap(get_icon_path("hash.svg")))
    # self.label_lamaLogo.setFixedHeight(30)
    self.labelNummer.setFixedSize(QtCore.QSize(15,15))
    self.labelNummer.setScaledContents(True)
    self.horizontalLayout_widgetNummer.addWidget(self.labelNummer)

    self.spinBox_nummer = QtWidgets.QSpinBox(self.widgetNummer)
    self.spinBox_nummer.setValue(1)
    self.spinBox_nummer_setvalue = 1
    self.spinBox_nummer.setObjectName("spinBox_nummer")
    self.spinBox_nummer.setToolTip("0 = keine Nummerierung")
    self.spinBox_nummer.valueChanged.connect(self.spinBox_nummer_changed)

    self.horizontalLayout_widgetNummer.addWidget(self.spinBox_nummer)
    self.gridLayout_SageMenu.addWidget(self.widgetNummer, 0,0,1,1, QtCore.Qt.AlignLeft)


    self.widget_datum = QtWidgets.QWidget(self.widget_SageMenu)
    self.widget_datum.setObjectName("widget_datum")
    self.horizontalLayout_frameDatum = create_new_horizontallayout(self.widget_datum)
    self.horizontalLayout_frameDatum.setContentsMargins(0,0,0,0)

    self.checkBox_date = create_new_checkbox(self.widget_datum, " ", checked = True)
    self.checkBox_date.setStyleSheet(f"""
            QCheckBox {{
                spacing: -5px;
                padding-top: 2px;
            }}

            QCheckBox::indicator:unchecked {{ 
                image: url({get_icon_path("square.svg")});
                width: 35px;
            }}

            QCheckBox::indicator:checked {{ 
                image: url({get_icon_path("check-square.svg")});
                width: 35px;
            }}""")
    self.horizontalLayout_frameDatum.addWidget(self.checkBox_date)
    self.checkBox_date.hide()


    self.labelDate = create_new_label(self.widget_datum,"")
    self.labelDate.setPixmap(QtGui.QPixmap(get_icon_path("calendar.svg")))
    # self.label_lamaLogo.setFixedHeight(30)
    self.labelDate.setFixedSize(QtCore.QSize(15,15))
    self.labelDate.setScaledContents(True)
    self.horizontalLayout_frameDatum.addWidget(self.labelDate)

    
    self.dateEdit = QtWidgets.QDateEdit(self.widget_datum)
    self.dateEdit.setCalendarPopup(True)
    self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
    self.dateEdit.setObjectName("dateEdit")
    self.horizontalLayout_frameDatum.addWidget(self.dateEdit)

    self.checkBox_date.stateChanged.connect(lambda: self.checkbox_enable_disable_widget(self.checkBox_date, self.dateEdit))


    self.gridLayout_SageMenu.addWidget(self.widget_datum, 1,0,1,1, QtCore.Qt.AlignLeft)


    self.widgetName = QtWidgets.QWidget(self.widget_SageMenu)
    if self.chosen_program == 'lama' and self.dict_titlepage['hide_all'] == False:
        self.widgetName.hide()
    elif self.chosen_program == 'cria' and self.dict_titlepage_cria['hide_all'] == False:
        self.widgetName.hide()
        
    self.horizontalLayout_widgetName = create_new_horizontallayout(self.widgetName)
    self.horizontalLayout_widgetName.setContentsMargins(0,0,0,0)

    self.checkBoxName = create_new_checkbox(self.widgetName, " ", checked = True)
    self.checkBoxName.setStyleSheet(f"""
            QCheckBox {{
                spacing: -5px;
                padding-top: 2px;
            }}

            QCheckBox::indicator:unchecked {{ 
                image: url({get_icon_path("square.svg")});
                width: 35px;
            }}

            QCheckBox::indicator:checked {{ 
                image: url({get_icon_path("check-square.svg")});
                width: 35px;
            }}""")
    self.horizontalLayout_widgetName.addWidget(self.checkBoxName)


    self.labelName = create_new_label(self.widgetName,"")
    self.labelName.setToolTip("Namensfeld anzeigen")
    self.labelName.setPixmap(QtGui.QPixmap(get_icon_path("pen-tool.svg")))
    self.labelName.setFixedSize(QtCore.QSize(15,15))
    self.labelName.setScaledContents(True)
    self.horizontalLayout_widgetName.addWidget(self.labelName)    


    self.pushButtonName = create_new_button(self.widgetName, "", self.pushButtonName_clicked, icon="align-left.svg")
    self.pushButtonName_current_index = 0
    self.horizontalLayout_widgetName.addWidget(self.pushButtonName)
    

    self.checkBoxName.stateChanged.connect(lambda: self.checkbox_enable_disable_widget(self.checkBoxName, self.labelName))
    self.checkBoxName.stateChanged.connect(lambda: self.checkbox_enable_disable_widget(self.checkBoxName, self.pushButtonName))

    self.gridLayout_SageMenu.addWidget(self.widgetName, 2,0,1,1, QtCore.Qt.AlignLeft)

    self.groupBox_klasse_sage = QtWidgets.QGroupBox(self.widget_SageMenu)
    self.groupBox_klasse_sage.setObjectName("groupBox_klasse_sage")
    self.groupBox_klasse_sage.setTitle("Klasse")
    self.groupBox_klasse_sage.setMaximumWidth(80)
    self.verticalLayout_4 = create_new_verticallayout(self.groupBox_klasse_sage)
    self.verticalLayout_4.setContentsMargins(0,5,0,0)
    self.lineEdit_klasse_sage = QtWidgets.QLineEdit(self.groupBox_klasse_sage)
    self.lineEdit_klasse_sage.setObjectName("lineEdit_klasse_sage")
    self.verticalLayout_4.addWidget(self.lineEdit_klasse_sage)
    self.gridLayout_SageMenu.addWidget(self.groupBox_klasse_sage,0,1,2,1)



    self.groupBox_default_pkt = QtWidgets.QGroupBox(self.widget_SageMenu)
    self.groupBox_default_pkt.setObjectName("groupBox_default_pkt")
    self.groupBox_default_pkt.setTitle("Typ1 Standard")
    self.groupBox_default_pkt.setMaximumWidth(80)
    # self.groupBox_default_pkt.setMaximumSize(QtCore.QSize(120, 16777215))
    self.verticalLayout_default_pkt = QtWidgets.QVBoxLayout(
        self.groupBox_default_pkt
    )
    self.verticalLayout_default_pkt.setContentsMargins(0,5,0,0)
    self.verticalLayout_default_pkt.setObjectName("verticalLayout_default_pkt")
    self.spinBox_default_pkt = SpinBox_noWheel(self.groupBox_default_pkt)
    # self.spinBox_default_pkt.setSizePolicy(SizePolicy_minimum_fixed)
    self.spinBox_default_pkt.setValue(1)
    self.spinBox_default_pkt.setToolTip("0 = Punkte ausblenden")
    self.spinBox_default_pkt.setObjectName("spinBox_default_pkt")
    self.verticalLayout_default_pkt.addWidget(self.spinBox_default_pkt)
    self.spinBox_default_pkt.valueChanged.connect(self.update_default_pkt)
    self.gridLayout_SageMenu.addWidget(self.groupBox_default_pkt,0,2,2,1)

    self.gridLayout_SageMenu.setColumnStretch(3,1)

    self.scrollArea_chosen = QtWidgets.QScrollArea(self.groupBox_sage)
    self.scrollArea_chosen.setFrameShape(QtWidgets.QFrame.StyledPanel)
    self.scrollArea_chosen.setWidgetResizable(True)
    self.scrollArea_chosen.setObjectName("scrollArea_chosen")
    self.scrollArea_chosen.setFocusPolicy(QtCore.Qt.ClickFocus)
    self.widgetscrollArea_sage = QtWidgets.QWidget(self.groupBox_sage)
    self.scrollArea_chosen.setWidget(self.widgetscrollArea_sage)
    self.verticalLayout_widgetscrollArea_sage = create_new_verticallayout(self.widgetscrollArea_sage)

    self.scrollAreaWidgetContents_typ1 = DragDropWidget(self, 1)
    self.scrollAreaWidgetContents_typ1.setObjectName("scrollAreaWidgetContents_typ1")
    self.scrollAreaWidgetContents_typ1.setFocusPolicy(QtCore.Qt.ClickFocus)
    self.verticalLayout_scrollArea_sage_typ1 = create_new_verticallayout(self.scrollAreaWidgetContents_typ1)
    self.verticalLayout_scrollArea_sage_typ1.addStretch()
    self.verticalLayout_scrollArea_sage_typ1.setContentsMargins(0,0,0,0)
    # self.gridLayout_8 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
    # self.gridLayout_8.setObjectName("gridLayout_8")
    self.verticalLayout_widgetscrollArea_sage.addWidget(self.scrollAreaWidgetContents_typ1)
    # self.scrollArea_chosen.setWidget(self.scrollAreaWidgetContents_2)
#

    self.scrollAreaWidgetContents_typ2 = DragDropWidget(self, 2)
    self.scrollAreaWidgetContents_typ2.hide()
    self.scrollAreaWidgetContents_typ2.setObjectName("scrollAreaWidgetContents_3")
    self.scrollAreaWidgetContents_typ2.setFocusPolicy(QtCore.Qt.ClickFocus)
    self.verticalLayout_scrollArea_sage_typ2 = create_new_verticallayout(self.scrollAreaWidgetContents_typ2)
    self.verticalLayout_scrollArea_sage_typ2.addStretch(0)
    self.verticalLayout_scrollArea_sage_typ2.setContentsMargins(0,0,0,0)
    # self.gridLayout_8 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
    # self.gridLayout_8.setObjectName("gridLayout_8")
    self.verticalLayout_widgetscrollArea_sage.addWidget(self.scrollAreaWidgetContents_typ2)
    # self.scrollArea_chosen.setWidget(self.scrollAreaWidgetContents_2)


    self.scrollArea_chosen.verticalScrollBar().rangeChanged.connect(
        self.change_scrollbar_position
    )

    self.gridLayout_5.addWidget(self.scrollArea_chosen, 1, 0, 1, 2)


    self.groupBox_notenschl = create_new_groupbox(
        self.groupBox_sage, "Notenschlüssel"
    )
    # QtWidgets.QGroupBox(self.groupBox_sage)
    # self.groupBox_notenschl.setObjectName("groupBox_notenschl")
    self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_notenschl)
    self.gridLayout_6.setObjectName("gridLayout_6")

    try:
        if self.chosen_program == 'cria':
            key = "prozente_cria"
        else:
            key = "prozente"

        sehr_gut = self.lama_settings[key][0]
        gut = self.lama_settings[key][1]
        befriedigend = self.lama_settings[key][2]
        genuegend = self.lama_settings[key][3]
    except KeyError:
        sehr_gut = 91
        gut = 80
        befriedigend = 64
        genuegend = 50

    self.combobox_notenschluessel_typ = create_new_combobox(self.groupBox_notenschl)
    add_new_option(self.combobox_notenschluessel_typ, 0, "Standard")
    add_new_option(self.combobox_notenschluessel_typ, 1, "Individuell")
    self.gridLayout_6.addWidget(self.combobox_notenschluessel_typ, 0,0,1,1)
    self.combobox_notenschluessel_typ.currentIndexChanged.connect(self.notenschluessel_changed)

    self.combobox_notenschluessel_saved = create_new_combobox(self.groupBox_notenschl)
    self.gridLayout_6.addWidget(self.combobox_notenschluessel_saved, 0,1,1,4)
    
    try:
        with open(lama_notenschluessel_file, "r", encoding="utf8") as f:
            dict_notenschluessel = load(f)
    except FileNotFoundError:
        dict_notenschluessel = {}

    add_new_option(self.combobox_notenschluessel_saved, 0, "")

    index = 1
    for all in dict_notenschluessel.keys():
        add_new_option(self.combobox_notenschluessel_saved, index, all)
        index +=1 
    
    self.combobox_notenschluessel_saved.hide()

    self.label_sg = create_new_label(self.groupBox_notenschl, "Sehr Gut:")
    self.label_sg.setSizePolicy(SizePolicy_fixed)
    self.gridLayout_6.addWidget(self.label_sg, 1, 0, 1, 1)
    self.spinBox_2 = create_new_spinbox(self.groupBox_notenschl, sehr_gut)
    self.spinBox_2.setSizePolicy(SizePolicy_fixed)
    self.spinBox_2.valueChanged.connect(self.update_punkte)
    self.gridLayout_6.addWidget(self.spinBox_2, 1, 1, 1, 1)
    self.label_sg_pkt = create_new_label(self.groupBox_notenschl, "% (ab 0)")
    self.gridLayout_6.addWidget(self.label_sg_pkt, 1, 2, 1, 1)

    regexp = QtCore.QRegExp("[0-9,;/\.]*")
    validator = QtGui.QRegExpValidator(regexp)

    # QRegExp, QRegExpValidator, .setValidator, 
    # https://social.msdn.microsoft.com/forums/en-US/a1e87254-b6c2-491c-b18b-e092611b5f9d/regular-expression-for-comma-separated-numbers?forum=aspgettingstarted

    self.lineedit_sg_upper_limit = create_new_lineedit(self.groupBox_notenschl)
    self.gridLayout_6.addWidget(self.lineedit_sg_upper_limit, 1, 1, 1, 1)
    self.lineedit_sg_upper_limit.setEnabled(False)
    self.lineedit_sg_upper_limit.setStyleSheet("background-color: lightGray")
    self.lineedit_sg_upper_limit.hide()
    self.lineedit_sg_lower_limit = create_new_lineedit(self.groupBox_notenschl)
    self.gridLayout_6.addWidget(self.lineedit_sg_lower_limit, 1, 3, 1, 1)
    self.lineedit_sg_lower_limit.setValidator(validator)
    self.lineedit_sg_lower_limit.hide()

    self.label_g = create_new_label(self.groupBox_notenschl, "Gut:")
    self.label_g.setSizePolicy(SizePolicy_fixed)
    self.gridLayout_6.addWidget(self.label_g, 1, 4, 1, 1)
    self.spinBox_3 = create_new_spinbox(self.groupBox_notenschl, gut)
    self.spinBox_3.setSizePolicy(SizePolicy_fixed)
    self.spinBox_3.valueChanged.connect(self.update_punkte)
    self.gridLayout_6.addWidget(self.spinBox_3, 1, 5, 1, 1)
    self.label_g_pkt = create_new_label(self.groupBox_notenschl, "% (ab 0)")
    self.gridLayout_6.addWidget(self.label_g_pkt, 1, 6, 1, 1)

    self.lineedit_g_upper_limit = create_new_lineedit(self.groupBox_notenschl)
    self.gridLayout_6.addWidget(self.lineedit_g_upper_limit, 1, 5, 1, 1)
    self.lineedit_g_upper_limit.setValidator(validator)
    self.lineedit_g_upper_limit.hide()
    self.lineedit_g_lower_limit = create_new_lineedit(self.groupBox_notenschl)
    self.gridLayout_6.addWidget(self.lineedit_g_lower_limit, 1, 7, 1, 1)
    self.lineedit_g_lower_limit.setValidator(validator)
    self.lineedit_g_lower_limit.hide()


    self.label_b = create_new_label(self.groupBox_notenschl, "Befriedigend:")
    self.label_b.setSizePolicy(SizePolicy_fixed)
    self.gridLayout_6.addWidget(self.label_b, 2, 0, 1, 1)
    self.spinBox_4 = create_new_spinbox(self.groupBox_notenschl, befriedigend)
    self.spinBox_4.setSizePolicy(SizePolicy_fixed)
    self.spinBox_4.valueChanged.connect(self.update_punkte)
    self.gridLayout_6.addWidget(self.spinBox_4, 2, 1, 1, 1)
    self.label_b_pkt = create_new_label(self.groupBox_notenschl, "% (ab 0)")
    self.gridLayout_6.addWidget(self.label_b_pkt, 2, 2, 1, 1)

    self.lineedit_b_upper_limit = create_new_lineedit(self.groupBox_notenschl)
    self.gridLayout_6.addWidget(self.lineedit_b_upper_limit, 2, 1, 1, 1)
    self.lineedit_b_upper_limit.setValidator(validator)
    self.lineedit_b_upper_limit.hide()
    self.lineedit_b_lower_limit = create_new_lineedit(self.groupBox_notenschl)
    self.gridLayout_6.addWidget(self.lineedit_b_lower_limit, 2, 3, 1, 1)
    self.lineedit_b_lower_limit.setValidator(validator)
    self.lineedit_b_lower_limit.hide()


    self.label_g_2 = create_new_label(self.groupBox_notenschl, "Genügend:")
    self.label_g_2.setSizePolicy(SizePolicy_fixed)
    self.gridLayout_6.addWidget(self.label_g_2, 2, 4, 1, 1)
    self.spinBox_5 = create_new_spinbox(self.groupBox_notenschl, genuegend)
    self.spinBox_5.setSizePolicy(SizePolicy_fixed)
    self.spinBox_5.valueChanged.connect(self.update_punkte)
    self.gridLayout_6.addWidget(self.spinBox_5, 2, 5, 1, 1)
    self.label_g_2_pkt = create_new_label(self.groupBox_notenschl, "% (ab 0)")
    self.gridLayout_6.addWidget(self.label_g_2_pkt, 2, 6, 1, 1)


    self.lineedit_g2_upper_limit = create_new_lineedit(self.groupBox_notenschl)
    self.gridLayout_6.addWidget(self.lineedit_g2_upper_limit, 2, 5, 1, 1)
    self.lineedit_g2_upper_limit.setValidator(validator)
    self.lineedit_g2_upper_limit.hide()
    self.lineedit_g2_lower_limit = create_new_lineedit(self.groupBox_notenschl)
    self.gridLayout_6.addWidget(self.lineedit_g2_lower_limit, 2, 7, 1, 1)
    self.lineedit_g2_lower_limit.setValidator(validator)
    self.lineedit_g2_lower_limit.hide()

    try:
        if self.chosen_program == 'cria':
            key_notenschluessel_individual = 'notenschluessel_cria_individual'
        else:
            key_notenschluessel_individual = 'notenschluessel_individual'

        list_ = self.lama_settings[key_notenschluessel_individual]

        self.lineedit_sg_lower_limit.setText(list_[0])
        self.lineedit_g_upper_limit.setText(list_[1])
        self.lineedit_g_lower_limit.setText(list_[2])
        self.lineedit_b_upper_limit.setText(list_[3])
        self.lineedit_b_lower_limit.setText(list_[4])
        self.lineedit_g2_upper_limit.setText(list_[5])
        self.lineedit_g2_lower_limit.setText(list_[6])
    except KeyError:
        pass

    self.combobox_notenschluessel_saved.currentIndexChanged.connect(self.combobox_notenschluessel_saved_changed)

    self.groupBox_notenschl_modus = create_new_groupbox(
        self.groupBox_notenschl, "Anzeige"
    )
    self.groupBox_notenschl_modus.setSizePolicy(SizePolicy_fixed)
    self.gridLayout_6.addWidget(self.groupBox_notenschl_modus, 0, 8, 3, 1, QtCore.Qt.AlignRight)

    self.verticalLayout_ns_modus = create_new_verticallayout(
        self.groupBox_notenschl_modus
    )

    try:
        if self.chosen_program == 'cria':
            key = "notenschluessel_cria"
        else:
            key = "notenschluessel"
        ns_halbe_punkte_checked = self.lama_settings[key][0]
    except KeyError:
        ns_halbe_punkte_checked = False

    self.cb_ns_halbe_pkt = create_new_checkbox(
        self.groupBox_notenschl_modus,
        "Halbe Punkte",
        checked=ns_halbe_punkte_checked,
    )
    self.verticalLayout_ns_modus.addWidget(self.cb_ns_halbe_pkt)

    try:
        if self.chosen_program == 'cria':
            key = "notenschluessel_cria"
        else:
            key = "notenschluessel"
        ns_prozente_checked = self.lama_settings[key][1]
    except KeyError:
        ns_prozente_checked = False

    self.cb_ns_prozent = create_new_checkbox(
        self.groupBox_notenschl_modus, "Prozentangabe", checked=ns_prozente_checked
    )
    self.verticalLayout_ns_modus.addWidget(self.cb_ns_prozent)

    # self.cb_ns_NMS = create_new_checkbox(self.groupBox_notenschl_modus, "Modus: NMS")
    # self.verticalLayout_ns_modus.addWidget(self.cb_ns_NMS)

    self.gridLayout_5.addWidget(self.groupBox_notenschl, 2, 0, 1, 2)



    ### Groupbox Beurteilungsraster #####

    # self.groupBox_beurteilungsraster = QtWidgets.QGroupBox(self.groupBox_sage)
    # self.groupBox_beurteilungsraster.setObjectName("groupBox_beurteilungsraster")
    # # self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_beurteilungsraster)
    # # self.gridLayout_6.setObjectName("gridLayout_6")
    # self.verticalLayout_beurteilungsraster = create_new_verticallayout(self.groupBox_beurteilungsraster)

    # self.label_typ1_pkt = QtWidgets.QLabel(self.groupBox_beurteilungsraster)
    # self.label_typ1_pkt.setObjectName("label_typ1_pkt")
    # self.verticalLayout_beurteilungsraster.addWidget(self.label_typ1_pkt)
    # # self.gridLayout_6.addWidget(self.label_typ1_pkt, 0, 0, 1, 2)
    # # self.label_typ1_pkt.setText(_translate("MainWindow", "Punkte Typ 1: 0",None))

    # self.label_typ2_pkt = QtWidgets.QLabel(self.groupBox_beurteilungsraster)
    # self.label_typ2_pkt.setObjectName("label_typ2_pkt")
    # self.verticalLayout_beurteilungsraster.addWidget(self.label_typ2_pkt)
    # # self.gridLayout_6.addWidget(self.label_typ2_pkt, 1, 0, 1, 2)

    # self.groupBox_beurteilungsraster.setTitle("Beurteilungsraster")

    # self.gridLayout_5.addWidget(self.groupBox_beurteilungsraster, 2, 0, 1, 2)
    # self.groupBox_beurteilungsraster.hide()

    ### Zusammenfassung d. SA ###
    self.widgetSummarySage = QtWidgets.QWidget(self.groupBox_sage)
    self.widgetSummarySage.setObjectName("widgetSummarySage")
    self.gridLayout_5.addWidget(self.widgetSummarySage,3, 0, 1, 1)
    self.verticalLayoutSummarySage = create_new_verticallayout(self.widgetSummarySage)


    label = None
    if self.chosen_program == "lama":
        label = "Anzahl der Aufgaben: 0\n(Typ1: 0 / Typ2: 0)"

    elif self.chosen_program == "cria":
        label = "Anzahl der Aufgaben: 0"

    self.label_gesamtbeispiele = create_new_label(self.widgetSummarySage, label, True)
    self.verticalLayoutSummarySage.addWidget(self.label_gesamtbeispiele)
    # self.gridLayout_5.addWidget(self.label_gesamtbeispiele, 5, 0, 1, 2)

    self.label_gesamtpunkte = QtWidgets.QLabel(self.widgetSummarySage)
    # self.gridLayout_5.addWidget(self.label_gesamtpunkte, 6, 0, 1, 2)
    self.label_gesamtpunkte.setObjectName("label_gesamtpunkte")
    self.label_gesamtpunkte.setText("Gesamtpunkte: 0")
    self.verticalLayoutSummarySage.addWidget(self.label_gesamtpunkte)

    self.widgetSetupSage = QtWidgets.QWidget(self.groupBox_sage)
    self.widgetSetupSage.setObjectName("widgetSetupSage")
    self.gridLayout_5.addWidget(self.widgetSetupSage,3, 1, 1, 1)
    self.gridLayoutSetupSage = create_new_gridlayout(self.widgetSetupSage)


    self.cb_solution_sage = QtWidgets.QCheckBox(self.widgetSetupSage)
    self.cb_solution_sage.setObjectName("cb_solution")
    self.cb_solution_sage.setText("Lösungen anzeigen")
    self.cb_solution_sage.setChecked(True)
    self.cb_solution_sage.setSizePolicy(SizePolicy_fixed)
    self.cb_solution_sage.setFocusPolicy(QtCore.Qt.ClickFocus)
    self.gridLayoutSetupSage.addWidget(self.cb_solution_sage, 0,0,1,2, QtCore.Qt.AlignRight)


    self.cb_drafts_sage = QtWidgets.QCheckBox(self.widgetSetupSage)
    self.cb_drafts_sage.setSizePolicy(SizePolicy_fixed)
    self.cb_drafts_sage.setObjectName("cb_drafts_sage")
    # self.gridLayout_5.addWidget(self.cb_drafts_sage, 8, 3, 1, 1)
    self.cb_drafts_sage.setText("Entwürfe anzeigen")
    # self.horizontalLayout_2.addWidget(self.cb_drafts_sage)
    self.cb_drafts_sage.toggled.connect(self.cb_drafts_sage_enabled)
    self.gridLayoutSetupSage.addWidget(self.cb_drafts_sage,1,0,1,2, QtCore.Qt.AlignRight)


    if self.chosen_program != 'wizard':
        self.comboBox_klassen_changed("sage")

    self.label_gruppe_AB  = create_new_label(self.widgetSetupSage, "Gruppe:")
    self.label_gruppe_AB.setSizePolicy(SizePolicy_fixed)
    tooltip_text_gruppe_AB = "Auswahl welche Gruppenvariation bei der Ausgabe\nder Vorschau angezeigt wird (falls eine vorhanden ist)."
    self.label_gruppe_AB.setToolTip(tooltip_text_gruppe_AB)
    # self.gridLayout_5.addWidget(self.label_gruppe_AB, 7,4,1,1, QtCore.Qt.AlignRight)
    self.comboBox_gruppe_AB = create_new_combobox(self.widgetSetupSage)
    self.comboBox_gruppe_AB.setSizePolicy(SizePolicy_fixed)
    # self.gridLayout_5.addWidget(self.comboBox_gruppe_AB, 7,5,1,1)
    add_new_option(self.comboBox_gruppe_AB, 0, "A")
    add_new_option(self.comboBox_gruppe_AB, 1, "B")
    self.comboBox_gruppe_AB.setToolTip(tooltip_text_gruppe_AB)

    self.gridLayoutSetupSage.addWidget(self.label_gruppe_AB,2,0,1,1, QtCore.Qt.AlignRight)
    self.gridLayoutSetupSage.addWidget(self.comboBox_gruppe_AB, 2,1,1,1)


    self.gridLayout_stackSage.addWidget(self.splitter_sage, 0, 0, 1, 1)



    self.buttonBox_sage = QtWidgets.QDialogButtonBox(self.stackSage)
    self.buttonBox_sage.setStandardButtons(
        QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Ok
    )

    # self.gridLayout.addWidget(self.buttonBox_create_worksheet_wizard, 10,1,1,2)
    # self.buttonBox_create_worksheet_wizard.hide()
    # buttonS = self.buttonBox_titlepage.button(QtWidgets.QDialogButtonBox.Save)
    # buttonS.setText('Speichern')
    self.pushButton_vorschau = self.buttonBox_sage.button(QtWidgets.QDialogButtonBox.Save)
    self.pushButton_vorschau.setText("Vorschau")
    self.pushButton_vorschau.setIcon(QtGui.QIcon(get_icon_path('eye.svg')))
    self.pushButton_vorschau.setShortcut("Return")
    self.pushButton_vorschau.setFocusPolicy(QtCore.Qt.ClickFocus)

    self.pushButton_erstellen = self.buttonBox_sage.button(QtWidgets.QDialogButtonBox.Ok)
    self.pushButton_erstellen.setText("Speichern")
    self.pushButton_erstellen.setIcon(QtGui.QIcon(get_icon_path('save.svg'))) 
    self.pushButton_erstellen.setFocusPolicy(QtCore.Qt.ClickFocus)

    self.pushButton_vorschau.clicked.connect(partial(self.pushButton_vorschau_pressed, "vorschau"))

    self.pushButton_erstellen.clicked.connect(lambda: self.pushButton_erstellen_pressed())

    self.gridLayout_stackSage.addWidget(self.buttonBox_sage,1, 0, 1, 1)
    # self.gridLayout_5.addWidget(self.buttonBox_sage,0, 1, 1, 1)

    

def setup_stackCreator(self):
    self.gridLayout_stackCreator = create_new_gridlayout(self.stackCreator)

    self.splitter_creator = QtWidgets.QSplitter(self.stackCreator)
    self.splitter_creator.setOrientation(QtCore.Qt.Horizontal)
    self.splitter_creator.setObjectName("splitter_creator")
    self.gridLayout_stackCreator.addWidget(self.splitter_creator, 0, 0, 1, 1)

    self.splitter_creator_left_widget = QtWidgets.QWidget(self.splitter_creator)
    self.splitter_creator_left_widget.setMinimumWidth(1)
    self.splitter_creator_left_widget.resize(450,0)
    self.verticalLayout_splitter_creator_left_widget = create_new_verticallayout(self.splitter_creator_left_widget)
    self.verticalLayout_splitter_creator_left_widget.setContentsMargins(0,0,0,0)


    self.splitter_creator_right_widget = QtWidgets.QWidget(self.splitter_creator)
    self.splitter_creator_right_widget.setMinimumWidth(1) 
    self.verticalLayout_splitter_creator_right_widget = create_new_verticallayout(self.splitter_creator_right_widget)
    self.verticalLayout_splitter_creator_right_widget.setContentsMargins(0,0,0,0)



    ############# CREATOR ###############

    self.groupBox_variation_cr = create_new_groupbox(
        self.splitter_creator, "Variation vorhandener Aufgabe"
    )
    # self.groupBox_variation_cr.setMaximumWidth(420)
    self.horizontalLayout_variation = create_new_horizontallayout(
        self.groupBox_variation_cr
    )  
    self.button_variation_cr = create_new_button(
        self.groupBox_variation_cr,
        "Aufgabenvariation",
        partial(self.button_variation_cr_pressed, "creator"),
    )
    self.button_variation_cr.setIcon(QtGui.QIcon(get_icon_path('git-branch.svg')))
    self.horizontalLayout_variation.addWidget(self.button_variation_cr)


    self.button_translation_cr = create_new_button(
        self.groupBox_variation_cr,
        "Übersetzung",
        partial(self.button_variation_cr_pressed, "translation"),
    )
    self.button_translation_cr.setIcon(QtGui.QIcon(get_icon_path('globe.svg')))
    self.horizontalLayout_variation.addWidget(self.button_translation_cr)



    self.verticalLayout_splitter_creator_left_widget.addWidget(self.groupBox_variation_cr)

    ######################################

    ################ EDITOR #####################

    self.groupBox_choose_file = create_new_groupbox(
        self.splitter_creator, "Aufgabe auswählen"
    )
    # self.groupBox_choose_file.setMinimumSize(1,1)
    # self.groupBox_choose_file.setSizePolicy(SizePolicy_fixed_height)
    # self.groupBox_choose_file.setMaximumWidth(420)
    self.verticalLayout_choose_file = create_new_verticallayout(
        self.groupBox_choose_file
    )
    self.verticalLayout_choose_file.setContentsMargins(5,10,5,5)

    self.button_choose_file = create_new_button(
        self.groupBox_choose_file,
        "Aufgabe suchen...",
        partial(self.button_variation_cr_pressed, "editor"),
    )
    # self.button_choose_file.setMinimumHeight(20)
    # self.button_choose_file.sizeHint()
    # self.button_choose_file.setMinimumWidth(0)
    self.verticalLayout_choose_file.addWidget(self.button_choose_file)

    self.verticalLayout_splitter_creator_left_widget.addWidget(self.groupBox_choose_file)

    ########################################

    self.groupBox_grundkompetenzen_cr = QtWidgets.QGroupBox(self.splitter_creator)
    self.groupBox_grundkompetenzen_cr.setFocusPolicy(QtCore.Qt.NoFocus)
    self.groupBox_grundkompetenzen_cr.setObjectName("groupBox_grundkompetenzen_cr")
    # self.groupBox_grundkompetenzen_cr.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum))
    self.gridLayout_11_cr = QtWidgets.QGridLayout(self.groupBox_grundkompetenzen_cr)
    self.gridLayout_11_cr.setObjectName("gridLayout_11_cr")
    self.tab_widget_gk_cr = QtWidgets.QTabWidget(self.groupBox_grundkompetenzen_cr)


    self.tab_widget_gk_cr.setFocusPolicy(QtCore.Qt.NoFocus)
    self.tab_widget_gk_cr.setObjectName("tab_widget_gk_cr")
    self.gridLayout_11_cr.addWidget(self.tab_widget_gk_cr, 0, 0, 1, 1)
    self.verticalLayout_splitter_creator_left_widget.addWidget(self.groupBox_grundkompetenzen_cr)

    self.groupBox_grundkompetenzen_cr.setTitle("Grundkompetenzen")

    ### CRIA SAGE ###
    self.groupBox_themengebiete_cria = QtWidgets.QGroupBox(self.splitter_creator)

    self.groupBox_themengebiete_cria.setObjectName("groupBox_themengebiete_cria")
    # self.groupBox_themengebiete_cria.setMaximumWidth(420)
    self.gridLayout_11_cr_cria = QtWidgets.QGridLayout(
        self.groupBox_themengebiete_cria
    )
    self.gridLayout_11_cr_cria.setObjectName("gridLayout_11_cr_cria")
    self.tab_widget_cr_cria = QtWidgets.QTabWidget(self.groupBox_themengebiete_cria)

    self.tab_widget_cr_cria.setObjectName("tab_widget_cr_cria")
    self.tab_widget_cr_cria.setFocusPolicy(QtCore.Qt.NoFocus)
    self.gridLayout_11_cr_cria.addWidget(self.tab_widget_cr_cria, 0, 0, 1, 1)
    self.verticalLayout_splitter_creator_left_widget.addWidget(self.groupBox_themengebiete_cria)
    self.groupBox_themengebiete_cria.setTitle("Themengebiete")
    # self.groupBox_themengebiete_cria.setMinimumSize(1,1)
    # self.groupBox_themengebiete_cria.hide()


    for klasse in list_klassen:
        new_tab = add_new_tab(
            self.tab_widget_cr_cria, "{}. Klasse".format(klasse[1])
        )
        new_gridlayout = QtWidgets.QGridLayout(new_tab)
        new_gridlayout.setObjectName("{}".format(new_gridlayout))

        new_scrollarea = QtWidgets.QScrollArea(new_tab)
        new_scrollarea.setObjectName("{}".format(new_scrollarea))
        new_scrollarea.setFrameShape(QtWidgets.QFrame.NoFrame)
        new_scrollarea.setFocusPolicy(QtCore.Qt.NoFocus)
        new_scrollarea.setWidgetResizable(True)
        new_scrollareacontent = QtWidgets.QWidget()
        new_scrollareacontent.setObjectName("{}".format(new_scrollareacontent))

        new_verticallayout = QtWidgets.QVBoxLayout(new_scrollareacontent)
        new_verticallayout.setObjectName("{}".format(new_verticallayout))

        combobox_kapitel = create_new_combobox(new_scrollareacontent)
        self.dict_widget_variables[
            "combobox_kapitel_creator_cria_{}".format(klasse)
        ] = combobox_kapitel
        dict_klasse_name = eval("dict_{}_name".format(klasse))
        index = 0
        for kapitel in dict_klasse_name:
            add_new_option(
                combobox_kapitel,
                index,
                dict_klasse_name[kapitel] + " (" + kapitel + ")",
            )
            index += 1
        combobox_kapitel.currentIndexChanged.connect(
            partial(
                self.comboBox_kapitel_changed_cr,
                new_scrollareacontent,
                new_verticallayout,
                klasse,
                'creator',
            )
        )

        new_verticallayout.addWidget(combobox_kapitel)
        
        dict_klasse = eval("dict_{}".format(klasse))
        kapitel = list(dict_klasse_name.keys())[0]

        for unterkapitel in dict_klasse[kapitel]:
            new_checkbox = create_new_checkbox(
                new_scrollareacontent,
                dict_unterkapitel[unterkapitel] + " (" + unterkapitel + ")"
            )
            new_checkbox.setToolTip(dict_unterkapitel[unterkapitel])

            new_checkbox.stateChanged.connect(
                partial(
                    self.checkbox_unterkapitel_checked_cria,
                    new_checkbox,
                    klasse,
                    kapitel,
                    unterkapitel,
                )
            )
            self.dict_widget_variables[
                "checkbox_unterkapitel_creator_{0}_{1}_{2}".format(
                    klasse, kapitel, unterkapitel
                )
            ] = new_checkbox
            new_verticallayout.addWidget(new_checkbox)
            new_checkbox.setFocusPolicy(QtCore.Qt.NoFocus)

        new_verticallayout.addStretch()

        new_scrollarea.setWidget(new_scrollareacontent)

        new_gridlayout.addWidget(new_scrollarea, 2, 0, 1, 1)

    ##########################



    self.groupBox_ausgew_gk_cr = create_new_groupbox(self.splitter_creator, "Auswahl")
    self.groupBox_ausgew_gk_cr.setMinimumSize(1,1)
    self.verticalLayout_2 = create_new_verticallayout(self.groupBox_ausgew_gk_cr)

    self.label_ausgew_gk_creator = create_new_label(
        self.groupBox_ausgew_gk_cr, "", True
    )

    self.verticalLayout_2.addWidget(self.label_ausgew_gk_creator)
    self.verticalLayout_splitter_creator_left_widget.addWidget(self.groupBox_ausgew_gk_cr)

    self.groupBox_bilder = create_new_groupbox(
        self.splitter_creator, "Bilder (klicken, um Bilder zu entfernen)"
    )
    # self.groupBox_bilder.setSizePolicy(SizePolicy_maximum_height)

    self.verticalLayout_bilder = create_new_verticallayout(self.groupBox_bilder)
    self.verticalLayout_bilder.setContentsMargins(0,8,0,0)
    # self.gridLayout_13 = QtWidgets.QGridLayout(self.groupBox_bilder)
    # self.gridLayout_13.setObjectName("gridLayout_13")
    self.scrollArea = QtWidgets.QScrollArea(self.groupBox_bilder)
    self.scrollArea.setWidgetResizable(True)
    self.scrollArea.setObjectName("scrollArea")
    self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
    self.scrollArea.setFocusPolicy(QtCore.Qt.NoFocus)
    self.scrollAreaWidgetContents_bilder = QtWidgets.QWidget()

    self.scrollAreaWidgetContents_bilder.setObjectName("scrollAreaWidgetContents_bilder")
    self.verticalLayout_bilder2 = QtWidgets.QVBoxLayout(
        self.scrollAreaWidgetContents_bilder
    )
    self.verticalLayout_bilder2.setContentsMargins(0,2,0,5)
    self.verticalLayout_bilder2.setObjectName("verticalLayout")
    self.scrollArea.setWidget(self.scrollAreaWidgetContents_bilder)
    self.verticalLayout_bilder.addWidget(self.scrollArea)
    self.groupBox_bilder.setTitle("Bilder")
    self.groupBox_bilder.setMinimumSize(1,1)
    # self.groupBox_bilder.setSizePolicy(SizePolicy_maximum_height)

   
    self.verticalLayout_bilder2.addStretch()
    self.btn_add_image = create_new_button(
        self.groupBox_bilder, "", self.btn_add_image_pressed
    )
    self.btn_add_image.setIcon(QtGui.QIcon(get_icon_path('plus-square.svg')))
    # self.btn_add_image.setSizePolicy(SizePolicy_fixed)
    self.verticalLayout_bilder2.addWidget(self.btn_add_image)
    

    self.verticalLayout_splitter_creator_left_widget.addWidget(self.groupBox_bilder)
    #### CREATE CHECKBOXES ####
    ##### AG #####
    self.create_tab_checkboxes_gk(
        self.tab_widget_gk_cr, "Algebra und Geometrie", ag_beschreibung, "creator"
    )

    # # #### FA ####
    self.create_tab_checkboxes_gk(
        self.tab_widget_gk_cr,
        "Funktionale Abhängigkeiten",
        fa_beschreibung,
        "creator",
    )

    # ##### AN ####
    self.create_tab_checkboxes_gk(
        self.tab_widget_gk_cr, "Analysis", an_beschreibung, "creator"
    )

    # ### WS ####
    self.create_tab_checkboxes_gk(
        self.tab_widget_gk_cr,
        "Wahrscheinlichkeit und Statistik",
        ws_beschreibung,
        "creator",
    )

    # ### Zusatzthemen ###
    self.create_tab_checkboxes_themen(self.tab_widget_gk_cr, "creator")

    ############################



    self.widget_basic_settings_creator = QtWidgets.QWidget(self.splitter_creator_right_widget)
    self.widget_basic_settings_creator.setMinimumSize(1,1)
    self.verticalLayout_splitter_creator_right_widget.addWidget(self.widget_basic_settings_creator)

    self.horizontalLayout_basic_settings_creator = create_new_horizontallayout(self.widget_basic_settings_creator)
    self.horizontalLayout_basic_settings_creator.setContentsMargins(0,0,0,0)


    self.groupBox_aufgabentyp = create_new_groupbox(self.widget_basic_settings_creator, "Aufgabentyp")
    # self.groupBox_aufgabentyp.setSizePolicy(SizePolicy_fixed)
    self.gridLayout_3 = create_new_horizontallayout(self.groupBox_aufgabentyp)

    self.comboBox_aufgabentyp_cr = create_new_combobox(self.groupBox_aufgabentyp)
    add_new_option(self.comboBox_aufgabentyp_cr, 0, "1")
    add_new_option(self.comboBox_aufgabentyp_cr, 1, "2")

    self.comboBox_aufgabentyp_cr.currentIndexChanged.connect(self.chosen_aufgabenformat_cr)
    self.gridLayout_3.addWidget(self.comboBox_aufgabentyp_cr)
    self.horizontalLayout_basic_settings_creator.addWidget(self.groupBox_aufgabentyp)   


    self.groupBox_punkte = create_new_groupbox(self.widget_basic_settings_creator, "Punkte")

    self.horizontalLayout_punkte_creator = create_new_horizontallayout(self.groupBox_punkte)

    self.spinBox_punkte = create_new_spinbox(self.groupBox_punkte, 1)

    
    self.horizontalLayout_punkte_creator.addWidget(self.spinBox_punkte)
    self.horizontalLayout_basic_settings_creator.addWidget(self.groupBox_punkte)


    self.groupBox_aufgabenformat = create_new_groupbox(self.widget_basic_settings_creator, "Aufgabenformat")


    self.horizontalLayout_aufgabenformat_creator = create_new_horizontallayout(self.groupBox_aufgabenformat)


    self.comboBox_af = create_new_combobox(self.groupBox_aufgabenformat)
    add_new_option(self.comboBox_af, 0, "bitte auswählen")

    self.horizontalLayout_aufgabenformat_creator.addWidget(self.comboBox_af)


    i = 1
    for all in dict_aufgabenformate:
        add_new_option(self.comboBox_af, i, dict_aufgabenformate[all])
        if self.chosen_program == "lama" and i == 4:
            break
        i += 1
    self.horizontalLayout_basic_settings_creator.addWidget(self.groupBox_aufgabenformat)

    self.groupBox_klassen_cr = create_new_groupbox(self.widget_basic_settings_creator, "Klasse")


    self.horizontalLayout_klassen_cr = create_new_horizontallayout(self.groupBox_klassen_cr)
    self.comboBox_klassen_cr = create_new_combobox(self.groupBox_klassen_cr)

    add_new_option(self.comboBox_klassen_cr, 0, "-")

    i=1
    for all in Klassen:
        if all != "univie" and all != "mat":
            add_new_option(self.comboBox_klassen_cr, i, Klassen[all])
            i+=1


    self.horizontalLayout_klassen_cr.addWidget(self.comboBox_klassen_cr)
    self.horizontalLayout_basic_settings_creator.addWidget(self.groupBox_klassen_cr)

    self.groupBox_abstand = create_new_groupbox(self.widget_basic_settings_creator, "Abstand")

    self.groupBox_abstand.setToolTip("Abstand unter der Aufgabe (in cm)")
    self.horizontalLayout_abstand = create_new_horizontallayout(
        self.groupBox_abstand
    )
    self.spinBox_abstand = create_new_spinbox(self.groupBox_abstand)
    self.horizontalLayout_abstand.addWidget(self.spinBox_abstand)

    self.horizontalLayout_basic_settings_creator.addWidget(self.groupBox_abstand)



    self.groupBox_pagebreak = create_new_groupbox(
        self.widget_basic_settings_creator, "Seitenumbruch"
    )

    self.horizontalLayout_pagebreak = create_new_horizontallayout(
        self.groupBox_pagebreak
    )
    self.comboBox_pagebreak = create_new_combobox(self.groupBox_pagebreak)
    add_new_option(self.comboBox_pagebreak, 0, "nicht möglich")
    add_new_option(self.comboBox_pagebreak, 1, "möglich")
    self.horizontalLayout_pagebreak.addWidget(self.comboBox_pagebreak)

    self.horizontalLayout_basic_settings_creator.addWidget(self.groupBox_pagebreak)

    self.button_language = QtWidgets.QPushButton(self.widget_basic_settings_creator)
    self.button_language.setIcon(QtGui.QIcon(get_icon_path("globe.svg")))
    self.button_language.setText("DE")
    self.button_language.setSizePolicy(SizePolicy_fixed)
    self.button_language.clicked.connect(lambda: self.button_language_pressed())
    self.button_language.setToolTip("Deutsch")
    self.button_language.sizeHint()
    self.horizontalLayout_basic_settings_creator.addWidget(self.button_language)
    


    self.cb_matura_tag = create_new_checkbox(self.widget_basic_settings_creator, "Matura")
    self.horizontalLayout_basic_settings_creator.addWidget(self.cb_matura_tag)
    self.cb_matura_tag.hide()


    self.cb_no_grade_tag = create_new_checkbox(
        self.widget_basic_settings_creator, "klassen-\nunabhängig"
    )
    self.horizontalLayout_basic_settings_creator.addWidget(self.cb_no_grade_tag)
    self.cb_no_grade_tag.hide()



    self.groupBox_titel_cr = QtWidgets.QGroupBox(self.splitter_creator_right_widget)
    self.groupBox_titel_cr.setObjectName("groupBox_titel_cr")
    # self.groupBox_titel_cr.setSizePolicy(SizePolicy_fixed_height)

    self.gridLayout_14 = QtWidgets.QGridLayout(self.groupBox_titel_cr)
    self.gridLayout_14.setObjectName("gridLayout_14")
    self.lineEdit_titel = QtWidgets.QLineEdit(self.groupBox_titel_cr)
    self.lineEdit_titel.setObjectName("lineEdit_titel")


    self.gridLayout_14.addWidget(self.lineEdit_titel, 0, 0, 1, 1)
    self.verticalLayout_splitter_creator_right_widget.addWidget(self.groupBox_titel_cr)

    self.groupBox_titel_cr.setTitle("Titel")
    self.groupBox_titel_cr.setMinimumSize(1,1)


    self.groupBox_beispieleingabe = QtWidgets.QGroupBox(self.splitter_creator)
    self.groupBox_beispieleingabe.setObjectName("groupBox_beispieleingabe")

    self.gridLayout_10 = QtWidgets.QGridLayout(self.groupBox_beispieleingabe)
    self.gridLayout_10.setObjectName("gridLayout_10")
    self.label = QtWidgets.QLabel(self.groupBox_beispieleingabe)

    self.label.setStyleSheet("border: 2px solid #C33A3F;")
    self.label.setWordWrap(True)
    self.label.setObjectName("label")
    self.gridLayout_10.addWidget(self.label, 0, 0, 1, 1)
    self.plainTextEdit = QtWidgets.QPlainTextEdit(self.groupBox_beispieleingabe)
    self.plainTextEdit.setObjectName("plainTextEdit")
    self.plainTextEdit.setTabChangesFocus(True)
    self.gridLayout_10.addWidget(self.plainTextEdit, 1, 0, 1, 1)
    self.verticalLayout_splitter_creator_right_widget.addWidget(self.groupBox_beispieleingabe)

    self.groupBox_beispieleingabe.setTitle("Aufgabeneingabe")
    self.groupBox_beispieleingabe.setMinimumSize(1,1)
    self.label.setText("Info: Eingabe des Aufgabentextes zwischen \\begin{beispiel}...\\end{beispiel}")


    self.groupBox_quelle = QtWidgets.QGroupBox(self.splitter_creator_right_widget)
    self.groupBox_quelle.setObjectName("groupBox_quelle")

    self.gridLayout_18 = QtWidgets.QGridLayout(self.groupBox_quelle)
    self.gridLayout_18.setObjectName("gridLayout_18")
    self.lineEdit_quelle = QtWidgets.QLineEdit(self.groupBox_quelle)
    self.lineEdit_quelle.setObjectName("lineEdit_quelle")
    try:
        quelle = self.lama_settings["quelle"]
    except KeyError:
        quelle = ""

    self.lineEdit_quelle.setText(quelle)
    self.gridLayout_18.addWidget(self.lineEdit_quelle, 0, 0, 1, 1)

    self.verticalLayout_splitter_creator_right_widget.addWidget(self.groupBox_quelle)

    self.groupBox_quelle.setTitle("Quelle oder Autor (Vorname Nachname) - Eingabe: VorNac")
    self.groupBox_quelle.setMinimumSize(1,1)

    self.widgetcreatorButtons = QtWidgets.QWidget(self.stackCreator)
    self.gridLayout_stackCreator.addWidget(self.widgetcreatorButtons, 1,0,1,1)
    self.widgetcreatorButtons.setSizePolicy(SizePolicy_fixed_height)
    self.horizontalLayout_creatorButtons = create_new_horizontallayout(self.widgetcreatorButtons)
    self.horizontalLayout_creatorButtons.setContentsMargins(0,0,0,0)


    self.horizontalLayout_creatorButtons.addStretch()
    self.pushButton_save = QtWidgets.QPushButton(self.widgetcreatorButtons)
    self.pushButton_save.setObjectName("pushButton_save")
    self.pushButton_save.setFocusPolicy(QtCore.Qt.NoFocus)
    self.pushButton_save.setSizePolicy(SizePolicy_fixed)
    self.horizontalLayout_creatorButtons.addWidget(self.pushButton_save)
    self.pushButton_save.setText("Speichern")
    self.pushButton_save.setIcon(QtGui.QIcon(get_icon_path('save.svg')))
    # self.pushButton_save.hide()

    self.pushButton_save_translation = QtWidgets.QPushButton(self.widgetcreatorButtons)
    self.pushButton_save_translation.setObjectName("pushButton_save")
    self.pushButton_save_translation.setFocusPolicy(QtCore.Qt.NoFocus)
    self.pushButton_save_translation.setSizePolicy(SizePolicy_fixed)
    self.horizontalLayout_creatorButtons.addWidget(self.pushButton_save_translation)
    self.pushButton_save_translation.setText("Speichern")
    self.pushButton_save_translation.setIcon(QtGui.QIcon(get_icon_path('save.svg')))
    self.pushButton_save_translation.hide()


    self.pushButton_vorschau_edit = create_new_button(
        self.widgetcreatorButtons, "Vorschau", self.button_vorschau_edit_pressed
    )
    self.pushButton_vorschau_edit.setIcon(QtGui.QIcon(get_icon_path('eye.svg')))
    self.pushButton_vorschau_edit.setShortcut("Ctrl+Return")
    self.pushButton_vorschau_edit.setToolTip("Strg+Enter")
    self.pushButton_vorschau_edit.setSizePolicy(SizePolicy_fixed)
    self.horizontalLayout_creatorButtons.addWidget(self.pushButton_vorschau_edit)
    # self.pushButton_vorschau_edit.hide()

    self.pushButton_delete_file = create_new_button(
        self.widgetcreatorButtons, "Aufgabe löschen", self.button_delete_file_pressed
    )
    self.pushButton_delete_file.setIcon(QtGui.QIcon(get_icon_path('trash-2.svg')))
    # self.pushButton_delete_file.setStyleSheet("color: red")
    self.pushButton_delete_file.setSizePolicy(SizePolicy_fixed)
    self.horizontalLayout_creatorButtons.addWidget(self.pushButton_delete_file)
    # self.pushButton_delete_file.hide()

    self.pushButton_save_as_variation_edit = create_new_button(
        self.widgetcreatorButtons,
        "Als Variation einer anderen Aufgabe speichern",
        self.pushButton_save_as_variation_edit_pressed,
    )
    self.pushButton_save_as_variation_edit.setIcon(QtGui.QIcon(get_icon_path('git-branch.svg')))
    self.pushButton_save_as_variation_edit.setSizePolicy(SizePolicy_fixed)
    self.horizontalLayout_creatorButtons.addWidget(self.pushButton_save_as_variation_edit)
    # self.pushButton_save_as_variation_edit.hide()

    self.pushButton_save_edit = create_new_button(
        self.stackCreator, "Änderung speichern", lambda: self.button_save_edit_pressed("editor")
    )
    self.pushButton_save_edit.setIcon(QtGui.QIcon(get_icon_path('save.svg')))
    self.pushButton_save_edit.setSizePolicy(SizePolicy_fixed)
    self.pushButton_save_edit.setFocusPolicy(QtCore.Qt.NoFocus)
    self.horizontalLayout_creatorButtons.addWidget(self.pushButton_save_edit)
    # self.pushButton_save_edit.hide()

    self.lineEdit_titel.setFocus()
    self.tab_widget_gk_cr.setCurrentIndex(0)
    QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    ############ Infos for GKs
    self.create_Tooltip(ag_beschreibung)
    self.create_Tooltip(fa_beschreibung)
    self.create_Tooltip(an_beschreibung)
    self.create_Tooltip(ws_beschreibung)
    ############################################

    self.comboBox_aufgabentyp_cr.currentIndexChanged.connect(self.chosen_aufgabenformat_cr)
    self.pushButton_save.clicked.connect(lambda: self.button_speichern_pressed())
    self.pushButton_save_translation.clicked.connect(lambda: self.button_save_edit_pressed("translation"))



def setup_stackFeedback(self):
    self.gridLayout_stackFeedback = create_new_gridlayout(self.stackFeedback)


    self.splitter_feedback = QtWidgets.QSplitter(self.stackFeedback)
    self.splitter_feedback.setOrientation(QtCore.Qt.Horizontal)
    self.splitter_feedback.setObjectName("splitter_feedback")
    self.gridLayout_stackFeedback.addWidget(self.splitter_feedback, 0, 0, 1, 1)


    self.splitter_feedback_left_widget = QtWidgets.QWidget(self.splitter_feedback)
    self.splitter_feedback_left_widget.setMinimumWidth(1)
    self.splitter_feedback_left_widget.resize(150,0)
    self.verticalLayout_splitter_feedback_left_widget = create_new_verticallayout(self.splitter_feedback_left_widget)
    self.verticalLayout_splitter_feedback_left_widget.setContentsMargins(0,0,0,0)


    self.groupBox_alle_aufgaben_fb = QtWidgets.QGroupBox(self.splitter_feedback_left_widget)
    self.groupBox_alle_aufgaben_fb.setMinimumWidth(1)
    self.groupBox_alle_aufgaben_fb.setObjectName("groupBox_alle_aufgaben_fb")
    self.verticalLayout_splitter_feedback_left_widget.addWidget(self.groupBox_alle_aufgaben_fb)

    self.verticalLayout_fb = QtWidgets.QVBoxLayout(self.groupBox_alle_aufgaben_fb)
    self.verticalLayout_fb.setObjectName("verticalLayout_fb")


    self.comboBox_at_fb = QtWidgets.QComboBox(self.groupBox_alle_aufgaben_fb)
    # self.comboBox_at_fb.setSizePolicy(SizePolicy_fixed)
    self.comboBox_at_fb.setObjectName("comboBox_at_fb")
    self.comboBox_at_fb.addItem("")
    self.comboBox_at_fb.addItem("")
    self.verticalLayout_fb.addWidget(self.comboBox_at_fb)

    self.comboBox_at_fb.setItemText(0, "Typ 1")
    self.comboBox_at_fb.setItemText(1, "Typ 2")
    self.comboBox_at_fb.addItem("")
    self.comboBox_at_fb.setItemText(2, "Allgemeine Rückmeldung")
    # if self.chosen_program == 'cria':
    #     self.comboBox_at_fb.setItemText(0, _translate("MainWindow", "Aufgabenrückmeldung", None))
    #     self.comboBox_at_fb.setItemText(1, _translate("MainWindow", "Allgemeine Rückmeldung", None))
    self.comboBox_at_fb.currentIndexChanged.connect(self.comboBox_at_fb_changed)
    # self.comboBox_at_fb.setFocusPolicy(QtCore.Qt.ClickFocus)
    # self.comboBox_at_fb.hide()

    self.comboBox_fb = QtWidgets.QComboBox(self.groupBox_alle_aufgaben_fb)
    self.comboBox_fb.setObjectName("comboBox_fb")
    list_comboBox_fb = ["", "AG", "FA", "AN", "WS", "Zusatzthemen"]
    index = 0
    for all in list_comboBox_fb:
        self.comboBox_fb.addItem("")
        self.comboBox_fb.setItemText(index, all)
        index += 1
    self.comboBox_fb.currentIndexChanged.connect(
        partial(self.comboBox_gk_changed, "feedback")
    )
    self.comboBox_fb.setFocusPolicy(QtCore.Qt.ClickFocus)
    self.verticalLayout_fb.addWidget(self.comboBox_fb)
    self.comboBox_fb_num = QtWidgets.QComboBox(self.groupBox_alle_aufgaben_fb)
    self.comboBox_fb_num.setObjectName("comboBox_gk_num")
    self.comboBox_fb_num.currentIndexChanged.connect(
        partial(self.comboBox_gk_num_changed, "feedback")
    )
    self.comboBox_fb_num.setFocusPolicy(QtCore.Qt.ClickFocus)
    self.verticalLayout_fb.addWidget(self.comboBox_fb_num)
    self.lineEdit_number_fb = QtWidgets.QLineEdit(self.groupBox_alle_aufgaben_fb)
    self.lineEdit_number_fb.setObjectName("lineEdit_number_fb")
    self.lineEdit_number_fb.textChanged.connect(
        partial(self.lineEdit_number_changed, "feedback")
    )
    self.verticalLayout_fb.addWidget(self.lineEdit_number_fb)
    self.listWidget_fb = QtWidgets.QListWidget(self.groupBox_alle_aufgaben)
    self.listWidget_fb.setObjectName("listWidget_fb")
    self.verticalLayout_fb.addWidget(self.listWidget_fb)
    self.listWidget_fb.itemClicked.connect(self.nummer_clicked_fb)



    #### Feedback Cria ##########################
    
    self.comboBox_at_fb_cria = QtWidgets.QComboBox(self.splitter_feedback_left_widget)
    self.comboBox_at_fb_cria.setObjectName("comboBox_at_fb_cria")
    self.comboBox_at_fb_cria.addItem("Aufgabenrückmeldung")
    self.comboBox_at_fb_cria.addItem("Allgemeine Rückmeldung")
    self.comboBox_at_fb_cria.currentIndexChanged.connect(
        self.comboBox_at_fb_cria_changed
    )

    self.verticalLayout_splitter_feedback_left_widget.addWidget(self.comboBox_at_fb_cria)
    # if self.chosen_program == 'cria':
    #     self.comboBox_at_fb.setItemText(0, _translate("MainWindow", "Aufgabenrückmeldung", None))
    #     self.comboBox_at_fb.setItemText(1, _translate("MainWindow", "Allgemeine Rückmeldung", None))
    # self.comboBox_at_fb.currentIndexChanged.connect(self.comboBox_at_fb_changed)
    # self.comboBox_at_fb.setFocusPolicy(QtCore.Qt.ClickFocus)

    # self.gridLayout_stackFeedback.addWidget(self.comboBox_at_fb_cria, 0, 0, 1, 1)
    # self.comboBox_at_fb_cria.hide()

    self.groupBox_alle_aufgaben_fb_cria = QtWidgets.QGroupBox(self.splitter_feedback_left_widget)
    self.groupBox_alle_aufgaben_fb_cria.setMinimumWidth(1)
    self.groupBox_alle_aufgaben_fb_cria.setObjectName("groupBox_alle_aufgaben_fb_cria")
    self.verticalLayout_splitter_feedback_left_widget.addWidget(self.groupBox_alle_aufgaben_fb_cria)

    self.verticalLayout_fb_cria = QtWidgets.QVBoxLayout(
        self.groupBox_alle_aufgaben_fb_cria
    )
    self.verticalLayout_fb_cria.setObjectName("verticalLayout_fb_cria")
    self.comboBox_klassen_fb_cria = QtWidgets.QComboBox(
        self.groupBox_alle_aufgaben_fb_cria
    )
    self.comboBox_klassen_fb_cria.setObjectName("self.comboBox_klassen_fb_cria")

    self.comboBox_klassen_fb_cria.addItem("")
    i = 1
    for all in list_klassen:

        self.comboBox_klassen_fb_cria.addItem("")

        self.comboBox_klassen_fb_cria.setItemText(i, f"{all[1]}. Klasse")
        i += 1

    self.comboBox_klassen_fb_cria.currentIndexChanged.connect(
        partial(self.comboBox_klassen_changed, "feedback")
    )

    self.comboBox_klassen_fb_cria.setFocusPolicy(QtCore.Qt.ClickFocus)
    self.verticalLayout_fb_cria.addWidget(self.comboBox_klassen_fb_cria)
    self.comboBox_kapitel_fb_cria = QtWidgets.QComboBox(
        self.groupBox_alle_aufgaben_fb_cria
    )
    self.comboBox_kapitel_fb_cria.setObjectName("self.comboBox_kapitel_fb_cria")

    # self.comboBox_kapitel_fb_cria.currentIndexChanged.connect(
    #     partial(self.comboBox_kapitel_changed, "feedback")
    # )
    self.comboBox_kapitel_fb_cria.setFocusPolicy(QtCore.Qt.ClickFocus)
    self.verticalLayout_fb_cria.addWidget(self.comboBox_kapitel_fb_cria)

    self.comboBox_unterkapitel_fb_cria = QtWidgets.QComboBox(
        self.groupBox_alle_aufgaben_fb_cria
    )
    self.comboBox_unterkapitel_fb_cria.setObjectName(
        "self.comboBox_unterkapitel_fb_cria"
    )

    # self.comboBox_unterkapitel_fb_cria.currentIndexChanged.connect(
    #     partial(self.comboBox_unterkapitel_changed, "feedback")
    # )
    self.comboBox_unterkapitel_fb_cria.setFocusPolicy(QtCore.Qt.ClickFocus)
    self.verticalLayout_fb_cria.addWidget(self.comboBox_unterkapitel_fb_cria)

    self.lineEdit_number_fb_cria = QtWidgets.QLineEdit(
        self.groupBox_alle_aufgaben_fb_cria
    )
    self.lineEdit_number_fb_cria.setObjectName("lineEdit_number_fb_cria")

    self.lineEdit_number_fb_cria.textChanged.connect(lambda: self.adapt_choosing_list("feedback"))
    
    self.verticalLayout_fb_cria.addWidget(self.lineEdit_number_fb_cria)
    self.listWidget_fb_cria = QtWidgets.QListWidget(
        self.groupBox_alle_aufgaben_fb_cria
    )
    self.listWidget_fb_cria.setObjectName("listWidget_fb_cria")
    self.verticalLayout_fb_cria.addWidget(self.listWidget_fb_cria)
    self.listWidget_fb_cria.itemClicked.connect(self.nummer_clicked_fb)
    # self.gridLayout_stackFeedback.addWidget(self.groupBox_alle_aufgaben_fb_cria, 1, 0, 1, 1)
    self.groupBox_alle_aufgaben_fb_cria.setTitle("Aufgaben")
    
    # self.groupBox_alle_aufgaben_fb_cria.hide()

    self.comboBox_kapitel_fb_cria.addItem("")
    for all in dict_k1_name:
        self.comboBox_kapitel_fb_cria.addItem(dict_k1_name[all] + " (" + all + ")")
    ###############################################


    self.comboBox_kapitel_fb_cria.currentIndexChanged.connect(
        partial(self.comboBox_kapitel_changed, "feedback")
    )

    self.comboBox_unterkapitel_fb_cria.currentIndexChanged.connect(
        partial(self.comboBox_unterkapitel_changed, "feedback")
    )





    # self.gridLayout_stackFeedback.addWidget(self.groupBox_alle_aufgaben_fb, 0, 0, 5, 1)
    self.groupBox_alle_aufgaben_fb.setTitle("Aufgaben")

    self.splitter_feedback_right_widget = QtWidgets.QWidget(self.splitter_feedback)
    self.splitter_feedback_right_widget.setMinimumWidth(1)  
    self.verticalLayout_splitter_feedback_right_widget = create_new_verticallayout(self.splitter_feedback_right_widget)
    self.verticalLayout_splitter_feedback_right_widget.setContentsMargins(0,0,0,0)



    self.label_example = QtWidgets.QLabel(self.splitter_feedback_right_widget)
    self.label_example.setMinimumWidth(1)
    self.label_example.setObjectName("label_example")
    # self.label_update.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    self.label_example.setText("Ausgewählte Aufgabe: -")
    self.verticalLayout_splitter_feedback_right_widget.addWidget(self.label_example)
    # self.gridLayout_stackFeedback.addWidget(self.label_example, 0, 1, 1, 1)

    self.groupBox_fehlertyp = QtWidgets.QGroupBox(self.splitter_feedback_right_widget)
    self.groupBox_fehlertyp.setMinimumWidth(1)
    # self.groupBox_fehlertyp.setSizePolicy(SizePolicy_fixed)
    self.groupBox_fehlertyp.setObjectName("groupBox_fehlertyp")
    self.gridLayout_fehlertyp = QtWidgets.QGridLayout(self.groupBox_fehlertyp)
    self.gridLayout_fehlertyp.setObjectName("gridLayout_feedback")
    self.groupBox_fehlertyp.setTitle("Betreff")

    self.comboBox_fehlertyp = QtWidgets.QComboBox(self.groupBox_fehlertyp)
    self.comboBox_fehlertyp.setObjectName("comboBox_pruefungstyp")

    list_fehlertypen = [
        "Feedback",
        "Fehler in der Angabe",
        "Fehler in der Lösung",
        "Bild wird nicht (richtig) angezeigt",
        "Grafik ist unleserlich/fehlerhaft",
        "Aufgabe ist doppelt vorhanden",
        "Falsche Kodierung (Grundkompetenz, Aufgabenformat, ...)",
        "Sonstiges",
    ]
    
    for i, all in enumerate(list_fehlertypen):
        add_new_option(self.comboBox_fehlertyp, i, all)


    self.comboBox_fehlertyp.setFocusPolicy(QtCore.Qt.ClickFocus)
    self.gridLayout_fehlertyp.addWidget(self.comboBox_fehlertyp, 0, 0, 1, 1)
    self.verticalLayout_splitter_feedback_right_widget.addWidget(self.groupBox_fehlertyp)
    # self.gridLayout_stackFeedback.addWidget(self.groupBox_fehlertyp, 1, 1, 1, 1)
    # self.groupBox_fehlertyp.hide()

    self.groupBox_feedback = QtWidgets.QGroupBox(self.splitter_feedback_right_widget)
    self.groupBox_feedback.setObjectName("groupBox_feedback")
    self.groupBox_feedback.setMinimumWidth(1)
    # self.groupBox_feedback.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding))
    self.gridLayout_fb = QtWidgets.QGridLayout(self.groupBox_feedback)
    self.gridLayout_fb.setObjectName("gridLayout_fb")
    self.plainTextEdit_fb = QtWidgets.QPlainTextEdit(self.groupBox_feedback)
    self.plainTextEdit_fb.setObjectName("plainTextEdit_fb")
    self.plainTextEdit_fb.setTabChangesFocus(True)

    self.gridLayout_fb.addWidget(self.plainTextEdit_fb, 0, 0, 1, 1)
    self.verticalLayout_splitter_feedback_right_widget.addWidget(self.groupBox_feedback)
    # self.gridLayout_stackFeedback.addWidget(self.groupBox_feedback, 2, 1, 1, 1)
    self.groupBox_feedback.setTitle("Feedback bzw. Problembeschreibung")
    # self.groupBox_feedback.hide()

    self.groupBox_email = QtWidgets.QGroupBox(self.splitter_feedback_right_widget)
    self.groupBox_email.setObjectName("groupBox_email")
    self.groupBox_email.setMinimumWidth(1)
    # self.groupBox_klasse.setMaximumSize(QtCore.QSize(200, 16777215))
    self.verticalLayout_email = QtWidgets.QVBoxLayout(self.groupBox_email)
    self.verticalLayout_email.setObjectName("verticalLayout_email")
    self.lineEdit_email = QtWidgets.QLineEdit(self.groupBox_email)
    self.lineEdit_email.setObjectName("lineEdit_email")
    self.groupBox_email.setTitle("E-Mail Adresse für Nachfragen (optional)")
    self.verticalLayout_email.addWidget(self.lineEdit_email)
    self.verticalLayout_splitter_feedback_right_widget.addWidget(self.groupBox_email)
    # self.gridLayout_stackFeedback.addWidget(self.groupBox_email, 3, 1, 1, 1)
    # self.groupBox_email.hide()


    self.buttonBox_feedback_send = QtWidgets.QDialogButtonBox(self.stackFeedback)
    self.buttonBox_feedback_send.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
    self.gridLayout_stackFeedback.addWidget(self.buttonBox_feedback_send, 1,0,1,2)

    button_send = self.buttonBox_feedback_send.button(QtWidgets.QDialogButtonBox.Ok)
    button_send.setText("Senden")
    button_send.setIcon(QtGui.QIcon(get_icon_path('send.svg')))
    button_send.clicked.connect(lambda: self.pushButton_send_pressed()) 


def setup_stackWizard(self):
    self.verticalLayout_stackWidget = create_new_verticallayout(self.stackWizard)
    self.worksheet_edited = True
    self.widgetTopics = QtWidgets.QWidget(self.stackWizard)
    self.widgetTopics.setSizePolicy(SizePolicy_fixed_height)
    self.verticalLayout_stackWidget.addWidget(self.widgetTopics)

    self.horizontalLayout_widgetTopics = create_new_horizontallayout(self.widgetTopics)
    self.horizontalLayout_widgetTopics.setContentsMargins(0,0,0,0)
    self.groupBox_topics = create_new_groupbox(self.widgetTopics, "Thema")
    self.horizontalLayout_widgetTopics.addWidget(self.groupBox_topics)

    self.horizontalLayout_groupBox_topics = create_new_horizontallayout(self.groupBox_topics)

    self.comboBox_themen_wizard = create_new_combobox(self.groupBox_topics)
    # self.horizontalLayout_groupBox_topics.addWidget(self.comboBox_themen_wizard)
    # for i, all in enumerate(dict_widgets_wizard.keys()):
    #     add_new_option(self.comboBox_themen_wizard, i, all)
    # self.comboBox_themen_wizard.currentIndexChanged.connect(self.themen_changed_wizard)
    self.comboBox_themen_wizard.hide()

    self.pushbutton_themen_wizard = QtWidgets.QPushButton(self.groupBox_topics)
    # print(list(dict_themen_wizard.values())[0][0])
    # self.pushbutton_themen_wizard.setText(dict_themen_wizard[list(dict_themen_wizard.values())[0][0]])
    self.pushbutton_themen_wizard.setText("Arithmetik \u2b9e Positive (Dezimal-)Zahlen \u2b9e Addition")
    self.chosen_topics_wizard = ["Arithmetik", "Positive (Dezimal-)Zahlen", "Addition"]
    self.horizontalLayout_groupBox_topics.addWidget(self.pushbutton_themen_wizard)

    self.menu_themen_wizard = QtWidgets.QMenu(self.groupBox_topics)
    # ag = QtGui.QActionGroup(self.filter_search, exclusive=False)

    def topic_chosen(list_topics):
        _string = list_topics[0]
        for all in list_topics[1:]:
            _string += f" \u2b9e {all}" 
        return lambda: self.pushbutton_themen_wizard.setText(_string)
    
    # def change_list_topic():
    #     button_text = self.pushbutton_themen_wizard.text()
    #     x = button_text.split(" \u2b9e ")
    #     self.chosen_topic_wizard = x
    #     print(self.chosen_topic_wizard)


    for level_0_keys, level_0_values in dict_themen_wizard.items():
        print(level_0_keys)
        print(level_0_values)
        submenu = self.menu_themen_wizard.addMenu(str(level_0_keys))

        for level_1_keys, level_1_values in level_0_values.items():
            print(level_1_keys)
            print(level_1_values)
            if type(level_1_values)==list:
                action = submenu.addAction(level_1_keys)
                list_topics = [level_0_keys, level_1_keys]
                action.triggered.connect(topic_chosen(list_topics))
            else:
                subsubmenu = submenu.addMenu(level_1_keys)

                for level_2_keys, level_2_values in level_1_values.items():
                    if type(level_2_values)==list: 
                        action = subsubmenu.addAction(level_2_keys)
                        list_topics = [level_0_keys, level_1_keys, level_2_keys]
                        action.triggered.connect(topic_chosen(list_topics))                                      
            # print(level_1_values)
        # for subtopic in subtopics:
        #     print(subtopic)
        #     subsubtopics = subtopics[subtopic]
            # if type(subsubtopics)==dict:
            #     subsubmenu = submenu.addMenu(str(subtopic))
                
            #     for subsubtopic in subsubtopics:
            #         action = subsubmenu.addAction(subsubtopic)
            #         list_topics = [topics, subtopic, subsubtopic]
            #         action.triggered.connect(topic_chosen(list_topics))
            # elif type(subsubtopics)==list:
            #     action = submenu.addAction(subtopic)
            #     list_topics = [topics, subtopic]
            #     action.triggered.connect(topic_chosen(list_topics))               


    self.menu_themen_wizard.triggered.connect(self.themen_changed_wizard)
    self.pushbutton_themen_wizard.setMenu(self.menu_themen_wizard)


    self.horizontalLayout_widgetTopics.addStretch()



    self.groupBox_setting_wizard = create_new_groupbox(self.stackWizard, "Voreinstellungen")
    self.groupBox_setting_wizard.setSizePolicy(SizePolicy_maximum_height)
    self.verticalLayout_stackWidget.addWidget(self.groupBox_setting_wizard)
    self.verticalLayout_setting_wizard = create_new_verticallayout(self.groupBox_setting_wizard)
    # self.groupBox_setting_wizard.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum,QtWidgets.QSizePolicy.Maximum))
    # self.gridLayout_wizard.addWidget(self.groupBox_setting_wizard, 1,0,1,2)
    # self.gridLayout_setting_wizard = create_new_gridlayout(self.groupBox_setting_wizard)
    # self.groupBox_setting_wizard.hide()

    self.widget_setting_wizard1 = QtWidgets.QWidget(self.groupBox_setting_wizard)
    self.verticalLayout_setting_wizard.addWidget(self.widget_setting_wizard1)
    self.horizontalLayout_setting_wizard1 = create_new_horizontallayout(self.widget_setting_wizard1)

    self.widget_number_wizard = QtWidgets.QWidget(self.widget_setting_wizard1)
    self.widget_number_wizard.setSizePolicy(SizePolicy_fixed)
    # create_new_groupbox(self.widget_setting_wizard1, "Aufgaben")
    # self.widget_number_wizard.setSizePolicy(SizePolicy_fixed)
    self.horizontalLayout_setting_wizard1.addWidget(self.widget_number_wizard)
    self.horizontalLayout_setting_wizard1.setContentsMargins(0,0,0,0)
    self.horizontalLayout_number_wizard = create_new_horizontallayout(self.widget_number_wizard)
    self.horizontalLayout_number_wizard.setContentsMargins(0,9,0,0)


    self.label_number_wizard = create_new_label(self.widget_number_wizard, "Aufgaben:")
    self.horizontalLayout_number_wizard.addWidget(self.label_number_wizard)

    self.spinBox_number_wizard = create_new_spinbox(self.widget_number_wizard, 10)

    self.spinBox_number_wizard.setMinimum(1)
    self.spinBox_number_wizard.valueChanged.connect(self.spinBox_number_wizard_changed)
    self.horizontalLayout_number_wizard.addWidget(self.spinBox_number_wizard)


    self.widget_column_wizard = QtWidgets.QWidget(self.widget_setting_wizard1)
    # create_new_groupbox(self.widgetWorksheetView, "Spalten")
    # self.widget_column_wizard.setSizePolicy(SizePolicy_fixed)
    self.horizontalLayout_setting_wizard1.addWidget(self.widget_column_wizard)

    self.horizontalLayout_column_wizard = create_new_horizontallayout(self.widget_column_wizard)
    self.horizontalLayout_column_wizard.setContentsMargins(0,9,0,0)
    self.icon_column_wizard = create_new_label_icon(self.widget_column_wizard, "columns.svg", icon_size=(20,20))
    self.horizontalLayout_column_wizard.addWidget(self.icon_column_wizard)

    self.spinBox_column_wizard = create_new_spinbox(self.widget_column_wizard, 2)
    self.spinBox_column_wizard.valueChanged.connect(self.spinBox_column_wizard_changed)
    self.spinBox_column_wizard.setRange(1, 10)
    self.horizontalLayout_column_wizard.addWidget(self.spinBox_column_wizard)   


    self.widget_settings_addon_wizard = QtWidgets.QWidget(self.widget_setting_wizard1)
    self.horizontalLayout_setting_wizard1.addWidget(self.widget_settings_addon_wizard)

    self.horizontalLayout_settings_addon_wizard = create_new_horizontallayout(self.widget_settings_addon_wizard)
    self.horizontalLayout_settings_addon_wizard.setContentsMargins(0,9,0,0)

    self.checkbox_enable_addition = create_new_checkbox(self.widget_settings_addon_wizard, "Addition", checked=True)
    self.horizontalLayout_settings_addon_wizard.addWidget(self.checkbox_enable_addition)
    self.checkbox_enable_addition.hide()

    self.checkbox_enable_subtraktion = create_new_checkbox(self.widget_settings_addon_wizard, "Subtraktion", checked=True)
    self.horizontalLayout_settings_addon_wizard.addWidget(self.checkbox_enable_subtraktion)  
    self.checkbox_enable_subtraktion.hide()


    self.widget_ausrichtung_wizard = QtWidgets.QWidget(self.widget_setting_wizard1)
    # create_new_groupbox(self.widget_setting_wizard1, "Ausrichtung")
    self.widget_ausrichtung_wizard.setSizePolicy(SizePolicy_fixed)
    self.horizontalLayout_setting_wizard1.addWidget(self.widget_ausrichtung_wizard)
    self.horizontalLayout_ausrichtung_wizard = create_new_horizontallayout(self.widget_ausrichtung_wizard)
    self.horizontalLayout_ausrichtung_wizard.setContentsMargins(0,9,0,0)


    self.label_ausrichtung_wizard = create_new_label(self.widget_ausrichtung_wizard, "Ausrichtung:")
    self.horizontalLayout_ausrichtung_wizard.addWidget(self.label_ausrichtung_wizard)

    self.combobox_ausrichtung_wizard = create_new_combobox(self.widget_ausrichtung_wizard)
    self.combobox_ausrichtung_wizard.currentIndexChanged.connect(self.combobox_ausrichtung_wizard_changed)
    add_new_option(self.combobox_ausrichtung_wizard, 0, "in der Spalte")
    add_new_option(self.combobox_ausrichtung_wizard, 1, "in der Zeile")
    self.horizontalLayout_ausrichtung_wizard.addWidget(self.combobox_ausrichtung_wizard)













    self.horizontalLayout_setting_wizard1.addStretch()
    # self.groupbox_instruction_wizard = create_new_groupbox(self.groupBox_setting_wizard, "Arbeitsanweisung")
    # self.gridLayout_setting_wizard.addWidget(self.groupbox_instruction_wizard, 1,0,1,1)
    # # self.groupbox_instruction_wizard.setSizePolicy(SizePolicy_maximum_height)

    # self.horizontalLayout_instruction_wizard = create_new_horizontallayout(self.groupbox_instruction_wizard)
    # self.plainTextEdit_instruction_wizard = QtWidgets.QPlainTextEdit(self.groupbox_instruction_wizard)
    # # self.plainTextEdit_instruction_wizard.setMaximumHeight(100)
    # self.horizontalLayout_instruction_wizard.addWidget(self.plainTextEdit_instruction_wizard)


    self.groupBox_zahlenbereich_wizard = create_new_groupbox(self.groupBox_setting_wizard, "Zahlenbereich")
    self.verticalLayout_setting_wizard.addWidget(self.groupBox_zahlenbereich_wizard)
    self.gridLayout_zahlenbereich_wizard = create_new_gridlayout(self.groupBox_zahlenbereich_wizard)



    # self.groupBox_zahlenbereich_anzahl = create_new_groupbox(self.groupBox_zahlenbereich_wizard, "Summanden")

    self.widgetZahlenbereich_anzahl = QtWidgets.QWidget(self.groupBox_zahlenbereich_wizard)
    self.widgetZahlenbereich_anzahl.setSizePolicy(SizePolicy_fixed)
    self.gridLayout_zahlenbereich_wizard.addWidget(self.widgetZahlenbereich_anzahl, 0,0,1,1)

    self.horizontalLayout_zahlenbereich_anzahl = create_new_horizontallayout(self.widgetZahlenbereich_anzahl)
    self.horizontalLayout_zahlenbereich_anzahl.setContentsMargins(0,0,0,0)

    # self.label_zahlenbereich_anzahl_wizard_icon = QtWidgets.QLabel(self.widgetZahlenbereich_anzahl)
    # self.label_zahlenbereich_anzahl_wizard_icon.setPixmap(QtGui.QPixmap(get_icon_path("hash.svg")))
    # # self.label_lamaLogo.setFixedHeight(30)
    # self.label_zahlenbereich_anzahl_wizard_icon.setFixedSize(QtCore.QSize(10,10))
    # self.label_zahlenbereich_anzahl_wizard_icon.setScaledContents(True)
    # self.horizontalLayout_zahlenbereich_anzahl.addWidget(self.label_zahlenbereich_anzahl_wizard_icon)

    self.label_zahlenbereich_anzahl_wizard = create_new_label(self.widgetZahlenbereich_anzahl, "Summanden:")
    self.horizontalLayout_zahlenbereich_anzahl.addWidget(self.label_zahlenbereich_anzahl_wizard)
    # self.horizontalLayout_zahlenbereich_anzahl.setContentsMargins(2,9,2,2)
    
    self.spinBox_zahlenbereich_anzahl_wizard = create_new_spinbox(self.widgetZahlenbereich_anzahl, 2)
    self.spinBox_zahlenbereich_anzahl_wizard.setRange(2,5)
    self.spinBox_zahlenbereich_anzahl_wizard.valueChanged.connect(self.worksheet_wizard_setting_changed)
    self.horizontalLayout_zahlenbereich_anzahl.addWidget(self.spinBox_zahlenbereich_anzahl_wizard)


    self.widget_zahlenbereich_minimum = QtWidgets.QWidget(self.groupBox_zahlenbereich_wizard)
    # create_new_groupbox(self.groupBox_zahlenbereich_wizard, "Minimum")
    self.gridLayout_zahlenbereich_wizard.addWidget(self.widget_zahlenbereich_minimum, 0,1,1,1)
    self.widget_zahlenbereich_minimum.setSizePolicy(SizePolicy_fixed)

    self.horizontalLayout_zahlenbereich_minimum = create_new_horizontallayout(self.widget_zahlenbereich_minimum)
    # self.onlyInt = QtGui.QIntValidator()

    self.label_zahlenbereich_minimum = create_new_label(self.widget_zahlenbereich_minimum, "Minimum:")
    self.horizontalLayout_zahlenbereich_minimum.addWidget(self.label_zahlenbereich_minimum)

    self.spinbox_zahlenbereich_minimum = create_new_spinbox(self.widget_zahlenbereich_minimum)
    self.spinbox_zahlenbereich_minimum.setRange(0,999999999)
    self.spinbox_zahlenbereich_minimum.setValue(100)
    self.horizontalLayout_zahlenbereich_minimum.addWidget(self.spinbox_zahlenbereich_minimum)


    self.widget_zahlenbereich_maximum = QtWidgets.QWidget(self.groupBox_zahlenbereich_wizard)
    self.widget_zahlenbereich_maximum.setSizePolicy(SizePolicy_fixed)
    # create_new_groupbox(self.groupBox_zahlenbereich_wizard, "Maximum")
    self.gridLayout_zahlenbereich_wizard.addWidget(self.widget_zahlenbereich_maximum, 0,2,1,1)
    self.horizontalLayout_zahlenbereich_maximum = create_new_horizontallayout(self.widget_zahlenbereich_maximum)

    self.label_zahlenbereich_maximum = create_new_label(self.widget_zahlenbereich_maximum, "Maximum:")
    self.horizontalLayout_zahlenbereich_maximum.addWidget(self.label_zahlenbereich_maximum)

    self.spinbox_zahlenbereich_maximum = create_new_spinbox(self.widget_zahlenbereich_maximum)
    self.spinbox_zahlenbereich_maximum.setRange(0,999999999)
    self.spinbox_zahlenbereich_maximum.setValue(999)
    self.horizontalLayout_zahlenbereich_maximum.addWidget(self.spinbox_zahlenbereich_maximum)
    self.spinbox_zahlenbereich_maximum.valueChanged.connect(self.worksheet_wizard_setting_changed)
    self.spinbox_zahlenbereich_minimum.valueChanged.connect(partial(self.minimum_changed_wizard, self.spinbox_zahlenbereich_minimum, self.spinbox_zahlenbereich_maximum))

    self.widget_kommastellen_wizard = QtWidgets.QWidget(self.groupBox_zahlenbereich_wizard)
    self.widget_kommastellen_wizard.setSizePolicy(SizePolicy_fixed)
    # create_new_groupbox(self.groupBox_zahlenbereich_wizard, "Kommastellen")
    self.gridLayout_zahlenbereich_wizard.addWidget(self.widget_kommastellen_wizard, 0,3,1,1)
    self.horizontalLayout_kommastellen_wizard = create_new_horizontallayout(self.widget_kommastellen_wizard)

    self.label_kommastellen_wizard = create_new_label(self.widget_kommastellen_wizard, "Kommastellen:")
    self.horizontalLayout_kommastellen_wizard.addWidget(self.label_kommastellen_wizard)

    self.combobox_kommastellen_wizard = create_new_combobox(self.widget_kommastellen_wizard)
    add_new_option(self.combobox_kommastellen_wizard, 0, "=")
    add_new_option(self.combobox_kommastellen_wizard, 1, "\u2264")
    self.combobox_kommastellen_wizard.currentIndexChanged.connect(self.worksheet_wizard_setting_changed)
    self.horizontalLayout_kommastellen_wizard.addWidget(self.combobox_kommastellen_wizard)
    self.spinbox_kommastellen_wizard = create_new_spinbox(self.widget_kommastellen_wizard)
    self.spinbox_kommastellen_wizard.setMaximum(14)
    self.spinbox_kommastellen_wizard.valueChanged.connect(self.worksheet_wizard_setting_changed)
    self.horizontalLayout_kommastellen_wizard.addWidget(self.spinbox_kommastellen_wizard)

    self.gridLayout_zahlenbereich_wizard.setColumnStretch(4, 1)

    self.checkbox_negative_ergebnisse_wizard = create_new_checkbox(self.groupBox_zahlenbereich_wizard, "negative Ergebnisse erlauben")
    self.checkbox_negative_ergebnisse_wizard.stateChanged.connect(self.worksheet_wizard_setting_changed)
    self.gridLayout_zahlenbereich_wizard.addWidget(self.checkbox_negative_ergebnisse_wizard, 3,0,1,2)
    self.checkbox_negative_ergebnisse_wizard.hide()

    self.checkbox_allow_brackets_wizard = create_new_checkbox(self.groupBox_zahlenbereich_wizard, "Klammern erlauben")
    self.checkbox_allow_brackets_wizard.stateChanged.connect(self.worksheet_wizard_setting_changed)
    self.gridLayout_zahlenbereich_wizard.addWidget(self.checkbox_allow_brackets_wizard, 3,0,1,2)
    self.checkbox_allow_brackets_wizard.hide()


    self.groupBox_first_number_wizard = create_new_groupbox(self.groupBox_zahlenbereich_wizard, "1. Faktor")
    self.gridLayout_zahlenbereich_wizard.addWidget(self.groupBox_first_number_wizard, 0,0,1,1)

    self.verticalLayout_first_number_wizard = create_new_verticallayout(self.groupBox_first_number_wizard)
    # self.gridLayout_first_number_wizard = create_new_gridlayout(self.groupBox_first_number_wizard)

    self.widget_first_number_min_wizard = QtWidgets.QWidget(self.groupBox_first_number_wizard)
    self.verticalLayout_first_number_wizard.addWidget(self.widget_first_number_min_wizard)
    
    self.horizontalLayout_widget_first_number_min_wizard = create_new_horizontallayout(self.widget_first_number_min_wizard)
    self.horizontalLayout_widget_first_number_min_wizard.setContentsMargins(0,0,0,0)


    self.label_first_number_min = create_new_label(self.widget_first_number_min_wizard, "Min:")
    self.horizontalLayout_widget_first_number_min_wizard.addWidget(self.label_first_number_min)
    self.spinBox_first_number_min = create_new_spinbox(self.groupBox_first_number_wizard)
    self.spinBox_first_number_min.setRange(0,999999999)
    self.spinBox_first_number_min.setValue(10)
    self.horizontalLayout_widget_first_number_min_wizard.addWidget(self.spinBox_first_number_min)



    self.widget_first_number_max_wizard = QtWidgets.QWidget(self.groupBox_first_number_wizard)
    self.verticalLayout_first_number_wizard.addWidget(self.widget_first_number_max_wizard)
    
    self.horizontalLayout_widget_first_number_max_wizard = create_new_horizontallayout(self.widget_first_number_max_wizard)
    self.horizontalLayout_widget_first_number_max_wizard.setContentsMargins(0,0,0,0)


    self.label_first_number_max = create_new_label(self.widget_first_number_max_wizard, "Max:")
    self.horizontalLayout_widget_first_number_max_wizard.addWidget(self.label_first_number_max)
    self.spinBox_first_number_max = create_new_spinbox(self.groupBox_first_number_wizard)
    self.spinBox_first_number_max.setRange(0,999999999)
    self.spinBox_first_number_max.setValue(99)
    self.horizontalLayout_widget_first_number_max_wizard.addWidget(self.spinBox_first_number_max)

    self.spinBox_first_number_max.valueChanged.connect(self.worksheet_wizard_setting_changed)
    self.spinBox_first_number_min.valueChanged.connect(partial(self.minimum_changed_wizard, self.spinBox_first_number_min, self.spinBox_first_number_max))        



    self.widget_first_number_decimal = QtWidgets.QWidget(self.groupBox_first_number_wizard)
    self.verticalLayout_first_number_wizard.addWidget(self.widget_first_number_decimal)

    self.horizontalLayout_widget_first_number_decimal = create_new_horizontallayout(self.widget_first_number_decimal)
    self.horizontalLayout_widget_first_number_decimal.setContentsMargins(0,0,0,0)


    self.label_first_number_decimal = create_new_label(self.groupBox_first_number_wizard, "Kommastellen:")
    self.horizontalLayout_widget_first_number_decimal.addWidget(self.label_first_number_decimal)

    self.combobox_first_number_decimal = create_new_combobox(self.groupBox_first_number_wizard)
    add_new_option(self.combobox_first_number_decimal, 0, "=")
    add_new_option(self.combobox_first_number_decimal, 1, "\u2264")
    self.combobox_first_number_decimal.currentIndexChanged.connect(self.worksheet_wizard_setting_changed)
    self.horizontalLayout_widget_first_number_decimal.addWidget(self.combobox_first_number_decimal)
    self.spinBox_first_number_decimal = create_new_spinbox(self.groupBox_first_number_wizard)
    self.spinBox_first_number_decimal.setMaximum(14)
    self.spinBox_first_number_decimal.valueChanged.connect(self.worksheet_wizard_setting_changed)
    self.horizontalLayout_widget_first_number_decimal.addWidget(self.spinBox_first_number_decimal)  
    self.groupBox_first_number_wizard.hide()




    self.groupBox_second_number_wizard = create_new_groupbox(self.groupBox_zahlenbereich_wizard, "2. Faktor")
    self.gridLayout_zahlenbereich_wizard.addWidget(self.groupBox_second_number_wizard, 0,1,1,1)

    self.verticalLayout_second_number_wizard = create_new_verticallayout(self.groupBox_second_number_wizard)
    # self.gridLayout_second_number_wizard = create_new_gridlayout(self.groupBox_second_number_wizard)

    self.widget_second_number_min_wizard = QtWidgets.QWidget(self.groupBox_second_number_wizard)
    self.verticalLayout_second_number_wizard.addWidget(self.widget_second_number_min_wizard)
    
    self.horizontalLayout_widget_second_number_min_wizard = create_new_horizontallayout(self.widget_second_number_min_wizard)
    self.horizontalLayout_widget_second_number_min_wizard.setContentsMargins(0,0,0,0)


    self.label_second_number_min = create_new_label(self.widget_second_number_min_wizard, "Min:")
    self.horizontalLayout_widget_second_number_min_wizard.addWidget(self.label_second_number_min)
    self.spinBox_second_number_min = create_new_spinbox(self.groupBox_second_number_wizard)
    self.spinBox_second_number_min.setRange(0,999999999)
    self.spinBox_second_number_min.setValue(10)
    self.horizontalLayout_widget_second_number_min_wizard.addWidget(self.spinBox_second_number_min)



    self.widget_second_number_max_wizard = QtWidgets.QWidget(self.groupBox_second_number_wizard)
    self.verticalLayout_second_number_wizard.addWidget(self.widget_second_number_max_wizard)
    
    self.horizontalLayout_widget_second_number_max_wizard = create_new_horizontallayout(self.widget_second_number_max_wizard)
    self.horizontalLayout_widget_second_number_max_wizard.setContentsMargins(0,0,0,0)


    self.label_second_number_max = create_new_label(self.widget_second_number_max_wizard, "Max:")
    self.horizontalLayout_widget_second_number_max_wizard.addWidget(self.label_second_number_max)
    self.spinBox_second_number_max = create_new_spinbox(self.groupBox_second_number_wizard)
    self.spinBox_second_number_max.setRange(0,999999999)
    self.spinBox_second_number_max.setValue(99)
    self.horizontalLayout_widget_second_number_max_wizard.addWidget(self.spinBox_second_number_max)

    self.spinBox_second_number_max.valueChanged.connect(self.worksheet_wizard_setting_changed)
    self.spinBox_second_number_min.valueChanged.connect(partial(self.minimum_changed_wizard, self.spinBox_second_number_min, self.spinBox_second_number_max))        



    self.widget_second_number_decimal = QtWidgets.QWidget(self.groupBox_second_number_wizard)
    self.verticalLayout_second_number_wizard.addWidget(self.widget_second_number_decimal)

    self.horizontalLayout_widget_second_number_decimal = create_new_horizontallayout(self.widget_second_number_decimal)
    self.horizontalLayout_widget_second_number_decimal.setContentsMargins(0,0,0,0)


    self.label_second_number_decimal = create_new_label(self.groupBox_second_number_wizard, "Kommastellen:")
    self.horizontalLayout_widget_second_number_decimal.addWidget(self.label_second_number_decimal)

    self.combobox_second_number_decimal = create_new_combobox(self.groupBox_second_number_wizard)
    add_new_option(self.combobox_second_number_decimal, 0, "=")
    add_new_option(self.combobox_second_number_decimal, 1, "\u2264")
    self.combobox_second_number_decimal.currentIndexChanged.connect(self.worksheet_wizard_setting_changed)
    self.horizontalLayout_widget_second_number_decimal.addWidget(self.combobox_second_number_decimal)
    self.spinBox_second_number_decimal = create_new_spinbox(self.groupBox_second_number_wizard)
    self.spinBox_second_number_decimal.setMaximum(14)
    self.spinBox_second_number_decimal.valueChanged.connect(self.worksheet_wizard_setting_changed)
    self.horizontalLayout_widget_second_number_decimal.addWidget(self.spinBox_second_number_decimal)  
    self.groupBox_second_number_wizard.hide()



    ##### Division ########

    self.groupBox_dividend_wizard = create_new_groupbox(self.groupBox_zahlenbereich_wizard, "Dividend")
    self.gridLayout_dividend_wizard = create_new_gridlayout(self.groupBox_dividend_wizard)
    self.gridLayout_zahlenbereich_wizard.addWidget(self.groupBox_dividend_wizard, 0,0, 1,1)

    self.combobox_dividend_wizard = create_new_combobox(self.groupBox_dividend_wizard)
    add_new_option(self.combobox_dividend_wizard, 0, "Natürliche Zahl")
    add_new_option(self.combobox_dividend_wizard, 1, "Dezimalzahl")
    self.gridLayout_dividend_wizard.addWidget(self.combobox_dividend_wizard, 0,0,1,1)

    self.label_dividend_min_wizard = create_new_label(self.groupBox_dividend_wizard, "Min:")
    self.gridLayout_dividend_wizard.addWidget(self.label_dividend_min_wizard, 0,1,1,1)
    self.spinbox_dividend_min_wizard = create_new_spinbox(self.groupBox_dividend_wizard)
    self.spinbox_dividend_min_wizard.setMaximum(999999999)
    self.spinbox_dividend_min_wizard.setValue(100)
    self.spinbox_dividend_min_wizard.valueChanged.connect(self.worksheet_wizard_setting_changed)
    self.gridLayout_dividend_wizard.addWidget(self.spinbox_dividend_min_wizard, 0,2,1,1)
    

    self.label_dividend_max_wizard = create_new_label(self.groupBox_dividend_wizard, "Max:")
    self.gridLayout_dividend_wizard.addWidget(self.label_dividend_max_wizard, 1,1,1,1)
    self.spinbox_dividend_max_wizard = create_new_spinbox(self.groupBox_dividend_wizard)
    self.spinbox_dividend_max_wizard.setMaximum(999999999)
    self.spinbox_dividend_max_wizard.setValue(1000)
    self.spinbox_dividend_max_wizard.valueChanged.connect(self.worksheet_wizard_setting_changed)
    self.gridLayout_dividend_wizard.addWidget(self.spinbox_dividend_max_wizard, 1,2,1,1)
    self.groupBox_dividend_wizard.hide()


    self.groupBox_divisor_wizard = create_new_groupbox(self.groupBox_zahlenbereich_wizard, "Divisor")
    self.gridLayout_divisor_wizard = create_new_gridlayout(self.groupBox_divisor_wizard)
    self.gridLayout_zahlenbereich_wizard.addWidget(self.groupBox_divisor_wizard, 0,1, 1,1)

    self.combobox_divisor_wizard = create_new_combobox(self.groupBox_divisor_wizard)
    add_new_option(self.combobox_divisor_wizard, 0, "Natürliche Zahl")
    add_new_option(self.combobox_divisor_wizard, 1, "Dezimalzahl")
    self.gridLayout_divisor_wizard.addWidget(self.combobox_divisor_wizard, 0,0,1,3)

    self.label_divisor_kommastelle_wizard = create_new_label(self.groupBox_divisor_wizard, "Kommastellen")
    self.gridLayout_divisor_wizard.addWidget(self.label_divisor_kommastelle_wizard, 1,0,1,1)

    self.combobox_divisor_kommastelle_wizard = create_new_combobox(self.combobox_divisor_wizard)
    add_new_option(self.combobox_divisor_kommastelle_wizard, 0, "=")
    add_new_option(self.combobox_divisor_kommastelle_wizard, 1, "\u2264")
    self.combobox_divisor_kommastelle_wizard.currentIndexChanged.connect(self.worksheet_wizard_setting_changed)
    self.gridLayout_divisor_wizard.addWidget(self.combobox_divisor_kommastelle_wizard, 1,1,1,1)
    self.spinBox_divisor_kommastellen_wizard = create_new_spinbox(self.groupBox_divisor_wizard, 0)
    self.spinBox_divisor_kommastellen_wizard.setMaximum(14)
    self.spinBox_divisor_kommastellen_wizard.valueChanged.connect(self.worksheet_wizard_setting_changed)
    self.gridLayout_divisor_wizard.addWidget(self.spinBox_divisor_kommastellen_wizard, 1,2,1,1)
    self.label_divisor_kommastelle_wizard.hide()
    self.combobox_divisor_kommastelle_wizard.hide()
    self.spinBox_divisor_kommastellen_wizard.hide()

    self.label_divisor_min_wizard = create_new_label(self.groupBox_divisor_wizard, "Min:")
    self.gridLayout_divisor_wizard.addWidget(self.label_divisor_min_wizard, 0,3,1,1)
    self.spinbox_divisor_min_wizard = create_new_spinbox(self.groupBox_divisor_wizard, 2)
    self.spinbox_divisor_min_wizard.setMaximum(999999999)
    self.spinbox_divisor_min_wizard.valueChanged.connect(self.worksheet_wizard_setting_changed)
    self.gridLayout_divisor_wizard.addWidget(self.spinbox_divisor_min_wizard, 0,4,1,1)
    

    self.label_divisor_max_wizard = create_new_label(self.groupBox_divisor_wizard, "Max:")
    self.gridLayout_divisor_wizard.addWidget(self.label_divisor_max_wizard, 1,3,1,1)
    self.spinbox_divisor_max_wizard = create_new_spinbox(self.groupBox_divisor_wizard, 99)
    self.spinbox_divisor_max_wizard.setMaximum(999999999)
    self.spinbox_divisor_max_wizard.valueChanged.connect(self.worksheet_wizard_setting_changed)
    self.gridLayout_divisor_wizard.addWidget(self.spinbox_divisor_max_wizard, 1,4,1,1)
    self.groupBox_divisor_wizard.hide()


    self.groupBox_ergebnis_wizard = create_new_groupbox(self.widgetZahlenbereich_anzahl, "Ergebnis")
    self.gridLayout_zahlenbereich_wizard.addWidget(self.groupBox_ergebnis_wizard, 2,0,1,1)
    self.horizontalLayout_ergebnis_wizard = create_new_horizontallayout(self.groupBox_ergebnis_wizard)

    self.radioButton_division_ohne_rest = create_new_radiobutton(self.groupBox_ergebnis_wizard, "ohne Rest")
    self.radioButton_division_ohne_rest.setChecked(True)
    self.radioButton_division_ohne_rest.toggled.connect(self.worksheet_wizard_setting_changed)
    self.horizontalLayout_ergebnis_wizard.addWidget(self.radioButton_division_ohne_rest)

    self.radioButton_division_rest = create_new_radiobutton(self.groupBox_ergebnis_wizard, "mit Rest")
    self.radioButton_division_rest.toggled.connect(self.worksheet_wizard_setting_changed)
    self.horizontalLayout_ergebnis_wizard.addWidget(self.radioButton_division_rest)



    self.label_ergebnis_kommastellen_wizard = create_new_label(self.groupBox_ergebnis_wizard, "Kommastellen:")
    self.horizontalLayout_ergebnis_wizard.addWidget(self.label_ergebnis_kommastellen_wizard)
    self.combobox_ergebnis_kommastellen_wizard = create_new_combobox(self.groupBox_ergebnis_wizard)
    add_new_option(self.combobox_ergebnis_kommastellen_wizard, 0, "=")
    add_new_option(self.combobox_ergebnis_kommastellen_wizard, 1, "\u2264")
    self.combobox_ergebnis_kommastellen_wizard.currentIndexChanged.connect(self.worksheet_wizard_setting_changed)
    self.horizontalLayout_ergebnis_wizard.addWidget(self.combobox_ergebnis_kommastellen_wizard)
    self.spinbox_ergebnis_kommastellen_wizard = create_new_spinbox(self.groupBox_ergebnis_wizard, 1)
    self.spinbox_ergebnis_kommastellen_wizard.setRange(1,14)
    self.spinbox_ergebnis_kommastellen_wizard.valueChanged.connect(self.worksheet_wizard_setting_changed)
    self.horizontalLayout_ergebnis_wizard.addWidget(self.spinbox_ergebnis_kommastellen_wizard)

    self.label_ergebnis_kommastellen_wizard.hide()
    self.combobox_ergebnis_kommastellen_wizard.hide()
    self.spinbox_ergebnis_kommastellen_wizard.hide()
    self.horizontalLayout_ergebnis_wizard.addStretch()

    self.combobox_dividend_wizard.currentIndexChanged.connect(self.combobox_divisor_dividend_changed)
    self.combobox_divisor_wizard.currentIndexChanged.connect(self.combobox_divisor_dividend_changed)
    self.groupBox_ergebnis_wizard.hide()


    #### Binomische Formeln ###

    # self.groupbox_binoms_combobox_mode = create_new_combobox(self.groupBox_zahlenbereich_wizard)
    # self.gridLayout_zahlenbereich_wizard.addWidget(self.groupbox_binoms_types, 0,3, 1,1)

    # add_new_option(self.groupbox_binoms_combobox_mode, 0, "Zahl +")


    self.groupbox_binoms_types = create_new_groupbox(self.groupBox_zahlenbereich_wizard, "Typen")
    self.vertical_binoms_types = create_new_verticallayout(self.groupbox_binoms_types)
    self.gridLayout_zahlenbereich_wizard.addWidget(self.groupbox_binoms_types, 0,0, 2,1)

    self.cb_binoms_1 = create_new_checkbox(self.groupbox_binoms_types, "(a + b)²", checked=True)
    self.vertical_binoms_types.addWidget(self.cb_binoms_1)

    self.cb_binoms_2 = create_new_checkbox(self.groupbox_binoms_types, "(a - b)²", checked=True)
    self.vertical_binoms_types.addWidget(self.cb_binoms_2)

    self.cb_binoms_3 = create_new_checkbox(self.groupbox_binoms_types, "(a + b)(a - b)", checked=True)
    self.vertical_binoms_types.addWidget(self.cb_binoms_3)
    self.groupbox_binoms_types.hide()


    self.widget_binoms_set_variables_factors = QtWidgets.QWidget(self.groupBox_zahlenbereich_wizard)
    self.gridLayout_zahlenbereich_wizard.addWidget(self.widget_binoms_set_variables_factors, 1,1, 1,1)
    
    self.gridlayout_binoms_set_variables = create_new_gridlayout(self.widget_binoms_set_variables_factors)
    self.gridlayout_binoms_set_variables.setContentsMargins(9,0,9,9)
    self.label_binoms_von = create_new_label(self.widget_binoms_set_variables_factors, "von")
    self.gridlayout_binoms_set_variables.addWidget(self.label_binoms_von, 1,2,1,1, QtCore.Qt.AlignCenter)

    self.label_binoms_bis = create_new_label(self.widget_binoms_set_variables_factors, "bis")
    self.gridlayout_binoms_set_variables.addWidget(self.label_binoms_bis, 1,4,1,1, QtCore.Qt.AlignCenter)


    self.checkbox_binoms_a = create_new_checkbox(self.widget_binoms_set_variables_factors, " ", checked=True)
    self.gridlayout_binoms_set_variables.addWidget(self.checkbox_binoms_a, 2,0,1,1)

    self.label_binoms_a = create_new_label(self.widget_binoms_set_variables_factors, "a =")
    self.gridlayout_binoms_set_variables.addWidget(self.label_binoms_a, 2,1,1,1)

    self.spinbox_binoms_a_min = create_new_spinbox(self.widget_binoms_set_variables_factors, value=1)
    self.spinbox_binoms_a_min.setRange(-99,10)
    self.gridlayout_binoms_set_variables.addWidget(self.spinbox_binoms_a_min, 2,2,1,1)

    self.label_binoms_a_to = create_new_label(self.widget_binoms_set_variables_factors, " - ")
    self.gridlayout_binoms_set_variables.addWidget(self.label_binoms_a_to, 2,3,1,1)

    self.spinbox_binoms_a_max = create_new_spinbox(self.widget_binoms_set_variables_factors, value=10)
    self.spinbox_binoms_a_max.setRange(-99,99)
    self.spinbox_binoms_a_max.valueChanged.connect(lambda: self.spinbox_binoms_a_min.setMaximum(self.spinbox_binoms_a_max.value()))
    self.gridlayout_binoms_set_variables.addWidget(self.spinbox_binoms_a_max, 2,4,1,1)

    self.checkbox_binoms_a.stateChanged.connect(self.checkbox_binoms_a_state_changed)

    self.checkbox_binoms_b = create_new_checkbox(self.widget_binoms_set_variables_factors, " ", checked=True)
    self.gridlayout_binoms_set_variables.addWidget(self.checkbox_binoms_b, 3,0,1,1)

    self.label_binoms_b = create_new_label(self.widget_binoms_set_variables_factors, "b =")
    self.gridlayout_binoms_set_variables.addWidget(self.label_binoms_b, 3,1,1,1)

    self.spinbox_binoms_b_min = create_new_spinbox(self.widget_binoms_set_variables_factors, value=1)
    self.spinbox_binoms_b_min.setRange(-99,10)
    self.gridlayout_binoms_set_variables.addWidget(self.spinbox_binoms_b_min, 3,2,1,1)

    self.label_binoms_b_to = create_new_label(self.widget_binoms_set_variables_factors, " - ")
    self.gridlayout_binoms_set_variables.addWidget(self.label_binoms_b_to, 3,3,1,1)

    self.spinbox_binoms_b_max = create_new_spinbox(self.widget_binoms_set_variables_factors, value=10)
    self.spinbox_binoms_b_max.setRange(-99,99)
    self.spinbox_binoms_b_max.valueChanged.connect(lambda: self.spinbox_binoms_b_min.setMaximum(self.spinbox_binoms_b_max.value()))
    self.gridlayout_binoms_set_variables.addWidget(self.spinbox_binoms_b_max, 3,4,1,1)

    self.checkbox_binoms_b.stateChanged.connect(self.checkbox_binoms_b_state_changed)

    self.widget_binoms_set_variables_factors.hide()

    self.widget_binoms_set_variables_exponents = QtWidgets.QWidget(self.groupBox_zahlenbereich_wizard)
    self.gridLayout_zahlenbereich_wizard.addWidget(self.widget_binoms_set_variables_exponents, 1,2, 1,1)
    
    self.gridlayout_binoms_set_exponents= create_new_gridlayout(self.widget_binoms_set_variables_exponents)
    self.gridlayout_binoms_set_exponents.setContentsMargins(9,0,9,9)
    self.label_binoms_von = create_new_label(self.widget_binoms_set_variables_exponents, "von")
    self.gridlayout_binoms_set_exponents.addWidget(self.label_binoms_von, 1,2,1,1, QtCore.Qt.AlignCenter)

    self.label_binoms_bis = create_new_label(self.widget_binoms_set_variables_exponents, "bis")
    self.gridlayout_binoms_set_exponents.addWidget(self.label_binoms_bis, 1,4,1,1, QtCore.Qt.AlignCenter)



    self.label_binoms_m = create_new_label(self.widget_binoms_set_variables_exponents, "m =")
    self.gridlayout_binoms_set_exponents.addWidget(self.label_binoms_m, 2,1,1,1)

    self.spinbox_binoms_m_min = create_new_spinbox(self.widget_binoms_set_variables_exponents, value=1)
    self.spinbox_binoms_m_min.setRange(1,1)

    self.gridlayout_binoms_set_exponents.addWidget(self.spinbox_binoms_m_min, 2,2,1,1)

    self.label_binoms_m_to = create_new_label(self.widget_binoms_set_variables_exponents, " - ")
    self.gridlayout_binoms_set_exponents.addWidget(self.label_binoms_m_to, 2,3,1,1)

    self.spinbox_binoms_m_max = create_new_spinbox(self.widget_binoms_set_variables_exponents, value=1)
    self.spinbox_binoms_m_max.setRange(1,9)
    self.spinbox_binoms_m_max.valueChanged.connect(lambda: self.spinbox_binoms_m_min.setMaximum(self.spinbox_binoms_m_max.value()))
    self.gridlayout_binoms_set_exponents.addWidget(self.spinbox_binoms_m_max, 2,4,1,1)


    self.checkbox_binoms_y = create_new_checkbox(self.widget_binoms_set_variables_factors, "y: ", checked=True)
    self.gridlayout_binoms_set_exponents.addWidget(self.checkbox_binoms_y, 3,0,1,1)

    self.label_binoms_n = create_new_label(self.widget_binoms_set_variables_exponents, "n =")
    self.gridlayout_binoms_set_exponents.addWidget(self.label_binoms_n, 3,1,1,1)

    self.spinbox_binoms_n_min = create_new_spinbox(self.widget_binoms_set_variables_exponents, value=1)
    self.spinbox_binoms_n_min.setRange(1,1)
    self.gridlayout_binoms_set_exponents.addWidget(self.spinbox_binoms_n_min, 3,2,1,1)

    self.label_binoms_n_to = create_new_label(self.widget_binoms_set_variables_exponents, " - ")
    self.gridlayout_binoms_set_exponents.addWidget(self.label_binoms_n_to, 3,3,1,1)

    self.spinbox_binoms_n_max = create_new_spinbox(self.widget_binoms_set_variables_exponents, value=1)
    self.spinbox_binoms_n_max.setRange(1,9)
    self.spinbox_binoms_n_max.valueChanged.connect(lambda: self.spinbox_binoms_n_min.setMaximum(self.spinbox_binoms_n_max.value()))
    self.gridlayout_binoms_set_exponents.addWidget(self.spinbox_binoms_n_max, 3,4,1,1)

    self.checkbox_binoms_y.stateChanged.connect(self.checkbox_binoms_y_state_changed)
    # self.checkbox_binoms_y.stateChanged.connect(lambda: self.checkbox_enable_disable_widget(self.checkbox_binoms_y, self.spinbox_binoms_n_min))
    # self.checkbox_binoms_y.stateChanged.connect(lambda: self.checkbox_enable_disable_widget(self.checkbox_binoms_y, self.spinbox_binoms_n_max))

    self.widget_binoms_set_variables_exponents.hide()


    self.label_binom_example = create_new_label(self.groupBox_zahlenbereich_wizard, "")
    self.label_binom_example.setFont(QtGui.QFont("IBM Plex Sans", 12))
    self.gridLayout_zahlenbereich_wizard.addWidget(self.label_binom_example, 0,1, 1,2, QtCore.Qt.AlignCenter)

    self.label_binom_example.hide()

    self.widget_binom_further_settings = QtWidgets.QWidget(self.groupBox_zahlenbereich_wizard)
    self.gridLayout_zahlenbereich_wizard.addWidget(self.widget_binom_further_settings, 0,3, 3,1)
    self.verticallayout_binom_further_settings = create_new_verticallayout(self.widget_binom_further_settings)

    self.widget_binoms_exponent = QtWidgets.QWidget(self.widget_binom_further_settings)
    self.verticallayout_binom_further_settings.addWidget(self.widget_binoms_exponent)

    self.horizontallayout_binoms_exponent = create_new_horizontallayout(self.widget_binoms_exponent)
    self.horizontallayout_binoms_exponent.setContentsMargins(12,0,0,0)    

    self.label_binoms_exponent = create_new_label(self.widget_binoms_exponent, "Exponent:")
    self.horizontallayout_binoms_exponent.addWidget(self.label_binoms_exponent)

    self.spinbox_binoms_exponent = create_new_spinbox(self.widget_binoms_exponent, value = 2)
    self.spinbox_binoms_exponent.valueChanged.connect(self.binom_update_label)
    self.spinbox_binoms_exponent.setRange(2,9)
    # self.spinbox_binoms_exponent.setSizePolicy(SizePolicy_maximum)
    self.horizontallayout_binoms_exponent.addWidget(self.spinbox_binoms_exponent)
    self.horizontallayout_binoms_exponent.addStretch()

    self.widget_binoms_direction = QtWidgets.QWidget(self.widget_binom_further_settings)
    self.verticallayout_binom_further_settings.addWidget(self.widget_binoms_direction)

    self.horizontallayout_binoms_direction = create_new_horizontallayout(self.widget_binoms_direction)
    self.horizontallayout_binoms_direction.setContentsMargins(12,0,0,0)

    self.label_binoms_direction_1 = create_new_label(self.widget_binoms_direction, "(a \u00B1 b)<sup>2</sup>")
    self.horizontallayout_binoms_direction.addWidget(self.label_binoms_direction_1)


    self.binoms_direction_index = 0
    self.pushbutton_binoms_direction = create_new_button(self.widget_binoms_direction, "", self.binoms_direction_changed, "chevron-right.svg")
    self.horizontallayout_binoms_direction.addWidget(self.pushbutton_binoms_direction)
    

    self.label_binoms_direction_2 = create_new_label(self.widget_binoms_direction, "a<sup>2</sup> \u00B1 2ab + b<sup>2</sup>")
    self.horizontallayout_binoms_direction.addWidget(self.label_binoms_direction_2)  

    self.checkbox_binoms_enable_fraction = create_new_checkbox(self.widget_binom_further_settings, "Brüche erlauben")
    self.verticallayout_binom_further_settings.addWidget(self.checkbox_binoms_enable_fraction)

    self.widget_choose_variables = QtWidgets.QWidget(self.widget_binom_further_settings)
    self.verticallayout_binom_further_settings.addWidget(self.widget_choose_variables)
    self.horizontallayout_choose_variables = create_new_horizontallayout(self.widget_choose_variables)

    self.label_choose_variables = create_new_label(self.widget_choose_variables, "Variablen:")
    self.horizontallayout_choose_variables.addWidget(self.label_choose_variables)

    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    self.combobox_choose_variables_1 = create_new_combobox(self.widget_choose_variables)
    self.horizontallayout_choose_variables.addWidget(self.combobox_choose_variables_1)
    add_new_option(self.combobox_choose_variables_1, 0, "")

    self.combobox_choose_variables_2 = create_new_combobox(self.widget_choose_variables)
    self.horizontallayout_choose_variables.addWidget(self.combobox_choose_variables_2)
    add_new_option(self.combobox_choose_variables_2, 0, "")
    
    i=1
    for all in alphabet:
        add_new_option(self.combobox_choose_variables_1, i, all)
        add_new_option(self.combobox_choose_variables_2, i, all)
        i +=1


    self.widget_binom_further_settings.hide()

    self.binom_update_label()
    ####################################################
    ######################################################
    #######################################################

    self.widget_buttons_create_new_examples = QtWidgets.QWidget(self.groupBox_setting_wizard)
    self.verticalLayout_setting_wizard.addWidget(self.widget_buttons_create_new_examples)
    
    self.horizontalLayout_buttons_create_new_examples = create_new_horizontallayout(self.widget_buttons_create_new_examples)
    self.horizontalLayout_buttons_create_new_examples.setContentsMargins(0,0,0,0)

    self.pushButton_calculate_new_examples = create_new_button(
        self.widget_buttons_create_new_examples,
        f"{self.spinBox_number_wizard.value()} neue Aufgaben berechnen",
        self.create_new_worksheet_wizard_pressed, 
        icon="activity.svg"
    )
    self.horizontalLayout_buttons_create_new_examples.addWidget(self.pushButton_calculate_new_examples)

    self.pushButton_add_single_example = create_new_button(
        self.widget_buttons_create_new_examples,
        "Einzelaufgabe",
        self.add_single_example_wizard,
        icon="plus-square.svg",
    )
    self.horizontalLayout_buttons_create_new_examples.addWidget(self.pushButton_add_single_example)

    self.horizontalLayout_buttons_create_new_examples.addStretch() 
    # self.pushButton_calculate_new_examples.setSizePolicy(SizePolicy_fixed)
    
    # self.verticalLayout_setting_wizard.addWidget(self.pushButton_calculate_new_examples, alignment=QtCore.Qt.AlignRight)

    # self.buttonBox_addto_worksheet_wizard = QtWidgets.QDialogButtonBox(self.widgetNewExamples_wizard)
    # self.buttonBox_addto_worksheet_wizard.setStandardButtons(
    #     QtWidgets.QDialogButtonBox.Ok
    # )
    # self.verticalLayout_newexamples_wizard.addWidget(self.buttonBox_addto_worksheet_wizard)


    # button_addto = self.buttonBox_addto_worksheet_wizard.button(QtWidgets.QDialogButtonBox.Ok)
    # button_addto.setText("Aufgaben zum Arbeitsblatt hinzufügen")
    # button_addto.setIcon(QtGui.QIcon(get_icon_path('plus-square.svg')))

    # button_addto.clicked.connect(still_to_define)
    # self.gridLayout_zahlenbereich_wizard.setRowStretch(4,1)
    # self.gridLayout_setting_wizard.setRowStretch(3, 2)





    self.widgetNewWorksheet_wizard = QtWidgets.QWidget(self.stackWizard)
#     self.widgetNewWorksheet_wizard.setSizePolicy(QtWidgets.QSizePolicy(
#     QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
# ))
    self.verticalLayout_stackWidget.addWidget(self.widgetNewWorksheet_wizard)

    self.horizontalLayout_newexamples = create_new_horizontallayout(self.widgetNewWorksheet_wizard)    



    self.splitter_newWorksheet = QtWidgets.QSplitter(self.widgetNewWorksheet_wizard)
    self.splitter_newWorksheet.setOrientation(QtCore.Qt.Horizontal)
    self.splitter_newWorksheet.setObjectName("splitter_newWorksheet")
    self.horizontalLayout_newexamples.addWidget(self.splitter_newWorksheet)


    self.widgetNewExamples_wizard = QtWidgets.QWidget(self.splitter_newWorksheet)
    # self.horizontalLayout_newexamples.addWidget(self.widgetNewExamples_wizard)
    self.verticalLayout_newexamples_wizard = create_new_verticallayout(self.widgetNewExamples_wizard)
    self.verticalLayout_newexamples_wizard.setContentsMargins(0,9,0,0)

    self.scrollArea_chosen_wizard = QtWidgets.QScrollArea(self.widgetNewExamples_wizard)
    # self.scrollArea_chosen_wizard.setFrameShape(QtWidgets.QFrame.StyledPanel)
    self.scrollArea_chosen_wizard.setWidgetResizable(True)
    self.scrollArea_chosen_wizard.setObjectName("scrollArea_chosen_wizard")
    self.scrollArea_chosen_wizard.setFocusPolicy(QtCore.Qt.ClickFocus)
    # self.scrollArea_chosen_wizard.setSizePolicy(SizePolicy_minimum)
    self.scrollAreaWidgetContents_wizard = QtWidgets.QWidget()
    self.scrollAreaWidgetContents_wizard.setObjectName("scrollAreaWidgetContents_wizard")
    self.scrollAreaWidgetContents_wizard.setFocusPolicy(QtCore.Qt.ClickFocus)
    self.gridLayout_scrollArea_wizard = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_wizard)
    self.gridLayout_scrollArea_wizard.setObjectName("gridLayout_scrollArea_wizard")
    self.scrollArea_chosen_wizard.setWidget(self.scrollAreaWidgetContents_wizard)
    self.scrollArea_chosen_wizard.verticalScrollBar().rangeChanged.connect(
        self.change_scrollbar_position
    )
    self.verticalLayout_newexamples_wizard.addWidget(self.scrollArea_chosen_wizard)

    self.buttonBox_addto_worksheet_wizard = QtWidgets.QDialogButtonBox(self.widgetNewExamples_wizard)
    self.buttonBox_addto_worksheet_wizard.setStandardButtons(
        QtWidgets.QDialogButtonBox.Ok
    )
    self.verticalLayout_newexamples_wizard.addWidget(self.buttonBox_addto_worksheet_wizard)


    self.pushButton_addto_worksheet_wizard = self.buttonBox_addto_worksheet_wizard.button(QtWidgets.QDialogButtonBox.Ok)
    self.pushButton_addto_worksheet_wizard.setText("Alle Aufgaben zum Arbeitsblatt hinzufügen")
    self.pushButton_addto_worksheet_wizard.setIcon(QtGui.QIcon(get_icon_path('chevrons-right.svg')))
    self.pushButton_addto_worksheet_wizard.setEnabled(False)

    self.pushButton_addto_worksheet_wizard.clicked.connect(self.add_to_worksheet_wizard)


    self.groupBox_complete_worksheet_wizard = create_new_groupbox(self.splitter_newWorksheet, "Arbeitsblatt")
    # self.horizontalLayout_newexamples.addWidget(self.groupBox_complete_worksheet_wizard)

    self.horizontalLayout_worksheet_wizard = create_new_horizontallayout(self.groupBox_complete_worksheet_wizard)

    self.scrollArea_complete_worksheet_wizard = QtWidgets.QScrollArea(self.groupBox_complete_worksheet_wizard)
    self.scrollArea_complete_worksheet_wizard.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
    # self.scrollArea_chosen_wizard.setFrameShape(QtWidgets.QFrame.StyledPanel)
    self.scrollArea_complete_worksheet_wizard.setWidgetResizable(True)
    self.scrollArea_complete_worksheet_wizard.setObjectName("scrollArea_complete_worksheet_wizard")
    self.scrollArea_complete_worksheet_wizard.setFocusPolicy(QtCore.Qt.ClickFocus)
    # self.scrollArea_complete_worksheet_wizard.setSizePolicy(SizePolicy_minimum)
    self.scrollAreaWidgetContents_complete_worksheet_wizard = DragDropWidget(self,None)
    self.scrollAreaWidgetContents_complete_worksheet_wizard.setObjectName("scrollAreaWidgetContents_complete_worksheet_wizard")
    self.scrollAreaWidgetContents_complete_worksheet_wizard.setFocusPolicy(QtCore.Qt.ClickFocus)

    self.verticalLayout_complete_worksheet_wizard = create_new_verticallayout(self.scrollAreaWidgetContents_complete_worksheet_wizard)
    self.verticalLayout_complete_worksheet_wizard.addStretch()
    # self.gridLayout_scrollArea_wizard = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_wizard)
    # self.gridLayout_scrollArea_wizard.setObjectName("gridLayout_scrollArea_wizard")
    self.scrollArea_complete_worksheet_wizard.setWidget(self.scrollAreaWidgetContents_complete_worksheet_wizard)
    self.scrollArea_complete_worksheet_wizard.verticalScrollBar().rangeChanged.connect(
        self.change_scrollbar_position
    )
    self.horizontalLayout_worksheet_wizard.addWidget(self.scrollArea_complete_worksheet_wizard)




    self.widgetWorksheetView = QtWidgets.QWidget(self.stackWizard)
    self.widgetWorksheetView.setSizePolicy(SizePolicy_fixed_height)
    self.verticalLayout_stackWidget.addWidget(self.widgetWorksheetView)

    self.horizontalLayout_worksheetview = create_new_horizontallayout(self.widgetWorksheetView)
    self.horizontalLayout_worksheetview.setContentsMargins(0,0,0,0)
    self.horizontalLayout_worksheetview.addStretch()



    self.widget_nummerierung_wizard = QtWidgets.QWidget(self.widgetWorksheetView)
    #create_new_groupbox(self.widgetWorksheetView, "Nummerierung")
    # self.widget_nummerierung_wizard.setSizePolicy(SizePolicy_fixed)
    self.horizontalLayout_worksheetview.addWidget(self.widget_nummerierung_wizard)
    self.horizontalLayout_worksheetview.setContentsMargins(0,0,0,0)
    # self.gridLayout_setting_wizard.addWidget(self.widget_nummerierung_wizard, 2,0,1,1)

    self.horizontalLayout_nummerierung_wizard = create_new_horizontallayout(self.widget_nummerierung_wizard)
    
    self.icon_nummerierung_wizard = create_new_label_icon(self.widget_nummerierung_wizard, icon= "hash.svg", icon_size=(15,15))
    self.horizontalLayout_nummerierung_wizard.addWidget(self.icon_nummerierung_wizard) 
    
    self.combobox_nummerierung_wizard = create_new_combobox(self.widget_nummerierung_wizard)
    add_new_option(self.combobox_nummerierung_wizard, 0, "-")
    add_new_option(self.combobox_nummerierung_wizard, 1, "(a)")
    add_new_option(self.combobox_nummerierung_wizard, 2, "(A)")
    add_new_option(self.combobox_nummerierung_wizard, 3, "(i)")
    add_new_option(self.combobox_nummerierung_wizard, 4, "(I)")
    add_new_option(self.combobox_nummerierung_wizard, 5, "(1)")
    
    
    self.horizontalLayout_nummerierung_wizard.addWidget(self.combobox_nummerierung_wizard) 


    self.widget_fontsize_wizard = QtWidgets.QWidget(self.widgetWorksheetView)
    # create_new_groupbox(self.widgetWorksheetView, "Schrift")
    # self.widget_fontsize_wizard.setSizePolicy(SizePolicy_fixed)
    self.horizontalLayout_worksheetview.addWidget(self.widget_fontsize_wizard)
    
    # self.gridLayout_setting_wizard.addWidget(self.groupBox_fontsize_wizard, 1,2,1,1)
    self.horizontalLayout_fontsize_wizard = create_new_horizontallayout(self.widget_fontsize_wizard)
    self.horizontalLayout_fontsize_wizard.setContentsMargins(0,0,0,0)

    self.icon_fontsize_wizard = create_new_label_icon(self.widget_fontsize_wizard, icon= "type.svg", icon_size=(15,15))
    self.horizontalLayout_fontsize_wizard.addWidget(self.icon_fontsize_wizard)  

    self.combobox_fontsize_wizard = create_new_combobox(self.widget_fontsize_wizard)
    add_new_option(self.combobox_fontsize_wizard, 0, "8pt")
    add_new_option(self.combobox_fontsize_wizard, 1, "9pt")
    add_new_option(self.combobox_fontsize_wizard, 2, "10pt")
    add_new_option(self.combobox_fontsize_wizard, 3, "11pt")
    add_new_option(self.combobox_fontsize_wizard, 4, "12pt")
    add_new_option(self.combobox_fontsize_wizard, 5, "14pt")
    add_new_option(self.combobox_fontsize_wizard, 6, "17pt")
    add_new_option(self.combobox_fontsize_wizard, 7, "20pt")
    self.combobox_fontsize_wizard.setCurrentIndex(4)
    self.horizontalLayout_fontsize_wizard.addWidget(self.combobox_fontsize_wizard)




    self.widget_show_nonogramm = QtWidgets.QWidget(self.widgetWorksheetView)
    # create_new_groupbox(self.groupBox_setting_wizard, "Selbstkontrolle")
    # self.groupBox_show_nonogramm.setSizePolicy(SizePolicy_fixed)
    self.horizontalLayout_worksheetview.addWidget(self.widget_show_nonogramm)
    
    # self.horizontalLayout_worksheetview.setContentsMargins(0,9,0,5)
    # self.gridLayout_setting_wizard.addWidget(self.groupBox_show_nonogramm, 4,0,1,3)
    self.horizontalLayout_show_nongramm = create_new_horizontallayout(self.widget_show_nonogramm)
    self.horizontalLayout_show_nongramm.setContentsMargins(0,0,9,0)
    self.checkBox_show_nonogramm = create_new_checkbox(self.widget_show_nonogramm, "Selbstkontrolle", True)
    self.horizontalLayout_show_nongramm.addWidget(self.checkBox_show_nonogramm)
    self.checkBox_show_nonogramm.stateChanged.connect(self.checkBox_show_nonogramm_changed) 

    self.combobox_nonogramm_wizard = create_new_combobox(self.widget_show_nonogramm)
    self.combobox_nonogramm_wizard.setToolTip("Die Zahlen in Klammer geben die Anzahl\nder Felder des Nonogramms an.")
    self.combobox_nonogramm_wizard.setStyleSheet("combobox-popup: 0;")
    self.horizontalLayout_show_nongramm.addWidget(self.combobox_nonogramm_wizard)
    self.combobox_nonogramm_wizard.currentIndexChanged.connect(self.worksheet_wizard_setting_changed)
    add_new_option(self.combobox_nonogramm_wizard, 0, 'Zufällig')
    i=1



    sorted_nonogramms = sorted(all_nonogramms.items(), key= lambda item: len(item[1]))
    for all in sorted_nonogramms:
        add_new_option(self.combobox_nonogramm_wizard, i, "{0} ({1})".format(all[0].title(), len(all[1])))
        i+=1


    self.pushButton_worksheet_instructions_wizard = create_new_button(self.widgetWorksheetView, "Layout", self.edit_worksheet_instructions, icon = "edit.svg")
    self.horizontalLayout_worksheetview.addWidget(self.pushButton_worksheet_instructions_wizard)


    self.checkbox_solutions_wizard = create_new_checkbox(self.widgetWorksheetView, "Lösungen anzeigen", checked=True)
    self.horizontalLayout_worksheetview.addWidget(self.checkbox_solutions_wizard)
    # self.gridLayout_wizard.addWidget(self.checkbox_solutions_wizard, 9,1,1,1, QtCore.Qt.AlignRight)
    # # self.checkbox_solutions_wizard.hide()


    self.comboBox_solution_type_wizard = create_new_combobox(self.stackWizard)
    add_new_option(self.comboBox_solution_type_wizard, 0, "kompakt")
    add_new_option(self.comboBox_solution_type_wizard, 1, "schrittweise")
    self.horizontalLayout_worksheetview.addWidget(self.comboBox_solution_type_wizard)

    # self.gridLayout_wizard.addWidget(self.comboBox_solution_type_wizard, 9, 0, 1, 1)
    self.comboBox_solution_type_wizard.hide()




    self.buttonBox_create_worksheet_wizard = QtWidgets.QDialogButtonBox(self.stackWizard)
    self.buttonBox_create_worksheet_wizard.setStandardButtons(
        QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Ok
    )
    self.verticalLayout_stackWidget.addWidget(self.buttonBox_create_worksheet_wizard)
    # self.gridLayout_wizard.addWidget(self.buttonBox_create_worksheet_wizard, 10,1,1,2)
    # self.buttonBox_create_worksheet_wizard.hide()

    button_create = self.buttonBox_create_worksheet_wizard.button(QtWidgets.QDialogButtonBox.Save)
    button_create.setIcon(QtGui.QIcon(get_icon_path('eye.svg')))
    button_create.setText("Vorschau")

    button_create.clicked.connect(self.create_vorschau_worksheet_wizard)

    button_save = self.buttonBox_create_worksheet_wizard.button(QtWidgets.QDialogButtonBox.Ok)
    button_save.setIcon(QtGui.QIcon(get_icon_path('save.svg')))
    button_save.setText("Speichern")


    button_save.clicked.connect(self.save_worksheet_wizard)

    










     



























    # self.pushButton_create_worksheet_wizard = create_new_button(self.stackWizard, "Neues Arbeitsblatt erzeugen", self.create_new_worksheet_wizard_pressed)
    # self.gridLayout_wizard.addWidget(self.pushButton_create_worksheet_wizard, 2,0,1,1, QtCore.Qt.AlignLeft)
    # self.pushButton_create_worksheet_wizard.hide()

    # self.pushButton_add_to_worksheet_wizard = create_new_button(self.stackWizard, "Zum bestehenden Arbeitsblatt hinzufügen", self.add_to_worksheet_wizard_pressed)
    # self.gridLayout_wizard.addWidget(self.pushButton_add_to_worksheet_wizard, 2,1,1,1, QtCore.Qt.AlignLeft)
    # self.pushButton_add_to_worksheet_wizard.hide()




