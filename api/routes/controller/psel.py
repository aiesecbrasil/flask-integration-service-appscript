from .. import Router
from api.cache import cache
from api.services import HttpClient
from api.config import APPSCRIPT_METADADOS_PSEL, APPSCRIPT_LEAD_PSEL
from api.globals import request
from api.http import responses

psel = Router(name="psel", url_prefix="/psel")
http = HttpClient()


@psel.get("/metadados")
def buscar_metadados():
    """
    Retorna os metadados dos leads PSEL.
    Cache de acordo com CACHE_TTL.
    """
    return cache.get_or_set(
        key="metadados_lead_psel",
        fetch=lambda: http.get(APPSCRIPT_METADADOS_PSEL)
    )


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
