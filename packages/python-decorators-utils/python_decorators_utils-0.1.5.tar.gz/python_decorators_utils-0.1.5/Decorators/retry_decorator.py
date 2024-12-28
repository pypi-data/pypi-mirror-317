
from typing import Callable, TypeVar, Any
import functools
import time

T = TypeVar("T")

def retry_decorator(max_retries: int = 3, delay: float = 1.0) -> Callable:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_retries:
                        raise e
                    time.sleep(delay)
            return func(*args, **kwargs)  # Final attempt
        return wrapper
    return decorator
