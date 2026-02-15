"""
Schemas Module
--------------

Ponto central de acesso para os serializadores Marshmallow da aplicação.
Centraliza o acesso ao schema individual e de lista para a entidade LeadPsel.
"""

# ==============================
# Importações Agregadas
# ==============================

# Importa as instâncias e classes definidas no submódulo schema.py
from .schema import ma, LeadPselSchema, lead_schema, leads_schema

# ==============================
# Exportação Consolidada
# ==============================

# O __all__ garante que, ao fazer 'from app.schemas import *',
# apenas estes objetos específicos sejam carregados no namespace.
__all__ = [
    "ma",              # Instância do Flask-Marshmallow
    "LeadPselSchema",  # Classe base do Schema para tipagem ou extensões
    "lead_schema",     # Instância configurada para um único objeto (dict)
    "leads_schema"     # Instância configurada para coleções de objetos (list of dicts)
]