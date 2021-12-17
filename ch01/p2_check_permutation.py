# permutation means a different/same sequence of another sequence
from typing import DefaultDict
import unittest

# should ask interviewer:
# 1. does space count in?
# 2. does different cases means different? like: God and dog

def check_permutation(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    # should not use set, because words can be duplicated.
    word_set = DefaultDict(lambda: 0)
    for c in a:
        word_set[c] += 1

    for c in b:
        word_set[c] -= 1

    for count in word_set.values():
        if count != 0:
            return False
    return True


class TestCheckPermutation(unittest.TestCase):
    def test(self):
        self.assertTrue(check_permutation("1234", "4321"))
        self.assertTrue(check_permutation("11234", "43211"))
        self.assertFalse(check_permutation("1234", "5321"))
        self.assertFalse(check_permutation("1234", "321"))

if __name__ == '__main__':
    unittest.main()
