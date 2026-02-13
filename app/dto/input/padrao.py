"""
Submodelos Pydantic de apoio para DTOs de entrada.

EmailItem, TelefoneItem e Comite compõem estruturas usadas em múltiplos DTOs.
"""
from pydantic import BaseModel, EmailStr

# =================================================================
# 1. SUB-MODELOS DE APOIO
# =================================================================

class EmailItem(BaseModel):
    tipo: str
    email: EmailStr


class TelefoneItem(BaseModel):
    tipo: str
    numero: str

class Comite(BaseModel):
    id: int
    nome: str

__all__ = [
    "Comite",
    "TelefoneItem",
    "EmailItem"
]