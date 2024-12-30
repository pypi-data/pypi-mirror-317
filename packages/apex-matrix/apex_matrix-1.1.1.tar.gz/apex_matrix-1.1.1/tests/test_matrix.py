import unittest
from apex_matrix.matrix import Matrix

class TestMatrix(unittest.TestCase):
    def test_addition(self):
        matrix_a = Matrix([[1, 2], [3, 4]])
        matrix_b = Matrix([[5, 6], [7, 8]])
        result = matrix_a + matrix_b
        expected = Matrix([[6, 8], [10, 12]])
        self.assertEqual(result, expected)

    def test_subtraction(self):
        matrix_a = Matrix([[-10, 5], [20, -1]])
        matrix_b = Matrix([[5, -2], [7, -10]])
        result = matrix_a - matrix_b
        expected = Matrix([[-15, 7], [13, 9]])
        self.assertEqual(result, expected)

    def test_matrix_x_matrix_multiplication(self):
        matrix_a = Matrix([[1, 2], [3, 4]])
        matrix_b = Matrix([[5, 6, 7], [8, 9 , 10]])
        result = matrix_a * matrix_b
        expected = Matrix([[21, 24, 27], [47, 54, 61]])
        self.assertEqual(result, expected)

    def test_matrix_x_scalar_multiplication(self):
        matrix_a = Matrix([[1, 2], [3, 4]])
        result = matrix_a * 2
        expected = Matrix([[2, 4], [6, 8]])
        self.assertEqual(result, expected)

    def test_scalar_x_matrix_multiplication(self):
        matrix_a = Matrix([[1, 2], [3, 4]])
        result = 2 * matrix_a
        expected = Matrix([[2, 4], [6, 8]])
        self.assertEqual(result, expected)

    def test_incompatible_dimension_matrix_multiplication(self):
        # 3x3 * 2x3 matrix should raise a value error
        matrix_a = Matrix([[1, 2, 0], [3, 4, 0], [3, 4, 0]])
        matrix_b = Matrix([[5, 6, 7], [8, 9, 10]])

        with self.assertRaises(ValueError):
            result = matrix_a * matrix_b

    def test_incompatible_matrix_dimension_in_element_wise_product(self):
        # 3x3 * 2x3 matrix should raise a value error
        matrix_a = Matrix([[1, 2, 0], [3, 4, 0], [3, 4, 0]])
        matrix_b = Matrix([[5, 6, 7], [8, 9, 10]])

        with self.assertRaises(ValueError):
            result = matrix_a * matrix_b


    def test_incompatible_type_in_element_wise_product(self):
        # 3x3 * 2x3 matrix should raise a value error
        matrix_a = Matrix([[1, 2, 0], [3, 4, 0], [3, 4, 0]])
        scalar = 2

        with self.assertRaises(TypeError):
            result = matrix_a.element_wise_product(scalar)

    def test_element_wise_matrix_product(self):
        # 3x3 * 2x3 matrix should raise a value error
        matrix_a = Matrix([[1, 2, 0], [3, 4, 10]])
        matrix_b = Matrix([[5, 6, 7], [8, 9, 0]])
        expected = Matrix([[5, 12, 0], [24, 36, 0]])
        result = matrix_a.element_wise_product(matrix_b)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()