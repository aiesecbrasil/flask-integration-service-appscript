from typing import Any
from urllib.parse import urlencode
from .. import Router
from app.repository import cadastrar_lead_psel
from app.schema import lead_schema
from app.cache import cache
from app.api import enviar_email_psel
from app.config import APP_ID_PSEL, URL_CONNECT
from app.repository import db,LeadPsel
from app.http import responses
from app.api import metadados,adicionar_lead,atualizar_lead,remover_lead
from app.type import LeadPselInput,LeadPselPodio,AtualizarPodioStatusFitCultural,ReponsePselPreCadastro

psel = Router(name="psel", url_prefix="/psel")



@psel.get("/metadados")
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

@psel.post("/inscricoes", responses={"201":ReponsePselPreCadastro})
def criar_incricao(body: LeadPselInput) -> tuple[dict[str, str], int] | dict[str, str | int | Any]:
    """
        Cria um card de lead interessado em participar da AIESEC assim como inicia o seu processo de inscrição.

        Args:
            body: (LeadPselInput): Dados do lead incluindo nome, emails, telefones e comitê.

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

    data = body # corpo de requisição recebido
    data_podio = None # dados da resposta recebida do podio
    novo_lead = None # dados que foram inseridos no banco de dados

    # INICIO DE VALIDADORES
    # AQUI VAI FICAR FUNÇÕES DE VALIDAÇÕES DE CONTEÚDO POIS TIPO É FEITO PELO FRAMEWORK
    # FIM DE VALIDADORES
    try:
        # monta padrão de envio de dados do podio
        dados_podio = LeadPselPodio(**data.model_dump()).to_json_podio()

        # cria a requisição para o podio
        data_podio, id_podio = adicionar_lead(chave="psel-token-podio", data=dados_podio,APP_ID=APP_ID_PSEL)

        # caso ocorre erro no podio e não criar usuário retorna esse erro
        if not id_podio:
            return responses.error(erro="Falha ao criar no Podio",status=502)

        # Cadastra Lead na Base de dados
        novo_lead = cadastrar_lead_psel(data,id_podio)

        # Atualizar Status do lead no podio para 203 que é o fit cultural enviado
        status_fit = AtualizarPodioStatusFitCultural(status=203).to_json_podio()
        atualizar_lead(chave="psel-token-podio", data=status_fit, data_response=data_podio)

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
        return responses.success(resposta.model_dump(), "Lead Criado com Sucesso", status=201)

    except Exception as e:
        # caso ocorra ERRO Impede dos dados no banco serem salvos caso estejam em transição
        db.session.rollback()
        print(f"Erro detectado: {str(e)}")

        # caso já tenha sido salvo quando ocorrer um erro ele o lead é apagado da base de dados
        if novo_lead and novo_lead.id:
            lead = db.session.get(LeadPsel,novo_lead.id)
            if lead:
                print(f"Id removido {lead.id_podio}")
                db.session.delete(novo_lead)
                db.session.commit()

        # Em caso de ERRO e o card no podio tiver sido criado ele é excluído para não ocorrer dados órfãos
        if data_podio:
            remover_lead("psel-token-podio", data_podio)

        print("RollBack Realizado")

        # RETORNO OBRIGATÓRIO EM CASO DE ERRO
        return responses.error( erro=str(e),details="Falha ao processar lead",status=500)

    finally:
        # Encerra o banco fechando suas instancias
        db.session.remove()

        # Limpa a resposta da requisição da memória
        if 'resposta' in locals(): del resposta

__all__ = ["psel"]
