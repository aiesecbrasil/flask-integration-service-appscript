"""
Schemas Marshmallow-SQLAlchemy para serialização das entidades do PSEL.

Fornece schemas para LeadPsel, Email e Telefone, com campos/relacionamentos
necessários para respostas de API.
"""

# ==============================
# Importações (Dependencies)
# ==============================
from ..core import ma  # Instância global do Flask-Marshmallow
from ..repository.model import LeadPsel, Email, Telefone  # Modelos do banco de dados (SQLAlchemy)
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema  # Classe base para geração automática de schemas

# ==============================
# Schemas de Apoio (Relacionados)
# ==============================

class EmailSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema de serialização para a entidade de E-mails.

    Este schema converte os registros da tabela 'Email' em objetos JSON.
    """
    class Meta:
        model = Email
        load_instance = True  # Permite que o marshmallow crie objetos da classe 'Email' no .load()
        include_fk = True     # Exibe explicitamente a chave estrangeira (ID do Lead) no JSON
        exclude = ("id",)     # Oculta o ID interno do banco para manter a resposta limpa

class TelefoneSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema de serialização para a entidade de Telefones.
    """
    class Meta:
        model = Telefone
        load_instance = True
        include_fk = True
        exclude = ("id",)

# ==============================
# Schema Principal
# ==============================

class LeadPselSchema(ma.SQLAlchemyAutoSchema):
    """
    Schema mestre para o LeadPsel.

    Realiza a composição de dados, aninhando as listas de e-mails e telefones
    dentro do objeto principal do Lead.
    """

    #

    # Relacionamentos Aninhados: Define como os objetos filhos devem aparecer no JSON
    # 'many=True' indica que um Lead pode possuir uma lista desses itens
    emails = ma.Nested(EmailSchema, many=True)
    telefones = ma.Nested(TelefoneSchema, many=True)

    class Meta:
        model = LeadPsel
        load_instance = True
        # Exclui o 'id' para que a identificação seja feita por outros campos (ex: e-mail)
        exclude = ("id",)

# ==============================
# Instâncias de Atalho
# ==============================

# Objeto único: usado em rotas de detalhes (ex: GET /lead/1)
lead_schema = LeadPselSchema()

# Lista de objetos: usado em rotas de listagem (ex: GET /leads)
leads_schema = LeadPselSchema(many=True)

# ==============================
# Exportações
# ==============================
__all__ = [
    "ma",
    "LeadPselSchema",
    "EmailSchema",
    "TelefoneSchema",
    "lead_schema",
    "leads_schema"
]