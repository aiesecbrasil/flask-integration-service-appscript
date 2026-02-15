"""
Controladores (camada HTTP) do Processo Seletivo (PSEL).

Realizam validações de conteúdo e delegam aos serviços a orquestração de
integrações externas e persistência.
"""

# ==============================
# Importações (Dependencies)
# ==============================
# concurrent.futures: Permite executar validações em paralelo para otimizar o tempo de resposta.
from concurrent.futures import ThreadPoolExecutor, as_completed
from pydantic import ConfigDict          # Configurações de comportamento dos modelos Pydantic
from app.dto import (                    # Objetos de transferência de dados e enums de status
    LeadPselInput,
    ReponseOutPutPreCadastro,
    HttpStatus
)
from app.api.version1.services import (  # Camada de Serviço: Onde a lógica de negócio reside
    cadastrar_lead_psel_service,
    validar_token_service
)
from app.utils import (                  # Funções utilitárias de validação de Regex e formatos
    validar_nome_com_acentos,
    validar_telefone,
    validar_tipo_telefone,
    validar_data_nascimento
)
from app.helper import tem_mais_de_31_anos # Regra específica da AIESEC para limite de idade

# =================================================================
# CONTROLLER: CADASTRO DE LEAD
# =================================================================

@validar
def cadastrar_lead_psel_controller(data: LeadPselInput) -> tuple[ReponseOutPutPreCadastro, int]:
    """
    Endpoint para pré-cadastro de lead no PSEL.
    Executa validações de conteúdo em paralelo (Fail Fast).
    """

    # 1. DEFINIÇÃO DAS TAREFAS DE VALIDAÇÃO
    # Criamos uma estrutura para validar campos únicos.
    tarefas_simples = [
        (validar_nome_com_acentos, data.nome, "Nome inválido"),
        (validar_data_nascimento, data.data_nascimento, "Data de nascimento inválida"),
        (tem_mais_de_31_anos, data.data_nascimento, "Candidato deve ter menos de 31 anos (Limite AIESEC)")
    ]

    # 2. EXECUÇÃO PARALELA (ThreadPoolExecutor)
    #
    with ThreadPoolExecutor() as executor:
        # Dicionário para mapear a 'Future' (tarefa em execução) à sua mensagem de erro
        futures = {executor.submit(func, arg): msg for func, arg, msg in tarefas_simples}

        # Adiciona validações dinâmicas para a lista de telefones
        for tel in data.telefones:
            futures[executor.submit(validar_telefone, tel.numero)] = f"Telefone {tel.numero} inválido"
            futures[executor.submit(validar_tipo_telefone, tel.tipo)] = f"Tipo de telefone {tel.tipo} inválido"

        # 3. MONITORAMENTO DE RESULTADOS (Fail Fast)
        # as_completed retorna as tarefas assim que elas terminam, não importando a ordem.
        for future in as_completed(futures):
            resultado = future.result()
            # Se qualquer validação retornar False, interrompemos e retornamos erro 400.
            if not resultado:
                erro_msg = futures[future]
                response_data = ReponseOutPutPreCadastro(**{
                    "status": "error",
                    "message": "Falha na validação de conteúdo",
                    "data": erro_msg,
                    "status_code": HttpStatus.BAD_REQUEST
                }).model_dump()
                return response_data, response_data.get("status_code")

    # 4. DELEGAÇÃO PARA O SERVICE
    # Se todas as validações passaram, enviamos para o Service orquestrar as APIs.
    return cadastrar_lead_psel_service(data)

# =================================================================
# CONTROLLER: VALIDAÇÃO DE TOKEN
# =================================================================

@validar(config=ConfigDict(arbitrary_types_allowed=True))
def validar_token_controller(id: int, nome: str, token: str) -> None:
    """
    Intermedeia a validação de segurança do token para o Fit Cultural.
    """
    return validar_token_service(id, nome, token)

# ==============================
# Exportações do Módulo
# ==============================
__all__ = [
    "cadastrar_lead_psel_controller",
    "validar_token_controller"
]