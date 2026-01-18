from typing import Any
from .. import Router
from app.repository import LeadPsel,Telefone,Email,db
from app.schema import lead_schema
from app.cache import cache
from app.services import HttpClient
from app.config import APP_ID_PSEL, APPSCRIPT_LEAD_PSEL
from app.globals import request
from app.http import responses
from app.api import metadados,adicionar_lead,atualizar_lead,remover_lead,buscar_id_card
from app.type import LeadPselInput,LeadPselPodio,AtualizarPodioStatusFitCultural,ReponsePselPreCadastro

psel = Router(name="psel", url_prefix="/psel")
http = HttpClient()


@psel.get("/metadados")
def buscar_metadados():
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


@psel.post("/inscricoes")
def criar_incricao():
    """
    Adiciona um novo lead PSEL.
    Valida se os dados foram enviados e chama o AppScript correspondente.
    """
    data = request.get_json()
    if not data:
        return responses.error("Dados não enviados")

    # Aqui você pode adicionar validações específicas de PSEL, se necessário
    # Ex: validar campos obrigatórios
    status, result = http.post(
        APPSCRIPT_LEAD_PSEL,
        payload=data
    )

    return responses.success(data=result, status=201)

@psel.post("/teste", responses={"201":ReponsePselPreCadastro})
def teste(body: LeadPselInput) -> tuple[ReponsePselPreCadastro, int] | tuple[dict[str, str], int]:
    data = body
    data_podio = None
    # Esta linha força o editor a entender que 'data' é LeadPselInput
    # Isso agora FUNCIONA e o Python reconhece como objeto!
    try:
        # 1. Criar a instância principal do Lead
        novo_lead = LeadPsel(
            nome=data.nome,
            aiesec_mais_proxima=data.comite.nome # Exemplo de mapeamento
        )

        # 2. Inserir Emails (Lista de objetos do banco)
        # Convertemos cada item da lista do Pydantic para um modelo do SQLAlchemy
        novo_lead.emails = [
            Email(endereco=email.email) for email in data.emails
        ]

        # 3. Inserir Telefones
        novo_lead.telefones = [
            Telefone(numero=telefone.numero) for telefone in data.telefones
        ]

        # 4. Persistir no Banco
        db.session.add(novo_lead)
        # Retornar a resposta para o Podio/AppScript
        dados_podio = LeadPselPodio(**data.model_dump()).to_json_podio()
        data_podio, id_podio = adicionar_lead(chave="psel-token-podio", data=dados_podio,
                                              APP_ID=APP_ID_PSEL)
        novo_lead.id_podio = id_podio # Aqui você colocaria o ID retornado pela API do Podio se já tivesse
        status = AtualizarPodioStatusFitCultural(status=203).to_json_podio()
        atualizar_lead(chave="psel-token-podio", data=status, data_response=data_podio)
        db.session.commit()
        # Montagem exata para a classe
        saida_bruta = ReponsePselPreCadastro(**{
            "banco_de_dados": lead_schema.dump(novo_lead),
            "podio": dados_podio, # Certifique-se que isso é uma instância de ModelPodio
        })

        # model_dump() resolve o erro de serialização
        return saida_bruta.model_dump(),201

    except Exception as e:
        db.session.rollback()
        print(f"Erro detectado: {str(e)}")
        # Tenta remover do Podio se já tiver sido criado
        if data_podio:
            item_id = buscar_id_card(data_podio)
            if item_id:
                remover_lead("psel-token-podio", item_id)
        print("RollBack Realizado")
        # RETORNO OBRIGATÓRIO EM CASO DE ERRO
        return {"error": str(e), "message": "Falha ao processar lead"}, 500

__all__ = ["psel"]
