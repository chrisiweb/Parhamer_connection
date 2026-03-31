from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QApplication
from PyQt5.QtCore import pyqtSignal, QThread, Qt, QEvent, QPoint
import fitz

from PdfCanvas import PdfCanvas
from RenderWorker import RenderWorker


class PdfViewer(QWidget):
    currentPageChanged = pyqtSignal(int)  # 1-based

    def __init__(self, pdf_path):
        super().__init__()

        self.doc = fitz.open(pdf_path)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        layout.addWidget(self.scroll)

        self.canvas = PdfCanvas(self.doc)
        self.scroll.setWidget(self.canvas)

        # Worker thread
        self.thread = QThread()
        self.worker = RenderWorker(self.doc)
        self.worker.moveToThread(self.thread)
        self.worker.rendered.connect(self.canvas.insert_rendered)
        self.thread.start()

        pages = self.visible_pages()
        self.worker.render_pages(pages, int(self.canvas.zoom * 100))

        self.scroll.verticalScrollBar().valueChanged.connect(self._on_scroll)

        # self.scroll.viewport().installEventFilter(self)

        self.scroll.viewport().setAttribute(Qt.WA_NoMousePropagation, True)
        self.scroll.viewport().installEventFilter(self)

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
        self.canvas.quick_scale()
        pages = self.visible_pages()
        self.worker.render_pages(pages, int(self.canvas.zoom*100))
        self.currentPageChanged.emit(self.currentPage())

    

    def load_document(self, pdf_path):
        """
        Lädt ein neues PDF und ersetzt sauber das alte Dokument.
        """
        # ---------- alten Worker stoppen ----------
        try:
            self.worker.rendered.disconnect()
        except:
            pass

        try:
            self.worker.stop()
        except:
            pass

        try:
            self.thread.quit()
            self.thread.wait()
        except:
            pass
        # ---------- PDF ersetzen ----------
        self.doc = fitz.open(pdf_path)
        self.canvas.doc = self.doc

        self.canvas.cache_raw.clear()
        self.canvas.cache_scaled.clear()

        self.canvas._compute_positions()
        self.canvas.sel_label_rects = []
        self.canvas.selected_text = ""
        self.canvas.update()

        # ---------- neuen Worker starten ----------
        self.thread = QThread()
        self.worker = RenderWorker(self.doc)
        self.worker.moveToThread(self.thread)
        self.worker.rendered.connect(self.canvas.insert_rendered)
        self.thread.start()

        pages = self.visible_pages()
        self.worker.render_pages(pages, int(self.canvas.zoom * 100))

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

        # Rendern
        pages = self.visible_pages()
        self.worker.render_pages(pages, int(new * 100))


    def event(self, ev):
        if ev.type() == QEvent.NativeGesture:
            if ev.gestureType() == Qt.ZoomNativeGesture:
                factor = 1.0 + ev.value()   # value etwa zwischen -0.1 und +0.1
                self.apply_zoom_factor(factor)
                return True
        return super().event(ev)


    def keyPressEvent(self, e):
        if e.modifiers() == Qt.ControlModifier:
            if e.key() == Qt.Key_Plus:
                self.zoom_in(step=0.1)
                return
            if e.key() == Qt.Key_Minus:
                self.zoom_out(step=0.1)
                return
        super().keyPressEvent(e)

    def zoom_in(self, step=0.1):
        self.apply_zoom_factor(1 + step)

    def zoom_out(self, step=0.1):
        self.apply_zoom_factor(1 - step)


    def visible_pages(self):
        top = self.scroll.verticalScrollBar().value()
        bottom = top + self.scroll.viewport().height()

        visible = []

        for i, (y, h) in enumerate(self.canvas.page_positions):
            if y + h >= top - 200 and y <= bottom + 200:
                visible.append(i)

        return visible
    
    def eventFilter(self, obj, e):
        if obj == self.scroll.viewport() and e.type() == QEvent.Wheel:
            if e.modifiers() & Qt.ControlModifier:

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
        try:
            self.worker.rendered.disconnect()
        except:
            pass
        try:
            self.worker.stop()
        except:
            pass
        try:
            self.thread.quit()
            self.thread.wait()
        except:
            pass
        super().closeEvent(e)
