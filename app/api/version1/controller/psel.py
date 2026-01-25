from concurrent.futures import ThreadPoolExecutor, as_completed
from app.globals import Any,Dict
from app.dto import LeadPselInput,ReponseOutPutPreCadastro,HttpStatus
from app.api.version1.services import cadastrar_lead_psel_service
from app.utils import validar_nome_com_acentos, validar_telefone, validar_tipo_telefone, \
    tem_mais_de_31_anos, validar_data_nascimento


@validar
def cadastrar_lead_psel_controller(data:LeadPselInput) -> tuple[ReponseOutPutPreCadastro, int]:
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

@validar
def validar_token_controller(data:Dict[str,Any]):
    return {}

__all__ = [
    "cadastrar_lead_psel_controller"
]