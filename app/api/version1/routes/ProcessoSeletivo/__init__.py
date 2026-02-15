"""
PSEL Routes Entry Point
-----------------------

Este módulo consolida as rotas do Processo Seletivo para exportação limpa.
"""

# =================================================================
# Importações de Submódulos
# =================================================================

# Importa o roteador 'processo_seletivo' e suas rotas (/metadados, /inscricoes, etc.)
# definidas no arquivo processo_seletivo.py
from .processo_seletivo import *

# =================================================================
# Exportação Consolidada
# =================================================================



# O __all__ limita a exposição ao objeto de roteamento configurado.
# Isso permite que o roteador de versões (version1/routes.py) faça:
# from .ProcessoSeletivo import processo_seletivo
__all__ = [
    "processo_seletivo"
]