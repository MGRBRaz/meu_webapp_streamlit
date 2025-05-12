import pandas as pd
import streamlit as st
import os
import json
import uuid
from datetime import datetime
from utils import format_date

# Default data structure based on the screenshots
DEFAULT_DATA = {
    "company_info": {
        "name": "JGR BROKER",
        "logo_path": "assets/images/jgr_logo.png",
        "contact": "contato@jgrbroker.com",
        "phone": "+55 (XX) XXXX-XXXX"
    },
    "config": {
        "storage_days_per_period": 30  # Dias por período de armazenagem (configurável)
    },
    "processes": [
        {
            "id": "20230001",
            "ref": "DKA-1/Sydex Adventure",
            "invoice": "148/23",
            "origin": "CHINA",
            "type": "FCL 1 X 40",
            "eta": "22/04/23",
            "status": "Em andamento",
            "observations": "",
            "last_update": "07/04/23",
            "exporter": "SNF INC",
            "ship": "MSC VIDHI",
            "agent": "MSC",
            "bl_number": "MEDBX123456",
            "arrival_date": "18/01/2023",
            "container": "TTNU1212342",
            "terminal": "ECOPORTO",
            "invoice_number": "7666",
            "di": "20/146885-6",
            "free_time": "7",
            "free_time_expiry": "25/01/2023",  # Vencimento do Free Time
            "return_date": "25/01/2023",
            "po": "PO123456",  # Número da Purchase Order
            "product": "Eletrônicos",  # Produto
            "map": "MAPA123",  # Número do Mapa
            "port_entry_date": "19/01/2023",  # Data de entrada no Porto/Recinto
            "current_period_start": "19/01/2023",  # Início do período atual de armazenagem
            "current_period_expiry": "18/02/2023",  # Vencimento do período
            "storage_days": "6",  # Dias armazenados (calculado)
            "original_docs": "Sim",  # Documentos originais
            "empty_return": "25/01/2023",  # Devolução de vazio
            "events": [
                {"date": "07/04/23", "description": "Processo criado", "user": "Admin"},
                {"date": "10/04/23", "description": "Documentação recebida", "user": "Admin"},
                {"date": "15/04/23", "description": "Navio em trânsito", "user": "Admin"}
            ]
        },
        {
            "id": "20230002",
            "ref": "DKL-1/Sydex Adventure",
            "invoice": "149/23",
            "origin": "CHINA",
            "type": "FCL 1 X 40",
            "eta": "25/04/23",
            "status": "Em andamento",
            "observations": "",
            "last_update": "08/04/23",
            "exporter": "SNF INC",
            "ship": "MSC VIDHI",
            "agent": "MSC",
            "bl_number": "MEDBX654321",
            "arrival_date": "20/01/2023",
            "container": "TTNU3434343",
            "terminal": "ECOPORTO",
            "invoice_number": "7667",
            "di": "20/146886-7",
            "free_time": "7",
            "free_time_expiry": "27/01/2023",  # Vencimento do Free Time
            "return_date": "27/01/2023",
            "po": "PO654321",  # Número da Purchase Order
            "product": "Máquinas",  # Produto
            "map": "MAPA456",  # Número do Mapa
            "port_entry_date": "21/01/2023",  # Data de entrada no Porto/Recinto
            "current_period_start": "21/01/2023",  # Início do período atual de armazenagem
            "current_period_expiry": "20/02/2023",  # Vencimento do período
            "storage_days": "8",  # Dias armazenados (calculado)
            "original_docs": "Não",  # Documentos originais
            "empty_return": "27/01/2023",  # Devolução de vazio
            "events": [
                {"date": "08/04/23", "description": "Processo criado", "user": "Admin"},
                {"date": "12/04/23", "description": "Documentação recebida", "user": "Admin"},
                {"date": "17/04/23", "description": "Navio em trânsito", "user": "Admin"}
            ]
        }
    ]
}

