from ..cache import cache
from ..routes import Router
from ..services import get_appscript,post_appscript
from ..config import APPSCRIPT_METADADOS,APPSCRIPT_ADICIONAR_CARD
from ..globals import request
from ..http import responses

router = Router(name="ogx")

@router.get("/metadados-card")
def metadados_card():
    return cache.get_or_set(
        key="metadados_card",
        fetch=lambda: get_appscript(APPSCRIPT_METADADOS)
    )

@router.post("/adicionar-card")
def adicionar_card():
    data = request.get_json()
    if not data:
        return responses.error("Dados não enviados")

    nome = formatar_nome_com_acentos(data.get("nome"))
    if not validar_nome_com_acentos(nome):
        return responses.error("Nome inválido")

    status, result = post_appscript(
        APPSCRIPT_ADICIONAR_CARD,
        payload=data
    )

    return responses.success(data=result, status=201)


__all__ = [
    "router"
]