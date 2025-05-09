import pandas as pd
import streamlit as st
from datetime import datetime
import io
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from twilio.rest import Client

def format_date(date_str):
    """Format date string to DD/MM/YYYY"""
    if pd.isna(date_str) or date_str == "":
        return ""
    try:
        date_obj = pd.to_datetime(date_str, dayfirst=True)
        return date_obj.strftime("%d/%m/%Y")
    except:
        return date_str

def get_status_color(status):
    """Get color for status indicator"""
    status_colors = {
        "Em andamento": "orange",
        "Concluído": "green",
        "Atrasado": "red",
        "Pendente": "blue",
        "Cancelado": "gray"
    }
    return status_colors.get(status, "orange")

def export_to_excel(df):
    """Export dataframe to Excel"""
    output = io.BytesIO()
    
    # This avoids the LSP error by explicitly specifying the engine
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    df.to_excel(writer, index=False, sheet_name='Processos')
    
    # Get the xlsxwriter workbook and worksheet objects
    workbook = writer.book
    worksheet = writer.sheets['Processos']
    
    # Add some formatting
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#D7E4BC',
        'border': 1
    })
    
    # Write the column headers with the defined format
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
        
    # Set column widths
    for i, col in enumerate(df.columns):
        worksheet.set_column(i, i, 15)
    
    writer.close()
    return output.getvalue()

def export_to_csv(df):
    """Export dataframe to CSV"""
    return df.to_csv(index=False).encode('utf-8')

def get_status_from_dates(date_str, expected_date_str):
    """Determine status based on dates"""
    if pd.isna(date_str) or date_str == "":
        return "Pendente"
    
    try:
        date = pd.to_datetime(date_str)
        today = pd.to_datetime(datetime.now().date())
        
        if date < today:
            return "Concluído"
        
        if expected_date_str and pd.to_datetime(expected_date_str) < today:
            return "Atrasado"
            
        return "Em andamento"
    except:
        return "Pendente"

def send_email(to_email, subject, message):
    """Send an email using SMTP"""
    # Note: For this to work, you need to set SMTP configuration
    # For Gmail, you might need an app-specific password
    try:
        # Try to get configurations from session state or environment variables
        smtp_server = st.session_state.get('smtp_server', os.environ.get('SMTP_SERVER', ''))
        smtp_port = int(st.session_state.get('smtp_port', os.environ.get('SMTP_PORT', 587)))
        smtp_username = st.session_state.get('smtp_username', os.environ.get('SMTP_USERNAME', ''))
        smtp_password = st.session_state.get('smtp_password', os.environ.get('SMTP_PASSWORD', ''))
        from_email = st.session_state.get('from_email', os.environ.get('FROM_EMAIL', smtp_username))
        
        # If configuration is incomplete, show a configuration form
        if not smtp_server or not smtp_username or not smtp_password:
            st.warning("Configuração de email incompleta. Configure nas configurações.")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        
        # Connect to server and send
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        st.error(f"Erro ao enviar email: {e}")
        return False

def send_sms(to_phone, message):
    """Send SMS via Twilio"""
    try:
        # Get Twilio credentials
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        from_phone = os.environ.get('TWILIO_PHONE_NUMBER')
        
        # Check if credentials are available
        if not account_sid or not auth_token or not from_phone:
            st.warning("Configuração do Twilio incompleta. Configure nas configurações.")
            return False
        
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Send message
        message = client.messages.create(
            body=message,
            from_=from_phone,
            to=to_phone
        )
        
        return True
    except Exception as e:
        st.error(f"Erro ao enviar SMS: {e}")
        return False
