"""
Helpers de validação específicos da camada de apresentação/regras de negócio.
"""

# ==============================
# Importações (Dependencies)
# ==============================
import re                           # Biblioteca de Expressões Regulares para validação de padrões
from ..globals import List, date, datetime # Tipagem e objetos de manipulação de data/tempo

# ==============================
# Validações de Formato e Regras
# ==============================

def validar_codigo_membresia(codigo: str) -> bool:
    """
    Valida se o código de membresia possui exatamente 5 dígitos numéricos.

    Esta função limpa caracteres especiais indesejados e foca na estrutura
    esperada para IDs internos da organização.

    Args:
        codigo (str): String contendo o código de membresia.

    Returns:
        bool: True se for um padrão numérico de 5 dígitos (incluindo espaços).
    """
    # Remove qualquer caractere que não seja número ou espaço (limpeza preventiva)
    codigo_limpo: str = re.sub(r'[^0-9\s]', '', codigo)

    # Define o padrão: apenas números e espaços do início ao fim
    regex: str = r'^[0-9\s]+$'

    return bool(re.fullmatch(regex, codigo_limpo) and len(codigo_limpo) == 5)


def validar_email_pessoal_obrigatorio(email: str) -> bool:
    """
    Valida se o e-mail pertence a um dos grandes provedores públicos.

    Regra de Negócio: Impede o uso de e-mails corporativos ou domínios
    desconhecidos em etapas onde o contato pessoal é obrigatório.



    Args:
        email (str): Endereço de e-mail para verificação.

    Returns:
        bool: True se o formato for válido e o domínio estiver na 'Allow List'.
    """
    dominios_permitidos: List[str] = ['gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com']

    # Padrão RFC padrão para validação de formato de e-mail
    regex_email: str = r'^[\w\.-]+@([\w-]+\.)+[\w-]{2,4}$'

    if not re.fullmatch(regex_email, email):
        return False

    # Extrai o domínio após o '@' para comparação
    dominio: str = email.split('@')[1].lower()
    return dominio in dominios_permitidos


def tem_mais_de_31_anos(data_nascimento: datetime | str) -> bool:
    """
    Verifica se o candidato atende ao critério de idade (limite: 31 anos).

    Esta é uma regra crítica para programas de intercâmbio ou voluntariado
    jovem que possuem restrição de faixa etária.



    Args:
        data_nascimento (datetime | str): Objeto de data ou string formatada.

    Returns:
        bool: True se a pessoa tiver 31 anos ou menos. False se tiver 32 ou mais.
    """
    # 1. Normalização da entrada para o tipo 'date'
    if isinstance(data_nascimento, datetime):
        nascimento = data_nascimento.date()
    elif isinstance(data_nascimento, str):
        # Converte a string considerando o formato padrão de timestamp do banco/API
        nascimento = datetime.strptime(data_nascimento, "%Y-%m-%d %H:%M:%S").date()
    else:
        nascimento = data_nascimento  # Assume que o objeto já é do tipo 'date'

    hoje = date.today()

    # Cálculo base pela diferença de anos
    idade = hoje.year - nascimento.year

    # Ajuste fino: Se o mês/dia atual for menor que o de nascimento,
    # significa que a pessoa ainda não fez aniversário este ano.
    if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
        idade -= 1

    # Retorna True se estiver dentro do limite (<= 31)
    return not (idade > 31)

# ==============================
# Exportações
# ==============================
__all__ = [
    "tem_mais_de_31_anos",
    "validar_codigo_membresia",
    "validar_email_pessoal_obrigatorio"
]