from typing import Deque, Optional

from .tree import BinaryTreeNode

from .p2_minimum_height_binary_search_tree import build_minimum_tree

import unittest

def is_searching_binary_tree(root: Optional[BinaryTreeNode], bottom=float('-inf'), top=float('inf')) -> bool:
    if not root:
        return True
    medium = root.value
    if medium <= bottom or medium > top: # >= or > , discuss with your interviewer
        return False
    # 越往下且越靠中間的節點，區間限縮越多
    #           5
    #        /     \
    #      3         7
    #    /   \
    #  1      ^只能 3 ～ 5 之間    
    return is_searching_binary_tree(root.left, bottom, medium) and is_searching_binary_tree(root.right, medium, top)

class TestIsBalance(unittest.TestCase):
    def test_is_balance(self):
        tree = build_minimum_tree(list(range(15)))
        assert is_searching_binary_tree(tree)

    def test_is_not_balance(self):
        tree = build_minimum_tree(list(range(15)))
        node = tree
        while node.left:
            node = node.left
        node.left = BinaryTreeNode(18)
        assert not is_searching_binary_tree(tree)

if __name__ == '__main__':
    unittest.main()
