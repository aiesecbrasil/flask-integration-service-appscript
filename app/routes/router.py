from ..globals import jsonify, Callable
from flask import Blueprint
import inspect

class Router:
    def __init__(self, name: str | None = None, url_prefix: str = ""):
        self.bp = Blueprint(
            name or __name__,
            __name__,
            url_prefix=url_prefix
        )

    def _wrap(self, fn: Callable):
        async def wrapper(*args, **kwargs):
            result = await fn(*args, **kwargs)

            # Se já for Response/tuple, retorna direto
            if isinstance(result, tuple):
                return result

            return jsonify(result)

        return wrapper

    def get(self, path: str):
        return self._route(path, ["GET"])

    def post(self, path: str):
        return self._route(path, ["POST"])

    def put(self, path: str):
        return self._route(path, ["PUT"])

    def delete(self, path: str):
        return self._route(path, ["DELETE"])

    def _route(self, path: str, methods: list[str]):
        def decorator(fn: Callable):
            endpoint = fn.__name__

            # Suporte a async e sync
            view = self._wrap(fn) if inspect.iscoroutinefunction(fn) else fn

            self.bp.add_url_rule(
                path,
                endpoint=endpoint,
                view_func=view,
                methods=methods
            )
            return fn
        return decorator

__all__ = ["Router"]
