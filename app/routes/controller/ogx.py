from .. import Router
from app.cache import cache
from app.services import HttpClient
from app.config import APP_ID_OGX, APPSCRIPT_ADICIONAR_CARD
from app.globals import request
from app.http import responses
from app.api import metadados


ogx = Router(name="ogx", url_prefix="/ogx")
http = HttpClient()


@ogx.get("/metadados")
def buscar_metadados()->dict:
    cache.get_or_set(
        key="metadados_card-ogx",
        fetch=lambda: metadados(
            chave="ogx-token-podio",
            APP_ID=APP_ID_OGX
        )
    )
    return cache.store["metadados_card-ogx"]


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

    return "oi"


@ogx.post("/teste")
def teste() -> dict[str,int]:
    data = request.get_json()
    return data

__all__ = ["ogx"]
