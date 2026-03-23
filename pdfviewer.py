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
from config import get_icon_path
import fitz  # PyMuPDF
from PyQt5.QtWidgets import (
    QLabel, QWidget, QScrollArea, QVBoxLayout,
    QToolBar, QLineEdit, QSizePolicy, QShortcut,
    QListWidget, QListWidgetItem, QSplitter, QHBoxLayout,
    QStyledItemDelegate, QStyle, QStyleOptionViewItem,
    QColorDialog, QPushButton, QGridLayout, QDialog, QCheckBox, QSpinBox, QAction, QToolButton
)
from PyQt5.QtGui import QPixmap, QImage, QKeySequence, QColor, QBrush, QPen, QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QRect, QModelIndex, QEvent, QTranslator, QLocale, QLibraryInfo, QObject, QPoint, QTimer
from config import logo_path


# ---------- Überschriften-Extraktion aus PDF ----------
# ---------- Überschriften-Extraktion aus PDF (erweitert) ----------
import re

# 1) „AG/WS/AN … 1.4 - 3“-artige Muster (wie bisher)
_HEADING_CODED = re.compile(
    r"""(?xmi)                               # x: verbose, m: ^ matcht Zeilenbeginn, i: case-insensitive
    ^                                        # Zeilenanfang
    (?P<full>
        (?P<prefix>[A-ZÄÖÜ]{2,}(?:-[A-Z])?)  # AG, WS, AN, AG-L, …
        \s*
        (?P<chap>\d+(?:\.\d+)*)              # 1.4, 2.10.3, …
        \s*[-–—]\s*                          # Bindestrich (alle Varianten)
        (?P<num>\d+)                         # laufende Nummer
        (?:\b.*)?                            # evtl. weiterer Titeltext
    )
    $                                        # Zeilenende
    """
)

