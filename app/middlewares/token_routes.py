from ..globals import request
from ..api import getAcessToken,buscarToken
from ..config import (CLIENT_SECRET_OGX,CLIENT_ID_PSEL,CLIENT_SECRET_PSEL,
                      CLIENT_ID_OGX,APP_ID_OGX,APP_TOKEN_OGX,APP_TOKEN_PSEL,APP_ID_PSEL)
from ..cache import cache

def verificar_rota():

    OGX = {
        "CLIENT_SECRET":CLIENT_SECRET_OGX,
        "CLIENT_ID":CLIENT_ID_OGX,
        "APP_ID":APP_ID_OGX,
        "APP_TOKEN":APP_TOKEN_OGX
    }

    PSEL = {
        "CLIENT_SECRET":CLIENT_SECRET_PSEL,
        "CLIENT_ID":CLIENT_ID_PSEL,
        "APP_ID":APP_ID_PSEL,
        "APP_TOKEN":APP_TOKEN_PSEL
    }

    rota = request.path
    if rota.startswith("/ogx"):
        cache.get_or_set(
            key="ogx-token-podio",
            fetch=lambda: getAcessToken(OGX)
        )
        return None
    if rota.startswith("/psel"):
        cache.get_or_set(
            key="psel-token-podio",
            fetch=lambda: getAcessToken(PSEL)
        )
        return None
    return None

__all__ = ["verificar_rota"]