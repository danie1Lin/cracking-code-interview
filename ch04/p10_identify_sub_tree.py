# 有可能會有重複值
# 
#   2       1
# 1   3        2
#                 3
# 中序分別是 1 2 3 & 1 2 3
# 前序是 2 1 3 & 1 2 3
#   2         2
# 1   3     1
#             3
# 這樣前序也是一樣
# 
# 將 n 當作
#      2
#   1     3
# n  n   n  n

import unittest
from .tree import BinaryTreeNode

class Node(BinaryTreeNode):
    def pre_order(self, end_node=False):
        yield self.value
        if self.left:
            yield from self.left.pre_order(end_node) 
        elif end_node:
            yield None
        if self.right:
            yield from self.right.pre_order(end_node) 
        elif end_node:
            yield None


    def is_sub_tree(self, sub_tree) -> bool:
        sub_tree_list = list(sub_tree.pre_order(True))
        cursor = 0
        for node_value in self.pre_order(True):
            if node_value == sub_tree_list[cursor]:
                cursor += 1
            else:
                cursor = 0
            """
            很容易寫在最前面而產生錯誤，因為有可能剛好for 結束沒有檢查到下一次
            """
            if cursor >= len(sub_tree_list):
                return True

        return False

class TestIdentifySubTree(unittest.TestCase):
    def test(self):
        treeA = Node(10, Node(2, Node(1), Node(3)), Node(2, Node(11), Node(12)))
        print(treeA)
        self.assertIsSubTree(treeA, Node(2, Node(1), Node(3)))
        self.assertIsSubTree(treeA, Node(1))
        self.assertIsSubTree(treeA, Node(2, Node(11), Node(12)))
        self.assertIsNotSubTree(treeA, Node(1, right=Node(2, right=Node(3))))
        self.assertIsNotSubTree(treeA, Node(2, left=Node(1, right=Node(3))))
    def assertIsSubTree(self, treeA, treeB):
        return self.assertTrue(treeA.is_sub_tree(treeB), f"{treeB}\nnot subtree of:\n{treeA}")

    def assertIsNotSubTree(self, treeA, treeB):
        return self.assertFalse(treeA.is_sub_tree(treeB), f"{treeB}\nis subtree of:\n{treeA}")


if __name__ == '__main__':
    unittest.main()

