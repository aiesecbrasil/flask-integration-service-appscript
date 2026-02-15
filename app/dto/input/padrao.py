"""
Submodelos Pydantic de apoio para DTOs de entrada.

EmailItem, TelefoneItem e Comite compõem estruturas usadas em múltiplos DTOs.
"""

# ==============================
# Importações (Dependencies)
# ==============================
from pydantic import (
    BaseModel, # Classe base para criação de modelos de dados com validação
    EmailStr   # Tipo especializado para validar se a string é um e-mail real (formato RFC)
)

# =================================================================
# 1. SUB-MODELOS DE APOIO
# =================================================================



class EmailItem(BaseModel):
    """
    Estrutura para itens de e-mail.
    Comum em sistemas que permitem múltiplos endereços (ex: pessoal, trabalho).
    """
    tipo: str    # Categoria do e-mail (Ex: 'home', 'work', 'other')
    email: EmailStr # Endereço de e-mail validado sintaticamente


class TelefoneItem(BaseModel):
    """
    Estrutura para itens de telefone.
    Segue o formato de lista de contatos esperado pela API do Podio.
    """
    tipo: str    # Categoria do telefone (Ex: 'mobile', 'work', 'home')
    numero: str  # String contendo o número (Ex: '+5511999999999')


class Comite(BaseModel):
    """
    Representa o Comitê Local (Unidade da AIESEC) selecionado pelo usuário.
    Crucial para o roteamento do lead para a equipe correta.
    """
    id: int      # ID interno do comitê (usado para mapeamento no Podio)
    nome: str    # Nome por extenso do comitê (Ex: 'AIESEC em São Paulo')


# ==============================
# Exportações do Módulo
# ==============================
__all__ = [
    "Comite",
    "TelefoneItem",
    "EmailItem"
]