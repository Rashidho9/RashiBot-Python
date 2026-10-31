"""Kommuniziert mit Ollama."""
import json

import requests

from config import MODELL, OLLAMA_URL


class KiClient:
    def frage_stellen(self, verlauf):
        """Schickt den Verlauf an Ollama und gibt die ganze Antwort zurück."""
        antwort = requests.post(
            OLLAMA_URL,
            json={"model": MODELL, "messages": verlauf, "stream": False},
            timeout=120,
        )
        antwort.raise_for_status()
        return antwort.json()["message"]["content"]

    def frage_streamen(self, verlauf):
        """Schickt den Verlauf und gibt die Antwort Stück für Stück aus."""
        antwort = requests.post(
            OLLAMA_URL,
            json={"model": MODELL, "messages": verlauf, "stream": True},
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