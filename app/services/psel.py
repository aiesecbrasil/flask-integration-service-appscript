from ..globals import Any
from ..repository import cadastrar_lead_psel
from ..schema import lead_schema
from ..repository import db,LeadPsel
from ..http import responses
from ..clients import enviar_email_psel,adicionar_lead,atualizar_lead,remover_lead
from ..config import APP_ID_PSEL, URL_CONNECT
from ..type import (LeadPselInput,LeadPselPodio,AtualizarPodioStatusFitCultural,ReponsePselPreCadastro,
                    ReponseOutPutPreCadastro)
from urllib.parse import urlencode
from pydantic import ValidationError

@validar
def cadastrar_lead_psel_service(data:LeadPselInput) -> Any:
    data_podio = None  # dados da resposta recebida do podio
    novo_lead = None  # dados que foram inseridos no banco de dados
    try:
        # monta padrão de envio de dados do podio
        dados_podio = LeadPselPodio(**data.model_dump()).to_json_podio()

        # cria a requisição para o podio
        data_podio, id_podio = adicionar_lead(chave="psel-token-podio", data=dados_podio.model_dump(), APP_ID=APP_ID_PSEL)

        # caso ocorre erro no podio e não criar usuário retorna esse erro
        if not id_podio:
            return responses.error(erro="Falha ao criar no Podio", status=502)

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
            "status_code": 201
        }).model_dump()

        return data,data.get("status_code")

    except (ValidationError,Exception) as e:
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

        # RETORNO OBRIGATÓRIO EM CASO DE ERRO
        return responses.error(erro=str(e), details="Falha ao processar lead", status=500)

    finally:
        # Encerra o banco fechando suas instancias
        db.session.remove()

        # Limpa a resposta da requisição da memória
        if 'resposta' in locals(): del resposta

__all__ = ["cadastrar_lead_psel_service"]