"""
DTOs de entrada e transformação para o fluxo do Processo Seletivo (PSEL).

Inclui modelos Pydantic para validação dos dados recebidos e métodos auxiliares
para montar payloads aceitos pelo Podio.
"""

# ==============================
# Importações (Dependencies)
# ==============================
from datetime import datetime            # Manipulação de objetos de data e hora
from typing import Dict, List, Any, Optional # Tipagem estática para maior segurança e clareza
from pydantic import (                   # Biblioteca principal para validação de dados
    BaseModel,
    Field,
    field_validator,
    model_validator,
    ConfigDict
)

# Importações de submodelos para composição e saída padronizada
from .padrao import Comite, EmailItem, TelefoneItem
from ..output import ModelPodio

# =================================================================
# 1. MODELOS DE ENTRADA (API -> FLASK)
# =================================================================

class LeadPselInput(BaseModel):
    """
    Dados brutos recebidos da requisição externa.

    Converte data_nascimento a partir de string para datetime quando necessário.
    """
    # Configuração de comportamento do modelo Pydantic
    model_config = {
        "populate_by_name": True, # Permite criar o objeto usando o nome do atributo ou o alias
        "from_attributes": True   # Permite que o modelo leia dados de objetos de classe (ex: ORM)
    }

    # Atributos do Lead
    nome: str                                    # Nome completo do candidato
    data_nascimento: datetime = Field(alias="dataNascimento") # Data de nascimento (mapeada do camelCase)
    emails: List[EmailItem]                      # Lista de objetos de e-mail (tipo e endereço)
    telefones: List[TelefoneItem]                # Lista de objetos de telefone (tipo e número)
    comite: Comite                               # Objeto contendo informações do comitê local (AIESEC)
    id_autorizacao: int = Field(alias="idAutorizacao") # Flag de autorização para LGPD/Comunicação

    @field_validator("data_nascimento", mode="before")
    @classmethod
    def parse_data(cls, value):
        """
        Lógica de normalização: Aceita 'YYYY-MM-DD HH:MM:SS' e fallback para 'YYYY-MM-DD'.
        Converte strings provenientes do JSON para objetos datetime do Python.
        """
        if isinstance(value, str):
            try:
                # Tenta o formato completo com horas
                return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                # Tenta o formato apenas com data (fallback)
                return datetime.strptime(value, "%Y-%m-%d")
        return value

class ParamsInput(BaseModel):
    """Parâmetros de rota/consulta para validação de token do PSEL."""
    id: int      # ID único identificador (geralmente do registro no banco ou CRM)
    nome: str    # Nome associado para conferência de integridade
    token: str   # Hash de segurança para validação da sessão/link

# =================================================================
# 2. MODELOS DE SAÍDA / TRANSFORMAÇÃO (PODIO)
# =================================================================



class LeadPselPodio(LeadPselInput):
    """
    Transforma o Lead validado no formato JSON aceito pelo Podio.
    Especialização do modelo de entrada para integração com o CRM.
    """

    def to_podio_payload(self) -> dict:
        """
        Mapeia os atributos da classe para as chaves (Slugs) esperadas pelo Podio.
        Realiza a formatação final de listas e datas para o padrão da API externa.
        """
        return {
            "titulo": self.nome,
            "data-de-nascimento": self.data_nascimento.strftime("%Y-%m-%d %H:%M:%S"),
            "email": [{"type": email.tipo, "value": email.email} for email in self.emails],
            "telefone": [{"type": telefone.tipo, "value": telefone.numero} for telefone in self.telefones],
            "autorizo-receber-informacoes-sobre-os-projetos-de-inter": self.id_autorizacao,
            "aiesec-mais-proxima-digite-primeira-letra-para-filtrar": self.comite.id,
            "tem-fit-cultural": 3 # ID correspondente ao status inicial no Podio
        }

    def to_json_podio(self) -> ModelPodio:
        """Instancia o ModelPodio com o dicionário de payload gerado."""
        return ModelPodio(**self.to_podio_payload())


class AtualizarPodioStatusFitCultural(BaseModel):
    """Modelo específico para atualização de status pós-inscição."""
    status: int # Valor numérico que representa o novo estado do teste no Podio

    def to_podio_payload(self) -> Dict[str, int]:
        """Gera o payload simplificado para atualização de um único campo."""
        return {"status": self.status}

    def to_json_podio(self) -> ModelPodio:
        """Gera o objeto de saída validado para a requisição ao Podio."""
        return ModelPodio(**self.to_podio_payload())

# ==============================
# Exportações do Módulo
# ==============================
__all__ = [
    "LeadPselInput",
    "LeadPselPodio",
    "AtualizarPodioStatusFitCultural",
    "ParamsInput"
]