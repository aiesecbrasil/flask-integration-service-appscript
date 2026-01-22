"""
http.response
-------------

Funções utilitárias para criar respostas HTTP consistentes.

Responsabilidades:
- Resposta de sucesso
- Resposta de erro
- Redirecionamento
- Status code padronizado

Este módulo:
- NÃO depende de Flask ou FastAPI
- Retorna dicionários prontos para JSON
"""
from typing import Any

from ..globals.std import Dict, Any, Optional

# ================================
# SUCCESS RESPONSE
# ================================
def success(
    data: Any,
    message: Optional[str] = None,
    status: int = 200
) -> dict[str, str | int | Any]:
    """
    Retorna resposta de sucesso padrão.

    Args:
        data (Any): Conteúdo principal da resposta.
        message (str, optional): Mensagem opcional.
        status (int, optional): Código HTTP (default=200).

    Returns:
        tuple[dict[str, str | int], int]: Estrutura da resposta.
    """
    return {
        "status": "success",
        "message": message or "Operação realizada com sucesso",
        "data": data,
        "status_code": status
    }


# ================================
# ERROR RESPONSE
# ================================
def error(
    erro: str,
    details: Optional[Any] = None,
    status: int = 400
) -> tuple[dict[str, Any], int]:
    """
    Retorna resposta de erro padrão.

    Args:
        erro (str): Mensagem de erro principal (chave usada pelo front).
        details (Any, optional): Detalhes adicionais do erro.
        status (int, optional): Código HTTP (default=400).

    Returns:
        tuple[dict[str, Any], int]: Estrutura da resposta.
    """
    resp: Dict[str,Any] = {
        "status": "error",
        "error": erro,
        "status_code": status
    }
    if details is not None:
        resp["details"] = details
    return resp,status


# ================================
# REDIRECT RESPONSE
# ================================
def redirect(
    url: str,
    status: int = 302
) -> tuple[dict[str, str | int], int]:
    """
    Retorna resposta de redirecionamento.

    Args:
        url (str): URL para redirecionar.
        status (int, optional): Código HTTP (default=302).

    Returns:
        tuple[dict[str, str | int], int]: Estrutura da resposta.
    """
    return {
        "status": f"Redirecionado para {url}",
        "url": url,
        "status_code": status
    },status


# ================================
# EXPORTS
# ================================
__all__ = [
    "success",
    "error",
    "redirect",
]
