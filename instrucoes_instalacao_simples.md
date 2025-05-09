# Instruções para Instalação e Uso do JGR Broker Importação

Este é um guia simplificado para instalar e executar o sistema JGR Broker Importação em um computador Windows sem a necessidade de conhecimentos técnicos.

## Requisitos Mínimos

- Windows 8, 10 ou 11
- 4GB de RAM
- 500MB de espaço em disco

## Passo a Passo para Instalação

### 1. Instalação do Python

1. Acesse o site oficial do Python: https://www.python.org/downloads/
2. Clique no botão "Download Python 3.11.x" (ou a versão mais recente)
3. Execute o arquivo baixado
4. **IMPORTANTE**: Na primeira tela da instalação, marque a opção "Add Python to PATH"
5. Clique em "Install Now" para iniciar a instalação
6. Aguarde a conclusão e clique em "Close"

### 2. Instalação do JGR Broker

1. Baixe o projeto completo do Replit
   - No Replit, clique nos três pontos (...) no canto superior direito
   - Selecione "Download as zip"
   - Extraia o zip para uma pasta de sua preferência (ex: C:\\JGRBroker)

2. Abra o Prompt de Comando:
   - Pressione a tecla Windows + R
   - Digite "cmd" e pressione Enter

3. Navegue até a pasta onde extraiu os arquivos:
   ```
   cd C:\caminho\para\pasta\extraida
   ```

4. Instale as dependências necessárias:
   ```
   pip install -r required_packages.txt
   ```

   Ou instale cada pacote individualmente:
   ```
   pip install streamlit==1.31.0 pandas==2.1.4 twilio==8.13.0 xlsxwriter==3.1.9
   ```

5. Execute o aplicativo:
   ```
   streamlit run app.py
   ```

6. Um navegador será aberto automaticamente com o sistema
   - Se não abrir, acesse manualmente: http://localhost:5000

### 3. Login no Sistema

- Usuário: `admin`
- Senha: `admin`

## Uso Diário

Para iniciar o sistema nas próximas vezes:

1. Abra o Prompt de Comando (Windows + R, digite "cmd")
2. Navegue até a pasta do sistema:
   ```
   cd C:\caminho\para\pasta\extraida
   ```
3. Execute o comando:
   ```
   streamlit run app.py
   ```

## Usando o Atalho para Facilitar o Acesso

Na pasta do sistema, você encontrará um arquivo chamado `iniciar_jgr.bat`. 

1. Para iniciar facilmente o sistema, basta dar um duplo-clique neste arquivo
2. Ele abrirá automaticamente a aplicação no navegador
3. Se o navegador não abrir automaticamente, aguarde cerca de 10 segundos e acesse manualmente: http://localhost:5000

O arquivo contém as seguintes instruções:
```
@echo off
cd /d "%~dp0"
echo Iniciando JGR Broker Importacao...
start "" "http://localhost:5000"
streamlit run app.py
```

## Importante

- Todos os dados são armazenados localmente na pasta do sistema
- Faça backups regulares dos arquivos `data.json`, `users.json` e `shared_links.json`
- Em caso de problemas, verifique se o Python foi instalado corretamente e se todas as dependências foram instaladas

## Suporte

Em caso de dúvidas ou problemas, entre em contato com o suporte técnico.