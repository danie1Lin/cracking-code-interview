from typing import Optional, Tuple
from ch02.linked_list import LinkedNode
import unittest

def sum_list_backward(l1: LinkedNode, l2: LinkedNode) -> LinkedNode:
    sum_root_gaurd = LinkedNode(None)
    sum_curr = sum_root_gaurd
    carry = 0
    while l1 or l2:
        sum_value = 0
        if l1:
            sum_value += l1.value
            l1 = l1.next
        if l2:
            sum_value += l2.value
            l2 = l2.next
        sum_value += carry
        carry = int(sum_value / 10)
        sum_value %= 10
        sum_curr.next = LinkedNode(sum_value)
        sum_curr = sum_curr.next
    return sum_root_gaurd.next

def sum_list_forward(l1: LinkedNode, l2: LinkedNode, carry=0) -> Optional[LinkedNode]:
    root, carry = sum_list_forward_with_carry(l1, l2)
    if carry != 0:
        root = LinkedNode(carry, root)
    return root

def sum_list_forward_with_carry(l1, l2) -> Tuple[Optional[LinkedNode], int]:
    if not l1 and not l2:
        return None, 0
    sum_value = 0
    if l1:
        sum_value += l1.value
        l1 = l1.next
    if l2:
        sum_value += l2.value
        l2 = l2.next
    next_node_result = sum_list_forward_with_carry(l1, l2)
    next_node, carry = next_node_result[0], next_node_result[1]
    sum_value += carry
    carry = int(sum_value / 10)
    sum_value %= 10
    return LinkedNode(sum_value, next_node), carry


class TestSumList(unittest.TestCase):
    def test_sum_list(self):
        self.assertEqual(sum_list_backward(LinkedNode(7, LinkedNode(1, LinkedNode(6))), LinkedNode(5, LinkedNode(9, LinkedNode(2)))), LinkedNode(2, LinkedNode(1, LinkedNode(9))))

    def test_sum_list_forward(self):
        self.assertEqual(sum_list_forward(LinkedNode(6, LinkedNode(1, LinkedNode(7))), LinkedNode(2, LinkedNode(9, LinkedNode(5)))), LinkedNode(9, LinkedNode(2, LinkedNode(1))))
        self.assertEqual(sum_list_forward(LinkedNode(1, LinkedNode(7)), LinkedNode(9, LinkedNode(5))), LinkedNode(1, LinkedNode(1, LinkedNode(2))))
        self.assertEqual(sum_list_forward(LinkedNode(1, LinkedNode(1, LinkedNode(7))), LinkedNode(9, LinkedNode(5))), LinkedNode(1, LinkedNode(2, LinkedNode(2))))


if __name__ == '__main__':
    unittest.main()
