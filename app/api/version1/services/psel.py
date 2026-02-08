import logging
from app.repository import cadastrar_lead_psel,buscar_token_lead_psel
from app.schema import lead_schema
from app.repository import db,LeadPsel
from app.clients import enviar_email_psel,adicionar_lead,atualizar_lead,remover_lead
from app.config import APP_ID_PSEL
from app.core import URL_CONNECT
from app.dto import (LeadPselInput, LeadPselPodio, AtualizarPodioStatusFitCultural, ReponsePselPreCadastro,
                     ReponseOutPutPreCadastro, HttpStatus)
from app.globals import Any
from urllib.parse import urlencode
from pydantic import ValidationError

@validar
def cadastrar_lead_psel_service(data:LeadPselInput) -> tuple[ReponseOutPutPreCadastro,int]:
    data_podio = None  # dados da resposta recebida do podio
    id_podio = None # id ainda não recuperado do podio
    logger = logging.getLogger(__name__) # instancia do log
    try:
        # monta padrão de envio de dados do podio
        dados_podio = LeadPselPodio(**data.model_dump()).to_json_podio()

        #guardando dados de envio em variável
        dados_dump = dados_podio.model_dump()

        # cria a requisição para o podio
        data_podio, id_podio = adicionar_lead(chave="psel-token-podio", data=dados_dump, APP_ID=APP_ID_PSEL)

        # caso ocorre erro no podio e não criar usuário retorna esse erro
        if not id_podio:
            data = ReponseOutPutPreCadastro(**{
                "status": "error",
                "message": "Falha ao processar lead",
                "data": "id do podio não foi gerado ou encontrado",
                "status_code": HttpStatus.BAD_GATEWAY
            }).model_dump()
            # RETORNO OBRIGATÓRIO EM CASO DE ERRO
            return data, data.get("status_code")

        # Cadastra Lead na Base de dados, mas sem commitar
        novo_lead = cadastrar_lead_psel(data, id_podio,commit=False)

        # Atualizar Status do lead no podio para 203 que é o fit cultural enviado
        status_fit = AtualizarPodioStatusFitCultural(status=203).to_json_podio()
        status_dump = status_fit.model_dump()
        atualizar_lead(chave="psel-token-podio", data=status_dump, data_response=data_podio)

        # Cria paramentro de URL
        params = urlencode({
            "nome": novo_lead.nome,
            "id": novo_lead.id_podio,
            "token": novo_lead.token,
        })

        # criar o corpo da requisição que será enviado para o APP SCRIPT
        payload = {
            "url": f"https://{URL_CONNECT}/validarToken/?{params}",
            "emails": [email.endereco for email in novo_lead.emails],
            "nome": novo_lead.nome
        }

        # Dispara E-mail via APP SCRIPT enviando o payload como url parametrizada para validar o token e responder o fit
        enviar_email_psel(payload=payload)

        # criando o commit depois de ter sucesso
        db.session.commit()
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
def validar_token_service(token:str) -> Any:
    lead = buscar_token_lead_psel(token)

    return lead


__all__ = ["cadastrar_lead_psel_service"]