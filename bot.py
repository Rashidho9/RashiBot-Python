import requests  # Bibliothek für Netzwerk-Anfragen

print("RashiBot(v2) ist bereit! Tippe 'exit' zum Beenden.")

while True:  # Endlosschleife: läuft, bis wir 'break' sagen
    frage = input("Du: ")

    if frage.lower() == "exit":  # .lower() macht alles klein
        print("Bot: Tschüss Rashid! 👋")
        break  # Schleife beenden

    antwort = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2:1b", "prompt": frage, "stream": False},
    )
    print("Bot:", antwort.json()["response"])