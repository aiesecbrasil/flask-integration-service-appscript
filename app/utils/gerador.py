"""
Geração de combinações de e-mails institucionais a partir de nome e sobrenome.
"""
from ..globals.std import List
from .formatar import limpar_palavras

def gerar_email(nome: str, sobrenome: str) -> List[str]:
    """
    Gera combinações possíveis de emails para um nome e sobrenome.

    Args:
        nome (str): Primeiro nome do usuário.
        sobrenome (str): Sobrenome do usuário.

    Returns:
        List[str]: Lista de emails possíveis.
    """
    primeiro_nome, ultimo_sobrenome =  limpar_palavras(nome, sobrenome)
    return [f"{n}.{s}@aiesec.org.br".lower() for n in primeiro_nome for s in reversed(ultimo_sobrenome)]

__all__ = ["gerar_email"]