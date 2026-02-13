"""
Controladores (camada HTTP) do Processo Seletivo (PSEL).

Realizam validações de conteúdo e delegam aos serviços a orquestração de
integrações externas e persistência.
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pydantic import  ConfigDict
from app.dto import LeadPselInput,ReponseOutPutPreCadastro,HttpStatus
from app.api.version1.services import cadastrar_lead_psel_service,validar_token_service
from app.utils import validar_nome_com_acentos, validar_telefone, validar_tipo_telefone, \
    validar_data_nascimento
from app.helper import tem_mais_de_31_anos

@validar
def cadastrar_lead_psel_controller(data:LeadPselInput) -> tuple[ReponseOutPutPreCadastro, int]:
    """
    Endpoint para pré-cadastro de lead no PSEL.

    Executa validações de conteúdo em paralelo (fail fast) e, em caso de sucesso,
    delega o processamento completo ao serviço correspondente.

    Parâmetros:
    - data: LeadPselInput
        Payload validado pelo framework contendo os dados do lead.

    Retorno:
    - tuple[ReponseOutPutPreCadastro, int]:
        Resposta padronizada e o status HTTP.
    """
    # INICIO DE VALIDADORES
    # AQUI VAI FICAR FUNÇÕES DE VALIDAÇÕES DE CONTEÚDO POIS TIPO É FEITO PELO FRAMEWORK
    # Definimos uma lista de funções de validação simples (nome e data)
    tarefas_simples = [
        (validar_nome_com_acentos, data.nome, "Nome inválido"),
        (validar_data_nascimento, data.data_nascimento, "Data de nascimento inválida"),
        (tem_mais_de_31_anos, data.data_nascimento, "Candidato deve ter menos de 31 anos")
    ]

    with ThreadPoolExecutor() as executor:
        # 1. Disparamos as validações simples
        futures = {executor.submit(func, arg): msg for func, arg, msg in tarefas_simples}

        # 2. Adicionamos as validações dos telefones (loop em paralelo)
        for tel in data.telefones:
            futures[executor.submit(validar_telefone, tel.numero)] = f"Telefone {tel.numero} inválido"
            futures[executor.submit(validar_tipo_telefone, tel.tipo)] = f"Tipo de telefone {tel.tipo} inválido"

        # 3. Verificamos os resultados conforme terminam (Fail Fast)
        for future in as_completed(futures):
            resultado = future.result()
            if not resultado:
                erro_msg = futures[future]
                data = ReponseOutPutPreCadastro(**{
                    "status": "error",
                    "message": "Falha ao processar lead",
                    "data": erro_msg,
                    "status_code": HttpStatus.BAD_REQUEST
                }).model_dump()
                return data,data.get("status_code")

    # FIM DE VALIDADORES
    return cadastrar_lead_psel_service(data)

@validar(config=ConfigDict(arbitrary_types_allowed=True))
def validar_token_controller(id:int,nome:str,token:str) -> None:
    """
    Endpoint que valida o token e redireciona o candidato para o Fit Cultural.

    Parâmetros:
    - id: int
    - nome: str
    - token: str
    """
    return validar_token_service(id,nome,token)

__all__ = [
    "cadastrar_lead_psel_controller",
    "validar_token_controller"
]