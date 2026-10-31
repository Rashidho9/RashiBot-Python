import requests  # Bibliothek für Netzwerk-Anfragen

MODELL = "llama3.2:1b"
CHARAKTER = (
    "Du bist RashiBot, ein freundlicher Assistent von Rashid. "
    "Antworte immer auf Deutsch, kurz und einfach."
)

# NEU: das Gedächtnis, eine Liste von Nachrichten
verlauf = [{"role": "system", "content": CHARAKTER}]

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