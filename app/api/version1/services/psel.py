"""
Serviços do Processo Seletivo (PSEL).

Este módulo orquestra o cadastro de leads no Podio, a persistência no banco de
dados e o envio do e-mail para realização do Fit Cultural via App Script.
"""

# ==============================
# Importações (Dependencies)
# ==============================
import logging                               # Registro de eventos e erros
from flask import redirect                   # Redirecionamento HTTP para o Fit Cultural
from typing import Any                       # Tipagem flexível
from app.repository import (                 # Camada de Dados (Consultas e Escrita)
    cadastrar_lead_psel,
    buscar_lead_psel,
    buscar_data_expiracao,
    db                                       # Instância do SQLAlchemy
)
from app.schema import lead_schema           # Serializador para transformar objeto DB em JSON
from app.clients import (                    # Clientes de integração externa
    enviar_email_psel,
    adicionar_lead,
    atualizar_lead,
    remover_lead
)
from app.config import APP_ID_PSEL           # ID do App no Podio
from app.core import URL_CONNECT             # URL base da nossa API
from app.dto import (                        # Objetos de Transferência de Dados
    LeadPselInput,
    LeadPselPodio,
    AtualizarPodioStatusFitCultural,
    ReponseOutPutPreCadastro,
    HttpStatus
)
from app.utils import agora_sem_timezone, formatar_url,resolve_exception
from app.helper import formatar_url_fit,payload_podio     # Helper para gerar URL do formulário externo

# =================================================================
# SERVIÇO: CADASTRO COMPLETO (ORQUESTRAÇÃO)
# =================================================================



@validar
def cadastrar_lead_psel_service(data: LeadPselInput) -> ReponseOutPutPreCadastro | Any:
    """
    Fluxo de Cadastro com Garantia de Consistência (Rollback Multi-sistema).
    """
    data_podio = None  # Referência para o item criado no Podio (para possível deleção)
    id_podio = None
    logger = logging.getLogger(__name__)

    try:
        # 1. INTEGRAÇÃO PODIO: Criar o Card
        logger.info("Iniciando fluxo no Podio...")
        dados_podio = LeadPselPodio(**data.model_dump()).to_podio_payload()

        data_podio, id_podio = adicionar_lead(
            chave="psel-token-podio",
            data=payload_podio(dados_podio),
            APP_ID=APP_ID_PSEL
        )

        if not id_podio:
            erro = resolve_exception(Exception("Falha crítica: Podio não retornou ID do item."))
            return erro.model_dump(),erro.status_code

        # 2. BANCO DE DADOS: Persistência Local (Sem Commit)
        logger.info("Persistindo lead no banco de dados local...")
        # commit=False mantém a transação aberta para rollback em caso de erro posterior
        novo_lead = cadastrar_lead_psel(data, id_podio, commit=False)

        # 3. ATUALIZAÇÃO PODIO: Status 'E-mail Enviado'
        # Atualizamos o card recém-criado para o estágio de Fit Cultural (Status 203)
        status_fit = AtualizarPodioStatusFitCultural(status=203).to_podio_payload()
        atualizar_lead(chave="psel-token-podio", data=payload_podio(status_fit), data_response=data_podio)

        # 4. GOOGLE APPS SCRIPT: Disparo de E-mail
        params = {"nome": novo_lead.nome, "id": novo_lead.id_podio, "token": novo_lead.token}
        url_validacao = f"http://{URL_CONNECT}/api/v1/processo-seletivo/validarToken"

        payload_email = {
            "url": formatar_url(url_validacao, params),
            "emails": [email.endereco for email in novo_lead.emails],
            "nome": novo_lead.nome
        }
        enviar_email_psel(payload=payload_email)

        # 5. FINALIZAÇÃO: Commit de segurança
        db.session.commit()
        logger.info(f"Processo concluído com sucesso para o Lead {id_podio}!")
        lead_cadastrado = lead_schema.dump(novo_lead)
        # Montagem da resposta de sucesso
        resposta = ReponseOutPutPreCadastro(
            status="success",
            message="Lead cadastrado e e-mail enviado!",
            podio=dados_podio,
            banco_de_dados=lead_cadastrado,
            status_code=HttpStatus.CREATED
        )
        return resposta.model_dump(), resposta.status_code

    except Exception as e:
        # MECANISMO DE ROLLBACK: Se o e-mail falhar, não salvamos no banco e limpamos o Podio.
        db.session.rollback()
        logger.exception(f"Erro no serviço. Iniciando Rollback: {str(e)}")

        if data_podio:
            remover_lead("psel-token-podio", data_podio)
            logger.warning(f"Card {id_podio} removido do Podio para evitar dados órfãos.")
        erro = resolve_exception(e)
        return erro.model_dump(),erro.status_code

    finally:
        db.session.remove()

# =================================================================
# SERVIÇO: VALIDAÇÃO DE TOKEN E REDIRECIONAMENTO
# =================================================================



@validar
def validar_token_service(id: int, nome: str, token: str) -> Any:
    """
    Valida a segurança e expiração do token antes de liberar o acesso ao Fit Cultural.
    """
    try:
        # Verificações de segurança (Fail-Fast)
        if not buscar_lead_psel(token):
            return {"erro": "Token inexistente"}, HttpStatus.UNAUTHORIZED

        if not buscar_lead_psel(id=id, token=token):
            return {"erro": "Token não pertence a este candidato"}, HttpStatus.UNAUTHORIZED

        if agora_sem_timezone() > buscar_data_expiracao(id):
            return {"erro": "Link expirado. Solicite um novo link."}, HttpStatus.UNAUTHORIZED

        # Redirecionamento 301 para o Typeform/Google Forms parametrizado
        target_url = formatar_url_fit({"id": id, "nome": nome})
        return redirect(target_url), HttpStatus.MOVED_PERMANENTLY

    except Exception as e:
        erro = resolve_exception(e)
        return erro.model_dump(), erro.status_code

__all__ = ["cadastrar_lead_psel_service", "validar_token_service"]