import logging
from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS
from spectree import SpecTree
from .core import db,migrate
from .schema import ma
from .manager import migration
from .api import api
from .middlewares import verificar_origem,verificar_rota
from .core import DOMINIOS_PERMITIDOS,DB_CONNECT


def create_app():
    app = OpenAPI(
        __name__,
        info=Info(title="API", version="1.10.0"),
        validate_response=True
    )
    spec = SpecTree("flask")

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )

    logging.info("Servidor iniciando...")
    CORS(app,origins=DOMINIOS_PERMITIDOS)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNECT
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app,db)

    with app.app_context():  # Cria um contexto de aplicação para criar as tabelas no banco de dados.
        migration()   #Executa a função de migração personalizada.

    # criação de documentação:
    spec.register(app)

    # verificar requisitos antes da requisição
    app.before_request(verificar_origem)
    app.before_request(verificar_rota)

    # ==============================
    # Registro de rotas
    # ==============================
    # 1. Cria o Blueprint pai com o prefixo /api
    app.register_api(api)

    # Mapeamento de URL
    """with app.app_context():
        print("\n--- TESTE DE ROTAS ---")
        for rule in app.url_map.iter_rules():
            print(f"URL: {rule.rule} | Endpoint: {rule.endpoint}")"""

    return app

__all__ = ["create_app"]