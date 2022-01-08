import unittest

INT_SIZE = 32
ODD_MASK = 0
for i in range(0, INT_SIZE, 2):
    ODD_MASK |= 0b01 << i
EVEN_MASK = ODD_MASK << 1

def pairwise_swap(n: int) -> int:
    # slow way
    # result, offset = 0, 0
    # while n > 0:
        # two_bits = ((n & 0b10)>>1) | ((n & 0b1)<<1)
        # result |= two_bits << offset
        # n >>= 2
        # offset += 2
    # return result
    return ((n & EVEN_MASK)>>1) | ((n & ODD_MASK)<<1)

class TestPairwiseSwap(unittest.TestCase):
    def test(self):
        self.assertEqual(0b11010110, pairwise_swap(0b11101001))
        
if __name__ == '__main__':
    unittest.main()
