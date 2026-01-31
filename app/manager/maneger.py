import os
import sys
import logging
from flask_migrate import init, migrate, upgrade, downgrade, current, show,stamp

def migration() -> None:
    """
    Função de migração do banco de dados.
    - Cria migrations se não existir (auto migrate + upgrade)
    - Detecta comando do terminal: migrate / upgrade / downgrade
    - Mostra debug das versões
    """
    # 1. capturando argumentos do terminal
    args = sys.argv
    # 2. Caminho atual
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    # 3. Raiz do projeto
    raiz_projeto = os.path.abspath(os.path.join(diretorio_atual, "..", ".."))
    # 4. Pasta migrations
    migrations_dir = os.path.join(raiz_projeto, 'migrations')
    # 5. Criando Log
    logger = logging.getLogger(__name__)
    # ---------- 1. Inicializa migrations automaticamente se não existir ----------
    if not os.path.exists(migrations_dir):
        logger.info(f"Diretório migrations não existe, criando em: {migrations_dir}")
        try:
            init(directory=migrations_dir)
            logger.info("Diretório migrations criado!")
            logger.info("Gerando primeira migration (auto)...")
            migrate(directory=migrations_dir)
            logger.info("Aplicando upgrade inicial...")
            upgrade(directory=migrations_dir)
            logger.info("Migration inicial e upgrade aplicados!")
        except Exception as e:
            logger.error(f"Falha ao inicializar migrations: {e}")
            return

    # ---------- 2. Detecta comando do terminal ----------
    if "migrate" in args:
        logger.log("Usuário executou MIGRATE")
        try:
            migrate(directory=migrations_dir)
            logger.info("MIGRATE concluído!")
        except Exception as e:
            logger.error(f"Falha no migrate: {e}")

    elif "upgrade" in args:
        logger.log("Usuário executou UPGRADE")
        try:
            upgrade(directory=migrations_dir)
            logger.info("UPGRADE concluído!")
        except Exception as e:
            logger.error(f"Falha no upgrade: {e}")

    elif "downgrade" in args:
        logger.log("Usuário executou DOWNGRADE")
        try:
            downgrade(directory=migrations_dir,sql=True)
            logger.info("DOWNGRADE concluído!")
        except Exception as e:
            logger.error(f"Falha no downgrade: {e}")


    # ---------- 3. Debug ----------
    """try:
        logger.debug(f"Versão atual do banco: {current(directory=migrations_dir)}")
        logger.debug("Migrations disponíveis:")
        logger.info(show(directory=migrations_dir))
    except Exception as e:
        logger.error(f"Debug migrations: {e}")"""
