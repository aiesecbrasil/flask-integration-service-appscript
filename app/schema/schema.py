from ..core import ma
from ..repository.model import LeadPsel, Email, Telefone
# Importe diretamente da biblioteca base para garantir
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class EmailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Email
        load_instance = True  # Permite criar instâncias do modelo ao carregar dados
        include_fk = True     # Inclui a chave estrangeira no JSON se necessário
        exclude = ("id",)

class TelefoneSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Telefone
        load_instance = True
        include_fk = True  # Inclui a chave estrangeira no JSON se necessário
        exclude = ("id",)

class LeadPselSchema(ma.SQLAlchemyAutoSchema):
    # Relacionamentos Aninhados
    emails = ma.Nested(EmailSchema, many=True)
    telefones = ma.Nested(TelefoneSchema, many=True)

    class Meta:
        model = LeadPsel
        load_instance = True
        # Podemos excluir campos sensíveis ou internos da resposta da API
        exclude = ("id",)

# Instâncias para uso rápido
lead_schema = LeadPselSchema()
leads_schema = LeadPselSchema(many=True)

__all__ = [
    "ma",
    "LeadPselSchema",
    "EmailSchema",
    "TelefoneSchema"
]