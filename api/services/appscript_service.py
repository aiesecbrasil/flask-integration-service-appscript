from ..globals import httpx, Dict, Any,Tuple

async def post_appscript(url: str, payload: Dict[str, Any]) -> Tuple[int, Any]:
    """
    Envia uma requisição HTTP POST assíncrona para a URL especificada.

    Args:
        url (str): Endereço da API ou recurso.
        payload (Dict[str, Any]): Dados a serem enviados no corpo da requisição em JSON.

    Returns:
        Tuple[int, Any]: Código HTTP (status) e conteúdo da resposta decodificado como JSON.
    """
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.post(
            url,
            json=payload,
            follow_redirects=True)
        return response.status_code, response.json()

async def get_appscript(url: str) -> Tuple[int, Any]:
    """
    Envia uma requisição HTTP GET assíncrona para a URL especificada.

    Args:
        url (str): Endereço da API ou recurso.

    Returns:
        Tuple[int, Any]: Código HTTP (status) e conteúdo da resposta decodificado como JSON.
    """
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
        follow_redirects=True
        )
        return response.status_code, response.json()

async def put_appscript(url: str, payload: Dict[str, Any]) -> Tuple[int, Any]:
    """
    Envia uma requisição HTTP PUT assíncrona para a URL especificada.

    Args:
        url (str): Endereço da API ou recurso.
        payload (Dict[str, Any]): Dados a serem atualizados no recurso em JSON.

    Returns:
        Tuple[int, Any]: Código HTTP (status) e conteúdo da resposta decodificado como JSON.
    """
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.put(url, json=payload, follow_redirects=True)
        return response.status_code, response.json()

async def delete_appscript(url: str) -> Tuple[int, Any]:
    """
    Envia uma requisição HTTP DELETE assíncrona para a URL especificada.

    Args:
        url (str): Endereço do recurso a ser deletado.

    Returns:
        Tuple[int, Any]: Código HTTP (status) e conteúdo da resposta decodificado como JSON.
    """
    async with httpx.AsyncClient(timeout=None) as client:
        response = await client.delete(url, follow_redirects=True)
        return response.status_code, response.json()


__all__ =[
    "get_appscript",
    "post_appscript",
    "put_appscript",
    "delete_appscript"
]