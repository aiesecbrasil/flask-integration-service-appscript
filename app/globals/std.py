"""
globals.std
----------

Imports globais da biblioteca padrão do Python e typing.
NÃO deve conter nada específico do projeto.

Uso:
    from globals.std import datetime, List
"""

import os
import time
import re
import base64
import unicodedata

from datetime import datetime, date
from typing import Any, Dict, List, Optional, Tuple,Callable,Iterable, Union
from urllib.parse import urlparse, quote

__all__ = [
    # módulos
    "os",
    "time",
    "re",
    "base64",
    "unicodedata",

    # datetime
    "datetime",
    "date",

    # typing
    "Any",
    "Dict",
    "List",
    "Optional",
    "Tuple",
    "Callable",
    "Iterable",
    "Union",

    # url
    "urlparse",
    "quote",
]
