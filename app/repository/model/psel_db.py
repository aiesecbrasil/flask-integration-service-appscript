"""
Modelos ORM relacionados ao Processo Seletivo (PSEL).

Define as entidades persistidas na base de dados para controle de leads, seus
contatos e metadados de expiração/validação.
"""
from app.utils import agora,expiracao_3dias,gerar_token
from app.core import db


class LeadPsel(db.Model):
    """
    Representa um lead do Processo Seletivo.

    Campos principais:
    - id: PK autoincremental
    - id_podio: Identificador do item no Podio (único)
    - nome: Nome do candidato
    - aiesec_mais_proxima: Escritório AIESEC mais próximo informado
    - data_criacao: Data/hora em que o lead foi criado
    - expiracao: Data/hora de expiração do token (72h após criação)
    - token: Token único para validação/acesso do candidato

    Relacionamentos:
    - emails: Lista de e-mails associados (cascade all, delete-orphan)
    - telefones: Lista de telefones associados (cascade all, delete-orphan)
    """
    __tablename__ = "lead_psel"
    id = db.Column(db.Integer, primary_key=True)
    id_podio = db.Column(db.Integer,unique=True,nullable=False)
    nome = db.Column(db.String(255), nullable=False)

    # Relacionamentos
    emails = db.relationship('Email', backref='lead_psel', cascade="all, delete-orphan")
    telefones = db.relationship('Telefone', backref='lead_psel', cascade="all, delete-orphan")

    # Outros campos
    aiesec_mais_proxima = db.Column(db.String(255),nullable=False)
    data_criacao = db.Column(db.DateTime, default=agora)  # junta dia/mês/ano
    expiracao = db.Column(db.DateTime, default=expiracao_3dias)
    token = db.Column(db.String(255), default=gerar_token,unique=True, nullable=False)


class Email(db.Model):
    """Modelo de e-mail vinculado a um LeadPsel."""
    id = db.Column(db.Integer, primary_key=True)
    endereco = db.Column(db.String(150), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('lead_psel.id'), nullable=False)


class Telefone(db.Model):
    """Modelo de telefone vinculado a um LeadPsel."""
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(30), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('lead_psel.id'), nullable=False)


__all__ = [
    "db",
    "LeadPsel",
    "Email",
    "Telefone"
]