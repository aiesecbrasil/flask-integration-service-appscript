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
    novo_lead = None  # dados que foram inseridos no banco de dados
    try:
        # monta padrão de envio de dados do podio
        dados_podio = LeadPselPodio(**data.model_dump()).to_json_podio()

        # cria a requisição para o podio
        data_podio, id_podio = adicionar_lead(chave="psel-token-podio", data=dados_podio.model_dump(), APP_ID=APP_ID_PSEL)

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

        # Cadastra Lead na Base de dados
        novo_lead = cadastrar_lead_psel(data, id_podio)

        # Atualizar Status do lead no podio para 203 que é o fit cultural enviado
        status_fit = AtualizarPodioStatusFitCultural(status=203).to_json_podio()
        atualizar_lead(chave="psel-token-podio", data=status_fit.model_dump(), data_response=data_podio)

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
        print(f"Erro detectado: {str(e)}")

        # caso já tenha sido salvo quando ocorrer um erro ele o lead é apagado da base de dados
        if novo_lead and novo_lead.id:
            lead = db.session.get(LeadPsel, novo_lead.id)
            if lead:
                print(f"Id removido {lead.id_podio}")
                db.session.delete(novo_lead)
                db.session.commit()

        # Em caso de ERRO e o card no podio tiver sido criado ele é excluído para não ocorrer dados órfãos
        if data_podio:
            remover_lead("psel-token-podio", data_podio)

        print("RollBack Realizado")

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

        # Limpa a resposta da requisição da memória
        if 'resposta' in locals(): del resposta

@validar
def validar_token_service(token:str) -> Any:
    lead = buscar_token_lead_psel(token)

    return lead


__all__ = ["cadastrar_lead_psel_service"]