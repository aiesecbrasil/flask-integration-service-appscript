"""
Utilitários de data e hora com suporte a fuso horário do Brasil (America/Sao_Paulo).

Este módulo centraliza funções para obter o horário atual com e sem timezone,
formatar datas em padrões brasileiros, calcular expiração e converter timestamps
para o formato esperado pelo sistema de logging.
"""
import pytz
import locale
from datetime import timedelta
from ..globals import datetime

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

def agora_timestamp(cidade_fuso="America/Sao_Paulo"):
    """Retorna o timestamp atual (segundos desde epoch) no fuso informado.

    Parâmetros:
    - cidade_fuso: str
        Identificador do fuso horário, por padrão America/Sao_Paulo.
    """
    fuso = pytz.timezone(str(cidade_fuso))
    return datetime.now(fuso).timestamp()

def agora(cidade_fuso="America/Sao_Paulo"):
    """Retorna o datetime atual com timezone no fuso informado."""
    fuso = pytz.timezone(str(cidade_fuso))
    return datetime.now(fuso)

def agora_sem_timezone(cidade_fuso="America/Sao_Paulo"):
    """Retorna o datetime atual sem informação de timezone (naive) no fuso informado."""
    fuso = pytz.timezone(str(cidade_fuso))
    return datetime.now(fuso).replace(tzinfo=None)

def expiracao_3dias(cidade_fuso="America/Sao_Paulo"):
    """
    Retorna a data/hora de expiração 3 dias (72h) a partir de agora
    no fuso horário especificado.
    """
    return agora(cidade_fuso) + timedelta(hours=72)  # 72h depois

def agora_format_brasil(cidade_fuso="America/Sao_Paulo"):
    """Retorna data/hora formatada como DD/MM/AAAA HH:MM:SS no fuso informado."""
    return agora(cidade_fuso).strftime("%d/%m/%Y %H:%M:%S")

def agora_format_brasil_mes(cidade_fuso="America/Sao_Paulo"):
    """Retorna data/hora formatada como DD/Mon/AAAA HH:MM:SS (abreviação do mês em pt_BR)."""
    return agora(cidade_fuso).strftime(f"%d/%b/%Y %H:%M:%S").title()


def logging_time_brasil(*args):
    """Converte um timestamp em struct_time no fuso America/Sao_Paulo para logging.

    Aceita assinatura variável, onde o timestamp pode vir como último argumento
    (padrão do logging: formatter, timestamp). Caso o valor não seja numérico,
    utiliza o horário atual como fallback.
    """
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
    "agora_format_brasil_mes",
    "agora_sem_timezone"
]