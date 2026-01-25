from .version1 import *

api = Router(name="api", url_prefix="/api")
api.register_api(v1)

__all__ = [
    "api"
]