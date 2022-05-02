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
    create_new_spinbox,
    add_new_option,
    add_new_tab,
    DragDropWidget,
    )
from predefined_size_policy import SizePolicy_fixed_height, SizePolicy_fixed, SizePolicy_fixed_width, SizePolicy_minimum_fixed, SizePolicy_maximum_height, SizePolicy_maximum_width
from config import *
from functools import partial
from create_pdf import prepare_tex_for_pdf
from standard_dialog_windows import warning_window





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

        dict_klasse = eval("dict_{}".format(klasse))
        kapitel = list(dict_klasse.keys())[0]

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


    self.entry_suchbegriffe = create_new_lineedit(self.frame_advanced_search, "entry_suchbegriffe")
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

    ####################
    self.verticalLayout_sage.addWidget(self.lineEdit_number)
    self.verticalLayout_sage.addWidget(self.listWidget)


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
            self.combobox_beurteilung.removeItem(self.combobox_beurteilung.findText("Beurteilungsraster"))
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

    self.gridLayout_SageMenu.addWidget(self.widget_datum, 1,0,1,1, QtCore.Qt.AlignLeft)


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

    self.label_sg = create_new_label(self.groupBox_notenschl, "Sehr Gut:")
    self.label_sg.setSizePolicy(SizePolicy_fixed)
    self.gridLayout_6.addWidget(self.label_sg, 0, 0, 1, 1)
    self.spinBox_2 = create_new_spinbox(self.groupBox_notenschl, sehr_gut)
    self.spinBox_2.setSizePolicy(SizePolicy_fixed)
    self.spinBox_2.valueChanged.connect(self.update_punkte)
    self.gridLayout_6.addWidget(self.spinBox_2, 0, 1, 1, 1)
    self.label_sg_pkt = create_new_label(self.groupBox_notenschl, "% (ab 0)")
    self.gridLayout_6.addWidget(self.label_sg_pkt, 0, 2, 1, 1)

    self.label_g = create_new_label(self.groupBox_notenschl, "Gut:")
    self.label_g.setSizePolicy(SizePolicy_fixed)
    self.gridLayout_6.addWidget(self.label_g, 0, 3, 1, 1)
    self.spinBox_3 = create_new_spinbox(self.groupBox_notenschl, gut)
    self.spinBox_3.setSizePolicy(SizePolicy_fixed)
    self.spinBox_3.valueChanged.connect(self.update_punkte)
    self.gridLayout_6.addWidget(self.spinBox_3, 0, 4, 1, 1)
    self.label_g_pkt = create_new_label(self.groupBox_notenschl, "% (ab 0)")
    self.gridLayout_6.addWidget(self.label_g_pkt, 0, 5, 1, 1)

    self.label_b = create_new_label(self.groupBox_notenschl, "Befriedigend:")
    self.label_b.setSizePolicy(SizePolicy_fixed)
    self.gridLayout_6.addWidget(self.label_b, 1, 0, 1, 1)
    self.spinBox_4 = create_new_spinbox(self.groupBox_notenschl, befriedigend)
    self.spinBox_4.setSizePolicy(SizePolicy_fixed)
    self.spinBox_4.valueChanged.connect(self.update_punkte)
    self.gridLayout_6.addWidget(self.spinBox_4, 1, 1, 1, 1)
    self.label_b_pkt = create_new_label(self.groupBox_notenschl, "% (ab 0)")
    self.gridLayout_6.addWidget(self.label_b_pkt, 1, 2, 1, 1)

    self.label_g_2 = create_new_label(self.groupBox_notenschl, "Genügend:")
    self.label_g_2.setSizePolicy(SizePolicy_fixed)
    self.gridLayout_6.addWidget(self.label_g_2, 1, 3, 1, 1)
    self.spinBox_5 = create_new_spinbox(self.groupBox_notenschl, genuegend)
    self.spinBox_5.setSizePolicy(SizePolicy_fixed)
    self.spinBox_5.valueChanged.connect(self.update_punkte)
    self.gridLayout_6.addWidget(self.spinBox_5, 1, 4, 1, 1)
    self.label_g_2_pkt = create_new_label(self.groupBox_notenschl, "% (ab 0)")
    self.gridLayout_6.addWidget(self.label_g_2_pkt, 1, 5, 1, 1)

    self.groupBox_notenschl_modus = create_new_groupbox(
        self.groupBox_notenschl, "Anzeige"
    )
    self.gridLayout_6.addWidget(self.groupBox_notenschl_modus, 0, 6, 2, 1)

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

    self.groupBox_beurteilungsraster = QtWidgets.QGroupBox(self.groupBox_sage)
    self.groupBox_beurteilungsraster.setObjectName("groupBox_beurteilungsraster")
    # self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_beurteilungsraster)
    # self.gridLayout_6.setObjectName("gridLayout_6")
    self.verticalLayout_beurteilungsraster = create_new_verticallayout(self.groupBox_beurteilungsraster)

    self.label_typ1_pkt = QtWidgets.QLabel(self.groupBox_beurteilungsraster)
    self.label_typ1_pkt.setObjectName("label_typ1_pkt")
    self.verticalLayout_beurteilungsraster.addWidget(self.label_typ1_pkt)
    # self.gridLayout_6.addWidget(self.label_typ1_pkt, 0, 0, 1, 2)
    # self.label_typ1_pkt.setText(_translate("MainWindow", "Punkte Typ 1: 0",None))

    self.label_typ2_pkt = QtWidgets.QLabel(self.groupBox_beurteilungsraster)
    self.label_typ2_pkt.setObjectName("label_typ2_pkt")
    self.verticalLayout_beurteilungsraster.addWidget(self.label_typ2_pkt)
    # self.gridLayout_6.addWidget(self.label_typ2_pkt, 1, 0, 1, 2)

    self.groupBox_beurteilungsraster.setTitle("Beurteilungsraster")

    self.gridLayout_5.addWidget(self.groupBox_beurteilungsraster, 2, 0, 1, 2)
    self.groupBox_beurteilungsraster.hide()

    ### Zusammenfassung d. SA ###
    self.widgetSummarySage = QtWidgets.QWidget(self.groupBox_sage)
    self.widgetSummarySage.setObjectName("widgetSummarySage")
    self.gridLayout_5.addWidget(self.widgetSummarySage,3, 0, 1, 1)
    self.verticalLayoutSummarySage = create_new_verticallayout(self.widgetSummarySage)



    if self.chosen_program == "lama":
        label = "Anzahl der Aufgaben: 0\n(Typ1: 0 / Typ2: 0)"

    if self.chosen_program == "cria":
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
    # self.splitter_creator_left_widget.setMinimumSize(1,1)
    # self.splitter_creator_left_widget.resize(450,0)
    self.verticalLayout_splitter_creator_left_widget = create_new_verticallayout(self.splitter_creator_left_widget)
    self.verticalLayout_splitter_creator_left_widget.setContentsMargins(0,0,0,0)


    self.splitter_creator_right_widget = QtWidgets.QWidget(self.splitter_creator)
    # self.splitter_creator_right_widget.setMinimumSize(1,1)  
    self.verticalLayout_splitter_creator_right_widget = create_new_verticallayout(self.splitter_creator_right_widget)
    self.verticalLayout_splitter_creator_right_widget.setContentsMargins(0,0,0,0)



    ############# CREATOR ###############

    self.groupBox_variation_cr = create_new_groupbox(
        self.splitter_creator, "Aufgabenvariation"
    )
    # self.groupBox_variation_cr.setMaximumWidth(420)
    self.verticalLayout_variation = create_new_verticallayout(
        self.groupBox_variation_cr
    )  
    self.button_variation_cr = create_new_button(
        self.groupBox_variation_cr,
        "Variation vorhandender Aufgabe...",
        partial(self.button_variation_cr_pressed, "creator"),
    )
    # self.button_variation_cr.setMinimumWidth(0)
    self.verticalLayout_variation.addWidget(self.button_variation_cr)

    self.verticalLayout_splitter_creator_left_widget.addWidget(self.groupBox_variation_cr)

    ######################################

    ################ EDITOR #####################

    self.groupBox_choose_file = create_new_groupbox(
        self.splitter_creator, "Aufgabe auswählen"
    )
    self.groupBox_choose_file.setMinimumSize(1,1)
    # self.groupBox_choose_file.setMaximumWidth(420)
    self.verticalLayout_choose_file = create_new_verticallayout(
        self.groupBox_choose_file
    )

    self.button_choose_file = create_new_button(
        self.groupBox_choose_file,
        "Aufgabe suchen...",
        partial(self.button_variation_cr_pressed, "editor"),
    )
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
    self.groupBox_themengebiete_cria.setMinimumSize(1,1)
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
        kapitel = list(dict_klasse.keys())[0]

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
    self.verticalLayout_bilder.setContentsMargins(0,5,0,0)
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
    add_new_option(self.comboBox_aufgabentyp_cr, 0, "Typ 1")
    add_new_option(self.comboBox_aufgabentyp_cr, 1, "Typ 2")

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
        self.stackCreator, "Änderung speichern", self.button_save_edit_pressed
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


