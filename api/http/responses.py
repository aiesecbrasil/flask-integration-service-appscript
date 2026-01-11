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

from ..globals.std import Dict, Any, Optional

# ================================
# SUCCESS RESPONSE
# ================================
def success(
    data: Any,
    message: Optional[str] = None,
    status: int = 200
) -> Dict[str, Any]:
    """
    Retorna resposta de sucesso padrão.

    Args:
        data (Any): Conteúdo principal da resposta.
        message (str, optional): Mensagem opcional.
        status (int, optional): Código HTTP (default=200).

    Returns:
        Dict[str, Any]: Estrutura da resposta.
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
) -> Dict[str, Any]:
    """
    Retorna resposta de erro padrão.

    Args:
        erro (str): Mensagem de erro principal (chave usada pelo front).
        details (Any, optional): Detalhes adicionais do erro.
        status (int, optional): Código HTTP (default=400).

    Returns:
        Dict[str, Any]: Estrutura da resposta.
    """
    resp: Dict[str, Any] = {
        "status": "error",
        "error": erro,
        "status_code": status
    }
    if details is not None:
        resp["details"] = details
    return resp


# ================================
# REDIRECT RESPONSE
# ================================
def redirect(
    url: str,
    status: int = 302
) -> Dict[str, Any]:
    """
    Retorna resposta de redirecionamento.

    Args:
        url (str): URL para redirecionar.
        status (int, optional): Código HTTP (default=302).

    Returns:
        Dict[str, Any]: Estrutura da resposta.
    """
    return {
        "status": "redirect",
        "url": url,
        "status_code": status
    }


# ================================
# EXPORTS
# ================================
__all__ = [
    "success",
    "error",
    "redirect",
]
