from ..cache import cache
from ..routes import Router
from ..services import HttpClient
from ..config import APPSCRIPT_METADADOS,APPSCRIPT_ADICIONAR_CARD
from ..globals import request
from ..http import responses

ogx = Router(name="ogx",url_prefix="/ogx")
http = HttpClient()

@ogx.get("/metadados")
def buscar_metadados():
    return cache.get_or_set(
        key="metadados_card",
        fetch=lambda: http.get(APPSCRIPT_METADADOS)
    )

@ogx.post("/inscricoes")
def criar_incricao():
    data = request.get_json()
    if not data:
        return responses.error("Dados não enviados")

    nome = formatar_nome_com_acentos(data.get("nome"))
    if not validar_nome_com_acentos(nome):
        return responses.error("Nome inválido")

    status, result = http.post(
        APPSCRIPT_ADICIONAR_CARD,
        payload=data
    )

    return responses.success(data=result, status=201)


__all__ = [
    "router"
]