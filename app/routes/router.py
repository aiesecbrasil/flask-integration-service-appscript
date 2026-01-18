from flask_openapi3 import APIBlueprint
from ..globals import Callable

class Router:
    def __init__(self, name: str | None = None, url_prefix: str = ""):
        self.router = APIBlueprint(
            name or __name__,
            __name__,
            url_prefix=url_prefix
        )

    # Adicionamos -> Callable para o editor saber que isso retorna um decorador
    def get(self, path: str, **kwargs) -> Callable:
        return self.router.get(path, **kwargs)

    def post(self, path: str, **kwargs) -> Callable:
        return self.router.post(path, **kwargs)

    def put(self, path: str, **kwargs) -> Callable:
        return self.router.put(path, **kwargs)

    def patch(self, path: str, **kwargs) -> Callable:
        return self.router.patch(path, **kwargs)

    def delete(self, path: str, **kwargs) -> Callable:
        return self.router.delete(path, **kwargs)

__all__ = ["Router"]
