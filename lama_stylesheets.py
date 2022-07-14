from config import get_color, get_icon_path
from lama_colors import *



StyleSheet_application = """
    QMenuBar::item:selected{{
        background-color: #2F4550;
        color: #F4F4F9; 
    }}

   
    QMenu::item:selected{{
        background-color: #2F4550;
        color: #F4F4F9;  
    }}

    QMenu::item:disabled{{
        color: gray
    }}

    QScrollBar {{
        border: none;    
    }}

    QScrollBar::handle::vertical {{
       background-color: #2F4550;
       border-radius: 7px;
       min-height: 30px;
    }}

    QScrollBar::handle::horizontal {{
       background-color: #2F4550;
       border-radius: 7px;
       min-width: 30px;
    }}

    QScrollBar::add-line{{
        border: none;
        background: none;
    }}

    QScrollBar::sub-line{{
        border: none;
        background: none;
    }}


    QTabBar::tab:selected {{
        background-color: #2F4550;
        color: #F4F4F9;
    }}


    QTabBar::tab::disabled {{
        background-color: gray;
        color: #F4F4F9;
    }}

    QTabBar::scroller{{
        background-color: #2F4550;
        color: #2F4550;
    }}

    QTabBar QToolButton::left-arrow {{
        background-color: #F4F4F9;
        image: url({0});        
    }}

    QTabBar QToolButton::right-arrow {{
        background-color: #F4F4F9;
        image: url({1});        
    }}


    #frame_tab_widget_gk {{
        border-color: #6E8784;
        border-width: 1px;
        border-style: solid;
        border-radius: 4px;
        margin-top: 0.5em;
    }}


    QToolButton {{
        background-color: #F4F4F9;
    }}

    QToolTip {{
        color: #F4F4F9; 
        background-color: #2F4550; 
        border: 0px;
        }}




    QCheckBox {{
        spacing: -5px;
        padding-top: 2px;
    }}

    QCheckBox::indicator:unchecked {{ 
        image: url({2});
        width: 35px;
    }}


    QCheckBox::indicator:checked {{ 
        image: url({3});
        width: 35px;
    }}

    #frameNummer {{
        border-color: #6E8784;
        border-width: 1px;
        border-style: solid;
        border-radius: 4px;
        margin-top: 0.5em;       
    }}

    /*#widget_datum {{
        border-color: #6E8784;
        border-width: 1px;
        border-style: solid;
        border-radius: 4px;
        margin-top: 0.5em;       
    }}
    #widgetNummer {{
        border-color: #6E8784;
        border-width: 1px;
        border-style: solid;
        border-radius: 4px;
        margin-top: 0.5em;       
    }}*/

    #entry_suchbegriffe{{
        border-color: #6E8784;
        border-width: 1px;
        border-style: solid;
        border-radius: 4px;
        padding: 3px 3px;        
    }}

    QLineEdit{{
        background-color: #F4F4F9; 
    }}

    QGroupBox {{
        border-color: #6E8784;
        border-width: 1px;
        border-style: solid;
        border-radius: 4px;
        margin-top: 0.5em;
        padding-right: 5px;
        padding-left: 5px;
    }}


    QGroupBox::title{{
        top: -5px;
        left: 1px;
        padding-left: 3px;   
    }}

    #combobox_searchtype {{
        padding-left: 5px;
        padding-right: 20px;
        padding-top: 2px;
        padding-bottom: 2px
    }}

    QCalendarWidget QWidget
    {{
        background-color: #F4F4F9;
        color: #2F4550;
    }} 
    
    QCalendarWidget QTableView 
    {{
        background-color: #F4F4F9;
        color: #2F4550;
        alternate-background-color: #D3E0DF;
    }}

    QCalendarWidget QMenu {{
        background-color: #F4F4F9;
        color: #2F4550;        
    }}

    QCalendarWidget QWidget#qt_calendar_prevmonth{{
        qproperty-icon:url({4});
    }}

    QCalendarWidget QWidget#qt_calendar_nextmonth{{
        qproperty-icon:url({5});
    }}

    QSplitter::handle {{
        image: url({6});
    }}   


    QSplitter::handle:vertical {{
        height: 20px;
        width: 50px;
    }}

    QPlainTextEdit:disabled {{
        color: gray;
    }}

    #filter_search {{
        padding-left: -2px;
        padding-right: 5px;
        padding-top: 3px;
        padding-bottom: 3px;  
    }}

""".format(
    get_icon_path("chevron-left.svg"),
    get_icon_path("chevron-right.svg"),
    get_icon_path("square.svg"),
    get_icon_path("check-square.svg"),
    get_icon_path("arrow-left-circle.svg"),
    get_icon_path("arrow-right-circle.svg"),
    get_icon_path("more-vertical.svg")
    )


StyleSheet_new_tab = "background-color: #F4F4F9; selection-background-color: #2F4550; selection-color: #F4F4F9"



