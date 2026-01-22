from datetime import datetime
from typing import Dict, List, Any,Optional
from pydantic import BaseModel, Field, field_validator, model_validator,ConfigDict
from app.type.input_type.padrao import Comite,EmailItem,TelefoneItem

# =================================================================
# 1. MODELOS DE RESPOSTA GENÉRICOS (BASE)
# =================================================================

class ModelPodio(BaseModel):
    """
    Classe modelo de contrução para envio para o podio
    Envelopa qualquer resposta no campo 'fields' exigido pelo Podio/AppScript."""
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
    status: str
    message: str
    data: ReponsePselPreCadastro
    status_code:int

    def model_dump(self, **kwargs):
        # O segredo: forçamos o modo JSON que converte TUDO (incluindo sub-classes) para dict/list/str
        kwargs.update({"mode": "json"})
        return super().model_dump(**kwargs)

__all__ = [
    "ModelPodio",
    "ReponseOutPutPreCadastro",
    "ReponsePselPreCadastro"
]
