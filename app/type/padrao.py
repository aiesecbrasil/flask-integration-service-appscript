from datetime import datetime
from typing import Dict, List, Any
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

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