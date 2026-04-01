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
        self.cache_preview = {}

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

    
        self.page_sizes = [
            (page.rect.width, page.rect.height)
            for page in self.doc
        ]
        self._last_quick_zoom = self.zoom
        

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



            
            # page_key = (index, int(self.zoom * 100))


            # ❗ SAFETY: Wenn Canvas in einem alten Zustand ist → einfach überspringen
            if index >= len(self.page_sizes):
                continue


            page_w_raw, page_h_raw = self.page_sizes[index]
            page_width = int(page_w_raw * self.zoom) + 2 * self.PAGE_PADDING

            x_page = max(0, (self.width() - page_width) // 2) #links zentriert: = 40

            if index in self.cache_scaled:
                scaled = self.cache_scaled[index]
                scaled_w = scaled.width()
                scaled_h = scaled.height()
            else:
                scaled_w = int(page_w_raw * self.zoom)
                scaled_h = int(page_h_raw * self.zoom)


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

            # Sollte scaled fehlen, preview bevorzugen
            if index not in self.cache_scaled and index in self.cache_preview:
                scaled = self.cache_preview[index].scaled(
                    scaled_w, scaled_h,
                    Qt.KeepAspectRatio,
                    Qt.FastTransformation
                )


            if scaled is not None:
                p.drawPixmap(
                    x_page + self.PAGE_PADDING,
                    y + self.PAGE_PADDING,
                    scaled  # ✅ wir nutzen die Variable, nicht self.cache_scaled[index]
                )

            else:
                preview = self.cache_preview.get(index)
                if preview:
                    # Preview hochskalieren, sehr schnell
                    p.drawPixmap(
                        x_page + self.PAGE_PADDING,
                        int(y) + self.PAGE_PADDING,
                        preview.scaled(
                            scaled_w, scaled_h,
                            Qt.KeepAspectRatio,
                            Qt.FastTransformation
                        )
                    )
                else:
                    # allererste Anzeige -> grauer Fallback
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

        # ------------------------------------------------------------
        # 0) Ohne gültige Seite → Abbruch
        # ------------------------------------------------------------
        if self.sel_page is None:
            self.sel_label_rects = []
            self.selected_text = ""
            return

        page_index = self.sel_page
        page = self.doc.load_page(page_index)

        # ------------------------------------------------------------
        # 1) Auswahlrechteck (Widget → PDF Koordinaten)
        # ------------------------------------------------------------
        # Positions-Offset der Seite herausfinden
        page_y, total_h = self.page_positions[page_index]
        page_x = max(0, (self.width() - (page.rect.width * self.zoom + 2*self.PAGE_PADDING)) // 2)

        # Maus-Start/Endpunkt in Widget-Space
        p0 = self.sel_start
        p1 = self.sel_end

        # Normiertes Auswahlrechteck in Widget-Space
        wx0, wy0 = min(p0.x(), p1.x()), min(p0.y(), p1.y())
        wx1, wy1 = max(p0.x(), p1.x()), max(p0.y(), p1.y())

        # In PDF-Space umrechnen
        pdf_x0 = (wx0 - page_x - self.PAGE_PADDING) / self.zoom
        pdf_y0 = (wy0 - page_y - self.PAGE_PADDING) / self.zoom
        pdf_x1 = (wx1 - page_x - self.PAGE_PADDING) / self.zoom
        pdf_y1 = (wy1 - page_y - self.PAGE_PADDING) / self.zoom

        # Auswahl speichern
        sel_x0, sel_y0, sel_x1, sel_y1 = pdf_x0, pdf_y0, pdf_x1, pdf_y1

        # ------------------------------------------------------------
        # 2) PAGE TEXT LADEN
        # ------------------------------------------------------------
        raw = page.get_text("rawdict")
        blocks = raw.get("blocks", [])

        # ------------------------------------------------------------
        # 3) WATERMARK-BLOCK entfernen ("LÖSUNGEN")
        # ------------------------------------------------------------
        filtered = []
        for b in blocks:
            if b.get("type", 0) != 0:
                filtered.append(b)
                continue

            x0, y0, x1, y1 = b.get("bbox", (0,0,0,0))
            bw = x1 - x0
            bh = y1 - y0

            if bw > page.rect.width * 0.40 and bh > page.rect.height * 0.20:
                # Wasserzeichen erkannt → nicht aufnehmen
                continue

            filtered.append(b)

        blocks = filtered

        # ------------------------------------------------------------
        # 4) ALLE ZEICHEN EXTRAHIEREN
        # ------------------------------------------------------------
        chars = []
        for b in blocks:
            if b.get("type", 0) != 0:
                continue
            for line in b.get("lines", []):
                for span in line.get("spans", []):
                    for c in span.get("chars", []):
                        cx0, cy0, cx1, cy1 = c["bbox"]
                        ch = c["c"]
                        chars.append([cx0, cy0, cx1, cy1, ch])

        if not chars:
            self.sel_label_rects = []
            self.selected_text = ""
            return

        chars.sort(key=lambda c: (c[1], c[0]))

        # ------------------------------------------------------------
        # 5) ZEILEN GRUPPIEREN
        # ------------------------------------------------------------
        lines = []
        current = [chars[0]]

        def same_line(a, b):
            return abs(a[1] - b[1]) < 5

        for c in chars[1:]:
            if same_line(current[-1], c):
                current.append(c)
            else:
                lines.append(current)
                current = [c]

        lines.append(current)

        # ------------------------------------------------------------
        # 6) SUMATRA-PDF-STYLE AUSWAHL: rein nach Zeichenreihenfolge
        # ------------------------------------------------------------

        # 1. PDF-Koordinaten der beiden Punkte
        p0 = self.sel_start
        p1 = self.sel_end

        # Umrechnung ins PDF-Koordinatensystem
        pdf_x0 = (p0.x() - page_x - self.PAGE_PADDING) / self.zoom
        pdf_y0 = (p0.y() - page_y - self.PAGE_PADDING) / self.zoom
        pdf_x1 = (p1.x() - page_x - self.PAGE_PADDING) / self.zoom
        pdf_y1 = (p1.y() - page_y - self.PAGE_PADDING) / self.zoom

        # 2. Char-Liste flatten:
        # Wir haben alle chars bereits extrahiert → in der Variablen 'chars'
        # (Liste von [x0,y0,x1,y1,char])
        # UND sie ist bereits sortiert, das passt perfekt.

        # 3. Finde Start- und Endindex
        idx_start = self._char_index_from_pdf_pos(chars, pdf_x0, pdf_y0)
        idx_end   = self._char_index_from_pdf_pos(chars, pdf_x1, pdf_y1)

        if idx_start > idx_end:
            idx_start, idx_end = idx_end, idx_start

        selected = chars[idx_start:idx_end+1]

        # 4. Text erzeugen
        self.selected_text = "".join(c[4] for c in selected)

        # 5. Rechtecke erzeugen (Zeilenbasiert aber nur für Darstellung)
        #    → wir gruppieren die ausgewählten Zeichen nach Linien

        # Linien finden
        line_groups = []
        current = [selected[0]]

        def same_line(a, b):
            return abs(a[1] - b[1]) < 5

        for c in selected[1:]:
            if same_line(current[-1], c):
                current.append(c)
            else:
                line_groups.append(current)
                current = [c]
        line_groups.append(current)

        sel_rects = []

        for group in line_groups:
            gx0 = min(c[0] for c in group)
            gy0 = min(c[1] for c in group)
            gx1 = max(c[2] for c in group)
            gy1 = max(c[3] for c in group)

            wx0 = int(page_x + self.PAGE_PADDING + gx0 * self.zoom)
            wy0 = int(page_y + self.PAGE_PADDING + gy0 * self.zoom)
            wx1 = int(page_x + self.PAGE_PADDING + gx1 * self.zoom)
            wy1 = int(page_y + self.PAGE_PADDING + gy1 * self.zoom)

            sel_rects.append(QRect(wx0, wy0, wx1 - wx0, wy1 - wy0))

        self.sel_label_rects = sel_rects


    # -------------------------------------------------------

    def _char_index_from_pdf_pos(self, chars, x, y):
        """
        Finde den Index des Zeichens, das am besten zum Punkt (x,y) passt.
        """
        best = None
        best_dist = 1e9

        for i, (x0, y0, x1, y1, ch) in enumerate(chars):
            if x0 <= x <= x1 and y0 <= y <= y1:
                return i  # perfekter Treffer

            # sonst Distanz zur Char-Bbox
            cx = (x0 + x1) / 2
            cy = (y0 + y1) / 2
            dist = (cx - x) ** 2 + (cy - y) ** 2
            if dist < best_dist:
                best_dist = dist
                best = i

        return best if best is not None else 0    
    
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

        # --- SAFETY: Seite existiert noch? ---
        if page_index < 0 or page_index >= len(self.page_sizes):
            return

        # --- SAFETY: PDF hat sich geändert? ---
        if page_index >= self.doc.page_count:
            return

        # --- SAFETY: passt Renderzoom noch zum aktuellen Viewerzoom? ---
        if zoom_int != int(self.zoom * 100):
            return


        # raw pixmap speichern
        self.cache_raw[(page_index, zoom_int)] = QPixmap.fromImage(qimage)

        # --- PREVIEW (Low-Res) erstellen ---
        page_w_raw, page_h_raw = self.page_sizes[page_index]
        preview_w = max(50, int(page_w_raw * self.zoom / 4))
        preview_h = max(50, int(page_h_raw * self.zoom / 4))

        self.cache_preview[page_index] = self.cache_raw[(page_index, zoom_int)].scaled(
            preview_w, preview_h,
            Qt.KeepAspectRatio,
            Qt.FastTransformation
        )


        positions_need_update = False
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
            positions_need_update = True

        if positions_need_update:    
            self._compute_positions()  
        self.update()


    def set_zoom(self, z):
        self.zoom = z
        # self.cache_raw.clear()
        self.cache_scaled.clear()
        self._compute_positions()
        self.update()


    def quick_scale(self):
        if abs(self.zoom - self._last_quick_zoom) < 0.01:
            return  # ✅ Kein neues Skalieren nötig

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

        vis = set(self.visible_pages())
        for page_index, (_, raw_pixmap) in latest_raw_per_page.items():
            if page_index not in vis:
                continue  # ✅ Nicht sichtbare Seiten ignorieren

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



    def visible_pages(self):
        scrollarea = self.parent().parent()
        top = scrollarea.verticalScrollBar().value()
        bottom = top + scrollarea.viewport().height()

        visible = []
        for i, (y, h) in enumerate(self.page_positions):
            if y + h >= top - 200 and y <= bottom + 200:
                visible.append(i)
        return visible

