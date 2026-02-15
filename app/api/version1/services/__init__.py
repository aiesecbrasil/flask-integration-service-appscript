"""
Services Registry
-----------------

Centraliza e expõe a lógica de negócio (Services) da aplicação.
Este módulo orquestra a comunicação entre Repositories, Clientes Externos e DTOs.
"""

# =================================================================
# Importações de Submódulos
# =================================================================

# Importa todas as funções de serviço do PSEL (Processo Seletivo)
# como 'cadastrar_lead_psel_service' e 'validar_token_service'.
from .psel import *

# =================================================================
# Exportação Consolidada
# =================================================================



# O __all__ herda a lista de exportação definida no arquivo psel.py.
# Isso mantém o encapsulamento: se você criar funções auxiliares dentro
# de psel.py que não estejam no __all__ de lá, elas permanecerão
# privadas ao módulo e não serão expostas para os Controllers.
__all__ = [
    psel.__all__
]