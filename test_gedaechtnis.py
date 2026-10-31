"""Tests für die Klasse Gedaechtnis."""
import gedaechtnis
from gedaechtnis import Gedaechtnis


def neues_gedaechtnis(tmp_path, monkeypatch):
    """Hilfsfunktion: Gedächtnis mit einer Test-Datei statt der echten."""
    test_datei = tmp_path / "test.json"  # tmp_path = temporärer Ordner
    monkeypatch.setattr(gedaechtnis, "DATEI", str(test_datei))
    return Gedaechtnis()


def test_neues_gedaechtnis_ist_leer(tmp_path, monkeypatch):
    g = neues_gedaechtnis(tmp_path, monkeypatch)
    assert g.anzahl() == 0  # assert = "ich erwarte, dass ..."


def test_hinzufuegen_erhoeht_anzahl(tmp_path, monkeypatch):
    g = neues_gedaechtnis(tmp_path, monkeypatch)
    g.hinzufuegen("user", "Hallo")
    assert g.anzahl() == 1


def test_letzte_entfernen(tmp_path, monkeypatch):
    g = neues_gedaechtnis(tmp_path, monkeypatch)
    g.hinzufuegen("user", "Hallo")
    g.letzte_entfernen()
    assert g.anzahl() == 0


def test_speichern_und_laden(tmp_path, monkeypatch):
    g = neues_gedaechtnis(tmp_path, monkeypatch)
    g.hinzufuegen("user", "Ich wohne in Mülheim")
    g.speichern()

    g2 = Gedaechtnis()  # neues Objekt liest dieselbe Datei
    assert g2.anzahl() == 1
    assert g2.verlauf[1]["content"] == "Ich wohne in Mülheim"


def test_leeren(tmp_path, monkeypatch):
    g = neues_gedaechtnis(tmp_path, monkeypatch)
    g.hinzufuegen("user", "Hallo")
    g.leeren()
    assert g.anzahl() == 0
    assert g.verlauf[0]["role"] == "system"  # Charakter bleibt