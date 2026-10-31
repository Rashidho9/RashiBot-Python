"""Speichert und lädt den Gesprächsverlauf."""
import json
import os

from config import CHARAKTER, DATEI


class Gedaechtnis:
    def __init__(self):
        self.verlauf = self._laden()

    def _laden(self):
        if os.path.exists(DATEI):
            with open(DATEI, "r", encoding="utf-8") as f:
                return json.load(f)
        return [{"role": "system", "content": CHARAKTER}]

    def speichern(self):
        with open(DATEI, "w", encoding="utf-8") as f:
            json.dump(self.verlauf, f, ensure_ascii=False, indent=2)

    def hinzufuegen(self, rolle, text):
        self.verlauf.append({"role": rolle, "content": text})

    def letzte_entfernen(self):
        self.verlauf.pop()

    def leeren(self):
        self.verlauf = [{"role": "system", "content": CHARAKTER}]
        self.speichern()

    def anzahl(self):
        return len(self.verlauf) - 1