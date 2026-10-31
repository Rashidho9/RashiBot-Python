import requests    #Bibliothek für Internet-/Netzwerk-Anfragen
frage = input("Du :")    # Text von der Tastatur lesen
# Anfrage an Ollama auf deinem eigenen PC schicken
antwort = requests.post("http://localhost:11434/api/generate",
    json={"model": "llama3.2:1b", "prompt": frage, "stream": False},
)

print("Bot:", antwort.json()["response"])  # Antwort anzeigen