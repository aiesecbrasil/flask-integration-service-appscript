"""
cache.py
--------

Gerenciamento de cache em memória usando timestamps no horário de Recife.
"""


from ..globals import jsonify,Any, Callable, Dict, Tuple
from ..config import CACHE_TTL
from ..utils import agora_timestamp,resolve_response

class CacheManager:
    def __init__(self):
        self.store: Dict[str, Dict[str, Any]] = {}

    def get_or_set(self, key: str, fetch: Callable[[], Tuple[Any, int]]):
        # Hora atual em São Paulo

        now = agora_timestamp()

        if key in self.store:
            item = self.store[key]
            if now - item["timestamp"] < CACHE_TTL:
                return jsonify(item["data"]), 200

        result = fetch()
        status,data = resolve_response(result)

        self.store[key] = {
            "data": data,
            "timestamp": now
        }

        return jsonify(data),status
cache = CacheManager()