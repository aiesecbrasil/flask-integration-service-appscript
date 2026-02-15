"""
globals.http
-----------

Imports globais para comunicação HTTP e processamento assíncrono.
Centraliza as ferramentas necessárias para integração com APIs externas (ex: Podio)
garantindo que o projeto utilize padrões não-bloqueantes.

Uso:
    from ..globals import httpx, asyncio
"""

# ==============================
# Comunicação e Async
# ==============================

# httpx: Cliente HTTP de última geração que suporta chamadas síncronas e assíncronas.
# É o sucessor espiritual do 'requests', sendo ideal para ambientes Flask/FastAPI.
import httpx

# asyncio: Biblioteca base para programação concorrente no Python.
# Usada para gerenciar loops de eventos e execução de múltiplas tarefas em paralelo.
import asyncio

# ==============================
# Exportação Pública
# ==============================



__all__ = [
    "httpx",   # Cliente HTTP para requisições externas
    "asyncio", # Gerenciador de corrotinas e concorrência
]