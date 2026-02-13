"""
Ponto de entrada do servidor.

- Carrega variáveis de ambiente (.env)
- Configura logging
- Inicializa a aplicação Flask
- Executa com app.run (desenvolvimento) ou waitress (produção)
"""
import os
from dotenv import load_dotenv

# Ele descobre a pasta do script e junta com '.env'
path_atual = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(path_atual, ".env"))

from app.core import setup_logging,IS_NON_PROD

setup_logging()

from app import create_app
from waitress import serve

app = create_app()

if __name__ == "__main__":
    if IS_NON_PROD:
        app.run(debug=True)
    else:
        serve(app, host="0.0.0.0", port=5000)