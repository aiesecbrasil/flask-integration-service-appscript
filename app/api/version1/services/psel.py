import logging
from flask import redirect
from typing import Any
from pydantic import ValidationError
from app.repository import cadastrar_lead_psel,buscar_token_lead_psel,buscar_token_id_podio_lead_psel\
    ,buscar_data_expiracao
from app.schema import lead_schema
from app.repository import db
from app.clients import enviar_email_psel,adicionar_lead,atualizar_lead,remover_lead
from app.config import APP_ID_PSEL
from app.core import URL_CONNECT
from app.dto import (LeadPselInput, LeadPselPodio, AtualizarPodioStatusFitCultural, ReponsePselPreCadastro,
                     ReponseOutPutPreCadastro, HttpStatus)
from app.utils import agora_sem_timezone,formatar_url
from app.helper import formatar_url_fit

@validar
def cadastrar_lead_psel_service(data:LeadPselInput) -> tuple[ReponseOutPutPreCadastro,int]:
    data_podio = None  # dados da resposta recebida do podio
    id_podio = None # id ainda não recuperado do podio
    logger = logging.getLogger(__name__) # instancia do log
    try:
        logger.info("Cadastrando lead no podio...")
        # monta padrão de envio de dados do podio
        dados_podio = LeadPselPodio(**data.model_dump()).to_json_podio()
        #guardando dados de envio em variável
        dados_dump = dados_podio.model_dump()

        # cria a requisição para o podio
        data_podio, id_podio = adicionar_lead(
            chave="psel-token-podio",
            data=dados_dump,
            APP_ID=APP_ID_PSEL,
        )
        logger.info(f"Lead {id_podio} cadastrado no podio com sucesso!")

        # caso ocorre erro no podio e não criar usuário retorna esse erro
        if not id_podio:
            logger.error("id do podio não foi gerado ou encontrado")
            data = ReponseOutPutPreCadastro(**{
                "status": "error",
                "message": "Falha ao processar lead",
                "data": "id do podio não foi gerado ou encontrado",
                "status_code": HttpStatus.BAD_GATEWAY
            }).model_dump()
            # RETORNO OBRIGATÓRIO EM CASO DE ERRO
            return data, data.get("status_code")
        logger.info("Cadastrando lead no Banco de dados...")
        # Cadastra Lead na Base de dados, mas sem commitar
        novo_lead = cadastrar_lead_psel(data, id_podio,commit=False)

        # Atualizar Status do lead no podio para 203 que é o fit cultural enviado
        logger.info("Atualizando Status do lead para fit cultural enviado...")
        status_fit = AtualizarPodioStatusFitCultural(status=203).to_json_podio()
        status_dump = status_fit.model_dump()
        atualizar_lead(chave="psel-token-podio", data=status_dump, data_response=data_podio)
        logger.info("Status do lead atualizado para fit cultural enviado com sucesso!")
        # Cria paramentro de URL
        params = {
            "nome": novo_lead.nome,
            "id": novo_lead.id_podio,
            "token": novo_lead.token,
        }
        url = f"http://{URL_CONNECT}/api/v1/processo-seletivo/validarToken"
        # criar o corpo da requisição que será enviado para o APP SCRIPT
        payload = {
            "url":formatar_url(url,params),
            "emails": [email.endereco for email in novo_lead.emails],
            "nome": novo_lead.nome
        }

        logger.info("Enviando e-mail para responder fit cultural...")
        # Dispara E-mail via APP SCRIPT enviando o payload como url parametrizada para validar o token e responder o fit
        enviar_email_psel(payload=payload)
        logger.info("E-mail fit cultural enviado com sucesso!")

        # criando o commit depois de ter sucesso
        db.session.commit()
        logger.info("Lead cadastro no Banco de dados com sucesso!")
        # Montagem exata para a classe
        resposta = ReponsePselPreCadastro(**{
            "banco_de_dados": lead_schema.dump(novo_lead),
            "podio": dados_podio,
        })

        # Resposta da rota
        data = ReponseOutPutPreCadastro(**{
            "status": "success",
            "message": "Operação realizada com sucesso",
            "data": resposta,
            "status_code": HttpStatus.CREATED
        }).model_dump()

        return data,data.get("status_code")

    except (ValidationError,Exception,TypeError) as e:
        # caso ocorra ERRO Impede dos dados no banco serem salvos caso estejam em transição
        db.session.rollback()

        # Log Informando a exceção
        logger.exception(f"Falha no processamento do Lead: {str(e)}")

        # Em caso de ERRO e o card no podio tiver sido criado ele é excluído para não ocorrer dados órfãos
        if data_podio:
            remover_lead("psel-token-podio", data_podio)
            logger.warning(f"Lead {id_podio} removido do podio")

        logger.info("RollBack Realizado")

        data = ReponseOutPutPreCadastro(**{
            "status": "error",
            "message": "Falha ao processar lead",
            "data": str(e),
            "status_code": HttpStatus.INTERNAL_ERROR
        }).model_dump()

        # RETORNO OBRIGATÓRIO EM CASO DE ERRO
        return data,data.get("status_code")

    finally:
        # Encerra o banco fechando suas instancias
        db.session.remove()

@validar
def validar_token_service(id:int,nome:str,token:str) -> tuple[dict[str, str], int] | Any:
    try:
        if not buscar_token_lead_psel(token):
            return {"erro":"Token Inválido"},HttpStatus.UNAUTHORIZED
        if not buscar_token_id_podio_lead_psel(id,token):
            return {"erro":"Token não pertence a esse usuário"},HttpStatus.UNAUTHORIZED
        if agora_sem_timezone() > buscar_data_expiracao(id):
            return {"erro": "Token Expirado"},HttpStatus.UNAUTHORIZED
        payload = {
            "id":id,
            "nome":nome
        }
        return redirect(formatar_url_fit(payload)),HttpStatus.MOVED_PERMANENTLY
    except Exception as e:
        return {"erro":str(e)},HttpStatus.INTERNAL_ERROR


__all__ = ["cadastrar_lead_psel_service","validar_token_service"]