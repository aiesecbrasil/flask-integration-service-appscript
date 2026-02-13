"""
Serviços do Processo Seletivo (PSEL).

Este módulo orquestra o cadastro de leads no Podio, a persistência no banco de
dados e o envio do e-mail para realização do Fit Cultural via App Script, além
da validação do token recebido pelo candidato.

Fluxos principais:
- cadastrar_lead_psel_service: cria o card no Podio, cadastra o lead no banco,
  atualiza o status no Podio e dispara o e-mail de Fit Cultural.
- validar_token_service: valida o token de acesso do candidato e redireciona
  para a URL do formulário de Fit Cultural quando válido.
"""
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
    """
    Cadastra um lead do PSEL, cria o item no Podio e envia o e-mail de Fit Cultural.

    Etapas do fluxo:
    - Monta o payload de envio para o Podio a partir do DTO recebido.
    - Cria o item (card) no Podio e valida o retorno (id do Podio).
    - Persiste o lead no banco de dados (transação pendente até commit).
    - Atualiza o status do lead no Podio para "Fit cultural enviado" (203).
    - Gera a URL parametrizada para validação do token e envia o e-mail via App Script.
    - Realiza commit da transação ao final do processamento bem-sucedido.

    Tratamento de erros:
    - Em caso de exceção, executa rollback e remove o card no Podio (se criado),
      retornando uma resposta padronizada de erro.

    Parâmetros:
    - data: LeadPselInput
        Objeto de entrada contendo os dados necessários para cadastro e envio ao Podio.

    Retorno:
    - tuple[ReponseOutPutPreCadastro, int]
        Tupla contendo o payload padronizado de resposta e o status code HTTP.
    """
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
    """
    Valida o token de acesso do candidato e redireciona para o formulário de Fit Cultural.

    Regras de validação:
    - Verifica se o token existe e está ativo.
    - Garante que o token pertence ao lead (id_podio) informado.
    - Checa se o token não está expirado.

    Em caso de sucesso, retorna um redirecionamento (HTTP 301) para a URL do Fit Cultural.

    Parâmetros:
    - id: int
        Identificador do lead no Podio.
    - nome: str
        Nome do candidato, utilizado na composição da URL.
    - token: str
        Token enviado ao candidato por e-mail.

    Retorno:
    - tuple[dict[str, str] | Response, int]
        Em caso de erro, retorna um dicionário com a mensagem e o status HTTP.
        Em caso de sucesso, retorna o redirect para a URL do Fit Cultural e o status HTTP.
    """
    try:
        # valida se o tokn existe
        if not buscar_token_lead_psel(token):
            return {"erro":"Token Inválido"},HttpStatus.UNAUTHORIZED
        # verifica se o token é daquele lead
        if not buscar_token_id_podio_lead_psel(id,token):
            return {"erro":"Token não pertence a esse usuário"},HttpStatus.UNAUTHORIZED
        # verifica se já não expirou
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