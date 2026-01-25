from flask_openapi3 import OpenAPI, Info,APIBlueprint
from flask_cors import CORS
from spectree import SpecTree
from .core import db
from .schema import ma
from .manager import migrates, migration
from .api import api
from .middlewares import verificar_origem,verificar_rota
from .config import AMBIENTE, DOMINIOS_PERMITIDOS,DB_CONNECT


def create_app():
    app = OpenAPI(
        __name__,
        info=Info(title="API", version="1.10.0"),
        validate_response=True
    )
    spec = SpecTree("flask")
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

    # criação de documentação:
    spec.register(app)
    app.before_request(verificar_origem)
    app.before_request(verificar_rota)

    # ==============================
    # Registro de rotas
    # ==============================
    # 1. Cria o Blueprint pai com o prefixo /api
    app.register_api(api)

    with app.app_context():
        print("\n--- TESTE DE ROTAS ---")
        for rule in app.url_map.iter_rules():
            print(f"URL: {rule.rule} | Endpoint: {rule.endpoint}")

    return app

__all__ = ["create_app"]