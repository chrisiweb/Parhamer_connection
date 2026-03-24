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

        if focal_point is None:
            focal_point = QPoint(
                self.scroll.horizontalScrollBar().value() + self.width() // 2,
                self.scroll.verticalScrollBar().value() + self.height() // 2
            )

        pdf_x = (focal_point.x() + self.scroll.horizontalScrollBar().value()) / old
        pdf_y = (focal_point.y() + self.scroll.verticalScrollBar().value()) / old

        # Zoom setzen
        self.canvas.zoom = new

        # <<< SMOOTH, NO‑LAG SCALING >>>
        self.canvas.quick_scale()

        new_x = pdf_x * new
        new_y = pdf_y * new

        self.scroll.horizontalScrollBar().setValue(int(new_x - focal_point.x()))
        self.scroll.verticalScrollBar().setValue(int(new_y - focal_point.y()))

        # <<< HINTERGRUND-NACHSCHÄRFUNG >>>

        pages = self.visible_pages()
        self.worker.render_pages(pages, int(new * 100))



    def wheelEvent(self, e):
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            delta = e.angleDelta().y()
            if delta > 0:
                self.zoom_in(step=0.1)
            else:
                self.zoom_out(step=0.1)
            return  # verhindert Scroll
        super().wheelEvent(e)

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
    