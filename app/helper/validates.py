import re
from ..globals import List,date,datetime
def validar_codigo_membresia(codigo: str) -> bool:
    """
    Valida se o código de membresia possui 5 dígitos numéricos.

    Args:
        codigo (str): Código a ser validado.

    Returns:
        bool: True se válido, False caso contrário.
    """
    # Remove qualquer caractere que não seja número ou espaço
    codigo_limpo: str = re.sub(r'[^0-9\s]', '', codigo)
    regex: str = r'^[0-9\s]+$'
    return bool(re.fullmatch(regex, codigo_limpo) and len(codigo_limpo) == 5)

def validar_email_pessoal_obrigatorio(email: str) -> bool:
    """
    Valida email pessoal em domínios permitidos: gmail.com, hotmail.com, outlook.com, yahoo.com

    Args:
        email (str): Email a ser validado.

    Returns:
        bool: True se válido ou vazio, False caso contrário.
    """
    dominios_permitidos: List[str] = ['gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com']
    regex_email: str = r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$'
    if not re.fullmatch(regex_email, email):
        return False
    dominio: str = email.split('@')[1].lower()
    return dominio in dominios_permitidos

def tem_mais_de_31_anos(data_nascimento:datetime|str) -> bool:
    # Converte string para data (formato: YYYY-MM-DD %H:%M:%S)
    # 1. Garante que temos um objeto date, não importa o que venha
    if isinstance(data_nascimento, datetime):
        nascimento = data_nascimento.date()
    elif isinstance(data_nascimento, str):
        # Caso venha string, converte (ajuste o formato se necessário)
        nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d %H:%M:%S").date()
    else:
        nascimento = data_nascimento # Assume que já é date

    hoje = date.today()

    idade = hoje.year - nascimento.year

    # Ajusta caso ainda não tenha feito aniversário este ano
    if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
        idade -= 1

    return not (idade > 31)

__all__ = [
    "tem_mais_de_31_anos",
    "validar_codigo_membresia",
    "validar_email_pessoal_obrigatorio"
]