from typing import Deque, Optional, Tuple
from .tree import BinaryTreeNode
from .p2_minimum_height_binary_search_tree import build_minimum_tree
import unittest

def layer_list_of_tree(root: Optional[BinaryTreeNode]) -> list[list[int]]:
    q: Deque[Tuple[Optional[BinaryTreeNode], int]] = Deque()
    q.append((root, 0))
    result = []
    while len(q) != 0:
        node, layer = q.popleft()
        if node:
            if layer > len(result) - 1:
                for i in range(len(result)-1, layer+1):
                    result.append([])
            if not result[layer]:
                result[layer] = []
            result[layer].append(node.value)
        else:
            continue
        if node.left:
            q.append((node.left, layer + 1))
        if node.right:
            q.append((node.right, layer + 1))
    return result

# Noticed that list in python is mutable its id wil not change even after expanded.
# in other language like: 
# Java ArrayList
# Golang *[]T
def layer_list_of_tree_dfs(root: Optional[BinaryTreeNode], layer_list: list[list[int]], layer=0 ): 
    if not root:
        return [[]]
    if layer_list is None:
        raise ValueError('writable layer_list not given')
    while len(layer_list) <= layer:
        layer_list.append([])
    layer_list[layer].append(root.value)
    layer_list_of_tree_dfs(root.left, layer_list, layer + 1)
    layer_list_of_tree_dfs(root.right, layer_list, layer + 1)
    return layer_list
    

class TestLayerListOfTree(unittest.TestCase):
    def test_layer_list_of_tree(self):
        tree = build_minimum_tree(list(range(15)))
        li = layer_list_of_tree(tree)
        print(li)
    def test_layer_list_of_tree_bfs(self):
        tree = build_minimum_tree(list(range(15)))
        layer_list = []
        layer_list_of_tree_dfs(tree, layer_list)
        print(layer_list)
        assert layer_list == layer_list_of_tree(tree)

        
if __name__ == '__main__':
    unittest.main()
