"""
Inicialização do Marshmallow para (de)serialização/validação de schemas.
Exponibiliza a instância global 'ma'.
"""
from flask_marshmallow import Marshmallow

ma = Marshmallow() # Inicialize após o db

__all__ = ["ma"]