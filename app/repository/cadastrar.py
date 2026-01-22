from .model import LeadPsel,Telefone,Email,db
from ..type import LeadPselInput


@validar
def cadastrar_lead_psel(data:LeadPselInput,id_podio:int) -> LeadPsel:
    # 1. Criar a instância principal do Lead
    novo_lead = LeadPsel(id_podio=id_podio, nome=data.nome, aiesec_mais_proxima=data.comite.nome)

    # 2. Inserir Emails (Lista de objetos do banco)
    # Convertemos cada item da lista do Pydantic para um modelo do SQLAlchemy
    novo_lead.emails = [Email(endereco=email.email) for email in data.emails]

    # 3. Inserir Telefones
    novo_lead.telefones = [Telefone(numero=telefone.numero) for telefone in data.telefones]

    # 4. Persistir no Banco
    db.session.add(novo_lead)
    db.session.commit()

    return novo_lead


__all__ = [
    "cadastrar_lead_psel"
]