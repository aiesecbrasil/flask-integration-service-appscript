"""
Helpers de formatacao especificos da camada de apresentacao/integracao.

Atualmente contem utilitario para construir a URL do Fit Cultural utilizando
hash fragment com os parametros codificados.
"""

# ==============================
# Importacoes (Dependencies)
# ==============================
from urllib.parse import urlencode  # Converte dicionarios em strings de consulta (key=value&...)
from ..config import URL_FIT_CULTURAL # URL base definida nas variaveis de ambiente/configuracao

# ==============================
# Formatadores de Integracao
# ==============================



@validar
def formatar_url_fit(payload: dict = None) -> str:
    """
    Monta a URL do Fit Cultural utilizando ancoragem/fragmento (#).

    Esta abordagem e comum para passar tokens ou identificadores para
    aplicacoes front-end (React/Vue/Angular) que gerenciam o estado da
    rota atraves do HashRouter.

    Args:
        payload (dict | None): Dados que serao serializados (ex: {'email': 'user@test.com'}).

    Returns:
        str: URL completa formatada como "https://dominio.com/fit#chave=valor".
    """
    # Se o payload for nulo, inicializamos como dicionario vazio para evitar erros
    params = payload if payload is not None else {}

    # urlencode transforma {'id': 123, 'origem': 'web'} em "id=123&origem=web"
    fragmento_codificado = urlencode(params)

    # Retorna a concatenacao da URL base com o fragmento
    return f"{URL_FIT_CULTURAL}#{fragmento_codificado}"

# ==============================
# Exportacoes
# ==============================
__all__ = ["formatar_url_fit"]