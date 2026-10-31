"""Kommuniziert mit Ollama."""
import json

import requests

from config import MODELL, OLLAMA_URL

class KiClient:
    def __init__(self):
        """Konstruktor: aktuelles Modell im Objekt merken."""
        self.modell = MODELL

    def modelle_auflisten(self):
        """Fragt Ollama nach allen installierten Modellen."""
        antwort = requests.get("http://localhost:11434/api/tags", timeout=10)
        antwort.raise_for_status()
        return [m["name"] for m in antwort.json()["models"]]

    def frage_stellen(self, verlauf):
        """Schickt den Verlauf und gibt die ganze Antwort zurück."""
        antwort = requests.post(
            OLLAMA_URL,
            json={"model": self.modell, "messages": verlauf, "stream": False},
            timeout=120,
        )
        antwort.raise_for_status()
        return antwort.json()["message"]["content"]

    def frage_streamen(self, verlauf):
        """Schickt den Verlauf und gibt die Antwort Stück für Stück aus."""
        antwort = requests.post(
            OLLAMA_URL,
            json={"model": self.modell, "messages": verlauf, "stream": True},
            stream=True,
            timeout=120,
        )
        antwort.raise_for_status()

        ganzer_text = ""
        for zeile in antwort.iter_lines():
            if not zeile:
                continue
            stueck = json.loads(zeile)
            wort = stueck["message"]["content"]
            print(wort, end="", flush=True)
            ganzer_text += wort
            if stueck.get("done"):
                break
        print()
        return ganzer_text