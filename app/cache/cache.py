"""
cache.py
--------

Gerenciamento de cache em memória usando timestamps no horário de São Paulo.
Garante que a aplicação não sobrecarregue serviços externos com chamadas repetitivas.
"""

# ==============================
# Importações (Dependencies)
# ==============================
import logging                      # Sistema de logs para monitorar hits/misses do cache
from ..globals import (
    jsonify,                        # Converte dicionários Python para resposta JSON do Flask
    Any,                            # Tipo genérico para qualquer valor
    Callable,                       # Define que um argumento deve ser uma função/executável
    Dict,                           # Define o tipo de dicionário
    Tuple                           # Define o tipo de tupla (status_code, data)
)
from ..config import CACHE_TTL      # Tempo de vida do cache definido nas configurações globais
from ..utils import (
    agora_timestamp,                # Captura o tempo atual em segundos (fuso SP)
    resolve_response                # Trata funções assíncronas para garantir o retorno dos dados
)

# Configura o logger específico para este módulo
logger = logging.getLogger(__name__)

# =================================================================
# GERENCIADOR DE CACHE
# =================================================================



class CacheManager:
    """
    Classe responsável por armazenar e validar dados temporários em memória RAM.
    """
    def __init__(self):
        # Dicionário que servirá como banco de dados volátil
        # Estrutura esperada: { "chave": { "data": valor, "timestamp": tempo_da_criacao } }
        self.store: Dict[str, Dict[str, Any]] = {}

    def get_or_set(self, key: str, fetch: Callable[[], Tuple[Any, int]], baixando: str):
        """
        Lógica de 'Cache-Aside': Se existe e é válido, retorna. Se não, busca e guarda.

        Args:
            key: Identificador único do recurso (ex: 'tokens_podio').
            fetch: Função que será executada caso o cache não exista ou expire.
            baixando: Nome amigável para aparecer nos registros de log.
        """

        # Captura o momento exato da verificação
        now = agora_timestamp()

        # 1. TENTATIVA DE HIT (Cache válido)
        if key in self.store:
            item = self.store[key]
            # Verifica se o tempo decorrido é menor que o TTL definido
            if now - item["timestamp"] < CACHE_TTL:
                logger.info(f"Cache HIT: {baixando} recuperado da memória.")
                return jsonify(item["data"]), 200

        # 2. TRATAMENTO DE MISS (Cache inexistente ou expirado)
        logger.info(f"Cache MISS: {baixando} expirado ou inexistente. Iniciando download...")

        # Executa a função de busca (callback)
        result = fetch()

        # Garante que, se a função for assíncrona, o resultado seja aguardado
        status, data = resolve_response(result)

        # 3. PERSISTÊNCIA EM MEMÓRIA
        # Registra os novos dados e reseta o cronômetro de expiração
        self.store[key] = {
            "data": data,
            "timestamp": now
        }
        logger.info(f"{baixando.title()} Concluido com Sucesso!")
        return jsonify(data), status

# Instância única (Singleton) para ser compartilhada por toda a aplicação
cache = CacheManager()