"""
Funções utilitárias de formatação de nomes e construção de URLs.

- Remoção de acentos e capitalização de nomes.
- Limpeza de palavras irrelevantes em nomes/sobrenomes para geração de e-mails.
- Montagem de URL com query string a partir de um payload.
"""

# ==============================
# Importações (Dependencies)
# ==============================
from ..globals import unicodedata, re  # Manipulação de caracteres Unicode e Expressões Regulares
from ..globals import List, Tuple      # Tipagem para listas e tuplas
from urllib.parse import urlencode     # Utilitário para converter dicionários em parâmetros de URL (query string)

# ==============================
# Processamento de Nomes
# ==============================

def formatar_nome(nome: str) -> str:
    """
    Remove acentos de uma string e aplica capitalização (Title Case).

    O processo utiliza a normalização NFD para separar caracteres de seus
    acentos e filtra apenas os caracteres base.

    Args:
        nome (str): A string original contendo o nome.

    Returns:
        str: Nome sem acentos, com cada palavra iniciando em maiúscula.
    """
    # Normaliza para decompor caracteres acentuados em (caractere + acento) e remove o acento
    nome_sem_acentos: str = ''.join(
        c for c in unicodedata.normalize('NFD', nome)
        if unicodedata.category(c) != 'Mn'
    )
    # Divide a string, capitaliza cada pedaço e junta novamente com espaços
    return ' '.join(p.capitalize() for p in nome_sem_acentos.split())

def formatar_nome_com_acentos(nome: str) -> str:
    """
    Padroniza a capitalização do nome, mas preserva os acentos originais.

    Args:
        nome (str): Nome a ser formatado.

    Returns:
        str: Nome com espaços limpos e palavras capitalizadas.
    """
    # Remove espaços extras nas extremidades e entre as palavras
    nome_limpo: str = ' '.join(nome.strip().split())
    return ' '.join(p.capitalize() for p in nome_limpo.split())

def limpar_palavras(nome: str, sobrenome: str) -> Tuple[List[str], List[str]]:
    """
    Filtra conectores e partículas gramaticais para preparação de geração de emails.

    Remove elementos como "de", "da" ou vogais soltas que não agregam valor
    em identificadores de usuários.

    Args:
        nome (str): Nome do usuário.
        sobrenome (str): Sobrenome do usuário.

    Returns:
        Tuple[List[str], List[str]]: Listas contendo (nomes_filtrados, sobrenomes_filtrados).
    """
    # Lista de termos irrelevantes para a composição de identificadores
    conectores: List[str] = ["de", "da", "di", "do", "du"]
    vogais_soltas: List[str] = ["a", "e", "i", "o", "u"]

    # Processa nomes: converte para minúsculo, separa por espaços e filtra conectores
    nomes: List[str] = [
        formatar_nome(p) for p in re.split(r"\s+", nome.lower().strip())
        if p not in conectores and p not in vogais_soltas
    ]

    # Processa sobrenomes com a mesma lógica de filtragem
    sobrenomes: List[str] = [
        formatar_nome(p) for p in re.split(r"\s+", sobrenome.lower().strip())
        if p not in conectores and p not in vogais_soltas
    ]

    return nomes, sobrenomes

# ==============================
# Utilitários de URL
# ==============================

@validar
def formatar_url(url: str, payload: dict = None) -> str:
    """
    Constrói uma URL válida injetando parâmetros via query string.

    Utiliza o 'urlencode' para garantir que caracteres especiais (espaços,
    caracteres especiais) no payload sejam convertidos para o formato %XX.



    Args:
        url (str): A URL base ou endpoint.
        payload (dict, optional): Dicionário com chaves e valores dos parâmetros.

    Returns:
        str: URL final formatada (ex: 'https://api.com?user=123&token=abc').
    """
    if not payload:
        return url

    # Gera a query string (ex: k1=v1&k2=v2) e concatena à URL base
    return f"{url}?{urlencode(payload)}"

# ==============================
# Exportações
# ==============================
__all__ = [
    "formatar_nome",
    "formatar_nome_com_acentos",
    "limpar_palavras",
    "formatar_url"
]