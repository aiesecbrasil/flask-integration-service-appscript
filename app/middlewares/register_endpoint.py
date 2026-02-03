import logging
from ..globals import request,Response
from ..utils import agora_format_brasil_mes

@validar
def register_url(response:Response):
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