def load_data():
    """Load data from file or return default data"""
    try:
        if os.path.exists("data.json"):
            with open("data.json", "r") as f:
                data = json.load(f)
        else:
            data = DEFAULT_DATA
            
        # Garantir que todos os processos tenham campos necessários
        for process in data["processes"]:
            # Garantir que todos os eventos tenham IDs únicos
            if "events" in process:
                # Realizar a verificação em dois passos para evitar erros de iteração
                events_to_update = []
                for i, event in enumerate(process["events"]):
                    if "id" not in event or event["id"] is None or event["id"] == "":
                        events_to_update.append(i)
                
                # Adicionar IDs aos eventos que não têm
                for i in events_to_update:
                    process["events"][i]["id"] = str(uuid.uuid4())
                    print(f"ID gerado para evento {i} do processo {process['id']}: {process['events'][i]['id']}")
            
            # Garantir que exista o campo 'type' (para compatibilidade)
            if "type" not in process:
                process["type"] = "importacao"  # Valor padrão
            
            # Para registros antigos, converter 'type' do tipo de carga para tipo de processo
            if process.get("type") in ["FCL 1 X 40", "FCL 1 X 20", "LCL"]:
                # Guardar o tipo de container/carga em outro campo
                process["container_type"] = process["type"]
                # Definir o tipo de processo como importação (valor padrão)
                process["type"] = "importacao"
        
        return data
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return DEFAULT_DATA

def save_data(data):
    """Save data to file"""
    try:
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar dados: {e}")
        return False

def get_process_by_id(process_id):
    """Get a process by ID"""
    for process in st.session_state.data["processes"]:
        if process["id"] == process_id:
            return process
    return None

def update_process(process_data):
    """Update an existing process"""
    for i, process in enumerate(st.session_state.data["processes"]):
        if process["id"] == process_data["id"]:
            st.session_state.data["processes"][i] = process_data
            save_data(st.session_state.data)
            return True
    return False

def add_process(process_data):
    """Add a new process"""
    # Generate a new ID if not provided
    if not process_data.get("id"):
        process_data["id"] = generate_process_id()
    
    # Add timestamp for creation
    now = datetime.now().strftime("%d/%m/%Y")
    process_data["last_update"] = now
    
    # Initialize empty events list if not provided
    if "events" not in process_data:
        process_data["events"] = []
    
    # Add creation event
    process_data["events"].append({
        "date": now,
        "description": "Processo criado",
        "user": "Admin"
    })
    
    st.session_state.data["processes"].append(process_data)
    save_data(st.session_state.data)
    return True

def delete_process(process_id):
    """Delete a process by ID"""
    for i, process in enumerate(st.session_state.data["processes"]):
        if process["id"] == process_id:
            del st.session_state.data["processes"][i]
            save_data(st.session_state.data)
            return True
    return False

def add_event(process_id, description, user=None):
    """Add an event to a process"""
    if user is None and 'username' in st.session_state:
        user = st.session_state.username
    else:
        user = "Admin"
        
    for process in st.session_state.data["processes"]:
        if process["id"] == process_id:
            # Gerar um ID único para o evento
            event_id = str(uuid.uuid4())
            new_event = {
                "id": event_id,
                "date": datetime.now().strftime("%d/%m/%Y"),
                "description": description,
                "user": user
            }
            print(f"Adicionando evento com ID {event_id} ao processo {process_id}")
            
            # Inicializar a lista de eventos se não existir
            if "events" not in process:
                process["events"] = []
                
            process["events"].append(new_event)
            process["last_update"] = datetime.now().strftime("%d/%m/%Y")
            save_data(st.session_state.data)
            return True
    return False

def edit_event(process_id, event_id, new_description):
    """Edit an existing event"""
    print(f"Tentando editar evento: process_id={process_id}, event_id={event_id}, nova descrição={new_description}")
    for process in st.session_state.data["processes"]:
        if process["id"] == process_id:
            # Debug: listar todos os eventos neste processo para diagnóstico
            print(f"Processo {process_id} encontrado, procurando evento {event_id}")
            for i, event in enumerate(process.get("events", [])):
                print(f"  Evento {i}: id={event.get('id')}, description={event.get('description')}")
                
                # Verificar se o ID do evento corresponde
                current_id = event.get("id")
                if current_id == event_id:
                    print(f"  Evento {event_id} encontrado! Atualizando descrição...")
                    event["description"] = new_description
                    process["last_update"] = datetime.now().strftime("%d/%m/%Y")
                    save_data(st.session_state.data)
                    return True
                
                # Verificação alternativa para índices como chaves
                if current_id is None and event_id.startswith("event_"):
                    try:
                        # Se event_id é algo como "event_3", extrair o índice
                        idx = int(event_id.split("_")[1])
                        if idx == i:
                            print(f"  Correspondência por índice {idx}! Atualizando descrição...")
                            event["description"] = new_description
                            # Adicionar um ID ao evento para referência futura
                            event["id"] = str(uuid.uuid4())
                            process["last_update"] = datetime.now().strftime("%d/%m/%Y")
                            save_data(st.session_state.data)
                            return True
                    except (ValueError, IndexError):
                        pass
    
    print(f"Evento não encontrado para edição")
    return False

