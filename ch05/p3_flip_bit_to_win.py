import unittest


def flip_bit_to_win(n: int) -> int:
    last_len, current_len, max_len  = 0, 0, 0
    while n > 0:
        if n & 1:
            current_len += 1
        else:
            if current_len != 0:
                last_len = current_len
                current_len = 0
            else:
                last_len = 0
        max_len = max(max_len, last_len + current_len + 1)
        n >>= 1
    return max_len 


class TestFlipBitToWin(unittest.TestCase):
    def test(self):
        self.assertEqual(flip_bit_to_win(1775), 8)
        self.assertEqual(flip_bit_to_win(175), 6)
        self.assertEqual(flip_bit_to_win(172), 4)

if __name__ == '__main__':
    unittest.main()
