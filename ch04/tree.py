from typing import Any, Generic, Optional, TypeVar
import math

"""
BinaryTree class is not necessary because binary tree has only one root.
class BinaryTree:
    root: BinaryTreeNode
"""

TBinaryTreeNode = TypeVar('TBinaryTreeNode', bound='BinaryTreeNode')
class BinaryTreeNode(Generic[TBinaryTreeNode]):
    value: Any
    left: Optional[TBinaryTreeNode]
    right: Optional[TBinaryTreeNode]

    def __init__(self, value, left = None, right = None) -> None:
        self.value = value
        self.left = left 
        self.right = right

    def in_order(self):
        if self.left:
            yield from self.left.in_order() 
        yield self.value
        if self.right:
            yield from self.right.in_order() 

    def post_order(self):
        if self.left:
            yield from self.left.post_order() 
        if self.right:
            yield from self.right.post_order() 
        yield self.value

    def pre_order(self):
        yield self.value
        if self.left:
            yield from self.left.pre_order() 
        if self.right:
            yield from self.right.pre_order() 


if __name__ == '__main__':
    nodes = []
    for i in range(16):
        nodes.append(BinaryTreeNode(i))

    i = 0
    while i * 2 + 2 < 16:
        nodes[i].left = nodes[i * 2 + 1]
        nodes[i].right = nodes[i * 2 + 2]
        i += 1
    
    root = nodes[0]
    for i in root.pre_order():
        print(f"{i} ", end='')

    print()
    for i in root.in_order():
        print(f"{i} ", end='')
    print()

    for i in root.post_order():
        print(f"{i} ", end='')
    print()

