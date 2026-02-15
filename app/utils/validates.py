"""
Validações utilitárias para entradas de usuário e dados de domínio.

Inclui validação de nome (com/sem acentos), senha, e-mail (gerado e pessoal),
telefone (+55 e nacional), foto base64, data de nascimento e tipos de campos.
"""

# ==============================
# Importações (Dependencies)
# ==============================
import base64  # Para decodificação e validação de arquivos em strings base64
from ..globals.std import datetime, date, re, unicodedata, Dict, Any, List  # Utilitários de sistema e tipos
from .gerador import gerar_email  # Para validar se o e-mail gerado pelo front condiz com a lógica do back

# ==============================
# Validações de Identidade
# ==============================

def validar_nome(nome: str) -> bool:
    """
    Valida se o nome contém apenas letras e espaços, após remover acentuação.

    Args:
        nome (str): String original contendo o nome do usuário.

    Returns:
        bool: True se for um nome válido (alfabético), False caso contrário.
    """
    if not nome:
        return False
    # Normaliza e remove acentos para validar apenas os caracteres base
    nome_sem_acentos: str = ''.join(c for c in unicodedata.normalize('NFD', nome) if unicodedata.category(c) != 'Mn')

    # Busca por qualquer caractere que NÃO seja letra ou espaço
    if re.search(r'[^A-Za-z\s]', nome_sem_acentos):
        return False

    # Garante que não restou apenas uma string vazia após a limpeza
    nome_limpo: str = re.sub(r'\s+', ' ', nome_sem_acentos).strip()
    return bool(nome_limpo)

def validar_nome_com_acentos(nome: str) -> bool:
    """
    Valida nomes permitindo caracteres acentuados latinos.

    Args:
        nome (str): Nome a ser validado.

    Returns:
        bool: True se o nome contiver apenas letras (acentuadas ou não) e espaços.
    """
    if not nome:
        return False
    nome_limpo: str = ' '.join(nome.strip().split())
    # Regex cobre o intervalo de caracteres acentuados da tabela Unicode/Latin-1
    regex: str = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$'
    return bool(re.fullmatch(regex, nome_limpo))

# ==============================
# Segurança e Credenciais
# ==============================

def validar_senha(senha: str) -> Dict[str, Any]:
    """
    Verifica a força da senha baseada em requisitos de complexidade.

    Regras: Mínimo 8 caracteres, sem espaços, 1 maiúscula, 1 minúscula, 1 número e 1 especial.



    Args:
        senha (str): A senha em texto puro.

    Returns:
        Dict[str, Any]: Dicionário com 'condicao' (bool) e 'mensagem' (str).
    """
    minimo: bool = len(senha) >= 8 and ' ' not in senha
    minusculo: bool = bool(re.search(r'[a-z]', senha))
    maiusculo: bool = bool(re.search(r'[A-Z]', senha))
    # Verifica simultaneamente número e caractere especial definido
    caracter_especial: bool = bool(re.search(r'\d', senha)) and bool(re.search(r'[@$!%*?&]', senha))

    all_ok: bool = minimo and minusculo and maiusculo and caracter_especial
    return {
        "condicao": all_ok,
        "mensagem": "" if all_ok else "Uma ou mais condições da senha não foi atendida"
    }

# ==============================
# Validações de Comunicação
# ==============================

def validar_email_gerado(nome: str, sobrenome: str, email_front: str) -> bool:
    """
    Valida se o e-mail institucional recebido do front-end é válido para o usuário.

    Args:
        nome (str): Primeiro nome.
        sobrenome (str): Sobrenome completo.
        email_front (str): E-mail que o usuário selecionou/digitou no front.

    Returns:
        bool: True se o e-mail for uma das combinações permitidas pela lógica interna.
    """
    combinacoes_validas: List[str] = gerar_email(nome, sobrenome)
    return email_front.lower() in combinacoes_validas

def validar_telefone_com_55(telefone: str) -> bool:
    """
    Valida o formato E.164 brasileiro com o prefixo do país (+55).
    Exemplo: +5511999999999
    """
    if telefone == "":
        return True
    padrao: str = r'^\+55[1-9][0-9]9\d{8}$'
    return bool(re.fullmatch(padrao, telefone))

def validar_telefone(telefone: str) -> bool:
    """Valida telefone celular brasileiro (DDD + 9 dígitos) sem o prefixo do país."""
    padrao: str = r'^[1-9][0-9]9\d{8}$'
    return bool(re.fullmatch(padrao, telefone))

def validar_email_pessoal(email: str) -> bool:
    """
    Valida se o e-mail pessoal pertence a domínios de grandes provedores.

    Args:
        email (str): E-mail pessoal fornecido.

    Returns:
        bool: True se vazio ou pertencente a: gmail, hotmail, outlook ou yahoo.
    """
    dominios_permitidos: List[str] = ['gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com']
    if email == "":
        return True

    regex_email: str = r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$'
    if not re.fullmatch(regex_email, email):
        return False

    dominio: str = email.split('@')[1].lower()
    return dominio in dominios_permitidos

# ==============================
# Arquivos e Datas
# ==============================

def validar_foto(foto: Dict[str, Any]) -> bool:
    """
    Valida a integridade de uma imagem enviada via Base64.

    Args:
        foto (Dict[str, Any]): Dicionário contendo {'base64': str, 'tipo': str}.

    Returns:
        bool: True se o tipo for permitido e o conteúdo for um Base64 válido.
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
        # Tenta decodificar para garantir que a string é um base64 real
        base64.b64decode(base64_str, validate=True)
    except Exception:
        return False
    return True

def validar_data_nascimento(data: datetime | str) -> bool:
    """
    Valida a data de nascimento e impede datas no futuro.

    Args:
        data (datetime | str): Objeto datetime ou string de data.

    Returns:
        bool: True se a data existir e for menor ou igual a hoje.
    """
    nascimento = None

    if isinstance(data, datetime):
        nascimento = data
    elif isinstance(data, str):
        # Tenta converter diversos formatos comuns de data
        try:
            nascimento = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                # Trata formato ISO (comum em APIs Javascript)
                nascimento = datetime.fromisoformat(data.replace('Z', '+00:00'))
            except ValueError:
                return False

    if not nascimento or nascimento.date() > date.today():
        return False

    return True

# ==============================
# Categorias de Campos (Enums)
# ==============================

def validar_tipo_email(tipo_email: str) -> bool:
    """Valida a categoria do e-mail: home, other ou work."""
    TIPOS_PERMITIDOS = ["home", "other", "work"]
    return tipo_email in TIPOS_PERMITIDOS

def validar_tipo_telefone(tipo_telefone: str) -> bool:
    """Valida a categoria do telefone conforme padrões do CRM/Sistema."""
    TIPOS_PERMITIDOS = ["home","main","mobile","other","private_fax","work","work_fax"]
    return tipo_telefone in TIPOS_PERMITIDOS

# ==============================
# Exportações
# ==============================
__all__ = [
    "validar_telefone",
    "validar_foto",
    "validar_nome",
    "validar_senha",
    "validar_tipo_email",
    "validar_tipo_telefone",
    "validar_data_nascimento",
    "validar_email_gerado",
    "validar_email_pessoal",
    "validar_telefone_com_55",
    "validar_nome_com_acentos"
]