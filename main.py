"""Startpunkt von RashiBot."""
import requests

from gedaechtnis import Gedaechtnis
from ki_client import KiClient


def hilfe_anzeigen():
    """Alle Befehle anzeigen."""
    print("📋 Befehle:")
    print("  /hilfe        - diese Hilfe anzeigen")
    print("  /neu          - Gedächtnis löschen")
    print("  /verlauf      - Anzahl gespeicherter Nachrichten")
    print("  /modelle      - installierte Modelle anzeigen")
    print("  /modell NAME  - Modell wechseln")
    print("  exit          - RashiBot beenden")


def main():
    gedaechtnis = Gedaechtnis()  # Objekt erzeugen (wie new in Java)
    ki = KiClient()
    print("RashiBot ist bereit! Tippe /hilfe für alle Befehle.")

    while True:
        frage = input("Du: ").strip()

        # --- Leere Eingabe ignorieren ---
        if frage == "":
            continue

        # --- Beenden ---
        if frage.lower() == "exit":
            print("Bot: Tschüss Rashid! 👋")
            break

        # --- Befehle ---
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

        if frage.lower() == "/modelle":
            try:
                for name in ki.modelle_auflisten():
                    zeichen = "👉" if name == ki.modell else "  "
                    print(f"{zeichen} {name}")
            except requests.exceptions.ConnectionError:
                print("Bot: ⚠️ Ollama läuft nicht.")
            continue

        if frage.lower().startswith("/modell "):
            neues = frage.split(" ", 1)[1].strip()
            try:
                if neues in ki.modelle_auflisten():
                    ki.modell = neues
                    print(f"Bot: ✅ Modell gewechselt zu {neues}")
                else:
                    print("Bot: ❓ Modell nicht gefunden. Tippe /modelle.")
            except requests.exceptions.ConnectionError:
                print("Bot: ⚠️ Ollama läuft nicht.")
            continue

        if frage.startswith("/"):
            print("Bot: ❓ Unbekannter Befehl. Tippe /hilfe.")
            continue

        # --- Normale Frage an die KI ---
        gedaechtnis.hinzufuegen("user", frage)
        try:
            print("Bot: ", end="", flush=True)
            text = ki.frage_streamen(gedaechtnis.verlauf)
        except requests.exceptions.ConnectionError:
            print("⚠️ Ollama läuft nicht.")
            gedaechtnis.letzte_entfernen()
            continue
        except requests.exceptions.Timeout:
            print("⏳ Zu lange gedauert.")
            gedaechtnis.letzte_entfernen()
            continue
        except Exception as fehler:
            print("❌ Fehler:", fehler)
            gedaechtnis.letzte_entfernen()
            continue

        gedaechtnis.hinzufuegen("assistant", text)
        gedaechtnis.speichern()

if __name__ == "__main__":  # nur starten, wenn diese Datei ausgeführt wird
    main()