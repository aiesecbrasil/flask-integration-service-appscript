import logging
from flask import current_app
from werkzeug.exceptions import NotFound
from ..globals import request
from ..clients import getAcessToken
from ..config import (CLIENT_SECRET_OGX, CLIENT_ID_OGX, APP_ID_OGX, APP_TOKEN_OGX,
                      CLIENT_SECRET_PSEL, CLIENT_ID_PSEL, APP_ID_PSEL, APP_TOKEN_PSEL)
from ..cache import cache

# 1. Centralizamos as configurações em um mapa
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

# 2. Instanciando o logger
logger = logging.getLogger(__name__)

def verificar_rota():
    path = request.path  # Ex: /api/v1/new-lead-ogx/metadados
    parts = path.strip("/").split("/")  # ['api', 'v1', 'new-lead-ogx', 'metadados']

    # Use "api.meu-site.com" em vez de string vazia
    adapter = current_app.url_map.bind("api.meu-site.com")
    try:
        logger.info("Autenticando endpoint...")
        # 2. Ignoramos o prefixo dinamicamente (pula 'api' e 'v1' ou 'v2')
        # O identificador do serviço geralmente é o 3º elemento (índice 2)
        adapter.match(path,method=request.method)
        if len(parts) >= 3:
            service_name = parts[2]

            # 3. Verificamos se esse serviço existe no nosso mapa
            config = CONFIG_MAP.get(service_name)

            if config:
                logger.info("Baixando Metadados do Podio...")
                cache.get_or_set(
                    key=config["key"],
                    fetch=lambda: getAcessToken(config["credenciais"])
                )
                logger.info("Metadados do Podio Baixados com Sucesso!")
            logger.info("Endpoint Autentica com Sucesso!")
        else:
            logger.error(f"Rota inexistente acessada: {path}")
        return None
    except NotFound:
        # Aqui capturamos URLs que não existem na API
        logger.error(f"Rota inexistente acessada: {path}")
        raise NotFound

    except ValueError as ve:
        mensagem = f"Erro nos valores na rota: {path}: {str(ve)}"
        # Captura outros erros (ex: ValueError se o tiver erro no valor passado)
        logger.error(mensagem)
        raise ValueError(mensagem)

    except Exception as e:
        # Captura outros erros (ex: MethodNotAllowed se o método HTTP estiver errado)
        logger.error(f"Erro na validação da rota {path}: {str(e)}")
        raise e

__all__ = ["verificar_rota"]