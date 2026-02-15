"""
Operações de escrita (cadastro) no repositório relacionadas ao PSEL.

Contém funções que traduzem DTOs em modelos persistentes do SQLAlchemy, com
controle de transação (commit opcional) para permitir orquestração em serviços.
"""

# ==============================
# Importações (Dependencies)
# ==============================
from .model import LeadPsel, Telefone, Email, db  # Modelos SQLAlchemy e instância do banco
from ..dto import LeadPselInput                    # Data Transfer Object para validação de entrada
from ..utils import gerar_token                   # Utilitário para criar tokens de acesso únicos

# ==============================
# Persistência de Dados
# ==============================

@validar
def cadastrar_lead_psel(data: LeadPselInput, id_podio: int, commit: bool = True) -> LeadPsel:
    """
    Persiste um LeadPsel e suas relações (e-mails, telefones) no banco de dados.

    A função mapeia os campos do DTO para o modelo ORM e gerencia a árvore de
    objetos relacionados. O uso do parâmetro 'commit' permite que esta função
    seja usada dentro de transações maiores (Atomicidade).



    Args:
        data (LeadPselInput): DTO validado contendo os dados do formulário.
        id_podio (int): ID de referência do item criado no CRM Podio.
        commit (bool): Se True, finaliza a transação imediatamente.
                       Se False, mantém os objetos na sessão para commit posterior.

    Returns:
        LeadPsel: A instância do Lead criada, já vinculada à sessão do banco.
    """

    # 1. Instanciação da entidade principal
    # O token é gerado automaticamente para permitir identificação futura segura
    novo_lead = LeadPsel(
        id_podio=id_podio,
        nome=data.nome,
        aiesec_mais_proxima=data.comite.nome,
        token=gerar_token()
    )

    # 2. Conversão e Vínculo de E-mails
    # Graças ao relacionamento do SQLAlchemy, ao adicionar na lista 'emails',
    # o FK (Foreign Key) é preenchido automaticamente no momento do flush.
    novo_lead.emails = [
        Email(endereco=item.email) for item in data.emails
    ]

    # 3. Conversão e Vínculo de Telefones
    novo_lead.telefones = [
        Telefone(numero=item.numero) for item in data.telefones
    ]

    # 4. Adição ao contexto de persistência
    db.session.add(novo_lead)

    # Controle de Transação
    # Se commit for False, o desenvolvedor pode realizar outras operações
    # antes de salvar tudo de uma vez, garantindo que não fiquem dados órfãos.
    if commit:
        db.session.commit()

    return novo_lead

# ==============================
# Exportações
# ==============================
__all__ = [
    "cadastrar_lead_psel"
]