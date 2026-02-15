"""
globals.flask
------------

Imports globais relacionados ao ecossistema Flask.
Centraliza objetos fundamentais para a manipulação do ciclo de vida da
requisição, respostas da API e redirecionamentos.

Uso:
    from ..globals import request, jsonify
"""

# ==============================
# Objetos de Ciclo de Vida HTTP
# ==============================
from flask import (
    request,   # Objeto proxy que contém dados da requisição (JSON, headers, IP)
    jsonify,   # Utilitário para serializar dicionários em respostas JSON (application/json)
    redirect,  # Função para gerar respostas de redirecionamento HTTP (301, 302)
    Response,  # Classe base para manipulação fina de cabeçalhos e corpo da resposta
)

# ==============================
# Exportação Pública
# ==============================



__all__ = [
    "request",
    "jsonify",
    "redirect",
    "Response",
]