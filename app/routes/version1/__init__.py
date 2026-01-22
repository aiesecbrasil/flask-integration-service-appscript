from .LeadB2C import new_lead_ogx
from .ProcessoSeletivo import processo_seletivo
from ..router import Router

v1 = Router("Api Versão 1", url_prefix="/v1")
v1.register_api(new_lead_ogx)
v1.register_api(processo_seletivo)

__all__ = [
    "v1"
]