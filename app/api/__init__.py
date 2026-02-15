"""
API Router
----------

Ponto central de agregação de rotas.
Responsável por versionar a API e organizar os prefixos de URL.
"""

# ==============================
# Importações (Dependencies)
# ==============================
# Importa todas as rotas e recursos definidos na Versão 1 da API
from .version1 import *

# [Nota: O objeto 'Router' e 'v1' são esperados como parte da estrutura
# da biblioteca de roteamento que você está utilizando (como Flask-RESTful ou similar)]

# =================================================================
# CONFIGURAÇÃO DE ROTEAMENTO GLOBAL
# =================================================================

#

# Inicializa o roteador principal com o prefixo global '/api'.
# Todas as rotas registradas aqui começarão com: https://seusite.com/api/...
api = Router(name="api", url_prefix="/api")

# Registra o módulo da Versão 1 no roteador principal.
# Isso cria a estrutura hierárquica (ex: /api/v1/leads, /api/v1/status)
api.register_api(v1)

# ==============================
# Exportações do Módulo
# ==============================

# O __all__ expõe apenas o objeto 'api' configurado.
# No seu arquivo principal (app.py), você usará algo como: app.register_blueprint(api)
__all__ = [
    "api"
]