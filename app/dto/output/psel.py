"""
DTOs de saída e envelopes de resposta para PSEL e integração com Podio.

Inclui enum de HttpStatus, envelope ModelPodio e respostas de pré-cadastro.
"""

# ==============================
# Importações (Dependencies)
# ==============================
from typing import Dict, Any, Optional                     # Tipagem para dicionários e valores opcionais
from enum import IntEnum                                   # Base para criação de enumeradores de inteiros
from pydantic import BaseModel, Field, model_validator, ConfigDict # Core do Pydantic para validação e esquemas

# =================================================================
# 1. MODELOS DE RESPOSTA GENÉRICOS (BASE)
# =================================================================

class HttpStatus(IntEnum):
    """
    Enum de códigos HTTP utilizados pelas respostas padronizadas.

    Facilita a legibilidade: usar 'HttpStatus.OK' é mais claro que usar '200'.
    """
    # Sucesso (2xx)
    OK = 200                # Requisição bem-sucedida
    CREATED = 201           # Recurso criado com sucesso
    NON_AUTHORITATIVE = 203 # Informação de fonte não confiável
    NO_CONTENT = 204

    # Redirecionamento (3xx)
    MOVED_PERMANENTLY = 301 # Recurso movido permanentemente
    FOUND = 302             # Recurso movido temporariamente

    # Erros do Cliente (4xx)
    BAD_REQUEST = 400           # Requisição inválida ou malformada
    UNAUTHORIZED = 401          # Falha na autenticação
    FORBIDDEN = 403             # Permissão negada
    NOT_FOUND = 404             # Recurso não encontrado
    CONFLICT = 409              # Conflito de estado (ex: e-mail já existe)
    UNPROCESSABLE_ENTITY = 422  # Erro semântico (validação de campos)

    # Erros do Servidor (5xx)
    INTERNAL_ERROR = 500       # Erro genérico no servidor
    BAD_GATEWAY = 502          # Falha na comunicação com API externa (ex: Podio fora do ar)
    SERVICE_UNAVAILABLE = 503  # Servidor em manutenção ou sobrecarregado
    GATEWAY_TIMEOUT = 504      # API externa demorou demais para responder



class ModelPodio(BaseModel):
    """
    Classe modelo de construção para envio para o Podio.

    Envelopa qualquer resposta no campo 'fields' exigido pelo Podio/AppScript.
    """
    # Atributos
    fields: Dict[str, Any] # Dicionário contendo os Slugs e valores para o CRM

    @model_validator(mode='before')
    @classmethod
    def build_fields_envelope(cls, data: Any) -> Any:
        """
        Lógica de Envelopamento:
        Garante que os dados enviados estejam sempre dentro da chave 'fields',
        como exigido pela API do Podio.
        """
        # Se receber um dicionário bruto sem a chave 'fields', nós a criamos
        if isinstance(data, dict) and "fields" not in data:
            return {"fields": data}

        # Se receber um objeto DTO (como LeadPselPodio), extrai o payload automaticamente
        if hasattr(data, "to_podio_payload"):
            return {"fields": data.to_podio_payload()}

        return data

    model_config = ConfigDict(extra="forbid") # Impede a inserção de campos não definidos

# =================================================================
# 4. RESPONSES / PSEL
# =================================================================

class ReponsePselPreCadastro(BaseModel):
    """
    Modelo de dados retornado após um pré-cadastro.
    Combina o que foi salvo localmente com o que foi enviado ao CRM.
    """
    # Atributos
    banco_de_dados: Optional[Dict[str, Any]] = Field(default_factory=dict) # Resumo do registro no SQL
    podio: ModelPodio # Cópia do payload enviado/recebido do Podio

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

class ReponseOutPutPreCadastro(BaseModel):
    """
    Envelope de resposta padrão para o pré-cadastro PSEL.
    Este é o formato final que o front-end receberá.
    """
    # Atributos
    status: str                  # 'success' ou 'error'
    message: str                 # Mensagem amigável para o usuário/desenvolvedor
    data: ReponsePselPreCadastro | str # Dados da operação ou mensagem de erro detalhada
    status_code: HttpStatus      # Código numérico HTTP (ex: 201)

    def model_dump(self, **kwargs):
        """
        Customização da serialização:
        Força a conversão automática de Enums e Datetimes para strings JSON
        ao retornar a resposta via Flask.
        """
        kwargs.update({"mode": "json"})
        return super().model_dump(**kwargs)

# ==============================
# Exportações do Módulo
# ==============================
__all__ = [
    "ModelPodio",
    "ReponseOutPutPreCadastro",
    "ReponsePselPreCadastro",
    "HttpStatus"
]