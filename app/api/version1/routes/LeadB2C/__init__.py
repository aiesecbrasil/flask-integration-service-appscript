"""
OGX Routes Entry Point
----------------------

Este módulo consolida as rotas de Novos Leads B2C (Intercâmbio) para exportação.
Atua como o ponto de acesso para o roteador de versões da API.
"""

# =================================================================
# Importações de Submódulos
# =================================================================

# Importa o roteador 'new_lead_ogx' e seus endpoints (/metadados, /inscricoes)
# definidos no arquivo new_lead_ogx.py
from .new_lead_ogx import *

# =================================================================
# Exportação Consolidada
# =================================================================



# O __all__ garante que apenas a instância do roteador configurado seja exposta.
# Isso mantém a integridade do sistema de rotas, permitindo que o roteador
# global (version1/routes.py) registre este módulo de forma limpa:
# v1.register_api(new_lead_ogx)
__all__ = [
    "new_lead_ogx"
]