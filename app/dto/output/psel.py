"""
DTOs de saída e envelopes de resposta para PSEL e integração com Podio.

Inclui enum de HttpStatus, envelope ModelPodio e respostas de pré-cadastro.
"""
from typing import Dict, Any,Optional
from enum import IntEnum
from pydantic import BaseModel, Field, model_validator,ConfigDict

# =================================================================
# 1. MODELOS DE RESPOSTA GENÉRICOS (BASE)
# =================================================================
class HttpStatus(IntEnum):
    """Enum de códigos HTTP utilizados pelas respostas padronizadas."""
    # Success
    OK = 200
    CREATED = 201
    NON_AUTHORITATIVE = 203

    # Redirection
    MOVED_PERMANENTLY = 301
    FOUND = 302

    # Client Errors
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422  # Útil para erros de validação Pydantic

    # Server Errors
    INTERNAL_ERROR = 500
    BAD_GATEWAY = 502  # O que você usará para falhas no Podio
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504

class ModelPodio(BaseModel):
    """
    Classe modelo de contrução para envio para o Podio.

    Envelopa qualquer resposta no campo 'fields' exigido pelo Podio/AppScript.
    """
    fields: Dict[str, Any]

    @model_validator(mode='before')
    @classmethod
    def build_fields_envelope(cls, data: Any) -> Any:
        # Se receber o objeto LeadPselPodio ou um dict bruto, envelopa em 'fields'
        if isinstance(data, dict) and "fields" not in data:
            return {"fields": data}
        # Se for o objeto vivo da LeadPselPodio, extraímos o payload
        if hasattr(data, "to_podio_payload"):
            return {"fields": data.to_podio_payload()}
        return data

    model_config = ConfigDict(extra="forbid")

# =================================================================
# 4. RESPONSES /
# =================================================================

class ReponsePselPreCadastro(BaseModel):
    """
    Estrutura:
        {
            "banco_de_dados": { ... },
            "podio": { "fields": { ... } }
        }
    """
    banco_de_dados: Optional[Dict[str, Any]] = Field(default_factory=dict)
    # Union permite aceitar o objeto vivo ou o dicionário para conversão
    podio: ModelPodio

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

class ReponseOutPutPreCadastro(BaseModel):
    """Envelope de resposta padrão para o pré-cadastro PSEL."""
    status: str
    message: str
    data: ReponsePselPreCadastro | str
    status_code: HttpStatus

    def model_dump(self, **kwargs):
        """Força o modo JSON para serializar sub-classes em dict/list/str."""
        kwargs.update({"mode": "json"})
        return super().model_dump(**kwargs)

__all__ = [
    "ModelPodio",
    "ReponseOutPutPreCadastro",
    "ReponsePselPreCadastro",
    "HttpStatus"
]
