import builtins
from .core import typed

builtins.typed = typed

from app.main import create_app

__all__ = [
    "create_app"
]