
import unittest
from Decorators.retry_decorator import retry_decorator

class TestRetryDecorator(unittest.TestCase):
    def test_successful_execution(self):
        @retry_decorator(max_retries=3)
        def successful_function():
            return "success"

        result = successful_function()
        self.assertEqual(result, "success")

    def test_retry_on_failure(self):
        self.attempt = 0

        @retry_decorator(max_retries=3)
        def failing_function():
            self.attempt += 1
            if self.attempt < 3:
                raise ValueError("Temporary error")
            return "success"

        result = failing_function()
        self.assertEqual(result, "success")
        self.assertEqual(self.attempt, 3)

    def test_max_retries_exceeded(self):
        @retry_decorator(max_retries=2)
        def always_fails():
            raise ValueError("Permanent error")

        with self.assertRaises(ValueError):
            always_fails()

if __name__ == "__main__":
    unittest.main()
