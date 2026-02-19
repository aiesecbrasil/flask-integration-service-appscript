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

@validar
def buscar_lead_psel(token:str,id:int=None) -> Optional[LeadPsel]:
    if id  is not None:
        return db.session.query(LeadPsel).filter(
            LeadPsel.id_podio == id,
            LeadPsel.token == token
        ).first()
    return db.session.query(LeadPsel).filter(LeadPsel.token == token).first()
# ==============================
# Consultas de Metadados
# ==============================
@validar
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
    "buscar_lead_psel",
    "buscar_data_expiracao"
]