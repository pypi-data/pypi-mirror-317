import unittest
from converter import series, factorial

class TestConverter(unittest.TestCase):
    def test_series(self):
        self.assertEqual(series(5),15)
        self.assertEqual(series(10),55)
        self.assertEqual(series(1),1)
    
    def test_factorial(self):
        self.assertEqual(factorial(5),120)
        self.assertEqual(factorial(10),3628800)
        self.assertEqual(factorial(1),1)

if __name__ == "__main__":
    unittest.main()