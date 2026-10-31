import requests  # Bibliothek für Netzwerk-Anfragen

# Konstanten: feste Werte schreibt man GROSS
MODELL = "llama3.2:1b"
CHARAKTER = (
    "Du bist RashiBot, ein freundlicher Assistent von Rashid. "
    "Antworte immer auf Deutsch, kurz und einfach."
)

print("RashiBot ist bereit! Tippe 'exit' zum Beenden.")

while True:
    frage = input("Du: ")

    if frage.lower() == "exit":
        print("Bot: Tschüss Rashid! 👋")
        break

    antwort = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODELL,
            "system": CHARAKTER,  # NEU: der Charakter des Bots
            "prompt": frage,
            "stream": False,
        },
    )
    print("Bot:", antwort.json()["response"])