import json  # NEU: Listen/Wörterbücher als Datei speichern
import os    # NEU: prüfen, ob eine Datei existiert
import requests  # Bibliothek für Netzwerk-Anfragen

MODELL = "llama3.2:1b"
DATEI = "gedaechtnis.json"  # NEU: Name der Gedächtnis-Datei
CHARAKTER = (
    "Du bist RashiBot, ein freundlicher Assistent von Rashid. "
    "Antworte immer auf Deutsch, kurz und einfach."
)

def laden():
    """Gedächtnis aus der Datei laden, sonst neu anfangen."""
    if os.path.exists(DATEI):
        with open(DATEI, "r", encoding="utf-8") as f:
            return json.load(f)
    return [{"role": "system", "content": CHARAKTER}]


def speichern(verlauf):
    """Gedächtnis in die Datei schreiben."""
    with open(DATEI, "w", encoding="utf-8") as f:
        json.dump(verlauf, f, ensure_ascii=False, indent=2)
    return None

def hilfe_anzeigen():
    """Alle Befehle anzeigen."""
    print("📋 Befehle:")
    print("  /hilfe   - diese Hilfe anzeigen")
    print("  /neu     - Gedächtnis löschen")
    print("  /verlauf - Anzahl gespeicherter Nachrichten")
    print("  exit     - RashiBot beenden")



verlauf = laden()
print("RashiBot ist bereit! Tippe 'exit' zum Beenden.")

while True:
    frage = input("Du: ")

    if frage.lower() == "exit":
        print("Bot: Tschüss Rashid! 👋")
        break
    if frage.lower() == "/hilfe":
        hilfe_anzeigen()
        continue
    if frage.lower() == "/neu":
        verlauf = [{"role": "system", "content": CHARAKTER}]
        speichern(verlauf)
        print("Bot: 🧹 Gedächtnis gelöscht. Wir fangen neu an!")
        continue
    if frage.lower() == "/verlauf":
        anzahl = len(verlauf) - 1  # ohne den System-Prompt
        print(f"Bot: 💬 Ich habe {anzahl} Nachrichten gespeichert.")
        continue
    if frage.startswith("/"):  # unbekannter Befehl
        print("Bot: ❓ Unbekannter Befehl. Tippe /hilfe.")
        continue
    if frage.strip() == "":  # leere Eingabe ignorieren
        continue

    # Deine Frage ins Gedächtnis schreiben
    verlauf.append({"role": "user", "content": frage})

    try:  # NEU: "versuche das hier"
        antwort = requests.post(
            "http://localhost:11434/api/chat",
            json={"model": MODELL, "messages": verlauf, "stream": False},
            timeout=120,  # NEU: max. 120 Sekunden warten
        )
        antwort.raise_for_status()  # NEU: Fehler, wenn der Server meckert
        text = antwort.json()["message"]["content"]
    except requests.exceptions.ConnectionError:
        print("Bot: ⚠️ Ollama läuft nicht. Starte Ollama und versuch es nochmal.")
        verlauf.pop()  # Frage wieder entfernen, sie wurde nicht beantwortet
        continue  # zurück an den Anfang der Schleife
    except requests.exceptions.Timeout:
        print("Bot: ⏳ Das hat zu lange gedauert. Versuch eine kürzere Frage.")
        verlauf.pop()
        continue
    except Exception as fehler:  # alle anderen Fehler
        print("Bot: ❌ Unbekannter Fehler:", fehler)
        verlauf.pop()
        continue
    print("Bot:", text)
    verlauf.append({"role": "assistant", "content": text})
    speichern(verlauf)