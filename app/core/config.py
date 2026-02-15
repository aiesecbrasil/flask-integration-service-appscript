"""
Configuração derivada por ambiente (produção vs não-produção).

Define domínios permitidos (CORS/origem), URLs de conexão e flags de ambiente,
com base em constantes importadas de app.config.settings.
"""

# ==============================
# Importações de Configurações
# ==============================
# Importa as constantes brutas do arquivo de configurações central (settings.py)
from ..config import (
    AMBIENTE,           # String identificadora do ambiente (ex: 'PROD', 'DEV')
    DOMINIOS_PRODUCAO,  # Lista de domínios oficiais da organização
    DOMINIOS_TESTE,     # Lista de domínios de homologação/staging
    DB_PRODUCAO,        # String de conexão com banco de dados real
    DB_TESTE,           # String de conexão com banco de dados de teste
    URL_PRODUCAO,       # URL base da API em produção
    URL_TESTE           # URL base da API em desenvolvimento
)

# ==============================
# Identificação de Ambiente
# ==============================

# Flag booleana para identificar se a execução ocorre em ambiente de Produção
IS_PRODUCTION: bool = AMBIENTE in {"PRODUCTION", "PROD"}

# Flag booleana para identificar ambientes de não-produção (Desenvolvimento/Testes)
IS_NON_PROD: bool = AMBIENTE in {"DEVELOPMENT", "DEV", "TEST", "TESTING"}

# Validação de Segurança: Impede que a aplicação suba sem um ambiente definido
if not (IS_PRODUCTION or IS_NON_PROD):
    raise ValueError(f"Ambiente inválido detectado: {AMBIENTE}")

# ==============================
# Definição de Variáveis Dinâmicas
# ==============================



# Define a lista de domínios permitidos para CORS baseada no ambiente atual.
# Adiciona o prefixo 'https://' para garantir a segurança das requisições.
if IS_PRODUCTION:
    DOMINIOS_PERMITIDOS = [f"https://{dominio}" for dominio in DOMINIOS_PRODUCAO]
else:
    DOMINIOS_PERMITIDOS = [f"https://{dominio}" for dominio in DOMINIOS_TESTE]

# Seleciona a string de conexão com o Banco de Dados correta
DB_CONNECT = DB_PRODUCAO if IS_PRODUCTION else DB_TESTE

# Seleciona a URL base para comunicações externas ou redirecionamentos
URL_CONNECT = URL_PRODUCAO if IS_PRODUCTION else URL_TESTE

# ==============================
# Exportações do Módulo
# ==============================

__all__ = [
    "DOMINIOS_PERMITIDOS", # Lista final de domínios para políticas de CORS
    "URL_CONNECT",         # URL ativa para a instância atual
    "DB_CONNECT",          # Conexão de banco ativa para o SQLAlchemy
    "IS_PRODUCTION",       # Booleano para verificações de segurança/logs
    "IS_NON_PROD"          # Booleano para habilitar ferramentas de debug
]