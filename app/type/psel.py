import json
from pydantic import BaseModel, EmailStr, field_validator,Field,model_validator
from datetime import datetime
from typing import Dict, List,Any

import json
from datetime import datetime
from typing import Dict, List, Any
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


# =================================================================
# 1. MODELOS DE RESPOSTA GENÉRICOS (BASE)
# =================================================================

class PselResponse(BaseModel):
    """Envelopa qualquer resposta no campo 'fields' exigido pelo Podio/AppScript."""
    fields: Dict[str, Any]

    @model_validator(mode='before')
    @classmethod
    def build_fields_envelope(cls, data: Any) -> Dict[str, Any]:
        if isinstance(data, dict) and "fields" not in data:
            return {"fields": data}
        return data

    model_config = {"extra": "allow"}


# =================================================================
# 2. SUB-MODELOS DE APOIO
# =================================================================

class EmailItem(BaseModel):
    tipo: str
    email: EmailStr


class TelefoneItem(BaseModel):
    tipo: str
    numero: str


# =================================================================
# 3. MODELOS DE ENTRADA (API -> FLASK)
# =================================================================

class LeadPselInput(BaseModel):
    """Dados brutos recebidos da requisição externa."""
    model_config = {
        "populate_by_name": True,
        "from_attributes": True
    }

    nome: str
    data_nascimento: datetime = Field(alias="dataNascimento")
    emails: List[EmailItem]
    telefones: List[TelefoneItem]
    id_comite: int = Field(alias="idComite")
    id_autorizacao: int = Field(alias="idAutorizacao")

    @field_validator("data_nascimento", mode="before")
    @classmethod
    def parse_data(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return datetime.strptime(v, "%Y-%m-%d")  # Fallback para data simples
        return v


# =================================================================
# 4. MODELOS DE SAÍDA / TRANSFORMAÇÃO (PODIO)
# =================================================================

class LeadPselPodio(LeadPselInput):
    """Transforma o Lead validado no formato JSON aceito pelo Podio."""

    def __init__(self, data):
        # Lógica para aceitar tanto dict quanto objetos Pydantic do @typed
        if len(data) == 1 and isinstance(next(iter(data.values())), BaseModel):
            actual_obj = next(iter(data.values()))
            data = actual_obj.model_dump(by_alias=True)
        super().__init__(**data)

    def to_podio_payload(self) -> dict:
        """Mapeia os campos do Pydantic para os slugs do Podio."""
        return {
            "titulo": self.nome,
            "data-de-nascimento": self.data_nascimento.strftime("%Y-%m-%d %H:%M:%S"),
            "email": [{"type": e.tipo, "value": e.email} for e in self.emails],
            "telefone": [{"type": t.tipo, "value": t.numero} for t in self.telefones],
            "autorizo-receber-informacoes-sobre-os-projetos-de-inter": self.id_autorizacao,
            "aiesec-mais-proxima-digite-primeira-letra-para-filtrar": self.id_comite,
            "tem-fit-cultural": 3
        }

    def to_json_podio(self) -> PselResponse:
        return PselResponse(**self.to_podio_payload())


class AtualizarPodioStatusFitCultural(BaseModel):
    """Modelo específico para atualização de status pós-inscição."""
    status: int

    def to_podio_payload(self) -> Dict[str, int]:
        return {"status": self.status}

    def to_json_podio(self) -> PselResponse:
        return PselResponse(**self.to_podio_payload())


__all__ = [
    "LeadPselInput",
    "LeadPselPodio",
    "AtualizarPodioStatusFitCultural",
    "PselResponse"
]
