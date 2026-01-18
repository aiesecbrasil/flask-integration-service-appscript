from datetime import datetime
from typing import Dict, List, Any,Optional,Union
from pydantic import BaseModel, Field, field_validator, model_validator,ConfigDict
from .padrao import Comite,EmailItem,TelefoneItem

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

    model_config = {
        "extra": "forbid"
    }

# =================================================================
# 2. MODELOS DE ENTRADA (API -> FLASK)
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
# 3. MODELOS DE SAÍDA / TRANSFORMAÇÃO (PODIO)
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

    @model_validator(mode='before')
    @classmethod
    def preparar_dados(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        podio_input = data.get("podio")

        # Se o dado vier 'sujo' com 'fields', nós limpamos para o Pydantic conseguir instanciar
        if isinstance(podio_input, dict) and "fields" in podio_input:
            podio_input = podio_input["fields"]

        # INSTÂNCIA RECURSIVA AUTOMÁTICA
        # Se for um dict de dados, transformamos na classe LeadPselPodio aqui
        if isinstance(podio_input, dict):
            data["podio"] = ModelPodio.model_validate(podio_input)

        return data

    def model_dump(self, **kwargs) -> Dict[str, Any]:
        """Garante que o JSON final tenha o formato que o Podio/AppScript exige"""
        d = super().model_dump(**kwargs)

        podio_val = self.podio
        # Se for nossa classe, usamos o método de mapeamento dela
        if hasattr(podio_val, "to_podio_payload"):
            d["podio"] = {"fields": podio_val.to_podio_payload()}
        return d

__all__ = [
    "LeadPselInput",
    "LeadPselPodio",
    "AtualizarPodioStatusFitCultural",
    "ReponsePselPreCadastro"
]
