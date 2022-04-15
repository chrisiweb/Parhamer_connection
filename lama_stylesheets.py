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



    QToolButton {{
        background-color: #F4F4F9;
    }}

    QToolTip {{
        color: #F4F4F9; 
        background-color: #2F4550; 
        border: 0px;
        }}

    QCheckBox {{
        spacing: 0px;
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

    #frame_tab_widget_gk {{
        border-color: #6E8784;
        border-width: 1px;
        border-style: solid;
        border-radius: 4px;
        margin-top: 0.5em;
    }}

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
    }}

    QGroupBox::title{{
        top: -5px;
        left: 5px;
        padding-left: 3px;
        padding-right: 2px;    
    }}

    #combobox_searchtype {{
        padding-left: 5px;
        padding-right: 20px;
        padding-top: 2px;
        padding-bottom: 2px
    }}        

""".format(
    get_icon_path("chevron-left.svg"),
    get_icon_path("chevron-right.svg"),
    get_icon_path("square.svg"),
    get_icon_path("check-square.svg"),
    )






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

StyleSheet_new_tab = """
QWidget {{color: {0}; background-color:{1}}}

QWidget::disabled {{background-color: lightGray}}
""".format(
    get_color(black), get_color(blue_2)
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
