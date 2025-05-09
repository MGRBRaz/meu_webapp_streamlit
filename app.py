import streamlit as st
import pandas as pd
from datetime import datetime
import os
import urllib.parse

from components.home import display_home
from components.add_edit import display_add_edit_form
from components.view_details import display_detail_view
from components.client_view import display_client_view
from components.share import display_share_interface, validate_share_token
from components.settings import display_settings
from data import load_data, save_data
from assets.stock_photos import get_random_image

# Page configuration
st.set_page_config(
    page_title="Sistema de Acompanhamento de Importação",
    page_icon="🚢",
    layout="wide",
)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = load_data()
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"
if 'selected_process' not in st.session_state:
    st.session_state.selected_process = None
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
if 'filter_value' not in st.session_state:
    st.session_state.filter_value = ""

# Check URL parameters for client view mode
query_params = st.query_params
if "token" in query_params:
    token = query_params["token"]
    process_id = validate_share_token(token)
    
    if process_id:
        # Display client view for this process
        st.image("assets/images/jgr_logo.png", width=150)
        st.title("JGR BROKER - Sistema de Acompanhamento de Importação")
        
        display_client_view(process_id)
        
        # Footer for client view
        st.divider()
        st.caption(f"© {datetime.now().year} JGR BROKER - Todos os direitos reservados")
        
        # Exit the app here to prevent showing the admin interface
        st.stop()
    else:
        st.error("Link de compartilhamento inválido ou expirado!")

# Navigation functions
def navigate_to(page, process_id=None):
    st.session_state.current_page = page
    if process_id is not None:
        st.session_state.selected_process = process_id
    st.rerun()

# Header with logo and navigation
col1, col2 = st.columns([1, 3])

with col1:
    st.image("assets/images/jgr_logo.png", width=150)
    
with col2:
    st.title("Sistema de Acompanhamento de Importação")
    st.caption("JGR BROKER - Monitoramento e gestão de processos de importação")

# Navigation bar
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)
with nav_col1:
    if st.button("📋 Painel", use_container_width=True):
        navigate_to("home")
with nav_col2:
    if st.button("➕ Novo Processo", use_container_width=True):
        st.session_state.edit_mode = False
        navigate_to("add_edit")
with nav_col3:
    if st.button("🔗 Compartilhar", use_container_width=True):
        navigate_to("share")
with nav_col4:
    if st.button("📊 Relatórios", use_container_width=True):
        navigate_to("reports")
with nav_col5:
    if st.button("⚙️ Configurações", use_container_width=True):
        navigate_to("settings")

st.divider()

# Display the current page
if st.session_state.current_page == "home":
    display_home(navigate_to)
elif st.session_state.current_page == "add_edit":
    display_add_edit_form(navigate_to)
elif st.session_state.current_page == "view_details":
    display_detail_view(navigate_to)
elif st.session_state.current_page == "share":
    display_share_interface()
elif st.session_state.current_page == "reports":
    st.header("Relatórios")
    st.info("Funcionalidade de relatórios será implementada em uma versão futura.")
elif st.session_state.current_page == "settings":
    display_settings()

# Footer
st.divider()
current_year = datetime.now().year
st.caption(f"© {current_year} JGR BROKER - Todos os direitos reservados")