def delete_event(process_id, event_id):
    """Delete an event from a process"""
    print(f"Tentando excluir evento: process_id={process_id}, event_id={event_id}")
    for process in st.session_state.data["processes"]:
        if process["id"] == process_id:
            # Debug: listar todos os eventos neste processo para diagnóstico
            print(f"Processo {process_id} encontrado, procurando evento {event_id}")
            for i, event in enumerate(process.get("events", [])):
                print(f"  Evento {i}: id={event.get('id')}, description={event.get('description')}")
                
                # Verificar se o ID do evento corresponde
                current_id = event.get("id")
                if current_id == event_id:
                    print(f"  Evento {event_id} encontrado! Excluindo...")
                    del process["events"][i]
                    process["last_update"] = datetime.now().strftime("%d/%m/%Y")
                    save_data(st.session_state.data)
                    return True
                
                # Verificação alternativa para índices como chaves
                if current_id is None and event_id.startswith("event_"):
                    try:
                        # Se event_id é algo como "event_3", extrair o índice
                        idx = int(event_id.split("_")[1])
                        if idx == i:
                            print(f"  Correspondência por índice {idx}! Excluindo...")
                            del process["events"][i]
                            process["last_update"] = datetime.now().strftime("%d/%m/%Y")
                            save_data(st.session_state.data)
                            return True
                    except (ValueError, IndexError):
                        pass
    
    print(f"Evento não encontrado para exclusão")
    return False

def generate_process_id():
    """Generate a new process ID"""
    year = datetime.now().year
    existing_ids = [p["id"] for p in st.session_state.data["processes"] if p["id"].startswith(str(year))]
    if not existing_ids:
        return f"{year}0001"
    
    max_id = max(existing_ids)
    next_num = int(max_id[4:]) + 1
    return f"{year}{next_num:04d}"

def get_processes_df():
    """Convert processes to a DataFrame for display"""
    if not st.session_state.data["processes"]:
        return pd.DataFrame()
    
    df = pd.DataFrame(st.session_state.data["processes"])
    
    # Atualizar os dias armazenados para todos os processos
    for i, process in enumerate(st.session_state.data["processes"]):
        if "port_entry_date" in process and process["port_entry_date"]:
            try:
                entry_date = pd.to_datetime(process["port_entry_date"], dayfirst=True)
                today = pd.to_datetime(datetime.now().date())
                days_stored = (today - entry_date).days
                st.session_state.data["processes"][i]["storage_days"] = str(max(0, days_stored))
            except Exception as e:
                pass
    
    # Atualizar o DataFrame
    df = pd.DataFrame(st.session_state.data["processes"])
    
    # Select columns for main table view (removido "id" conforme solicitado)
    display_columns = [
        "status", "po", "ref", "origin", "product", "eta", 
        "free_time", "free_time_expiry", "empty_return", "map", 
        "invoice_number", "port_entry_date", "current_period_start", 
        "current_period_expiry", "storage_days", "original_docs"
    ]
    
    # Manter o id para uso interno, embora não seja exibido na tabela
    internal_id_column = "id"
    
    # Garantir que todas as colunas existam
    for col in display_columns:
        if col not in df.columns:
            df[col] = ""
    
    # Criar uma cópia do dataframe com as colunas de exibição e ID
    # Isso garante que o ID está disponível para operações internas
    # mas não aparece na tabela visível para o usuário
    full_df = df.copy()
    
    # Formatação das colunas de data para o padrão brasileiro (DD/MM/YYYY)
    date_columns = [
        "eta", "free_time_expiry", "empty_return", "port_entry_date", 
        "current_period_start", "current_period_expiry", "return_date"
    ]
    
    # Aplicar formatação apenas às colunas de data que existem no dataframe
    for col in date_columns:
        if col in full_df.columns:
            full_df[col] = full_df[col].apply(lambda x: format_date(x) if x else "")
    
    # Reorganizar colunas para que ID seja a primeira (para uso interno)
    columns_with_id = ["id"] + display_columns
    
    # Garantir que não há duplicatas
    columns_with_id = list(dict.fromkeys(columns_with_id))
    
    return full_df[columns_with_id]
