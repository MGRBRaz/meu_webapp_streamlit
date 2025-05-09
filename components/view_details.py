import streamlit as st
import pandas as pd
from datetime import datetime

from data import get_process_by_id, add_event
from components.event_log import display_event_log
from utils import format_date, get_status_color

def display_detail_view(navigate_function):
    """Display detailed view of a process"""
    process_id = st.session_state.selected_process
    process = get_process_by_id(process_id)
    
    if process is None:
        st.error("Processo não encontrado!")
        if st.button("← Voltar para a lista de processos"):
            navigate_function("home")
        return
    
    # Title with process ID and status
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header(f"Processo de Importação - {process['id']}")
        st.caption(f"Referência: {process.get('ref', '')}")
    
    with col2:
        status = process.get('status', 'Em andamento')
        status_color = get_status_color(status)
        st.markdown(f"""
        <div style="background-color: {status_color}; color: white; padding: 10px; 
        border-radius: 5px; text-align: center; font-weight: bold;">
            {status}
        </div>
        """, unsafe_allow_html=True)
    
    # Main information in tabs
    tab1, tab2, tab3 = st.tabs(["Informações Gerais", "Eventos", "Documentos"])
    
    # Tab 1: General Information
    with tab1:
        # Display process details in a structured way
        st.subheader("Detalhes do Processo")
        
        # First row: Basic info
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Código:**")
            st.markdown(process.get('id', ''))
            
            st.markdown("**Referência:**")
            st.markdown(process.get('ref', ''))
            
            st.markdown("**Invoice:**")
            st.markdown(process.get('invoice', ''))
        
        with col2:
            st.markdown("**Origem:**")
            st.markdown(process.get('origin', ''))
            
            st.markdown("**Tipo:**")
            st.markdown(process.get('type', ''))
            
            st.markdown("**ETA:**")
            st.markdown(format_date(process.get('eta', '')))
        
        with col3:
            st.markdown("**Status:**")
            st.markdown(process.get('status', ''))
            
            st.markdown("**Última Atualização:**")
            st.markdown(format_date(process.get('last_update', '')))
        
        st.divider()
        
        # Second row: Shipping info
        st.subheader("Informações de Embarque")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Exportador:**")
            st.markdown(process.get('exporter', ''))
            
            st.markdown("**Navio:**")
            st.markdown(process.get('ship', ''))
        
        with col2:
            st.markdown("**Agente:**")
            st.markdown(process.get('agent', ''))
            
            st.markdown("**Número B/L:**")
            st.markdown(process.get('bl_number', ''))
        
        with col3:
            st.markdown("**Previsão de Chegada:**")
            st.markdown(format_date(process.get('arrival_date', '')))
            
            st.markdown("**Container:**")
            st.markdown(process.get('container', ''))
        
        st.divider()
        
        # Third row: Additional info
        st.subheader("Informações Adicionais")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Terminal:**")
            st.markdown(process.get('terminal', ''))
            
            st.markdown("**Nota Fiscal:**")
            st.markdown(process.get('invoice_number', ''))
        
        with col2:
            st.markdown("**D.I.:**")
            st.markdown(process.get('di', ''))
            
            st.markdown("**Free Time:**")
            st.markdown(f"{process.get('free_time', '')} dias")
        
        with col3:
            st.markdown("**Data de Devolução:**")
            st.markdown(format_date(process.get('return_date', '')))
        
        st.divider()
        
        # Observations
        st.subheader("Observações")
        st.text_area("", value=process.get('observations', ''), disabled=True, height=100)
    
    # Tab 2: Events log
    with tab2:
        display_event_log(process)
        
        # Add new event
        st.subheader("Adicionar Novo Evento")
        with st.form("add_event_form"):
            event_description = st.text_area("Descrição do Evento", height=100)
            
            col1, col2 = st.columns(2)
            
            with col1:
                submit = st.form_submit_button("Adicionar Evento", use_container_width=True)
            
            with col2:
                cancel = st.form_submit_button("Cancelar", use_container_width=True)
        
        if submit and event_description:
            if add_event(process_id, event_description):
                st.success("Evento adicionado com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao adicionar evento!")
    
    # Tab 3: Documents
    with tab3:
        st.info("Funcionalidade de documentos será implementada em uma versão futura.")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("← Voltar para a lista", use_container_width=True):
            navigate_function("home")
    
    with col2:
        if st.button("✏️ Editar Processo", use_container_width=True):
            st.session_state.edit_mode = True
            navigate_function("add_edit", process_id)
    
    with col3:
        st.download_button(
            label="📄 Exportar Detalhes (PDF)",
            data="Funcionalidade em desenvolvimento",
            file_name=f"processo_{process_id}.txt",
            mime="text/plain",
            disabled=True,
            use_container_width=True
        )
