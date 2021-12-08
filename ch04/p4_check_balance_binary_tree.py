from typing import Deque, Optional

from .tree import BinaryTreeNode

from .p2_minimum_height_binary_search_tree import build_minimum_tree

import unittest

def is_balance(root: Optional[BinaryTreeNode]) -> bool:
    if not root:
        return False # Determined by your interviewer
    minimum, maximum = float('inf') , -1
    queue = Deque()
    queue.append((root, 0))
    while len(queue) != 0:
        node, layer = queue.popleft()
        if layer > maximum:
            maximum = layer
        # TODO: check the priority of or and not
        # or is lower than and so need to 
        # not x is higher than and
        # reference: https://docs.python.org/3/reference/expressions.html#operator-precedence
        if (not node.left or not node.right) and minimum > layer:
            minimum = layer
        if node.left:
            queue.append((node.left, layer+1))
        if node.right:
            queue.append((node.right, layer+1))
    print(minimum, maximum)
    if minimum + 1 >= maximum:
        return True
    return False

class TestIsBalance(unittest.TestCase):
    def test_is_balance(self):
        tree = build_minimum_tree(list(range(15)))
        assert is_balance(tree)

    def test_is_not_balance(self):
        tree = build_minimum_tree(list(range(15)))
        node = tree
        while node.right:
            node = node.right
        node.right = BinaryTreeNode(18)
        node.right.right = BinaryTreeNode(20)
        assert not is_balance(tree)

if __name__ == '__main__':
    unittest.main()
