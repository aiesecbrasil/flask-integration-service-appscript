import json

from .. import Router
from app.cache import cache
from app.services import HttpClient
from app.config import APP_ID_PSEL, APPSCRIPT_LEAD_PSEL
from app.globals import request
from app.http import responses
from app.api import metadados

psel = Router(name="psel", url_prefix="/psel")
http = HttpClient()


@psel.get("/metadados")
def buscar_metadados():
    """
    Retorna os metadados dos leads PSEL.
    Cache de acordo com CACHE_TTL.
    """
    cache.get_or_set(
        key="metadados_card-psel",
        fetch=lambda: metadados(
            chave="psel-token-podio",
            APP_ID=APP_ID_PSEL
        )
    )
    return cache.store["metadados_card-psel"]


@psel.post("/inscricoes")
def criar_incricao():
    """
    Adiciona um novo lead PSEL.
    Valida se os dados foram enviados e chama o AppScript correspondente.
    """
    data = request.get_json()
    if not data:
        return responses.error("Dados não enviados")

    # Aqui você pode adicionar validações específicas de PSEL, se necessário
    # Ex: validar campos obrigatórios
    status, result = http.post(
        APPSCRIPT_LEAD_PSEL,
        payload=data
    )

    return responses.success(data=result, status=201)


__all__ = ["psel"]
