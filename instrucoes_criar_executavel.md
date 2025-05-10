# Instruções para Criar o Executável do JGR Broker Importação

Este documento apresenta o passo a passo para gerar um executável do sistema JGR Broker Importação que pode ser usado em qualquer computador Windows sem necessidade de instalação de Python ou outras dependências.

> **IMPORTANTE:** Esta etapa deve ser realizada em um computador Windows com Python instalado corretamente. O executável resultante poderá então ser distribuído para outros computadores sem Python.

## Pré-requisitos

Para gerar o executável, você precisará de:

1. Python instalado no computador onde será criado o executável (não é necessário no computador final onde será usado)
2. Conexão à internet para download das dependências

## Passo a Passo

### 1. Instalar Dependências

Abra um prompt de comando (cmd) ou PowerShell e execute:

```
pip install pyinstaller pandas streamlit xlsxwriter twilio
```

### 2. Gerar o Executável

1. Navegue até a pasta onde estão os arquivos do projeto
2. Execute o script `create_exe.py` com o comando:

```
python create_exe.py
```

3. Aguarde a conclusão do processo. Isso pode levar alguns minutos.
4. Ao finalizar, uma pasta `dist` será criada contendo todos os arquivos necessários.

### 3. Distribuir o Executável

Para distribuir o sistema para uso em outros computadores:

1. Copie toda a pasta `dist` para um pen drive ou outro meio de transferência
2. No computador de destino, copie a pasta para o local desejado (por exemplo, na área de trabalho ou em "Meus Documentos")
3. O usuário final não precisa instalar nada, basta executar o arquivo `JGRBrokerImportacao.exe` ou usar o `iniciar_jgr.bat` que está dentro da pasta

### 4. Uso do Sistema

Para iniciar o sistema:

1. Execute o arquivo `JGRBrokerImportacao.exe` ou `iniciar_jgr.bat`
2. Automaticamente será aberto um navegador com o sistema
3. Faça login com as credenciais:
   - Usuário: `admin`
   - Senha: `admin`

### 5. Importante

- Todos os dados são armazenados localmente nos arquivos JSON dentro da pasta
- Para fazer backup dos dados, copie os arquivos `data.json`, `users.json` e `shared_links.json`
- Se precisar restaurar um backup, substitua esses arquivos pelos arquivos de backup

### 6. Solução de Problemas

Se o navegador não abrir automaticamente, aguarde cerca de 10 segundos após executar o arquivo `.bat` e acesse manualmente o endereço http://localhost:5000 em qualquer navegador.

---

Caso tenha dúvidas ou precise de suporte adicional, entre em contato com a equipe técnica.