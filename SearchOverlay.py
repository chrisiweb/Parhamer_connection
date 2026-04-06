# SearchOverlay.py
from PyQt5.QtWidgets import (
    QWidget, QLineEdit, QHBoxLayout, QPushButton, QLabel
)
from PyQt5.QtCore import Qt, pyqtSignal


class SearchOverlay(QWidget):
    searchRequested = pyqtSignal(str)
    nextRequested = pyqtSignal()
    prevRequested = pyqtSignal()
    closeRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint      # bleibt oben
            | Qt.Window                      # eigener Fokus, aber schließt sich NICHT automatisch
        )


        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            QWidget {
                background: #ffffff;
                border: 1px solid #999;
                border-radius: 6px;
            }
            QLineEdit {
                border: none;
                padding: 6px;
                font-size: 14px;
                min-width: 160px;
            }
            QPushButton {
                border: none;
                padding: 6px 8px;
            }
            QPushButton:hover {
                background: #e5e5e5;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 5, 8, 5)
        layout.setSpacing(4)

        self.edt = QLineEdit()
        self.edt.setPlaceholderText("Suchen...")
        self.edt.textChanged.connect(self._trigger_search)
        layout.addWidget(self.edt)

        self.lbl_count = QLabel("")

        self.lbl_count.setStyleSheet("""
            QLabel {
                color: #666;
                padding: 0 4px;
                background: transparent;
                border: none;
            }
        """)
        self.lbl_count.hide()      # ✅ Ausblenden
        layout.addWidget(self.lbl_count)


        self.btn_prev = QPushButton("▲")
        self.btn_prev.clicked.connect(self.prevRequested.emit)
        layout.addWidget(self.btn_prev)

        self.btn_next = QPushButton("▼")
        self.btn_next.clicked.connect(self.nextRequested.emit)
        layout.addWidget(self.btn_next)

        self.btn_close = QPushButton("✕")
        self.btn_close.clicked.connect(self._close)
        layout.addWidget(self.btn_close)


    def _trigger_search(self):

        if self.edt.text().strip() == "":
            self.lbl_count.hide()
            self.searchRequested.emit("")   # ✅ Suche leeren → Canvas entfernt Markierungen

        text = self.edt.text().strip()
        self.searchRequested.emit(text)


    def _close(self):
        self.closeRequested.emit()
        self.hide()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self._close()
        else:
            super().keyPressEvent(e)



    def setCount(self, index, total):
        """index = aktueller Treffer (0-basiert), total = Anzahl Treffer"""
        if total == 0:
            self.lbl_count.setText("")
            self.lbl_count.hide()      # ✅ Ausblenden
        else:
            self.lbl_count.setText(f"{index+1} / {total}")
            self.lbl_count.show()      # ✅ Ausblenden
