from ..routes import Router
from ..cache import cache
from ..services import get_appscript, post_appscript
from ..config import APPSCRIPT_METADADOS_PSEL, APPSCRIPT_LEAD_PSEL
from ..globals import request
from ..http import responses

router = Router(name="psel")


@router.get("/metadados-lead-psel")
def metadados_lead():
    """
    Retorna os metadados dos leads PSEL.
    Cache de acordo com CACHE_TTL.
    """
    return cache.get_or_set(
        key="metadados_lead_psel",
        fetch=lambda: get_appscript(APPSCRIPT_METADADOS_PSEL)
    )


@router.post("/adicionar-lead")
def adicionar_lead():
    """
    Adiciona um novo lead PSEL.
    Valida se os dados foram enviados e chama o AppScript correspondente.
    """
    data = request.get_json()
    if not data:
        return responses.error("Dados não enviados")

    # Aqui você pode adicionar validações específicas de PSEL, se necessário
    # Ex: validar campos obrigatórios
    status, result = post_appscript(
        APPSCRIPT_LEAD_PSEL,
        payload=data
    )

    return responses.success(data=result, status=201)


__all__ = [
    "router"
]