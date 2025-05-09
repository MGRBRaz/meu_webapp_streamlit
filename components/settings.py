import streamlit as st
import os
from data import load_data, save_data

def display_settings():
    """Display settings page for configuring email and SMS"""
    st.header("Configurações")
    
    # Create tabs for different settings
    tab1, tab2, tab3 = st.tabs(["Email", "SMS", "Configurações Gerais"])
    
    # Tab 1: Email Settings
    with tab1:
        st.subheader("Configurações de Email")
        st.info("Configure as informações do servidor SMTP para envio de emails.")
        
        # Get existing values from session state
        smtp_server = st.session_state.get('smtp_server', os.environ.get('SMTP_SERVER', ''))
        smtp_port = st.session_state.get('smtp_port', os.environ.get('SMTP_PORT', 587))
        smtp_username = st.session_state.get('smtp_username', os.environ.get('SMTP_USERNAME', ''))
        smtp_password = st.session_state.get('smtp_password', os.environ.get('SMTP_PASSWORD', ''))
        from_email = st.session_state.get('from_email', os.environ.get('FROM_EMAIL', ''))
        
        with st.form("email_settings"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_smtp_server = st.text_input("Servidor SMTP", value=smtp_server)
                new_smtp_username = st.text_input("Usuário SMTP", value=smtp_username)
                new_from_email = st.text_input("Email de Envio", value=from_email or smtp_username)
            
            with col2:
                new_smtp_port = st.number_input("Porta SMTP", value=int(smtp_port), min_value=1, max_value=65535)
                new_smtp_password = st.text_input("Senha SMTP", value=smtp_password, type="password")
            
            submit = st.form_submit_button("Salvar Configurações de Email")
            
            if submit:
                # Store in session state
                st.session_state.smtp_server = new_smtp_server
                st.session_state.smtp_port = new_smtp_port
                st.session_state.smtp_username = new_smtp_username
                st.session_state.smtp_password = new_smtp_password
                st.session_state.from_email = new_from_email
                
                # Save to environment variables for current session
                os.environ['SMTP_SERVER'] = new_smtp_server
                os.environ['SMTP_PORT'] = str(new_smtp_port)
                os.environ['SMTP_USERNAME'] = new_smtp_username
                os.environ['SMTP_PASSWORD'] = new_smtp_password
                os.environ['FROM_EMAIL'] = new_from_email
                
                st.success("Configurações de email salvas com sucesso!")
        
        # Test email
        st.subheader("Testar Configurações de Email")
        with st.form("test_email"):
            test_email = st.text_input("Email para teste")
            test_submit = st.form_submit_button("Enviar Email de Teste")
            
            if test_submit and test_email:
                from utils import send_email
                result = send_email(
                    test_email, 
                    "Teste de Configuração de Email", 
                    "Este é um email de teste do Sistema de Acompanhamento de Importação."
                )
                
                if result:
                    st.success("Email de teste enviado com sucesso!")
                else:
                    st.error("Falha ao enviar email de teste. Verifique as configurações.")
    
    # Tab 2: SMS Settings
    with tab2:
        st.subheader("Configurações de SMS (Twilio)")
        st.info("Configure as credenciais do Twilio para envio de SMS.")
        
        # Get existing values
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID', '')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN', '')
        phone_number = os.environ.get('TWILIO_PHONE_NUMBER', '')
        
        with st.form("sms_settings"):
            new_account_sid = st.text_input("Twilio Account SID", value=account_sid)
            new_auth_token = st.text_input("Twilio Auth Token", value=auth_token, type="password")
            new_phone_number = st.text_input("Número de Telefone Twilio", value=phone_number, 
                                         help="Formato: +553140025000")
            
            submit = st.form_submit_button("Salvar Configurações de SMS")
            
            if submit:
                # Save to environment variables
                os.environ['TWILIO_ACCOUNT_SID'] = new_account_sid
                os.environ['TWILIO_AUTH_TOKEN'] = new_auth_token
                os.environ['TWILIO_PHONE_NUMBER'] = new_phone_number
                
                st.success("Configurações de SMS salvas com sucesso!")
        
        # Test SMS
        st.subheader("Testar Configurações de SMS")
        with st.form("test_sms"):
            test_phone = st.text_input("Número de telefone para teste (com código do país)", 
                                   help="Exemplo: +5511912345678")
            test_submit = st.form_submit_button("Enviar SMS de Teste")
            
            if test_submit and test_phone:
                from utils import send_sms
                result = send_sms(
                    test_phone, 
                    "Teste do Sistema de Acompanhamento de Importação."
                )
                
                if result:
                    st.success("SMS de teste enviado com sucesso!")
                else:
                    st.error("Falha ao enviar SMS de teste. Verifique as configurações.")
    
    # Tab 3: General Settings
    with tab3:
        st.subheader("Configurações Gerais")
        
        # Company information
        st.info("Informações da Empresa (exibidas nos relatórios e emails)")
        
        with st.form("company_info"):
            company_name = st.text_input("Nome da Empresa", 
                                    value=st.session_state.get('company_name', ''))
            company_logo_url = st.text_input("URL do Logo da Empresa", 
                                        value=st.session_state.get('company_logo_url', ''))
            company_contact = st.text_input("Contato da Empresa", 
                                       value=st.session_state.get('company_contact', ''))
            
            submit = st.form_submit_button("Salvar Informações da Empresa")
            
            if submit:
                st.session_state.company_name = company_name
                st.session_state.company_logo_url = company_logo_url
                st.session_state.company_contact = company_contact
                
                st.success("Informações da empresa salvas com sucesso!")
        
        # Backup and Restore
        st.subheader("Backup e Restauração")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Fazer Backup dos Dados", use_container_width=True):
                import json
                import base64
                from datetime import datetime
                
                # Get data
                data = load_data()
                
                # Convert to JSON string
                json_str = json.dumps(data, indent=4)
                
                # Create download link
                b64 = base64.b64encode(json_str.encode()).decode()
                date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"backup_importacao_{date_str}.json"
                
                href = f'<a href="data:application/json;base64,{b64}" download="{filename}">Clique para baixar o arquivo de backup</a>'
                st.markdown(href, unsafe_allow_html=True)
                
                st.success("Backup gerado com sucesso!")
        
        with col2:
            uploaded_file = st.file_uploader("Restaurar a partir de Backup", type=["json"])
            
            if uploaded_file is not None:
                try:
                    import json
                    content = uploaded_file.read().decode()
                    data = json.loads(content)
                    
                    if st.button("Confirmar Restauração"):
                        # Validate data structure
                        if "processes" in data:
                            # Save the data
                            save_data(data)
                            st.session_state.data = data
                            st.success("Dados restaurados com sucesso!")
                            st.rerun()
                        else:
                            st.error("Arquivo de backup inválido!")
                except Exception as e:
                    st.error(f"Erro ao processar arquivo: {e}")