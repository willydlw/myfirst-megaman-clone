import unittest 

from vector2d import Vector2D 

class TestVector2D(unittest.TestCase):
    def setUp(self):
        self.v1 = Vector2D(3.0, 4.0)
        self.v2 = Vector2D(1.0, 2.0)

    def test_addition(self):
        result = self.v1 + self.v2 
        self.assertEqual(result, Vector2D(4.0, 6.0))

    def test_subtraction(self):
        result = self.v1 - self.v2 
        self.assertEqual(result, Vector2D(2.0, 2.0))

    def test_multiplication(self):
        result = self.v1 * 2 
        self.assertEqual(result, Vector2D(6.0, 8.0))

    def test_magnitude(self):
        self.assertAlmostEqual(self.v1.magnitude(), 5.0)
    
    def test_dot_product(self):
        self.assertEqual(self.v1.dot(self.v2), 11.0)


if __name__ == "__main__":
    unittest.main()