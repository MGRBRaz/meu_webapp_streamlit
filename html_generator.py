"""
Gerador de HTML para exportar processos
"""
import os
import base64
from datetime import datetime
from data import get_process_by_id, get_processes_df
from utils import format_date, get_status_color

HTML_EXPORTS_DIR = "html_exports"


def generate_process_html(process_id, include_details=True):
    """
    Gera um arquivo HTML contendo as informações do processo especificado.
    
    Args:
        process_id: ID do processo
        include_details: Se True, inclui a seção de detalhes
        
    Returns:
        tuple: (caminho do arquivo gerado, URL relativo)
    """
    process = get_process_by_id(process_id)
    if not process:
        return None, None
    
    # Criar diretório de exportação se não existir
    if not os.path.exists(HTML_EXPORTS_DIR):
        os.makedirs(HTML_EXPORTS_DIR)
        
    # Nome do arquivo
    filename = f"processo_{process_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = os.path.join(HTML_EXPORTS_DIR, filename)
    
    # Status
    status = process.get('status', 'Em andamento')
    status_color = get_status_color(status)
    
    # Criar HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Processo de Importação - {process_id}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                color: #333;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: #fff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 5px;
            }}
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                border-bottom: 1px solid #eee;
                padding-bottom: 10px;
            }}
            .status-badge {{
                background-color: {status_color};
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                font-weight: bold;
                display: inline-block;
            }}
            .section {{
                margin-bottom: 30px;
                padding: 15px;
                background: #f9f9f9;
                border-radius: 5px;
                border-left: 4px solid #2c3e50;
            }}
            .section-title {{
                margin-top: 0;
                color: #2c3e50;
                font-size: 1.2em;
            }}
            .grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 15px;
            }}
            .grid-item {{
                margin-bottom: 10px;
            }}
            .label {{
                font-weight: bold;
                font-size: 0.9em;
                color: #555;
                margin-bottom: 5px;
            }}
            .value {{
                background: #f5f5f5;
                padding: 8px;
                border-radius: 4px;
                font-size: 0.95em;
            }}
            .logo {{
                width: 150px;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                font-size: 0.8em;
                color: #777;
                border-top: 1px solid #eee;
                padding-top: 10px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }}
            table th, table td {{
                padding: 8px 10px;
                text-align: left;
                border-bottom: 1px solid #eee;
            }}
            table th {{
                background: #f5f5f5;
                font-weight: bold;
            }}
            @media print {{
                body {{
                    padding: 0;
                    font-size: 12pt;
                }}
                .container {{
                    box-shadow: none;
                    max-width: 100%;
                }}
                .section {{
                    page-break-inside: avoid;
                }}
                .no-print {{
                    display: none;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div>
                    <h1>Processo de Importação - {process_id}</h1>
                    <p>Referência: {process.get('ref', '')}</p>
                </div>
                <div>
                    <div class="status-badge">{status}</div>
                </div>
            </div>
    """
    
    # Seção de Informações Gerais
    html += f"""
            <div class="section">
                <h2 class="section-title">Informações Gerais</h2>
                <div class="grid">
                    <div class="grid-item">
                        <div class="label">Código</div>
                        <div class="value">{process.get('id', '')}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Referência</div>
                        <div class="value">{process.get('ref', '')}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">PO</div>
                        <div class="value">{process.get('po', '')}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Invoice</div>
                        <div class="value">{process.get('invoice', '')}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Origem</div>
                        <div class="value">{process.get('origin', '')}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Produto</div>
                        <div class="value">{process.get('product', '')}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Tipo</div>
                        <div class="value">{process.get('type', '')}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">ETA</div>
                        <div class="value">{format_date(process.get('eta', ''))}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Status</div>
                        <div class="value">{process.get('status', '')}</div>
                    </div>
                </div>
            </div>
    """
    
    # Seção de Embarque
    html += f"""
            <div class="section">
                <h2 class="section-title">Informações de Embarque</h2>
                <div class="grid">
                    <div class="grid-item">
                        <div class="label">Exportador</div>
                        <div class="value">{process.get('exporter', '')}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Navio</div>
                        <div class="value">{process.get('ship', '')}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Agente</div>
                        <div class="value">{process.get('agent', '')}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Número B/L</div>
                        <div class="value">{process.get('bl_number', '')}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Container</div>
                        <div class="value">{process.get('container', '')}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Previsão de Chegada</div>
                        <div class="value">{format_date(process.get('arrival_date', ''))}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Free Time</div>
                        <div class="value">{process.get('free_time', '')} dias</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Vencimento Free Time</div>
                        <div class="value">{format_date(process.get('free_time_expiry', ''))}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Devolução de Vazio</div>
                        <div class="value">{format_date(process.get('empty_return', ''))}</div>
                    </div>
                </div>
            </div>
    """
    
    # Seção de Armazenagem
    html += f"""
            <div class="section">
                <h2 class="section-title">Informações de Armazenagem</h2>
                <div class="grid">
                    <div class="grid-item">
                        <div class="label">Terminal</div>
                        <div class="value">{process.get('terminal', '')}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Entrada no Porto/Recinto</div>
                        <div class="value">{format_date(process.get('port_entry_date', ''))}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Início do Período Atual</div>
                        <div class="value">{format_date(process.get('current_period_start', ''))}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Vencimento do Período</div>
                        <div class="value">{format_date(process.get('current_period_expiry', ''))}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Dias Armazenados</div>
                        <div class="value">{process.get('storage_days', '0')}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Mapa</div>
                        <div class="value">{process.get('map', '')}</div>
                    </div>
                </div>
            </div>
    """
    
    # Seção de Documentos
    html += f"""
            <div class="section">
                <h2 class="section-title">Documentos e Informações Adicionais</h2>
                <div class="grid">
                    <div class="grid-item">
                        <div class="label">Nota Fiscal</div>
                        <div class="value">{process.get('invoice_number', '')}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">D.I.</div>
                        <div class="value">{process.get('di', '')}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Documentos Originais</div>
                        <div class="value">{process.get('original_docs', '')}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Data de Devolução</div>
                        <div class="value">{format_date(process.get('return_date', ''))}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">Última Atualização</div>
                        <div class="value">{format_date(process.get('last_update', ''))}</div>
                    </div>
                </div>
            </div>
    """
    
    if include_details:
        # Seção de Observações
        html += f"""
                <div class="section">
                    <h2 class="section-title">Observações</h2>
                    <div class="value" style="min-height: 60px;">
                        {process.get('observations', '')}
                    </div>
                </div>
        """
        
        # Seção de Eventos
        if 'events' in process and process['events']:
            html += """
                <div class="section">
                    <h2 class="section-title">Histórico de Eventos</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Data</th>
                                <th>Descrição</th>
                                <th>Usuário</th>
                            </tr>
                        </thead>
                        <tbody>
            """
            
            for event in process['events']:
                # Filtrar eventos de atribuição
                if not "atribuído" in event.get('description', '').lower():
                    html += f"""
                            <tr>
                                <td>{event.get('date', '')}</td>
                                <td>{event.get('description', '')}</td>
                                <td>{event.get('user', '')}</td>
                            </tr>
                    """
            
            html += """
                        </tbody>
                    </table>
                </div>
            """
    
    # Rodapé
    current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    html += f"""
            <div class="footer">
                <p>Documento gerado em {current_date} | JGR Broker</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Salvar arquivo
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return filepath, filename


def generate_processes_table_html(filtered_df=None, process_ids=None, include_details=True, client_filter=None, client_name=None):
    """
    Gera um arquivo HTML contendo uma tabela de processos com funcionalidade de expansão de detalhes.
    
    Args:
        filtered_df: DataFrame com os processos filtrados (opcional)
        process_ids: Lista de IDs de processos para incluir (opcional)
        include_details: Se True, inclui a seção de detalhes
        client_filter: ID do cliente para filtrar processos (opcional)
        client_name: Nome do cliente para personalizar o relatório (opcional)
        
    Returns:
        tuple: (caminho do arquivo gerado, URL relativo)
    """
    # Obter dados
    if filtered_df is None:
        filtered_df = get_processes_df()
    
    # Filtrar por IDs específicos (para visualização de cliente)
    if process_ids is not None:
        filtered_df = filtered_df[filtered_df['id'].isin(process_ids)]
    
    # Filtrar por cliente (novo)
    if client_filter:
        from components.auth import get_users
        users = get_users()
        
        # Encontrar o cliente pelo ID
        client = next((u for u in users if u['id'] == client_filter), None)
        
        if client and 'processes' in client and client['processes']:
            # Filtrar processos pelo cliente selecionado
            filtered_df = filtered_df[filtered_df['id'].isin(client['processes'])]
    
    # Verificar se há dados
    if filtered_df.empty:
        return None, None
    
    # Criar diretório de exportação se não existir
    if not os.path.exists(HTML_EXPORTS_DIR):
        os.makedirs(HTML_EXPORTS_DIR)
    
    # Nome do arquivo
    client_suffix = ""
    if client_name:
        client_suffix = f"_cliente_{client_name.replace(' ', '_')}"
    elif client_filter:
        client_suffix = f"_cliente_{client_filter}"
        
    filename = f"processos{client_suffix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = os.path.join(HTML_EXPORTS_DIR, filename)
    
    # Título personalizado com nome do cliente, se fornecido
    title = "Processos de Importação e Exportação - JGR Broker"
    if client_name:
        title = f"Processos de Importação e Exportação - Cliente: {client_name} - JGR Broker"
    
    # Criar HTML com estilos e scripts
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                color: #333;
            }}
            .container {{
                max-width: 100%;
                margin: 0 auto;
                padding: 20px;
                background: #fff;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 5px;
            }}
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                border-bottom: 1px solid #eee;
                padding-bottom: 10px;
            }}
            .filter-container {{
                margin: 20px 0;
                padding: 15px;
                background: #f9f9f9;
                border-radius: 5px;
                display: flex;
                align-items: center;
            }}
            .filter-input {{
                padding: 8px 12px;
                border: 1px solid #ddd;
                border-radius: 4px;
                margin-right: 10px;
                width: 300px;
            }}
            .filter-label {{
                margin-right: 10px;
                font-weight: bold;
            }}
            .status-badge {{
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                font-weight: bold;
                display: inline-block;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }}
            table th, table td {{
                padding: 8px 10px;
                text-align: left;
                border-bottom: 1px solid #eee;
            }}
            table th {{
                background: #f5f5f5;
                font-weight: bold;
                cursor: pointer;
            }}
            .process-row {{
                cursor: pointer;
            }}
            .process-row:hover {{
                background-color: #f5f5f5;
            }}
            .details-row {{
                display: none;
            }}
            .details-container {{
                padding: 15px;
                background: #f9f9f9;
                border-radius: 5px;
                margin: 10px 0;
            }}
            .tab-container {{
                overflow: hidden;
                border: 1px solid #ccc;
                background-color: #f1f1f1;
                border-radius: 5px 5px 0 0;
            }}
            .tab {{
                background-color: inherit;
                float: left;
                border: none;
                outline: none;
                cursor: pointer;
                padding: 10px 16px;
                transition: 0.3s;
                font-size: 14px;
            }}
            .tab:hover {{
                background-color: #ddd;
            }}
            .tab.active {{
                background-color: #2c3e50;
                color: white;
            }}
            .tabcontent {{
                display: none;
                padding: 15px;
                border: 1px solid #ccc;
                border-top: none;
                border-radius: 0 0 5px 5px;
            }}
            .details-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 15px;
            }}
            .details-item {{
                margin-bottom: 10px;
            }}
            .details-label {{
                font-weight: bold;
                font-size: 0.9em;
                color: #555;
                margin-bottom: 5px;
            }}
            .details-value {{
                background: #f5f5f5;
                padding: 8px;
                border-radius: 4px;
                font-size: 0.95em;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                font-size: 0.8em;
                color: #777;
                border-top: 1px solid #eee;
                padding-top: 10px;
            }}
            @media print {{
                body {{
                    padding: 0;
                    font-size: 11pt;
                }}
                .container {{
                    box-shadow: none;
                    max-width: 100%;
                    padding: 0;
                }}
                .filter-container, .no-print {{
                    display: none !important;
                }}
                .details-row {{
                    display: table-row;
                }}
                .details-container {{
                    page-break-inside: avoid;
                }}
                .tabcontent {{
                    display: block !important;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                {f'<h1>Processos de Importação e Exportação - Cliente: {client_name} - JGR Broker</h1>' if client_name else '<h1>Processos de Importação e Exportação - JGR Broker</h1>'}
                <div style="display: flex; justify-content: space-between; color: #777; font-size: 0.9em;">
                    <p>Relatório gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}</p>
                    <p>Total de processos: {len(filtered_df)}</p>
                </div>
            </div>
            
            <div class="filter-container no-print">
                <span class="filter-label">Buscar:</span>
                <input type="text" id="filterInput" class="filter-input" placeholder="Digite para filtrar (ID, Referência, PO, etc.)">
                
                <span class="filter-label" style="margin-left: 20px;">Tipo de Processo:</span>
                <select id="processTypeFilter" class="filter-input">
                    <option value="todos">Todos</option>
                    <option value="importacao">Importação</option>
                    <option value="exportacao">Exportação</option>
                </select>
            </div>
            
            <table id="processesTable">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Status</th>
                        <th>Tipo</th>
                        <th>Referência</th>
                        <th>PO</th>
                        <th>Origem</th>
                        <th>Produto</th>
                        <th>ETA</th>
                        <th>Free Time</th>
                        <th>Vencimento Free Time</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # Adicionar cada processo como uma linha da tabela
    process_details_html = ""
    
    for _, row in filtered_df.iterrows():
        process_id = row['id']
        status = row.get('status', '')
        status_color = get_status_color(status)
        
        # Linha principal com dados básicos
        html += f"""
                    <tr class="process-row" data-id="{process_id}" data-type="{row.get('type', '')}" onclick="toggleDetails('{process_id}')">
                        <td>{process_id}</td>
                        <td><div class="status-badge" style="background-color: {status_color}">{status}</div></td>
                        <td>{"Exportação" if row.get('type', '') == "exportacao" else "Importação"}</td>
                        <td>{row.get('ref', '')}</td>
                        <td>{row.get('po', '')}</td>
                        <td>{row.get('origin', '')}</td>
                        <td>{row.get('product', '')}</td>
                        <td>{format_date(row.get('eta', ''))}</td>
                        <td>{row.get('free_time', '')}</td>
                        <td>{format_date(row.get('free_time_expiry', ''))}</td>
                    </tr>
        """
        
        # Obter detalhes completos do processo
        process = get_process_by_id(process_id)
        if not process:
            continue
            
        # Adicionar linha de detalhes expandível
        process_details_html += f"""
                    <tr class="details-row" id="details-{process_id}">
                        <td colspan="10">
                            <div class="details-container">
                                <div class="tab-container no-print">
                                    <button class="tab active" onclick="openTab(event, '{process_id}-info')">Informações Gerais</button>
                                    <button class="tab" onclick="openTab(event, '{process_id}-transport')">Transporte</button>
                                    <button class="tab" onclick="openTab(event, '{process_id}-dates')">Datas</button>
                                    <button class="tab" onclick="openTab(event, '{process_id}-storage')">Armazenagem</button>
                                    <button class="tab" onclick="openTab(event, '{process_id}-docs')">Documentos</button>
                                    <button class="tab" onclick="openTab(event, '{process_id}-events')">Eventos</button>
                                </div>
                                
                                <div id="{process_id}-info" class="tabcontent" style="display: block;">
                                    <h3>Informações Gerais</h3>
                                    <div class="details-grid">
                                        <div class="details-item">
                                            <div class="details-label">Código</div>
                                            <div class="details-value">{process.get('id', '')}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Referência</div>
                                            <div class="details-value">{process.get('ref', '')}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">PO</div>
                                            <div class="details-value">{process.get('po', '')}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Invoice</div>
                                            <div class="details-value">{process.get('invoice', '')}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Origem</div>
                                            <div class="details-value">{process.get('origin', '')}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Produto</div>
                                            <div class="details-value">{process.get('product', '')}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Tipo</div>
                                            <div class="details-value">{"Exportação" if process.get('type', '') == "exportacao" else "Importação"}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">ETA</div>
                                            <div class="details-value">{format_date(process.get('eta', ''))}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Status</div>
                                            <div class="details-value">{process.get('status', '')}</div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div id="{process_id}-transport" class="tabcontent">
                                    <h3>Transporte</h3>
                                    <div class="details-grid">
                                        <div class="details-item">
                                            <div class="details-label">Exportador</div>
                                            <div class="details-value">{process.get('exporter', '')}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Navio</div>
                                            <div class="details-value">{process.get('ship', '')}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Agente</div>
                                            <div class="details-value">{process.get('agent', '')}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Número B/L</div>
                                            <div class="details-value">{process.get('bl_number', '')}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Container</div>
                                            <div class="details-value">{process.get('container', '')}</div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div id="{process_id}-dates" class="tabcontent">
                                    <h3>Datas</h3>
                                    <div class="details-grid">
                                        <div class="details-item">
                                            <div class="details-label">ETA</div>
                                            <div class="details-value">{format_date(process.get('eta', ''))}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Previsão de Chegada</div>
                                            <div class="details-value">{format_date(process.get('arrival_date', ''))}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Free Time</div>
                                            <div class="details-value">{process.get('free_time', '')} dias</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Vencimento Free Time</div>
                                            <div class="details-value">{format_date(process.get('free_time_expiry', ''))}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Devolução de Vazio</div>
                                            <div class="details-value">{format_date(process.get('empty_return', ''))}</div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div id="{process_id}-storage" class="tabcontent">
                                    <h3>Armazenagem</h3>
                                    <div class="details-grid">
                                        <div class="details-item">
                                            <div class="details-label">Terminal</div>
                                            <div class="details-value">{process.get('terminal', '')}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Entrada no Porto/Recinto</div>
                                            <div class="details-value">{format_date(process.get('port_entry_date', ''))}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Início do Período Atual</div>
                                            <div class="details-value">{format_date(process.get('current_period_start', ''))}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Vencimento do Período</div>
                                            <div class="details-value">{format_date(process.get('current_period_expiry', ''))}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Dias Armazenados</div>
                                            <div class="details-value">{process.get('storage_days', '0')}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Mapa</div>
                                            <div class="details-value">{process.get('map', '')}</div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div id="{process_id}-docs" class="tabcontent">
                                    <h3>Documentos</h3>
                                    <div class="details-grid">
                                        <div class="details-item">
                                            <div class="details-label">Nota Fiscal</div>
                                            <div class="details-value">{process.get('invoice_number', '')}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">D.I.</div>
                                            <div class="details-value">{process.get('di', '')}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Documentos Originais</div>
                                            <div class="details-value">{process.get('original_docs', '')}</div>
                                        </div>
                                        <div class="details-item">
                                            <div class="details-label">Data de Devolução</div>
                                            <div class="details-value">{format_date(process.get('return_date', ''))}</div>
                                        </div>
                                    </div>
                                </div>
        """
        
        if include_details and 'events' in process and process['events']:
            process_details_html += f"""
                                <div id="{process_id}-events" class="tabcontent">
                                    <h3>Histórico de Eventos</h3>
                                    <table>
                                        <thead>
                                            <tr>
                                                <th>Data</th>
                                                <th>Descrição</th>
                                                <th>Usuário</th>
                                            </tr>
                                        </thead>
                                        <tbody>
            """
            
            for event in process['events']:
                # Filtrar eventos de atribuição
                if not "atribuído" in event.get('description', '').lower():
                    process_details_html += f"""
                                            <tr>
                                                <td>{event.get('date', '')}</td>
                                                <td>{event.get('description', '')}</td>
                                                <td>{event.get('user', '')}</td>
                                            </tr>
                    """
            
            process_details_html += """
                                        </tbody>
                                    </table>
                                </div>
            """
        else:
            process_details_html += f"""
                                <div id="{process_id}-events" class="tabcontent">
                                    <h3>Histórico de Eventos</h3>
                                    <p>Sem eventos registrados para este processo.</p>
                                </div>
            """
            
        process_details_html += """
                            </div>
                        </td>
                    </tr>
        """
    
    # Adicionar detalhes de processos ao HTML
    html += process_details_html
    
    # Adicionar scripts e rodapé
    html += """
                </tbody>
            </table>
            
            <div class="footer">
                <p>© 2025 JGR BROKER - Todos os direitos reservados</p>
            </div>
        </div>
        
        <script>
            // Filtro de tabela
            document.getElementById('filterInput').addEventListener('keyup', function() {
                filterTable();
            });
            
            document.getElementById('processTypeFilter').addEventListener('change', function() {
                filterTable();
            });
            
            function filterTable() {
                const filterValue = document.getElementById('filterInput').value.toLowerCase();
                const typeFilter = document.getElementById('processTypeFilter').value;
                const table = document.getElementById('processesTable');
                const rows = table.getElementsByClassName('process-row');
                
                for (let i = 0; i < rows.length; i++) {
                    const row = rows[i];
                    const cells = row.getElementsByTagName('td');
                    const processType = row.getAttribute('data-type') || '';
                    let matchesText = false;
                    
                    // Verificar se corresponde ao texto de busca
                    for (let j = 0; j < cells.length; j++) {
                        const cell = cells[j];
                        if (cell.textContent.toLowerCase().indexOf(filterValue) > -1) {
                            matchesText = true;
                            break;
                        }
                    }
                    
                    // Verificar se corresponde ao tipo de processo
                    let matchesType = true;
                    if (typeFilter !== 'todos') {
                        matchesType = (processType === typeFilter);
                        
                        // Processos de importação podem não ter o tipo definido (legado)
                        if (typeFilter === 'importacao' && processType === '') {
                            matchesType = true;
                        }
                    }
                    
                    // Mostrar apenas se corresponder a ambos os filtros
                    if (matchesText && matchesType) {
                        row.style.display = '';
                    } else {
                        row.style.display = 'none';
                        // Esconder também a linha de detalhes
                        const processId = row.getAttribute('data-id');
                        const detailsRow = document.getElementById('details-' + processId);
                        if (detailsRow) {
                            detailsRow.style.display = 'none';
                        }
                    }
                }
            }
            
            // Variável para rastrear o processo atualmente aberto
            let currentOpenProcess = null;
            
            // Expandir/colapsar detalhes
            function toggleDetails(processId) {
                const detailsRow = document.getElementById('details-' + processId);
                
                // Se o processo já está aberto, apenas fecha
                if (detailsRow.style.display === 'table-row') {
                    detailsRow.style.display = 'none';
                    currentOpenProcess = null;
                } else {
                    // Fecha o processo atualmente aberto (se houver)
                    if (currentOpenProcess !== null && currentOpenProcess !== processId) {
                        const currentOpenRow = document.getElementById('details-' + currentOpenProcess);
                        if (currentOpenRow) {
                            currentOpenRow.style.display = 'none';
                        }
                    }
                    
                    // Abre o novo processo
                    detailsRow.style.display = 'table-row';
                    currentOpenProcess = processId;
                }
            }
            
            // Trocar abas
            function openTab(evt, tabId) {
                // Obter o ID do processo (primeira parte do ID da aba)
                const processId = tabId.split('-')[0];
                
                // Esconder todas as abas de conteúdo deste processo
                const tabcontent = document.getElementsByClassName('tabcontent');
                for (let i = 0; i < tabcontent.length; i++) {
                    if (tabcontent[i].id.startsWith(processId)) {
                        tabcontent[i].style.display = 'none';
                    }
                }
                
                // Remover classe "active" de todas as abas deste processo
                const tablinks = evt.currentTarget.parentNode.getElementsByClassName('tab');
                for (let i = 0; i < tablinks.length; i++) {
                    tablinks[i].className = tablinks[i].className.replace(' active', '');
                }
                
                // Mostrar a aba selecionada
                document.getElementById(tabId).style.display = 'block';
                evt.currentTarget.className += ' active';
            }
            
            // Ordenação da tabela
            document.querySelectorAll('#processesTable th').forEach((header, index) => {
                header.addEventListener('click', () => {
                    const table = document.getElementById('processesTable');
                    const rows = Array.from(table.querySelectorAll('tr.process-row'));
                    const detailsRows = {};
                    
                    // Salvar as linhas de detalhes
                    rows.forEach(row => {
                        const processId = row.getAttribute('data-id');
                        const detailsRow = document.getElementById('details-' + processId);
                        if (detailsRow) {
                            detailsRows[processId] = detailsRow;
                        }
                    });
                    
                    // Ordenar as linhas
                    const sortedRows = rows.sort((a, b) => {
                        const aValue = a.cells[index].textContent.trim();
                        const bValue = b.cells[index].textContent.trim();
                        return aValue.localeCompare(bValue, 'pt-BR');
                    });
                    
                    // Remover todas as linhas
                    rows.forEach(row => {
                        const processId = row.getAttribute('data-id');
                        const detailsRow = document.getElementById('details-' + processId);
                        if (detailsRow) {
                            detailsRow.remove();
                        }
                        row.remove();
                    });
                    
                    // Re-adicionar linhas ordenadas
                    const tbody = table.querySelector('tbody');
                    sortedRows.forEach(row => {
                        tbody.appendChild(row);
                        const processId = row.getAttribute('data-id');
                        if (detailsRows[processId]) {
                            tbody.appendChild(detailsRows[processId]);
                        }
                    });
                });
            });
        </script>
    </body>
    </html>
    """
    
    # Salvar arquivo
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return filepath, filename


def get_download_link(filepath, filename):
    """
    Cria um link para download do arquivo HTML gerado.
    
    Args:
        filepath: Caminho completo do arquivo
        filename: Nome do arquivo para exibição
        
    Returns:
        str: HTML com link para download
    """
    # Ler o conteúdo do arquivo HTML
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Aqui criamos um link para download do conteúdo
    html_bytes = html_content.encode('utf-8')
    import base64
    b64 = base64.b64encode(html_bytes).decode('utf-8')
    href = f'data:text/html;base64,{b64}'
    
    return href, filename