# def setup_stackEditor(self):
#     self.gridLayout_stackEditor = create_new_gridlayout(self.stackEditor)

    # self.splitter_editor = QtWidgets.QSplitter(self.stackEditor)
    # self.splitter_editor.setOrientation(QtCore.Qt.Horizontal)
    # self.splitter_editor.setObjectName("splitter_editor")
    # self.gridLayout_stackEditor.addWidget(self.splitter_editor, 0, 0, 1, 1)

    # self.splitter_editor_left_widget = QtWidgets.QWidget(self.splitter_editor)
    # self.splitter_editor_left_widget.setMinimumSize(1,1)
    # self.splitter_editor_left_widget.resize(450,0)
    # self.verticalLayout_splitter_editor_left_widget = create_new_verticallayout(self.splitter_editor_left_widget)
    # self.verticalLayout_splitter_editor_left_widget.setContentsMargins(0,0,0,0)


    # self.splitter_editor_right_widget = QtWidgets.QWidget(self.splitter_editor)
    # self.splitter_editor_right_widget.setMinimumSize(1,1)  
    # self.verticalLayout_splitter_editor_right_widget = create_new_verticallayout(self.splitter_editor_right_widget)
    # self.verticalLayout_splitter_editor_right_widget.setContentsMargins(0,0,0,0)



    # # self.groupBox_variation_editor = create_new_groupbox(
    # #     self.splitter_editor, "Aufgabenvariation"
    # # )
    # # # self.groupBox_variation_cr.setMaximumWidth(420)
    # # self.verticalLayout_variation = create_new_verticallayout(
    # #     self.groupBox_variation_editor
    # # )  

    # # self.button_variation_cr = create_new_button(
    # #     self.groupBox_variation_cr,
    # #     "Variation vorhandender Aufgabe...",
    # #     partial(self.button_variation_cr_pressed, "creator"),
    # # )
    # # self.button_variation_cr.setMinimumWidth(0)
    # # self.verticalLayout_variation.addWidget(self.button_variation_cr)

    # # self.verticalLayout_splitter_creator_left_widget.addWidget(self.groupBox_variation_cr)



    # self.groupBox_choose_file_editor = create_new_groupbox(
    #     self.splitter_editor, "Aufgabe auswählen"
    # )
    # self.groupBox_choose_file_editor.setMaximumWidth(420)
    # self.verticalLayout_choose_file_editor = create_new_verticallayout(
    #     self.groupBox_choose_file_editor
    # )

    # self.button_choose_file_editor = create_new_button(
    #     self.groupBox_choose_file_editor,
    #     "Aufgabe suchen...",
    #     partial(self.button_variation_cr_pressed, "editor"),
    # )
    # self.button_choose_file_editor.setMinimumWidth(0)
    # self.verticalLayout_choose_file.addWidget(self.button_choose_file_editor)

    # self.gridLayout_stackEditor.addWidget(self.groupBox_choose_file_editor, 0, 0, 1, 1)


    # self.groupBox_grundkompetenzen_editor = QtWidgets.QGroupBox(self.splitter_editor)
    # self.groupBox_grundkompetenzen_editor.setFocusPolicy(QtCore.Qt.NoFocus)
    # self.groupBox_grundkompetenzen_editor.setObjectName("groupBox_grundkompetenzen_editor")
    # self.groupBox_grundkompetenzen_editor.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum))
    # self.gridLayout_11_editor = QtWidgets.QGridLayout(self.groupBox_grundkompetenzen_editor)
    # self.gridLayout_11_editor.setObjectName("gridLayout_11_editor")
    # self.tab_widget_gk_editor = QtWidgets.QTabWidget(self.groupBox_grundkompetenzen_editor)


    # self.tab_widget_gk_editor.setFocusPolicy(QtCore.Qt.NoFocus)
    # self.tab_widget_gk_editor.setObjectName("tab_widget_gk_editor")
    # self.gridLayout_11_editor.addWidget(self.tab_widget_gk_editor, 0, 0, 1, 1)
    # self.verticalLayout_splitter_editor_left_widget.addWidget(self.groupBox_grundkompetenzen_editor)

    # self.groupBox_grundkompetenzen_editor.setTitle("Grundkompetenzen")


    # self.groupBox_ausgew_gk_editor = create_new_groupbox(self.splitter_editor, "Auswahl")

    # self.verticalLayout_2_editor = create_new_verticallayout(self.groupBox_ausgew_gk_editor)

    # self.label_ausgew_gk_editor = create_new_label(
    #     self.groupBox_ausgew_gk_editor, "", True
    # )

    # self.verticalLayout_2_editor.addWidget(self.label_ausgew_gk_editor)
    # self.verticalLayout_splitter_editor_left_widget.addWidget(self.groupBox_ausgew_gk_editor)

    # self.groupBox_bilder_editor = create_new_groupbox(
    #     self.splitter_editor, "Bilder (klicken, um Bilder zu entfernen)"
    # )

    # self.gridLayout_13_editor = QtWidgets.QGridLayout(self.groupBox_bilder)
    # self.gridLayout_13_editor.setObjectName("gridLayout_13_editor")
    # self.scrollArea_editor = QtWidgets.QScrollArea(self.groupBox_bilder_editor)
    # self.scrollArea_editor.setWidgetResizable(True)
    # self.scrollArea_editor.setObjectName("scrollArea_editor")
    # self.scrollArea_editor.setFrameShape(QtWidgets.QFrame.NoFrame)
    # self.scrollArea_editor.setFocusPolicy(QtCore.Qt.NoFocus)
    # self.scrollAreaWidgetContents_bilder_editor = QtWidgets.QWidget()

    # self.scrollAreaWidgetContents_bilder_editor.setObjectName("scrollAreaWidgetContents_bilder")
    # self.verticalLayout_editor = QtWidgets.QVBoxLayout(
    #     self.scrollAreaWidgetContents_bilder_editor
    # )
    # self.verticalLayout_editor.setObjectName("verticalLayout_editor")
    # self.scrollArea_editor.setWidget(self.scrollAreaWidgetContents_bilder_editor)
    # self.gridLayout_13_editor.addWidget(self.scrollArea_editor, 1, 0, 1, 1)
    # self.groupBox_bilder_editor.setTitle("Bilder (klicken, um Bilder zu entfernen)")
    # self.groupBox_bilder_editor.setSizePolicy(SizePolicy_maximum_height)


    # self.verticalLayout_splitter_editor_left_widget.addWidget(self.groupBox_bilder_editor)

    # self.btn_add_image_editor = create_new_button(
    #     self.groupBox_bilder_editor, "Hinzufügen", self.btn_add_image_pressed
    # )
    # self.verticalLayout.addWidget(self.btn_add_image_editor)

    # #### CREATE CHECKBOXES ####
    # ##### AG #####
    # self.create_tab_checkboxes_gk(
    #     self.tab_widget_gk_editor, "Algebra und Geometrie", ag_beschreibung, "editor"
    # )

    # # # #### FA ####
    # self.create_tab_checkboxes_gk(
    #     self.tab_widget_gk_editor,
    #     "Funktionale Abhängigkeiten",
    #     fa_beschreibung,
    #     "editor",
    # )

    # # ##### AN ####
    # self.create_tab_checkboxes_gk(
    #     self.tab_widget_gk_editor, "Analysis", an_beschreibung, "editor"
    # )

    # # ### WS ####
    # self.create_tab_checkboxes_gk(
    #     self.tab_widget_gk_editor,
    #     "Wahrscheinlichkeit und Statistik",
    #     ws_beschreibung,
    #     "editor",
    # )

    # # ### Zusatzthemen ###
    # self.create_tab_checkboxes_themen(self.tab_widget_gk_editor, "editor")

    # ############################

    # self.widget_basic_settings_editor = QtWidgets.QWidget(self.splitter_editor_right_widget)
    # self.verticalLayout_splitter_editor_right_widget.addWidget(self.widget_basic_settings_editor)

    # self.horizontalLayout_basic_settings_editor = create_new_horizontallayout(self.widget_basic_settings_editor)
    # self.horizontalLayout_basic_settings_editor.setContentsMargins(0,0,0,0)


    # self.groupBox_aufgabentyp_editor = create_new_groupbox(self.widget_basic_settings_editor, "Aufgabentyp")
    # self.groupBox_aufgabentyp_editor.setSizePolicy(SizePolicy_fixed)
    # self.gridLayout_3_editor = create_new_horizontallayout(self.groupBox_aufgabentyp_editor)

    # add_new_option(self.comboBox_aufgabentyp_editor, 0, "Typ 1")
    # add_new_option(self.comboBox_aufgabentyp_editor, 1, "Typ 2")

    # self.comboBox_aufgabentyp_editor.currentIndexChanged.connect(self.chosen_aufgabenformat_editor)
    # self.gridLayout_3_editor.addWidget(self.comboBox_aufgabentyp_editor)
    # self.horizontalLayout_basic_settings_editor.addWidget(self.groupBox_aufgabentyp_editor)   


    # self.groupBox_punkte_editor = create_new_groupbox(self.widget_basic_settings_editor, "Punkte")

    # self.horizontalLayout_punkte_editor = create_new_horizontallayout(self.groupBox_punkte_editor)

    # self.spinBox_punkte_editor = create_new_spinbox(self.groupBox_punkte_editor, 1)

    
    # self.horizontalLayout_punkte_editor.addWidget(self.spinBox_punkte_editor)
    # self.horizontalLayout_basic_settings_editor.addWidget(self.groupBox_punkte_editor)


    # self.groupBox_aufgabenformat_editor = create_new_groupbox(self.widget_basic_settings_editor, "Aufgabenformat")


    # self.horizontalLayout_aufgabenformat_editor = create_new_horizontallayout(self.groupBox_aufgabenformat_editor)


    # self.comboBox_af_editor = create_new_combobox(self.groupBox_aufgabenformat_editor)
    # add_new_option(self.comboBox_af_editor, 0, "bitte auswählen")

    # self.horizontalLayout_aufgabenformat_editor.addWidget(self.comboBox_af_editor)


    # i = 1
    # for all in dict_aufgabenformate:
    #     add_new_option(self.comboBox_af_editor, i, dict_aufgabenformate[all])
    #     if self.chosen_program == "lama" and i == 4:
    #         break
    #     i += 1
    # self.horizontalLayout_basic_settings_editor.addWidget(self.groupBox_aufgabenformat_editor)

    # self.groupBox_klassen_editor = create_new_groupbox(self.widget_basic_settings_editor, "Klasse")


    # self.horizontalLayout_klassen_editor = create_new_horizontallayout(self.groupBox_klassen_editor)
    # self.comboBox_klassen_editor = create_new_combobox(self.groupBox_klassen_editor)

    # add_new_option(self.comboBox_klassen_editor, 0, "-")

    # i=1
    # for all in Klassen:
    #     if all != "univie" and all != "mat":
    #         add_new_option(self.comboBox_klassen_editor, i, Klassen[all])
    #         i+=1


    # self.horizontalLayout_klassen_editor.addWidget(self.comboBox_klassen_editor)
    # self.horizontalLayout_basic_settings_editor.addWidget(self.groupBox_klassen_editor)

    # self.groupBox_abstand_editor = create_new_groupbox(self.widget_basic_settings_editor, "Abstand")

    # self.groupBox_abstand_editor.setToolTip("Abstand unter der Aufgabe (in cm)")
    # self.horizontalLayout_abstand_editor = create_new_horizontallayout(
    #     self.groupBox_abstand_editor
    # )
    # self.spinBox_abstand_editor = create_new_spinbox(self.groupBox_abstand_editor)
    # self.horizontalLayout_abstand_editor.addWidget(self.spinBox_abstand_editor)

    # self.horizontalLayout_basic_settings_editor.addWidget(self.groupBox_abstand_editor)



    # self.groupBox_pagebreak_editor = create_new_groupbox(
    #     self.widget_basic_settings_editor, "Seitenumbruch"
    # )

    # self.horizontalLayout_pagebreak_editor = create_new_horizontallayout(
    #     self.groupBox_pagebreak_editor
    # )
    # self.comboBox_pagebreak_editor = create_new_combobox(self.groupBox_pagebreak_editor)
    # add_new_option(self.comboBox_pagebreak_editor, 0, "nicht möglich")
    # add_new_option(self.comboBox_pagebreak_editor, 1, "möglich")
    # self.horizontalLayout_pagebreak_editor.addWidget(self.comboBox_pagebreak_editor)

    # self.horizontalLayout_basic_settings_editor.addWidget(self.groupBox_pagebreak_editor)

    # self.cb_matura_tag_editor = create_new_checkbox(self.widget_basic_settings_editor, "Matura")
    # self.horizontalLayout_basic_settings_editor.addWidget(self.cb_matura_tag_editor)
    # self.cb_matura_tag_editor.hide()

    # self.cb_no_grade_tag_editor = create_new_checkbox(
    #     self.widget_basic_settings_editor, "klassen-\nunabhängig"
    # )
    # self.horizontalLayout_basic_settings_editor.addWidget(self.cb_no_grade_tag_editor)
    # self.cb_no_grade_tag_editor.hide()


    # self.groupBox_titel_editor = QtWidgets.QGroupBox(self.splitter_editor_right_widget)
    # self.groupBox_titel_editor.setObjectName("groupBox_titel_editor")
    # self.groupBox_titel_editor.setSizePolicy(SizePolicy_fixed_height)

    # self.gridLayout_14_editor = QtWidgets.QGridLayout(self.groupBox_titel_editor)
    # self.gridLayout_14_editor.setObjectName("gridLayout_14_editor")
    # self.lineEdit_titel_editor = QtWidgets.QLineEdit(self.groupBox_titel_editor)
    # self.lineEdit_titel_editor.setObjectName("lineEdit_titel_editor")


    # self.gridLayout_14_editor.addWidget(self.lineEdit_titel_editor, 0, 0, 1, 1)
    # self.verticalLayout_splitter_editor_right_widget.addWidget(self.groupBox_titel_editor)

    # self.groupBox_titel_editor.setTitle("Titel")


    # self.groupBox_beispieleingabe_editor = QtWidgets.QGroupBox(self.splitter_editor)
    # self.groupBox_beispieleingabe_editor.setObjectName("groupBox_beispieleingabe_editor")

    # self.gridLayout_10_editor = QtWidgets.QGridLayout(self.groupBox_beispieleingabe_editor)
    # self.gridLayout_10_editor.setObjectName("gridLayout_10_editor")
    # self.label_editor = QtWidgets.QLabel(self.groupBox_beispieleingabe_editor)

    # self.label_editor.setStyleSheet("border: 2px solid #C33A3F;")
    # self.label_editor.setWordWrap(True)
    # self.label_editor.setObjectName("label")
    # self.gridLayout_10_editor.addWidget(self.label_editor, 0, 0, 1, 1)
    # self.plainTextEdit_editor = QtWidgets.QPlainTextEdit(self.groupBox_beispieleingabe_editor)
    # self.plainTextEdit_editor.setObjectName("plainTextEdit")
    # self.plainTextEdit_editor.setTabChangesFocus(True)
    # self.gridLayout_10_editor.addWidget(self.plainTextEdit_editor, 1, 0, 1, 1)
    # self.verticalLayout_splitter_editor_right_widget.addWidget(self.groupBox_beispieleingabe_editor)

    # self.groupBox_beispieleingabe_editor.setTitle("Aufgabeneingabe")
    # self.label_editor.setText("Info: Eingabe des Aufgabentextes zwischen \\begin{beispiel}...\\end{beispiel}")


    # self.groupBox_quelle_editor = QtWidgets.QGroupBox(self.splitter_editor_right_widget)
    # self.groupBox_quelle_editor.setObjectName("groupBox_quelle_editor")

    # self.gridLayout_18_editor = QtWidgets.QGridLayout(self.groupBox_quelle_editor)
    # self.gridLayout_18_editor.setObjectName("gridLayout_18_editor")
    # self.lineEdit_quelle_editor = QtWidgets.QLineEdit(self.groupBox_quelle_editor)
    # self.lineEdit_quelle_editor.setObjectName("lineEdit_quelle_editor")
    # try:
    #     quelle = self.lama_settings["quelle"]
    # except KeyError:
    #     quelle = ""

    # self.lineEdit_quelle_editor.setText(quelle)
    # self.gridLayout_18_editor.addWidget(self.lineEdit_quelle_editor, 0, 0, 1, 1)

    # self.verticalLayout_splitter_editor_right_widget.addWidget(self.groupBox_quelle_editor)

    # self.groupBox_quelle_editor.setTitle("Quelle oder Autor (Vorname Nachname) - Eingabe: VorNac")


    # self.widgeteditorButtons_editor = QtWidgets.QWidget(self.stackEditor)
    # self.gridLayout_stackEditor.addWidget(self.widgeteditorButtons_editor, 1,0,1,1)
    # self.widgeteditorButtons_editor.setSizePolicy(SizePolicy_fixed_height)
    # self.horizontalLayout_editorButtons_editor = create_new_horizontallayout(self.widgeteditorButtons_editor)
    # self.horizontalLayout_editorButtons_editor.setContentsMargins(0,0,0,0)


    # self.horizontalLayout_editorButtons.addStretch()
    # self.pushButton_save_editor = QtWidgets.QPushButton(self.widgeteditorButtons)
    # self.pushButton_save_editor.setObjectName("pushButton_save_editor")
    # self.pushButton_save_editor.setFocusPolicy(QtCore.Qt.NoFocus)
    # self.pushButton_save_editor.setSizePolicy(SizePolicy_fixed)
    # self.horizontalLayout_editorButtons.addWidget(self.pushButton_save_editor)
    # self.pushButton_save_editor.setText("Speichern")
    # self.pushButton_save_editor.setIcon(QtGui.QIcon(get_icon_path('save.svg')))


    # self.pushButton_vorschau_edit_editor = create_new_button(
    #     self.widgeteditorButtons, "Vorschau", self.button_vorschau_edit_pressed
    # )
    # self.pushButton_vorschau_edit_editor.setIcon(QtGui.QIcon(get_icon_path('eye.svg')))
    # self.pushButton_vorschau_edit_editor.setShortcut("Ctrl+Return")
    # self.pushButton_vorschau_edit_editor.setToolTip("Strg+Enter")
    # self.pushButton_vorschau_edit_editor.setSizePolicy(SizePolicy_fixed)
    # self.horizontalLayout_editorButtons.addWidget(self.pushButton_vorschau_edit_editor)
    # # self.pushButton_vorschau_edit.hide()

    # self.pushButton_delete_file_editor = create_new_button(
    #     self.widgeteditorButtons, "Aufgabe löschen", self.button_delete_file_pressed
    # )
    # self.pushButton_delete_file_editor.setIcon(QtGui.QIcon(get_icon_path('trash-2.svg')))
    # # self.pushButton_delete_file.setStyleSheet("color: red")
    # self.pushButton_delete_file_editor.setSizePolicy(SizePolicy_fixed)
    # self.horizontalLayout_editorButtons.addWidget(self.pushButton_delete_file_editor)
    # # self.pushButton_delete_file_editor.hide()

    # self.pushButton_save_as_variation_edit_editor = create_new_button(
    #     self.widgeteditorButtons,
    #     "Als Variation einer anderen Aufgabe speichern",
    #     self.pushButton_save_as_variation_edit_pressed,
    # )
    # self.pushButton_save_as_variation_edit_editor.setIcon(QtGui.QIcon(get_icon_path('git-branch.svg')))
    # self.pushButton_save_as_variation_edit_editor.setSizePolicy(SizePolicy_fixed)
    # self.horizontalLayout_editorButtons.addWidget(self.pushButton_save_as_variation_edit_editor)
    # # self.pushButton_save_as_variation_edit.hide()

    # self.pushButton_save_edit_editor = create_new_button(
    #     self.stackEditor, "Änderung speichern", self.button_save_edit_pressed
    # )
    # self.pushButton_save_edit_editor.setIcon(QtGui.QIcon(get_icon_path('save.svg')))
    # self.pushButton_save_edit_editor.setSizePolicy(SizePolicy_fixed)
    # self.pushButton_save_edit_editor.setFocusPolicy(QtCore.Qt.NoFocus)
    # self.horizontalLayout_editorButtons.addWidget(self.pushButton_save_edit_editor)
    # # self.pushButton_save_edit.hide()

    # self.lineEdit_titel_editor.setFocus()
    # self.tab_widget_gk_editor.setCurrentIndex(0)
    # QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    # ############ Infos for GKs
    # self.create_Tooltip(ag_beschreibung)
    # self.create_Tooltip(fa_beschreibung)
    # self.create_Tooltip(an_beschreibung)
    # self.create_Tooltip(ws_beschreibung)
    # ############################################

    # self.comboBox_aufgabentyp_editor.currentIndexChanged.connect(self.chosen_aufgabenformat_cr)
    # self.pushButton_save.clicked.connect(lambda: self.button_speichern_pressed())



