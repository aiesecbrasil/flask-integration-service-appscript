from .model import db,LeadPsel,Email,Telefone
from .cadastrar import *
from .buscar import *

__all__ = [
    "db",
    "LeadPsel",
    "Email",
    "Telefone",
    cadastrar.__all__+
    buscar.__all__
]