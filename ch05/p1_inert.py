import unittest

def insert(n, m, i, j):
    return clean_up(n, i, j) | (m << i)

def clean_up(n, i, j):
    n_high = n >> (j + 1) << (j + 1)
    n_low = n - (n >> (i + 1) << (i + 1)) 
    return n_high | n_low

def insert_std(n, m, i, j):
    all_ones = ~0
    left_mask = all_ones << j
    # tips:
    # 1 << i -> 10000... amount of 0 is i
    # 10000... -1 -> 1111.... amount of 1 is i
    right_mask = (1 << i) - 1
    mask = left_mask | right_mask
    return (n & mask) | (m << i)

class TestInsert(unittest.TestCase):
    longMessage = True

    def test(self):
        self.assertEqual(insert(0b10000000000, 0b10011, 2, 6), 0b10001001100)
        self.assertEqual(insert(0b10000010001, 0b10011, 2, 6), 0b10001001101, "should overwrite between the range")
        self.assertEqual(insert_std(0b10000000000, 0b10011, 2, 6), 0b10001001100)
        self.assertEqual(insert_std(0b10000010001, 0b10011, 2, 6), 0b10001001101, "should overwrite between the range")


if __name__ == '__main__':
    unittest.main()
