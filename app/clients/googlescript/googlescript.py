"""
Cliente para integração com Google Apps Script (envio de e-mails PSEL).

Utiliza um HttpClient com base na URL pública do Apps Script, compondo o path
com o ID do script e o endpoint /exec.
"""
from app.clients.http_request import HttpClient
from app.config import ID_APPSCRIPT_EMAIL_LEADS_PSEL
from app.utils import resolve_response

http = HttpClient(base_url="https://script.google.com",prefix="/macros/s")

@validar
def enviar_email_psel(payload:dict) -> None:
    """
    Dispara a execução do Apps Script responsável por enviar e-mails do PSEL.

    Parâmetros:
    - payload: dict
        Dados necessários ao script (ex.: url parametrizada, e-mails, nome).
    """
    resolve_response(http.post(path=f"/{ID_APPSCRIPT_EMAIL_LEADS_PSEL}/exec",payload=payload))

__all__ = [
    "enviar_email_psel"
]