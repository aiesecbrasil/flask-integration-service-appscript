import os
from dotenv import load_dotenv
load_dotenv(".env")

from api import create_app
from waitress import serve

app = create_app()

if __name__ == "__main__":
    if os.getenv("AMBIENTE") in {"DEVELOPMENT", "DEV", "TEST", "TESTING"}:
        app.run(debug=True)
    else:
        serve(app, host="0.0.0.0", port=5000)