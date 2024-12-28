import unittest
import time
from Decorators.timing_decorators import timing_decorator


class TestTimingDecorator(unittest.TestCase):
    def test_timing_decorator_basic(self):
        @timing_decorator
        def test_function():
            time.sleep(1)
            return "test complete"

        result = test_function()
        self.assertEqual(result, "test complete")

    def test_timing_decorator_with_args(self):
        @timing_decorator
        def test_function_with_args(x, y):
            time.sleep(0.5)
            return x + y

        result = test_function_with_args(3, 4)
        self.assertEqual(result, 7)

    def test_timing_decorator_with_kwargs(self):
        @timing_decorator
        def test_function_with_kwargs(x, y=10):
            time.sleep(0.5)
            return x + y

        result = test_function_with_kwargs(5, y=15)
        self.assertEqual(result, 20)


if __name__ == "__main__":
    unittest.main()
