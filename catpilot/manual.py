"""Panneau « Mode d'emploi » : le manuel intégré (assets/manuel.html), avec recherche,
impression et enregistrement en PDF. L'historique des versions vient d'assets/nouveautes.html."""
import os
import sys

from PySide6.QtCore import QMarginsF, Qt
from PySide6.QtGui import QPageLayout, QPageSize, QTextDocument
from PySide6.QtWidgets import (
    QDockWidget, QFileDialog, QHBoxLayout, QLineEdit, QMessageBox, QPushButton, QTextBrowser, QVBoxLayout,
    QWidget,
)

from . import __version__


def _asset(name):
    base = getattr(sys, "_MEIPASS", os.path.join(os.path.dirname(__file__), ".."))
    try:
        with open(os.path.join(base, "assets", name), encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def manual_html():
    html = _asset("manuel.html") or "<p>Mode d'emploi introuvable.</p>"
    return html.replace("{VERSION}", __version__).replace("{NOUVEAUTES}", _asset("nouveautes.html"))


class ManualDock(QDockWidget):
    def __init__(self, win):
        super().__init__("Mode d'emploi", win)
        self.win = win
        self.setObjectName("manualdock")
        w = QWidget()
        v = QVBoxLayout(w)
        h = QHBoxLayout()
        self.ed_find = QLineEdit()
        self.ed_find.setPlaceholderText("Rechercher dans le mode d'emploi, puis Entrée (suivant)")
        self.ed_find.returnPressed.connect(self.find_next)
        h.addWidget(self.ed_find, 1)
        for label, slot, tip in (("Sommaire", self.go_top, "Revenir au sommaire"),
                                 ("A−", lambda: self.view.zoomOut(1), "Texte plus petit"),
                                 ("A+", lambda: self.view.zoomIn(1), "Texte plus grand"),
                                 ("Imprimer…", self.print_manual, "Imprimer le mode d'emploi"),
                                 ("Enregistrer en PDF…", self.save_pdf, "Enregistrer le mode d'emploi en PDF")):
            b = QPushButton(label)
            b.setToolTip(tip)
            b.clicked.connect(slot)
            h.addWidget(b)
        v.addLayout(h)
        self.view = QTextBrowser()
        self.view.setOpenExternalLinks(True)
        self.view.setOpenLinks(True)
        self.view.document().setDefaultStyleSheet("a { color: #7ab8ff; }")   # liens lisibles sur fond sombre
        self.view.setHtml(manual_html())
        v.addWidget(self.view, 1)
        self.setWidget(w)
        self.setMinimumWidth(520)

    def go_top(self):
        self.view.scrollToAnchor("sommaire")

    def find_next(self):
        txt = self.ed_find.text().strip()
        if not txt:
            return
        if not self.view.find(txt):
            cur = self.view.textCursor()            # fin du texte atteinte : on repart du début
            cur.movePosition(cur.MoveOperation.Start)
            self.view.setTextCursor(cur)
            if not self.view.find(txt):
                self.win.statusBar().showMessage(f"« {txt} » introuvable dans le mode d'emploi", 5000)

    def _document(self):
        """Document propre pour l'impression : texte noir sur blanc, quel que soit le thème de l'écran."""
        doc = QTextDocument()
        doc.setDefaultStyleSheet("body { color: black; background: white; } a { color: #0645ad; }")
        doc.setHtml(manual_html())
        return doc

    def _printer(self):
        from PySide6.QtPrintSupport import QPrinter
        p = QPrinter(QPrinter.HighResolution)
        p.setPageLayout(QPageLayout(QPageSize(QPageSize.A4), QPageLayout.Portrait, QMarginsF(15, 15, 15, 15),
                                    QPageLayout.Millimeter))
        p.setDocName(f"CAT Pilot FT-817 {__version__} - mode d'emploi")
        return p

    def print_manual(self):
        from PySide6.QtPrintSupport import QPrintDialog
        p = self._printer()
        d = QPrintDialog(p, self)
        d.setWindowTitle("Imprimer le mode d'emploi")
        if d.exec():
            self._document().print_(p)

    def save_pdf(self):
        from PySide6.QtPrintSupport import QPrinter
        default = os.path.join(os.path.expanduser("~"), "Documents", f"CAT Pilot FT-817 {__version__} - mode d'emploi.pdf")
        path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le mode d'emploi en PDF", default, "PDF (*.pdf)")
        if not path:
            return
        if not path.lower().endswith(".pdf"):
            path += ".pdf"
        p = self._printer()
        p.setOutputFormat(QPrinter.PdfFormat)
        p.setOutputFileName(path)
        self._document().print_(p)
        QMessageBox.information(self, "Mode d'emploi", f"Mode d'emploi enregistré :\n{path}")
