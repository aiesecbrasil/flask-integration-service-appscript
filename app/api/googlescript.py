from ..services import HttpClient
from ..config import ID_APPSCRIPT_EMAIL_LEADS_PSEL
from ..utils import resolve_response

http = HttpClient(base_url="https://script.google.com",prefix="/macros/s")

@validar
def enviar_email_psel(payload:dict) -> None:
    resolve_response(http.post(path=f"/{ID_APPSCRIPT_EMAIL_LEADS_PSEL}/exec",payload=payload))

__all__ = [
    "enviar_email_psel"
]