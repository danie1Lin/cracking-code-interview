import unittest
from ch02.linked_list import LinkedNode


def partition(root: LinkedNode, v):
    curr = root
    large = None
    small = None
    while curr:
        if curr.value >= v:
            tmp = curr
            curr = tmp.next
            tmp.next = large
            large = tmp
        else:
            tmp = curr
            curr = tmp.next
            tmp.next = small
            small = tmp
    c = small
    while c.next:
        c = c.next
    c.next = large
    return small

class TestPartition(unittest.TestCase):
    def test(self):
        root = LinkedNode(3, LinkedNode(5, LinkedNode(8, LinkedNode(5, LinkedNode(10, LinkedNode(2, LinkedNode(1)))))))
        partition_result = partition(root, 5)
        print(partition_result)

if __name__ == '__main__':
    unittest.main()
