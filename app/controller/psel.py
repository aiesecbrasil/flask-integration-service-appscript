from ..globals import Any
from ..type import LeadPselInput
from ..services import cadastrar_lead_psel_service
from ..utils import validar_nome,validar_telefone,validar_tipo_telefone,validar_tipo_email,tem_mais_de_31_anos

@validar
def cadastrar_lead_psel_controller(data:LeadPselInput) -> tuple[dict[str, Any], int] | tuple[
    dict[str, str | int | Any], int]:
    # INICIO DE VALIDADORES
    # AQUI VAI FICAR FUNÇÕES DE VALIDAÇÕES DE CONTEÚDO POIS TIPO É FEITO PELO FRAMEWORK
    # FIM DE VALIDADORES
    return cadastrar_lead_psel_service(data)


__all__ = [
    "cadastrar_lead_psel_controller"
]