import builtins
from pydantic import validate_call

builtins.validar = validate_call

from app.main import create_app

__all__ = [
    "create_app"
]