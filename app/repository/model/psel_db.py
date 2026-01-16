from flask_sqlalchemy import SQLAlchemy
from app.utils import agora,expiracao_3dias,gerar_token

db = SQLAlchemy()

class LeadPsel(db.Model):
    __tablename__ = "lead_psel"
    id = db.Column(db.Integer, primary_key=True)
    id_podio = db.Column(db.Integer,unique=True,nullable=False)
    nome = db.Column(db.String(255), nullable=False)

    # Relacionamentos
    emails = db.relationship('Email', backref='lead_psel', cascade="all, delete-orphan")
    telefones = db.relationship('Telefone', backref='lead_psel', cascade="all, delete-orphan")

    # Outros campos
    aiesec_mais_proxima = db.Column(db.Integer,nullable=False)
    data_criacao = db.Column(db.DateTime, default=agora)  # junta dia/mês/ano
    expiracao = db.Column(db.DateTime, default=expiracao_3dias)
    token = db.Column(db.String(255), default=gerar_token,unique=True, nullable=False)


class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    endereco = db.Column(db.String(150), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('lead_psel.id'), nullable=False)


class Telefone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(30), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('lead_psel.id'), nullable=False)


__all__ = [
    "db",
    "LeadPsel",
    "Email",
    "Telefone"
]