from config import get_color
from lama_colors import *

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
    get_color(white), get_color(blue_7), get_color(white)
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
