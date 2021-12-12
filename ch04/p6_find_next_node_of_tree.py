from typing import Optional
import unittest
from .tree import BinaryTreeNode

# We can assume that node knows its parent
# We have two ways to find next(in order) of node in searching binary tree
# 1. transform the list, and found the node and its next
# 2. store parent on every node, so we can found the node if it has the leftest node of the right sub tree.

class BinaryTreeNodeWithParent(BinaryTreeNode):
    parent: BinaryTreeNode
    def __init__(self, value, left=None, right=None) -> None:
        self.parent = None
        super().__init__(value, left=left, right=right)

    def set_left(self, node: Optional[BinaryTreeNode]) -> None:
        if node:
            node.parent = self
        return super().set_left(node)

    def set_right(self, node: Optional[BinaryTreeNode]) -> None:
        if node:
            node.parent = self
        return super().set_right(node)
    
    def deep(self) -> int:
        deep = 0
        curr = self
        while curr.parent:
            curr = curr.parent
            deep += 1
        return deep

    def go_up(self, layer_num):
        curr = self
        for i in range(layer_num, 0,-1):
            if not curr:
                return None
            curr = curr.parent
        return curr


    def next_of(self, value):
        node = self.find(value)
        if not node:
            raise ValueError(f'node {value} not found')
        if node.right:
            tree = node.right
            while tree and tree.left:
                tree = tree.left
            return tree.value
        else:
            # 往上找到有右子樹且根不是自己
            tree = node
            while tree.parent: 
                if tree.parent.right == tree:
                    tree = tree.parent
                else:
                    return tree.parent.value
            return None #解決找不到右邊的樹，但是應該右更好的做法


class TestBuildMinimumTree(unittest.TestCase):
    def test_parent_is_right(self):
        node = BinaryTreeNodeWithParent.build_minimum_searching_tree(list(range(15)))
        for side in ['left', 'right']:
            while node.__getattribute__(side):
                assert node.__getattribute__(side).parent == node
                node = node.__getattribute__(side) 

    def test_next_of(self):
        tree = BinaryTreeNodeWithParent.build_minimum_searching_tree(list(range(15)))
        for i in range(13):
            self.assertIs(tree.next_of(i), i+1)
        self.assertIs(tree.next_of(14), None)
        with self.assertRaises(ValueError) as c:
            tree.next_of(15)

        self.assertTrue('node 15 not found' in str(c.exception)) # use str() or get TypeError
        




if __name__ == '__main__':
    unittest.main()

