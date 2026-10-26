"""Sauvegarde automatique du carnet de trafic à la fermeture du logiciel.

Si le carnet a été modifié pendant la séance (QSO ajoutés, modifiés, supprimés, importés),
un dossier daté est créé dans Documents/CATPilot-FT817/sauvegardes_carnet/ avec :
- carnet.sqlite  : copie complète de la base (à restaurer telle quelle) ;
- carnet.adi     : tout le carnet en ADIF (lisible par tout logiciel de carnet) ;
- modifications.adi et modifications.txt : ce qui a changé pendant la séance.
Les 30 dernières sauvegardes sont gardées.
"""
import datetime
import os
import shutil
import sqlite3

from . import __version__, adif
from .logbook import data_dir

KEEP = 30


def backup_root():
    d = os.path.join(data_dir(), "sauvegardes_carnet")
    os.makedirs(d, exist_ok=True)
    return d


def list_backups():
    root = backup_root()
    return sorted((d for d in os.listdir(root) if os.path.isfile(os.path.join(root, d, "carnet.sqlite"))),
                  reverse=True)


def _fmt(r):
    d, t = r.get("qso_date") or "", (r.get("time_on") or "")
    return (f"{d[6:8]}/{d[4:6]}/{d[:4]} {t[:2]}:{t[2:4]}  {r.get('call', ''):<12} {r.get('band') or '':<5} "
            f"{r.get('submode') or r.get('mode') or '':<6} {r.get('station_callsign') or ''}").rstrip()


def save(log, reason="fermeture du logiciel"):
    """Crée une sauvegarde datée du carnet. Renvoie le dossier créé."""
    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    folder, n = os.path.join(backup_root(), stamp), 1
    while os.path.exists(folder):                     # jamais deux sauvegardes dans le même dossier
        n += 1
        folder = os.path.join(backup_root(), f"{stamp}_{n}")
    os.makedirs(folder)
    with log.lock:
        dst = sqlite3.connect(os.path.join(folder, "carnet.sqlite"))
        log.db.backup(dst)
        dst.close()
    rows = log.query()
    with open(os.path.join(folder, "carnet.adi"), "w", encoding="utf-8") as f:
        f.write(adif.write(log.export_records(rows), "CAT Pilot FT-817", __version__))
    ses = log.session
    by_id = {r["id"]: r for r in rows}
    added = [by_id[i] for i in ses["added"] if i in by_id]
    updated = [by_id[i] for i in sorted(ses["updated"]) if i in by_id and i not in ses["added"]]
    with open(os.path.join(folder, "modifications.adi"), "w", encoding="utf-8") as f:
        f.write(adif.write(log.export_records(added + updated), "CAT Pilot FT-817", __version__))
    lines = [f"Sauvegarde du carnet — {datetime.datetime.now():%d/%m/%Y %H:%M} ({reason})",
             f"CAT Pilot FT-817 {__version__} — {len(rows)} QSO dans le carnet", ""]
    for title, recs in ((f"QSO ajoutés ({len(added)})", added), (f"QSO modifiés ({len(updated)})", updated),
                        (f"QSO supprimés ({len(ses['deleted'])})", ses["deleted"])):
        lines.append(title)
        lines += ["  " + _fmt(r) for r in recs] or ["  aucun"]
        lines.append("")
    with open(os.path.join(folder, "modifications.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    for old in list_backups()[KEEP:]:
        shutil.rmtree(os.path.join(backup_root(), old), ignore_errors=True)
    return folder


def restore(log, name):
    """Remplace le carnet par la sauvegarde « name » (le carnet actuel est d'abord sauvegardé)."""
    src = os.path.join(backup_root(), name, "carnet.sqlite")
    if not os.path.isfile(src):
        raise FileNotFoundError(src)
    import tempfile
    fd, copy = tempfile.mkstemp(suffix=".sqlite")
    os.close(fd)
    shutil.copyfile(src, copy)              # la sauvegarde choisie est mise à l'abri d'abord
    try:
        save(log, f"avant restauration de la sauvegarde {name}")
        with log.lock:
            tmp = sqlite3.connect(copy)
            tmp.backup(log.db)              # copie en place, dans la base ouverte
            tmp.close()
    finally:
        os.remove(copy)
    log.session = {"added": [], "updated": set(), "deleted": []}
    log.changed.emit()
