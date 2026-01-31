"""
middlewares
-----------

Middlewares comuns para uso em aplicações web.
Inclui validação de API keys, verificação de domínios e outras funcionalidades de request.
"""

from .auth import verificar_origem
from .token_routes import verificar_rota
from .register_endpoint import register_url

__all__ = [
    "verificar_origem",
    "verificar_rota",
    "register_url"
]
