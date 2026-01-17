from flask import Response

from ..globals import Any,Dict,Tuple,jsonify
from ..services import HttpClient
from ..utils import agora
from ..cache import cache
from ..utils import resolve_response

http = HttpClient(base_url="https://api.podio.com")
http2 = http.clone(prefix="/item/app")
http3 = http2.clone(prefix="/item")

@validar
def getAcessToken(item: Dict[str,Any], PATH: str = "/oauth/token") -> tuple[int, dict[str, Any]]:
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


        status, data = resolve_response(respose)
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

@validar
def buscarToken(chave:str) -> int:
    return cache.store[chave]["data"]["access_token"]

@validar
def metadados(chave:str,APP_ID:int) -> Tuple[int,dict]:
    headers = {
        "Authorization": f"Bearer {buscarToken(chave)}",
        "Content-Type": "application/json"
    }
    response = http.get(path=f"/app/{APP_ID}", headers=headers)

    status, data = resolve_response(response)
    return status,data

@validar
def adicionar_lead(chave:str,data:Any,APP_ID:int) -> tuple[dict, int]:

    headers = {
        "Authorization": f"Bearer {buscarToken(chave)}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = data.model_dump()
    response = http2.post(path=f"/{APP_ID}",payload=payload,headers=headers)
    status, data = resolve_response(response)

    return data,buscar_id_lead(data)

@validar
def atualizar_lead(chave:str,data:Any,data_response:dict) -> Tuple[int,int]:
    item_id = buscar_id_card(data_response)
    headers = {
        "Authorization": f"Bearer {buscarToken(chave)}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = data.model_dump()

    response = http3.put(path=f"/{item_id}",payload=payload,headers=headers)
    status, data = resolve_response(response)

    return status,data

@validar
def buscar_id_lead(data:dict) -> int:
    return data["app_item_id"]

@validar
def buscar_id_card(data:dict) -> int:
    return data["item_id"]

__all__ = ["getAcessToken","buscarToken","metadados","adicionar_lead","atualizar_lead"]