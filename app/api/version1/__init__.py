"""
API Version 1 Registry
----------------------

Este módulo organiza e registra todos os recursos (Blueprints/Rotas)
pertencentes à primeira versão da API.
"""

# ==============================
# Importações (Dependencies)
# ==============================
# Importa todos os sub-roteadores e recursos definidos no arquivo routes.py
# (ex: new_lead_ogx, processo_seletivo, Router)
from .routes import *

# =================================================================
# DEFINIÇÃO DO SUB-ROTEADOR V1
# =================================================================



# Cria a instância do roteador para a Versão 1.
# O prefixo '/v1' será aplicado automaticamente a todas as APIs registradas aqui.
# Exemplo de rota final: /api/v1/psel ou /api/v1/ogx
v1 = Router("versao_1", url_prefix="/v1")

# 1. Registro do módulo de Leads B2C (OGX)
# Geralmente lida com novos inscritos interessados em intercâmbio.
v1.register_api(new_lead_ogx)

# 2. Registro do módulo de Processo Seletivo (PSEL)
# Lida com a jornada de candidatos que desejam se tornar membros da AIESEC.
v1.register_api(processo_seletivo)

# ==============================
# Exportações do Módulo
# ==============================

# O __all__ expõe o roteador v1 e a classe Router para que possam ser
# utilizados pelo roteador central (central_router.py).
__all__ = [
    "v1",
    "Router"
]