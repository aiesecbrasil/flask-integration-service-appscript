"""
Repository Module
-----------------

Ponto central de acesso aos dados da aplicação.
Integra os modelos de banco de dados (SQLAlchemy) com as funções de
persistência (cadastrar) e consulta (buscar).
"""

# ==============================
# Importações de Infraestrutura
# ==============================
from .model import db, LeadPsel, Email, Telefone

# ==============================
# Importações de Operações
# ==============================
from .cadastrar import *
from .buscar import *

# ==============================
# Exportação Consolidada
# ==============================

# 

# O __all__ define a interface pública do repositório.
# Concatenamos as classes do modelo com as funções exportadas nos submódulos.
__all__ = [
    "db",
    "LeadPsel",
    "Email",
    "Telefone"
] + cadastrar.__all__ + buscar.__all__