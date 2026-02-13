from ..globals import Optional,datetime
from .model import LeadPsel,db

def buscar_token_lead_psel(token:str) -> bool:
    return db.session.query(LeadPsel).filter(LeadPsel.token == token).first()

def buscar_token_id_podio_lead_psel(id:int,token:str) -> bool:
    return db.session.query(LeadPsel).filter(LeadPsel.id_podio == id,LeadPsel.token==token).first()

def buscar_data_expiracao(id_podio: int) -> Optional[datetime]:
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