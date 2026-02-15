"""
Fábrica da aplicação Flask (OpenAPI) com configuração de CORS, banco,
Migrações, documentação, middlewares e registro de rotas.
"""

# ==============================
# Importações (Dependencies)
# ==============================
import logging  # Registro de eventos para monitoramento do ciclo de vida da app
from flask_openapi3 import OpenAPI, Info  # Extensão Flask para documentação automática OpenAPI/Swagger
from flask_cors import CORS  # Gerenciamento de permissões de acesso entre domínios (CORS)
from spectree import SpecTree  # Gerador de documentação para APIs baseadas em tipagem
from .core import db, migrate, ma  # Instâncias de Banco (SQLAlchemy), Migrações e Serialização (Marshmallow)
from .manager import migration  # Função responsável por gerenciar a execução das migrações de dados
from .api import api  # Blueprint ou conjunto de rotas principais da aplicação
from .middlewares import verificar_origem, verificar_rota, register_url  # Funções de interceptação
from .core import  DB_CONNECT  # Configurações de ambiente: domínios e banco


def create_app() -> OpenAPI:
    """
    Inicializa e configura a aplicação Flask utilizando o padrão Factory.

    Processos realizados:
    - Instancia o objeto OpenAPI com metadados da API.
    - Carrega e registra documentação interativa via SpecTree.
    - Configura políticas de CORS para liberar headers customizados (ex: X-API-KEY).
    - Inicializa extensões de persistência (SQLAlchemy) e serialização (Marshmallow).
    - Sincroniza o esquema do banco de dados via Flask-Migrate.
    - Injeta middlewares de segurança (before_request) e auditoria (after_request).
    - Registra a árvore de rotas (Blueprints/API).

    Args:
        Nenhum parâmetro de entrada é exigido, as configurações são lidas do .env.

    Returns:
        OpenAPI: Uma instância configurada da aplicação Flask pronta para execução.

    Raises:
        Exception: Caso ocorra uma falha crítica na conexão com o banco ou inicialização.
    """

    # Inicializa o logger para capturar eventos durante o startup
    logger = logging.getLogger(__name__)

    try:
        logger.info("Servidor iniciando...")

        # Instanciação da aplicação com suporte nativo a OpenAPI 3
        app = OpenAPI(
            __name__,
            info=Info(title="API", version="1.10.0"),
            validate_response=True  # Valida se a resposta da rota condiz com a documentação
        )

        # ==========================
        # Documentação da API
        # ==========================
        logger.info("Carregando URLs de Documentação...")
        spec = SpecTree("flask")
        spec.register(app)
        logger.info("Carregamento URLs de Documentação Completo!")

        # ==========================
        # Configuração de CORS
        # ==========================
        # Permite que domínios externos consumam a API, autorizando o header X-API-KEY
        #
        logger.info("Permitindo Acesso de Domínios Autorizados...")
        CORS(app, origins=["*"],
             allow_headers=["X-API-KEY", "Content-Type", "ngrok-skip-browser-warning"],
             methods=["GET", "POST", "OPTIONS"])
        logger.info("Domínios Autorizados Cadastrados com Sucesso!")

        # ==========================
        # Conexão com Banco de Dados
        # ==========================
        # Oculta credenciais sensíveis no log
        logger.info(f"Tentando conectar ao banco: {DB_CONNECT.split('@')[-1]}")
        app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNECT

        # Inicialização técnica das extensões:

        # db (SQLAlchemy): O ORM que mapeia classes Python para tabelas relacionais.
        db.init_app(app)

        # ma (Marshmallow): O esquema que transforma dados do banco em JSON estruturado.
        ma.init_app(app)

        # migrate (Flask-Migrate): O controlador que aplica mudanças de colunas/tabelas no banco.
        migrate.init_app(app, db)

        logger.info("Banco Conectado com Sucesso!")

        # ==========================
        # Rotinas de Migração
        # ==========================
        # Executa as migrações dentro do contexto da aplicação (App Context)
        with app.app_context():
            logger.info("Entrou no contexto da aplicação. Iniciando migrações...")
            migration()
            logger.info("Migração finalizada com Sucesso!")

        # ==========================
        # Middlewares (Antes da Rota)
        # ==========================
        # Validam segurança, origem e chaves de API antes de chegar no processamento principal
        app.before_request(verificar_origem)
        app.before_request(verificar_rota)

        # Registro oficial da estrutura de endpoints
        app.register_api(api)

        logger.info("Servidor Inicializado com Sucesso!")

        # ==========================
        # Middlewares (Depois da Rota)
        # ==========================
        # Registra métricas, logs de saída ou manipula a resposta final
        app.after_request(register_url)
        for url in app.url_map.iter_rules():
            print(url.rule)

        return app

    except Exception as e:
        # Registra a falha no log e interrompe o startup para evitar estado inconsistente
        logger.error(f"FALHA CRÍTICA NO STARTUP: {str(e)}")
        raise e


# Exportação explícita da função factory
__all__ = ["create_app"]