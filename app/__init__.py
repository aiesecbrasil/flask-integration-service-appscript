import builtins
from .core import typed
from pydantic import validate_call

builtins.typed = typed
builtins.validar = validate_call()

from app.main import create_app

__all__ = [
    "create_app"
]