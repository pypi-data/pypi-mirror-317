import unittest
from matrix_operations_amber.operations import add_matrices, multiply_matrices

class TestMatrixOperations(unittest.TestCase):

    def test_add_matrices(self):
        matrix1 = [[1, 2], [3, 4]]
        matrix2 = [[5, 6], [7, 8]]
        expected_result = [[6, 8], [10, 12]]
        self.assertEqual(add_matrices(matrix1, matrix2), expected_result)

    def test_multiply_matrices(self):
        matrix1 = [[1, 2], [3, 4]]
        matrix2 = [[5, 6], [7, 8]]
        expected_result = [[19, 22], [43, 50]]
        self.assertEqual(multiply_matrices(matrix1, matrix2), expected_result)

    def test_add_matrices_invalid_dimensions(self):
        matrix1 = [[1, 2, 3], [4, 5, 6]]
        matrix2 = [[7, 8], [9, 10]]
        with self.assertRaises(ValueError):
            add_matrices(matrix1, matrix2)

    def test_multiply_matrices_invalid_dimensions(self):
        matrix1 = [[1, 2, 3], [4, 5, 6]]
        matrix2 = [[7, 8, 9], [10, 11, 12]]
        with self.assertRaises(ValueError):
            multiply_matrices(matrix1, matrix2)

if __name__ == '__main__':
    unittest.main()