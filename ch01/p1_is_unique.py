import unittest

def is_uniq_ascii_with_bit(s: str) -> bool:
    # ask interviewer 
    # is ascii only? 256 words
    # is a-zA-Z only? less
    bitmap = 0
    for i in s:
        pos = ord(i) 
        if flag_at(bitmap, pos):
            return False
        bitmap |= 1 << pos
    return True
    
def flag_at(bits, pos) -> bool:
    if bits & (1 << pos) > 0:
        return True
    return False

def is_uniq(s: str) -> bool:
    for i in range(len(s)):
        for j in range(i+1, len(s)):
            if s[i] == s[j]:
                return False
    return True

def is_uniq_sort_frist(s: str) -> bool:
    # sort first and check neighbor
    # T will be O(nlogn)
    s = sorted(s)
    for i in range(len(s)-1):
        if s[i] == s[i+1]:
            return False
    return True


class TestIsUniq(unittest.TestCase):
    def test(self):
        self.assertTrue(is_uniq('daniel'))
        self.assertFalse(is_uniq('hello'))
        self.assertFalse(is_uniq('Interview'))

    def test_ascii(self):
        self.assertTrue(is_uniq_ascii_with_bit('daniel'))
        self.assertFalse(is_uniq_ascii_with_bit('hello'))
        self.assertFalse(is_uniq_ascii_with_bit('Interview'))

    def test_sort_fist(self):
        self.assertTrue(is_uniq_sort_frist('daniel'))
        self.assertFalse(is_uniq_sort_frist('danniel'))
        self.assertFalse(is_uniq_sort_frist('hello'))
        self.assertFalse(is_uniq_sort_frist('Interview'))



if __name__ == '__main__':
    unittest.main()
