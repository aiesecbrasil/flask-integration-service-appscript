"""
Routes Inventory
----------------

Este módulo centraliza a importação de todos os controllers (blueprints)
especializados da aplicação, facilitando o registro em massa no roteador v1.
"""

# ==============================
# Importações (Dependencies)
# ==============================

# Importa a classe Router customizada (baseada no Flask-OpenAPI3)
from .router import Router

# Importa as rotas relacionadas ao Processo Seletivo (Inscrições, Membros)
from .ProcessoSeletivo import *

# Importa as rotas relacionadas ao LeadB2C (Intercâmbios/OGX)
from .LeadB2C import *

# =================================================================
# EXPORTAÇÃO DE RECURSOS
# =================================================================



# O __all__ define quais objetos estarão disponíveis quando este módulo
# for importado via 'from .routes import *'.
# Ele expõe os roteadores específicos que já foram instanciados
# dentro de seus respectivos arquivos.
__all__ = [
    "Router",            # A classe base para criação de novos módulos
    "processo_seletivo", # O blueprint de rotas do PSEL
    "new_lead_ogx"       # O blueprint de rotas de Intercâmbio
]