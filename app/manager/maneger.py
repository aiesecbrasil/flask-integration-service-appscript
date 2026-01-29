import os
import sys
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

    # ---------- 1. Inicializa migrations automaticamente se não existir ----------
    if not os.path.exists(migrations_dir):
        print(f"[INFO] Diretório migrations não existe, criando em: {migrations_dir}")
        try:
            init(directory=migrations_dir)
            print("[INFO] Diretório migrations criado!")
            print("[INFO] Gerando primeira migration (auto)...")
            migrate(directory=migrations_dir)
            print("[INFO] Aplicando upgrade inicial...")
            upgrade(directory=migrations_dir)
            print("[OK] Migration inicial e upgrade aplicados!")
        except Exception as e:
            print(f"[ERRO] Falha ao inicializar migrations: {e}")
            return

    # ---------- 2. Detecta comando do terminal ----------
    if "migrate" in args:
        print("[LOG] Usuário executou MIGRATE")
        try:
            migrate(directory=migrations_dir)
            print("[OK] MIGRATE concluído!")
        except Exception as e:
            print(f"[ERRO] Falha no migrate: {e}")

    elif "upgrade" in args:
        print("[LOG] Usuário executou UPGRADE")
        try:
            upgrade(directory=migrations_dir)
            print("[OK] UPGRADE concluído!")
        except Exception as e:
            print(f"[ERRO] Falha no upgrade: {e}")

    elif "downgrade" in args:
        print("[LOG] Usuário executou DOWNGRADE")
        try:
            downgrade(directory=migrations_dir,sql=True)
            print("[OK] DOWNGRADE concluído!")
        except Exception as e:
            print(f"[ERRO] Falha no downgrade: {e}")

    # ---------- 3. Debug ----------
    try:
        print(f"[DEBUG] Versão atual do banco: {current(directory=migrations_dir)}")
        print("[DEBUG] Migrations disponíveis:")
        show(directory=migrations_dir)
    except Exception as e:
        print(f"[ERRO] Debug migrations: {e}")

