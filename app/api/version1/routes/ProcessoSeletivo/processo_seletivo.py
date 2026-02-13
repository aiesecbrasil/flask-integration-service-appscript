from app.api.version1.routes import Router
from app.cache import cache
from app.clients import metadados
from app.config import APP_ID_PSEL
from app.dto import LeadPselInput,ReponseOutPutPreCadastro,ParamsInput
from app.api.version1.controller import cadastrar_lead_psel_controller,validar_token_controller
from app.globals import Any

processo_seletivo = Router(name="processo_seletivo", url_prefix="/processo-seletivo")

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

@processo_seletivo.post("/inscricoes", responses={201:ReponseOutPutPreCadastro},description="Rota Responsavel pelo pré-cadastro de novos leads")
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

@processo_seletivo.get("/validarToken",description="Rota responsavel por validar token de fit cultural")
def validar_token(query:ParamsInput) -> Any:
    id = query.id
    nome = query.nome
    token = query.token
    return validar_token_controller(id,nome,token)

__all__ = ["processo_seletivo","validar_token"]
