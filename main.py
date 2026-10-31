"""Startpunkt von RashiBot."""
import requests

from gedaechtnis import Gedaechtnis
from ki_client import KiClient


def hilfe_anzeigen():
    print("📋 Befehle:")
    print("  /hilfe   - diese Hilfe anzeigen")
    print("  /neu     - Gedächtnis löschen")
    print("  /verlauf - Anzahl gespeicherter Nachrichten")
    print("  exit     - RashiBot beenden")


def main():
    gedaechtnis = Gedaechtnis()  # Objekt erzeugen (wie new in Java)
    ki = KiClient()
    print("RashiBot ist bereit! Tippe /hilfe für alle Befehle.")

    while True:
        frage = input("Du: ").strip()

        if frage == "":
            continue
        if frage.lower() == "exit":
            print("Bot: Tschüss Rashid! 👋")
            break
        if frage.lower() == "/hilfe":
            hilfe_anzeigen()
            continue
        if frage.lower() == "/neu":
            gedaechtnis.leeren()
            print("Bot: 🧹 Gedächtnis gelöscht.")
            continue
        if frage.lower() == "/verlauf":
            print(f"Bot: 💬 {gedaechtnis.anzahl()} Nachrichten gespeichert.")
            continue
        if frage.startswith("/"):
            print("Bot: ❓ Unbekannter Befehl. Tippe /hilfe.")
            continue

        gedaechtnis.hinzufuegen("user", frage)
        try:
            print("Bot: ", end="", flush=True)
            text = ki.frage_streamen(gedaechtnis.verlauf)
        except requests.exceptions.ConnectionError:
            print("Bot: ⚠️ Ollama läuft nicht.")
            gedaechtnis.letzte_entfernen()
            continue
        except requests.exceptions.Timeout:
            print("Bot: ⏳ Zu lange gedauert.")
            gedaechtnis.letzte_entfernen()
            continue
        except Exception as fehler:
            print("Bot: ❌ Fehler:", fehler)
            gedaechtnis.letzte_entfernen()
            continue

        gedaechtnis.hinzufuegen("assistant", text)
        gedaechtnis.speichern()


if __name__ == "__main__":  # nur starten, wenn diese Datei ausgeführt wird
    main()