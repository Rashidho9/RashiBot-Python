@echo off
cd /d %~dp0
echo RashiBot wird installiert...
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull llama3.2:1b
echo Fertig! Starte jetzt starten.bat
pause