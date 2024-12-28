
import unittest
from Decorators.execution_counter_decorator import execution_counter

class TestExecutionCounter(unittest.TestCase):
    def test_counter(self):
        @execution_counter
        def example_function():
            return "test"

        for _ in range(3):
            example_function()

        self.assertEqual(example_function.get_count(), 3)

    def test_multiple_functions(self):
        @execution_counter
        def func1():
            return "func1"

        @execution_counter
        def func2():
            return "func2"

        func1()
        func1()
        func2()

        self.assertEqual(func1.get_count(), 2)
        self.assertEqual(func2.get_count(), 1)

if __name__ == "__main__":
    unittest.main()
