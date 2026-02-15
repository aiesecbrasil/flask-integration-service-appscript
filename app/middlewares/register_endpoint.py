"""
Middleware pós-request para registrar linha de log no formato common log format
(IP, timestamp, método, endpoint, protocolo e status).
"""

# ==============================
# Importações (Dependencies)
# ==============================
import logging                      # Sistema de logging do Python para saída em console/arquivo
from pydantic import ConfigDict      # Configuração para validação de tipos complexos (Pydantic)
from ..globals import request, Response # Objetos globais para acessar dados da requisição e resposta
from ..utils import agora_format_brasil_mes # Utilitário para formatação de data no padrão brasileiro

# ==============================
# Middleware de Auditoria
# ==============================



@validar(config=ConfigDict(arbitrary_types_allowed=True))
def register_url(response: Response) -> Response:
    """
    Registra uma linha de auditoria resumida após a execução da rota.

    Esta função captura metadados do ambiente de execução e da resposta final
    para compor um log estruturado. Também define políticas de cache.

    Args:
        response (Response): Objeto de resposta gerado pelo controller.

    Returns:
        Response: O mesmo objeto de resposta, agora com headers de cache injetados.
    """

    # 1. Extração de Metadados do Ambiente (WSGI)
    # SERVER_PROTOCOL identifica a versão do HTTP (ex: HTTP/1.1)
    protocol = request.environ.get("SERVER_PROTOCOL")

    # 2. Identificação da Origem
    # remote_addr captura o IP do cliente (ou do Proxy/Load Balancer)
    ip = request.remote_addr

    # 3. Timestamp e Rota
    hora = agora_format_brasil_mes()
    metodo = request.method
    endpoint = request.path

    # 4. Composição da Mensagem (Common Log Format)
    # Formato: IP - - [Data] "MÉTODO ENDPOINT PROTOCOLO" STATUS -
    mensagem = f'{ip} - - [{hora}] "{metodo} {endpoint} {protocol}" {response.status_code} -'

    # 5. Registro no Logger
    # Obtemos o logger do módulo para garantir que o nome apareça corretamente nos registros
    logger = logging.getLogger(__name__)
    logger.info(mensagem)

    # 6. Otimização de Performance (Headers)
    # 'public': Permite que CDNs e Browsers guardem o cache.
    # 'max-age=7200': Define o tempo de vida do cache para 2 horas ou 7200 segundos.
    # 'must-revalidate': Obriga o cliente a checar com o servidor após o tempo expirar.
    response.headers['Cache-Control'] = 'public, max-age=7200, must-revalidate'

    return response

# ==============================
# Exportações
# ==============================
__all__ = ['register_url']