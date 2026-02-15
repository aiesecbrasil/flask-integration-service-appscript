"""
globals
------

Pacote de imports globais do projeto.
Contém apenas dependências genéricas (stdlib, Flask, HTTP).

Este módulo atua como uma camada de abstração para bibliotecas externas,
garantindo que o restante da aplicação não precise importar diretamente
de terceiros, facilitando futuras trocas de bibliotecas.
"""

# ==============================
# Importações de Submódulos
# ==============================

# 1. Standard Library (std.py):
# Contém tipos básicos e utilitários como Any, Dict, List, datetime, etc.
from .std import *

# 2. Flask Framework (flask.py):
# Contém objetos do framework como request, jsonify, make_response e Blueprints.
from .flask import *

# 3. Protocolos HTTP (http.py):
# Contém clientes como httpx ou requests e tratadores de status code.
from .http import *

# =================================================================
# COMPOSIÇÃO DO NAMESPACE GLOBAL
# =================================================================



# O __all__ aqui é uma composição aritmética das listas de exportação.
# Ao somar as tuplas/listas __all__ de cada submódulo, criamos um
# "Super-Import" que permite que em qualquer lugar do sistema você use:
# from app.globals import Any, request, httpx, jsonify
__all__ = (
    std.__all__ +
    flask.__all__ +
    http.__all__
)