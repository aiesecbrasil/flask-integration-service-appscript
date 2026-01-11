"""
globals.http
-----------

Imports globais para comunicação HTTP e async.
Usado principalmente em services.

Uso:
    from globals.http import httpx, asyncio
"""

import httpx
import asyncio

__all__ = [
    "httpx",
    "asyncio",
]
