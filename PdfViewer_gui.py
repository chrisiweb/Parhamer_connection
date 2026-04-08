from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QApplication, QShortcut
from PyQt5.QtCore import pyqtSignal, QThread, Qt, QEvent, QPoint, QTimer, QObject
from PyQt5.QtGui import QKeySequence 
import fitz

from PdfCanvas import PdfCanvas
from SearchOverlay import SearchOverlay

class _DialogEscBlocker(QObject):
    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.KeyPress and ev.key() == Qt.Key_Escape:
            return True  # ESC komplett blockieren
        return False


class PdfViewer(QWidget):
    currentPageChanged = pyqtSignal(int)  # 1-based

    def __init__(self, pdf_path, ui_dialog=None, tindb_data = None):
        super().__init__()
        self.ui_dialog = ui_dialog
        self.tindb_data = tindb_data
        self.doc = fitz.open(pdf_path)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        layout.addWidget(self.scroll)

        self.canvas = PdfCanvas(self.doc, ui_dialog=self.ui_dialog, tindb_data = self.tindb_data)
        self.scroll.setWidget(self.canvas)



        self.scroll.verticalScrollBar().valueChanged.connect(self._on_scroll)

        # self.scroll.viewport().installEventFilter(self)

        self.scroll.viewport().setAttribute(Qt.WA_NoMousePropagation, True)
        self.scroll.viewport().installEventFilter(self)


        # --- Such-Overlay ---
        self.search = SearchOverlay(None)
        self.search.hide()

        self.search.searchRequested.connect(self._on_search)
        self.search.nextRequested.connect(self._on_search_next)
        self.search.prevRequested.connect(self._on_search_prev)
        self.search.closeRequested.connect(self._on_search_close)

        self._search_results = []
        self._search_index = -1
        self.setMinimumWidth(400)



        # ESC global abfangen
        self._esc_shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self._esc_shortcut.setContext(Qt.ApplicationShortcut)
        self._esc_shortcut.activated.connect(self._on_escape)      

        self._esc_blocker = _DialogEscBlocker()
        self.ui_dialog.Dialog.installEventFilter(self._esc_blocker)


        self._find_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_F), self)
        self._find_shortcut.setContext(Qt.ApplicationShortcut)
        self._find_shortcut.activated.connect(self._open_search)


    # ========== API-KOMPATIBILITÄT ZU DEINEM ALTEN PdfWidget ==========

    def pageCount(self):
        return self.doc.page_count

    def currentPage(self):
        scroll_y = self.scroll.verticalScrollBar().value()
        for i, (y, h) in enumerate(self.canvas.page_positions):
            if y + h > scroll_y + 10:
                return i + 1
        return 1

    def scrollToPage(self, p):
        p = max(1, min(self.pageCount(), p))
        y, _ = self.canvas.page_positions[p - 1]
        self.scroll.verticalScrollBar().setValue(int(y))

    def scrollToPageLocation(self, p, ratio, margin_px=8):
        if ratio is None:
            self.scrollToPage(p)
            return

        p = max(1, min(self.pageCount(), p))
        y, h = self.canvas.page_positions[p - 1]
        target = int(y + max(0, min(1, ratio)) * h - margin_px)
        self.scroll.verticalScrollBar().setValue(target)

    def gotoPrev(self):
        self.scrollToPage(self.currentPage() - 1)

    def gotoNext(self):
        self.scrollToPage(self.currentPage() + 1)

    # ========== INTERNAL ==========

    def _on_scroll(self):
        self.canvas.update()  # <- NEU: einfach neu zeichnen
        self.currentPageChanged.emit(self.currentPage())

    

    def load_document(self, pdf_path):

        # HARTE ABKÜHLUNG: Queue leeren und alle alten Renderjobs verwerfen

        """
        Lädt ein neues PDF und ersetzt sauber das alte Dokument.
        """

        # ---------- PDF ersetzen ----------
        self.doc = fitz.open(pdf_path)
        self.canvas.doc = self.doc

        self.canvas.cache_raw.clear()
        self.canvas.cache_scaled.clear()

        self.canvas._compute_positions()
        self.canvas.sel_label_rects = []
        self.canvas.selected_text = ""
        self.canvas.update()


        # ---------- Seite 1 anzeigen ----------
        if len(self.canvas.page_positions) > 0:
            y, _ = self.canvas.page_positions[0]
            self.scroll.verticalScrollBar().setValue(int(y))

        self.currentPageChanged.emit(1)


    def apply_zoom_factor(self, factor, focal_point=None):
        old = self.canvas.zoom
        new = max(0.2, min(5.0, old * factor))

        if abs(new - old) < 0.001:
            return

        # 1) Focal point im viewport
        if focal_point is None:
            focal_point = QPoint(
                self.scroll.viewport().width() // 2,
                self.scroll.viewport().height() // 2
            )

        # 2) globale Canvas-Koordinaten
        canvas_x = self.scroll.horizontalScrollBar().value() + focal_point.x()
        canvas_y = self.scroll.verticalScrollBar().value() + focal_point.y()

        # 3) Seite finden
        page_index = None
        for i, (py, ph) in enumerate(self.canvas.page_positions):
            if py <= canvas_y <= py + ph:
                page_index = i
                break
        if page_index is None:
            page_index = 0

        page = self.canvas.doc[page_index]

        # -----------------------------
        #    WICHTIGSTE ÄNDERUNG:
        # -----------------------------
        # HORIZONTALER OFFSET MUSS IDENTISCH ZU paintEvent SEIN!
        # UND IMMER scaled.width() VERWENDEN!
        # -----------------------------

        # VOR DEM ZOOM
        if page_index in self.canvas.cache_scaled:
            old_scaled = self.canvas.cache_scaled[page_index]
            old_page_pixel_width = old_scaled.width()
        else:
            old_page_pixel_width = int(page.rect.width * old)

        # old_page_total_width = old_page_pixel_width + 2 * self.canvas.PAGE_PADDING

        old_x_page = self.compute_x_page(page_index, old)
        old_pdf_left_canvas = old_x_page + self.canvas.PAGE_PADDING


        # Vertikal vor Zoom
        old_page_y_top = self.canvas.page_positions[page_index][0]
        old_pdf_top = old_page_y_top + self.canvas.PAGE_PADDING

        # Canvas → PDF
        pdf_x = (canvas_x - old_pdf_left_canvas) / old
        pdf_y = (canvas_y - old_pdf_top) / old

        # -----------------------------
        # 4) Zoom durchführen
        # -----------------------------
        self.canvas.zoom = new
        self.canvas.quick_scale()
        self.canvas._compute_positions()

        # neue Mindestbreite setzen
        self.canvas.updateGeometry()

        # JETZT ERNEUT Breite + Offsets HOLEN
        if page_index in self.canvas.cache_scaled:
            new_scaled = self.canvas.cache_scaled[page_index]
            new_page_pixel_width = new_scaled.width()
        else:
            new_page_pixel_width = int(page.rect.width * new)

        # new_page_total_width = new_page_pixel_width + 2 * self.canvas.PAGE_PADDING

        new_x_page = self.compute_x_page(page_index, new)
        new_pdf_left_canvas = new_x_page + self.canvas.PAGE_PADDING


        new_page_y_top = self.canvas.page_positions[page_index][0]
        new_pdf_top = new_page_y_top + self.canvas.PAGE_PADDING

        # 5) PDF zurück → Canvas
        new_canvas_x = pdf_x * new + new_pdf_left_canvas
        new_canvas_y = pdf_y * new + new_pdf_top

        # 6) Scrollbars setzen
        self.scroll.horizontalScrollBar().setValue(int(new_canvas_x - focal_point.x()))
        self.scroll.verticalScrollBar().setValue(int(new_canvas_y - focal_point.y()))




    def event(self, ev):
        if ev.type() == QEvent.NativeGesture:
            if ev.gestureType() == Qt.ZoomNativeGesture:
                factor = 1.0 + ev.value()   # value etwa zwischen -0.1 und +0.1
                self.apply_zoom_factor(factor)
                return True
        return super().event(ev)


    def resizeEvent(self, ev):

        super().resizeEvent(ev)
        if self.search and self.search.isVisible():
            self.position_search_popup()



    def keyPressEvent(self, e):

        # if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_F:

        #     self.search.show()
        #     self.search.raise_()
        #     self.position_search_popup()
        #     self.start_popup_tracking()   # ✅ HIER

        #     QTimer.singleShot(0, lambda: (
        #         self.search.activateWindow(),
        #         self.search.edt.setFocus()
        #     ))


        #     self.search.setCount(0, 0)
        #     self.search.edt.clear()
        #     return


        if e.modifiers() == Qt.ControlModifier:
            if e.key() == Qt.Key_Plus:
                self.zoom_in(step=0.1)
                return
            if e.key() == Qt.Key_Minus:
                self.zoom_out(step=0.1)
                return
        super().keyPressEvent(e)

    def zoom_in(self, step=0.1):
        self.canvas.clear_selection()
        self.apply_zoom_factor(1 + step)

    def zoom_out(self, step=0.1):
        self.canvas.clear_selection()
        self.apply_zoom_factor(1 - step)


    def visible_pages(self):
        top = self.scroll.verticalScrollBar().value()
        bottom = top + self.scroll.viewport().height()

        visible = []
        for i, (y, h) in enumerate(self.canvas.page_positions):
            # Eine Seite ist dann sichtbar, wenn sie zumindest 1 Pixel im Sichtbereich hat
            if y < bottom and (y + h) > top:
                visible.append(i)

        # ✅ Sicherheitslimit: maximal 4 Seiten
        return visible[:4]
    
    def eventFilter(self, obj, e):
        # # ✅ STRG + rechte Maustaste -> Notizfenster öffnen
        # if obj == self.scroll.viewport() and e.type() == QEvent.MouseButtonPress:
        #     if e.button() == Qt.RightButton and QApplication.keyboardModifiers() & Qt.ControlModifier:
                
        #         # Aufgabennummer bestimmen
        #         page = self.currentPage()      # 1-based
                
        #         aufgabe = f"Aufgabe {page}"

        #         # Fenster öffnen
        #         dlg = Sour(aufgabe, parent=self)
        #         dlg.exec_()

        #         return True
        if obj == self.scroll.viewport() and e.type() == QEvent.Wheel:
            if e.modifiers() & Qt.ControlModifier:
                self.canvas.clear_selection()
                # Viewport-Koordinate der Maus
                vp_x = e.pos().x()
                vp_y = e.pos().y()
                # # ScrollOffsets holen
                # sx = self.scroll.horizontalScrollBar().value()
                # sy = self.scroll.verticalScrollBar().value()

                # ✅ CANVAS-Koordinaten des Mauspunktes
                focal = QPoint(vp_x, vp_y)
                # Zoom-Faktor bestimmen
                if e.angleDelta().y() > 0:
                    self.apply_zoom_factor(1.3, focal_point=focal)
                else:
                    self.apply_zoom_factor(0.7, focal_point=focal)

                # ScrollEvent vollständig blockieren
                
                return True

        return super().eventFilter(obj, e)
    

    def compute_x_page(self, page_index, zoom):
        # Der Canvas zeichnet IMMER nach scaled.width(), nicht nach PDF-Maßen!
        if page_index in self.canvas.cache_scaled:
            scaled = self.canvas.cache_scaled[page_index]
            page_pixel_width = scaled.width()
        else:
            # fallback – aber korrekt!
            page = self.canvas.doc[page_index]
            page_pixel_width = int(page.rect.width * zoom)

        total_width = page_pixel_width + 2 * self.canvas.PAGE_PADDING
        x_page = max(0, (self.canvas.width() - total_width) // 2)
        return x_page

    def closeEvent(self, e):
        pass


    def _on_search(self, text):
        text = text.strip().lower()

        # ✅ ALLES zurücksetzen
        self._search_results = []
        self._search_index = -1
        self.canvas.search_highlights = []
        self.canvas.update()

        # ✅ Leeres Feld → nichts suchen, nichts markieren
        if text == "":
            self.search.setCount(0, 0)
            return

        # ✅ Treffer suchen
        for pno in range(self.doc.page_count):
            page = self.doc[pno]
            rects = page.search_for(text)
            for r in rects:
                self._search_results.append((pno, r))

        # ✅ Keine Treffer → Zähler auf 0
        if not self._search_results:
            self.search.setCount(0, 0)
            return

        # ✅ Ersten Treffer anspringen
        self._search_index = 0
        self._goto_search_result(0)

        # ✅ Trefferzähler setzen
        self.search.setCount(self._search_index, len(self._search_results))



    def _on_search_next(self):
        if not self._search_results:
            return
        self._search_index = (self._search_index + 1) % len(self._search_results)
        self._goto_search_result(self._search_index)
        self.search.setCount(self._search_index, len(self._search_results))


    def _on_search_prev(self):
        if not self._search_results:
            return
        self._search_index = (self._search_index - 1) % len(self._search_results)
        self._goto_search_result(self._search_index)
        self.search.setCount(self._search_index, len(self._search_results))


    def _on_search_close(self):
        if self.canvas:
            self.canvas.search_highlights = []
            self.canvas.update()
            self.search.setCount(0, 0)


    def _goto_search_result(self, i):
        page_index, rect = self._search_results[i]

        self.scrollToPage(page_index + 1)

        # highlight setzen
        if hasattr(self.canvas, "apply_search_highlight"):
            self.canvas.apply_search_highlight(page_index, rect)



    def position_search_popup(self):
        if not self.search.isVisible():
            return

        margin_x = 100
        margin_y = 50

        # ✅ globale Position des QDialogs holen
        dialog_global = self.ui_dialog.Dialog.mapToGlobal(QPoint(0, 0))

        # ✅ relative Position des PdfViewers innerhalb des QDialogs
        relative = self.mapTo(self.ui_dialog.Dialog, QPoint(0, 0))

        # ✅ finale globale Position des Suchfensters
        x = dialog_global.x() + relative.x() + self.width() - self.search.width() - margin_x
        y = dialog_global.y() + relative.y() + margin_y

        self.search.move(x, y)


    def start_popup_tracking(self):
        self._last_dialog_pos = None

        def check_position():
            if not self.search.isVisible():
                return

            dialog = self.ui_dialog.Dialog
            if dialog is None:
                return

            current = dialog.pos()
            if self._last_dialog_pos != current:
                self._last_dialog_pos = current
                self.position_search_popup()

        # alle 30 ms prüfen
        self._popup_tracker = QTimer(self)
        self._popup_tracker.timeout.connect(check_position)
        self._popup_tracker.start(30)


    def _on_escape(self):
        # 1) Wenn Suche offen → schließen
        if self.search and self.search.isVisible():
            self._on_search_close()
            self.search.hide()
            return

    def _open_search(self):
        self.search.show()
        self.search.raise_()
        self.position_search_popup()
        self.start_popup_tracking()

        self.search.setCount(0, 0)
        self.search.edt.clear()
        self.search.edt.setFocus()