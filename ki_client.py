"""Kommuniziert mit Ollama."""
import requests

from config import MODELL, OLLAMA_URL


class KiClient:
    def frage_stellen(self, verlauf):
        """Schickt den Verlauf an Ollama und gibt die Antwort zurück."""
        antwort = requests.post(
            OLLAMA_URL,
            json={"model": MODELL, "messages": verlauf, "stream": False},
            timeout=120,
        )
        antwort.raise_for_status()
        return antwort.json()["message"]["content"]