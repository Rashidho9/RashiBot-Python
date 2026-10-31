# 🤖 RashiBot

Ein persönlicher KI-Chatbot in Python, der **lokal** mit [Ollama](https://ollama.com) läuft.
Keine Cloud, keine Kosten, die Daten bleiben auf dem eigenen PC.

## ✨ Funktionen
- Chat im Terminal mit Live-Antworten (Streaming)
- Gedächtnis, das in einer JSON-Datei gespeichert wird
- Eigener Charakter über einen System-Prompt
- Modelle wechseln mit `/modell`
- Fehlerbehandlung, wenn Ollama nicht läuft
- Automatische Tests mit pytest

## 🛠️ Installation
1. [Ollama](https://ollama.com/download) installieren
2. Modell laden: `ollama pull llama3.2:1b`
3. Projekt klonen und Pakete installieren:
   ```
   git clone https://github.com/DEIN-NAME/RashiBot.git
   cd RashiBot
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

## ▶️ Starten
```
python main.py
```

## ⌨️ Befehle
| Befehl | Funktion |
|---|---|
| `/hilfe` | Alle Befehle anzeigen |
| `/neu` | Gedächtnis löschen |
| `/verlauf` | Anzahl gespeicherter Nachrichten |
| `/modelle` | Installierte Modelle anzeigen |
| `/modell NAME` | Modell wechseln |
| `exit` | Beenden |

## 🧪 Tests
```
pytest -v
```

## 📁 Projektstruktur
```
config.py          Einstellungen
gedaechtnis.py     Klasse Gedaechtnis
ki_client.py       Klasse KiClient (Ollama)
main.py            Startpunkt
test_gedaechtnis.py  Tests
```

## 👤 Autor
Rashid Hosseini, Umschulung Fachinformatiker Anwendungsentwicklung (IAL)