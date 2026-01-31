import logging
import sys
from flask_openapi3 import OpenAPI, Info
from flask_cors import CORS
from spectree import SpecTree
from .core import db, migrate
from .schema import ma
from .manager import migration
from .api import api
from .middlewares import verificar_origem, verificar_rota
from .core import DOMINIOS_PERMITIDOS, DB_CONNECT


def create_app():
    logger = logging.getLogger(__name__)
    try:
        logger.info("Servidor iniciando...")
        app = OpenAPI(
            __name__,
            info=Info(title="API", version="1.10.0"),
            validate_response=True
        )

        # Criação de documentação
        logger.info("Carregando URL de Documentação...")
        spec = SpecTree("flask")
        spec.register(app)
        logger.info("Carregamento de Url Documentação Completo!")

        # Configurando CORS
        logger.info("Permitindo Acesso de Domínios Autorizados...")
        CORS(app, origins=DOMINIOS_PERMITIDOS)
        logger.info("Acesso de Domínios Autorizados com Sucesso!")

        # Conectando Banco de dados
        app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNECT
        logger.info(f"Tentando conectar ao banco: {DB_CONNECT.split('@')[-1]}")
        db.init_app(app)
        ma.init_app(app)
        migrate.init_app(app, db)
        logger.info("Banco Conectado.")

        # Execução de Migrações
        with app.app_context():
            logger.info("Entrou no contexto da aplicação. Iniciando migrações...")
            migration()
            logger.info("Migração finalizada.")

        # Verificar requisitos antes da requisição
        app.before_request(verificar_origem)
        app.before_request(verificar_rota)

        # Registro de rotas
        app.register_api(api)

        logger.info("Servidor Inicializado com Sucesso!")
        # Mapeamento de URL

        """with app.app_context():
            print("\n--- TESTE DE ROTAS ---")
            for rule in app.url_map.iter_rules():
                print(f"URL: {rule.rule} | Endpoint: {rule.endpoint}")"""
        return app

    except Exception as e:
        logger.error(f"FALHA CRÍTICA NO STARTUP: {str(e)}")
        raise e


__all__ = ["create_app"]