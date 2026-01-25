from .model import LeadPsel,db

def buscar_token_lead_psel(token:str) -> bool:
    lead = db.session.query(LeadPsel).filter(LeadPsel.token == token).first()
    return lead


__all__ = [
    "buscar_token_lead_psel"
]