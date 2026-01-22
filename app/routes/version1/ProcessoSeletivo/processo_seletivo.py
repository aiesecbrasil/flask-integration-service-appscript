from typing import Any
from app.routes import Router
from app.cache import cache
from app.clients import metadados
from app.config import APP_ID_PSEL
from app.type import LeadPselInput,ReponseOutPutPreCadastro
from app.controller import cadastrar_lead_psel_controller

processo_seletivo = Router(name="Processo Seletivo", url_prefix="/processo-seletivo")

@processo_seletivo.get("/metadados")
def buscar_metadados() -> dict:
    #criar futuramente o tipo Cache
    """
    Retorna os metadados dos leads PSEL.
    Cache de acordo com CACHE_TTL.
    """
    cache.get_or_set(
        key="metadados_card-psel",
        fetch=lambda: metadados(
            chave="psel-token-podio",
            APP_ID=APP_ID_PSEL
        )
    )
    return cache.store["metadados_card-psel"]

@processo_seletivo.post("/inscricoes", responses={201:ReponseOutPutPreCadastro},)
def criar_incricao(body: LeadPselInput) -> tuple[ReponseOutPutPreCadastro, int]:
    """
        Cria um card de lead interessado em participar da AIESEC assim como inicia o seu processo de inscrição.

        Args:
            body (LeadPselInput): Dados do lead incluindo nome, emails, telefones e comitê.

        Returns:
            dict: Um dicionário com as chaves:
                - status (str): Indica se a operação foi bem-sucedida.
                - message (str): Mensagem de sucesso ou erro.
                - data (dict): Dados do lead criado, incluindo:
                    - banco_de_dados (dict): Informações do lead na base local.
                    - podio (dict): Dados retornados pelo Podio.

        Raises:
            Exception: Erro ao criar lead no Podio, persistir no banco de dados ou enviar e-mail via AppScript.

        Notes:
            - Caso ocorra erro após criar lead no Podio ou no banco, ambos serão revertidos.
            - O payload de e-mail é enviado para o AppScript com a URL parametrizada do lead.
    """
    return cadastrar_lead_psel_controller(body)

__all__ = ["processo_seletivo"]
