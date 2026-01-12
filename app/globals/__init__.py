"""
globals
------

Pacote de imports globais do projeto.
Contém apenas dependências genéricas (stdlib, Flask, HTTP).

NUNCA colocar:
- settings
- services
- cache
- response custom
"""

from .std import *
from .flask import *
from .http import *

__all__ = (
    std.__all__ +
    flask.__all__ +
    http.__all__
)
