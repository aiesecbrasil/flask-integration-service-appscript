"""
Módulo de Infraestrutura: AIESEC Security - Cache Layer.

Gerenciamento de cache em memória (RAM) utilizando o padrão Cache-Aside.
Este módulo evita chamadas repetitivas a serviços externos, respeitando um
tempo de vida (TTL) configurado globalmente.
"""

# ==============================
# Importações (Dependencies)
# ==============================
import logging                      # Sistema de registros para monitoramento
from dataclasses import dataclass    # Facilita a criação de classes de estrutura de dados
from ..globals import (
    jsonify,                        # Serializador JSON para respostas HTTP
    Any,                            # Tipo flexível para aceitar diversos formatos de dados
    Callable,                       # Tipo para funções passadas como argumento (callbacks)
    Dict,                           # Definição de dicionários tipados
    Tuple                           # Definição de tuplas para retorno (status, data)
)
from ..config import CACHE_TTL      # Tempo limite (em segundos) definido no ambiente global
from ..utils import (
    agora_timestamp,                # Função para obter tempo atual (Horário de São Paulo)
    resolve_response                # Garante o tratamento de retornos síncronos ou assíncronos
)

# =================================================================
# CONFIGURAÇÕES DE LOGGING
# =================================================================

# Permite rastrear economia de processamento e falhas de sincronização.
logger = logging.getLogger(__name__)

# =================================================================
# GERENCIADOR DE CACHE
# =================================================================

@dataclass
class CacheManager:
    """
    Controla o ciclo de vida de dados voláteis armazenados em memória.
    """
    def __init__(self):
        """
        Inicializa o repositório central de cache.
        """
        # store: Dicionário que mapeia uma 'chave' para um objeto contendo os dados e o tempo de criação.
        # Exemplo: { "podio_token": { "data": {...}, "timestamp": 1700000000 } }
        self.store: Dict[str, Dict[str, Any]] = {}

    def get_or_set(self, key: str, fetch: Callable[[], Tuple[Any, int]], baixando: str):
        """
        Executa a estratégia Cache-Aside. Se os dados estiverem válidos, retorna o cache (HIT).
        Caso contrário, busca os dados na fonte e atualiza a memória (MISS).

        Args:
            key (str): Identificador único do recurso no cache.
            fetch (Callable): Função de fallback para buscar os dados se o cache falhar.
            baixando (str): Nome descritivo do recurso para logs de auditoria.

        Returns:
            Response: Objeto JSON formatado e o status HTTP correspondente.
        """

        # now: Captura o timestamp atual em segundos para validar a expiração.
        now = agora_timestamp()

        # --- 1. CENÁRIO: CACHE HIT (Sucesso na Memória) ---
        if key in self.store:
            # item: Recupera o registro do cache para verificação de tempo.
            item = self.store[key]

            # Verifica se o tempo desde a criação é menor que o tempo de vida permitido (TTL).
            if now - item["timestamp"] < CACHE_TTL:
                logger.info(f"AIESEC Cache | HIT: '{baixando}' recuperado da memória.")
                return jsonify(item["data"]), 200

        # --- 2. CENÁRIO: CACHE MISS (Inexistente ou Expirado) ---
        logger.info(f"AIESEC Cache | MISS: '{baixando}' expirado ou novo. Sincronizando com a fonte...")

        # result: Chama a função (callback) para obter os dados originais.
        result = fetch()

        # status, data: Resolve o resultado (aguarda se for assíncrono) e extrai status e corpo.
        status, data = resolve_response(result)

        # --- 3. PERSISTÊNCIA E ATUALIZAÇÃO ---
        # Armazena os dados e reseta o cronômetro para o próximo ciclo de cache.
        self.store[key] = {
            "data": data,
            "timestamp": now
        }

        logger.info(f"AIESEC Security | Sincronização de '{baixando}' concluída com sucesso!")

        return jsonify(data), status

# ==============================
# Singleton (Instância Única)
# ==============================

# cache: Objeto global utilizado para manter o estado do cache entre todas as requisições.
cache = CacheManager()

# ==============================
# Exportações
# ==============================
__all__ = ['cache']