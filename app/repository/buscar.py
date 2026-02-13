"""
Consultas de leitura (buscar) relacionadas ao PSEL.

Funções utilitárias para acessar token e data de expiração no banco.
"""
from ..globals import Optional,datetime
from .model import LeadPsel,db

def buscar_token_lead_psel(token:str) -> bool:
    """Retorna o LeadPsel correspondente ao token, ou None se não existir."""
    return db.session.query(LeadPsel).filter(LeadPsel.token == token).first()

def buscar_token_id_podio_lead_psel(id:int,token:str) -> bool:
    """Retorna o LeadPsel quando id_podio e token coincidem, caso contrário None."""
    return db.session.query(LeadPsel).filter(LeadPsel.id_podio == id,LeadPsel.token==token).first()

def buscar_data_expiracao(id_podio: int) -> Optional[datetime]:
    """Recupera o campo 'expiracao' do LeadPsel pelo id_podio."""
    return (
        db.session.query(LeadPsel.expiracao)
        .filter(LeadPsel.id_podio == id_podio)
        .scalar()
    )

__all__ = [
    "buscar_token_lead_psel",
    "buscar_token_id_podio_lead_psel",
    "buscar_data_expiracao"
]