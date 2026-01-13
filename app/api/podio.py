from ..globals import asyncio,Any
from ..services import HttpClient
from ..utils import agora
from ..cache import cache

http = HttpClient(base_url="https://api.podio.com")

def getAcessToken(item: dict, PATH: str = "/oauth/token") -> tuple[int, dict[str, Any]]:
    payload = {
        "grant_type": "app",
        "client_id": item["CLIENT_ID"],
        "client_secret": item["CLIENT_SECRET"],
        "app_id": item["APP_ID"],
        "app_token": item["APP_TOKEN"]
    }
    try:
        # 🚀 Tenta a requisição
        respose = http.post(path=PATH, payload=payload, as_form=True)

        if asyncio.iscoroutine(respose):
            status, data = asyncio.run(respose)
        else:
            status, data = respose

        # 🛑 Se o Podio retornar erro, levantamos uma exceção para parar tudo
        if status != 200:
            error_msg = data.get("error_description", "Erro desconhecido no Podio")
            raise ValueError(f"Parada Crítica: Falha na Autenticação ({status}) - {error_msg}, por favor recarregue a página")

        # ✨ Se chegou aqui, deu certo. Montamos o retorno esperado pelo Cache
        return status, {
            "access_token": data["access_token"],
            "expires_in": data["expires_in"],
            "refresh_token": data["refresh_token"],
            "created_at": agora()
        }

    except KeyError as e:
        # Para tudo se faltar uma chave essencial no dicionário de resposta
        raise RuntimeError(f"Erro de estrutura nos dados do Podio: Chave {e} não encontrada.") from e

    except Exception as e:
        # Para tudo em caso de erro de conexão ou qualquer outro problema
        raise RuntimeError(f"Erro Fatal na integração: {str(e)}") from e

def buscarToken(chave):
    return cache.store[chave]["data"]["access_token"]

def metadados(chave,APP_ID):
    hearders = {
        "Authorization": f"Bearer {buscarToken(chave)}"
    }
    response = http.get(path=f"/app/{APP_ID}", headers=hearders)
    if asyncio.iscoroutine(response):
        status, data = asyncio.run(response)
    else:
        status, data = response
    return status,data

__all__ = ["getAcessToken","buscarToken","metadados"]