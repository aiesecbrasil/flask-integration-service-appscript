from secrets import token_urlsafe

def gerar_token(tamanho_bytes=64) -> str:
    """
    Gera um token super seguro e URL-safe.
    - tamanho_bytes: quantidade de bytes de entropia (64 bytes = ~86 caracteres)
    """
    return token_urlsafe(tamanho_bytes)

__all__ = [
    "gerar_token"
]