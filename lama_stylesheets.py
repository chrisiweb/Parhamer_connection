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
    get_color(blue_7), get_color(white), get_color(white), get_color(dark_gray)
)


# StyleSheet_tabWidget = """
# QTabBar::tab:selected {{
# background: {0}; color: {1};
# padding-right: 10px; padding-left: 10px;
# border-top: 2px solid {3};
# border-left: 2px solid {3};
# border-right: 2px solid {3};
# }}

# QTabBar::tab::disabled {{
# background-color: gray;
# }}


# QWidget {{color: {2};background-color: {3}}}

# """.format(
#     get_color(blue_2), get_color(black), get_color(white), get_color(blue_7)
# )

StyleSheet_new_tab = """
QWidget {{color: {0}; background-color:{1}}}

QWidget::disabled {{background-color: lightGray}}

QButton {{background-color: {2}; color{0}}}

""".format(
    get_color(white), get_color(blue_7), get_color(dark_gray)
)



# StyleSheet_new_tab = """
# QWidget {{color: {0}; background-color:{1}}}

# QWidget::disabled {{background-color: lightGray}}
# """.format(
#     get_color(black), get_color(blue_2)
# )





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
    get_color(blue_7), get_color(white), get_color(white), get_color(dark_gray)
)

# StyleSheet_tab_widget_themen = """
# QTabBar::tab:selected {{
# background: {0}; color: {1};
# padding-right: 10px; padding-left: 10px; padding-bottom: 5px; padding-top: 5px;
# border-top: 2px solid {3};
# border-left: 2px solid {3};
# border-right: 2px solid {3};
# }}

# QWidget {{color: {2};background-color: {3}}}

# """.format(
#     get_color(blue_2), get_color(black), get_color(white), get_color(blue_7)
# )

StyleSheet_button_check_all = "background-color: {}; ".format(get_color(dark_gray))

# StyleSheet_button_check_all = "background-color: {}; ".format(get_color(blue_3))


StyleSheet_unterkapitel_cria = "background-color: {}".format(get_color(blue_7))
# StyleSheet_unterkapitel_cria = "background-color: {}".format(get_color(blue_2))


StyleSheet_combobox_kapitel = "background-color: {0};selection-background-color: {1}; selection-color: {2}".format(
    get_color(white), get_color(blue_7), get_color(white)
)

# StyleSheet_combobox_kapitel = "background-color: {0};selection-background-color: {1}; selection-color: {2}".format(
#     get_color(white), selection_background_color, selection_text_color
# )

StyleSheet_aufgaben_groupbox = "QGroupBox {{background-color: {0};}} ".format(get_color(blue_7))

# StyleSheet_aufgaben_groupbox = "QGroupBox {{background-color: {0};}} ".format(get_color(blue_1))


StyleSheet_typ2 = """
QGroupBox {{background-color: {0}; color: {1}}}
QLabel {{color:  {1}}}
""".format(
    get_color(blue_5), get_color(white)
)

# StyleSheet_typ2 = """
# QGroupBox {{background-color: {0}; color: {1}}}
# QLabel {{color:  {1}}}
# """.format(
#     get_color(blue_3), get_color(black)
# )




StyleSheet_new_checkbox =  """
QToolTip {{ 
color: {0}; background-color: {1}; border: 0px; 
}} 

QCheckBox {{
padding-right: 10px; padding-bottom: 10px; color: {0}; 
}}

QCheckBox::indicator {{
    width: 13px;
    height: 13px;
}}

QCheckBox::indicator:unchecked {{
    color: white;background-color: white
}}

QCheckBox::indicator:unchecked:hover{{
    color: white;background-color: white
}}

QCheckBox::indicator:unchecked:pressed {{
    color: red;background-color: red
}}

QCheckBox::indicator:checked {{
    color: white;background-color: blue
}}
""".format(
    get_color(white),
    get_color(dark_gray),
)
 

# QCheckBox::indicator {{
#     border: 1px solid {0} ; color: white;
# }}




# StyleSheet_new_checkbox =  """
# QToolTip {{ 
# color: {0}; background-color: {1}; border: 0px; 
# }}       
# QCheckBox {{
# padding-right: 10px, padding-bottom: 10px
# }}
# """.format(
#     get_color(white),
#     get_color(blue_7)
# )

StyleSheet_calender = """
QCalendarWidget QTableView 
{{
    alternate-background-color: {};
}}
""".format(get_color(blue_5))

StyleSheet_ausgleichspunkte = "color: white"

# StyleSheet_ausgleichspunkte = "color: black"