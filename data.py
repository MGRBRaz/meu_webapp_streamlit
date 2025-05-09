import pandas as pd
import streamlit as st
import os
import json
from datetime import datetime

# Default data structure based on the screenshots
DEFAULT_DATA = {
    "company_info": {
        "name": "JGR BROKER",
        "logo_path": "assets/images/jgr_logo.png",
        "contact": "contato@jgrbroker.com",
        "phone": "+55 (XX) XXXX-XXXX"
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
            "return_date": "25/01/2023",
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
            "return_date": "27/01/2023",
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
                return json.load(f)
        else:
            return DEFAULT_DATA
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

def add_event(process_id, description):
    """Add an event to a process"""
    for process in st.session_state.data["processes"]:
        if process["id"] == process_id:
            process["events"].append({
                "date": datetime.now().strftime("%d/%m/%Y"),
                "description": description,
                "user": "Admin"
            })
            process["last_update"] = datetime.now().strftime("%d/%m/%Y")
            save_data(st.session_state.data)
            return True
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
    
    # Select columns for main table view
    display_columns = ["id", "ref", "invoice", "origin", "type", "eta", 
                       "status", "observations", "last_update"]
    
    return df[display_columns]
