import unittest
from nnthvn.module2 import to_uppercase, reverse_string

class TestModule2(unittest.TestCase):
    def test_to_uppercase(self):
        self.assertEqual(to_uppercase('hello'), 'HELLO')
        self.assertEqual(to_uppercase('world'), 'WORLD')

    def test_reverse_string(self):
        self.assertEqual(reverse_string('abc'), 'cba')
        self.assertEqual(reverse_string('12345'), '54321')

if __name__ == '__main__':
    unittest.main()
