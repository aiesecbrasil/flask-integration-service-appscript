"""
Middleware pós-request para registrar linha de log no formato common log format
(IP, timestamp, método, endpoint, protocolo e status).
"""
import logging
from pydantic import  ConfigDict
from ..globals import request,Response
from ..utils import agora_format_brasil_mes

@validar(config=ConfigDict(arbitrary_types_allowed=True))
def register_url(response:Response) -> Response:
    """
    Registra uma linha de auditoria resumida após a execução da rota.

    Retorna o mesmo Response recebido, sem modificação.
    """
    protocol = request.environ.get("SERVER_PROTOCOL")
    ip = request.remote_addr
    hora = agora_format_brasil_mes()
    metodo = request.method
    endpoint = request.path
    mensagem = f'{ip} - - [{hora}] "{metodo} {endpoint} {protocol}" {response.status_code} -'
    logger = logging.getLogger(__name__)
    logger.info(mensagem)
    return response

__all__ = ['register_url']