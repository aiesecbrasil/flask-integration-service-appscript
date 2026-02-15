"""
Middleware que verifica a rota acessada e garante que o token do Podio para o
serviço correspondente esteja em cache, autenticando quando necessário.
"""

# ==============================
# Importações (Dependencies)
# ==============================
import logging                      # Registro de eventos para monitoramento e debug
from flask import current_app       # Referência à instância atual da aplicação Flask
from werkzeug.exceptions import NotFound # Exceção padrão para recursos não encontrados
from ..globals import request       # Objeto que encapsula os dados da requisição HTTP atual
from ..clients import getAcessToken # Função que realiza a comunicação com a API do Podio para pegar tokens
from ..cache import cache           # Gerenciador de cache para evitar múltiplas chamadas à API

# Importação de credenciais sensíveis do arquivo de configuração central
from ..config import (
    CLIENT_SECRET_OGX, CLIENT_ID_OGX, APP_ID_OGX, APP_TOKEN_OGX,
    CLIENT_SECRET_PSEL, CLIENT_ID_PSEL, APP_ID_PSEL, APP_TOKEN_PSEL
)

# ==============================
# Configuração de Serviços
# ==============================

# Mapa que associa o nome do serviço (slug na URL) às suas credenciais de autenticação.
# Isso centraliza a manutenção: para adicionar um novo serviço, basta mexer aqui.
CONFIG_MAP = {
    "new-lead-ogx": {
        "key": "ogx-token-podio",
        "credenciais": {
            "CLIENT_SECRET": CLIENT_SECRET_OGX,
            "CLIENT_ID": CLIENT_ID_OGX,
            "APP_ID": APP_ID_OGX,
            "APP_TOKEN": APP_TOKEN_OGX
        }
    },
    "processo-seletivo": {
        "key": "psel-token-podio",
        "credenciais": {
            "CLIENT_SECRET": CLIENT_SECRET_PSEL,
            "CLIENT_ID": CLIENT_ID_PSEL,
            "APP_ID": APP_ID_PSEL,
            "APP_TOKEN": APP_TOKEN_PSEL
        }
    }
}

# Logger específico do módulo para rastrear falhas de roteamento e autenticação
logger = logging.getLogger(__name__)

# ==============================
# Função Principal (Middleware)
# ==============================

def verificar_rota() -> None:
    """
    Garante metadados/token do Podio para o serviço identificado na rota.
    """
    # 1. Captura o caminho da URL (Ex: /api/v1/processo-seletivo/metadados)
    path: str = request.path

    # 2. Divide a string em partes ignorando as barras iniciais e finais
    # Transformamos o path em uma lista de segmentos: ['api', 'v1', 'processo-seletivo', 'metadados']
    parts: list[str] = path.strip("/").split("/")

    # 3. Criamos um "Adapter" do mapa de rotas do Flask
    # bind() é essencial aqui pois estamos verificando a rota manualmente antes de
    # ela ser despachada para o controller final.
    adapter = current_app.url_map.bind("api.meu-site.com")

    try:
        logger.info(f"Middleware verificando endpoint: {path}")

        # 4. Validação de Existência e Método:
        # O Flask verifica se a URL existe e se o método (GET/POST/etc) é permitido.
        # Se falhar, o Werkzeug lança automaticamente NotFound ou MethodNotAllowed.
        adapter.match(path, method=request.method)

        # 5. Lógica de Identificação do Serviço:
        # Por padrão, o identificador do serviço (Ex: 'processo-seletivo')
        # está no terceiro segmento do path (índice 2).
        if len(parts) >= 3:
            service_name: str = parts[2]

            # 6. Busca as configurações de credenciais no mapa definido acima
            config: dict = CONFIG_MAP.get(service_name)

            if config:
                logger.info(f"Verificando autenticação para o serviço: {service_name}")

                #

                # 7. Gerenciamento do Token via Cache (Estratégia Lazy Loading):
                # O 'get_or_set' evita chamadas repetitivas e desnecessárias à API do Podio.
                # Se o token estiver no cache e for válido, ele o recupera instantaneamente.
                # Se não (lambda fetch), ele dispara o 'getAcessToken' e atualiza o cache.
                cache.get_or_set(
                    key=config["key"],
                    fetch=lambda: getAcessToken(config["credenciais"]),
                    baixando="chave de acesso ao podio"
                )
                logger.info(f"Token do Podio para {service_name} validado com sucesso.")

            logger.info("Validação do middleware concluída.")
        else:
            # Caso o path seja menor do que o esperado (Ex: apenas /api/v1/)
            logger.warning(f"Acesso a endpoint genérico sem identificação de serviço: {path}")

        return None

    except NotFound:
        # Erro quando o usuário digita uma URL que não existe na API
        logger.error(f"Erro 404: Endpoint '{path}' não existe ou método '{request.method}' proibido.")
        raise NotFound(f"O recurso {path} não foi encontrado no servidor.")

    except ValueError as ve:
        # Erro de processamento interno ou parâmetros inválidos na extração do path
        mensagem: str = f"Inconsistência de valores na rota {path}: {str(ve)}"
        logger.error(mensagem)
        raise ValueError(mensagem)

    except Exception as e:
        # Captura erros inesperados (Ex: queda de conexão com o Podio ou erro de sintaxe)
        logger.error(f"Falha crítica no middleware de rota: {str(e)}")
        raise e

# ==============================
# Exportações
# ==============================
__all__ = ["verificar_rota"]