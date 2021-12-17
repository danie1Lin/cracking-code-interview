from typing import DefaultDict
import unittest


def check_palindrome_permutation(s: str) -> bool:
    s = s.lower()
    counts = DefaultDict(lambda: 0)
    len_without_space = 0
    for c in s:
        if c == " ":
            continue
        counts[c] += 1
        len_without_space += 1

    # only one word count can be odd when length except space is odd
    len_odd = len_without_space % 2 == 1
    found_odd = False
    for v in counts.values():
        if v % 2 == 1:
            if not len_odd:
                return False
            if found_odd:
                return False
            found_odd = True
    return True



class TestCheckPalindromePermutation(unittest.TestCase):
    def test(self):
        self.assertTrue(check_palindrome_permutation("Tact Coa"))

if __name__ == '__main__':
    unittest.main()
