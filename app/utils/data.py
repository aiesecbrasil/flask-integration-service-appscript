import pytz
from datetime import timedelta
from ..globals import datetime,date

def agora_timestamp(cidade_fuso="America/Sao_Paulo"):
    fuso = pytz.timezone(str(cidade_fuso))
    return datetime.now(fuso).timestamp()

def agora(cidade_fuso="America/Sao_Paulo"):
    fuso = pytz.timezone(str(cidade_fuso))
    return datetime.now(fuso)

def expiracao_3dias(cidade_fuso="America/Sao_Paulo"):
    """
    Retorna a data/hora de expiração 3 dias (72h) a partir de agora
    no fuso horário especificado.
    """
    return agora() + timedelta(hours=72)  # 72h depois

__all__ = [
    "agora_timestamp",
    "agora",
    "expiracao_3dias"
]