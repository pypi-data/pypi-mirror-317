import unittest
from matrix_operations.operations import add_matrices, multiply_matrices

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

if __name__ == '__main__':
    unittest.main()