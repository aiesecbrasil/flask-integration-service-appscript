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
from typing import Any

from pydantic import ConfigDict          # Configurações de comportamento dos modelos Pydantic

from app.dto import (  # Objetos de transferência de dados e enums de status
    LeadPselInput,
    ReponseOutPutPreCadastro,
    HttpStatus, BaseErrorResponse, ValidationErrorResponse
)
from app.api.version1.services import (  # Camada de Serviço: Onde a lógica de negócio reside
    cadastrar_lead_psel_service,
    validar_token_service
)
from app.utils import (                  # Funções utilitárias de validação de Regex e formatos
    validar_nome_com_acentos,
    validar_telefone
)
from app.globals import List,Dict
from app.helper import tem_mais_de_31_anos # Regra específica da AIESEC para limite de idade

# =================================================================
# CONTROLLER: CADASTRO DE LEAD
# =================================================================

@validar
def cadastrar_lead_psel_controller(data: LeadPselInput) -> tuple[
                                                               BaseErrorResponse, HttpStatus] | ReponseOutPutPreCadastro | Any:
    """
    Endpoint para pré-cadastro de lead no PSEL.
    Executa validações de conteúdo em paralelo (Fail Fast).
    """

    # 1. DEFINIÇÃO DAS TAREFAS DE VALIDAÇÃO
    # Criamos uma estrutura para validar campos únicos.
    tarefas_simples = [
        (validar_nome_com_acentos, data.nome, ["Nome","Nome inválido"]),
        (tem_mais_de_31_anos, data.data_nascimento, ["Data de Nascimento","Candidato deve ter menos de 31 anos (Limite AIESEC)"])
    ]

    # 2. EXECUÇÃO PARALELA (ThreadPoolExecutor)
    #
    with ThreadPoolExecutor() as executor:
        # Dicionário para mapear a 'Future' (tarefa em execução) à sua mensagem de erro
        futures = {executor.submit(func, arg): msg for func, arg, msg in tarefas_simples}

        # Adiciona validações dinâmicas para a lista de telefones
        for tel in data.telefones:
            futures[executor.submit(validar_telefone, tel.numero)] = ["numero",f"Telefone {tel.numero} inválido"]

        # 3. MONITORAMENTO DE RESULTADOS (Fail Fast)
        # as_completed retorna as tarefas assim que elas terminam, não importando a ordem.
        erro_msg:List[str] = []
        campo:List[str] = []
        formatar_detalhe:List[Dict[str,str]] = []
        chave_verificadora:set = set()
        cont_camp:int = 0
        cont_erro_msg:int = 0
        for future in as_completed(futures):
            resultado = future.result()
            # Se qualquer validação retornar False, interrompemos e retornamos erro 400.
            if not resultado:
                campo.append(futures[future][0])
                erro_msg.append(futures[future][1])
                chave_unica = f"{campo[cont_camp]}|{erro_msg[cont_erro_msg]}"
                if chave_unica not in chave_verificadora:
                    formatar_detalhe.append({
                        "loc":campo[cont_camp],
                        "msg":erro_msg[cont_erro_msg]
                    })
                    chave_verificadora.add(chave_unica)
                    cont_camp+=1
                    cont_erro_msg+=1

        if len(erro_msg) > 0:
            data = {
                "type": "ValidationError",
                "message": "Dados inválidos",
                "error_details":formatar_detalhe,
                "status_code": HttpStatus.UNPROCESSABLE_ENTITY
            }
            response_data =ValidationErrorResponse(**data)
            return response_data.model_dump(), response_data.status_code

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