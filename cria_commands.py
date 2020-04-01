# from PyQt5 import QtCore, QtWidgets, QtGui
# import os
# from config import config_loader, path_programm

# config_file = os.path.join(path_programm, "_database", "_config", "config1.yml")

# list_klassen = config_loader(config_file, "list_klassen")
# dict_aufgabenformate = config_loader(config_file, "dict_aufgabenformate")


# for klasse in list_klassen:
#     exec('dict_{0} = config_loader(config_file,"dict_{0}")'.format(klasse))
#     exec('dict_{0}_name = config_loader(config_file,"dict_{0}_name")'.format(klasse))


# def create_kapitel_cria(layout, klasse, kapitel):
#     dict_klasse_name = eval("dict_k{}_name".format(klasse))
#     exec(
#         "self.radioButton_k{0}_{1} = QtWidgets.QRadioButton(self.scrollAreaWidgetContents_k{0})".format(
#             klasse, kapitel
#         )
#     )
#     radioButton_klasse_kapitel = eval(
#         "self.radioButton_k{0}_{1}".format(klasse, kapitel)
#     )
#     radioButton_klasse_kapitel.setObjectName("radioButton_klasse_kapitel")
#     # chosen_layout = eval('{0}_k{1}'.format(layout, klasse))
#     layout.addWidget(radioButton_klasse_kapitel)
#     radioButton_klasse_kapitel.setText(
#         _translate("MainWindow", dict_klasse_name[kapitel] + " (" + kapitel + ")")
#     )
#     # radioButton_klasse_kapitel.toggled.connect(
#     #     partial(self.chosen_radiobutton, klasse, kapitel)
#     # )