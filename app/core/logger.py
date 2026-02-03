import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from ..utils import logging_time_brasil


# 1. Caminho atual
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
# 2. Raiz do projeto
raiz_projeto = os.path.abspath(os.path.join(diretorio_atual, "..", ".."))
# 3. Pasta migrations
LOG_DIR = os.path.join(raiz_projeto, "logs")

class RequestContextFilter(logging.Filter):
    def filter(self, record):
        try:
            from flask import request, g
            record.ip = request.remote_addr if request else "-"
            record.request_id = getattr(g, "request_id", "-")
            record.user_id = getattr(g, "user_id", "-")
        except Exception:
            record.ip = "-"
            record.request_id = "-"
            record.user_id = "-"

        return True
# ISSO AQUI resolve o seu problema:
class FlushHandler(TimedRotatingFileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush() # Força a injeção no disco a cada mensagem

def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)

    # -------- FORMATOS --------
    logging.Formatter.converter = logging_time_brasil

    APP_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    AUDIT_FORMAT = "%(asctime)s | AUDIT | %(name)s | IP=%(ip)s | USER=%(user_id)s | REQ=%(request_id)s | %(message)s"

    app_formatter = logging.Formatter(APP_FORMAT)
    audit_formatter = logging.Formatter(AUDIT_FORMAT)


    root = logging.getLogger("app")
    root.setLevel(logging.INFO)
    # IMPORTANTE: Não deixe os logs do app subirem para o Root,
    # senão eles podem ser duplicados no console se o Root tiver um handler.
    root.propagate = False
    # ---------- APP LOG ----------
    app_handler = FlushHandler(
        os.path.join(LOG_DIR, "app.log"),
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8",
    )
    app_handler.suffix = "%Y-%m-%d.log"
    app_handler.setFormatter(app_formatter)
    app_handler.addFilter(RequestContextFilter())
    # Isso garante que o log não fique preso no buffer
    app_handler.flush()
    # 3. HANDLER DO CONSOLE (Para você ver no terminal também)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(app_formatter)
    # Adiciona os dois handlers ao logger "app"
    if not root.handlers:
        root.addHandler(app_handler)
        root.addHandler(console_handler)

    # 4. CONFIGURA O FLASK (WERKZEUG) PARA IR SÓ PARA O TERMINAL
    # Isso evita que o log do terminal "vaze" para o seu arquivo app.log
    flask_logger = logging.getLogger("werkzeug")
    if not flask_logger.handlers:
        flask_logger.addHandler(console_handler)
        flask_logger.propagate = False
    # ---------- AUDIT LOG ----------
    audit_handler = TimedRotatingFileHandler(
        os.path.join(LOG_DIR, "audit.log"),
        when="midnight",
        interval=1,
        backupCount=180,
        encoding="utf-8",
    )
    audit_handler.suffix = "%Y-%m-%d.log"
    audit_handler.setFormatter(audit_formatter)
    audit_handler.addFilter(RequestContextFilter())

    # evita duplicar
    if not root.handlers:
        root.addHandler(app_handler)

    audit_logger = logging.getLogger("audit")
    audit_logger.setLevel(logging.INFO)
    audit_logger.addHandler(audit_handler)
    audit_logger.propagate = False

__all__ = ["setup_logging"]