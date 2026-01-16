import asyncio
from typing import Any, Tuple

def resolve_response(result: Any) -> Tuple[int, Any]:
    if asyncio.iscoroutine(result):
        return asyncio.run(result)
    return result

__all__ = ["resolve_response"]