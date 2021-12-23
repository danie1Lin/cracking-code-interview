import unittest

def is_rotation(s1: str, s2: str) -> bool:
    if len(s1) != len(s2):
        return False
    start_idx = -1
    for i in range(len(s2)):
        if is_substring(s1, s2[i:]):
            start_idx = i
            break

    if start_idx >= 0:
        return is_substring(s1, s2[:start_idx])
    return False
    
def is_rotation_simpler(s1: str, s2: str) -> bool:
    if len(s1) != len(s2):
        return False

    # brilliant! concat s1 twice
    return is_substring(s1 + s1, s2)

def is_substring(s1: str, s2: str):
    return s2 in s1

def is_rotation_without_is_substring(s1: str, s2: str) -> bool:
    if len(s1) != len(s2):
        return False
    curr1, curr2 = 0, 0
    start = False
    while curr1 < len(s1) and curr2 < 2 * len(s2):
        if s1[curr1] != s2[curr2 % len(s2)]:
            # reset
            start = False
            curr1 = 0
        else:
            start = True
            curr1 += 1
        curr2 += 1
    return start


class TestIsSubstring(unittest.TestCase):
    def test_simpler(self):
        self.assertTrue(is_rotation_simpler("waterbottle", "erbottlewat"))
        self.assertTrue(is_rotation_simpler("waterbottle", "bottlewater"))
        self.assertTrue(is_rotation_simpler("wa", "aw"))
        self.assertTrue(is_rotation_simpler("w", "w"))
        self.assertFalse(is_rotation_simpler("abc", "bcad"))
        self.assertFalse(is_rotation_simpler("abc", "bcd"))

    def test(self):
        self.assertTrue(is_rotation("waterbottle", "erbottlewat"))
        self.assertTrue(is_rotation("waterbottle", "bottlewater"))
        self.assertTrue(is_rotation("wa", "aw"))
        self.assertTrue(is_rotation("w", "w"))
        self.assertFalse(is_rotation("abc", "bcad"))
        self.assertFalse(is_rotation("abc", "bcd"))

    def test_without_is_substring(self):
        self.assertTrue(is_rotation_without_is_substring("waterbottle", "erbottlewat"))
        self.assertTrue(is_rotation_without_is_substring("waterbottle", "bottlewater"))
        self.assertTrue(is_rotation_without_is_substring("wa", "aw"))
        self.assertTrue(is_rotation_without_is_substring("w", "w"))
        self.assertFalse(is_rotation_without_is_substring("abc", "bcad"))
        self.assertFalse(is_rotation_without_is_substring("abc", "bcd"))


if __name__ == '__main__':
    unittest.main()
