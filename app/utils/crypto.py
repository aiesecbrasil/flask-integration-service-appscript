"""
Segurança
---------

Utilitários para geração de credenciais e tokens criptograficamente seguros.
Ideal para chaves de API, tokens de redefinição de senha ou identificadores de sessão.
"""

# ==============================
# Importações (Dependencies)
# ==============================
from secrets import token_urlsafe  # Gera strings aleatórias seguras para uso em URLs (Base64)

# ==============================
# Funções de Geração
# ==============================

def gerar_token(tamanho_bytes: int = 64) -> str:
    """
    Gera um token criptograficamente forte, codificado em Base64 URL-safe.

    Diferente do módulo 'random', o 'secrets' utiliza fontes de entropia do
    sistema operacional (como /dev/urandom), tornando os tokens impossíveis
    de prever.

    Args:
        tamanho_bytes (int): Quantidade de bytes de entropia.
                            64 bytes resultam em aproximadamente 86 caracteres.

    Returns:
        str: Um token aleatório contendo caracteres [a-z, A-Z, 0-9, -, _].
    """
    #
    return token_urlsafe(tamanho_bytes)

# ==============================
# Exportações
# ==============================
__all__ = [
    "gerar_token"
]