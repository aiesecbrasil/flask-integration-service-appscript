"""
Utilitário para normalizar resultados de operações assíncronas/síncronas.

resolve_response executa corotinas (awaitables) imediatamente com asyncio.run
quando necessário, retornando sempre uma tupla consistente (status, data).
"""
import asyncio
from typing import Any, Tuple

def resolve_response(result: Any) -> Tuple[int, Any]:
    """
    Resolve o resultado retornando (status, data) de forma uniforme.

    - Se result for uma coroutine, executa-a com asyncio.run e retorna seu valor.
    - Se for síncrono, retorna diretamente o valor informado.
    """
    if asyncio.iscoroutine(result):
        return asyncio.run(result)
    return result

__all__ = ["resolve_response"]