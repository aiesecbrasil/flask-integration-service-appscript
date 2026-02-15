"""
Modelos ORM relacionados ao Processo Seletivo (PSEL).

Define as entidades persistidas na base de dados para controle de leads, seus
contatos e metadados de expiração/validação.
"""

# ==============================
# Importações (Dependencies)
# ==============================
from app.utils import agora, expiracao_3dias, gerar_token  # Utilitários de tempo e segurança
from app.core import db  # Instância do SQLAlchemy vinculada à aplicação


# ==============================
# Entidade Principal
# ==============================

class LeadPsel(db.Model):
    """
    Representa um lead (candidato) do Processo Seletivo.

    Esta entidade centraliza as informações do candidato e gerencia o ciclo de vida
    do seu acesso através de tokens e datas de expiração.

    Attributes:
        id (int): Chave primária interna do sistema.
        id_podio (int): Identificador único do item no CRM Podio (Sincronização).
        nome (str): Nome completo ou formatado do candidato.
        aiesec_mais_proxima (str): Nome do comitê local de referência.
        data_criacao (datetime): Momento do registro (Padrão: Horário de Brasília).
        expiracao (datetime): Prazo de validade do acesso (Padrão: +72h).
        token (str): String aleatória única para autenticação sem senha.
    """
    __tablename__ = "lead_psel"

    id = db.Column(db.Integer, primary_key=True)
    id_podio = db.Column(db.Integer, unique=True, nullable=False)
    nome = db.Column(db.String(255), nullable=False)

    # Relacionamentos (One-to-Many)
    #

    # cascade="all, delete-orphan": Garante que se um Lead for deletado, seus
    # e-mails e telefones também serão removidos do banco automaticamente.
    emails = db.relationship('Email', backref='lead_psel', cascade="all, delete-orphan")
    telefones = db.relationship('Telefone', backref='lead_psel', cascade="all, delete-orphan")

    # Metadados e Controle de Acesso
    aiesec_mais_proxima = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.DateTime, default=agora)
    expiracao = db.Column(db.DateTime, default=expiracao_3dias)
    token = db.Column(db.String(255), default=gerar_token, unique=True, nullable=False)


# ==============================
# Entidades de Contato
# ==============================

class Email(db.Model):
    """
    Modelo de e-mail vinculado a um LeadPsel.

    Armazena os múltiplos endereços de e-mail que um único candidato pode possuir.
    """
    __tablename__ = "email"
    id = db.Column(db.Integer, primary_key=True)
    endereco = db.Column(db.String(150), nullable=False)

    # Chave estrangeira ligando o e-mail ao Lead correspondente
    usuario_id = db.Column(db.Integer, db.ForeignKey('lead_psel.id'), nullable=False)


class Telefone(db.Model):
    """
    Modelo de telefone vinculado a um LeadPsel.

    Armazena os contatos telefônicos (celular/fixo) do candidato.
    """
    __tablename__ = "telefone"
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(30), nullable=False)

    # Chave estrangeira ligando o telefone ao Lead correspondente
    usuario_id = db.Column(db.Integer, db.ForeignKey('lead_psel.id'), nullable=False)


# ==============================
# Exportações
# ==============================
__all__ = [
    "db",
    "LeadPsel",
    "Email",
    "Telefone"
]