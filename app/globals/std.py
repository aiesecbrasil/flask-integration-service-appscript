"""
globals.std
----------

Centralizador de imports da biblioteca padrão do Python e utilitários de tipagem.
Este módulo serve para manter o namespace do projeto limpo e facilitar a
manutenção de dependências nativas.

Uso recomendado:
    from ..globals import datetime, List, Optional
"""

# ==============================
# Módulos do Sistema e Utilitários
# ==============================
import os               # Interação com o sistema operacional (caminhos, env vars)
import time             # Manipulação de tempo e medição de performance
import re               # Expressões regulares para busca e validação de padrões
import base64           # Codificação e decodificação de dados em base64
import unicodedata      # Manipulação de caracteres Unicode (ex: remoção de acentos)

# ==============================
# Manipulação de Data e Tempo
# ==============================
from datetime import datetime, date  # Classes para representação de data e hora

# ==============================
# Infraestrutura de Tipagem (Typing)
# ==============================
# Essencial para garantir a segurança de tipos e o funcionamento do Pydantic/Mypy
from typing import (
    Any,        # Aceita qualquer tipo de dado
    Dict,       # Tipo dicionário {chave: valor}
    List,       # Tipo lista [item1, item2]
    Optional,   # Indica que o valor pode ser do tipo especificado ou None
    Tuple,      # Tipo tupla (imutável)
    Callable,   # Indica um objeto que pode ser chamado (função)
    Iterable,   # Indica objetos que podem ser iterados (listas, sets, generators)
    Union       # Permite que uma variável aceite mais de um tipo (ex: Union[int, str])
)

# ==============================
# Utilitários de URL
# ==============================
from urllib.parse import urlparse, quote  # Análise de URLs e codificação de caracteres especiais

# ==============================
# Exportação Pública
# ==============================



__all__ = [
    # Módulos Base
    "os",
    "time",
    "re",
    "base64",
    "unicodedata",

    # Datetime
    "datetime",
    "date",

    # Typing
    "Any",
    "Dict",
    "List",
    "Optional",
    "Tuple",
    "Callable",
    "Iterable",
    "Union",

    # URL Utils
    "urlparse",
    "quote",
]