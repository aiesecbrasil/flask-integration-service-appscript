from flask import Flask
from flask_cors import CORS
from .cache import cache   # 🔥 força a inicialização
from .routes import ogx_router,psel_router
from .middlewares import verificar_origem
from .config import AMBIENTE, DOMINIOS_PERMITIDOS

def create_app():
    app = Flask(__name__)
    if AMBIENTE == "PRODUCTION":
        CORS(app, origins=[f"https://{d}" for d in DOMINIOS_PERMITIDOS])
    else:
        CORS(app, origins="*")

    app.before_request(verificar_origem)

    # ==============================
    # Registro de rotas
    # ==============================
    app.register_blueprint(ogx_router.bp)
    app.register_blueprint(psel_router.bp)
    """app.register_blueprint()
    app.register_blueprint()"""

    return app

__all__ = [
    "create_app"
]