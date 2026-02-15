"""
Controllers Registry
--------------------

Centraliza e expõe os controladores da camada HTTP. 
Este arquivo permite que as rotas importem a lógica de validação e 
orquestração de forma simplificada.
"""

# =================================================================
# Importações de Submódulos
# =================================================================

# Importa todas as funções exportadas pelo controlador do PSEL
# (ex: cadastrar_lead_psel_controller, validar_token_controller)
from .psel import *

# =================================================================
# Exportação Consolidada
# =================================================================



# O __all__ herda a lista de exportação definida no arquivo psel.py.
# Isso garante consistência: se você adicionar um novo controller no arquivo 
# base e incluí-lo no __all__ de lá, ele aparecerá aqui automaticamente.
__all__ = (
    psel.__all__
)