from datetime import datetime
from typing import Dict, List, Any,Optional
from pydantic import BaseModel, Field, field_validator, model_validator,ConfigDict
from .padrao import Comite,EmailItem,TelefoneItem
from ..output_type import ModelPodio

# =================================================================
# 1. MODELOS DE ENTRADA (API -> FLASK)
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
    comite: Comite
    id_autorizacao: int = Field(alias="idAutorizacao")

    @field_validator("data_nascimento", mode="before")
    @classmethod
    def parse_data(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return datetime.strptime(value, "%Y-%m-%d")  # Fallback para data simples
        return value


# =================================================================
# 2. MODELOS DE SAÍDA / TRANSFORMAÇÃO (PODIO)
# =================================================================

class LeadPselPodio(LeadPselInput):
    """Transforma o Lead validado no formato JSON aceito pelo Podio."""

    def to_podio_payload(self) -> dict:
        """Mapeia os campos do Pydantic para os slugs do Podio."""
        return {
            "titulo": self.nome,
            "data-de-nascimento": self.data_nascimento.strftime("%Y-%m-%d %H:%M:%S"),
            "email": [{"type": email.tipo, "value": email.email} for email in self.emails],
            "telefone": [{"type": telefone.tipo, "value": telefone.numero} for telefone in self.telefones],
            "autorizo-receber-informacoes-sobre-os-projetos-de-inter": self.id_autorizacao,
            "aiesec-mais-proxima-digite-primeira-letra-para-filtrar": self.comite.id,
            "tem-fit-cultural": 3
        }

    def to_json_podio(self) -> ModelPodio:
        return ModelPodio(**self.to_podio_payload())


class AtualizarPodioStatusFitCultural(BaseModel):
    """Modelo específico para atualização de status pós-inscição."""
    status: int

    def to_podio_payload(self) -> Dict[str, int]:
        return {"status": self.status}

    def to_json_podio(self) -> ModelPodio:
        return ModelPodio(**self.to_podio_payload())

__all__ = [
    "LeadPselInput",
    "LeadPselPodio",
    "AtualizarPodioStatusFitCultural"
]