def setup_stackFeedback(self):
    self.gridLayout_stackFeedback = create_new_gridlayout(self.stackFeedback)


    self.splitter_feedback = QtWidgets.QSplitter(self.stackFeedback)
    self.splitter_feedback.setOrientation(QtCore.Qt.Horizontal)
    self.splitter_feedback.setObjectName("splitter_feedback")
    self.gridLayout_stackFeedback.addWidget(self.splitter_feedback, 0, 0, 1, 1)


    self.splitter_feedback_left_widget = QtWidgets.QWidget(self.splitter_feedback)
    # self.splitter_feedback_left_widget.setMinimumSize(1,1)  
    self.verticalLayout_splitter_feedback_left_widget = create_new_verticallayout(self.splitter_feedback_left_widget)
    self.verticalLayout_splitter_feedback_left_widget.setContentsMargins(0,0,0,0)


    self.groupBox_alle_aufgaben_fb = QtWidgets.QGroupBox(self.splitter_feedback_left_widget)
    # self.groupBox_alle_aufgaben_fb.setMinimumSize(1,1)
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

    self.lineEdit_number_fb_cria.textChanged.connect(
        partial(self.adapt_choosing_list, "feedback")
    )
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
    # self.splitter_feedback_right_widget.setMinimumSize(1,1)  
    self.verticalLayout_splitter_feedback_right_widget = create_new_verticallayout(self.splitter_feedback_right_widget)
    self.verticalLayout_splitter_feedback_right_widget.setContentsMargins(0,0,0,0)



    self.label_example = QtWidgets.QLabel(self.splitter_feedback_right_widget)
    self.label_example.setObjectName("label_example")
    # self.label_update.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
    self.label_example.setText("Ausgewählte Aufgabe: -")
    self.verticalLayout_splitter_feedback_right_widget.addWidget(self.label_example)
    # self.gridLayout_stackFeedback.addWidget(self.label_example, 0, 1, 1, 1)

    self.groupBox_fehlertyp = QtWidgets.QGroupBox(self.splitter_feedback_right_widget)
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

    # self.adapt_choosing_list('feedback')


    # self.pushButton_send = QtWidgets.QPushButton(self.splitter_feedback_right_widget)
    # self.pushButton_send.setObjectName("pushButton_send")
    # self.pushButton_send.setSizePolicy(SizePolicy_fixed)
    # self.verticalLayout_splitter_feedback_right_widget.addWidget(self.pushButton_send)
    # # self.gridLayout_stackFeedback.addWidget(
    # #     self.pushButton_send, 4, 1, 1, 1, QtCore.Qt.AlignRight
    # # )
    # self.pushButton_send.setText("Senden")
    # self.pushButton_send.setIcon(QtGui.QIcon(get_icon_path('send.svg'))) 
    # self.pushButton_send.clicked.connect(lambda: self.pushButton_send_pressed())
    # # self.pushButton_send.hide()




