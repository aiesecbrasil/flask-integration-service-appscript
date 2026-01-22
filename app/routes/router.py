from flask_openapi3 import APIBlueprint
from ..globals import Callable

class Router(APIBlueprint):
    def __init__(self, name: str | None = None, url_prefix: str = ""):
        # Inicializa a classe pai (APIBlueprint)
        super().__init__(
            name or __name__,
            __name__,
            url_prefix=url_prefix,
            validate_response=True
        )

__all__ = ["Router"]
