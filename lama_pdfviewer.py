#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF-Viewer (PyQt5 + PyMuPDF) mit:
- moderner Toolbar (zentriert: Seite [aktuell editierbar] / [gesamt])
- Tastatur: ←/→ vorige/nächste Seite; Enter im Feld springt zur Seite
- links: Kopfbereich mit drei Zeilen (Farbkästchen + editierbarer Text)
         Standard: Rot/„Übungsblatt“, Gelb/„Schularbeit“, Grün/„Nachschularbeit“
         -> Farbe per Klick (QColorDialog), Text direkt änderbar
- darunter: Aufgabenliste (aus PDF-Überschriften)
  * Klick auf NICHT ausgewähltes Item -> nur Navigation (keine Farbänderung)
  * Klick auf bereits ausgewähltes Item -> Farbzyklus (Kategorie 1 -> 2 -> 3 -> Weiß -> …)
- Kein blaues Auswahl-Fill; nur Rahmen um das ausgewählte Item
- Zoom: Strg+Mausrad / Strg+Plus/Minus / Strg+0
"""

import os
import re
from config import get_icon_path
import fitz  # PyMuPDF
from PyQt5.QtWidgets import (
    QLabel, QWidget, QVBoxLayout,
    QToolBar, QLineEdit, QSizePolicy, QShortcut,
    QListWidget, QListWidgetItem, QSplitter, QHBoxLayout,
    QStyledItemDelegate, QStyle, QStyleOptionViewItem,
    QColorDialog, QPushButton, QGridLayout, QDialog, QCheckBox, QSpinBox, QToolButton, QMessageBox, QDialogButtonBox, QAbstractItemView
)
from PyQt5.QtGui import QPixmap, QImage, QKeySequence, QColor, QBrush, QPen, QIcon, QPainter
from PyQt5.QtCore import Qt, pyqtSignal, QRect, QModelIndex, QEvent, QTranslator, QLocale, QLibraryInfo, QObject, QPoint, QTimer
from config import logo_path, save_pdf_selection_dict, lama_pdf_selection_file
from PdfViewer_gui import PdfViewer
from create_new_widgets import create_new_label

import re

# ---------- Überschriften-Extraktion aus PDF ----------
_HEADING = re.compile(
    r"""(?xmi)
    ^
    (?P<full>

        #######################################################
        # (A) Kapitelbasierte Aufgaben: AG/WS/AN/FA 1.1 - 3...
        #######################################################
        (?:
            (?P<prefixA>AG|WS|AN|FA)        # feste Präfixe
            \s+
            (?P<chapter>\d+(?:\.\d+)*)      # Kapitelnummer
            \s*[-–—]\s*
            (?P<numA>
                \d+(?:\[\d+\])?             # 3 oder 3[1]
              | [il]\.\d+                   # i.74 oder l.74
            )
            (?:\s*[-–—]\s*.*)?              # optionaler Titel
        )

        |

        #######################################################
        # (B) Zusatzthemen: KKK - 1 - Titel, LGM1 - i.74 ...
        #######################################################
        (?:
            (?P<prefixB>[A-Z][A-Z0-9]{1,})  # beliebiges Kürzel ≥2 Zeichen
            \s*[-–—]\s*
            (?P<numB>
                \d+(?:\[\d+\])?
              | [il]\.\d+
            )
            (?:\s*[-–—]\s*.*)?
        )

        |

        #######################################################
        # (C) Rein numerische Aufgaben: 4 - Titel, 118[2] - ...
        #######################################################
        (?:
            (?P<numC>
                \d{1,3}(?:\[\d+\])?
              | [il]\.\d+                   # auch i.74 ohne Prefix erlauben
            )
            \s+[-–—]\s+
            .+                              # Titel muss folgen
        )

    )
    $
    """
)


# --- Neu: Deutsche Übersetzungen aktivieren ---------------------------------
def enable_german_ui(app):
    """
    Aktiviert die Qt-Übersetzungen (Deutsch) für Standard-Dialoge wie QColorDialog.
    Funktioniert mit PyQt5 5.15.x auf Windows 11.
    """
    # 1) Standard-Locale auf Deutsch (AT) setzen (DE ginge auch)
    QLocale.setDefault(QLocale(QLocale.German, QLocale.Austria))

    # 2) Übersetzungsverzeichnisse ermitteln
    candidates = []
    try:
        # Der offizielle Qt-Translations-Pfad
        candidates.append(QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    except Exception:
        pass
    # Fallback: PyQt5/Qt/translations relativ zum Paket
    try:
        import PyQt5
        candidates.append(os.path.join(os.path.dirname(PyQt5.__file__), "Qt", "translations"))
    except Exception:
        pass

    # 3) Benötigte Qt-Module laden: 'qtbase' deckt die meisten Widgets/Dialogs ab,
    #    'qt' ergänzt einige allgemeine Strings (optional, aber schadet nicht).
    loaded = []
    for base in ("qtbase", "qt"):
        tr = QTranslator(app)
        ok = False
        for path in candidates:
            if path and os.path.isdir(path):
                # Variante A: automatische Locale-Auswahl (z. B. qtbase_de.qm)
                if tr.load(QLocale(), base, "_", path):
                    ok = True
                    break
                # Variante B: explizit 'de' probieren
                if tr.load(f"{base}_de", path):
                    ok = True
                    break
        if ok:
            app.installTranslator(tr)
            loaded.append(tr)

    # Referenzen halten, damit die Translator-Objekte nicht vorzeitig ge-GCed werden
    app._de_translators = loaded


def normalize_heading(s: str) -> str:
    return (
        s.replace("–", "-")
         .replace("—", "-")
         .replace("‑", "-")
         .replace("‒", "-")
         .replace("−", "-")
         .replace("\u2212", "-")
         .replace("\xad", "")   # Soft hyphen
    )


def extract_headings_with_positions(pdf_path: str):
    results = []
    seen = set()

    with fitz.open(pdf_path) as doc:
        for pno in range(len(doc)):
            page = doc[pno]
            text = page.get_text("text") or ""
            if not text:
                continue

            for raw_line in text.splitlines():
                line = raw_line.strip()
                if not line:
                    continue

                m = _HEADING.match(line)
                if not m:
                    continue

                full = m.group("full").strip()
                key = (full, pno)
                if key in seen:
                    continue
                seen.add(key)

                
                try:
                    rects = []  # ✅ rects JEDES MAL zurücksetzen

                    norm_full = normalize_heading(full)
                    norm_page_text = normalize_heading(page.get_text("text"))

                    y_ratio = None

                    if norm_full in norm_page_text:
                        rects = page.search_for(norm_full)
                        if rects:
                            r0 = rects[0]
                            if page.rect.height > 0:
                                y_ratio = r0.y0 / page.rect.height

                except:
                    y_ratio = None

                results.append((full, pno + 1, y_ratio))

    return results


# ---------- Delegate: malt stets Item-Farbe + nur Rahmen bei Auswahl ----------
class ColorAwareBorderDelegate(QStyledItemDelegate):
    def __init__(self, border_color="#0078D4", border_width=2, radius=6, parent=None):
        super().__init__(parent)
        self._border = QColor(border_color)
        self._bw = border_width
        self._r = radius

    def paint(self, painter, option: QStyleOptionViewItem, index: QModelIndex):
        # Hintergrund (Model-Farbe) malen
        bg = index.data(Qt.BackgroundRole)
        painter.save()
        painter.fillRect(option.rect, bg if isinstance(bg, QBrush) else Qt.white)
        painter.restore()

        # Inhalt ohne Hover/Selected-Fill zeichnen
        opt = QStyleOptionViewItem(option)
        opt.state &= ~QStyle.State_MouseOver
        opt.state &= ~QStyle.State_Selected
        opt.state &= ~QStyle.State_HasFocus
        super().paint(painter, opt, index)

        # Auswahl-Rahmen
        if option.state & QStyle.State_Selected:
            painter.save()
            painter.setPen(QPen(self._border, self._bw))
            r = option.rect.adjusted(2, 2, -2, -2)
            painter.drawRoundedRect(r, self._r, self._r)
            painter.restore()


# ---------- Header-Widget mit 3 Zeilen (Farbkästchen + editierbarer Text) ----------

class CategoryHeaderWidget(QWidget):
    """
    Drei Zeilen:
      [Checkbox] [Farbkästchen] [editierbarer Text]
    - Checkbox steuert Sichtbarkeit & Verfügbarkeit der jeweiligen Farbe.
    Signale:
      - colorChanged(index:int, color:QColor)
      - labelChanged(index:int, text:str)
      - categoryToggled(index:int, enabled:bool)
    Zugriff:
      - colors() -> List[QColor]
      - labels() -> List[str]
      - categoryEnabled(i) -> bool
      - enabledMask() -> int (Bitmaske, Bit0=Rot, Bit1=Gelb, Bit2=Grün)
    """

    colorChanged    = pyqtSignal(int, QColor)   # 0..2
    labelChanged    = pyqtSignal(int, str)      # 0..2
    categoryToggled = pyqtSignal(int, bool)     # 0..2, enabled
    trashClicked = pyqtSignal(int)   # index 0..2

    def __init__(self, counts, dict_pdf_chosen_examples, typ, parent=None):
        super().__init__(parent)
        self.dict_pdf_chosen_examples = dict_pdf_chosen_examples
        self.typ = typ
        if counts is None:
            counts = [0, 0, 0]

        self._counts = counts


        self._colors = [
            QColor(self.dict_pdf_chosen_examples[self.typ]["colors"].get(1, "#d3f9d8")),
            QColor(self.dict_pdf_chosen_examples[self.typ]["colors"].get(2, "#ffd6d6")),
            QColor(self.dict_pdf_chosen_examples[self.typ]["colors"].get(3, "#fff3bf")),
        ]


        # if "colors" in dict_pdf_chosen_examples[self.typ]:
        #     for i in range(3):
        #         hexcol = dict_pdf_chosen_examples[self.typ]["colors"].get(i+1)
        #         if hexcol:
        #             self._colors[i] = QColor(hexcol)

        self._labels = [
            self.dict_pdf_chosen_examples[self.typ]["names"][1],
            self.dict_pdf_chosen_examples[self.typ]["names"][2],
            self.dict_pdf_chosen_examples[self.typ]["names"][3],
        ]

        self._enabled = [
            self.dict_pdf_chosen_examples[self.typ]["enabled"][1],
            self.dict_pdf_chosen_examples[self.typ]["enabled"][2], 
            self.dict_pdf_chosen_examples[self.typ]["enabled"][3],
        ]  # standardmäßig alle aktiv

        grid = QGridLayout(self)
        grid.setContentsMargins(8, 8, 8, 8)
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(8)

        grid.setColumnMinimumWidth(0, 36)      # <<--- NEU: Platz für das Kästchen
        grid.setColumnStretch(2, 1)

        self._checks = []
        self._btns   = []
        self._edits  = []

        for i in range(3):
            # Checkbox
            chk = QCheckBox()
            chk.setChecked(self._enabled[i])

            chk.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            # Indicator-Größe explizit auf DPI-freundliche Maße setzen:



            chk.setStyleSheet("""
                QCheckBox { padding: 0px; }
                QCheckBox::indicator {
                    width: 22px; height: 22px;      /* gut sichtbar */
                    margin-left: 2px; margin-right: 4px;
                    subcontrol-position: left;       /* explizit links */
                }
            """)




            chk.toggled.connect(lambda state, ix=i: self._on_toggle(ix, state))
            self._checks.append(chk)
            grid.addWidget(chk, i, 0)


            # Farbkastl als Label mit Zahl
            count_value = self._counts[i]
            lbl = create_new_label(
                None,
                str(count_value),
                clickable=True
                )
            lbl.setFixedSize(26, 20)  # etwas breiter, damit Zahl reinpasst
            lbl.setAlignment(Qt.AlignCenter)
            lbl.clicked.connect(lambda ix=i: self._pick_color(ix))
            # Farbe + Zahl vorbereiten
            
            # count_value = [self.parent().len_list_1,
            #             self.parent().len_list_2,
            #             self.parent().len_list_3][i]

            # lbl.setText(str(count_value))
            lbl.setToolTip("")  # wird später dynamisch befüllt

            lbl.setStyleSheet(self._label_style(self._colors[i], self._enabled[i]))

            self._btns.append(lbl)
            grid.addWidget(lbl, i, 1)

            # btn = QPushButton("")
            # btn.setFixedSize(20, 20)
            # btn.setCursor(Qt.PointingHandCursor)
            # btn.setStyleSheet(self._btn_style(self._colors[i], enabled=True))
            # # btn.clicked.connect(lambda _, ix=i: self._pick_color(ix))

            # btn.setAutoDefault(False)          # verhindert Auto-Default-Verhalten
            # btn.setDefault(False)              # kein Default-Button
            # btn.setFocusPolicy(Qt.NoFocus)     # Button bekommt keinen Tastatur-Fokus

            # self._btns.append(btn)
            # grid.addWidget(btn, i, 1)

            # Editierbarer Titel
            edit = QLineEdit(self._labels[i])
            edit.setEnabled(self._enabled[i])
            edit.setPlaceholderText("Bezeichnung eingeben…")
            edit.textEdited.connect(lambda txt, ix=i: self._on_label(ix, txt))
            self._edits.append(edit)
            grid.addWidget(edit, i, 2)

            # --- Trash-Button ---
            btn_trash = QPushButton()
            btn_trash.setIcon(QIcon(get_icon_path("trash-2.svg")))   # ← dein Icon
            btn_trash.setFixedSize(26, 26)
            btn_trash.setStyleSheet("border: none;")
            btn_trash.setCursor(Qt.PointingHandCursor)
    

            btn_trash.setStyleSheet("""
                QPushButton {
                    background: #f5f5f5;
                    border: 1px solid #cccccc;
                    border-radius: 6px;
                    padding: 3px;
                }
                QPushButton:hover {
                    background: #ffffff;
                    border: 1px solid #999999;
                }
                QPushButton:pressed {
                    background: #e0e0e0;
                    border: 1px solid #888888;
                }
            """)


            # Callback zum Hauptfenster durchreichen
            btn_trash.clicked.connect(lambda _, ix=i: self._on_trash_clicked(ix))

            grid.addWidget(btn_trash, i, 3)            

        # Spalten: 0 = Checkbox (schmal), 1 = Kastl, 2 = Edit (flexibel)
        grid.setColumnStretch(2, 1)

        # dezente Linie unten
        sep = QWidget()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background:#e5e5e5; margin:0px;")
        grid.addWidget(sep, 3, 0, 1, 3)

    # ---------- Helper ----------

    def markingEnabled(self) -> bool:
        """Kompatibilitäts-Helper: 'global aktiv' = mindestens eine Kategorie aktiv."""
        return any(self._enabled)



    def updateCounts(self, counts, dict_pdf_chosen_examples, typ):
        self._counts = counts

        for i, lbl in enumerate(self._btns):
            lbl.setText(str(counts[i]))

            if dict_pdf_chosen_examples:
                items = dict_pdf_chosen_examples[typ]["lists"][i+1]
                lbl.setToolTip("\n".join(items) if items else "")

            # ✅ wichtig: erneut Stylesheet setzen, damit es NIE verloren geht
            lbl.setStyleSheet(self._label_style(self._colors[i], self._enabled[i]))

        save_pdf_selection_dict(lama_pdf_selection_file, self.dict_pdf_chosen_examples)
                        
    def _on_trash_clicked(self, index: int):
        self.trashClicked.emit(index)
    
    # def update_header_counts(self):
    #     counts = [self.len_list_1, self.len_list_2, self.len_list_3]
    #     for i, lbl in enumerate(self.header._btns):
    #         lbl.setText(str(counts[i]))

    def _label_style(self, color: QColor, enabled: bool) -> str:
        base = color.name() if enabled else "#dbdbdb"
        border = "1px solid #c8c8c8" if enabled else "1px dashed #999"
        opacity = "" if enabled else "opacity: 0.45;"

        return f"""
            QLabel {{
                background: {base};
                border: {border};
                border-radius: 4px;
                {opacity}
            }}

            QToolTip {{
                color: #F4F4F9;
                background-color: #2F4550;
                border: 0px;
                padding: 6px;
                font-size: 12px;
            }}
        """


    ### FARBAUSWAHL WORKING!!! >>>> OPTIONEN!
    def _pick_color(self, index: int):
        start = self._colors[index]

        # 🔹 ColorDialog mit "Standard wiederherstellen"
        dlg = QColorDialog(start, self)
        dlg.setOption(QColorDialog.ShowAlphaChannel, False)

        # reset_btn = dlg.findChild(QPushButton, "qt_colorreset")
        # if reset_btn is None:
        reset_btn = QPushButton("Standard wiederherstellen", dlg)
        # reset_btn.setObjectName("qt_colorreset")
        # dlg.layout().addWidget(reset_btn)

        def reset_color():
            # Standardfarben
            defaults = {
                0: "#d3f9d8",
                1: "#ffd6d6",
                2: "#fff3bf"
            }
            col = QColor(defaults[index])
            self._colors[index] = col
            self._btns[index].setStyleSheet(self._label_style(col, self._enabled[index]))

            # ✅ auch im JSON speichern
            self.dict_pdf_chosen_examples[self.typ]["colors"][index+1] = col.name()

            save_pdf_selection_dict(lama_pdf_selection_file, self.dict_pdf_chosen_examples)
            self.colorChanged.emit(index, col)
            dlg.close()

        reset_btn.clicked.connect(reset_color)


        # ---- ButtonBox finden ----
        buttonbox = None
        for child in dlg.children():
            if isinstance(child, QDialogButtonBox):
                buttonbox = child
                break

        # ---- Untere Zeile bauen: [Standard] ... [OK][Abbrechen] ----
        bottom = QHBoxLayout()
        bottom.addWidget(reset_btn)
        bottom.addStretch()
        bottom.addWidget(buttonbox)

        dlg.layout().addLayout(bottom)

        if dlg.exec_():
            col = dlg.currentColor()
            if col.isValid():
                # ✅ 1. interne Farbe setzen
                self._colors[index] = col

                # ✅ 2. Kasten einfärben
                self._btns[index].setStyleSheet(self._label_style(col, self._enabled[index]))

                # ✅ 3. In JSON speichern
                self.dict_pdf_chosen_examples[self.typ]["colors"][index+1] = col.name()

                save_pdf_selection_dict(lama_pdf_selection_file, self.dict_pdf_chosen_examples)

                # ✅ 4. Items neu einfärben
                self.colorChanged.emit(index, col)


    def _on_label(self, index: int, text: str):
        self._labels[index] = text

        self.dict_pdf_chosen_examples[self.typ]["names"][index+1] = text
        save_pdf_selection_dict(lama_pdf_selection_file, self.dict_pdf_chosen_examples) 
        
        self.labelChanged.emit(index, text)

    def _on_toggle(self, index: int, state: bool):
        self._enabled[index] = state
        self._edits[index].setEnabled(state)
        col = self._colors[index]
        lbl = self._btns[index]
        base = self._colors[index].name()

        lbl.setStyleSheet(self._label_style(QColor(base), state))

        self.dict_pdf_chosen_examples[self.typ]["enabled"][index+1] = state

        save_pdf_selection_dict(lama_pdf_selection_file, self.dict_pdf_chosen_examples)        
        self.categoryToggled.emit(index, state)

    # ---------- API ----------
    def colors(self): return list(self._colors)
    def labels(self): return list(self._labels)
    def categoryEnabled(self, i: int) -> bool: return bool(self._enabled[i])
    def enabledMask(self) -> int:
        # Bit0=Rot, Bit1=Gelb, Bit2=Grün
        mask = 0
        for i, en in enumerate(self._enabled):
            if en: mask |= (1 << i)
        return mask
    

class _CtrlWheelFilter(QObject):
    """Fängt STRG+Mausrad am Viewport ab und delegiert ans PdfWidget (kein Scrollen)."""
    def __init__(self, pdf_widget, parent=None):
        super().__init__(parent)
        self._pdf = pdf_widget

    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.Wheel:
            if ev.modifiers() & Qt.ControlModifier:
                # unser eigenes Zoom-Handling; verhindert Standard-Scrollen
                self._pdf._on_ctrl_wheel(ev)
                return True  # Event konsumiert -> QScrollArea scrollt NICHT
        return False



# # --- nötige Imports ---
# import os
# from PyQt5 import QtCore, QtWidgets
# from PyQt5.QtCore import Qt, QEvent
# from PyQt5.QtGui import QKeySequence, QColor
# from PyQt5.QtWidgets import (
#     QDialog, QWidget, QVBoxLayout, QHBoxLayout, QToolBar, QStatusBar, QSplitter,
#     QLabel, QLineEdit, QSizePolicy, QShortcut, QListWidget, QListWidgetItem
# )

# Annahme: Diese Klassen/Funktionen existieren in deinem Projekt:
# - CategoryHeaderWidget  (mit .colors() und .colorChanged/.labelChanged)
# - ColorAwareBorderDelegate
# - PdfWidget             (mit .pageCount(), .currentPageChanged, .scrollToPage(), .scrollToPageLocation(), .gotoPrev(), .gotoNext())
# - extract_headings_with_positions(pdf_path) -> [(text, page, y_ratio_or_None), ...]

class PageImage(QLabel):
    """
    QLabel, das echte Textmarkierung als temporäre UI-Selektion ermöglicht:
    - gelbe rechteckige Markierung um Wörter
    - verschwindet beim nächsten Klick
    - KEINE PDF-Annotation
    - Cursorwechsel Crosshair/IBeam
    """
    selectionMade = pyqtSignal(int, list)   # <<< WICHTIG! Das fehlte bei dir.

    def __init__(self, pdfw, page_index, pixmap, parent=None):
        super().__init__(parent)
        self._pdfw = pdfw
        self._page_index = page_index

        if isinstance(pixmap, QPixmap):
            self.setPixmap(pixmap)
        else:
            self.setPixmap(QPixmap())   # leerer Platzhalter


        self.setStyleSheet("background: transparent;")
        self.setAlignment(Qt.AlignCenter)
        self.setCursor(Qt.IBeamCursor)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._selected_text = ""
        self.setFocusPolicy(Qt.ClickFocus) 

        self._dragging = False
        self._p0 = None
        self._p1 = None

        self._temp_label_rects = []     # Live während der Auswahl
        self._final_label_rects = []    # Sichtbare Markierung
        self.setCursor(Qt.IBeamCursor)

    def mousePressEvent(self, ev):
        if ev.button() == Qt.LeftButton:
            self._final_label_rects = []
            self._temp_label_rects = []
            self.update()

            self._dragging = True
            self._p0 = ev.pos()
            self._p1 = ev.pos()
            
            # ✅ Cursor bleibt Textcursor (KEIN Crosshair)
            self.setCursor(Qt.IBeamCursor)
            self.setFocus(Qt.MouseFocusReason)

        super().mousePressEvent(ev)


    def mouseMoveEvent(self, ev):
        if self._dragging:
            self._p1 = ev.pos()

            # Wörter automatisch bestimmen
            _pdf_rects, label_rects = self._pdfw.compute_smart_selection(
                self._page_index,
                self._p0,
                self._p1,
                self
            )
            self._temp_label_rects = label_rects
            self.update()
        super().mouseMoveEvent(ev)


    def mouseReleaseEvent(self, ev):
        if ev.button() == Qt.LeftButton and self._dragging:
            self._dragging = False
            self.setCursor(Qt.IBeamCursor)


            if (self._p0 - self._p1).manhattanLength() >= 6:
                pdf_rects, label_rects = self._pdfw.compute_smart_selection(
                    self._page_index, self._p0, self._p1, self
                )
                self._final_label_rects = label_rects

                # 🔹 Text extrahieren & merken
                self._selected_text = self._pdfw.extract_text_from_pdf_rects(
                    self._page_index, pdf_rects
                )
                # 🔹 Optional auch zentral im PdfWidget merken (für globalen Shortcut)
                self._pdfw._last_selected_text = self._selected_text


            else:
                # Klick ohne Auswahl → alles löschen
                self._final_label_rects = []
                self._selected_text = ""

            self._temp_label_rects = []
            self.update()

        super().mouseReleaseEvent(ev)


    def paintEvent(self, ev):
        super().paintEvent(ev)

        from PyQt5.QtGui import QPainter, QColor
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, False)
        p.setPen(Qt.NoPen)

        # ✅ DEZENTES HELLBLAU für Live-Vorschau
        p.setBrush(QColor(150, 200, 255, 100))
        for r in self._temp_label_rects:
            p.drawRect(r)

        # ✅ DEZENTES HELLBLAU für finale Auswahl
        p.setBrush(QColor(150, 200, 255, 140))
        for r in self._final_label_rects:
            p.drawRect(r)

        p.end()

    def copy_to_clipboard(self):
        from PyQt5.QtWidgets import QApplication
        QApplication.clipboard().setText(self._selected_text or "")

    def keyPressEvent(self, ev):
        if ev.matches(QKeySequence.Copy):
            self.copy_to_clipboard()
            return
        super().keyPressEvent(ev)

class _PressStateFilter(QObject):
    def __init__(self, viewport):
        # Parent ist der Viewport -> Filter wird zusammen mit ihm gelöscht.
        super().__init__(viewport)
        self.pressed_item = None
        self.was_selected = False

    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.MouseButtonPress:
            # obj ist der Viewport; parent() ist die QListWidget
            lw = obj.parent()
            item = lw.itemAt(ev.pos()) if lw is not None else None
            self.pressed_item = item
            self.was_selected = bool(item and item.isSelected())
        return False



class TagPopup(QWidget):
    """
    Dynamisches Popup für Kategorien:
     - categories: Liste von (tagname, labeltext)
     - tags: set() mit aktiven Kategorien
     - on_change: Callback bei Änderung
    """

    def __init__(self, parent, tags: set, categories: list, on_change):
        super().__init__(parent, Qt.Popup)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()
        self.tags = tags
        self.on_change = on_change
        self.categories = categories   # [(tagname, label), ...]

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)

        # Checkboxen dynamisch bauen
        self.checkboxes = {}

        for tagname, label in categories:
            cb = QCheckBox(label)
            cb.setChecked(tagname in tags)
            cb.stateChanged.connect(lambda _, t=tagname: self._update(t))
            layout.addWidget(cb)
            self.checkboxes[tagname] = cb

    def _update(self, tagname):
        if tagname in self.tags:
            self.tags.discard(tagname)
        else:
            self.tags.add(tagname)
        self.on_change()

        ## Schließt nach der Auwahl
        self.close()


    def keyPressEvent(self, ev):
        key = ev.key()

        # 1,2,3 → die drei Kategorien toggeln
        if key in (Qt.Key_1, Qt.Key_2, Qt.Key_3):
            index = key - Qt.Key_1  # 0,1,2

            if 0 <= index < len(self.categories):
                tagname, _ = self.categories[index]

                # Toggle wie Checkbox
                if tagname in self.tags:
                    self.tags.remove(tagname)
                else:
                    self.tags.add(tagname)

                # Callback ausführen
                self.on_change()

            # Popup sofort schließen (genau wie bei Checkbox-Klick)
            self.close()
        else:
            super().keyPressEvent(ev)

class _BlockNumberNavigation(QObject):
    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.KeyPress:
            # 1,2,3 sollen NICHT die Auswahl im QListWidget verändern
            if ev.key() in (Qt.Key_1, Qt.Key_2, Qt.Key_3):
                return True  # Event wird abgefangen → NICHT weitergeben
        return False


class Ui_Dialog_pdfviewer(object):
    ROLE_TARGET = Qt.UserRole          # (page, y_ratio)
    ROLE_COLORSTATE = Qt.UserRole + 1  # 0..3 (0=weiß,1=cat0,2=cat1,3=cat2)

    def setupUi(self, Dialog: QDialog, file_path: str, dict_pdf_chosen_examples, typ, show_selection_list=False, gesammeltedateien=None):
        self.gesammeltedateien = gesammeltedateien or []
        # --- State ---
        if typ != 'cria':
            self.typ = 'lama'
        else:
            self.typ = typ

        self._current_pdf_path = file_path
        self.show_selection_list = show_selection_list
        self._manual_selection = False
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("PDF Viewer")
        Dialog.setWindowIcon(QIcon(logo_path))  # logo_path muss gültig sein
       
        Dialog.setStyleSheet("""
            QToolTip {
                color: #F4F4F9;
                background-color: #2F4550;
                border: 0px;
                padding: 6px;
                font-size: 12px;
            }
        """)

        # --- Hauptlayout ---
        main = QVBoxLayout(Dialog)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        # --- Toolbar (oben) ---
        tb = QToolBar(self.Dialog)
        tb.setMovable(False)
        tb.setFloatable(False)
        main.addWidget(tb)

        spacer_left = QWidget(); spacer_left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        tb.addWidget(spacer_left)

        center = QWidget(); row_layout = QHBoxLayout(center)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(6)

        # self.edt_current = QLineEdit()
        # self.edt_current.setFixedWidth(56)
        # self.edt_current.setAlignment(Qt.AlignCenter)
        # self.edt_current.setToolTip("Aktuelle Seite (Enter zum Springen)")

        self.spin_page = QSpinBox()
        self.spin_page.setButtonSymbols(QSpinBox.NoButtons)     # „modern“ ohne kleine Pfeile; weglassen, wenn du Pfeile willst
        self.spin_page.setFixedWidth(56)
        self.spin_page.setAlignment(Qt.AlignCenter)
        self.spin_page.setMinimum(1)                             # Range kommt unten nach dem Laden
        self.spin_page.setToolTip("Aktuelle Seite • Eingabe = springen")

        self.lbl_total = QLabel("/ 1")
        self.lbl_total.setStyleSheet("color:#666;")

        row_layout.addWidget(self.spin_page)
        row_layout.addWidget(self.lbl_total)

        # ---- Zoom Buttons (rechts neben Seitenangabe) ----
        # from PyQt5.QtWidgets import QToolButton
        # from PyQt5.QtGui import QIcon, QKeySequence

        btn_zoom_out = QToolButton(center)
        btn_zoom_out.setIcon(QIcon(get_icon_path('zoom-out.svg')))
        btn_zoom_out.setToolTip("Verkleinern (Strg + -)")
        row_layout.addWidget(btn_zoom_out)

        btn_zoom_in = QToolButton(center)
        btn_zoom_in.setIcon(QIcon(get_icon_path('zoom-in.svg')))
        btn_zoom_in.setToolTip("Vergrößern (Strg + +)")
        row_layout.addWidget(btn_zoom_in)

        # Verbindungen
        btn_zoom_out.clicked.connect(lambda: self.viewer.zoom_out())
        btn_zoom_in.clicked.connect(lambda: self.viewer.zoom_in())

        # (optional) Shortcuts
        btn_zoom_in.setShortcut(QKeySequence.ZoomIn)
        btn_zoom_out.setShortcut(QKeySequence.ZoomOut)

        # row_layout.addWidget(self.edt_current)
        # row_layout.addWidget(self.lbl_total)
        tb.addWidget(center)

        spacer_right = QWidget(); spacer_right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        tb.addWidget(spacer_right)

        # --- Linkes Panel: Header + Liste ---

        self.list = QListWidget()
        self.list.setAlternatingRowColors(False)
        self.list.setSelectionBehavior(self.list.SelectionBehavior.SelectItems)
        self.list.setSelectionMode(self.list.SelectionMode.SingleSelection)
        self.list.setUniformItemSizes(True)
        self.list.setStyleSheet("""
            QListWidget {
                border: none;
                padding: 6px 4px;
                background: white;
            }
            QListWidget::item { padding: 6px 8px; }
        """)
        self.list.setItemDelegate(
            ColorAwareBorderDelegate(border_color="#0078D4", border_width=2, radius=6, parent=self.list)
        )

        self.list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list.customContextMenuRequested.connect(self._on_list_context_menu)
        self.list.currentRowChanged.connect(self.selected_item_changed)

        # self.icon_green  = make_square(QColor("#b7f5a9"))
        # self.icon_red    = make_square(QColor("#ffb4b4"))
        # self.icon_yellow = make_square(QColor("#ffeaa2"))        
        self.dict_pdf_chosen_examples = dict_pdf_chosen_examples
        self.len_list_1 = len(self.dict_pdf_chosen_examples[self.typ]['lists'][1])
        self.len_list_2 = len(self.dict_pdf_chosen_examples[self.typ]['lists'][2])
        self.len_list_3 = len(self.dict_pdf_chosen_examples[self.typ]['lists'][3])

        self.header = CategoryHeaderWidget(
            counts=[self.len_list_1, self.len_list_2, self.len_list_3],
            dict_pdf_chosen_examples=self.dict_pdf_chosen_examples,
            typ=self.typ
        )


        # ✅ Farben aus JSON laden
        saved_colors = self.dict_pdf_chosen_examples[self.typ]["colors"]
        for i in range(3):
            hexcol = saved_colors.get(i+1)
            if hexcol:
                col = QColor(hexcol)
                self.header._colors[i] = col
                self.header._btns[i].setStyleSheet(
                    self.header._label_style(col, self.header._enabled[i])
                )

        self.left_panel = QWidget()
        left_layout = QVBoxLayout(self.left_panel)
        # WICHTIG: links etwas Luft, damit Checkbox-Indikatoren nicht abgeschnitten werden
        left_layout.setContentsMargins(12, 0, 0, 0)   # ← 12px linker Innenabstand
        left_layout.setSpacing(0)
        left_layout.addWidget(self.header)
        left_layout.addWidget(self.list)
                


        # --- Rechte Seite: PDF-Viewer ---
        self.viewer = PdfViewer(self._current_pdf_path, ui_dialog=self, tindb_data = self.gesammeltedateien)
        self.viewer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.spin_zoom.setValue(self.viewer.get_zoom_percent())
        # --- Splitter (Mitte) ---
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.left_panel)
        self.splitter.addWidget(self.viewer)

        # if not self.show_selection_list:
        #     self._lehide_splitter_hand()

        self.splitter.setStretchFactor(0, 0)   # linkes Panel
        self.splitter.setStretchFactor(1, 1)   # Viewer dehnt
        self.splitter.setSizes([300, 2000])    # Start: viel Platz rechts

        if not self.show_selection_list:
            self.left_panel.hide()
            self.splitter.handle(1).setEnabled(False)
            # self.splitter.handle(1).setStyleSheet("background: transparent; width: 0px; image: none")
            self.splitter.setSizes([0, 1_000_000])
    #             QSplitter::handle {{
    #     # image: url({get_icon_path("more-vertical.svg")});
    # }}  

        # --- Zentrale Fläche ---
        central = QWidget()
        lay = QHBoxLayout(central)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.splitter)
        main.addWidget(central)

        # --- Initialwerte (Toolbar) ---
        total = self.viewer.pageCount()
        self.lbl_total.setText(f"/ {total}")
        self.spin_page.blockSignals(True)
        self.spin_page.setMaximum(max(1, total))
        self.spin_page.setValue(1)
        self.spin_page.blockSignals(False)

        # --- Liste initial befüllen (NACH Aufbau, VOR Signal-Connects!) ---
        self._fill_tasks_from_pdf(self._current_pdf_path)

        # Liste: Aufgabe → PDF-Seite
        # --- Task-Positionsliste NEU aufbauen ---
        self.task_positions = []
        for row in range(self.list.count()):
            item = self.list.item(row)
            page, y_ratio = item.data(self.ROLE_TARGET)
            self.task_positions.append({
                "row": row,
                "page": page,
                "ratio": y_ratio
            })


        self._restore_selections_from_dict()


        # --- Beim ersten Anzeigen: erste Aufgabe auswählen ---
        if self.list.count() > 0:
            self.list.setCurrentRow(0)
            first_page, first_ratio = self.list.item(0).data(self.ROLE_TARGET)
            self.viewer.scrollToPageLocation(first_page, first_ratio)

        # # Viewer -> Spinbox (Scrollen/Seitenwechsel aktualisiert Anzeige)
        # self.viewer.currentPageChanged.connect(self._on_current_page_changed)



        # --- Verbindungen & Event-Filter (erst jetzt!) ---
        # Toolbar-Interaktion
        self.viewer.currentPageChanged.connect(self._on_current_page_changed)
        # Spinbox -> Viewer (Eingabe springt)
        self.spin_page.valueChanged.connect(self._on_spin_value_changed)
        # self.edt_current.returnPressed.connect(self._jump_to_entered_page)


        # Shortcuts
        sc_left  = QShortcut(QKeySequence(Qt.Key_Left),  self.Dialog, activated=self.viewer.gotoPrev)
        sc_right = QShortcut(QKeySequence(Qt.Key_Right), self.Dialog, activated=self.viewer.gotoNext)

        # Kontext auf Anwendungsebene -> wird nicht von fokussierten Widgets geschluckt
        sc_left.setContext(Qt.ApplicationShortcut)
        sc_right.setContext(Qt.ApplicationShortcut)


        # Click-Logik mit robustem Press-Filter (am viewport parenten)
        vp = self.list.viewport()
        self._pressFilter = _PressStateFilter(vp)  # QObject-Filter, parent = viewport
        vp.installEventFilter(self._pressFilter)
        self.list.itemClicked.connect(self._on_task_clicked)

        # verhindert, dass 1/2/3 die Listen-Auswahl verändern
        self._numberBlocker = _BlockNumberNavigation()
        self.list.installEventFilter(self._numberBlocker)

        # Header-Änderungen -> Anzeige aktualisieren
        self.header.categoryToggled.connect(self._on_category_toggled)
        self.header.colorChanged.connect(self._on_category_color_changed)
        self.header.labelChanged.connect(self._on_category_label_changed)
        self.header.trashClicked.connect(self._on_header_trash_clicked)
        # (optional, wenn noch genutzt) globaler Shim:
        # self.header.markingToggled.connect(self._on_marking_toggled)
        # Buttons -> Viewer
        # actZoomOut.triggered.connect(lambda: self._on_zoom_button(False))
        # actZoomIn.triggered.connect(lambda: self._on_zoom_button(True))

        # SpinBox -> Viewer
        # self.spin_zoom.valueChanged.connect(self._on_zoom_spin_changed)

        # Viewer -> SpinBox (wenn via Rad/Shortcuts gezoomt wurde)
        # self.viewer.zoomChanged.connect(self._on_viewer_zoom_changed)
        # --- Start ---
        Dialog.showMaximized()
        # ✅ MoveEvent des echten Dialogs überwachen
        Dialog.moveEvent = self._on_dialog_moved


        # 🔹 Strg+C überall im Dialog -> kopiert die aktuelle Bildauswahl
        sc_copy = QShortcut(QKeySequence.Copy, self.Dialog)
        sc_copy.setContext(Qt.ApplicationShortcut)

        class ArrowKeyFilter(QObject):
            def __init__(self, ui):
                super().__init__(ui.Dialog)
                self.ui = ui

            def eventFilter(self, obj, ev):
                if ev.type() != QEvent.KeyPress:
                    return False

                key = ev.key()
                if key not in (Qt.Key_Up, Qt.Key_Down):
                    return False

                # linkes Panel nicht sichtbar → abbrechen
                if not self.ui.left_panel.isVisible():
                    return False

                lw = self.ui.list
                row = lw.currentRow()
                if row < 0:
                    return False

                # neue Zeile bestimmen
                if key == Qt.Key_Up:
                    new_row = max(0, row - 1)
                else:
                    new_row = min(lw.count() - 1, row + 1)

                lw.setCurrentRow(new_row)
                item = lw.item(new_row)

                # ✅ HIER die Korrektur:
                page, ratio = item.data(self.ui.ROLE_TARGET)

                # PDF anspringen
                self.ui.viewer.scrollToPageLocation(page, ratio)

                return True
            

            
        self._arrowFilter = ArrowKeyFilter(self)
        Dialog.installEventFilter(self._arrowFilter)





        def _on_copy():
            from PyQt5.QtWidgets import QApplication

            # 1) Canvas direkt fragen
            if hasattr(self.viewer, "canvas"):
                txt = self.viewer.canvas.selected_text
                if txt:
                    QApplication.clipboard().setText(txt)
                    return

            # 2) Falls später weitere Viewer-Arten vorhanden wären
            if hasattr(self.viewer, "get_last_selected_text"):
                txt = self.viewer.get_last_selected_text()
                if txt:
                    QApplication.clipboard().setText(txt)
                    return

        sc_copy.activated.connect(_on_copy)

    def set_typ(self, new_typ):
        self.typ = new_typ
    
    def get_current_dict(self):
        return self.dict_pdf_chosen_examples

    def refresh_pdf(self, file_path: str, typ=None, show_selection_list=None):
        if typ is not None:
            if typ != 'cria':
                self.typ = 'lama'  # <--- neuer typ wird hier aktualisiert!
            else:
                self.typ = typ

        if show_selection_list is not None:
            self.show_selection_list = show_selection_list

            if show_selection_list:
                # self.header.show()
                # self.list.show()
                self.left_panel.show()

                # Handle normal anzeigen
                self.splitter.handle(1).setEnabled(True)
                # self.splitter.handle(1).setStyleSheet('image: url({get_icon_path("more-vertical.svg")}')
                self.splitter.setSizes([300, 2000])

            else:

                self.left_panel.hide()
                self.splitter.handle(1).setEnabled(False)
                # self.splitter.handle(1).setStyleSheet("background: transparent; width: 0px; image: none")
                self.splitter.setSizes([0, 1_000_000])
                # self.header.hide()
                # self.splitter.handle(1).setEnabled(False)
                # self.splitter.handle(1).setStyleSheet("background: transparent; width: 0px; image: none")
                # self.list.hide()
                # self.splitter.setSizes([0, 1_000_000])
                # self._hide_splitter_handle()


        """Öffentliche API: PDF austauschen + Liste neu aufbauen."""
        if not file_path or not os.path.isfile(file_path):
            return
        self._current_pdf_path = file_path

        # 1) PDF im Viewer laden/neu rendern
        self.viewer.load_document(file_path)

        # 2) Seite(n)-Anzeige aktualisieren

        total = self.viewer.pageCount()
        self.lbl_total.setText(f"/ {total}")
        self.spin_page.blockSignals(True)
        self.spin_page.setMaximum(max(1, total))
        self.spin_page.setValue(1)
        self.spin_page.blockSignals(False)


        # 3) Aufgabenliste neu aus den Überschriften bauen
        self._fill_tasks_from_pdf(self._current_pdf_path)

        # --- Task-Positionsliste NEU aufbauen ---
        self.task_positions = []
        for row in range(self.list.count()):
            item = self.list.item(row)
            page, y_ratio = item.data(self.ROLE_TARGET)
            self.task_positions.append({
                "row": row,
                "page": page,
                "ratio": y_ratio
            })



        self._restore_selections_from_dict()



        # --- Beim ersten Anzeigen: erste Aufgabe auswählen ---
        if self.list.count() > 0:
            self.list.setCurrentRow(0)
            first_page, first_ratio = self.list.item(0).data(self.ROLE_TARGET)
            self.viewer.scrollToPageLocation(first_page, first_ratio)

        # # Listenlängen berechnen
        # self.len_list_1 = 1
        # self.len_list_2 = 5
        # self.len_list_3 = 10

        # Header-Zahlen aktualisieren

        # ✅ Zuerst neue Längen für den aktuellen typ berechnen!
        self.len_list_1 = len(self.dict_pdf_chosen_examples[self.typ]["lists"][1])
        self.len_list_2 = len(self.dict_pdf_chosen_examples[self.typ]["lists"][2])
        self.len_list_3 = len(self.dict_pdf_chosen_examples[self.typ]["lists"][3])

        # ✅ Danach Header aktualisieren
        self.header.updateCounts([
            self.len_list_1,
            self.len_list_2,
            self.len_list_3
        ], self.dict_pdf_chosen_examples, self.typ)


        # 4) (optional) ganz nach oben springen
        self.viewer.scrollToPage(1)


    def _on_category_toggled(self, index: int, enabled: bool):
        # Anzeige aktualisieren: deaktivierte Kategorien werden weiß gezeigt
        self._recolor_all_items()

    def _on_marking_toggled(self, enabled: bool):
        # Beim Ausschalten: alles weiß anzeigen (Zustand bleibt aber im Model erhalten)
        self._recolor_all_items()
    # ----- Liste befüllen -----
    def _fill_tasks_from_pdf(self, pdf_path: str):
        headings = extract_headings_with_positions(pdf_path)
        self.list.clear()
        if not headings:
            return

        for text, page, y_ratio in headings:
            it = QListWidgetItem(text)
            it.setData(self.ROLE_TARGET, (page, y_ratio))
            it.setData(self.ROLE_COLORSTATE, 0)  # 0=weiß
            it.setData(Qt.UserRole + 5, set())
            # Anzeige abhängig vom Markierungsstatus
            if self.header.markingEnabled():
                it.setBackground(Qt.white); it.setForeground(Qt.black)
            else:
                # bei aus: ohnehin weiß
                it.setBackground(Qt.white); it.setForeground(Qt.black)
            self.list.addItem(it)


    # ----- Click-Handling -----
    def _on_task_clicked(self, item: QListWidgetItem):
        # Manuelles Klicken → automatische Auswahl pausieren
        self._manual_selection = True

        data = item.data(self.ROLE_TARGET)
        if data:
            page, y_ratio = data
            self.viewer.scrollToPageLocation(page, y_ratio)



        # Seite manuell setzen
        self.spin_page.blockSignals(True)
        self.spin_page.setValue(page)
        self.spin_page.blockSignals(False)

        # Nach kurzer Zeit wieder Auto-Sync erlauben
        QTimer.singleShot(200, lambda: setattr(self, "_manual_selection", False))


    def _next_enabled_state(self, cur: int) -> int:
        """
        Liefert den nächsten erlaubten Zustand im Zyklus:
        weiß(0) -> rot(1) -> gelb(2) -> grün(3) -> weiß(0) -> ...
        Deaktivierte Kategorien (per Checkbox) werden übersprungen.
        Falls alle Kategorien deaktiviert sind: immer 0 (weiß).
        """
        mask = self.header.enabledMask()  # Bit0..2
        if mask == 0:
            return 0  # alles aus -> bleibt weiß

        # Reihenfolge des Zyklus
        order = [0, 1, 2, 3]  # 0=weiß, 1=rot, 2=gelb, 3=grün
        # Starte ab dem nächsten Schritt
        start_idx = (order.index(cur) + 1) % len(order)

        for k in range(len(order)):
            st = order[(start_idx + k) % len(order)]
            if st == 0:
                # Weiß ist immer erlaubt
                return 0
            else:
                cat_idx = st - 1  # 0..2
                if (mask & (1 << cat_idx)) != 0:
                    # Kategorie aktiv -> erlaubter nächster Zustand
                    return st
        # Fallback (sollte nicht passieren, falls mask != 0)
        return 0

    # ----- Header-Änderungen -----
    def _on_category_color_changed(self, index: int, color: QColor):
        # existierende Markierungen direkt neu einfärben
        self._recolor_all_items()

    def _on_category_label_changed(self, index: int, text: str):

        """
        Aktualisiert name_list_x im Dictionary, wenn oben der Titel geändert wird.
        index = 0 → Übungsblatt
        index = 1 → Schularbeit
        index = 2 → Nachschularbeit
        """
        self.typ 
        if index == 0:
            self.dict_pdf_chosen_examples[self.typ]['names'][1] = text
        elif index == 1:
            self.dict_pdf_chosen_examples[self.typ]['names'][2] = text
        elif index == 2:
            self.dict_pdf_chosen_examples[self.typ]['names'][3] = text


        save_pdf_selection_dict(lama_pdf_selection_file, self.dict_pdf_chosen_examples)
        # aktuell nur Info; später evtl. Tooltips/Badges etc.
        # pass

    # ----- Toolbar-Events -----


    def _on_current_page_changed(self, page_one_based: int):
        """Aktualisiert Spinbox und markiert die Aufgabe,
        die im sichtbaren Teil der Seite am weitesten oben steht."""
        # Wenn der Benutzer gerade aktiv in der Liste geklickt hat:
        if self._manual_selection:
            return
        # ---- Spinbox aktualisieren ----
        if self.spin_page.value() != page_one_based:
            self.spin_page.blockSignals(True)
            self.spin_page.setValue(page_one_based)
            self.spin_page.blockSignals(False)

        # ---- aktuelle Scrollposition im Viewer bestimmen ----
        scroll_y = self.viewer.scroll.verticalScrollBar().value()

        # Seitenpositionen im Canvas:
        page_y, page_height = self.viewer.canvas.page_positions[page_one_based - 1]


        # relative Position IN der Seite (0..1)
        rel = max(0.0, min(1.0, (scroll_y - page_y) / float(page_height)))

        # --- Sonderfall: Wenn auf dieser Seite genau EINE Aufgabe steht ---
        tasks_on_page = [pos for pos in self.task_positions if pos["page"] == page_one_based]
        # only = tasks_on_page[0]

        # # Nur wenn die Überschrift wirklich auf dieser Seite ist!
        # if only["ratio"] is not None:
        if len(tasks_on_page) == 1:
            if tasks_on_page[0] is not None:
                only_row = tasks_on_page[0]["row"]
                self.list.blockSignals(True)
                self.list.setCurrentRow(only_row)
                self.list.scrollToItem(
                    self.list.item(only_row),
                    QAbstractItemView.PositionAtCenter
                )
                self.list.blockSignals(False)
                return

        # ---- passende Aufgabe suchen ----
        best_row = None
        best_ratio = -1

        for pos in self.task_positions:
            if pos["page"] != page_one_based:
                continue
            if pos["ratio"] <= rel and pos["ratio"] > best_ratio:
                best_ratio = pos["ratio"]
                best_row = pos["row"]

        # falls nichts passt -> nimm die erste Aufgabe auf der Seite
        if best_row is None:
            for pos in self.task_positions:
                if pos["page"] == page_one_based:
                    best_row = pos["row"]
                    break

        # ---- Liste aktualisieren ----
        if best_row is not None:
            self.list.blockSignals(True)
            self.list.setCurrentRow(best_row)
            self.list.scrollToItem(
                self.list.item(best_row),
                QAbstractItemView.PositionAtCenter
            )
            self.list.blockSignals(False)


    def _select_task_row(self, index):
        self.list.blockSignals(True)
        self.list.setCurrentRow(index)
        self.list.scrollToItem(
            self.list.item(index),
            QAbstractItemView.PositionAtCenter
        )
        self.list.blockSignals(False)



    def _on_spin_value_changed(self, val: int):
        """Benutzer ändert die Zahl -> zur Seite springen."""
        total = self.viewer.pageCount()
        if total <= 0:
            return
        if val < 1:
            val = 1
        elif val > total:
            val = total
        # nur springen, wenn nötig
        if self.viewer.currentPage() != val:
            self.viewer.scrollToPage(val)



    def _jump_to_entered_page(self):
        text = self.edt_current.text().strip()
        if not text.isdigit():
            self.edt_current.setText(str(self.viewer.currentPage()))
            return
        self.viewer.scrollToPage(int(text))
        

    def _update_item_icons(self, item):
        tags = item.data(Qt.UserRole + 5) or set()

        # Aktuelle Farben aus dem Header holen
        colors = self.header.colors()  # [color0, color1, color2]

        cat_info = [
            ("uebung",        self.header.categoryEnabled(0), colors[0]),
            ("schularbeit",   self.header.categoryEnabled(1), colors[1]),
            ("nachschularbeit", self.header.categoryEnabled(2), colors[2]),
        ]

        # aktive Kästchen erstellen (NEUE Pixmaps!)
        pixmaps = []
        for tagname, enabled, color in cat_info:
            if enabled and tagname in tags:
                pix = self._make_square(color, size=14)
                pixmaps.append(pix)

        if not pixmaps:
            item.setIcon(QIcon())
            return

        # Gemeinsames Icon für alle Pixmaps (nebeneinander)
        spacing = 4
        h = pixmaps[0].height()
        total_w = sum(pm.width() for pm in pixmaps) + spacing * (len(pixmaps) - 1)

        final_pm = QPixmap(total_w, h)
        final_pm.fill(Qt.transparent)

        p = QPainter(final_pm)
        x = 0
        for pm in pixmaps:
            p.drawPixmap(x, 0, pm)
            x += pm.width() + spacing
        p.end()

        item.setIcon(QIcon(final_pm))

    def _on_list_context_menu(self, pos):
        item = self.list.itemAt(pos)
        if not item:
            return

        # aktive Kategorien prüfen
        enabled = self.header._enabled               # [bool, bool, bool]
        idx_enabled = [i for i, e in enumerate(enabled) if e]

        # Tags holen oder initialisieren
        tags = item.data(Qt.UserRole + 5)
        if tags is None:
            tags = set()
            item.setData(Qt.UserRole + 5, tags)

        # ✅ FALL 0 → Keine Kategorie aktiv → NICHTS tun
        if len(idx_enabled) == 0:
            return

        # ✅ FALL 1 → genau eine Kategorie aktiv → direkt taggen
        if len(idx_enabled) == 1:
            index = idx_enabled[0]          # 0, 1 oder 2
            tagname = ["uebung", "schularbeit", "nachschularbeit"][index]

            # toggeln wie im Popup
            if tagname in tags:
                tags.remove(tagname)
            else:
                tags.add(tagname)

            item.setData(Qt.UserRole + 5, tags)

            # UI + Dictionary aktualisieren
            self._update_item_icons(item)
            self._update_dict_for_item(item)
            return

        # ✅ FALL 2 → mehrere Kategorien aktiv → Popup anzeigen
        categories = []
        if self.header.categoryEnabled(0):
            categories.append(("uebung", self.header.labels()[0]))
        if self.header.categoryEnabled(1):
            categories.append(("schularbeit", self.header.labels()[1]))
        if self.header.categoryEnabled(2):
            categories.append(("nachschularbeit", self.header.labels()[2]))

        def on_tag_change():
            self._update_item_icons(item)
            self._update_dict_for_item(item)

        popup = TagPopup(
            parent=self.list,
            tags=tags,
            categories=categories,
            on_change=on_tag_change
        )

        global_pos = self.list.viewport().mapToGlobal(pos)
        popup.move(global_pos)
        popup.show()

    def _recolor_all_items(self):
        for i in range(self.list.count()):
            it = self.list.item(i)
            self._update_item_icons(it)

    def _make_square(self, color: QColor, size=14):
        pm = QPixmap(size, size)
        pm.fill(color)
        return pm
    
    def _update_dict_for_item(self, item):

        # Gesamten Text vom Item holen
        full_text = item.text()

        # Nur die Aufgabennummer extrahieren
        task_id = self._extract_task_number(full_text)

        # Tags (Kategorien) aus dem Item holen
        tags = item.data(Qt.UserRole + 5) or set()

        # --- 1) zuerst aus allen Listen entfernen ---
        for key in (1,2,3):
            if task_id in self.dict_pdf_chosen_examples[self.typ]['lists'][key]:
                self.dict_pdf_chosen_examples[self.typ]['lists'][key].remove(task_id)

        # --- 2) neue Tags einfügen ---
        if "uebung" in tags:
            if task_id not in self.dict_pdf_chosen_examples[self.typ]['lists'][1]:
                self.dict_pdf_chosen_examples[self.typ]['lists'][1].append(task_id)

        if "schularbeit" in tags:
            if task_id not in self.dict_pdf_chosen_examples[self.typ]['lists'][2]:
                self.dict_pdf_chosen_examples[self.typ]['lists'][2].append(task_id)

        if "nachschularbeit" in tags:
            if task_id not in self.dict_pdf_chosen_examples[self.typ]['lists'][3]:
                self.dict_pdf_chosen_examples[self.typ]['lists'][3].append(task_id)

        # --- 3) Header-Kästchen aktualisieren ---
        self.len_list_1 = len(self.dict_pdf_chosen_examples[self.typ]['lists'][1])
        self.len_list_2 = len(self.dict_pdf_chosen_examples[self.typ]['lists'][2])
        self.len_list_3 = len(self.dict_pdf_chosen_examples[self.typ]['lists'][3])

        self.header.updateCounts([
            self.len_list_1,
            self.len_list_2,
            self.len_list_3
        ],self.dict_pdf_chosen_examples, self.typ)


    def _extract_task_number(self, text: str) -> str:
        """
        Entfernt immer den letzten Teil nach ' - '.
        Beispiel:
        'AG 1.4 - 3 - Titel' -> 'AG 1.4 - 3'
        '98 - Polynomfunktion dritten Grades' -> '98'
        'WS-XY 2.3 - 1 - Irgendein Titel - Noch mehr' -> 'WS-XY 2.3 - 1'
        """
        if " - " not in text:
            return text

        parts = text.split(" - ")
        # alle Teile außer dem letzten wieder zusammensetzen
        cleaned = " - ".join(parts[:-1])
        return cleaned.strip()
    
# from PyQt5.QtWidgets import QMessageBox

    def _on_header_trash_clicked(self, index: int):
        """
        Löscht alle Aufgaben einer Kategorie – mit Sicherheitsabfrage,
        falls die Liste nicht leer ist.
        index 0 → list 1
        index 1 → list 2
        index 2 → list 3
        """

        # 0→1, 1→2, 2→3
        list_num = index + 1

        # Zugriff auf Namen und Listen anhand des aktuellen Typs ("lama" / "cria")
        name_list = self.dict_pdf_chosen_examples[self.typ]["names"][list_num]
        current_list = self.dict_pdf_chosen_examples[self.typ]["lists"][list_num]

        # Wenn die Liste leer ist → nichts tun
        if len(current_list) > 0:

            # Sicherheitsdialog
            msg = QMessageBox(self.Dialog)
            msg.setWindowTitle("Bestätigung")
            msg.setText(
                f"Sind Sie sicher, dass Sie die Aufgabenliste "
                f"„{name_list}“ unwiderruflich löschen möchten?"
            )

            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.Yes)  # Enter bestätigt 'Ja'

            result = msg.exec_()

            if result != QMessageBox.Yes:
                return  # abbrechen

        # --- Ab hier wirklich löschen ---

        # 1) Liste im Dictionary leeren
        self.dict_pdf_chosen_examples[self.typ]["lists"][list_num].clear()

        # 2) Tags in UI entfernen
        tag_map = {0: "uebung", 1: "schularbeit", 2: "nachschularbeit"}
        tag_to_remove = tag_map[index]

        for i in range(self.list.count()):
            item = self.list.item(i)
            tags = item.data(Qt.UserRole + 5) or set()

            if tag_to_remove in tags:
                tags.discard(tag_to_remove)
                item.setData(Qt.UserRole + 5, tags)
                self._update_item_icons(item)

        # 3) Header‑Zähler aktualisieren
        self.header.updateCounts([
            len(self.dict_pdf_chosen_examples[self.typ]["lists"][1]),
            len(self.dict_pdf_chosen_examples[self.typ]["lists"][2]),
            len(self.dict_pdf_chosen_examples[self.typ]["lists"][3]),
        ], self.dict_pdf_chosen_examples, self.typ)
        save_pdf_selection_dict(lama_pdf_selection_file, self.dict_pdf_chosen_examples)


    def _restore_selections_from_dict(self):
        """
        Setzt die Markierungen im ListWidget anhand des gespeicherten Dictionaries wieder.
        """
        for i in range(self.list.count()):
            item = self.list.item(i)

            task_id = self._extract_task_number(item.text())
            tags = item.data(Qt.UserRole + 5) or set()

            # Reset
            tags.clear()

            # Kategorie zuordnen
            if task_id in self.dict_pdf_chosen_examples[self.typ]['lists'][1]:
                tags.add("uebung")

            if task_id in self.dict_pdf_chosen_examples[self.typ]['lists'][2]:
                tags.add("schularbeit")

            if task_id in self.dict_pdf_chosen_examples[self.typ]['lists'][3]:
                tags.add("nachschularbeit")

            item.setData(Qt.UserRole + 5, tags)
            self._update_item_icons(item)

    def _find_page_for_task(self, task_name: str) -> int:
        """
        Sucht im PDF nach der echten Aufgabenkennung (AG 1.1 - 36 …).
        Gibt die Seite (1-basiert) zurück.
        """

        # ECHTE Kennung extrahieren (z.B. "AG 1.1 - 36")
        key = self._extract_task_number(task_name)

        for page_index in range(self.viewer.doc.page_count):
            page = self.viewer.doc[page_index]
            text = page.get_text("text")

            # exakte Suche nach Aufgabenkennung
            if key in text:
                return page_index + 1

        return 1
    
    def selected_item_changed(self):
        row = self.list.currentRow()
        if row < 0:
            return

        self._manual_selection = True

        item = self.list.item(row)
        page, ratio = item.data(self.ROLE_TARGET)

        # Jetzt PDF springen lassen
        self.viewer.scrollToPageLocation(page, ratio)



        # Seite manuell setzen
        self.spin_page.blockSignals(True)
        self.spin_page.setValue(page)
        self.spin_page.blockSignals(False)


        # nach kurzer Zeit Automatik wieder erlauben
        QTimer.singleShot(150, lambda: setattr(self, "_manual_selection", False))



    def moveEvent(self, event):
        super(type(self.Dialog), self.Dialog).moveEvent(event)
        if hasattr(self, "viewer"):
            self.viewer.position_search_popup()


    def _on_dialog_moved(self, event):
        # super aufrufen, damit alles normal weiterläuft
        try:
            super(type(self.Dialog), self.Dialog).moveEvent(event)
        except Exception:
            pass
        
        # ✅ Wenn PdfViewer existiert → Position aktualisieren
        if hasattr(self, "viewer"):
            try:
                self.viewer.position_search_popup()
            except:
                pass