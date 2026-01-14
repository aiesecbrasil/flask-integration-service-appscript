import os
from flask_migrate import init, migrate, upgrade, Migrate

migrates = Migrate()


def migration() -> None:
    # 1. Pega o caminho de: /home/BaziAiesectest/flask-integration-service-appscript/app/manager/
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    # 2. Sobe dois níveis para chegar em: /home/BaziAiesectest/flask-integration-service-appscript/
    raiz_projeto = os.path.abspath(os.path.join(diretorio_atual, "..", ".."))

    # 3. Define a pasta migrations na raiz
    migrations_dir = os.path.join(raiz_projeto, 'migrations')

    if not os.path.exists(migrations_dir):
        print(f"Criando diretório de migrações em: {migrations_dir}")
        init(directory=migrations_dir)

    try:
        print("Executando migrate e upgrade...")
        migrate(directory=migrations_dir)
        upgrade(directory=migrations_dir)
    except Exception as e:
        print(f"Erro na migração: {e}")