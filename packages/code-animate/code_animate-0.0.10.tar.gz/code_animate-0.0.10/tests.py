# unit tests

import unittest
from textwrap import dedent

from src.code_animate.helpers.func_helper import is_recursive

class MainTest(unittest.TestCase):

    def test_string_helper__is_recursive(self):
        src1: str = dedent("""
            def fac(n):
                if n == 1:
                    return 1
                return n * fac(n - 1)
        """)
        self.assertTrue(is_recursive(src1))

        src2: str = dedent("""
            def fib(n):
                if n <= 1:
                    return n
                return fib(n-2) + fib(n-1)
        """)
        self.assertTrue(is_recursive(src2))

        src3: str = dedent("""
            def triangle(n):
                for i in range(1, n+1)"
                    print(i * "*")
        """)
        self.assertFalse(is_recursive(src3))

if __name__ == "__main__":
    unittest.main()