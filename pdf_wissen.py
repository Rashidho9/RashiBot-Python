"""Liest PDFs und findet passende Textstellen zu einer Frage."""
import re

from pypdf import PdfReader

STUECK_GROESSE = 800  # Zeichen pro Stück


class PdfWissen:
    def __init__(self):
        self.stuecke = []      # Liste von (dateiname, text)
        self.dateien = []

    def laden(self, pfad):
        """PDF lesen und in Stücke zerteilen. Gibt die Seitenzahl zurück."""
        leser = PdfReader(pfad)
        text = ""
        for seite in leser.pages:
            text += (seite.extract_text() or "") + "\n"

        name = pfad.replace("\\", "/").split("/")[-1]
        for i in range(0, len(text), STUECK_GROESSE):
            stueck = text[i:i + STUECK_GROESSE].strip()
            if stueck:
                self.stuecke.append((name, stueck))
        self.dateien.append(name)
        return len(leser.pages)

    @staticmethod
    def _woerter(text):
        """Text in kleine Wörter (ab 4 Buchstaben) zerlegen."""
        return set(re.findall(r"\w{4,}", text.lower()))

    def suchen(self, frage, anzahl=3):
        """Die Stücke finden, die am besten zur Frage passen."""
        frage_woerter = self._woerter(frage)
        bewertet = []
        for name, stueck in self.stuecke:
            treffer = len(frage_woerter & self._woerter(stueck))  # & = gemeinsame Wörter
            if treffer > 0:
                bewertet.append((treffer, name, stueck))
        bewertet.sort(reverse=True)  # beste zuerst
        return bewertet[:anzahl]

    def leeren(self):
        self.stuecke = []
        self.dateien = []