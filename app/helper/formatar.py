"""
Helpers de formatação específicos da camada de apresentação/integração.

Atualmente contém utilitário para construir a URL do Fit Cultural utilizando
hash fragment com os parâmetros codificados.
"""
from urllib.parse import urlencode
from ..config import URL_FIT_CULTURAL

@validar
def formatar_url_fit(payload:dict=None) -> str:
    """
    Monta a URL do Fit Cultural com parâmetros no fragmento (#).

    Parâmetros:
    - payload: dict | None
        Dicionário com os parâmetros que serão codificados após o '#'.

    Retorno:
    - str: URL no formato "<URL_FIT_CULTURAL>#k1=v1&k2=v2".
    """
    return f"{URL_FIT_CULTURAL}#{urlencode(payload)}"

__all__ = ["formatar_url_fit"]