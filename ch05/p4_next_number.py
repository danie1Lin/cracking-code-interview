import unittest

# next biggest number means smaller than n, same number of 1, biggest in the rest.
# next smallest number means bigger than n, same number of 1, smallest in the rest.

def next_number(n: int):
    l0, l1 = count_zero_first(n)
    set_first_mask = 1 << (l0 + l1)
    set_zero_mask = ((1 << 32) - 1) << (l0 + l1)
    n |= set_first_mask
    n &= set_zero_mask
    n |= (1 << (l1 - 1)) - 1
    print("next",bin(n))
    return n

def count_zero_first(n: int):
    tmp, l0, l1 = n, 0, 0
    while tmp > 0:
        if not tmp & 1:
            l0 += 1
        else:
            break
        tmp >>= 1
    while tmp > 0:
        if tmp & 1:
            l1 += 1
        else:
            break
        tmp >>= 1
    return l0, l1

def count_one_first(n: int):
    tmp, l0, l1 = n, 0, 0
    while tmp > 0:
        if tmp & 1:
            l1 += 1
        else:
            break
        tmp >>= 1
    while tmp > 0:
        if not tmp & 1:
            l0 += 1
        else:
            break
        tmp >>= 1
    return l0, l1

def pre_number(n: int):
    l0, l1 = count_one_first(n)
    # set right most 1 to 0
    zero_mask = ((1<<32) - 1) << (l1 + l0 + 1) 
    n &= zero_mask
    # set left most 0 in first 0s to 1
    one_mask = ((1 << (l1+1)) - 1) << (l0 - 1)
    n |= one_mask
    return n


class TestNextNum(unittest.TestCase):
    def test(self):
        self.assertEqual(0b11011010001111, next_number(13948))
        self.assertEqual(0b10011110000101, next_number(0b10011110000011))
        self.assertEqual(0b11011001111010, pre_number(13948))
        self.assertEqual(0b10011101110000, pre_number(0b10011110000011))

if __name__ == '__main__':
    unittest.main()
