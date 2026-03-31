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

    def request_render_all_pages(self, zoom_int):
        """Render ALL pages for the new zoom in background."""
        self.queue.clear()

        for i in range(len(self.doc)):
            self.queue.append((i, zoom_int))

        if not self._busy:
            self._process_next()

    def _process_next(self):
        if not self.queue:
            self._busy = False
            return

        self._busy = True

        page_index, zoom_int = self.queue.pop(0)
        zoom = zoom_int / 100.0
        mat = fitz.Matrix(zoom, zoom)

        # render page to pixmap
        pix = self.doc[page_index].get_pixmap(matrix=mat, alpha=True)

        # convert to QImage
        img = QImage(
            pix.samples,
            pix.width,
            pix.height,
            pix.stride,
            QImage.Format_RGBA8888
        ).copy()

        # send result
        self.rendered.emit(page_index, zoom_int, img)

        QTimer.singleShot(0, self._process_next)


    def render_pages(self, pages, zoom_int):
        # Nur Jobs für DIESEN Zoom ersetzen
        new_queue = []
        for p in pages:
            new_queue.append((p, zoom_int))

        # Ersetze queue durch neue Jobs
        self.queue = new_queue


        self._busy = False
        QTimer.singleShot(0, self._process_next)


    def stop(self):
        self._busy = False
        self.queue.clear()
        self.doc = None

    # def render_pages(self, pages, zoom_int): ##SEHR SCHNELL!!!
    #     self.queue.clear()
    #     for i in pages:
    #         self.queue.append((i, zoom_int))
    #     if not self._busy:
    #         QTimer.singleShot(0, self._process_next)