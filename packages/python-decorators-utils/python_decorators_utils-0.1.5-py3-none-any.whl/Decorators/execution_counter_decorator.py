
import functools
from typing import Callable, Any

def execution_counter(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        wrapper.count += 1
        return func(*args, **kwargs)
    
    wrapper.count = 0
    wrapper.get_count = lambda: wrapper.count
    return wrapper
