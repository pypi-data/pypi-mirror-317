import time
from typing import Callable

def timing_decorator(func: Callable)->Callable:
  
  def wrapper(*args, **kwargs):
    
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time  = time.time()

    func_name = getattr(func, "__name__", "<anonymous>")
    
    if func_name == "<lambda>":
        func_name = "Lambda Function"
      
    print(f"Function {func.__name__} took {end_time - start_time:.4f} seconds to run")

    return result
  return wrapper


  
    
  