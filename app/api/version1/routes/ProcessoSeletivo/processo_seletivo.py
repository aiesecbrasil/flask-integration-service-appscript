"""
Processo Seletivo (PSEL) Routes
-------------------------------

Define os endpoints para gestão de candidatos, incluindo busca de metadados,
inscrições (pré-cadastro) e validação de tokens de fit cultural.
"""

# ==============================
# Importações (Dependencies)
# ==============================
import logging  # Sistema de log para rastreamento de operações
from app.api.version1.routes import Router  # Nossa classe base de roteamento OpenAPI
from app.cache import cache  # Gerenciador de memória para evitar chamadas repetitivas
from app.clients import metadados  # Cliente que conversa com a API do Podio
from app.config import APP_ID_PSEL  # ID do App de PSEL no Podio (vindo do .env)
from app.dto import (  # Data Transfer Objects para validação de entrada/saída
    LeadPselInput,
    ExceptionErrorResponse,
    ParamsInput,
    Metadados,
    ReponseOutPutPreCadastro,
    ValidationErrorResponse
)
from app.api.version1.controller import (  # Lógica de negócio (Controllers) que processa os dados
    cadastrar_lead_psel_controller,
    validar_token_controller
)
from app.globals import Any  # Tipagem para flexibilidade em retornos específicos
from app.utils import resolve_exception
# =================================================================
# CONFIGURAÇÃO DO ROTEADOR ESPECÍFICO
# =================================================================

# Instancia o roteador para o PSEL. URL Final: /api/v1/processo-seletivo/...
processo_seletivo = Router(name="processo_seletivo", url_prefix="/processo-seletivo")
logger = logging.getLogger(__name__)


# =================================================================
# ENDPOINTS (ROTAS)
# =================================================================

@processo_seletivo.get("/metadados",responses={200:Metadados})
def buscar_metadados() -> dict:
    """
    Retorna a estrutura (campos) do App de PSEL no Podio.
    Utiliza Cache para não estourar o limite de requisições da API.
    """
    # 

    cache.get_or_set(
        key="metadados_card-psel",
        fetch=lambda: metadados(
            chave="psel-token-podio",  # Chave de acesso ao token no cache
            APP_ID=APP_ID_PSEL
        ),
        baixando="Metadados do Processo Seletivo"
    )
    return Metadados(**cache.store["metadados_card-psel"]).model_dump()


@processo_seletivo.post(
    "/inscricoes",
    responses={
        201: ReponseOutPutPreCadastro,
        422: ValidationErrorResponse,
        500: ExceptionErrorResponse
    },
)
def criar_incricao(body: LeadPselInput) -> tuple[ReponseOutPutPreCadastro, int]:
    """
    Pré-Cadastro para o Processo Seletivo AIESEC.

    Fluxo complexo de inscrição:
        1. Valida o input via LeadPselInput.
        2. Cria o card no Podio.
        3. Salva no Banco de Dados local.
        4. Dispara e-mail de confirmação via Google Script.
        5. Reverte operações (Rollback) em caso de falha em qualquer etapa.
    """
    try:
        # Delega a orquestração para o controller especializado
        return cadastrar_lead_psel_controller(body)
    except Exception as e:
        erro = resolve_exception(e)
        return erro.model_dump(), erro.status_code


@processo_seletivo.get("/validarToken", description="Rota responsável por validar token de fit cultural")
def validar_token(query: ParamsInput) -> Any:
    """
    Verifica se o token enviado pelo candidato via URL é válido para prosseguir com o teste de fit cultural.
    """
    # Extração de parâmetros validados pelo DTO ParamsInput (via Query String)
    id = query.id
    nome = query.nome
    token = query.token

    # Chama o controller que verifica a integridade do token no banco de dados
    return validar_token_controller(id, nome, token)


# ==============================
# Exportações do Módulo
# ==============================
__all__ = ["processo_seletivo", "validar_token"]