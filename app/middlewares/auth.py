"""
auth
----

Middleware para validação de API Keys e domínios.

Regras:
- Rotas em ROTAS_SEM_VALIDACAO são isentas.
- Se X-API-KEY presente, deve ser autorizada.
- Domínio (Host) deve pertencer aos domínios permitidos.
- Em produção, bloqueia requisições diretas.
"""

# ==============================
# Importações (Dependencies)
# ==============================
import logging # Biblioteca padrão para monitoramento e registro de eventos do sistema
from ..config import API_KEYS_PERMITIDAS # Lista de chaves válidas definida no arquivo de configuração
from ..core import DOMINIOS_PERMITIDOS, IS_PRODUCTION # Lista de domínios (Whitelist) e flag de ambiente (Prod/Dev)
from ..globals import request, jsonify, List, Optional,Dict # Objetos globais do Flask e tipagem estática do Python

# ==============================
# Configurações de Segurança
# ==============================
# Define endpoints que podem ser acessados publicamente sem chaves ou travas
ROTAS_SEM_VALIDACAO: List[str] = ["/validarToken"]

# Configuração do rastreador de eventos para este módulo específico
logger = logging.getLogger(__name__)

# ==============================
# Middleware de Validação
# ==============================
def verificar_origem() -> None | Dict[str,str]:
    """
    Middleware global que valida API Key e domínio antes de qualquer request.
    Retorna JSON de erro com status 403 caso bloqueado, ou None se permitido.
    """

    # Bypass para requisições de 'Preflight' do navegador (CORS)
    # Sem isso, o navegador não consegue validar se o servidor aceita headers customizados
    if request.method == 'OPTIONS':
        return None

    # Log de rastreio: indica que a requisição entrou no fluxo de segurança
    logger.info("Autenticando origem...")

    # Verificação de Whitelist de caminhos (Rotas isentas)
    if request.path in ROTAS_SEM_VALIDACAO:
        # Log informativo para debug de rotas públicas
        logger.info(f"Rota não precisou ser validada: {request.path}")
        return None

    # ==========================
    # Validação de API Key
    # ==========================
    # Extrai a chave enviada no cabeçalho HTTP
    api_key: Optional[str] = request.headers.get("X-API-KEY")

    # Se uma chave foi enviada, mas não consta na lista de permitidas, bloqueia imediatamente
    if api_key and api_key not in API_KEYS_PERMITIDAS:
        # Log de erro: registra a tentativa de acesso com chave inválida para auditoria
        logger.error(f"Chave de Api {api_key} não autorizada")
        return jsonify({"error": "API Key inválida"}), 403

    # ==========================
    # Validação de domínio (Host)
    # ==========================
    # Reconstrói a URL do Host para comparação com a lista permitida
    host: Optional[str] = f'https://{request.headers.get("Host")}'

    # Se o domínio de origem é desconhecido, a presença da API Key torna-se obrigatória
    if host and host not in DOMINIOS_PERMITIDOS:
        if not api_key:
            # Log de erro crítico: tentativa de acesso de domínio externo sem credenciais
            logger.error(f"O host {host} não autorizado")
            return jsonify({"error": "Domínio não autorizado"}), 403

    # ==========================
    # Bloqueio de Acesso Direto (Browser)
    # ==========================
    # Em produção, impede que a API seja acessada via barra de endereço (navegação direta)
    # O header 'Sec-Fetch-Mode: navigate' identifica essa ação do usuário
    if IS_PRODUCTION and request.headers.get("Sec-Fetch-Mode") == "navigate":
        # Log de segurança: impede o consumo manual dos dados da API
        logger.error(f"A api não pode ser acessada por meio de Requisições Diretas")
        return jsonify({"error": "Bloqueado: requisições diretas não são permitidas"}), 403

    # Log de sucesso: encerramento positivo do ciclo de autenticação
    logger.info("Origem autenticada com sucesso!")

    # Retornar None sinaliza ao Flask para seguir para a função da rota
    return None

# ==============================
# Exportações
# ==============================
__all__ = [
    "verificar_origem"
]