"""
Inicialização do SQLAlchemy para a aplicação Flask.

Este módulo expõe a instância global 'db' a ser importada pelos modelos e
camadas que interagem com o banco de dados.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

__all__ = ["db"]