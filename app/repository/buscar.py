"""
Consultas de leitura (buscar) relacionadas ao PSEL.

Funções utilitárias para acessar registros via token e verificar prazos
de expiração no banco de dados.
"""

# ==============================
# Importações (Dependencies)
# ==============================
from ..globals import Optional, datetime  # Tipagem para valores nulos e manipulação de tempo
from .model import LeadPsel, db           # Modelo da entidade e instância da sessão do banco

# ==============================
# Consultas de Identificação
# ==============================

def buscar_token_lead_psel(token: str) -> Optional[LeadPsel]:
    """
    Localiza um registro de Lead utilizando apenas o token de segurança.

    Args:
        token (str): O token único gerado no momento do cadastro.

    Returns:
        Optional[LeadPsel]: Instância do Lead se encontrado, caso contrário None.
    """
    return db.session.query(LeadPsel).filter(LeadPsel.token == token).first()

def buscar_token_id_podio_lead_psel(id: int, token: str) -> Optional[LeadPsel]:
    """
    Realiza uma busca combinada por ID do Podio e Token.

    Esta função aumenta a segurança ao exigir dois fatores de identificação
    antes de permitir o acesso aos dados do Lead.

    Args:
        id (int): O identificador vindo do CRM Podio.
        token (str): O token de segurança vinculado ao Lead.

    Returns:
        Optional[LeadPsel]: Instância do Lead se ambos os campos coincidirem.
    """
    return db.session.query(LeadPsel).filter(
        LeadPsel.id_podio == id,
        LeadPsel.token == token
    ).first()

# ==============================
# Consultas de Metadados
# ==============================

def buscar_data_expiracao(id_podio: int) -> Optional[datetime]:
    """
    Recupera exclusivamente o campo de expiração de um Lead.

    Utiliza o método '.scalar()' para retornar diretamente o valor da coluna
    em vez de um objeto de linha ou instância completa, otimizando a memória.



    Args:
        id_podio (int): O identificador do item no Podio.

    Returns:
        Optional[datetime]: A data/hora de expiração ou None se não localizado.
    """
    return (
        db.session.query(LeadPsel.expiracao)
        .filter(LeadPsel.id_podio == id_podio)
        .scalar()
    )

# ==============================
# Exportações
# ==============================
__all__ = [
    "buscar_token_lead_psel",
    "buscar_token_id_podio_lead_psel",
    "buscar_data_expiracao"
]