from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPixmap, QKeySequence
from PyQt5.QtCore import QRect, Qt, QPoint
import fitz


class PdfCanvas(QWidget):
    BACKGROUND_COLOR = QColor("#e5e5e5")
    PAGE_BORDER = QColor("#c8c8c8")
    PAGE_BG = QColor("#ffffff")
    PAGE_MARGIN = 20
    PAGE_PADDING = 12

    def __init__(self, doc):
        super().__init__()
        self.doc = doc
        self.zoom = 1.5

        # ✅ Original (vom Worker) + skaliert (für Anzeige/Auswahl)
        self.cache_raw = {}
        self.cache_scaled = {}

        # ✅ Auswahl
        self._selecting = False
        self.sel_page = None
        self.sel_start = None
        self.sel_end = None
        self.sel_label_rects = []
        self.selected_text = ""

        self._compute_positions()
        self.setFocusPolicy(Qt.StrongFocus)
        self.setCursor(Qt.IBeamCursor)

    # -------------------------------------------------------
    # Layout
    # -------------------------------------------------------
    def _compute_positions(self):
        self.page_positions = []
        y = self.PAGE_MARGIN

        for i in range(self.doc.page_count):
            scaled = self.cache_scaled.get(i)

            if scaled is not None:
                h = scaled.height()
            else:
                # letzte bekannte Höhe merken (aus raw render)
                page = self.doc[i]
                h = int(page.rect.height * self.zoom)

            total = h + 2 * self.PAGE_PADDING
            self.page_positions.append((y, total))
            y += total + self.PAGE_MARGIN

        self.setMinimumHeight(int(y + self.PAGE_MARGIN))


        # --- neue Mindestbreite basierend auf der breitesten Seite ---
        max_width = 0
        for i, page in enumerate(self.doc):
            if i in self.cache_scaled:
                w = self.cache_scaled[i].width() + 2 * self.PAGE_PADDING
            else:
                w = int(page.rect.width * self.zoom) + 2 * self.PAGE_PADDING
            max_width = max(max_width, w)

        self.setMinimumWidth(max_width + self.PAGE_MARGIN * 2)
    # -------------------------------------------------------
    # Rendering
    # -------------------------------------------------------
    def paintEvent(self, ev):

        p = QPainter(self)
        p.fillRect(self.rect(), self.BACKGROUND_COLOR)


        for index, (y, total_h) in enumerate(self.page_positions):

            # Korrekte ScrollArea holen
            scrollarea = self.parent().parent()  # viewport -> scrollarea

            view_y_top = scrollarea.verticalScrollBar().value()
            view_y_bottom = view_y_top + scrollarea.viewport().height()

            # Seite oberhalb des sichtbaren Bereichs
            if y + total_h < view_y_top - 200:
                continue

            # Seite unterhalb des sichtbaren Bereichs
            if y > view_y_bottom + 200:
                break



            page = self.doc[index]
            page_key = (index, int(self.zoom * 100))


            
            page_width = int(page.rect.width * self.zoom) + 2 * self.PAGE_PADDING
            x_page = max(0, (self.width() - page_width) // 2) #links zentriert: = 40

            if index in self.cache_scaled:
                scaled = self.cache_scaled[index]
                scaled_w = scaled.width()
                scaled_h = scaled.height()
            else:
                scaled_w = int(page.rect.width * self.zoom)
                scaled_h = int(page.rect.height * self.zoom)

            # Karte
            p.fillRect(QRect(x_page, int(y),
                             scaled_w + 2*self.PAGE_PADDING,
                             scaled_h + 2*self.PAGE_PADDING),
                       self.PAGE_BG)
            p.setPen(self.PAGE_BORDER)
            p.drawRect(QRect(x_page, int(y),
                             scaled_w + 2*self.PAGE_PADDING,
                             scaled_h + 2*self.PAGE_PADDING))

            # Pixmap
            # Pixmap anzeigen — PURE SUMATRA-LOGIK:
            scaled = self.cache_scaled.get(index)

            if scaled is not None:
                p.drawPixmap(
                    x_page + self.PAGE_PADDING,
                    y + self.PAGE_PADDING,
                    self.cache_scaled[index]
                )
            else:
                # Kein scaled-Bild verfügbar → grauer Platzhalter.
                # ABER: quick_scale wird beim nächsten paintEvent scaled erzeugen!
                p.fillRect(
                    QRect(
                        x_page + self.PAGE_PADDING,
                        int(y) + self.PAGE_PADDING,
                        scaled_w,
                        scaled_h
                    ),
                    QColor("#d0d0d0")
                )
            # else:
            #     # Placeholder
            #     p.fillRect(
            #         QRect(x_page + self.PAGE_PADDING,
            #               int(y) + self.PAGE_PADDING,
            #               scaled_w, scaled_h),
            #         QColor("#d0d0d0")
            #     )

        # Auswahl
        p.setBrush(QColor(150, 200, 255, 120))
        p.setPen(Qt.NoPen)
        for r in self.sel_label_rects:
            p.drawRect(r)

        p.end()

    # -------------------------------------------------------
    # Mouse
    # -------------------------------------------------------
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.sel_label_rects = []
            self.selected_text = ""
            self.update()

            self.sel_page = self._page_at(e.pos())
            if self.sel_page is None:
                return

            self._selecting = True
            self.sel_start = e.pos()
            self.sel_end = e.pos()

    def mouseMoveEvent(self, e):
        if self._selecting:
            self.sel_end = e.pos()
            self._recompute_selection()
            self.update()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self._selecting:
            self._selecting = False
            self._recompute_selection(final=True)
            self.update()

    # -------------------------------------------------------
    # Selection
    # -------------------------------------------------------
    def _page_at(self, pos):
        for i, (y, h) in enumerate(self.page_positions):
            if y <= pos.y() <= y + h:
                return i
        return None

    def _recompute_selection(self, final=False):
        if self.sel_page is None:
            return

        page = self.doc[self.sel_page]
        y_page, total_h = self.page_positions[self.sel_page]

        pix = self.cache_scaled.get(self.sel_page)
        if pix is None:
            return

        scaled_w = pix.width()
        scaled_h = pix.height()

        pix_sx = scaled_w / page.rect.width
        pix_sy = scaled_h / page.rect.height

        page = self.doc[self.sel_page]
        page_width = int(page.rect.width * self.zoom) + 2 * self.PAGE_PADDING
        x_page = max(0, (self.width() - page_width) // 2)   # exakt wie in paintEvent

        pix_x = x_page + self.PAGE_PADDING
        pix_y = int(y_page) + self.PAGE_PADDING

        # Canvas → Pixmap
        def to_pix(pt):
            return QPoint(pt.x() - pix_x, pt.y() - pix_y)

        p0_pix = to_pix(self.sel_start)
        p1_pix = to_pix(self.sel_end)

        p0 = fitz.Point(p0_pix.x() / pix_sx, p0_pix.y() / pix_sy)
        p1 = fitz.Point(p1_pix.x() / pix_sx, p1_pix.y() / pix_sy)

        # -------------------------------------------------------
        # 1) WORDS + Wasserzeichen filtern
        # -------------------------------------------------------
        raw = page.get_text("words") or []
        words = []
        for w in raw:
            x0,y0,x1,y1,text,block,line,word = w

            if "LÖSUNGEN" in text.upper():
                continue
            if (y1 - y0) > 20:
                continue
            if (x1 - x0) > page.rect.width * 0.6:
                continue

            words.append(w)

        if not words:
            return

        # -------------------------------------------------------
        # 2) VISUELLE Sortierung + Zeilencluster
        # -------------------------------------------------------
        words.sort(key=lambda w: (w[1], w[0]))

        lines = []
        cur = []

        for w in words:
            r = fitz.Rect(w[:4])
            if not cur:
                cur = [w]
                continue

            prev_r = fitz.Rect(cur[-1][:4])

            # gleiche Zeile (vertikale Überlappung)
            if r.y0 < prev_r.y1 and r.y1 > prev_r.y0:
                cur.append(w)
            else:
                lines.append(cur)
                cur = [w]

        if cur:
            lines.append(cur)

        # -------------------------------------------------------
        # 3) Start- und Endzeile
        # -------------------------------------------------------
        def line_of_point(pt):
            for i, line in enumerate(lines):
                lr = fitz.Rect(line[0][:4])
                for w in line[1:]:
                    lr |= fitz.Rect(w[:4])
                if lr.y0 <= pt.y <= lr.y1:
                    return i
            return None

        s = line_of_point(p0)
        e = line_of_point(p1)

        if s is None or e is None:
            return

        if s > e:
            s, e = e, s

        # -------------------------------------------------------
        # 4) PRO-LINE TEXTBREITE: wie Sumatra
        # -------------------------------------------------------
        line_rects = []

        for ln in range(s, e+1):
            line = lines[ln]

            # Breite des Textblocks = rechtester Wortrand
            rightmost = max(w[2] for w in line)

            # dynamische Erweiterung bis rechter Rand des Absatzes
            # aber niemals in Tabellenbereich hinein
            # daher 82% der Seitenbreite als Limit 
            # (für DEIN PDF optimal)
            safe_right = min(rightmost + 15, page.rect.width * 0.82)

            lr = fitz.Rect(line[0][:4])
            for w in line[1:]:
                lr |= fitz.Rect(w[:4])

            lr.x1 = safe_right
            line_rects.append(lr)

        # teilwort:
        line_rects[0].x0 = max(line_rects[0].x0, p0.x)
        # rechter Rand der letzten Zeile darf NIE breiter sein als ihre echte Wortbreite
        last_line_words = lines[e]
        natural_right = max(w[2] for w in last_line_words)   # echter rechter Rand der Textzeile

        # Wenn die Mausposition innerhalb der Textbreite war → Teilwort
        if p1.x < natural_right:
            line_rects[-1].x1 = max(line_rects[-1].x0, p1.x)
        else:
            # Maus rechts außerhalb -> NICHT übernehmen -> natürliche Breite nutzen
            line_rects[-1].x1 = natural_right

        # -------------------------------------------------------
        # 5) PDF→Canvas
        # -------------------------------------------------------
        rects = []
        for r in line_rects:
            cx0 = pix_x + r.x0 * pix_sx
            cy0 = pix_y + r.y0 * pix_sy
            cx1 = pix_x + r.x1 * pix_sx
            cy1 = pix_y + r.y1 * pix_sy
            rects.append(QRect(int(cx0), int(cy0), int(cx1-cx0), int(cy1-cy0)))

        self.sel_label_rects = rects

        # -------------------------------------------------------
        # 6) Copy-Text
        # -------------------------------------------------------

        if final:
            result_lines = []

            # Für jede markierte Zeile (Canvas-Rechteck bekannt!)
            for idx, r_pdf in enumerate(line_rects):
                # PDF-Rect → wir filtern nach PDF-Koordinaten
                line_words = sorted(lines[s + idx], key=lambda w: w[0])

                filtered_words = []
                for w in line_words:
                    wx0, wy0, wx1, wy1, text, block, line, wn = w

                    # Wort liegt (teilweise) innerhalb des markierten PDF-Zeilen-Rechtecks?
                    if wx1 >= r_pdf.x0 and wx0 <= r_pdf.x1:
                        filtered_words.append(text)

                # gesamten Text der Linie erzeugen
                line_text = " ".join(filtered_words)
                line_text = " ".join(line_text.split())   # Mehrfachspaces korrigieren

                result_lines.append(line_text)

            self.selected_text = "\n".join(result_lines)


        self.update()

    # -------------------------------------------------------
    def _merge_rects(self, rects):
        x0 = min(r.x() for r in rects)
        y0 = min(r.y() for r in rects)
        x1 = max(r.x() + r.width() for r in rects)
        y1 = max(r.y() + r.height() for r in rects)
        return QRect(x0, y0, x1-x0, y1-y0)

    # -------------------------------------------------------
    def keyPressEvent(self, e):
        if e.matches(QKeySequence.Copy):
            QApplication.clipboard().setText(self.selected_text)
            return
        super().keyPressEvent(e)

    # -------------------------------------------------------
    def insert_rendered(self, page_index, zoom_int, qimage):
        # raw pixmap speichern
        self.cache_raw[(page_index, zoom_int)] = QPixmap.fromImage(qimage)

        # skaliertes Bild anhand aktuellem Zoom neu erzeugen
        if zoom_int == int(self.zoom * 100):
            page = self.doc[page_index]
            sw = int(page.rect.width * self.zoom)
            sh = int(page.rect.height * self.zoom)

            scaled = self.cache_raw[(page_index, zoom_int)].scaled(
                sw, sh,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.cache_scaled[page_index] = scaled
            self._compute_positions()  
        self.update()


    def set_zoom(self, z):
        self.zoom = z
        # self.cache_raw.clear()
        self.cache_scaled.clear()
        self._compute_positions()
        self.update()


    def quick_scale(self):
        if not self.cache_raw:
            return

        # ❌ scaled NICHT löschen!
        # self.cache_scaled.clear()

        # ✅ Ausgabe-Cache NICHT löschen, sondern nur updaten
        latest_raw_per_page = {}

        # neueste RAW-Version je Seite finden
        for (page_index, zoom_int), raw in self.cache_raw.items():
            if page_index not in latest_raw_per_page:
                latest_raw_per_page[page_index] = (zoom_int, raw)
            elif zoom_int > latest_raw_per_page[page_index][0]:
                latest_raw_per_page[page_index] = (zoom_int, raw)

        # ✅ skaliere neueste RAWs
        for page_index, (_, raw_pixmap) in latest_raw_per_page.items():
            page = self.doc[page_index]

            sw = int(page.rect.width * self.zoom)
            sh = int(page.rect.height * self.zoom)

            scaled = raw_pixmap.scaled(
                sw, sh,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            # ✅ wichtig: aktualisiere NUR diese Seite
            self.cache_scaled[page_index] = scaled

        # ✅ jetzt erst die Positionen neu berechnen
        self._compute_positions()
        self.update()

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
