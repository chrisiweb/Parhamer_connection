from PyQt5 import QtWidgets

SizePolicy_fixed = QtWidgets.QSizePolicy(
    QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
)
SizePolicy_fixed_height = QtWidgets.QSizePolicy(
    QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
)
SizePolicy_fixed_width = QtWidgets.QSizePolicy(
    QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding
)
SizePolicy_preferred = QtWidgets.QSizePolicy(
    QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
)
SizePolicy_preferred_width = QtWidgets.QSizePolicy(
    QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
)
SizePolicy_maximum = QtWidgets.QSizePolicy(
    QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum
)
SizePolicy_maximum_height = QtWidgets.QSizePolicy(
    QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum
)
SizePolicy_maximum_width = QtWidgets.QSizePolicy(
    QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding
)
SizePolicy_minimum = QtWidgets.QSizePolicy(
    QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum
)
SizePolicy_minimum_height = QtWidgets.QSizePolicy(
    QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
)
SizePolicy_minimum_width = QtWidgets.QSizePolicy(
    QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
)

