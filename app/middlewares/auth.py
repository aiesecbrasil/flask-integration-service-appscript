"""
auth
----

Middleware para validação de API Keys e domínios.
"""

from ..config import API_KEYS_PERMITIDAS
from ..core import DOMINIOS_PERMITIDOS,IS_PRODUCTION
from ..globals import request, jsonify, List, Optional

# ==============================
# Configurações
# ==============================
ROTAS_SEM_VALIDACAO: List[str] = ["/favicon.ico","/validarToken"]

# ==============================
# Middleware global
# ==============================
def verificar_origem():
    """
    Middleware global que valida API Key e domínio antes de qualquer request.
    Retorna JSON de erro com status 403 caso bloqueado, ou None se permitido.
    """

    # Rotas que não precisam de validação
    if request.path in ROTAS_SEM_VALIDACAO:
        return None

    # ==========================
    # Validação de API Key
    # ==========================
    api_key: Optional[str] = request.headers.get("X-API-KEY")
    if api_key and api_key not in API_KEYS_PERMITIDAS:
        return jsonify({"error": "API Key inválida"}), 403

    # ==========================
    # Validação de domínio
    # ==========================
    host: Optional[str] = request.headers.get("Host")
    if host:
        if host not in DOMINIOS_PERMITIDOS:
            return jsonify({"error": "Domínio não autorizado"}), 403

    # ==========================
    # Bloqueio total em produção para requisições diretas
    # ==========================
    if IS_PRODUCTION:
        return jsonify({"error": "Bloqueado: requisições diretas não são permitidas"}), 403

    # Se tudo ok, retorna None e o Flask continua a execução
    return None


# ==============================
# Exportações
# ==============================
__all__ = [
    "verificar_origem"
]
