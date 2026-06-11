from PyQt5.QtWidgets import QWidget, QApplication, QDialog, QPlainTextEdit, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPixmap, QKeySequence, QImage
from PyQt5.QtCore import QRect, Qt, QPoint
import fitz
from standard_dialog_windows import warning_window

class SourceCodeWindow(QDialog):
    def __init__(self, title, text="", parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"LaTeX Quellcode - {title}")
        self.resize(600, 400)

        self.setWindowFlags(
            self.windowFlags()
            & ~Qt.WindowContextHelpButtonHint
        )
        layout = QVBoxLayout(self)
        self.editor = QPlainTextEdit()
        self.editor.setPlainText(text)
        layout.addWidget(self.editor)

class PdfCanvas(QWidget):
    BACKGROUND_COLOR = QColor("#e5e5e5")
    PAGE_BORDER = QColor("#c8c8c8")
    PAGE_BG = QColor("#ffffff")
    PAGE_MARGIN = 20
    PAGE_PADDING = 12

    def __init__(self, doc, ui_dialog=None, tindb_data = None):
        super().__init__()
        self.ui_dialog = ui_dialog
        self.tindb_data = tindb_data
        self.doc = doc
        self.zoom = 1.5

        # ✅ Original (vom Worker) + skaliert (für Anzeige/Auswahl)
        self.cache_raw = {}
        self.cache_scaled = {}
        self.cache_preview = {}
        self.search_highlights = []
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
            page = self.doc[i]
            h = int(page.rect.height * self.zoom) + 2 * self.PAGE_PADDING
            self.page_positions.append((y, h))
            y += h + self.PAGE_MARGIN

        self.setMinimumHeight(y)


        # Mindestbreite anhand der größten Seite berechnen
        max_width = 0
        for page in self.doc:
            w = int(page.rect.width * self.zoom) + 2 * self.PAGE_PADDING
            max_width = max(max_width, w)

        self.setMinimumWidth(max_width + self.PAGE_MARGIN * 2)

    # -------------------------------------------------------
    # Rendering
    # -------------------------------------------------------
    def paintEvent(self, ev):
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.BACKGROUND_COLOR)

        scroll = self.parent().parent()
        view_top = scroll.verticalScrollBar().value()
        view_bottom = view_top + scroll.viewport().height()

        for index, (y, total_h) in enumerate(self.page_positions):

            # --- Sichtbarkeit check ---
            if y + total_h < view_top - 50:
                continue
            if y > view_bottom + 50:
                break

            page = self.doc[index]
            w = int(page.rect.width * self.zoom)
            h = int(page.rect.height * self.zoom)

            x_page = max(0, (self.width() - (w + 2*self.PAGE_PADDING)) // 2)

            # Hintergrund
            # painter.fillRect(
            #     QRect(x_page, y, w + 2*self.PAGE_PADDING, h + 2*self.PAGE_PADDING),
            #     self.PAGE_BG
            # )
            # painter.setPen(self.PAGE_BORDER)
            # painter.drawRect(
            #     QRect(x_page, y, w + 2*self.PAGE_PADDING, h + 2*self.PAGE_PADDING)
            # )

            # Seite rendern
            mat = fitz.Matrix(self.zoom, self.zoom)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)

            painter.drawImage(
                QPoint(x_page + self.PAGE_PADDING, y + self.PAGE_PADDING),
                img
            )

            # ✅ --- TEXT-AUSWAHL ---
            painter.setBrush(QColor(150, 200, 255, 120))
            painter.setPen(Qt.NoPen)
            for rect in self.sel_label_rects:
                painter.drawRect(rect)

            # ✅ --- SUCHTREFFER (nur GENAU auf dieser Seite) ---
            painter.setBrush(QColor(255, 240, 100, 160))
            painter.setPen(Qt.NoPen)

            for (pi, r) in self.search_highlights:
                if pi != index:
                    continue  # Treffer gehört zu einer anderen Seite

                # PDF → Widget-Koordinaten
                wx0 = int(x_page + self.PAGE_PADDING + r.x0 * self.zoom)
                wy0 = int(y       + self.PAGE_PADDING + r.y0 * self.zoom)
                wx1 = int(x_page + self.PAGE_PADDING + r.x1 * self.zoom)
                wy1 = int(y       + self.PAGE_PADDING + r.y1 * self.zoom)

                painter.drawRect(wx0, wy0, wx1 - wx0, wy1 - wy0)

        painter.end()
    # -------------------------------------------------------
    # Mouse
    # -------------------------------------------------------
    def mousePressEvent(self, e):
        # STRG + Rechts → Quellcodefenster
        if e.button() == Qt.RightButton and (e.modifiers() & Qt.ControlModifier):
            title = self._find_task_by_click(e.pos())

            if not title:
                warning_window("Der Quellcode konnte nicht gefunden werden.")
                return
            
            latex = self._find_latex_for_task(title)
            dlg = SourceCodeWindow(title, latex or f"Kein Quellcode gefunden für: {title}", parent=self)
            dlg.exec_()
            return

        if e.button() == Qt.LeftButton:
            # Start merken, aber NICHT selektieren
            self._selecting = True
            self.sel_page  = self._page_at(e.pos())
            self.sel_start = e.pos()
            self.sel_end   = e.pos()
            self.setCursor(Qt.IBeamCursor)

        super().mousePressEvent(e)



    def mouseMoveEvent(self, e):
        if self._selecting:

            self.sel_end = e.pos()

            # DRAG-SCHWELLE
            if (self.sel_start - self.sel_end).manhattanLength() < 6:
                self.sel_label_rects = []
                self.update()
                super().mouseMoveEvent(e)
                return

            # ECHTE Markierung
            self._recompute_selection(final=False)
            self.update()

        super().mouseMoveEvent(e)


    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self._selecting:
            self._selecting = False
            self.setCursor(Qt.IBeamCursor)

            # Klick → alles löschen
            if (self.sel_start - self.sel_end).manhattanLength() < 6:
                self.sel_label_rects = []
                self.selected_text = ""
                self.update()
                super().mouseReleaseEvent(e)
                return

            # Drag → Auswahl finalisieren
            self._recompute_selection(final=True)
            self.update()

        super().mouseReleaseEvent(e)

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
        page_y, total_h = self.page_positions[page_index]
        page_x = max(0, (self.width() - (page.rect.width * self.zoom + 2*self.PAGE_PADDING)) // 2)

        p0 = self.sel_start
        p1 = self.sel_end

        wx0, wy0 = min(p0.x(), p1.x()), min(p0.y(), p1.y())
        wx1, wy1 = max(p0.x(), p1.x()), max(p0.y(), p1.y())

        pdf_x0 = (wx0 - page_x - self.PAGE_PADDING) / self.zoom
        pdf_y0 = (wy0 - page_y - self.PAGE_PADDING) / self.zoom
        pdf_x1 = (wx1 - page_x - self.PAGE_PADDING) / self.zoom
        pdf_y1 = (wy1 - page_y - self.PAGE_PADDING) / self.zoom

        sel_x0, sel_y0, sel_x1, sel_y1 = pdf_x0, pdf_y0, pdf_x1, pdf_y1

        # ------------------------------------------------------------
        # 2) PAGE TEXT LADEN
        # ------------------------------------------------------------

        try:
            raw = page.get_text("rawdict")
        except Exception as e:
            print("MuPDF Fehler:", e)
            self.sel_label_rects = []
            self.selected_text = ""
            return

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

        # ------------------------------------------------------------
        # NEU ✅: Rechtsstehenden Rand-Text herausfiltern
        # ------------------------------------------------------------

        if chars:
            # X-Koordinaten analysieren
            xs = [c[0] for c in chars]   # linke Seite
            max_x_main = sorted(xs)[int(len(xs) * 0.97)]  
            # → 97%-Quantil: trennt sauber Haupttext von rechten Randinfos

            # Filter anwenden: nur Chars innerhalb des Haupttextblocks behalten
            chars = [c for c in chars if c[0] <= max_x_main + 2]  # kleine Toleranz


        if not chars:
            self.sel_label_rects = []
            self.selected_text = ""
            return


        # ------------------------------------------------------------
        # NEU ✅: Große vertikale Lücke erkennen (z.B. beim Überschreiten der Trennlinie)
        # ------------------------------------------------------------
        # Text-Y-Positionen (Zeilenhöhe)
        ys = [c[1] for c in chars]
        ys_sorted = sorted(ys)

        # Typische Zeilenabstände sind klein (< 50 px), der Strich erzeugt Lücken von > 100–200 px
        vertical_gaps = [
            ys_sorted[i+1] - ys_sorted[i]
            for i in range(len(ys_sorted)-1)
        ]

        # größte Lücke suchen
        if vertical_gaps:
            max_gap = max(vertical_gaps)
            if max_gap > 120:  # 120 px ist ein sehr guter Trenner für deine PDFs
                gap_index = vertical_gaps.index(max_gap)
                cutoff_y = ys_sorted[gap_index+1]

                # ✅ ALLES unterhalb der Trennlinie rausfiltern
                chars = [c for c in chars if c[1] < cutoff_y + 2]


        if not chars:
            self.sel_label_rects = []
            self.selected_text = ""
            return    
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
        # 6) SUMATRA-PDF-STYLE AUSWAHL
        # ------------------------------------------------------------
        pdf_x0 = (p0.x() - page_x - self.PAGE_PADDING) / self.zoom
        pdf_y0 = (p0.y() - page_y - self.PAGE_PADDING) / self.zoom
        pdf_x1 = (p1.x() - page_x - self.PAGE_PADDING) / self.zoom
        pdf_y1 = (p1.y() - page_y - self.PAGE_PADDING) / self.zoom

        idx_start = self._char_index_from_pdf_pos(chars, pdf_x0, pdf_y0)
        idx_end   = self._char_index_from_pdf_pos(chars, pdf_x1, pdf_y1)

        if idx_start > idx_end:
            idx_start, idx_end = idx_end, idx_start

        selected = chars[idx_start:idx_end+1]
        
        if not selected:
            self.sel_label_rects = []
            self.selected_text = ""
            return



        # TEXT
        self.selected_text = "".join(c[4] for c in selected)

        # ------------------------------------------------------------
        # 7) Rechtecke erzeugen (für Darstellung)
        # ------------------------------------------------------------
        line_groups = []




        current = [selected[0]]
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

        # print("INSERT", page_index, "scaled exists?", page_index in self.cache_scaled)
        # print("raw exists?", (page_index, zoom_int) in self.cache_raw)

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

        # ✅ RAW‑CACHE LIMITIEREN — verhindert Memory Overflow
        if len(self.cache_raw) > 40:                # 40 Einträge genügt völlig
            keys = list(self.cache_raw.keys())
            keys.sort(key=lambda x: x[0])           # sortiere nach page_index
            for old_key in keys[:-20]:              # behalte nur die letzten 20
                del self.cache_raw[old_key]

        # --- PREVIEW (Low-Res) erstellen ---
        page_w_raw, page_h_raw = self.page_sizes[page_index]
        preview_w = max(50, int(page_w_raw * self.zoom / 4))
        preview_h = max(50, int(page_h_raw * self.zoom / 4))

        # ✅ RAW speichern
        self.cache_raw[(page_index, zoom_int)] = QPixmap.fromImage(qimage)

        # ✅ PREVIEW sicher erstellen – ohne KeyError
        raw_pm = self.cache_raw.get((page_index, zoom_int))
        if raw_pm:
            preview = raw_pm.scaled(
                preview_w, preview_h,
                Qt.KeepAspectRatio,
                Qt.FastTransformation
            )
        else:
            # ✅ RAW fehlt (durch Cache-Limit oder Race) → fallback
            preview = QPixmap.fromImage(qimage).scaled(
                preview_w, preview_h,
                Qt.KeepAspectRatio,
                Qt.FastTransformation
            )

        self.cache_preview[page_index] = preview


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


            # ✅ SCALED‑CACHE LIMITIEREN
            if len(self.cache_scaled) > 40:
                keys = sorted(self.cache_scaled.keys())
                for old_page in keys[:-20]:             # nur 20 Seiten behalten
                    del self.cache_scaled[old_page]

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
        pass




    def visible_pages(self):
        scrollarea = self.parent().parent()
        top = scrollarea.verticalScrollBar().value()
        bottom = top + scrollarea.viewport().height()

        visible = []
        for i, (y, h) in enumerate(self.page_positions):
            if y + h >= top - 200 and y <= bottom + 200:
                visible.append(i)
        return visible


    def _get_task_title_for_current_page(self):
        """
        Ermittelt die Aufgabe, die zur aktuellen Seite am besten passt.
        Nimmt NICHT die markierte Aufgabe, sondern berechnet es wie deine Auto-Auswahl.
        """
        # Ui-Dialog suchen
        ui = None
        p = self
        while p is not None:
            if hasattr(p, "task_positions"):
                ui = p
                break
            p = p.parent()
        if ui is None:
            return None

        scrollarea = self.parent().parent()
        viewer = scrollarea.parent()
        page = viewer.currentPage()  # 1-based

        # alle Aufgaben der aktuellen Seite
        tasks = [t for t in ui.task_positions if t["page"] == page]
        if not tasks:
            return None

        # beste Aufgabe = kleinster ratio-Wert
        best = min(tasks, key=lambda t: (t["ratio"] if t["ratio"] is not None else 1.0))

        item = ui.list.item(best["row"])
        if not item:
            return None

        return ui._extract_task_number(item.text())

    def _find_task_by_click(self, pos):
        ui = self.ui_dialog
        if ui is None:
            return None

        scroll = self.parent().parent()
        viewer = scroll.parent()

        page_num = viewer.currentPage()   # 1-based
        page_index = page_num - 1

        if page_index < 0 or page_index >= len(self.page_positions):
            return None

        page_y, page_h = self.page_positions[page_index]

        # Klick -> relative Position in der Seite
        click_ratio = (pos.y() - page_y) / float(page_h)
        click_ratio = max(0.0, min(1.0, click_ratio))

        # Alle Aufgaben dieser Seite
        tasks = [t for t in ui.task_positions if t["page"] == page_num]
        if not tasks:
            return None

        # Beste Aufgabe = ratio <= click_ratio UND maximal
        best = None
        best_r = -1
        for t in tasks:
            r = t["ratio"]
            if r is not None and r <= click_ratio and r > best_r:
                best = t
                best_r = r

        if best is None:
            # Nimm erste Aufgabe auf der Seite
            best = min(tasks, key=lambda t: t["ratio"] or 0)

        item = ui.list.item(best["row"])
        if not item:
            return None

        return ui._extract_task_number(item.text())
    

    def _find_latex_for_task(self, task_name):
        """
        Sucht in der TiNDB-Datenliste nach name == task_name
        und gibt den LaTeX-Content zurück.
        """
        if not self.tindb_data:
            return None

        # exakte Übereinstimmung (z.B. "WS 3.3 - 2")
        for entry in self.tindb_data:
            if entry.get("name") == task_name:
                return entry.get("content")

        # Falls Varianten wie  "WS 3.3 - 2[1]" existieren
        base = task_name.split("[")[0]
        for entry in self.tindb_data:
            if entry.get("name", "").startswith(base):
                return entry.get("content")
        
        return None
    

    def clear_selection(self):
        self._selecting = False
        self.sel_page = None
        self.sel_start = None
        self.sel_end = None
        self.sel_label_rects = []
        self.selected_text = ""
        self.update()


    def apply_search_highlight(self, page_index, rect):
        self.search_highlights = [(page_index, rect)]
        self.update()