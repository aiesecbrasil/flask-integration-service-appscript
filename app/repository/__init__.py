from .model import db,LeadPsel,Email,Telefone
from .cadastrar import *

__all__ = [
    "db",
    "LeadPsel",
    "Email",
    "Telefone",
    cadastrar.__all__
]