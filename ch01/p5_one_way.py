import unittest

def change_max_once(s1: str, s2: str) -> bool:
    changed = 0
    curr1, curr2 = 0, 0
    len_gap = 0
    while curr2 < len(s2) and curr1 < len(s1):
        if changed > 1:
            return False
        if s1[curr1] == s2[curr2]:
            curr1 += 1
            curr2 += 1
            continue
        else:
            changed += 1
            if len(s1) > curr1 + 1 and s1[curr1 + 1] == s2[curr2]:
                curr1 += 2
                curr2 += 1
                len_gap += 1
            elif len(s2) > curr2 + 1 and s1[curr1] == s2[curr2+1]:
                curr1 += 1 
                curr2 += 2 
                len_gap -= 1
            else:
                curr1 += 1
                curr2 += 1

    if changed > 1:
        return False
    # 剩下字數的差的如果和之前的 changed 加起來超過 1
    elif abs(len(s1) - 1 - curr1 - (len(s2) - 1 - curr2)) + changed > 1:
        return False
    return True


# 比較簡潔
def change_max_once_v2(s1: str, s2: str) -> bool:
    # 先檢查
    if abs(len(s1) -len(s2)) > 1:
        return False
    changed = 0
    curr1, curr2 = 0, 0
    len_gap = 0
    # 把長的放前面
    if len(s1) < len(s2):
        s2, s1 = s1, s2
    while curr2 < len(s2) and curr1 < len(s1):
        if changed > 1:
            return False
        if s1[curr1] == s2[curr2]:
            curr2 += 1
        else:
            changed += 1
            # 如果 s2 刪了一個字就不加短指針
            if len(s1) != len(s2):
                pass
            else:
                curr2 += 1
        curr1 += 1
    if changed > 1:
        return False
    return True

class TestChangeMaxOnce(unittest.TestCase):
    def test(self):
        self.assertTrue(change_max_once("pale", "ple"))
        self.assertTrue(change_max_once("pale", "pal"))
        self.assertFalse(change_max_once("pale", "pa"))
        self.assertFalse(change_max_once("a", "pale"))
        self.assertTrue(change_max_once("pales", "pale"))
        self.assertTrue(change_max_once("pale", "bale"))
        self.assertFalse(change_max_once("pale", "bake"))

    def test_v2(self):
        self.assertTrue(change_max_once_v2("pale", "ple"))
        self.assertTrue(change_max_once_v2("pale", "pal"))
        self.assertFalse(change_max_once_v2("pale", "pa"))
        self.assertFalse(change_max_once_v2("a", "pale"))
        self.assertTrue(change_max_once_v2("pales", "pale"))
        self.assertTrue(change_max_once_v2("pale", "bale"))
        self.assertFalse(change_max_once_v2("pale", "bake"))

if __name__ == '__main__':
    unittest.main()
