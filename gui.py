"""Grafische Oberfläche für RashiBot."""
import threading
import tkinter as tk
from tkinter import scrolledtext

from gedaechtnis import Gedaechtnis
from ki_client import KiClient


class RashiBotGUI:
    def __init__(self, fenster):
        self.fenster = fenster
        self.gedaechtnis = Gedaechtnis()
        self.ki = KiClient()

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

        self.verlauf_anzeigen()  # NEU: alten Verlauf beim Start zeigen

    def schreiben(self, text):
        """Text unten im Chat anhängen."""
        self.chat.configure(state="normal")
        self.chat.insert(tk.END, text)
        self.chat.see(tk.END)  # automatisch nach unten scrollen
        self.chat.configure(state="disabled")

    def verlauf_anzeigen(self):
        """Gespeicherten Verlauf aus dem Gedächtnis ins Fenster schreiben."""
        for nachricht in self.gedaechtnis.verlauf:
            if nachricht["role"] == "user":
                self.schreiben(f"Du: {nachricht['content']}\n")
            elif nachricht["role"] == "assistant":
                self.schreiben(f"Bot: {nachricht['content']}\n\n")
        self.schreiben(f"Bot: Hallo Rashid! Modell: {self.ki.modell}. "
                       "Tippe /hilfe für Befehle.\n\n")

    def befehl_ausfuehren(self, befehl):
        """Befehle wie im Terminal. Gibt True zurück, wenn es ein Befehl war."""
        b = befehl.lower()
        if b == "/hilfe":
            self.schreiben(
                "📋 Befehle:\n"
                "  /hilfe        - diese Hilfe\n"
                "  /neu          - Gedächtnis löschen\n"
                "  /verlauf      - Anzahl Nachrichten\n"
                "  /modelle      - installierte Modelle\n"
                "  /modell NAME  - Modell wechseln\n\n"
            )
        elif b == "/neu":
            self.neu()
        elif b == "/verlauf":
            self.schreiben(f"Bot: 💬 {self.gedaechtnis.anzahl()} Nachrichten gespeichert.\n\n")
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
        return True

    def senden(self):
        frage = self.eingabe.get().strip()
        if not frage:
            return
        self.eingabe.delete(0, tk.END)

        if frage.startswith("/"):  # NEU: Befehle abfangen
            self.schreiben(f"Du: {frage}\n")
            self.befehl_ausfuehren(frage)
            return

        self.schreiben(f"Du: {frage}\nBot: ")
        self.senden_btn.configure(state="disabled")
        self.gedaechtnis.hinzufuegen("user", frage)
        threading.Thread(target=self._ki_fragen, daemon=True).start()

    def _ki_fragen(self):
        try:
            text = self.ki.frage_streamen(
                self.gedaechtnis.verlauf,
                # Fenster nur im Haupt-Thread ändern, darum after()
                bei_wort=lambda w: self.fenster.after(0, self.schreiben, w),
            )
            self.gedaechtnis.hinzufuegen("assistant", text)
            self.gedaechtnis.speichern()
        except Exception as fehler:
            self.gedaechtnis.letzte_entfernen()
            self.fenster.after(0, self.schreiben, f"⚠️ Fehler: {fehler}")
        self.fenster.after(0, self._fertig)

    def _fertig(self):
        self.schreiben("\n\n")
        self.senden_btn.configure(state="normal")

    def neu(self):
        self.gedaechtnis.leeren()
        self.schreiben("Bot: 🧹 Gedächtnis gelöscht.\n\n")


if __name__ == "__main__":
    fenster = tk.Tk()
    RashiBotGUI(fenster)
    fenster.mainloop()  # Fenster offen halten und auf Klicks warten