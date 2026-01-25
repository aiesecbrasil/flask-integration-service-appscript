from .routes import *

v1 = Router("versao_1", url_prefix="/v1")
v1.register_api(new_lead_ogx)
v1.register_api(processo_seletivo)

__all__ = [
    "v1",
    "Router"
]