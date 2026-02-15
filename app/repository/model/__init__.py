"""
Models Module
-------------

Ponto central de acesso aos modelos ORM da aplicação.
Este módulo expõe a instância do banco de dados e as tabelas relacionadas
ao Processo Seletivo (PSEL) para facilitar o gerenciamento da persistência.
"""

# ==============================
# Importações de Entidades
# ==============================

# Importa a instância do banco e as classes de modelo do arquivo de definição
from .psel_db import db, LeadPsel, Email, Telefone

# ==============================
# Exportação Consolidada
# ==============================

# O __all__ define a interface pública deste pacote.
# Quando você fizer 'from app.models import *', apenas estes itens serão expostos.
__all__ = [
    "db",        # Instância do SQLAlchemy (Core)
    "LeadPsel",  # Entidade principal de candidatos
    "Email",     # Entidade de contatos de e-mail
    "Telefone"   # Entidade de contatos telefônicos
]