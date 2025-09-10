
import unittest
from UnitTest_examples import add, subtract, multiply, divide

class TestCalculator(unittest.TestCase):
    """unit tests for the calculator's functions"""

    def test_addition(self):
        self.assertEqual(add(5,3),8)
        self.assertEqual(add(-1,1),0)
        self.assertEqual(add(0,0),0)
    def test_subtraction(self):
        self.assertEqual(subtract(10,4),6)
        self.assertEqual(subtract(5,10),-5)
        self.assertEqual(subtract(0,0),0)
    def test_multiplication(self):
        self.assertEqual(multiply(2,3),6)
        self.assertEqual(multiply(-2,4),-8)
        self.assertEqual(multiply(0,5),0)
    def test_division(self):
        self.assertEqual(divide(10,2),5)
        self.assertEqual(divide(-8,4),-2)
        self.assertEqual(divide(0,5),0)
        with self.assertRaises(ValueError):
            divide(10,0)

if __name__ == '__main__':
    unittest.main()
