"""
Operações de escrita (cadastro) no repositório relacionadas ao PSEL.

Contém funções que traduzem DTOs em modelos persistentes do SQLAlchemy, com
controle de transação (commit opcional) para permitir orquestração em serviços.
"""
from .model import LeadPsel,Telefone,Email,db
from ..dto import LeadPselInput
from ..utils import gerar_token


@validar
def cadastrar_lead_psel(data:LeadPselInput,id_podio:int,commit:bool=True) -> LeadPsel:
    """
    Persiste um LeadPsel e suas relações (e-mails, telefones) a partir do DTO.

    Parâmetros:
    - data: LeadPselInput
        Dados de entrada validados (Pydantic) para criação do lead.
    - id_podio: int
        Identificador do item criado no Podio, armazenado no modelo.
    - commit: bool (default: True)
        Indica se deve efetuar commit imediatamente. Quando False, deixa a
        transação aberta para que o serviço decida o momento do commit/rollback.

    Retorno:
    - LeadPsel: Instância recém-persistida (pode estar pendente de commit).
    """
    # 1. Criar a instância principal do Lead
    novo_lead = LeadPsel(id_podio=id_podio,
                         nome=data.nome,
                         aiesec_mais_proxima=data.comite.nome,
                         token=gerar_token()
                )

    # 2. Inserir Emails (Lista de objetos do banco)
    # Convertemos cada item da lista do Pydantic para um modelo do SQLAlchemy
    novo_lead.emails = [Email(endereco=email.email) for email in data.emails]

    # 3. Inserir Telefones
    novo_lead.telefones = [Telefone(numero=telefone.numero) for telefone in data.telefones]

    # 4. Persistir no Banco
    db.session.add(novo_lead)

    if commit:
        db.session.commit()

    return novo_lead


__all__ = [
    "cadastrar_lead_psel"
]