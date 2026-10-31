"""Grafische Oberfläche für RashiBot."""
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext

from gedaechtnis import Gedaechtnis
from ki_client import KiClient
from pdf_wissen import PdfWissen


class RashiBotGUI:
    def __init__(self, fenster):
        self.fenster = fenster
        self.gedaechtnis = Gedaechtnis()
        self.ki = KiClient()
        self.wissen = PdfWissen()

        fenster.title("🤖 RashiBot")
        fenster.geometry("700x550")

        # Chat-Bereich (nur lesen, mit Scrollbalken)
        self.chat = scrolledtext.ScrolledText(
            fenster, wrap=tk.WORD, state="disabled", font=("Segoe UI", 11)
        )
        self.chat.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Unterer Bereich: Eingabe + Buttons
        unten = tk.Frame(fenster)
        unten.pack(fill=tk.X, padx=10, pady=(0, 10))

        self.eingabe = tk.Entry(unten, font=("Segoe UI", 11))
        self.eingabe.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.eingabe.bind("<Return>", lambda e: self.senden())  # Enter = senden
        self.eingabe.focus()

        self.senden_btn = tk.Button(unten, text="Senden", command=self.senden)
        self.senden_btn.pack(side=tk.LEFT, padx=5)

        tk.Button(unten, text="🧹 Neu", command=self.neu).pack(side=tk.LEFT)
        tk.Button(unten, text="📄 PDF", command=self.pdf_laden).pack(side=tk.LEFT, padx=5)

        self.verlauf_anzeigen()

    # ---------- Anzeige ----------
    def schreiben(self, text):
        """Text unten im Chat anhängen."""
        self.chat.configure(state="normal")
        self.chat.insert(tk.END, text)
        self.chat.see(tk.END)
        self.chat.configure(state="disabled")

    def verlauf_anzeigen(self):
        """Gespeicherten Verlauf beim Start ins Fenster schreiben."""
        for nachricht in self.gedaechtnis.verlauf:
            if nachricht["role"] == "user":
                self.schreiben(f"Du: {nachricht['content']}\n")
            elif nachricht["role"] == "assistant":
                self.schreiben(f"Bot: {nachricht['content']}\n\n")
        self.schreiben(f"Bot: Hallo Rashid! Modell: {self.ki.modell}. "
                       "Tippe /hilfe für Befehle.\n\n")

    # ---------- Befehle ----------
    def befehl_ausfuehren(self, befehl):
        """Befehle wie im Terminal."""
        b = befehl.lower()
        if b == "/hilfe":
            self.schreiben(
                "📋 Befehle:\n"
                "  /hilfe        - diese Hilfe\n"
                "  /neu          - Gedächtnis löschen\n"
                "  /verlauf      - Anzahl Nachrichten\n"
                "  /modelle      - installierte Modelle\n"
                "  /modell NAME  - Modell wechseln\n"
                "  /pdfs         - geladene PDFs anzeigen\n\n"
            )
        elif b == "/neu":
            self.neu()
        elif b == "/verlauf":
            self.schreiben(f"Bot: 💬 {self.gedaechtnis.anzahl()} Nachrichten gespeichert.\n\n")
        elif b == "/pdfs":
            if self.wissen.dateien:
                self.schreiben("Bot: 📚 " + ", ".join(self.wissen.dateien) + "\n\n")
            else:
                self.schreiben("Bot: Noch keine PDF geladen.\n\n")
        elif b == "/modelle":
            try:
                for name in self.ki.modelle_auflisten():
                    zeichen = "👉" if name == self.ki.modell else "   "
                    self.schreiben(f"{zeichen} {name}\n")
                self.schreiben("\n")
            except Exception:
                self.schreiben("Bot: ⚠️ Ollama läuft nicht.\n\n")
        elif b.startswith("/modell "):
            neues = befehl.split(" ", 1)[1].strip()
            try:
                if neues in self.ki.modelle_auflisten():
                    self.ki.modell = neues
                    self.schreiben(f"Bot: ✅ Modell gewechselt zu {neues}\n\n")
                else:
                    self.schreiben("Bot: ❓ Modell nicht gefunden. Tippe /modelle.\n\n")
            except Exception:
                self.schreiben("Bot: ⚠️ Ollama läuft nicht.\n\n")
        else:
            self.schreiben("Bot: ❓ Unbekannter Befehl. Tippe /hilfe.\n\n")

    # ---------- Senden ----------
    def senden(self):
        frage = self.eingabe.get().strip()
        if not frage:
            return
        self.eingabe.delete(0, tk.END)

        if frage.startswith("/"):
            self.schreiben(f"Du: {frage}\n")
            self.befehl_ausfuehren(frage)
            return

        self.schreiben(f"Du: {frage}\nBot: ")
        self.senden_btn.configure(state="disabled")
        self.gedaechtnis.hinzufuegen("user", frage)
        threading.Thread(target=self._ki_fragen, daemon=True).start()

    def _ki_fragen(self):
        """Läuft im Hintergrund-Thread."""
        try:
            nachrichten = list(self.gedaechtnis.verlauf)  # Kopie!
            frage = nachrichten[-1]["content"]
            treffer = self.wissen.suchen(frage)
            if treffer:
                kontext = "\n\n".join(f"[{name}]\n{text}" for _, name, text in treffer)
                nachrichten[-1] = {
                    "role": "user",
                    "content": (
                        "Beantworte die Frage NUR mit diesen Auszügen aus meinen PDFs. "
                        "Wenn die Antwort nicht drinsteht, sag das ehrlich.\n\n"
                        f"{kontext}\n\nFrage: {frage}"
                    ),
                }
            text = self.ki.frage_streamen(
                nachrichten,
                bei_wort=lambda w: self.fenster.after(0, self.schreiben, w),
            )
            if treffer:
                quellen = ", ".join(sorted({name for _, name, _ in treffer}))
                self.fenster.after(0, self.schreiben, f"\n📚 Quelle: {quellen}")
            self.gedaechtnis.hinzufuegen("assistant", text)
            self.gedaechtnis.speichern()
        except Exception as fehler:
            self.gedaechtnis.letzte_entfernen()
            self.fenster.after(0, self.schreiben, f"⚠️ Fehler: {fehler}")
        self.fenster.after(0, self._fertig)

    def _fertig(self):
        self.schreiben("\n\n")
        self.senden_btn.configure(state="normal")

    # ---------- Buttons ----------
    def neu(self):
        self.gedaechtnis.leeren()
        self.schreiben("Bot: 🧹 Gedächtnis gelöscht.\n\n")

    def pdf_laden(self):
        """Dateidialog öffnen und PDF einlesen."""
        pfad = filedialog.askopenfilename(filetypes=[("PDF-Dateien", "*.pdf")])
        if not pfad:
            return
        try:
            seiten = self.wissen.laden(pfad)
            self.schreiben(f"Bot: 📄 PDF geladen ({seiten} Seiten). "
                           "Stell mir Fragen dazu!\n\n")
        except Exception as fehler:
            self.schreiben(f"Bot: ⚠️ PDF konnte nicht gelesen werden: {fehler}\n\n")


if __name__ == "__main__":
    fenster = tk.Tk()
    RashiBotGUI(fenster)
    fenster.mainloop()