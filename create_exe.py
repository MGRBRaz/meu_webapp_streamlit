import os
import sys
import shutil
import subprocess
import json

def create_exe():
    """Script simplificado para criar o executável do JGR Broker"""
    print("Iniciando criação do executável JGR Broker Importação...")
    
    # Criar pasta .streamlit se não existir
    streamlit_dir = ".streamlit"
    if not os.path.exists(streamlit_dir):
        os.makedirs(streamlit_dir)
        print(f"Pasta {streamlit_dir} criada")
        
    # Criar arquivo de configuração do Streamlit
    config_path = os.path.join(streamlit_dir, "config.toml")
    with open(config_path, "w") as f:
        f.write("""
[server]
headless = true
port = 5000
address = "localhost"
enableCORS = false
enableXsrfProtection = false

[theme]
primaryColor = "#4e89ae"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
        """)
    print(f"Arquivo de configuração do Streamlit criado em {config_path}")
    
    # Copiar arquivos de dados para a pasta dist
    print("Preparando arquivos de dados...")
    os.makedirs("dist", exist_ok=True)
    
    # Definir arquivos de dados a serem copiados
    data_files = ["data.json", "users.json", "shared_links.json"]
    
    # Verificar e criar arquivos vazios se não existirem
    for file in data_files:
        if not os.path.exists(file):
            if file == "data.json":
                default_data = {"processes": [], "config": {"storage_days_per_period": 10}}
                with open(file, "w") as f:
                    json.dump(default_data, f, indent=4)
                print(f"Arquivo {file} não encontrado. Criado arquivo vazio.")
            elif file == "users.json":
                default_users = {"users": [
                    {
                        "id": "admin-001",
                        "name": "Administrador",
                        "email": "admin",
                        "password": "admin",
                        "role": "admin"
                    }
                ]}
                with open(file, "w") as f:
                    json.dump(default_users, f, indent=4)
                print(f"Arquivo {file} não encontrado. Criado arquivo com usuário admin padrão.")
            elif file == "shared_links.json":
                default_links = {"links": []}
                with open(file, "w") as f:
                    json.dump(default_links, f, indent=4)
                print(f"Arquivo {file} não encontrado. Criado arquivo vazio.")
                
        # Copiar para a pasta dist
        shutil.copy(file, os.path.join("dist", file))
        print(f"Arquivo {file} copiado para dist/")
    
    # Criar pastas necessárias na pasta dist
    for folder in ["html_exports", "assets"]:
        folder_path = os.path.join("dist", folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Pasta {folder} criada em dist/")
    
    # Copiar pasta assets se existir
    if os.path.exists("assets"):
        asset_dest = os.path.join("dist", "assets")
        for item in os.listdir("assets"):
            item_path = os.path.join("assets", item)
            if os.path.isfile(item_path):
                shutil.copy2(item_path, os.path.join(asset_dest, item))
            elif os.path.isdir(item_path):
                dest_dir = os.path.join(asset_dest, item)
                shutil.copytree(item_path, dest_dir, dirs_exist_ok=True)
        print("Pasta assets copiada para dist/")
    
    # Detectar sistema operacional
    is_windows = sys.platform.startswith('win')
    separator = ";" if is_windows else ":"
    
    # Criar comando PyInstaller com todas as dependências necessárias
    cmd = [
        "pyinstaller",
        "--name=JGRBrokerImportacao",
        "--onefile",
        "--windowed",
        f"--add-data=data.json{separator}.",
        f"--add-data=users.json{separator}.",
        f"--add-data=shared_links.json{separator}.",
        f"--add-data=components{separator}components",
        f"--add-data=utils.py{separator}.",
        f"--add-data=html_generator.py{separator}.",
        f"--add-data=data.py{separator}.",
        f"--add-data=.streamlit{separator}.streamlit",
        "--icon=generated-icon.png" if os.path.exists("generated-icon.png") else "",
        "--hidden-import=streamlit.runtime.scriptrunner.magic_funcs",
        "--hidden-import=pandas",
        "--hidden-import=streamlit",
        "--hidden-import=xlsxwriter",
        "--hidden-import=twilio",
        "--hidden-import=twilio.rest",
        "app.py"
    ]
    
    # Remover argumentos vazios
    cmd = [arg for arg in cmd if arg]
    
    # Executar PyInstaller
    print("Executando PyInstaller...")
    print(" ".join(cmd))
    try:
        subprocess.run(cmd, check=True)
        print("\nExecutável criado com sucesso em dist/JGRBrokerImportacao.exe")
        
        # Copiar configuração do Streamlit para a pasta dist
        dist_streamlit_dir = os.path.join("dist", ".streamlit")
        if not os.path.exists(dist_streamlit_dir):
            os.makedirs(dist_streamlit_dir)
        shutil.copy(config_path, os.path.join(dist_streamlit_dir, "config.toml"))
        
        # Criar arquivo batch para Windows
        if is_windows:
            bat_path = os.path.join("dist", "Start_JGR_Broker.bat")
            with open(bat_path, "w") as f:
                f.write('@echo off\n')
                f.write('echo Iniciando JGR Broker Importacao...\n')
                f.write('cd /d "%~dp0"\n')
                f.write('start "" "JGRBrokerImportacao.exe"\n')
                f.write('echo Aguardando inicializacao do servidor (5 segundos)...\n')
                f.write('timeout /t 5 /nobreak\n')
                f.write('echo Abrindo navegador...\n')
                f.write('start http://localhost:5000\n')
                f.write('echo Sistema iniciado com sucesso!\n')
            print(f"Arquivo de inicialização criado em {bat_path}")
        else:
            # Criar script shell para Linux/Mac
            sh_path = os.path.join("dist", "start_jgr_broker.sh")
            with open(sh_path, "w") as f:
                f.write('#!/bin/bash\n')
                f.write('echo "Iniciando JGR Broker Importacao..."\n')
                f.write('cd "$(dirname "$0")"\n')
                f.write('./JGRBrokerImportacao &\n')
                f.write('echo "Aguardando inicializacao do servidor (5 segundos)..."\n')
                f.write('sleep 5\n')
                f.write('echo "Abrindo navegador..."\n')
                f.write('xdg-open http://localhost:5000 || open http://localhost:5000\n')
                f.write('echo "Sistema iniciado com sucesso!"\n')
            # Tornar o script executável
            os.chmod(sh_path, 0o755)
            print(f"Script de inicialização criado em {sh_path}")
        
        # Criar arquivo README.txt com instruções
        readme_path = os.path.join("dist", "README.txt")
        with open(readme_path, "w") as f:
            f.write("=== JGR BROKER IMPORTAÇÃO ===\n\n")
            if is_windows:
                f.write("Para iniciar o sistema:\n")
                f.write("1. Execute o arquivo 'Start_JGR_Broker.bat'\n")
                f.write("2. O servidor será iniciado e o navegador abrirá automaticamente\n")
                f.write("3. Se o navegador não abrir, acesse manualmente: http://localhost:5000\n\n")
            else:
                f.write("Para iniciar o sistema:\n")
                f.write("1. Execute o arquivo 'start_jgr_broker.sh'\n")
                f.write("2. O servidor será iniciado e o navegador abrirá automaticamente\n")
                f.write("3. Se o navegador não abrir, acesse manualmente: http://localhost:5000\n\n")
            f.write("Credenciais padrão:\n")
            f.write("- Login: admin\n")
            f.write("- Senha: admin\n\n")
            f.write("Importante:\n")
            f.write("- Não exclua nenhum arquivo ou pasta dentro deste diretório\n")
            f.write("- Os dados são salvos localmente nos arquivos JSON\n")
            f.write("- Para backup, copie os arquivos data.json, users.json e shared_links.json\n")
        print(f"Arquivo de instruções criado em {readme_path}")
        
        print("\nPROCESSO CONCLUÍDO!")
        print("O executável e todos os arquivos necessários foram criados na pasta 'dist'")
        if is_windows:
            print("Para executar, vá até a pasta 'dist' e execute o arquivo 'Start_JGR_Broker.bat'")
        else:
            print("Para executar, vá até a pasta 'dist' e execute o arquivo 'start_jgr_broker.sh'")
        
    except subprocess.CalledProcessError as e:
        print(f"Erro ao criar executável: {e}")

if __name__ == "__main__":
    create_exe()