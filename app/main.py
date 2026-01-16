from flask import Flask
from flask_cors import CORS
from .repository import db
from .schema import ma
from .manager import migrates, migration
from .routes import ogx_router,psel_router
from .middlewares import verificar_origem,verificar_rota
from .config import AMBIENTE, DOMINIOS_PERMITIDOS,DB_CONNECT
from .cache import cache   # 🔥 força a inicialização



def create_app():
    app = Flask(__name__)

    if AMBIENTE == "PRODUCTION":
        CORS(app, origins=[f"https://{d}" for d in DOMINIOS_PERMITIDOS])
    else:
        CORS(app, origins="*")

    app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNECT
    db.init_app(app)
    ma.init_app(app)
    migrates.init_app(app,db)

    with app.app_context():  # Cria um contexto de aplicação para criar as tabelas no banco de dados.
        migration()   #Executa a função de migração personalizada.
        db.create_all()  # Cria todas as tabelas definidas nos modelos do banco de dados.

    app.before_request(verificar_origem)
    app.before_request(verificar_rota)

    # ==============================
    # Registro de rotas
    # ==============================
    app.register_blueprint(ogx_router.bp)
    app.register_blueprint(psel_router.bp)
    """app.register_blueprint()
    app.register_blueprint()"""

    return app

__all__ = ["create_app"]