from PyQt5.QtWidgets import QSizePolicy

SizePolicy_fixed = QSizePolicy(
    QSizePolicy.Fixed, QSizePolicy.Fixed
)
SizePolicy_fixed_height = QSizePolicy(
    QSizePolicy.Expanding, QSizePolicy.Fixed
)
SizePolicy_fixed_width = QSizePolicy(
    QSizePolicy.Fixed, QSizePolicy.Expanding
)
SizePolicy_preferred = QSizePolicy(
    QSizePolicy.Preferred, QSizePolicy.Preferred
)
SizePolicy_preferred_width = QSizePolicy(
    QSizePolicy.Preferred, QSizePolicy.Expanding
)
SizePolicy_maximum = QSizePolicy(
    QSizePolicy.Maximum, QSizePolicy.Maximum
)
SizePolicy_maximum_height = QSizePolicy(
    QSizePolicy.Expanding, QSizePolicy.Maximum
)
SizePolicy_maximum_width = QSizePolicy(
    QSizePolicy.Maximum, QSizePolicy.Expanding
)
SizePolicy_minimum = QSizePolicy(
    QSizePolicy.Minimum, QSizePolicy.Minimum
)
SizePolicy_minimum_height = QSizePolicy(
    QSizePolicy.Expanding, QSizePolicy.Minimum
)
SizePolicy_minimum_width = QSizePolicy(
    QSizePolicy.Minimum, QSizePolicy.Expanding
)

SizePolicy_minimum_fixed =QSizePolicy(
    QSizePolicy.Minimum, QSizePolicy.Fixed
)

SizePolicy_expanding = QSizePolicy(
    QSizePolicy.Expanding, QSizePolicy.Expanding
)