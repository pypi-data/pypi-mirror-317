
import unittest
from Decorators.debug_decorator import debug_decorator
from io import StringIO
import sys

class TestDebugDecorator(unittest.TestCase):
    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_debug_output(self):
        @debug_decorator
        def example_function(x, y):
            return x + y

        result = example_function(2, 3)
        output = self.held_output.getvalue()

        self.assertEqual(result, 5)
        self.assertIn("Function example_function called with arguments (2, 3)", output)
        self.assertIn("Returned: 5", output)

    def test_debug_with_kwargs(self):
        @debug_decorator
        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}"

        result = greet("Alice", greeting="Hi")
        output = self.held_output.getvalue()

        self.assertEqual(result, "Hi, Alice")
        self.assertIn("keywargs {'greeting': 'Hi'}", output)

if __name__ == "__main__":
    unittest.main()
