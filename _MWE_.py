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
import sys
from typing import List, Tuple, Optional

import fitz  # PyMuPDF
from PyQt5.QtWidgets import (
    QApplication, QLabel, QWidget, QScrollArea, QVBoxLayout,
    QMainWindow, QToolBar, QLineEdit, QSizePolicy, QShortcut,
    QListWidget, QListWidgetItem, QSplitter, QHBoxLayout, QStatusBar,
    QStyledItemDelegate, QStyle, QStyleOptionViewItem,
    QColorDialog, QPushButton, QGridLayout
)
from PyQt5.QtGui import QPixmap, QImage, QKeySequence, QColor, QBrush, QPen
from PyQt5.QtCore import Qt, pyqtSignal, QRect, QModelIndex, QEvent, QTranslator, QLocale, QLibraryInfo


# ---------- Überschriften-Extraktion aus PDF ----------
_heading_re = re.compile(
    r"""(?ix)
    \b(
        [A-ZÄÖÜ]{2,}            # Präfix (z.B. AG, WS, AN oder AG-L)
        (?:-[A-Z])?             # optionales -L etc.
        \s*
        \d+(?:\.\d+)*           # Kapitelnummer (z.B. 1.4)
        \s*-\s*
        \d+                     # laufende Aufgabennummer (z.B. 1)
    )\b
    """.strip()
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



def extract_headings_with_positions(pdf_path: str) -> List[Tuple[str, int, Optional[float]]]:
    """
    Liefert Liste von (heading_text, page_one_based, y_ratio [0..1 oder None]).
    """
    results: List[Tuple[str, int, Optional[float]]] = []
    seen = set()
    with fitz.open(pdf_path) as doc:
        for pno in range(len(doc)):
            page = doc[pno]
            text = page.get_text("text") or ""
            for ln in text.splitlines():
                m = _heading_re.search(ln)
                if not m:
                    continue
                heading = m.group(1).strip()
                key = (heading, pno)
                if key in seen:
                    continue
                y_ratio: Optional[float] = None
                try:
                    rects = page.search_for(heading, quads=False)
                    if rects:
                        r = rects[0]
                        y_ratio = float(r.y0 / page.rect.height)
                except Exception:
                    pass
                results.append((heading, pno + 1, y_ratio))
                seen.add(key)
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
    colorChanged = pyqtSignal(int, QColor)  # index (0..2), color
    labelChanged = pyqtSignal(int, str)     # index (0..2), text

    def __init__(self, parent=None):
        super().__init__(parent)
        # Standardfarben (pastellig, gut lesbar)
        self._colors = [
            QColor("#d3f9d8"),  # grün
            QColor("#ffd6d6"),  # rot
            QColor("#fff3bf"),  # gelb
        ]
        self._labels = ["Übungsblatt", "Schularbeit", "Nachschularbeit"]

        grid = QGridLayout(self)
        grid.setContentsMargins(6, 6, 6, 6)
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(6)

        self._btns: List[QPushButton] = []
        self._edits: List[QLineEdit] = []

        for i in range(3):
            btn = QPushButton("")
            btn.setFixedSize(20, 20)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(self._btn_style(self._colors[i]))
            btn.clicked.connect(lambda _, ix=i: self._pick_color(ix))
            self._btns.append(btn)

            edit = QLineEdit(self._labels[i])
            edit.setPlaceholderText("Bezeichnung eingeben…")
            edit.textEdited.connect(lambda txt, ix=i: self._on_label(ix, txt))
            self._edits.append(edit)

            grid.addWidget(btn,  i, 0)
            grid.addWidget(edit, i, 1)

        # eine schmale Linie nach unten für optische Trennung
        sep = QWidget()
        sep.setFixedHeight(1)
        sep.setStyleSheet("background:#e5e5e5; margin:0px;")
        grid.addWidget(sep, 3, 0, 1, 2)

    def _btn_style(self, qcolor: QColor) -> str:
        c = qcolor.name()
        return (
            "QPushButton {"
            f" background:{c}; border:1px solid #c8c8c8; border-radius:4px;"
            "}"
            "QPushButton:hover { border-color:#888; }"
            "QPushButton:pressed { border-color:#555; }"
        )

    def _pick_color(self, index: int):
        col = QColorDialog.getColor(self._colors[index], self, "Farbe wählen")
        if col and col.isValid():
            self._colors[index] = col
            self._btns[index].setStyleSheet(self._btn_style(col))
            self.colorChanged.emit(index, col)

    def _on_label(self, index: int, text: str):
        self._labels[index] = text
        self.labelChanged.emit(index, text)

    # Zugriff
    def colors(self) -> List[QColor]:
        return list(self._colors)

    def labels(self) -> List[str]:
        return list(self._labels)


# ---------------- PDF-Anzeige-Widget ----------------
class PdfWidget(QWidget):
    currentPageChanged = pyqtSignal(int)  # 1-basierter Index

    def __init__(self, pdf_path, parent=None):
        super().__init__(parent)
        self._doc = fitz.open(pdf_path)
        self._zoom = 1.5
        self._container = QWidget()
        self._layout = QVBoxLayout(self._container)
        self._layout.setContentsMargins(12, 12, 12, 12)
        self._layout.setSpacing(12)
        self._labels: List[QLabel] = []
        self._last_reported_page = 1

        self._render_pages()

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setWidget(self._container)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(self._scroll)

        self._scroll.verticalScrollBar().valueChanged.connect(self._update_current_page)
        self._scroll.viewport().installEventFilter(self)
        self._update_current_page()

    def pageCount(self) -> int:
        return self._doc.page_count

    def currentPage(self) -> int:
        return self._last_reported_page

    def scrollToPage(self, page_one_based: int):
        n = self.pageCount()
        if n == 0:
            return
        p = max(1, min(n, page_one_based))
        if 1 <= p <= len(self._labels):
            y = self._labels[p - 1].y()
            self._scroll.verticalScrollBar().setValue(y)
            self._update_current_page(force=True)

    def scrollToPageLocation(self, page_one_based: int, y_ratio: Optional[float] = None, margin_px: int = 8):
        self.scrollToPage(page_one_based)
        if y_ratio is None:
            return
        p = max(1, min(self.pageCount(), page_one_based))
        if 1 <= p <= len(self._labels):
            label = self._labels[p - 1]
            pm = label.pixmap()
            if pm is not None and not pm.isNull():
                extra = int(max(0, min(1, y_ratio)) * pm.height())
                self._scroll.verticalScrollBar().setValue(label.y() + max(0, extra - margin_px))
                self._update_current_page(force=True)

    def gotoNext(self): self.scrollToPage(self.currentPage() + 1)
    def gotoPrev(self): self.scrollToPage(self.currentPage() - 1)

    def _render_pages(self):
        for lbl in self._labels:
            lbl.deleteLater()
        self._labels.clear()

        mat = fitz.Matrix(self._zoom, self._zoom)
        for page in self._doc:
            pix = page.get_pixmap(matrix=mat, alpha=False)
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
            lbl = QLabel()
            lbl.setAlignment(Qt.AlignHCenter)
            lbl.setPixmap(QPixmap.fromImage(img.copy()))
            lbl.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self._layout.addWidget(lbl)
            self._labels.append(lbl)

        spacer = QWidget(); spacer.setFixedHeight(1)
        self._layout.addWidget(spacer)
        self._container.adjustSize()

    def _update_current_page(self, *_args, force=False):
        if not self._labels:
            return
        viewport = self._scroll.viewport()
        y_top = self._scroll.verticalScrollBar().value()
        rect_visible = QRect(0, y_top, viewport.width(), viewport.height())

        best_idx, best_score = 0, -1
        for i, lbl in enumerate(self._labels):
            r = QRect(lbl.pos(), lbl.size())
            inter = r.intersected(rect_visible)
            score = inter.width() * inter.height()
            if score > best_score:
                best_score, best_idx = score, i

        current_one_based = best_idx + 1
        if force or current_one_based != self._last_reported_page:
            self._last_reported_page = current_one_based
            self.currentPageChanged.emit(current_one_based)

    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            delta = event.angleDelta().y()
            self._zoom = min(6.0, self._zoom * 1.1) if delta > 0 else max(0.3, self._zoom / 1.1)
            cur = self._last_reported_page
            self._render_pages(); self.scrollToPage(cur)
            event.accept()
        else:
            super().wheelEvent(event)

    def keyPressEvent(self, event):
        ctrl = bool(event.modifiers() & Qt.ControlModifier)
        if ctrl and event.key() in (Qt.Key_Plus, Qt.Key_Equal):
            self._zoom = min(6.0, self._zoom * 1.2); cur = self._last_reported_page
            self._render_pages(); self.scrollToPage(cur); return
        if ctrl and event.key() == Qt.Key_Minus:
            self._zoom = max(0.3, self._zoom / 1.2); cur = self._last_reported_page
            self._render_pages(); self.scrollToPage(cur); return
        if ctrl and event.key() == Qt.Key_0:
            self._zoom = 1.5; cur = self._last_reported_page
            self._render_pages(); self.scrollToPage(cur); return
        if event.key() == Qt.Key_Left:  self.gotoPrev(); return
        if event.key() == Qt.Key_Right: self.gotoNext(); return
        super().keyPressEvent(event)


# ---------------- Hauptfenster ----------------
class MainWindow(QMainWindow):
    ROLE_TARGET = Qt.UserRole          # (page, y_ratio)
    ROLE_COLORSTATE = Qt.UserRole + 1  # 0..3 (0=weiß,1=cat0,2=cat1,3=cat2)

    def __init__(self, pdf_path, parent=None):
        super().__init__(parent)

        # --- Linke Seite: Header + Liste (in einem Panel) ---
        self.header = CategoryHeaderWidget()
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
            QListWidget::item {
                padding: 6px 8px;
            }
        """)
        self.list.setItemDelegate(ColorAwareBorderDelegate(border_color="#0078D4", border_width=2, radius=6, parent=self.list))

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        left_layout.addWidget(self.header)
        left_layout.addWidget(self.list)

        # --- Rechte Seite: PDF ---
        self.viewer = PdfWidget(pdf_path)

        # --- Splitter ---
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(self.viewer)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([300, 900])

        central = QWidget()
        lay = QHBoxLayout(central)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(splitter)
        self.setCentralWidget(central)

        self.setWindowTitle("Einfacher PDF Viewer (PyMuPDF)")

        # ---- Toolbar (zentriert) ----
        tb = QToolBar(); tb.setMovable(False); tb.setFloatable(False); self.addToolBar(tb)
        spacer_left = QWidget(); spacer_left.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred); tb.addWidget(spacer_left)

        center = QWidget(); row_layout = QHBoxLayout(center)
        row_layout.setContentsMargins(0, 0, 0, 0); row_layout.setSpacing(6)
        lbl_prefix = QLabel("<span style='color:#666'>Seite&nbsp;</span>")
        self.edt_current = QLineEdit(); self.edt_current.setFixedWidth(56); self.edt_current.setAlignment(Qt.AlignCenter)
        self.edt_current.setToolTip("Aktuelle Seite (Enter zum Springen)")
        self.lbl_total = QLabel("/ 1"); self.lbl_total.setStyleSheet("color:#666;")
        row_layout.addWidget(lbl_prefix); row_layout.addWidget(self.edt_current); row_layout.addWidget(self.lbl_total)
        tb.addWidget(center)

        spacer_right = QWidget(); spacer_right.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred); tb.addWidget(spacer_right)

        # Statusbar
        self.setStatusBar(QStatusBar())

        # Initialwerte & Bindings
        total = self.viewer.pageCount()
        self.lbl_total.setText(f"/ {total}")
        self.edt_current.setText("1")
        self.viewer.currentPageChanged.connect(self._on_current_page_changed)
        self.edt_current.returnPressed.connect(self._jump_to_entered_page)
        QShortcut(QKeySequence(Qt.Key_Left),  self, activated=self.viewer.gotoPrev)
        QShortcut(QKeySequence(Qt.Key_Right), self, activated=self.viewer.gotoNext)

        # Liste füllen
        self._fill_tasks_from_pdf(pdf_path)

        # Klick-Logik: Erster Klick auf nicht ausgewählt -> nur springen
        self._press_was_selected = False
        self._pressed_item = None
        self.list.viewport().installEventFilter(self)
        self.list.itemClicked.connect(self._on_task_clicked)

        # Header-Änderungen -> Farben übernehmen
        self.header.colorChanged.connect(self._on_category_color_changed)
        self.header.labelChanged.connect(self._on_category_label_changed)

        self.showMaximized()

    # ----- Event-Filter (für Click-Vorzustand) -----
    def eventFilter(self, obj, event):
        if obj is self.list.viewport() and event.type() == QEvent.MouseButtonPress:
            item = self.list.itemAt(event.pos())
            self._pressed_item = item
            self._press_was_selected = bool(item and item.isSelected())
            return False
        return super().eventFilter(obj, event)

    # ----- Liste befüllen -----
    def _fill_tasks_from_pdf(self, pdf_path: str):
        headings = extract_headings_with_positions(pdf_path)
        self.list.clear()
        if not headings:
            self.statusBar().showMessage("Keine Überschriften erkannt.", 4000)
            return

        for text, page, y_ratio in headings:
            it = QListWidgetItem(text)
            it.setData(self.ROLE_TARGET, (page, y_ratio))
            it.setData(self.ROLE_COLORSTATE, 0)  # 0=weiß
            it.setBackground(Qt.white)
            it.setForeground(Qt.black)
            self.list.addItem(it)

    # ----- Farben anwenden (state: 0=weiß,1=cat0,2=cat1,3=cat2) -----
    def _apply_color_state(self, item: QListWidgetItem, state: int):
        if state == 0:
            item.setBackground(Qt.white); item.setForeground(Qt.black)
        else:
            # state 1..3 -> Kategorien 0..2
            cat_idx = state - 1
            col = self.header.colors()[cat_idx]
            item.setBackground(col); item.setForeground(Qt.black)
        item.setData(self.ROLE_COLORSTATE, state)

    def _recolor_all_items(self):
        for i in range(self.list.count()):
            it = self.list.item(i)
            st = int(it.data(self.ROLE_COLORSTATE) or 0)
            self._apply_color_state(it, st)

    # ----- Click-Handling auf Items -----
    def _on_task_clicked(self, item: QListWidgetItem):
        # 1) Navigation: immer
        data = item.data(self.ROLE_TARGET)
        if data:
            page, y_ratio = data
            self.viewer.scrollToPageLocation(page, y_ratio)
            self.statusBar().showMessage(f"Gehe zu: {item.text()} (Seite {page})", 2000)

        # 2) Farbzyklus nur, wenn Item VOR dem Klick schon ausgewählt war
        if self._press_was_selected and (item is self._pressed_item):
            cur = int(item.data(self.ROLE_COLORSTATE) or 0)
            nxt = (cur + 1) % 4  # 0=weiß, 1/2/3 = Kategorie 0/1/2
            self._apply_color_state(item, nxt)

        # Flags zurücksetzen
        self._press_was_selected = False
        self._pressed_item = None

    # ----- Header-Änderungen -----
    def _on_category_color_changed(self, index: int, color: QColor):
        # existierende Markierungen direkt neu einfärben
        self._recolor_all_items()

    def _on_category_label_changed(self, index: int, text: str):
        # aktuell nur Info; später könnten wir Tooltips etc. setzen
        pass

    # ----- Toolbar-Events -----
    def _on_current_page_changed(self, page_one_based: int):
        if self.edt_current.text() != str(page_one_based):
            self.edt_current.setText(str(page_one_based))

    def _jump_to_entered_page(self):
        text = self.edt_current.text().strip()
        if not text.isdigit():
            self.edt_current.setText(str(self.viewer.currentPage()))
            return
        self.viewer.scrollToPage(int(text))


# ---------------- main ----------------
def main():
    app = QApplication(sys.argv)
    enable_german_ui(app)
    script_dir = os.path.abspath(os.path.dirname(__file__))
    pdf_path = os.path.join(script_dir, "test.pdf")
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError("test.pdf nicht gefunden – lege sie neben dieses Skript.")
    w = MainWindow(pdf_path)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()