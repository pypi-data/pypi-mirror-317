
import unittest
from ..cache_decorator import cache_decorator

class TestCacheDecorator(unittest.TestCase):
    def test_cache_hit(self):
        # Test function to be cached
        @cache_decorator
        def add(x, y):
            return x + y
        
        # First call - should cache result
        result1 = add(2, 3)
        # Second call - should use cached result
        result2 = add(2, 3)
        
        self.assertEqual(result1, 5)
        self.assertEqual(result2, 5)
    
    def test_different_args(self):
        # Test function with different arguments
        @cache_decorator
        def multiply(x, y):
            return x * y
        
        result1 = multiply(2, 3)
        result2 = multiply(3, 4)
        
        self.assertEqual(result1, 6)
        self.assertEqual(result2, 12)
    
    def test_fibonacci(self):
        # Test with recursive function
        @cache_decorator
        def fibonacci(n):
            if n < 2:
                return n
            return fibonacci(n-1) + fibonacci(n-2)
        
        result = fibonacci(5)
        self.assertEqual(result, 5)

if __name__ == '__main__':
    unittest.main()
