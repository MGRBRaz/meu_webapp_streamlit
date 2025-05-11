# Guia Simplificado de Instalação na Hostinger (Docker)

Este é um guia passo a passo simplificado para instalar o JGR Broker Import na Hostinger usando Docker.

## Preparação dos Arquivos (No seu computador)

1. **Crie uma pasta** chamada `jgr_deploy`

2. **Copie os seguintes arquivos e pastas** para a pasta `jgr_deploy`:
   - Todos os arquivos `.py` do projeto
   - Pasta `components`
   - Pasta `assets`
   - Pasta `.streamlit`
   - Arquivos `data.json` e `users.json`
   - Arquivos `Dockerfile` e `docker-compose.yml` (criados anteriormente)
   - Arquivo `required_packages.txt`

3. **Compacte a pasta** `jgr_deploy` em um arquivo ZIP

## Instalação (Na Hostinger)

1. **Acesse o painel da Hostinger** e navegue até seu servidor Docker

2. **Acesse o gerenciador de arquivos**:
   - Vá para "File Manager" ou similar no painel da Hostinger
   - Navegue até a pasta raiz (geralmente `/public_html`)

3. **Faça upload do ZIP**:
   - Selecione "Upload" e escolha o arquivo ZIP criado
   - Depois de concluído, extraia o ZIP no servidor

4. **Acesse o Terminal** (clique no botão "Terminal do navegador" no canto superior direito)

5. **Execute os comandos**:
   ```bash
   # Vá para a pasta onde os arquivos foram extraídos
   cd /public_html
   
   # Renomeie o arquivo de requisitos
   mv required_packages.txt requirements.txt
   
   # Construa e inicie o contêiner Docker
   docker-compose build
   docker-compose up -d
   ```

6. **Verifique se está funcionando**:
   ```bash
   # Veja se o contêiner está rodando
   docker ps
   
   # Veja os logs em caso de problemas
   docker-compose logs
   ```

7. **Configure o acesso**:
   - No painel da Hostinger, vá para "Regras do Firewall"
   - Adicione regra para permitir tráfego na porta 8501
   - Acesse sua aplicação em: `http://seu_dominio.com:8501`

## Solução Rápida de Problemas

- **App não inicia**: Verifique logs com `docker-compose logs`
- **Problemas de permissão**: Execute `chmod 666 data.json users.json`
- **Não consegue acessar via navegador**: Verifique se porta 8501 está aberta no firewall

## Comandos Úteis

- **Ver logs**: `docker-compose logs -f`
- **Reiniciar app**: `docker-compose restart`
- **Parar app**: `docker-compose down`
- **Atualizar após mudanças**: 
  ```bash
  docker-compose down
  docker-compose build
  docker-compose up -d
  ```

## Dicas Extras

- Faça backup regular dos arquivos `data.json` e `users.json`
- Para atualizar a aplicação, substitua apenas os arquivos alterados e reinicie o contêiner
- Use o comando `docker-compose down && docker-compose up -d` para reiniciar completamente