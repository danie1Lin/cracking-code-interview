from typing import Deque, Optional, Tuple
import unittest
from ch02.linked_list import LinkedNode


def is_palindrome(node: LinkedNode):
    # queue = Deque()
    # 用 list 只要比對前面一半就好
    queue = []
    cursor = node
    while cursor:
        queue.append(cursor)
        cursor = cursor.next

    cursor = node
    i = len(queue) - 1 
    while i > len(queue) / 2:
        if cursor != queue[i]:
            return False
        cursor = cursor.next
        i -= 1
    return True

def is_palindrome_recursive(node: LinkedNode) -> bool:
    l = 0
    cursor = node
    while cursor:
        l += 1
        cursor = cursor.next
    result = is_palindrome_recursive_with(node, l)
    return result[1]

def is_palindrome_recursive_with(node: LinkedNode, length: int) -> Tuple[LinkedNode, bool]:
    if node == None:
        raise ValueError('node can not be None')
    if length == 0:
        return node, True
    if length == 1:
        return node.next, True

    result = is_palindrome_recursive_with(node.next, length - 2)
    if not result[1]:
        return None, False
    if result[0] and result[0].value == node.value:
        return result[0].next, True
    return None, False
    

class TestIsPalindrome(unittest.TestCase):
    test_cases = [
        {'node': LinkedNode('A', LinkedNode('B', LinkedNode('C', LinkedNode('B', LinkedNode('A'))))), 'expect': True},
        {'node': LinkedNode('A', LinkedNode('B', LinkedNode('C', LinkedNode('C', LinkedNode('B', LinkedNode('A')))))), 'expect': True},
        {'node': LinkedNode('A', LinkedNode('B', LinkedNode('C', LinkedNode('C', LinkedNode('A'))))), 'expect': False}
    ]

    def test(self):
        for test_case in self.test_cases:
            self.assertIs(is_palindrome(test_case['node']), test_case['expect']) 
    def test_recursive(self):
        for test_case in self.test_cases:
            self.assertIs(is_palindrome_recursive(test_case['node']), test_case['expect'], f"{test_case}") 

if __name__ == '__main__':
    unittest.main()

