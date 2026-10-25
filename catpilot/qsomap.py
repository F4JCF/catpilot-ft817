"""Mini-carte du QSO en cours : ma station, le correspondant, le trajet (grand cercle),
les départements français et celui du correspondant en surbrillance."""
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainterPath, QPen, QPolygonF

from . import departements
from .worldmap import WorldMap


class QsoMap(WorldMap):
    min_span = (0.4, 0.25)
    hint = "Molette : zoom · double-clic : recadrer"

    def __init__(self):
        super().__init__()
        self.greyline = False
        self.setMinimumSize(300, 190)
        self.me = self.contact = None
        self.dept = ""
        self.caption = ""
        self._dep_paths = None
        self._dep_key = None
        self.show_region(46.5, 2.5, 10)

    def set_qso(self, me, my_label, contact, contact_label, dept="", caption=""):
        """me / contact : (lat, lon) ou None."""
        self.me, self.contact, self.dept, self.caption = me, contact, dept, caption
        self.station = me
        pts = []
        if me:
            pts.append({"lat": me[0], "lon": me[1], "label": my_label, "color": "#e8412c", "size": 4})
        if contact:
            pts.append({"lat": contact[0], "lon": contact[1], "label": contact_label, "color": "#ffb000",
                        "size": 5, "line": bool(me), "tip": contact_label})
        self.layers = {"qso": pts}
        self.recenter()

    def recenter(self):
        pts = [p for p in (self.me, self.contact) if p]
        if not pts:
            self.update()
            return
        lats, lons = [p[0] for p in pts], [p[1] for p in pts]
        if len(pts) == 2 and abs(lons[0] - lons[1]) > 180:          # trajet par l'antiméridien
            self.show_world()
            return
        h = max(max(lats) - min(lats), 1.2) * 1.9
        w = max(max(lons) - min(lons), 1.6) * 1.35
        cy, cx = (max(lats) + min(lats)) / 2, (max(lons) + min(lons)) / 2
        self.view = [cx - w / 2, cy - h / 2, w, h]
        self._clamp()
        self.update()

    def mouseDoubleClickEvent(self, _e):
        self.recenter()

    # --- départements --------------------------------------------------------------------
    def _paint_extra(self, p):
        lon0, lat0, w, h = self._fit()
        if w > 30 or lon0 > 10 or lon0 + w < -6 or lat0 > 52 or lat0 + h < 41:
            return
        key = (tuple(round(v, 3) for v in (lon0, lat0, w, h)), self.width(), self.height())
        if self._dep_key != key:
            paths = {}
            for d in departements.data():
                path = QPainterPath()
                for r in d["rings"]:
                    poly = QPolygonF([QPointF(*self.to_xy(r[i + 1], r[i])) for i in range(0, len(r) - 1, 2)])
                    path.addPolygon(poly)
                    path.closeSubpath()
                paths[d["code"]] = path
            self._dep_paths, self._dep_key = paths, key
        if self.dept in self._dep_paths:
            p.setPen(Qt.NoPen)
            p.setBrush(QColor(255, 176, 0, 55))
            p.drawPath(self._dep_paths[self.dept])
        p.setBrush(Qt.NoBrush)
        p.setPen(QPen(QColor(255, 255, 255, 55), 0.6))
        for path in self._dep_paths.values():
            p.drawPath(path)
        if self.dept in self._dep_paths:
            p.setPen(QPen(QColor(255, 176, 0, 200), 1.2))
            p.drawPath(self._dep_paths[self.dept])

    def _paint_top(self, p):
        if not self.caption:
            return
        f = QFont()
        f.setPointSize(9)
        f.setBold(True)
        p.setFont(f)
        r = QRectF(6, 4, self.width() - 12, 18)
        p.setPen(QColor(0, 0, 0, 200))
        p.drawText(r.translated(1, 1), Qt.AlignLeft, self.caption)
        p.setPen(QColor("#ffd27a"))
        p.drawText(r, Qt.AlignLeft, self.caption)
