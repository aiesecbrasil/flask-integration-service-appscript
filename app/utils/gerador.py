"""
Geração de combinações de e-mails institucionais a partir de nome e sobrenome.
"""

# ==============================
# Importações (Dependencies)
# ==============================
from ..globals.std import List  # Tipagem para listas conforme o padrão do projeto
from .formatar import limpar_palavras  # Função que remove acentos, conectores (de, da) e vogais soltas


# ==============================
# Lógica de Geração de E-mails
# ==============================

def gerar_email(nome: str, sobrenome: str) -> List[str]:
    """
    Gera combinações possíveis de e-mails institucionais baseadas em nome e sobrenome.

    A função limpa as palavras irrelevantes e cria uma lista de endereços no 
    formato 'nome.sobrenome@aiesec.org.br'. A ordem dos sobrenomes é invertida 
    para priorizar o sobrenome final (geralmente o principal).



    Args:
        nome (str): Primeiro nome (ou nome completo) do usuário.
        sobrenome (str): Sobrenome(s) do usuário.

    Returns:
        List[str]: Lista de strings contendo as combinações de e-mails em letras minúsculas.

    Exemplo:
        gerar_email("João", "da Silva Sauro") 
        -> ["joao.sauro@aiesec.org.br", "joao.silva@aiesec.org.br"]
    """

    # 1. Filtra conectores e acentos: "João da Silva" -> (["Joao"], ["Silva"])
    primeiro_nome, ultimo_sobrenome = limpar_palavras(nome, sobrenome)

    # 2. Gera a permutação entre os nomes e os sobrenomes filtrados
    # O uso do 'reversed' no sobrenome garante que o e-mail com o último sobrenome venha primeiro na lista.
    return [
        f"{n}.{s}@aiesec.org.br".lower()
        for n in primeiro_nome
        for s in reversed(ultimo_sobrenome)
    ]


# ==============================
# Exportações
# ==============================
__all__ = ["gerar_email"]