"""
DTOs (Data Transfer Objects)
----------------------------

Este pacote centraliza todos os contratos de dados da aplicação.
Divide-se em 'input' para validação de requisições e 'response' para
formatação de respostas e integrações.
"""

# =================================================================
# Importações de Pacotes (Subdiretórios)
# =================================================================

# Importa todas as definições de entrada (Leads, Parâmetros, etc.)
from .input import *

# Importa todas as definições de saída (Status HTTP, Envelopes Podio, etc.)
from .response import *

from .exception import *

# =================================================================
# Exportação Consolidada
# =================================================================



# O __all__ aqui expõe os submódulos para permitir acesso via namespace
# Exemplo: from app.dtos import input, response
__all__ = (
   input,  # Referência ao pacote de modelos de entrada
   response, # Referência ao pacote de modelos de saída
   exception
)