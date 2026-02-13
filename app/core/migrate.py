"""
Inicialização do Flask-Migrate (integração Alembic) para migrações de banco.
Exponibiliza a instância global 'migrate'.
"""
from flask_migrate import Migrate

migrate = Migrate()

__all__ = ["migrate"]