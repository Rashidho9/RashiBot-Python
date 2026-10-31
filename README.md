# 🤖 RashiBot

Ein persönlicher KI-Chatbot in Python, der **lokal** mit [Ollama](https://ollama.com) läuft.
Keine Cloud, keine Kosten, die Daten bleiben auf dem eigenen PC.

## ✨ Funktionen
- 🖼️ Grafische Oberfläche (tkinter) und Terminal-Version
- ⚡ Live-Antworten (Streaming)
- 🧠 Gedächtnis, gespeichert in einer JSON-Datei
- 🎭 Eigener Charakter über einen System-Prompt
- 📄 PDFs hochladen und Fragen dazu stellen (mit Quellenangabe)
- 🔄 Modelle wechseln mit `/modell`
- 🛡️ Fehlerbehandlung, wenn Ollama nicht läuft
- 🧪 Automatische Tests mit pytest

## 🛠️ Installation
1. [Ollama](https://ollama.com/download) installieren
2. Modelle laden:
   ```
   ollama pull llama3.2:1b
   ollama pull qwen2.5:1.5b
   ```
3. Projekt klonen und Pakete installieren:
   ```
   git clone https://github.com/Rashidho9/RashiBot-Python.git
   cd RashiBot-Python
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

## ▶️ Starten
| Version | Befehl |
|---|---|
| Fenster (GUI) | `python gui.py` |
| Terminal | `python main.py` |

## ⌨️ Befehle
| Befehl | Funktion |
|---|---|
| `/hilfe` | Alle Befehle anzeigen |
| `/neu` | Gedächtnis löschen |
| `/verlauf` | Anzahl gespeicherter Nachrichten |
| `/modelle` | Installierte Modelle anzeigen |
| `/modell NAME` | Modell wechseln |
| `/pdfs` | Geladene PDFs anzeigen (nur GUI) |
| `exit` | Beenden (nur Terminal) |

## 📄 Fragen zu PDFs
1. In der GUI auf **📄 PDF** klicken und eine Datei wählen
2. Frage stellen: RashiBot sucht die passenden Textstellen und antwortet mit **📚 Quelle**

**Grenzen:** Gescannte PDFs (nur Bilder) werden nicht gelesen. Die Suche basiert auf gemeinsamen Wörtern.

## 🧪 Tests
```
pytest -v
```

## 📁 Projektstruktur
```
config.py            Einstellungen (Modell, URL, Charakter)
gedaechtnis.py       Klasse Gedaechtnis (laden/speichern)
ki_client.py         Klasse KiClient (Ollama, Streaming)
pdf_wissen.py        Klasse PdfWissen (PDFs lesen und durchsuchen)
gui.py               Klasse RashiBotGUI (Fenster)
main.py              Terminal-Version
test_gedaechtnis.py  Tests
```

## 🧰 Technologien
Python 3 · tkinter · requests · pypdf · pytest · Ollama · Git/GitHub

## 👤 Autor
Rashid Hosseini, Umschulung Fachinformatiker Anwendungsentwicklung (IAL)
GitHub: [Rashidho9](https://github.com/Rashidho9)