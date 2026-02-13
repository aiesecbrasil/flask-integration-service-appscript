"""
Cliente de integração com a API do Podio.

Provê funções para autenticação via credenciais de App, além de operações
básicas de CRUD de itens (cards) relacionados ao app do Podio.
"""
from app.clients.http_request import HttpClient
from app.globals import Any,Dict,Tuple
from app.utils import agora
from app.cache import cache
from app.utils import resolve_response

http = HttpClient(base_url="https://api.podio.com")
http2 = http.clone(prefix="/item/app")
http3 = http2.clone(prefix="/item")

@validar
def getAcessToken(item: Dict[str,Any], PATH: str = "/oauth/token") -> tuple[int, dict[str, Any]]:
    """
    Obtém tokens de acesso/refresh do Podio para um App específico.

    Parâmetros:
    - item: Dict[str, Any]
        Dicionário contendo CLIENT_ID, CLIENT_SECRET, APP_ID e APP_TOKEN.
    - PATH: str
        Caminho do endpoint de autenticação (default: /oauth/token).

    Retorno:
    - tuple[int, dict]
        Status HTTP e dicionário com access_token, expires_in, refresh_token e created_at.

    Erros:
    - Levanta ValueError em caso de falha de autenticação.
    - Levanta RuntimeError para erros de estrutura da resposta ou problemas gerais de integração.
    """
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
    """Recupera o access_token armazenado no cache para a chave informada."""
    return cache.store[chave]["data"]["access_token"]

@validar
def metadados(chave:str,APP_ID:int) -> Tuple[int,dict]:
    """
    Busca metadados de um App no Podio.

    Parâmetros:
    - chave: str
        Chave utilizada para recuperar o token no cache.
    - APP_ID: int
        Identificador do App no Podio.

    Retorno: (status, data) do Podio já resolvidos.
    """
    headers = {
        "Authorization": f"Bearer {buscarToken(chave)}",
        "Content-Type": "application/json"
    }
    response = http.get(path=f"/app/{APP_ID}", headers=headers)

    status, data = resolve_response(response)
    return status,data

@validar
def adicionar_lead(chave:str,data:Any,APP_ID:int) -> tuple[dict, int]:
    """
    Cria um novo item (lead) no App do Podio.

    Parâmetros:
    - chave: str
        Chave para recuperar o access token do cache.
    - data: Any
        Payload no formato esperado pela API do Podio para criação de item.
    - APP_ID: int
        Identificador do App de destino no Podio.

    Retorno:
    - tuple[data_response: dict, id_podio: int]
        Dicionário de resposta e o app_item_id extraído.
    """

    headers = {
        "Authorization": f"Bearer {buscarToken(chave)}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = data
    response = http2.post(path=f"/{APP_ID}",payload=payload,headers=headers)
    status, data = resolve_response(response)

    return data,buscar_id_lead(data)

@validar
def atualizar_lead(chave:str,data:Any,data_response:dict) -> Tuple[int,int]:
    """
    Atualiza um item existente no Podio.

    Parâmetros:
    - chave: str
        Chave para recuperar o token do cache.
    - data: Any
        Payload de atualização.
    - data_response: dict
        Resposta original do Podio contendo identificadores do item criado.

    Retorno:
    - tuple[item_id: int, status: int]
        Identificador do card e o status da operação.
    """
    item_id = buscar_id_card(data_response)
    headers = {
        "Authorization": f"Bearer {buscarToken(chave)}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = data

    response = http3.put(path=f"/{item_id}",payload=payload,headers=headers)
    status, data = resolve_response(response)

    return item_id,data

@validar
def remover_lead(chave:str,data_response:dict) -> bool | tuple[bool, Any]:
    """
    Remove um item no Podio.

    Parâmetros:
    - chave: str
        Chave para recuperar o token do cache.
    - data_response: dict
        Resposta com informações necessárias para identificar o item (item_id).

    Retorno:
    - True quando a exclusão retorna HTTP 204. Caso contrário, (False, data).
    """
    item_id = buscar_id_card(data_response)
    headers = {
        "Authorization": f"Bearer {buscarToken(chave)}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = http3.delete(path=f"/{item_id}",headers=headers)
    status,data = resolve_response(response)

    if status == 204:
        return True
    else:
        return False, data

@validar
def buscar_id_lead(data:dict) -> int:
    """Extrai o app_item_id (id lógico do item dentro do App) da resposta do Podio."""
    return data.get("app_item_id")

@validar
def buscar_id_card(data:dict) -> int:
    """Extrai o item_id (id único do card no Podio) da resposta do Podio."""
    return data.get("item_id")

__all__ = [
    "getAcessToken",
    "buscarToken",
    "metadados",
    "adicionar_lead",
    "atualizar_lead",
    "remover_lead",
    "buscar_id_card",
    "buscar_id_lead"
]