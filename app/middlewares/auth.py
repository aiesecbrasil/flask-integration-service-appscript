"""
auth
----

Middleware para validação de API Keys e domínios.

Regras:
- Rotas em ROTAS_SEM_VALIDACAO são isentas.
- Se X-API-KEY presente, deve ser autorizada.
- Domínio (Host) deve pertencer aos domínios permitidos.
- Em produção, bloqueia requisições diretas.
"""
import logging
from ..config import API_KEYS_PERMITIDAS
from ..core import DOMINIOS_PERMITIDOS,IS_PRODUCTION
from ..globals import request, jsonify, List, Optional

# ==============================
# Configurações
# ==============================
ROTAS_SEM_VALIDACAO: List[str] = ["/validarToken"]
logger = logging.getLogger(__name__)
# ==============================
# Middleware global
# ==============================
def verificar_origem():
    """
    Middleware global que valida API Key e domínio antes de qualquer request.
    Retorna JSON de erro com status 403 caso bloqueado, ou None se permitido.
    """
    logger.info("Autenticando origem...")
    # Rotas que não precisam de validação
    if request.path in ROTAS_SEM_VALIDACAO:
        logger.info(f"Rota não precisou ser validada: {request.path}")
        return None

    # ==========================
    # Validação de API Key
    # ==========================
    api_key: Optional[str] = request.headers.get("X-API-KEY")
    if api_key and api_key not in API_KEYS_PERMITIDAS:
        logger.error(f"Chave de Api {api_key} não autorizada")
        return jsonify({"error": "API Key inválida"}), 403

    # ==========================
    # Validação de domínio
    # ==========================
    host: Optional[str] = f'https://{request.headers.get("Host")}'
    if host and host not in DOMINIOS_PERMITIDOS:
        logger.error(f"O host {host} não autorizado")
        return jsonify({"error": "Domínio não autorizado"}), 403

    # ==========================
    # Bloqueio total em produção para requisições diretas
    # ==========================
    if IS_PRODUCTION:
        logger.error(f"A api não pode ser acessada por meio de Requisições Diretas")
        return jsonify({"error": "Bloqueado: requisições diretas não são permitidas"}), 403
    logger.info("Origem autenticada com sucesso!")
    # Se tudo ok, retorna None e o Flask continua a execução
    return None


# ==============================
# Exportações
# ==============================
__all__ = [
    "verificar_origem"
]
