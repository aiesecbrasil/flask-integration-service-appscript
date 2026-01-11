"""
globals.flask
------------

Imports globais relacionados ao Flask.
Centraliza objetos usados em rotas e middlewares.

Uso:
    from globals.flask import request, jsonify
"""

from flask import (
    request,
    jsonify,
    redirect,
    Response,
)

__all__ = [
    "request",
    "jsonify",
    "redirect",
    "Response",
]