StyleSheet_tabWidget = """
QTabBar::tab:selected {{
background: {0}; color: {1};
padding-right: 10px; padding-left: 10px;
border-top: 2px solid {3};
border-left: 2px solid {3};
border-right: 2px solid {3};
}}

QTabBar::tab::disabled {{
background-color: gray;
}}


QWidget {{color: {2};background-color: {3}}}

""".format(
    get_color(blue_2), get_color(black), get_color(white), get_color(blue_7)
)



StyleSheet_tab_widget_themen = """
QTabBar::tab:selected {{
background: {0}; color: {1};
padding-right: 10px; padding-left: 10px; padding-bottom: 5px; padding-top: 5px;
border-top: 2px solid {3};
border-left: 2px solid {3};
border-right: 2px solid {3};
}}

QWidget {{color: {2};background-color: {3}}}

""".format(
    get_color(blue_2), get_color(black), get_color(white), get_color(blue_7)
)

StyleSheet_button_check_all = "background-color: {}; ".format(get_color(blue_3))

StyleSheet_unterkapitel_cria = "background-color: {}".format(get_color(blue_2))

StyleSheet_combobox_kapitel = "background-color: {0};selection-background-color: {1}; selection-color: {2}".format(
    get_color(white), get_color(blue_7), get_color(white)
)

StyleSheet_aufgaben_groupbox = "QGroupBox {{background-color: {0};}} ".format(get_color(blue_1))

StyleSheet_typ2 = """
QGroupBox {{background-color: {0}; color: {1}}}
QLabel {{color:  {1}}}
""".format(
    get_color(blue_3), get_color(black)
)


StyleSheet_new_checkbox =  """
QToolTip {{ 
color: {0}; background-color: {1}; border: 0px; 
}}       
QCheckBox {{
padding-right: 10px, padding-bottom: 10px
}}
""".format(
    get_color(white),
    get_color(blue_7)
)


StyleSheet_ausgleichspunkte = "color: black"

StyleSheet_subwindow_ausgleichspunkte = "background-color: {}".format(get_color(blue_2))
StyleSheet_subwindow_ausgleichspunkte_dark_mode = "background-color: {}".format(get_color(blue_7))

StyleSheet_tabWidget_dark_mode = """
QTabBar::tab:selected {{
background: {0}; color: {1};
padding-right: 10px; padding-left: 10px;
border-top: 2px solid {3};
border-left: 2px solid {3};
border-right: 2px solid {3};
}}

QTabBar::tab::disabled {{
background-color: gray;
}}


QWidget {{color: {2};background-color: {3}}}

""".format(
    get_color(blue_7), get_color(white), get_color(white), get_color(dark_gray)
)


StyleSheet_new_tab_dark_mode = """
QWidget {{color: {0}; background-color:{1}}}

QWidget::disabled {{background-color: lightGray}}

QButton {{background-color: {2}; color{0}}}

""".format(
    get_color(white), get_color(blue_7), get_color(dark_gray)
)



StyleSheet_tab_widget_themen_dark_mode = """
QTabBar::tab:selected {{
background: {0}; color: {1};
padding-right: 10px; padding-left: 10px; padding-bottom: 5px; padding-top: 5px;
border-top: 2px solid {3};
border-left: 2px solid {3};
border-right: 2px solid {3};
}}

QWidget {{color: {2};background-color: {3}}}




""".format(
    get_color(blue_7), get_color(white), get_color(white), get_color(dark_gray)
)



StyleSheet_button_check_all_dark_mode = "background-color: {}; ".format(get_color(dark_gray))




StyleSheet_unterkapitel_cria_dark_mode = "background-color: {}".format(get_color(blue_7))



StyleSheet_combobox_kapitel_dark_mode = "background-color: {0};selection-background-color: {1}; selection-color: {2}".format(
    get_color(dark_gray), get_color(blue_7), get_color(white)
)


StyleSheet_aufgaben_groupbox_dark_mode = "QGroupBox {{background-color: {0};}} ".format(get_color(blue_7))



StyleSheet_typ2_dark_mode = """
QGroupBox {{background-color: {0}; color: {1}}}
QLabel {{color:  {1}}}
""".format(
    get_color(blue_6), get_color(white)
)






StyleSheet_new_checkbox_dark_mode =  """
QToolTip {{ 
color: {0}; background-color: {1}; border: 0px; 
}} 

QCheckBox {{
padding-right: 10px; padding-bottom: 10px; color: {0}; 
}}

""".format(
    get_color(white),
    get_color(dark_gray),
)
 
# QCheckBox::indicator:checked {{
#     color: white
# }}

# QCheckBox::indicator {{
#     border: 1px solid {0} ; color: white;
# }}





StyleSheet_calender_dark_mode = """
QCalendarWidget QTableView 
{{
    alternate-background-color: {};
}}
""".format(get_color(blue_5))

StyleSheet_ausgleichspunkte_dark_mode = "color: white"
