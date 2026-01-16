import base64
from ..globals.std import datetime,date,re,unicodedata,Dict,Any,List
from .gerador import gerar_email


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

def validar_nome(nome: str) -> bool:
    """
    Valida nomes sem acentos, apenas letras e espaços.

    Args:
        nome (str): Nome a ser validado.

    Returns:
        bool: True se válido, False caso contrário.
    """
    if not nome:
        return False
    # Remove acentos do nome
    nome_sem_acentos: str = ''.join(c for c in unicodedata.normalize('NFD', nome) if unicodedata.category(c) != 'Mn')
    # Verifica se existem caracteres diferentes de letras e espaços
    if re.search(r'[^A-Za-z\s]', nome_sem_acentos):
        return False
    # Limpa espaços extras
    nome_limpo: str = re.sub(r'\s+', ' ', nome_sem_acentos).strip()
    return bool(nome_limpo)

def validar_nome_com_acentos(nome: str) -> bool:
    """
    Valida nomes que podem conter acentos.
    Aceita caracteres latinos e espaços.

    Args:
        nome (str): Nome a ser validado.

    Returns:
        bool: True se válido, False caso contrário.
    """
    if not nome:
        return False
    nome_limpo: str = ' '.join(nome.strip().split())  # Remove espaços extras
    regex: str = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$'  # Letras latinas e acentos
    return bool(re.fullmatch(regex, nome_limpo))

def validar_senha(senha: str) -> Dict[str, Any]:
    """
    Valida senha com condições:
      - mínimo 8 caracteres
      - sem espaços
      - pelo menos uma letra minúscula
      - pelo menos uma letra maiúscula
      - pelo menos um número
      - pelo menos um caractere especial

    Args:
        senha (str): Senha a ser validada.

    Returns:
        Dict[str, Any]: Resultado da validação.
    """
    minimo: bool = len(senha) >= 8 and ' ' not in senha
    minusculo: bool = bool(re.search(r'[a-z]', senha))
    maiusculo: bool = bool(re.search(r'[A-Z]', senha))
    caracter_especial: bool = bool(re.search(r'\d', senha)) and bool(re.search(r'[@$!%*?&]', senha))
    all_ok: bool = minimo and minusculo and maiusculo and caracter_especial
    return {"condicao": all_ok, "mensagem": "" if all_ok else "Uma ou mais condições da senha não foi atendida"}

def validar_email_gerado(nome: str, sobrenome: str, email_front: str) -> bool:
    """
    Valida se o email gerado está correto comparando combinações possíveis.

    Args:
        nome (str): Primeiro nome do usuário.
        sobrenome (str): Sobrenome do usuário.
        email_front (str): Email a ser validado.

    Returns:
        bool: True se email válido, False caso contrário.
    """
    combinacoes_validas: List[str] =  gerar_email(nome, sobrenome)
    return email_front.lower() in combinacoes_validas

def validar_telefone_com_55(telefone: str) -> bool:
    """
    Valida telefone no formato internacional brasileiro +55.

    Args:
        telefone (str): Telefone a ser validado.

    Returns:
        bool: True se válido, False caso contrário.
    """
    if telefone == "":
        return True
    padrao: str = r'^\+55[1-9][0-9]9\d{8}$'
    return bool(re.fullmatch(padrao, telefone))

def validar_telefone(telefone: str) -> bool:
    """
    Valida telefone no formato internacional brasileiro +55.

    Args:
        telefone (str): Telefone a ser validado.

    Returns:
        bool: True se válido, False caso contrário.
    """
    padrao: str = r'^[1-9][0-9]9\d{8}$'
    return bool(re.fullmatch(padrao, telefone))

def validar_foto(foto: Dict[str, Any]) -> bool:
    """
    Valida foto no formato base64 e tipo permitido.

    Args:
        foto (Dict[str, Any]): Dicionário com 'base64' e 'tipo'.

    Returns:
        bool: True se válido, False caso contrário.
    """
    if not foto or not isinstance(foto, dict):
        return False
    base64_str: str = foto.get("base64", "")
    tipo: str = foto.get("tipo", "")
    if base64_str == "" and tipo == "":
        return True
    if tipo not in ['image/jpeg', 'image/jpg', 'image/png']:
        return False
    try:
        base64.b64decode(base64_str, validate=True)
    except Exception:
        return False
    return True

def validar_email_pessoal(email: str) -> bool:
    """
    Valida email pessoal em domínios permitidos: gmail.com, hotmail.com, outlook.com, yahoo.com

    Args:
        email (str): Email a ser validado.

    Returns:
        bool: True se válido ou vazio, False caso contrário.
    """
    dominios_permitidos: List[str] = ['gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com']
    if email == "":
        return True
    regex_email: str = r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$'
    if not re.fullmatch(regex_email, email):
        return False
    dominio: str = email.split('@')[1].lower()
    return dominio in dominios_permitidos

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

def validar_data_nascimento(data: str) -> bool:
    """
    Valida se a data de nascimento está no formato 'YYYY-MM-DD HH:MM:SS'.

    Args:
        data (str): Data a ser validada.

    Returns:
        bool: True se válido, False se inválido.
    """
    try:
        datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

def validar_tipo_email(tipo_email: str) -> bool:
    """
    Verifica se todos os tipos de email da lista estão permitidos.

    Args:
        emails (List[Dict[str, str]]): Lista de emails no formato {"tipo": ..., "email": ...}

    Returns:
        bool: True se todos forem válidos, False caso algum tipo seja inválido.
    """
    TIPOS_PERMITIDOS = ["home", "other", "work"]
    if tipo_email not in TIPOS_PERMITIDOS:
        return False
    return True

def validar_tipo_telefone(tipo_telefone: str) -> bool:
    """
    Verifica se todos os tipos de email da lista estão permitidos.

    Args:
        emails (List[Dict[str, str]]): Lista de emails no formato {"tipo": ..., "email": ...}

    Returns:
        bool: True se todos forem válidos, False caso algum tipo seja inválido.
    """
    TIPOS_PERMITIDOS = ["home","main","mobile","other","private_fax","work","work_fax"]
    if tipo_telefone not in TIPOS_PERMITIDOS:
        return False
    return True

def tem_mais_de_31_anos(data_nascimento_str):
    # Converte string para data (formato: YYYY-MM-DD %H:%M:%S)
    nascimento = datetime.strptime(data_nascimento_str, "%Y-%m-%d %H:%M:%S").date()
    hoje = date.today()

    idade = hoje.year - nascimento.year

    # Ajusta caso ainda não tenha feito aniversário este ano
    if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
        idade -= 1

    return idade > 31

__all__ = [
    "validar_telefone",
    "validar_foto",
    "validar_nome",
    "validar_senha",
    "validar_codigo_membresia",
    "validar_tipo_email",
    "validar_tipo_telefone",
    "validar_data_nascimento",
    "validar_email_gerado",
    "validar_email_pessoal",
    "validar_telefone_com_55",
    "validar_nome_com_acentos",
    "validar_email_pessoal_obrigatorio",
    "tem_mais_de_31_anos"
]