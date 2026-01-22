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


def verificar_rota():
    path = request.path  # Ex: /api/v1/new-lead-ogx/metadados
    parts = path.strip("/").split("/")  # ['api', 'v1', 'new-lead-ogx', 'metadados']

    # 2. Ignoramos o prefixo dinamicamente (pula 'api' e 'v1' ou 'v2')
    # O identificador do serviço geralmente é o 3º elemento (índice 2)
    if len(parts) >= 3:
        service_name = parts[2]

        # 3. Verificamos se esse serviço existe no nosso mapa
        config = CONFIG_MAP.get(service_name)

        if config:
            cache.get_or_set(
                key=config["key"],
                fetch=lambda: getAcessToken(config["credenciais"])
            )

    return None

__all__ = ["verificar_rota"]