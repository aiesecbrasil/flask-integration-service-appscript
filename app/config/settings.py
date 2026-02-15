"""
config.settings
---------------

Configuração central da aplicação.
Responsável por carregar, validar e tipar variáveis de ambiente.

Este módulo segue o princípio de imutabilidade de configuração e
garante a segurança operacional do sistema.
"""

# ==============================
# Importações (Dependencies)
# ==============================
# Importamos do nosso pacote 'globals.std' para manter a consistência de tipos e módulos
from ..globals.std import os, List

# ================================
# FUNÇÃO AUXILIAR DE VALIDAÇÃO
# ================================

def get_env_or_fail(var_name: str) -> str:
    """
    Recupera uma variável de ambiente obrigatória do S.O.

    Args:
        var_name (str): Nome da chave (ex: 'DB_PRODUCAO').

    Returns:
        str: Valor limpo (sem espaços em branco).

    Raises:
        ValueError: Interrompe a execução se a variável estiver ausente ou vazia.
    """
    valor = os.getenv(var_name, "").strip()
    if not valor:
        raise ValueError(f"CRITICAL ERROR: Variável de ambiente '{var_name}' não está definida!")
    return valor


# ================================
# AMBIENTE E SEGURANÇA
# ================================

# Define o contexto de execução: 'PRODUCTION', 'DEVELOPMENT' ou 'TEST'
AMBIENTE: str = get_env_or_fail("AMBIENTE").upper()

# Lista de chaves de API autorizadas para consumir os endpoints protegidos
API_KEYS_PERMITIDAS: List[str] = [
    k.strip() for k in get_env_or_fail("API_KEYS_PERMITIDAS").split(",")
]

# ================================
# POLÍTICAS DE DOMÍNIO (CORS)
# ================================
# Domínios oficiais da AIESEC para produção
DOMINIOS_PRODUCAO: List[str] = get_env_or_fail("DOMINIOS_PRODUCAO").split(",")

# Domínios de homologação e staging para testes
DOMINIOS_TESTE: List[str] = get_env_or_fail("DOMINIOS_TESTE").split(",")


# ===============================
# INFRAESTRUTURA (DB E URL)
# ===============================
# Strings de conexão SQLAlchemy (ex: postgresql://user:pass@host:port/db)
DB_PRODUCAO = get_env_or_fail("DB_PRODUCAO")
DB_TESTE = get_env_or_fail("DB_TESTE")

# URLs base para identificação e redirecionamentos
URL_PRODUCAO = get_env_or_fail("URL_PRODUCAO")
URL_TESTE = get_env_or_fail("URL_TESTE")


# ================================
# INTEGRAÇÕES GOOGLE APPS SCRIPT
# ================================
# Endpoints legados ou utilitários para busca e inserção via Google Sheets/Email
APPSCRIPT_BUSCAR = get_env_or_fail("APPSCRIPT_BUSCAR")
APPSCRIPT_INSERIR = get_env_or_fail("APPSCRIPT_INSERIR")
APPSCRIPT_METADADOS = get_env_or_fail("APPSCRIPT_METADADOS_CARD_OGX")
APPSCRIPT_ADICIONAR_CARD = get_env_or_fail("APPSCRIPT_ADICIONAR_CARD_OGX")
ID_APPSCRIPT_EMAIL_LEADS_PSEL = get_env_or_fail("ID_APPSCRIPT_EMAIL_LEADS_PSEL")

# ================================
# ACESSO EXTERNO E PERFORMANCE
# ================================
# Link para a plataforma de teste psicométrico
URL_FIT_CULTURAL = get_env_or_fail("URL_FIT_CULTURAL")

# Tempo de vida do cache em segundos (ex: 3600 para 1 hora)
CACHE_TTL: int = int(get_env_or_fail("CACHE_TTL"))


# ================================
# CREDENCIAIS PODIO - Novos Leads B2C(OGX) E PROCESSO SELETIVO(PSEL)
# ================================
# Configurações de API para os diferentes Workspaces da AIESEC no Podio
CLIENT_ID_OGX = get_env_or_fail("CLIENT_ID_OGX")
CLIENT_SECRET_OGX = get_env_or_fail("CLIENT_SECRET_OGX")
APP_ID_OGX = get_env_or_fail("APP_ID_OGX")
APP_TOKEN_OGX = get_env_or_fail("APP_TOKEN_OGX")

CLIENT_ID_PSEL = get_env_or_fail("CLIENT_ID_PSEL")
CLIENT_SECRET_PSEL = get_env_or_fail("CLIENT_SECRET_PSEL")
APP_ID_PSEL = get_env_or_fail("APP_ID_PSEL")
APP_TOKEN_PSEL = get_env_or_fail("APP_TOKEN_PSEL")

# ================================
# INTEGRAÇÃO GLOBAL (EXPA)
# ================================
# Token de acesso à API oficial da AIESEC International (GIS)
TOKEN_EXPA = get_env_or_fail("TOKEN_EXPA")

# ================================
# EXPORTAÇÃO PÚBLICA (INTERFACE)
# ================================



__all__ = [
    "AMBIENTE",
    "DOMINIOS_PRODUCAO",
    "DOMINIOS_TESTE",
    "DB_PRODUCAO",
    "DB_TESTE",
    "URL_PRODUCAO",
    "URL_TESTE",
    "API_KEYS_PERMITIDAS",
    "CACHE_TTL",
    "CLIENT_ID_PSEL",
    "CLIENT_SECRET_OGX",
    "CLIENT_ID_OGX",
    "CLIENT_SECRET_PSEL",
    "APP_ID_OGX",
    "APP_TOKEN_OGX",
    "APP_ID_PSEL",
    "APP_TOKEN_PSEL",
    "TOKEN_EXPA",
    "APPSCRIPT_BUSCAR",
    "APPSCRIPT_INSERIR",
    "APPSCRIPT_METADADOS",
    "APPSCRIPT_ADICIONAR_CARD",
    "ID_APPSCRIPT_EMAIL_LEADS_PSEL",
    "URL_FIT_CULTURAL"
]