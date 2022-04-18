from PyQt5 import QtCore, QtWidgets, QtGui
from create_new_widgets import (
    add_action,
    create_new_label,
    create_new_horizontallayout,
    create_new_verticallayout,
    create_new_gridlayout,
    create_new_combobox,
    create_new_checkbox,
    create_new_button,
    create_new_groupbox,
    create_new_lineedit,
    add_new_option,
    )
from predefined_size_policy import SizePolicy_fixed_height
from config import get_icon_path, ag_beschreibung, fa_beschreibung, an_beschreibung, ws_beschreibung, zusatzthemen_beschreibung, still_to_define
from functools import partial
from create_pdf import prepare_tex_for_pdf

def setup_MenuBar(self):
    MainWindow = self.MainWindow
    self.menuBar = QtWidgets.QMenuBar(self.MainWindow)
    self.menuBar.setGeometry(QtCore.QRect(0, 0, 950, 21))
    self.menuBar.setObjectName("menuBar")

    self.menuDatei = QtWidgets.QMenu(self.menuBar)
    self.menuNeu = QtWidgets.QMenu(self.menuBar)
    self.menuChangeProgram = QtWidgets.QMenu(self.menuDatei)
    self.menuChangeProgram.setTitle("Wechseln zu ...")
    self.menuSage = QtWidgets.QMenu(self.menuBar)
    self.menuSuche = QtWidgets.QMenu(self.menuBar)
    self.menuWizard = QtWidgets.QMenu(self.menuBar)
    self.menuFeedback = QtWidgets.QMenu(self.menuBar)
    self.menuOptionen = QtWidgets.QMenu(self.menuBar)
    self.menuOptionen.setTitle("Optionen")
    self.menuHelp = QtWidgets.QMenu(self.menuBar)
    self.menuUpdate = QtWidgets.QMenu(self.menuHelp)
    self.menuUpdate.setTitle("Update...")
    self.menuDeveloper = QtWidgets.QMenu(self.menuBar)

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
        "Datenbank aufräumen",
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
            "LaMA Cria (Unterstufe)",
            partial(self.change_program, "cria"), #
        )

    self.action_lama = add_action(
            MainWindow,
            self.menuChangeProgram,
            "LaMA (Oberstufe)",
            partial(self.change_program, "lama"), #
        )

    self.action_wizard = add_action(
            MainWindow,
            self.menuChangeProgram,
            "LaMA Worksheet Wizard",
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
    if self.chosen_program == "lama":
        label = "Alle Dateien ausgeben, die ausschließlich diese Themengebiete enthalten"
    if self.chosen_program == "cria":
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
    # self.verticalLayout_frame_gk.setContentsMargins(1,1,1,1)

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

    self.gridLayout_stackSearch.addWidget(self.widget_headMenu, 0,0,1,2)


    self.frame_tab_widget_gk = QtWidgets.QFrame(self.stackSearch)
    self.frame_tab_widget_gk.setObjectName("frame_tab_widget_gk")
    self.verticalLayout_frame_gk = create_new_verticallayout(self.frame_tab_widget_gk)
    # self.verticalLayout_frame_gk.setContentsMargins(1,1,1,1)

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

    self.groupBox_ausgew_gk = create_new_groupbox(
        self.stackSearch, "Auswahl"
    )
    # self.groupBox_ausgew_gk.setMaximumHeight(110)

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
    # self.widget_searchMenu.setContentsMargins(0,0,0,0)
    self.gridLayout_stackSearch.addWidget(self.widget_searchMenu, 1 , 1,2,1)

    self.verticalLayout_searchMenu = create_new_verticallayout(self.widget_searchMenu)
    self.verticalLayout_searchMenu.setContentsMargins(0,0,0,0)

    self.groupBox_af = QtWidgets.QGroupBox(self.widget_searchMenu)
    self.groupBox_af.setSizePolicy(SizePolicy_fixed_height)
    # self.groupBox_af.setMaximumSize(QtCore.QSize(375, 16777215))
    self.groupBox_af.setObjectName("groupBox_af")
    # self.groupBox_af.setMaximumHeight(80)
    self.gridLayout_af = QtWidgets.QGridLayout(self.groupBox_af)
    self.gridLayout_af.setObjectName("gridLayout_af")
    self.gridLayout_af.setContentsMargins(0,15,5,10)

    self.cb_af_mc = QtWidgets.QCheckBox(self.groupBox_af)
    self.cb_af_mc.setObjectName("cb_af_mc")
    self.gridLayout_af.addWidget(self.cb_af_mc, 0, 0, 1, 1)


    self.cb_af_zo = QtWidgets.QCheckBox(self.groupBox_af)        
    self.cb_af_zo.setObjectName("cb_af_zo")
    self.gridLayout_af.addWidget(self.cb_af_zo, 1, 0, 1, 1)

    self.cb_af_lt = QtWidgets.QCheckBox(self.groupBox_af)
    self.cb_af_lt.setObjectName("cb_af_lt")
    self.gridLayout_af.addWidget(self.cb_af_lt, 2, 0, 1, 1)        
    
    self.cb_af_oa = QtWidgets.QCheckBox(self.groupBox_af)
    self.cb_af_oa.setObjectName("cb_af_oa")
    self.gridLayout_af.addWidget(self.cb_af_oa, 3, 0, 1, 1)


    self.cb_af_ta = QtWidgets.QCheckBox(self.groupBox_af)
    self.cb_af_ta.setObjectName("cb_af_ta")
    self.gridLayout_af.addWidget(self.cb_af_ta, 0, 1, 1, 1)

    self.cb_af_rf = QtWidgets.QCheckBox(self.groupBox_af)
    self.cb_af_rf.setObjectName("cb_af_rf")
    self.gridLayout_af.addWidget(self.cb_af_rf, 1, 1, 1, 1)

    self.cb_af_ko = QtWidgets.QCheckBox(self.groupBox_af)
    self.cb_af_ko.setObjectName("cb_af_ko")
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
    # self.groupBox_advanced_search = create_new_groupbox(
    #     self.centralwidget, "Erweiterte Suche:"
    # )
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


    self.entry_suchbegriffe = create_new_lineedit(self.frame_advanced_search, "entry_suchbegriffe")
    self.horizontalLayout_advanced_search.addWidget(self.entry_suchbegriffe)

    self.filter_search = create_new_button(self.frame_advanced_search, "", still_to_define)
    self.filter_search.setIcon(QtGui.QIcon(get_icon_path('filter.svg')))
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
    self.splitter_sage.splitterMoved.connect(self.splitter_sage_moved)

    self.groupBox_alle_aufgaben = QtWidgets.QGroupBox(self.splitter_sage)
    self.groupBox_alle_aufgaben.setMinimumWidth(10)
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

