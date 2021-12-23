import unittest
from ch02.p7_intersection import LinkedNode

# Derive
# number in loop is .y
# when slow_i at the begin of loop, which is postion x.
# fast_i = x + k
# 2x = x + k -> k = x
# now fast_i and slow_i distance is k in counter-clockwise, y - k in clockwise.
# so when slow_i moves y - k steps and fast_i moves 2 * (y - k) steps, they will meet.
# so meet at x + (y - k) postion then move k steps will arrive start of the loop again.
# k is x, so the from point they meet and the root move x steps will be the begin of the loop.

def begin_of_loop(node: LinkedNode) -> LinkedNode:
    # at least three edge form a loop
    if not node or not node.next or not node.next.next:
        return None
    slow = node.next
    fast = node.next.next
    meet = None
    while fast.next.next and slow.next:
        if slow == fast:
            meet = slow
            break
        slow = slow.next
        fast = fast.next.next
    if not meet:
        return None
    while meet != node:
        meet = meet.next
        node = node.next
    return node

class TestHasLoop(unittest.TestCase):
    def test(self):
        nodes = []
        for i in range(10):
            nodes.append(LinkedNode(i))
            nodes[i-1].next = nodes[i]
        for i in range(10):
            nodes[9].next = nodes[i]
            self.assertIs(begin_of_loop(nodes[0]), nodes[i])

if __name__ == '__main__':
    unittest.main()
