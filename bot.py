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

verlauf = laden()
print("RashiBot ist bereit! Tippe 'exit' zum Beenden.")

while True:
    frage = input("Du: ")

    if frage.lower() == "exit":
        print("Bot: Tschüss Rashid! 👋")
        break

    # Deine Frage ins Gedächtnis schreiben
    verlauf.append({"role": "user", "content": frage})

    antwort = requests.post(
        "http://localhost:11434/api/chat",  # NEU: chat statt generate
        json={"model": MODELL, "messages": verlauf, "stream": False},
    )
    text = antwort.json()["message"]["content"]  # NEU: anderer Pfad
    print("Bot:", text)

    # Antwort des Bots auch merken
    verlauf.append({"role": "assistant", "content": text})
    speichern(verlauf)