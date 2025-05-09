@echo off
cd /d "%~dp0"
echo Iniciando JGR Broker Importacao...
start "" "http://localhost:5000"
streamlit run app.py