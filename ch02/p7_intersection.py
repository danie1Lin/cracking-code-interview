# by reference mean the intersaction first node's next will be the same too, so we can connect them together if it is circular.
# better: first you can move forward the longer list
# best: look at the last node it must be same
# so ask first: 
# the two list are not circular? if not, we can use this way. It's time is O(n).
# If it is, it have to compare to each other.
import unittest
class LinkedNode:
    def __init__(self, value, next=None) -> None:
        self.value = value
        self.next = next
    def __repr__(self):
        return f'Node[{self.value}]'

def is_intersacting(root1, root2) -> LinkedNode:
    l1, l2 = 1, 1 
    c1, c2 = root1, root2
    while c1.next:
        l1 += 1
        c1 = c1.next
    while c2.next:
        l2 += 1 
        c2 = c2.next
    if c1 != c2:
        return None
    if l1 < l2:
        l1, l2 = l2, l1
        root1, root2 = root2, root1
    for _i in range(l1 - l2):
        root1 = root1.next
    for i in range(l2):
        if root1 == root2:
            return root1
        root1 = root1.next
        root2 = root2.next
    return None


class TestIsIntersecting(unittest.TestCase):
    def test(self):
        intersected = LinkedNode('B', LinkedNode('A', LinkedNode('C')))
        l1 = LinkedNode('C', intersected)
        l2 = LinkedNode('F', LinkedNode('G', intersected))
        self.assertIs(is_intersacting(l1, l2), intersected)

if __name__ == '__main__':
    unittest.main()
