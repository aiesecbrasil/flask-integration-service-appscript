"""
config.settings
---------------

Configuração central da aplicação.

Responsabilidades:
- Ler variáveis de ambiente obrigatórias
- Definir ambiente de execução
- Selecionar domínios permitidos por ambiente
- Centralizar URLs externas e cache

Este módulo:
- NÃO importa Flask
- NÃO importa código de rotas ou services
- FALHA rápido se configuração estiver errada
"""

from ..globals.std import os, List


# ================================
# FUNÇÃO AUXILIAR
# ================================

def get_env_or_fail(var_name: str) -> str:
    """
    Recupera uma variável de ambiente obrigatória.

    Args:
        var_name (str): Nome da variável de ambiente.

    Returns:
        str: Valor da variável.

    Raises:
        ValueError: Se a variável não estiver definida ou vazia.
    """
    valor = os.getenv(var_name, "").strip()
    if not valor:
        raise ValueError(f"Variável de ambiente {var_name} não está definida!")
    return valor


# ================================
# AMBIENTE
# ================================

AMBIENTE: str = get_env_or_fail("AMBIENTE").upper()

IS_PRODUCTION: bool = AMBIENTE == "PRODUCTION"
IS_NON_PROD: bool = AMBIENTE in {"DEVELOPMENT", "DEV", "TEST", "TESTING"}

if not (IS_PRODUCTION or IS_NON_PROD):
    raise ValueError(f"Ambiente inválido: {AMBIENTE}")


# ================================
# DOMÍNIOS
# ================================

DOMINIOS_PRODUCAO: List[str] = get_env_or_fail("DOMINIOS_PRODUCAO").split(",")

DOMINIOS_TESTE: List[str] = get_env_or_fail("DOMINIOS_TESTE").split(",")

# Seleção de domínios por ambiente
DOMINIOS_PERMITIDOS: List[str] = DOMINIOS_PRODUCAO if IS_PRODUCTION else DOMINIOS_TESTE



# ================================
# API KEYS
# ================================

API_KEYS_PERMITIDAS: List[str] = [
    k.strip() for k in get_env_or_fail("API_KEYS_PERMITIDAS").split(",")
]


# ================================
# APPS SCRIPT
# ================================

APPSCRIPT_BUSCAR = get_env_or_fail("APPSCRIPT_BUSCAR")
APPSCRIPT_INSERIR = get_env_or_fail("APPSCRIPT_INSERIR")
APPSCRIPT_METADADOS = get_env_or_fail("APPSCRIPT_METADADOS_CARD_OGX")
APPSCRIPT_ADICIONAR_CARD = get_env_or_fail("APPSCRIPT_ADICIONAR_CARD_OGX")
APPSCRIPT_VALIDAR_URL = get_env_or_fail("APPSCRIPT_VALIDAR_URL")
APPSCRIPT_LEAD_PSEL = get_env_or_fail("APPSCRIPT_ADICIONAR_LEADS_PSEL")
APPSCRIPT_METADADOS_PSEL = get_env_or_fail("APPSCRIPT_METADADOS_LEAD_PSEL")


# ================================
# CACHE
# ================================

CACHE_TTL: int = int(get_env_or_fail("CACHE_TTL"))


# ================================
# EXPORTS
# ================================

__all__ = [
    # env
    "AMBIENTE",
    "IS_PRODUCTION",
    "IS_NON_PROD",

    # domains
    "DOMINIOS_PRODUCAO",
    "DOMINIOS_TESTE",
    "DOMINIOS_PERMITIDOS",

    # security
    "API_KEYS_PERMITIDAS",

    # cache
    "CACHE_TTL",

    # apps script
    "APPSCRIPT_BUSCAR",
    "APPSCRIPT_INSERIR",
    "APPSCRIPT_METADADOS",
    "APPSCRIPT_ADICIONAR_CARD",
    "APPSCRIPT_VALIDAR_URL",
    "APPSCRIPT_LEAD_PSEL",
    "APPSCRIPT_METADADOS_PSEL",
]
