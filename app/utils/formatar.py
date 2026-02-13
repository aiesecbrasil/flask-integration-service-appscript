from ..globals import unicodedata,re
from ..globals import List,Tuple
from urllib.parse import urlencode

def formatar_nome(nome: str) -> str:
    """
    Remove acentos de um nome e capitaliza cada palavra.

    Args:
        nome (str): Nome a ser formatado.

    Returns:
        str: Nome formatado sem acentos.
    """
    nome_sem_acentos: str = ''.join(c for c in unicodedata.normalize('NFD', nome) if unicodedata.category(c) != 'Mn')
    return ' '.join(p.capitalize() for p in nome_sem_acentos.split())

def formatar_nome_com_acentos(nome: str) -> str:
    """
    Formata nome com acentos, capitalizando cada palavra.

    Args:
        nome (str): Nome a ser formatado.

    Returns:
        str: Nome formatado mantendo acentos.
    """
    nome_limpo: str = ' '.join(nome.strip().split())
    return ' '.join(p.capitalize() for p in nome_limpo.split())

def limpar_palavras(nome: str, sobrenome: str) -> Tuple[List[str], List[str]]:
    """
    Remove conectores e vogais soltas de nomes e sobrenomes para gerar emails.

    Args:
        nome (str): Nome do usuário.
        sobrenome (str): Sobrenome do usuário.

    Returns:
        Tuple[List[str], List[str]]: Listas de nomes e sobrenomes filtrados.
    """
    conectores: List[str] = ["de", "da", "di", "do", "du"]
    vogais_soltas: List[str] = ["a", "e", "i", "o", "u"]

    nomes: List[str] = [formatar_nome(p) for p in re.split(r"\s+", nome.lower().strip())
                        if p not in conectores and p not in vogais_soltas]

    sobrenomes: List[str] = [formatar_nome(p) for p in re.split(r"\s+", sobrenome.lower().strip())
                             if p not in conectores and p not in vogais_soltas]

    return nomes, sobrenomes

@validar
def formatar_url(url,payload:dict=None) -> str:
    return f"{url}?{urlencode(payload)}"

__all__ = [
    "formatar_nome",
    "formatar_nome_com_acentos",
    "limpar_palavras",
    "formatar_url"
]