import unittest

from ch02 import linked_list

class LinkedNode(linked_list.LinkedNode):
    # the Kth to the last means count from tail
    def kth_to_last(self, k: int):
        return self.kth_to_last_with_num(k)[0]

    def kth_to_last_with_num(self, k: int):
        if not self.next:
            return self, 1 
        else:
            result = self.next.kth_to_last_with_num(k)
            if result[1] == k:
                return result
            else:
                return self, result[1] + 1

    def kth_to_last_two_pointer(self, k: int):
        fore, knth = self, self
        for i in range(k): 
            if not fore.next:
                return None
            fore = fore.next
        # 0 ~ （k), 平移 x 到碰到尾
        # x - (k) ~  最後的後一個,  倒數 k 個
        while fore:
            fore = fore.next
            knth = knth.next
        return knth


class TestKthToLast(unittest.TestCase):
    def test(self):
        linked_list = LinkedNode(1, LinkedNode(2, LinkedNode(3, LinkedNode(4, LinkedNode(5, LinkedNode(6))))))
        self.assertEqual(linked_list.kth_to_last(1), LinkedNode(6))
        self.assertEqual(linked_list.kth_to_last(3), LinkedNode(4))

    def test_with_two_pointer(self):
        linked_list = LinkedNode(1, LinkedNode(2, LinkedNode(3, LinkedNode(4, LinkedNode(5, LinkedNode(6))))))
        self.assertEqual(linked_list.kth_to_last_two_pointer(1), LinkedNode(6))
        self.assertEqual(linked_list.kth_to_last_two_pointer(3), LinkedNode(4))


if __name__ == '__main__':
    unittest.main()


