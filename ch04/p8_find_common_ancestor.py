from typing import NamedTuple, Optional
import unittest
from ch04.p2_minimum_height_binary_search_tree import build_minimum_tree
from ch04.p6_find_next_node_of_tree import BinaryTreeNodeWithParent
from ch04.tree import BinaryTreeNode
# noted:
# 1. can not use other space
# 2. the tree is not necessary searching tree or any rule

# solution：
# 1. 可以用記錄 parent 的話

# Tips:
# 如果深度不同其中一個上移就好


# TODO:
# 用 stack 回傳的到底是算不算用額外空間？ 會問這個問題應該是方向搞錯了

def find_common_ancestor(root: Optional[BinaryTreeNode], nodeA: int, nodeB: int) -> Optional[BinaryTreeNode]:
    res = ancestor(root, nodeA, nodeB)
    if res.is_common:
        return res.node
    return None
    
class Result(NamedTuple):
    node: Optional[BinaryTreeNode]
    is_common: bool

def ancestor(root: Optional[BinaryTreeNode], nodeA, nodeB) -> Result:
    if not root:
        return Result(None, False)
    if root == nodeA and root == nodeB:
        return Result(root, True)
    '''
    #TODO: 這個為何不能放？
    要跟子樹的狀況做比較，不能單看 root == nodeA/B
    elif root == nodeA:
        return Result(root, False)
    elif root == nodeB:
        return Result(root, False)
    '''
    left_result = ancestor(root.left, nodeA, nodeB)
    if left_result.is_common:
        return left_result
    
    right_result = ancestor(root.right, nodeA, nodeB)
    if right_result.is_common:
        return right_result

    if left_result.node and right_result.node:
        return Result(root, True)
    elif root == nodeA or root == nodeB:
        # nodeA 是 root 且 B 在 root 的子樹中
        is_ancestor = not not left_result.node or not not right_result.node 
        return Result(root, is_ancestor)
    # 如果子樹有找到，往上提到 root
    elif left_result.node or right_result.node: 
        return Result(root, False)
    else:
        return Result(None, False)


# 用提升的方式會變得簡單許多
def find_common_ancestor_with_parent(root: Optional[BinaryTreeNodeWithParent], nodeA, nodeB) -> Optional[BinaryTreeNodeWithParent]:

    nodeA = root.find(nodeA)
    nodeB = root.find(nodeB)
    if not nodeA or not nodeB:
        return None

    nodeADeep = nodeA.deep()
    nodeBDeep = nodeB.deep()
    if nodeADeep > nodeBDeep:
        nodeA = nodeA.go_up(nodeADeep - nodeBDeep)
    else:
        nodeB = nodeB.go_up(nodeBDeep - nodeADeep)
    # 這邊容易忘記檢查
    if nodeA == nodeB:
        return nodeA
    for i in range(min(nodeADeep, nodeBDeep)):
        nodeA = nodeA.go_up(1)
        nodeB = nodeB.go_up(1)
        if nodeA == nodeB:
            return nodeA

class TestFindCommonAncestor(unittest.TestCase):
    test_cases = [
        dict(
            root=list(range(15)),
            a=0,
            b=14,
            ancestor=7,
        ),
        dict(
            root=list(range(15)),
            a=1,
            b=6,
            ancestor=3,
        ),
        dict(
            root=list(range(15)),
            a=3,
            b=6,
            ancestor=3,
        ),
    ]
    def test_find_common_ancestor(self):
        for test_case in self.test_cases:
            node = find_common_ancestor(BinaryTreeNode.build_minimum_searching_tree(test_case['root']), test_case['a'], test_case['b'])
            self.assertIsNotNone(node, test_case)
            if node:
                self.assertIs(
                    node.value,
                    test_case['ancestor']
                )
    def test_find_common_ancestor_with_parent(self):
        for test_case in self.test_cases:
            node = find_common_ancestor_with_parent(BinaryTreeNodeWithParent.build_minimum_searching_tree(test_case['root']), test_case['a'], test_case['b'])
            self.assertIsNotNone(node, test_case)
            if node:
                self.assertIs(
                    node.value,
                    test_case['ancestor']
                )


if __name__ == '__main__':
    unittest.main()
