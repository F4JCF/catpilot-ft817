"""Département français d'un correspondant.

Ordre de recherche :
1. le code postal donné par QRZ.com / HamQTH (le plus sûr) ;
2. le préfixe pour les départements d'outre-mer (FG, FM, FY, FR, FH) ;
3. le locator (6 caractères au moins) : point dans le contour des départements
   métropolitains (IGN Admin Express, Licence ouverte, via france-geojson).

Le code est rangé dans le champ ADIF STATE (subdivision administrative : « 38 », « 2A »…).
"""
import json
import math
import os
import re
import sys

DOM = {"971": "Guadeloupe", "972": "Martinique", "973": "Guyane", "974": "La Réunion", "976": "Mayotte"}
DOM_PREFIX = {"FG": "971", "FM": "972", "FY": "973", "FR": "974", "FH": "976"}

_DATA = None


def data():
    """[{code, nom, rings, bbox}] des départements métropolitains."""
    global _DATA
    if _DATA is None:
        base = getattr(sys, "_MEIPASS", os.path.join(os.path.dirname(__file__), ".."))
        try:
            with open(os.path.join(base, "assets", "departements.json"), encoding="utf-8") as f:
                deps = json.load(f)["dep"]
        except (OSError, ValueError, KeyError):
            deps = []
        for d in deps:
            xs = [x for r in d["rings"] for x in r[0::2]]
            ys = [y for r in d["rings"] for y in r[1::2]]
            d["bbox"] = (min(xs), min(ys), max(xs), max(ys)) if xs else (0, 0, 0, 0)
        _DATA = deps
    return _DATA


def names():
    out = {d["code"]: d["nom"] for d in data()}
    out.update(DOM)
    return out


def label(code):
    """« 38 — Isère » (ou le code seul s'il est inconnu)."""
    code = (code or "").strip().upper()
    nom = names().get(code)
    return f"{code} — {nom}" if nom else code


def normalize(text):
    """Texte saisi (« 38 », « 38 — Isère », « isère », « 2a ») -> code, ou chaîne vide."""
    t = (text or "").strip()
    if not t:
        return ""
    m = re.match(r"^\s*(97[1-6]|2[AaBb]|\d{1,2})\b", t)
    if m:
        c = m.group(1).upper()
        return c.zfill(2) if c.isdigit() and len(c) < 3 else c
    low = _plain(t)
    for code, nom in names().items():
        if _plain(nom) == low:
            return code
    return ""


def _plain(s):
    import unicodedata
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn").replace("-", " ").strip()


def from_zip(zipcode):
    """Code postal français -> département."""
    z = re.sub(r"\D", "", zipcode or "")
    if len(z) != 5:
        return ""
    if z.startswith("97"):
        return z[:3] if z[:3] in DOM else ""
    if z.startswith("20"):                  # Corse : 200xx-201xx = 2A, 202xx-206xx = 2B
        return "2A" if int(z[:3]) < 202 else "2B"
    return z[:2] if z[:2] != "00" else ""


def _inside(lon, lat, ring):
    inside = False
    n = len(ring) // 2
    j = n - 1
    for i in range(n):
        xi, yi, xj, yj = ring[2 * i], ring[2 * i + 1], ring[2 * j], ring[2 * j + 1]
        if (yi > lat) != (yj > lat) and lon < (xj - xi) * (lat - yi) / ((yj - yi) or 1e-12) + xi:
            inside = not inside
        j = i
    return inside


def from_position(lat, lon, near_km=12.0):
    """Département contenant le point ; à défaut (locator en bord de mer), le plus proche à near_km près."""
    for d in data():
        x0, y0, x1, y1 = d["bbox"]
        if x0 <= lon <= x1 and y0 <= lat <= y1 and any(_inside(lon, lat, r) for r in d["rings"]):
            return d["code"]
    best, bd = "", near_km
    k = math.cos(math.radians(lat))
    for d in data():
        x0, y0, x1, y1 = d["bbox"]
        if not (x0 - 0.3 <= lon <= x1 + 0.3 and y0 - 0.2 <= lat <= y1 + 0.2):
            continue
        for r in d["rings"]:
            for i in range(0, len(r), 2):
                km = math.hypot((r[i] - lon) * k, r[i + 1] - lat) * 111.2
                if km < bd:
                    best, bd = d["code"], km
    return best


def is_french(call, country=""):
    c = (country or "").lower()
    if "france" in c or "corse" in c:
        return True
    base = max((call or "").upper().split("/"), key=len, default="")
    return bool(re.match(r"^(F|TM|TK|TO|TP|TV|TW|TX|TQ|HW|HX|HY)\d", base))


def resolve(call, country="", zipcode="", grid=""):
    """Département du correspondant, ou chaîne vide si on ne peut pas le savoir."""
    call = (call or "").upper()
    for part in call.split("/"):
        if part[:2] in DOM_PREFIX and len(part) <= 3:       # FG/F4JCF, FR/F4JCF…
            return DOM_PREFIX[part[:2]]
    base = max(call.split("/"), key=len, default="")
    if base[:2] in DOM_PREFIX and re.match(r"^F[GMYRH]\d", base):
        return DOM_PREFIX[base[:2]]
    french = is_french(call, country)
    if french:
        code = from_zip(zipcode)
        if code:
            return code
    if grid and len(grid.strip()) >= 6:
        from .geo import from_locator
        try:
            g = grid.strip()
            lat, lon = from_locator(g[:8] if len(g) >= 8 else g[:6])
        except ValueError:
            return ""
        code = from_position(lat, lon, near_km=12.0 if french else 0.0)
        return code
    return ""