# 2) „8 - Haber'sche Regel“-artige Muster (zahlbasierte Überschrift),
#    aber KEINE Seitenangaben wie „1 / 18“ und keine leeren Titel
_HEADING_NUMERIC = re.compile(
    r"""(?xmi)
    ^                                  # Zeilenanfang
    (?P<full>
        (?P<num>\d{1,3})               # 1..3-stellige Nummer (anpassbar)
        \s*[-–—]\s*                    # Bindestrich
        (?P<title>                     # Titel: keine Slash-Zeilen (z.B. '1 / 18')
            (?![^/\n]*\s/\s*\d+\b)     # negative lookahead: keine '… / …'
            [^\n]{1,120}               # etwas Text (max. 120 Zeichen, anpassbar)
        )
    )
    $                                  # Zeilenende
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



def extract_headings_with_positions(pdf_path: str):
    """
    Liefert Liste von (heading_text, page_one_based, y_ratio[0..1|None]).
    Erfasst:
      - Schemata wie 'AG-L 1.4 - 3 - …'
      - Zahlbasierte Überschriften wie '8 - Haber'sche Regel'
    """
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

                m = _HEADING_CODED.match(line)
                if not m:
                    m = _HEADING_NUMERIC.match(line)

                if not m:
                    continue

                full = m.group("full").strip()
                key = (full, pno)
                if key in seen:
                    continue

                # Versuche, die genaue Y-Position über den exakten Zeilenstring zu finden
                y_ratio = None
                try:
                    rects = page.search_for(full, quads=False)
                    if rects:
                        r0 = rects[0]
                        y_ratio = float(r0.y0 / page.rect.height) if page.rect.height else None
                except Exception:
                    pass

                results.append((full, pno + 1, y_ratio))
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

    def __init__(self, parent=None):
        super().__init__(parent)

        self._colors = [
            QColor("#d3f9d8"), # Grün
            QColor("#ffd6d6"),  # Rot
            QColor("#fff3bf"),  # Gelb
        ]
        self._labels = ["Übungsblatt", "Schularbeit", "Nachschularbeit"]
        self._enabled = [True, True, True]  # standardmäßig alle aktiv

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
            chk.setChecked(True)

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

            # Farbkastl
            btn = QPushButton("")
            btn.setFixedSize(20, 20)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(self._btn_style(self._colors[i], enabled=True))
            btn.clicked.connect(lambda _, ix=i: self._pick_color(ix))

            btn.setAutoDefault(False)          # verhindert Auto-Default-Verhalten
            btn.setDefault(False)              # kein Default-Button
            btn.setFocusPolicy(Qt.NoFocus)     # Button bekommt keinen Tastatur-Fokus

            self._btns.append(btn)
            grid.addWidget(btn, i, 1)

            # Editierbarer Titel
            edit = QLineEdit(self._labels[i])
            edit.setPlaceholderText("Bezeichnung eingeben…")
            edit.textEdited.connect(lambda txt, ix=i: self._on_label(ix, txt))
            self._edits.append(edit)
            grid.addWidget(edit, i, 2)

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

    def _btn_style(self, qcolor: QColor, enabled: bool) -> str:
        c = qcolor.name()
        if enabled:
            return (
                "QPushButton {"
                f" background:{c}; border:1px solid #c8c8c8; border-radius:4px;"
                "}"
                "QPushButton:hover { border-color:#888; }"
                "QPushButton:pressed { border-color:#555; }"
            )
        else:
            # deaktiviert: ausgrauen
            return (
                "QPushButton {"
                f" background:{c}; border:1px dashed #bbbbbb; border-radius:4px; opacity:0.45;"
                "}"
            )

    def _pick_color(self, index: int):
        # Farbe nur ändern lassen, auch wenn disabled – Anzeige bleibt jedoch gräulich,
        # aber die definierte Farbe bleibt gespeichert (wird wieder aktiv, wenn reaktiviert).
        start = self._colors[index]
        col = QColorDialog.getColor(start, self, "Farbe wählen")
        if col.isValid():
            self._colors[index] = col
            self._btns[index].setStyleSheet(self._btn_style(col, self._enabled[index]))
            self.colorChanged.emit(index, col)

    def _on_label(self, index: int, text: str):
        self._labels[index] = text
        self.labelChanged.emit(index, text)

    def _on_toggle(self, index: int, state: bool):
        self._enabled[index] = state
        # Kastl-Stil aktualisieren (gräulich bei aus)
        self._btns[index].setStyleSheet(self._btn_style(self._colors[index], state))
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

# ---------------- PDF-Anzeige-Widget ----------------
class PdfWidget(QWidget):
    currentPageChanged = pyqtSignal(int)  # 1-basierter Index
    zoomChanged = pyqtSignal(float)

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
        self._last_selected_text = ""   # 🔹 globaler Puffer für Strg+C
        self._render_pages()

        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setWidget(self._container)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(self._scroll)

        self._scroll.setStyleSheet("QScrollArea { background: #f3f4f6; }")
        self._container.setStyleSheet("background: transparent;")  # Container durchsichtig

        self._scroll.verticalScrollBar().valueChanged.connect(self._update_current_page)

        self._ctrlWheelFilter = _CtrlWheelFilter(self, self._scroll.viewport())
        self._scroll.viewport().installEventFilter(self._ctrlWheelFilter)

        self._update_current_page()

        # --- Zoom Coalescing (flüssiges Touchpad-Zoom) ---
        self._zoom_target = self._zoom
        self._zoom_timer = QTimer(self)
        self._zoom_timer.setSingleShot(True)
        self._zoom_timer.setInterval(18)  # 18–25 ms: angenehm flüssig
        self._zoom_timer.timeout.connect(self._apply_coalesced_zoom)

    def get_last_selected_text(self) -> str:
        return self._last_selected_text or ""

    def _container_pos(self, w: QWidget) -> QPoint:
        """Position eines Widgets relativ zu self._container."""
        return w.mapTo(self._container, QPoint(0, 0))

    def _container_rect(self, w: QWidget) -> QRect:
        """Rect eines Widgets relativ zu self._container."""
        return QRect(self._container_pos(w), w.size())


    def pageCount(self) -> int:
        return self._doc.page_count

    def currentPage(self) -> int:
        return self._last_reported_page


    def _apply_coalesced_zoom(self):
        """Wendet den in _zoom_target gesammelten Zoom an (einmalig rendern)."""
        vsb = self._scroll.verticalScrollBar()
        frozen_val = vsb.value()

        self._scroll.setUpdatesEnabled(False)
        try:
            self._zoom = max(0.3, min(6.0, self._zoom_target))
            self._render_pages()
            vsb.setValue(max(vsb.minimum(), min(vsb.maximum(), frozen_val)))
        finally:
            self._scroll.setUpdatesEnabled(True)

        # kleiner Post-Layout-Fix
        QTimer.singleShot(0, lambda: vsb.setValue(max(vsb.minimum(), min(vsb.maximum(), frozen_val))))
        self.zoomChanged.emit(self._zoom)


    def zoom_in(self, factor: float = 1.2):
        """Zoomt hinein (Standard +20%) – coalesced, kein Doppelt-Rendern."""
        self._zoom_target = min(6.0, self._zoom * factor)
        self._zoom_timer.start()  # coalesced
        # kein _freeze_zoom_and_render() hier!

    def zoom_out(self, factor: float = 1/1.2):
        """Zoomt hinaus (Standard −20%) – coalesced, kein Doppelt-Rendern."""
        self._zoom_target = max(0.3, self._zoom * factor)
        self._zoom_timer.start()


    def reset_zoom(self, value: float = 1.5):
        """Setzt den Zoom auf einen Fixwert (Standard 150%)."""
        value = max(0.3, min(6.0, float(value)))
        self._freeze_zoom_and_render(value)
        self.zoomChanged.emit(self._zoom)

    def _on_ctrl_wheel(self, event):
        """
        STRG + Wheel/Touchpad -> Zoom (coalesced, flüssig).
        - pixelDelta (Touchpad): feines, kontinuierliches Zoomen
        - angleDelta (klassisches Rad): 10% pro Notch
        - Rendering wird auf ~18 ms coalesced -> keine "Lag"-Gefühle
        """
        dy = event.angleDelta().y()
        pixel_dy = 0
        if hasattr(event, "pixelDelta"):
            pd = event.pixelDelta()
            if pd and not pd.isNull():
                pixel_dy = pd.y()

        # Nichts zu tun?
        if dy == 0 and pixel_dy == 0:
            event.accept()
            return

        # Aktuelle Ziel-Zoom-Basis ist _zoom_target (nicht _zoom)
        z = float(self._zoom_target)

        if pixel_dy != 0:
            # Touchpad: feines, kontinuierliches Zoomen
            # Da pixelDelta je nach Gerät klein ausfällt: skaliere moderat.
            # 60 px "Scroll" ~ 15% Zoom
            steps = pixel_dy / 40.0
            z += (pixel_dy * 0.003)

        else:
            # Klassisches Rad (angleDelta): 120 -> ~10%
            steps = dy / 120.0
            z *= (1.10 ** steps)

        # Grenzen & Setzen
        self._zoom_target = max(0.3, min(6.0, z))

        # Coalescing: Timer (re)starten -> rendert erst, wenn Events kurz pausieren
        self._zoom_timer.start()

        # Scrollen verhindern
        event.accept()

    def scrollToPage(self, page_one_based: int):
        n = self.pageCount()
        if n == 0:
            return
        p = max(1, min(n, page_one_based))
        if 1 <= p <= len(self._labels):
            target_label = self._labels[p - 1]           # das innere QLabel (Pixmaps)
            card = target_label.parentWidget()           # Seitenkarte (Wrapper)
            y_target = self._container_y(card)           # KONTAINER-relative Y-Pos!
            self._scroll.verticalScrollBar().setValue(y_target)
            self._update_current_page(force=True)

    def _container_y(self, w: QWidget) -> int:
        """Y-Position eines Widgets relativ zum Container (self._container)."""
        return w.mapTo(self._container, QPoint(0, 0)).y()
    
    def scrollToPageLocation(self, page_one_based: int, page_y_ratio: Optional[float] = None, margin_px: int = 8):
        """Springt zur Seite und (falls vorhanden) zur ungefähren Y-Position innerhalb der Seite."""
        self.scrollToPage(page_one_based)
        if page_y_ratio is None:
            return

        p = max(1, min(self.pageCount(), page_one_based))
        if 1 <= p <= len(self._labels):
            target_label = self._labels[p - 1]     # inneres QLabel (Pixmap)
            card = target_label.parentWidget()     # Seitenkarte (Wrapper)
            pm = target_label.pixmap()
            if pm is None or pm.isNull():
                return

            # Padding (Innenabstand) der Seitenkarte berücksichtigen:
            pad_top = 0
            if card.layout() is not None:
                pad_top = card.layout().contentsMargins().top()

            # KONTAINER-relative Basisposition der Karte:
            base_y = self._container_y(card)

            # Zusätzlicher Offset innerhalb der Seite (in Pixeln des Pixmap-Inhalts):
            extra = int(max(0.0, min(1.0, float(page_y_ratio))) * pm.height())

            # Zielwert: Karten-Top + Innenabstand + Y in der Seite - kleiner Korrekturabzug
            y_target = base_y + pad_top + max(0, extra - margin_px)

            self._scroll.verticalScrollBar().setValue(y_target)
            self._update_current_page(force=True)


    def compute_smart_selection(self, page_index: int,
                                p0_label: QPoint, p1_label: QPoint,
                                label: QLabel):
        """
        Intelligente Textauswahl wie im PDF-Viewer:
        - Mapping Label -> PDF
        - findet Wörter in Lesereihenfolge
        - gruppiert Wörter pro Zeile
        - merged Rechtecke pro Zeile zu EINEM Balken
        """
        page = self._doc[page_index]
        pm = label.pixmap()
        if pm is None or pm.isNull():
            return [], []

        sx = page.rect.width / pm.width()
        sy = page.rect.height / pm.height()

        # Auswahlpunkte in PDF-Koordinaten
        p0 = fitz.Point(p0_label.x()*sx, p0_label.y()*sy)
        p1 = fitz.Point(p1_label.x()*sx, p1_label.y()*sy)

        words = page.get_text("words") or []
        if not words:
            return [], []

        # Sortieren nach (block, line, word)
        words.sort(key=lambda w: (w[5], w[6], w[7]))

        def center(w):
            return ((w[0]+w[2])/2, (w[1]+w[3])/2)

        def nearest(pt):
            best, best_d = 0, 1e99
            for i,w in enumerate(words):
                cx,cy = center(w)
                d = (cx-pt.x)**2 + (cy-pt.y)**2
                if d < best_d:
                    best_d = d
                    best = i
            return best

        i0 = nearest(p0)
        i1 = nearest(p1)
        if i0 > i1:
            i0, i1 = i1, i0

        selected = words[i0:i1+1]
        if not selected:
            return [], []

        # -------------------------
        # MERGING PRO ZEILE
        # -------------------------
        merged_pdf_rects = []
        merged_label_rects = []

        sx_inv = 1/sx
        sy_inv = 1/sy

        current_line = selected[0][6]
        line_rect = fitz.Rect(selected[0][0], selected[0][1],
                            selected[0][2], selected[0][3])

        for w in selected[1:]:
            if w[6] == current_line:
                # selbe Zeile → erweitern
                line_rect |= fitz.Rect(w[:4])
            else:
                # neue Zeile → vorherige abschließen
                merged_pdf_rects.append(line_rect)

                lx0 = int(line_rect.x0 * sx_inv)
                ly0 = int(line_rect.y0 * sy_inv)
                lx1 = int(line_rect.x1 * sx_inv)
                ly1 = int(line_rect.y1 * sy_inv)
                merged_label_rects.append(
                    QRect(lx0, ly0, lx1-lx0, ly1-ly0)
                )

                # Neue Zeile beginnen
                current_line = w[6]
                line_rect = fitz.Rect(w[0], w[1], w[2], w[3])

        # Letzte Zeile hinzufügen
        merged_pdf_rects.append(line_rect)
        lx0 = int(line_rect.x0 * sx_inv)
        ly0 = int(line_rect.y0 * sy_inv)
        lx1 = int(line_rect.x1 * sx_inv)
        ly1 = int(line_rect.y1 * sy_inv)
        merged_label_rects.append(QRect(lx0, ly0, lx1-lx0, ly1-ly0))

        return merged_pdf_rects, merged_label_rects


    def apply_highlight(self, page_index: int, pdf_rects: list):
        """
        Legt Highlight-Annotationen an und rendert neu (Scrollposition bleibt).
        """
        if not pdf_rects:
            return
        page = self._doc[page_index]
        for r in pdf_rects:
            a = page.add_highlight_annot(r)
            if a:
                a.set_opacity(0.35)
                a.update()

        # sichtbar machen
        vsb = self._scroll.verticalScrollBar()
        pos = vsb.value()
        self._render_pages()
        vsb.setValue(min(max(pos, vsb.minimum()), vsb.maximum()))

    def gotoNext(self): self.scrollToPage(self.currentPage() + 1)
    def gotoPrev(self): self.scrollToPage(self.currentPage() - 1)

    def _make_page_card(self, qimage):
        """
        Baut einen 'Seitenkarten'-Wrapper (weiß, Rand, Radius, Padding) + QLabel mit Pixmap.
        Weiß liegt NUR auf dem Wrapper – das Label selbst bleibt transparent.
        """
        from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
        from PyQt5.QtGui import QPixmap
        from PyQt5.QtCore import Qt, QSize

        wrapper = QWidget()
        wrapper.setObjectName("pageCard")
        # Nur der Wrapper ist weiß – Label bleibt transparent:
        wrapper.setStyleSheet("""
            QWidget#pageCard {
                background: white;
                border: 1px solid #d9d9dc;
                border-radius: 8px;
            }
        """)

        v = QVBoxLayout(wrapper)
        v.setContentsMargins(16, 16, 16, 16)   # Innenrand (weißer Rand um die Seite)
        v.setSpacing(0)

        lbl = QLabel()
        lbl.setStyleSheet("background: transparent;")  # wichtig: transparent!
        lbl.setAlignment(Qt.AlignCenter)               # Bild mittig innerhalb der Karte
        pm = QPixmap.fromImage(qimage)
        lbl.setPixmap(pm)

        # Damit die Karte NICHT horizontal streckt: wrapper orientiert sich an Inhalt
        lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        wrapper.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        v.addWidget(lbl, 0, Qt.AlignCenter)
        return wrapper


    def _render_pages(self):
        # Alte Widgets löschen
        for i in reversed(range(self._layout.count())):
            w = self._layout.itemAt(i).widget()
            if w:
                w.deleteLater()
        self._labels.clear()

        mat = fitz.Matrix(self._zoom, self._zoom)

        for page in self._doc:
            pix = page.get_pixmap(matrix=mat, alpha=False)
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)

            card = self._make_page_card(img)

            # --- ALT ---
            # inner_lbl = card.findChild(QLabel)
            # self._labels.append(inner_lbl)

            # --- NEU: inneres Label gegen PageImage tauschen ---
            inner_lbl = card.findChild(QLabel)  # das von _make_page_card erstellte
            pm = inner_lbl.pixmap()
            page_index = page.number

            pg = PageImage(self, page_index, pm, parent=card)
            pg.setStyleSheet(inner_lbl.styleSheet())
            pg.setAlignment(inner_lbl.alignment())
            pg.setSizePolicy(inner_lbl.sizePolicy())

            # Live-Auswahl finalisieren -> echte PDF-Highlights setzen
            # pg.selectionMade.connect(lambda idx, rects: self.apply_highlight(idx, rects))

            lay = card.layout()
            lay.removeWidget(inner_lbl)
            inner_lbl.deleteLater()
            lay.addWidget(pg, 0, Qt.AlignCenter)

            # Für Scroll-/Seitentracking weiterhin speichern
            self._labels.append(pg)

            # Karte in Spalte
            self._layout.addWidget(card, 0, Qt.AlignHCenter)

        self._layout.setSpacing(16)
        spacer = QWidget(); spacer.setFixedHeight(1)
        self._layout.addWidget(spacer)
        self._container.adjustSize()

    def _update_current_page(self, *_args, force=False):
        if not self._labels:
            return

        # Sichtbarer Bereich im Container-Koordinatensystem
        y_top = self._scroll.verticalScrollBar().value()
        # Breite ruhig „groß“ wählen – wir vergleichen vertikal
        rect_visible = QRect(0, y_top, self._container.width(), self._scroll.viewport().height())

        best_idx, best_score = 0, -1
        for i, lbl in enumerate(self._labels):
            # -> WICHTIG: die KARTEN-Geometrie (Eltern-Widget) nehmen
            card = lbl.parentWidget()
            r = self._container_rect(card)
            inter = r.intersected(rect_visible)
            score = inter.width() * inter.height()
            if score > best_score:
                best_score, best_idx = score, i

        current_one_based = best_idx + 1
        if force or current_one_based != self._last_reported_page:
            self._last_reported_page = current_one_based
            self.currentPageChanged.emit(current_one_based)

    def load_document(self, pdf_path: str):
        """Dokument tauschen und neu rendern (Fit-to-Width bleibt erhalten)."""
        # Altes Dokument sauber schließen
        try:
            if hasattr(self, "_doc") and self._doc is not None:
                self._doc.close()
        except Exception:
            pass

        # Neues Dokument öffnen
        self._doc = fitz.open(pdf_path)

        # Basisbreite für Fit-to-Width neu bestimmen (falls du das nutzt)
        try:
            first_page = self._doc[0] if self._doc.page_count > 0 else None
            self._base_page_width = first_page.rect.width if first_page else 595.0
        except Exception:
            self._base_page_width = 595.0

        # Rendern
        if getattr(self, "_fit_to_width", False):
            self._set_zoom_to_fit_width()
        self._render_pages()
        self._update_current_page(force=True)

# from PyQt5.QtCore import QTimer
    def wheelEvent(self, event):
        # STRG+Rad wird vom _CtrlWheelFilter am Viewport vollständig abgefangen
        super().wheelEvent(event)


    def _freeze_zoom_and_render(self, new_zoom: float):
        vsb = self._scroll.verticalScrollBar()
        frozen_val = vsb.value()

        self._scroll.setUpdatesEnabled(False)
        try:
            self._zoom = new_zoom
            self._render_pages()
            vsb.setValue(max(vsb.minimum(), min(vsb.maximum(), frozen_val)))
        finally:
            self._scroll.setUpdatesEnabled(True)
        # zweiter Set nach Layout
        QTimer.singleShot(0, lambda: vsb.setValue(max(vsb.minimum(), min(vsb.maximum(), frozen_val))))
        self.zoomChanged.emit(self._zoom)

    def keyPressEvent(self, event):
        ctrl = bool(event.modifiers() & Qt.ControlModifier)
        if ctrl and event.key() in (Qt.Key_Plus, Qt.Key_Equal):
            self._freeze_zoom_and_render(min(6.0, self._zoom * 1.2)); return
        if ctrl and event.key() == Qt.Key_Minus:
            self._freeze_zoom_and_render(max(0.3, self._zoom / 1.2)); return
        if ctrl and event.key() == Qt.Key_0:
            self._freeze_zoom_and_render(1.5); return
        if event.key() == Qt.Key_Left:  self.gotoPrev(); return
        if event.key() == Qt.Key_Right: self.gotoNext(); return
        super().keyPressEvent(event)

    def extract_quads_from_label_rect(self, page_index, rect_in_label, label: QLabel):
        page = self._doc[page_index]
        pm = label.pixmap()
        if pm is None:
            return []

        # Berechne Verhältnis Label→PDF
        scale_x = page.rect.width / pm.width()
        scale_y = page.rect.height / pm.height()

        # Transformiere Auswahl-Rect in PDF-Koordinaten
        pdf_rect = fitz.Rect(
            rect_in_label.x() * scale_x,
            rect_in_label.y() * scale_y,
            rect_in_label.right() * scale_x,
            rect_in_label.bottom() * scale_y
        )

        # Alle Wörter der Seite abrufen
        words = page.get_text("words")  # (x0,y0,x1,y1, word, block_no, line_no, word_no)

        quads = []
        for w in words:
            wrect = fitz.Rect(w[:4])
            if pdf_rect.intersects(wrect):
                quads.append(wrect)

        return quads
    
    def apply_highlight(self, page_index, quads):
        page = self._doc[page_index]

        for rect in quads:
            page.add_highlight_annot(rect)

        # Seite neu rendern
        vsb = self._scroll.verticalScrollBar()
        pos = vsb.value()
        self._render_pages()
        vsb.setValue(pos)


    def extract_text_from_pdf_rects(self, page_index: int, rects: list) -> str:
        """Gibt den Text der ausgewählten Rechtecke (in Reihenfolge) zurück."""
        if not rects:
            return ""

        page = self._doc[page_index]
        parts = []

        for r in rects:
            txt = page.get_textbox(r)  # exakter Text des Wort- oder Zeilen-Rects
            if txt:
                parts.append(txt.strip())

        # Leerzeichen/Zeilenumbrüche sinnvoll setzen
        return " ".join(parts)
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
        self.setPixmap(pixmap)

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


class Ui_Dialog_pdfviewer(object):
    ROLE_TARGET = Qt.UserRole          # (page, y_ratio)
    ROLE_COLORSTATE = Qt.UserRole + 1  # 0..3 (0=weiß,1=cat0,2=cat1,3=cat2)

    def setupUi(self, Dialog: QDialog, file_path: str):
        # --- State ---
        self._current_pdf_path = file_path
        self.Dialog = Dialog
        self.Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("PDF Viewer")
        Dialog.setWindowIcon(QIcon(logo_path))  # logo_path muss gültig sein

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
            QListWidget::item { padding: 6px 8px; }
        """)
        self.list.setItemDelegate(
            ColorAwareBorderDelegate(border_color="#0078D4", border_width=2, radius=6, parent=self.list)
        )

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        # WICHTIG: links etwas Luft, damit Checkbox-Indikatoren nicht abgeschnitten werden
        left_layout.setContentsMargins(12, 0, 0, 0)   # ← 12px linker Innenabstand
        left_layout.setSpacing(0)
        left_layout.addWidget(self.header)
        left_layout.addWidget(self.list)

        # --- Rechte Seite: PDF-Viewer ---
        self.viewer = PdfWidget(self._current_pdf_path)
        self.viewer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.spin_zoom.setValue(self.viewer.get_zoom_percent())
        # --- Splitter (Mitte) ---
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(self.viewer)
        splitter.setStretchFactor(0, 0)   # linkes Panel
        splitter.setStretchFactor(1, 1)   # Viewer dehnt
        splitter.setSizes([300, 2000])    # Start: viel Platz rechts

        # --- Zentrale Fläche ---
        central = QWidget()
        lay = QHBoxLayout(central)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(splitter)
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

        # Header-Änderungen -> Anzeige aktualisieren
        self.header.categoryToggled.connect(self._on_category_toggled)
        self.header.colorChanged.connect(self._on_category_color_changed)
        self.header.labelChanged.connect(self._on_category_label_changed)
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


        # 🔹 Strg+C überall im Dialog -> kopiert die aktuelle Bildauswahl
        sc_copy = QShortcut(QKeySequence.Copy, self.Dialog)
        sc_copy.setContext(Qt.ApplicationShortcut)

        def _on_copy():
            w = self.Dialog.focusWidget()
            # Falls gerade das Bild den Fokus hat, dort kopieren
            if isinstance(w, PageImage):
                w.copy_to_clipboard()
                return
            # Sonst: letzten Text aus dem Viewer nehmen (falls vorhanden)
            from PyQt5.QtWidgets import QApplication
            txt = self.viewer.get_last_selected_text() if hasattr(self.viewer, "get_last_selected_text") else ""
            if txt:
                QApplication.clipboard().setText(txt)

        sc_copy.activated.connect(_on_copy)

    def refresh_pdf(self, file_path: str):
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
            # Anzeige abhängig vom Markierungsstatus
            if self.header.markingEnabled():
                it.setBackground(Qt.white); it.setForeground(Qt.black)
            else:
                # bei aus: ohnehin weiß
                it.setBackground(Qt.white); it.setForeground(Qt.black)
            self.list.addItem(it)

    # ----- Farben anwenden (state: 0=weiß,1=cat0,2=cat1,3=cat2) -----
    def _apply_color_state(self, item: QListWidgetItem, state: int):
        # Zustand setzen (logisch)
        item.setData(self.ROLE_COLORSTATE, state)
        # Anzeige über Recolor zentral aktualisieren
        # (so ist Masken-Logik an EINER Stelle)
        st = int(item.data(self.ROLE_COLORSTATE) or 0)
        if st == 0:
            item.setBackground(Qt.white); item.setForeground(Qt.black); return
        mask = self.header.enabledMask()
        cat_idx = st - 1
        if (mask & (1 << cat_idx)) == 0:
            item.setBackground(Qt.white); item.setForeground(Qt.black)
        else:
            col = self.header.colors()[cat_idx]
            item.setBackground(col); item.setForeground(Qt.black)

    def _recolor_all_items(self):
        mask = self.header.enabledMask()  # Bit0=Rot(1), Bit1=Gelb(2), Bit2=Grün(4)
        for i in range(self.list.count()):
            it = self.list.item(i)
            st = int(it.data(self.ROLE_COLORSTATE) or 0)  # 0=weiß, 1=rot, 2=gelb, 3=grün
            if st == 0:
                it.setBackground(Qt.white); it.setForeground(Qt.black)
            else:
                cat_idx = st - 1  # 0..2
                if (mask & (1 << cat_idx)) == 0:
                    # Kategorie ist deaktiviert -> weiß darstellen
                    it.setBackground(Qt.white); it.setForeground(Qt.black)
                else:
                    # Kategorie aktiv -> echte Farbe anwenden
                    col = self.header.colors()[cat_idx]
                    it.setBackground(col); it.setForeground(Qt.black)

    # ----- Click-Handling -----
    def _on_task_clicked(self, item: QListWidgetItem):
        # 1) Navigation
        data = item.data(self.ROLE_TARGET)
        if data:
            page, y_ratio = data
            self.viewer.scrollToPageLocation(page, y_ratio)

        # 2) Farbzyklus nur, wenn Item VOR dem Klick schon ausgewählt war
        pf = self._pressFilter
        if pf.was_selected and (item is pf.pressed_item):
            cur = int(item.data(self.ROLE_COLORSTATE) or 0)  # 0..3
            nxt = self._next_enabled_state(cur)
            # Nur ändern, wenn sich der Zustand tatsächlich ändert
            if nxt != cur:
                self._apply_color_state(item, nxt)
        # Flags zurücksetzen
        pf.was_selected = False
        pf.pressed_item = None

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
        # aktuell nur Info; später evtl. Tooltips/Badges etc.
        pass

    # ----- Toolbar-Events -----


    def _on_current_page_changed(self, page_one_based: int):
        """Vom Viewer beim Scrollen/Wechseln gefeuert -> Spinbox nachziehen."""
        if self.spin_page.value() != page_one_based:
            self.spin_page.blockSignals(True)
            self.spin_page.setValue(page_one_based)
            self.spin_page.blockSignals(False)


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