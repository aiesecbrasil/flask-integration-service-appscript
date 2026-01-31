import pytz
import locale
from datetime import timedelta
from ..globals import datetime

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

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
    return agora(cidade_fuso) + timedelta(hours=72)  # 72h depois

def agora_format_brasil(cidade_fuso="America/Sao_Paulo"):
    return agora(cidade_fuso).strftime("%d/%m/%Y %H:%M:%S")

def agora_format_brasil_mes(cidade_fuso="America/Sao_Paulo"):
    return agora(cidade_fuso).strftime(f"%d/%b/%Y %H:%M:%S").title()


def logging_time_brasil(*args):
    # O logging pode passar (timestamp) ou (formatter, timestamp)
    # Pegamos o último elemento da tupla, que costuma ser o timestamp (float)
    seconds = args[-1]

    cidade_fuso = "America/Sao_Paulo"
    tz = pytz.timezone(cidade_fuso)

    # Garantimos que 'seconds' seja um número antes de converter
    if not isinstance(seconds, (int, float)):
        # Fallback caso algo muito estranho aconteça
        seconds = datetime.now().timestamp()

    dt = datetime.fromtimestamp(seconds, tz)
    return dt.timetuple()

__all__ = [
    "agora_timestamp",
    "agora",
    "expiracao_3dias",
    "agora_format_brasil",
    "logging_time_brasil",
    "agora_format_brasil_mes"
]