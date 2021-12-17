# permutation means a different/same sequence of another sequence
import unittest

def check_permutation(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    word_set = set()
    for c in a:
        word_set.add(c)
    try:
        for c in b:
            word_set.remove(c)
    except KeyError:
        return False
    if len(word_set) != 0:
        return False
    return True


class TestCheckPermutation(unittest.TestCase):
    def test(self):
        self.assertTrue(check_permutation("1234", "4321"))
        self.assertFalse(check_permutation("1234", "5321"))
        self.assertFalse(check_permutation("1234", "321"))

if __name__ == '__main__':
    unittest.main()
