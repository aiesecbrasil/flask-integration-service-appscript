from urllib.parse import urlencode
from ..config import URL_FIT_CULTURAL

@validar
def formatar_url_fit(payload:dict=None) -> str:
    return f"{URL_FIT_CULTURAL}#{urlencode(payload)}"

__all__ = ["formatar_url_fit"]