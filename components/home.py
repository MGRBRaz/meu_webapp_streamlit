import streamlit as st
import pandas as pd
from data import get_processes_df, get_process_by_id, delete_process
from utils import export_to_excel, export_to_csv, get_status_color

def display_home(navigate_function):
    """Display the home page with the processes table"""
    st.header("Processos de Importação")
    
    # Search and filter section
    col1, col2, col3 = st.columns([3, 2, 2])
    
    with col1:
        search_term = st.text_input("Buscar processo", value=st.session_state.filter_value)
        st.session_state.filter_value = search_term
    
    with col2:
        status_filter = st.multiselect("Filtrar por status", 
                                      ["Em andamento", "Concluído", "Atrasado", "Pendente", "Cancelado"])
    
    with col3:
        date_range = st.date_input("Período", value=[], help="Selecione um intervalo de datas")
    
    # Get processes data
    df = get_processes_df()
    
    if df.empty:
        st.info("Nenhum processo encontrado. Adicione um novo processo clicando em 'Novo Processo'.")
        return
    
    # Apply filters
    filtered_df = df.copy()
    
    if search_term:
        filter_condition = False
        for col in filtered_df.columns:
            filter_condition |= filtered_df[col].astype(str).str.contains(search_term, case=False, na=False)
        filtered_df = filtered_df[filter_condition]
    
    if status_filter:
        filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
        
    # Display export options
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📥 Exportar para Excel",
            data=export_to_excel(filtered_df),
            file_name="processos_importacao.xlsx",
            mime="application/vnd.ms-excel"
        )
    
    with col2:
        st.download_button(
            label="📄 Exportar para CSV",
            data=export_to_csv(filtered_df),
            file_name="processos_importacao.csv",
            mime="text/csv"
        )
    
    # Add styling to the status column
    def color_status(val):
        color = get_status_color(val)
        return f'background-color: {color}; color: white; border-radius: 4px; padding: 0.2rem; text-align: center'
    
    # Display dataframe with styling (using .map instead of .applymap which is deprecated)
    st.dataframe(
        filtered_df.style.map(
            lambda x: color_status(x) if x in ["Em andamento", "Concluído", "Atrasado", "Pendente", "Cancelado"] else '',
            subset=['status']
        ),
        use_container_width=True,
        height=400,
        column_config={
            "id": "Código",
            "ref": "Referência",
            "invoice": "Invoice",
            "origin": "Origem",
            "type": "Tipo",
            "eta": "ETA",
            "status": "Status",
            "observations": "Observações",
            "last_update": "Última Atualização"
        }
    )
    
    # Action buttons for each row
    st.subheader("Ações")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        process_id = st.selectbox("Selecione um processo", filtered_df["id"].tolist())
    
    with col2:
        if st.button("👁️ Visualizar Detalhes", use_container_width=True):
            navigate_function("view_details", process_id)
    
    with col3:
        if st.button("✏️ Editar Processo", use_container_width=True):
            st.session_state.edit_mode = True
            navigate_function("add_edit", process_id)
    
    # Delete process option (with confirmation)
    if st.button("🗑️ Excluir Processo", use_container_width=True):
        st.warning("Tem certeza que deseja excluir este processo? Esta ação não pode ser desfeita.")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✓ Confirmar Exclusão", use_container_width=True):
                if delete_process(process_id):
                    st.success("Processo excluído com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao excluir processo.")
        
        with col2:
            if st.button("✗ Cancelar", use_container_width=True):
                st.rerun()
