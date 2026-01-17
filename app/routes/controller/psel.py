from .. import Router
from app.repository import LeadPsel,Telefone,Email,db
from app.schema import lead_schema
from app.cache import cache
from app.services import HttpClient
from app.config import APP_ID_PSEL, APPSCRIPT_LEAD_PSEL
from app.globals import request
from app.http import responses
from app.api import metadados,adicionar_lead,atualizar_lead
from app.type import LeadPselInput,LeadPselPodio,AtualizarPodioStatusFitCultural,PselResponse

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
@typed
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

@psel.post("/teste")
@typed
def teste(data: LeadPselInput) -> PselResponse:
    # Esta linha força o editor a entender que 'data' é LeadPselInput
    # Isso agora FUNCIONA e o Python reconhece como objeto!
    try:
        # 1. Criar a instância principal do Lead
        novo_lead = LeadPsel(
            nome=data.nome,
            aiesec_mais_proxima=data.id_comite # Exemplo de mapeamento
        )

        # 2. Inserir Emails (Lista de objetos do banco)
        # Convertemos cada item da lista do Pydantic para um modelo do SQLAlchemy
        novo_lead.emails = [
            Email(endereco=e.email) for e in data.emails
        ]

        # 3. Inserir Telefones
        novo_lead.telefones = [
            Telefone(numero=t.numero) for t in data.telefones
        ]

        # 4. Persistir no Banco
        db.session.add(novo_lead)
        # Retornar a resposta para o Podio/AppScript
        dados_podio = LeadPselPodio(**data.model_dump())
        data_podio, id_podio = adicionar_lead(chave="psel-token-podio", data=dados_podio.to_json_podio(),
                                              APP_ID=APP_ID_PSEL)
        novo_lead.id_podio = id_podio # Aqui você colocaria o ID retornado pela API do Podio se já tivesse
        db.session.commit()
        status = AtualizarPodioStatusFitCultural(status=203)
        atualizar_lead(chave="psel-token-podio",data=status.to_json_podio(),data_response=data_podio)
        lead = lead_schema.dump(novo_lead)
        return lead

    except Exception as e:
        db.session.rollback()
        raise e

__all__ = ["psel"]
