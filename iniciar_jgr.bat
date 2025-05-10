@echo off
cd /d "%~dp0"
echo Iniciando JGR Broker Importacao...
streamlit run app.py --server.port 5000 --server.address 0.0.0.0
REM O navegador será aberto automaticamente pelo Streamlit