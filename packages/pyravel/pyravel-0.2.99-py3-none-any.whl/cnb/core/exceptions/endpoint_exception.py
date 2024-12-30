from functools import wraps
from typing import Any, Callable
from loguru import logger

def handle_exceptions(operation: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error during {operation}: {e}")
                raise e
        return wrapper
    return decorator