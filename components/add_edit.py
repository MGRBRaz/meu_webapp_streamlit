import streamlit as st
import pandas as pd
from datetime import datetime
from data import get_process_by_id, add_process, update_process

def display_add_edit_form(navigate_function):
    """Display form for adding or editing a process"""
    
    if st.session_state.edit_mode:
        st.header("Editar Processo de Importação")
        process = get_process_by_id(st.session_state.selected_process)
        if process is None:
            st.error("Processo não encontrado!")
            return
    else:
        st.header("Novo Processo de Importação")
        process = {}
    
    # Create a form with multiple sections
    with st.form("process_form"):
        # Basic Information Section
        st.subheader("Informações Básicas")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            process_id = st.text_input("Código", value=process.get("id", ""), disabled=st.session_state.edit_mode)
            reference = st.text_input("Referência", value=process.get("ref", ""))
        
        with col2:
            invoice = st.text_input("Invoice", value=process.get("invoice", ""))
            origin = st.selectbox("Origem", options=["CHINA", "USA", "GERMANY", "JAPAN", "OTHER"], 
                                 index=0 if not process.get("origin") else ["CHINA", "USA", "GERMANY", "JAPAN", "OTHER"].index(process.get("origin")))
        
        with col3:
            container_type = st.text_input("Tipo", value=process.get("type", "FCL 1 X 40"))
            eta = st.date_input("ETA", value=None if not process.get("eta") else pd.to_datetime(process.get("eta"), format="%d/%m/%y"))
        
        # Shipping Information Section
        st.subheader("Informações de Embarque")
        col1, col2 = st.columns(2)
        
        with col1:
            exporter = st.text_input("Exportador", value=process.get("exporter", ""))
            ship = st.text_input("Navio", value=process.get("ship", ""))
            agent = st.text_input("Agente", value=process.get("agent", ""))
        
        with col2:
            bl_number = st.text_input("Número B/L", value=process.get("bl_number", ""))
            arrival_date = st.date_input("Previsão de Chegada", value=None if not process.get("arrival_date") else pd.to_datetime(process.get("arrival_date"), format="%d/%m/%Y"))
            container = st.text_input("Container", value=process.get("container", ""))
        
        # Additional Information Section
        st.subheader("Informações Adicionais")
        col1, col2 = st.columns(2)
        
        with col1:
            terminal = st.text_input("Terminal", value=process.get("terminal", ""))
            invoice_number = st.text_input("Nota Fiscal", value=process.get("invoice_number", ""))
            di = st.text_input("D.I.", value=process.get("di", ""))
        
        with col2:
            free_time = st.text_input("Free Time (dias)", value=process.get("free_time", "7"))
            return_date = st.date_input("Data de Devolução", value=None if not process.get("return_date") else pd.to_datetime(process.get("return_date"), format="%d/%m/%Y"))
            status = st.selectbox("Status", options=["Em andamento", "Concluído", "Atrasado", "Pendente", "Cancelado"], 
                                 index=0 if not process.get("status") else ["Em andamento", "Concluído", "Atrasado", "Pendente", "Cancelado"].index(process.get("status")))
        
        # Observations
        observations = st.text_area("Observações", value=process.get("observations", ""), height=100)
        
        # Submit buttons
        col1, col2 = st.columns(2)
        
        with col1:
            submit_button = st.form_submit_button("Salvar", use_container_width=True)
        
        with col2:
            cancel_button = st.form_submit_button("Cancelar", use_container_width=True)
    
    # Handle form submission
    if submit_button:
        # Prepare process data
        process_data = {
            "id": process_id if process_id else None,
            "ref": reference,
            "invoice": invoice,
            "origin": origin,
            "type": container_type,
            "eta": eta.strftime("%d/%m/%y") if eta else "",
            "status": status,
            "observations": observations,
            "exporter": exporter,
            "ship": ship,
            "agent": agent,
            "bl_number": bl_number,
            "arrival_date": arrival_date.strftime("%d/%m/%Y") if arrival_date else "",
            "container": container,
            "terminal": terminal,
            "invoice_number": invoice_number,
            "di": di,
            "free_time": free_time,
            "return_date": return_date.strftime("%d/%m/%Y") if return_date else "",
            "last_update": datetime.now().strftime("%d/%m/%y")
        }
        
        # If editing, maintain the existing events
        if st.session_state.edit_mode:
            process_data["events"] = process.get("events", [])
            
            # Add an update event
            process_data["events"].append({
                "date": datetime.now().strftime("%d/%m/%Y"),
                "description": "Processo atualizado",
                "user": "Admin"
            })
            
            # Update the process
            if update_process(process_data):
                st.success("Processo atualizado com sucesso!")
                st.session_state.edit_mode = False
                navigate_function("home")
            else:
                st.error("Erro ao atualizar processo!")
        else:
            # Add a new process
            if add_process(process_data):
                st.success("Processo adicionado com sucesso!")
                navigate_function("home")
            else:
                st.error("Erro ao adicionar processo!")
    
    if cancel_button:
        st.session_state.edit_mode = False
        navigate_function("home")
