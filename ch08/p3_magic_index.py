import unittest


def magic_index_slow(array: list[int]) -> int:
    for idx, v in enumerate(array):
        if idx == v :
            return v

    return -1

# O(log(n))
def magic_index(array: list[int], low=None, high=None) -> int:
    if low == None:
        low = 0
    if high == None:
        high = len(array) - 1
    if len(array[low:high+1]) == 0:
        return -1
    middle = (low+high) // 2
    if middle == array[middle]:
        return middle
    elif array[middle] < middle:
        return magic_index(array, middle + 1, high)
    elif array[middle] > middle:
        return magic_index(array, low, middle - 1)

class TestMagicIndex(unittest.TestCase):
    cases = {
            3: [-3, -2, 0, 3, 5, 8, 9],
            0: [0, 3, 5, 8, 9],
            4: [-3, -2, 0, 2, 4],
            -1: [-3, -2, 0, 2, 5],
            }
    def test_slow(self):
        for expected_magic_index, sorted_array in self.cases.items():
            self.assertEqual(expected_magic_index, magic_index_slow(sorted_array))

    def test_fast(self):
        for expected_magic_index, sorted_array in self.cases.items():
            self.assertEqual(expected_magic_index, magic_index(sorted_array))


def magic_index_not_distinct(array: list[int], low=None, high=None) -> int:
    if len(array) == 0:
        return -1
    if low == None:
        low = 0
    if high == None:
        high = len(array) - 1
    # low > high is inportant to exclude the array[middle] is negative
    # Infact, low < 0 or len(array) <= high will never happen.
    if low > high: 
        return -1
    middle = (low + high) // 2
    if array[middle] == middle:
        return middle
    elif array[middle] > middle:
        left = magic_index_not_distinct(array, low, middle - 1)
        if left >= 0:
            return left
        right = magic_index_not_distinct(array, array[middle], high)
        if right >= 0:
            return right
        return -1
    elif array[middle] < middle:
        left = magic_index_not_distinct(array, low, array[middle])
        if left >= 0:
            return left
        right = magic_index_not_distinct(array, middle + 1, high)
        if right >= 0:
            return right
        return -1
    return -1

class TestMagicIndexNotDistinct(unittest.TestCase):
    cases = {
            2: [1, 2, 2, 4, 8],
            0: [0, 3, 3, 4, 5],
            4: [-1, -1, -1, -1, 4],
            -1: [-1, -1, 3, 4, 5]
        }
    def test_slow(self):
        for expected_magic_index, sorted_array in self.cases.items():
            self.assertEqual(magic_index_not_distinct(sorted_array), expected_magic_index)

if __name__ == '__main__':
    unittest.main()
