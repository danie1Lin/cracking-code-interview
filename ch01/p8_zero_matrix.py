import unittest


def zero_matrix(matrix: list[list[int]]):
    zero_rows, zero_columns = set(), set()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                zero_rows.add(i)
                zero_columns.add(j)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i in zero_rows or j in zero_columns:
                matrix[i][j] = 0



class TestZeroMatrix(unittest.TestCase):
    def test(self):
        m1 = [
            [0, 1, 2, 3],
            [1, 2, 0, 4],
            [0, 1, 2, 3],
            [1, 2, 3, 4],
        ]
        zero_matrix(m1)
        self.assertEqual(m1, [
            [0, 0, 0, 0],
            [0, 0 ,0, 0],
            [0, 0 ,0, 0],
            [0, 2 ,0, 4],
        ])

if __name__ == '__main__':
    unittest.main()
