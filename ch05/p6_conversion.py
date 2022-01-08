import unittest


def diff_digits(a: int, b: int) -> int:
    diff = a ^ b
    count = 0
    while diff > 0:
        """
        if diff & 1:
            count += 1
        """
        count += diff & 1
        diff >>= 1
    return count

class TestDiffDigits(unittest.TestCase):
    def test(self):
        self.assertEqual(2, diff_digits(0b11101, 0b01111))

if __name__ == '__main__':
    unittest.main()
