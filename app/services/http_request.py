from ..globals import httpx, Dict, Any,Tuple,Optional
from urllib.parse import urlencode

class HttpClient:
    """
    Cliente HTTP assíncrono.

    - timeout_base: timeout padrão da instância
    - timeout: override temporário (auto-reset)
    """

    def __init__(
        self,
        base_url: str = "",
        prefix: str = "",
        timeout: Optional[float] = None
    ):
        # 🔒 Infraestrutura
        self._base_url = base_url.rstrip("/")
        self._prefix = prefix

        # 🌐 Timeout
        self._timeout_base = timeout
        self._timeout_override: Optional[float] = None

    # ================================
    # TIMEOUT CONTROL
    # ================================

    @property
    def timeout(self) -> Optional[float]:
        """
        Retorna o timeout atual (override se existir).
        """
        return (
            self._timeout_override
            if self._timeout_override is not None
            else self._timeout_base
        )

    @timeout.setter
    def timeout(self, value: Optional[float]):
        """
        Define um timeout temporário.
        Ele será resetado automaticamente após a próxima request.
        """
        self._timeout_override = value

    def _consume_timeout(self) -> Optional[float]:
        """
        Usa o timeout atual e reseta o override.
        """
        timeout = self.timeout
        self._timeout_override = None
        return timeout

    # ================================
    # URL BUILDER
    # ================================

    def _build_url(
        self,
        path: str = "",
        params: Optional[Dict[str, Any]] = None
    ) -> str:
        if self._base_url:
            parts = [self._base_url]

            if self._prefix:
                parts.append(self._prefix)

            if path:
                parts.append(path.strip("/"))

            url = "/".join(parts)

            if params:
                url += f"?{urlencode(params, doseq=True)}"

            return url
        return path

    # ================================
    # HTTP METHODS
    # ================================

    async def get(
        self,
        path: str = "",
        params: Optional[Dict[str, Any]] = None,
        headers=None
    ) -> Tuple[int, Any]:

        if headers is None:
            headers = {"Content-Type": "application/json", "Accept": "application/json"}

        timeout = self._consume_timeout()
        url = self._build_url(path, params)

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(
                url,
                headers=headers,
                follow_redirects=True
            )
            return response.status_code, response.json()

    async def post(
        self,
        path: str = "",
        payload: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        as_form: bool = False,  # 👈 Adicione este parâmetro
        headers = None
        ) -> Tuple[int, Any]:

        if headers is None:
            headers = {
                "Content-Type": f"{
                "application/x-www-form-urlencoded" if as_form else "application/json"}",
                "Accept": "application/json"
            }

        timeout = self._consume_timeout()
        url = self._build_url(path, params)

        async with httpx.AsyncClient(timeout=timeout) as client:
            # Seleciona o cabeçalho e o argumento correto do httpx
            if as_form:
                # Usamos 'data' para Form Data
                response = await client.post(url, data=payload, headers=headers, follow_redirects=True)
            else:
                # Usamos 'json' para JSON
                response = await client.post(url, json=payload, headers=headers, follow_redirects=True)
            return response.status_code, response.json()

    async def put(
        self,
        path: str = "",
        payload: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers=None
    ) -> Tuple[int, Any]:
        if headers is None:
            headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
            }
        timeout = self._consume_timeout()
        url = self._build_url(path, params)

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.put(
                url,
                json=payload,
                headers=headers,
                follow_redirects=True
            )
            return response.status_code, response.json()

    async def delete(
        self,
        path: str = "",
        params: Optional[Dict[str, Any]] = None,
        headers = None
    ) -> Tuple[int, Any]:
        if headers is None:
            headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
            }
        timeout = self._consume_timeout()
        url = self._build_url(path, params)

        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.delete(
                url,
                headers=headers,
                follow_redirects=True
            )
            return response.status_code, response.json()


__all__ = ["HttpClient"]