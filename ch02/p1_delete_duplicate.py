import unittest

def delete_dup(l: list[int]):
    for i in range(len(l)):
        if i + 1 >= len(l):
            break
        # TIPS:
        # 從後面刪回來，可以避免刪除後元素平移
        for j in range(len(l) - 1, i, -1):
            if l[i] == l[j]:
                l = l[:j] + l[j + 1:]
    return l

class TestDeleteDuplicat(unittest.TestCase):
    def test(self):
        l = [4, 2, 1, 1,4, 5, 3, 4, 5]
        uniq_l = delete_dup(l)
        self.assertListEqual(uniq_l, [4,2, 1, 5, 3])

if __name__ == '__main__':
    unittest.main()
