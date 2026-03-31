from PyQt5.QtCore import QObject, pyqtSignal, QTimer
import fitz
from PyQt5.QtGui import QImage

class RenderWorker(QObject):
    rendered = pyqtSignal(int, int, QImage)  # page_index, zoom_int, image

    def __init__(self, doc):
        super().__init__()
        self.doc = doc
        self.queue = []
        self._busy = False
        self._stop = False   # ✅ Abbruchflag

    def stop(self):
        """Stoppt alle zukünftigen Renderjobs."""
        self._stop = True
        self.queue.clear()
        self._busy = False

    # ----------------------------------------------------

    def request_render_all_pages(self, zoom_int):
        self.queue.clear()
        self._stop = False   # ✅ neu starten erlaubt

        for i in range(len(self.doc)):
            self.queue.append((i, zoom_int))

        if not self._busy:
            self._process_next()

    # ----------------------------------------------------

    def render_pages(self, pages, zoom_int):
        """Rendert NUR die angegebenen Seiten für den aktuellen Zoom."""
        self.queue = [(p, zoom_int) for p in pages]
        self._stop = False
        self._busy = False
        QTimer.singleShot(0, self._process_next)

    # ----------------------------------------------------

    def _process_next(self):
        """Interner Render-Loop."""
        # ✅ Abbruch prüfen
        if self._stop:
            self.queue.clear()
            self._busy = False
            return

        # ✅ Queue leer?
        if not self.queue:
            self._busy = False
            return

        self._busy = True

        page_index, zoom_int = self.queue.pop(0)

        # ✅ PDF gelockt?
        if self.doc is None:
            return

        # ✅ Seite existiert noch?
        if page_index < 0 or page_index >= len(self.doc):
            return

        zoom = zoom_int / 100.0
        mat = fitz.Matrix(zoom, zoom)

        try:
            pix = self.doc[page_index].get_pixmap(matrix=mat, alpha=True)
        except:
            return  # PDF wurde gewechselt oder geschlossen

        img = QImage(
            pix.samples,
            pix.width,
            pix.height,
            pix.stride,
            QImage.Format_RGBA8888
        ).copy()

        # ✅ Ergebnis senden, aber nur wenn NICHT abgebrochen
        if not self._stop:
            self.rendered.emit(page_index, zoom_int, img)

        # Wieder nächsten Job ausführen
        QTimer.singleShot(0, self._process_next)