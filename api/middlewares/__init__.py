"""
middlewares
-----------

Middlewares comuns para uso em aplicações web.
Inclui validação de API keys, verificação de domínios e outras funcionalidades de request.
"""

from .auth import verificar_origem

__all__ = [
    "verificar_origem"
]
