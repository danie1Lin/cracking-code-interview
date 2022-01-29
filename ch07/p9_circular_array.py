import itertools
from typing import Any
import unittest


class CircularArray:
    def __init__(self, arr: list[Any]) -> None:
        self.arr = arr
        self.head = 0

    def rotate(self, n: int=1):
        self.head = self.true_index(n)  

    def __len__(self):
        return len(self.arr)

    def true_index(self, n):
        return (self.head + n) % len(self)
    
    def __getitem__(self, n: int):
        return self.arr[self.true_index(n)]

    def __setitem__(self, n: int, data):
        self.arr[self.true_index(n)] = data

    # have to implement or for i in self will be an infinite loop
    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

class TestCircularArrayIter(unittest.TestCase):
    def setUp(self) -> None:
        self.array = CircularArray(range(10))

    def test(self):
        self.assertEqual(1, self.array[1])
        self.array.rotate(3)
        self.assertEqual(4, self.array[1])
        # in python -8 % 3 == 1
        # in java -8 % 3 == -2
        self.assertEqual(2, self.array[-1])
        self.array.rotate(9)
        self.assertEqual(3, self.array[1])
        expect_seq = list(itertools.chain(range(2, 10), range(0, 2)))
        for idx, value in enumerate(self.array):
            self.assertEqual(expect_seq[idx], value)

if __name__ == '__main__':
    unittest.main()
