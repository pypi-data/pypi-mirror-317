
# Python Decorators Utils

A collection of useful Python decorators including:
- Timing decorator: Measures function execution time
- Cache decorator: Implements function result caching

## Installation
```bash
pip install python-decorators-utils
```

## Usage
```python
from python_decorators_utils import timing_decorator, cache_decorator

@timing_decorator
def slow_function():
    time.sleep(1)
    return "done"

@cache_decorator
def fibonacci(n):
    if n < 2: return n
    return fibonacci(n-1) + fibonacci(n-2)
```
