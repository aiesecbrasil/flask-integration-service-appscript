from app.api.version1.routes import Router
from app.cache import cache
from app.config import APP_ID_OGX
from app.clients import metadados

new_lead_ogx = Router(name="novos_leads_ogx", url_prefix="/new-lead-ogx")


@new_lead_ogx.get("/metadados")
def buscar_metadados() -> dict:
    cache.get_or_set(
        key="metadados_card-ogx",
        fetch=lambda: metadados(
            chave="ogx-token-podio",
            APP_ID=APP_ID_OGX
        )
    )
    return cache.store["metadados_card-ogx"]


@new_lead_ogx.post("/inscricoes")
def criar_incricao():
    return "oi"


__all__ = [
    "new_lead_ogx"
]
