from typing import Any, Deque, Generic, Optional, TypeVar
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

    def __eq__(self, __o: object) -> bool:
       return self.value == __o or (hasattr(__o, 'value') and __o.value == self.value)

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

    def set_left(self, node: Optional[Any]) -> None:
        self.left = node

    def set_right(self, node: Optional[Any]) -> None:
        self.right = node

    def find(self, value):
        if self.value == value:
            return self
        if self.left:
            node = self.left.find(value)
            if node:
                return node
        if self.right:
            node = self.right.find(value)
            if node:
                return node

    def __repr__(self) -> str:
        max_layer = self.max_layer()
        max_value = self.max()
        value_width = int(math.log10(max_value)) + 1 + 2
        line_width = (2 ** (max_layer + 1)) * value_width - 1
        queue = Deque()
        queue.appendleft((self, 0, int(line_width / 2) + 1, line_width - 1))
        lines = [" " * line_width] * (max_layer + 1) * 2
        while len(queue) != 0:
            node, line_num, pos, value_width = queue.pop()
            if not node:
                # TODO： 印出N
                continue
            else:
                s = str(node.value) 
            line = lines[line_num]
            lines[line_num] = line[:pos] + s + line[pos + len(s):]
            next_line = lines[line_num + 1]
            # TODO: 可以算要加多少層連接
            lines[line_num+1]= next_line[:pos - 1] + "/" + next_line[pos:pos+len(s)] + "\\" + next_line[pos+len(s)+1:]
            if node:
                width = int(value_width / 2) 
                queue.append((node.left, line_num + 2, pos - int(width/2), width))
                queue.append((node.right, line_num + 2, pos + int(width/2), width))
        lines.insert(0, f"{self.__class__}")
        return "\n".join(lines)


    def max(self):
        maximum = float('-inf')
        for i in self.pre_order():
            if not i:
                continue
            maximum = max(i, maximum)
        return maximum

    def max_layer(self):
        layer = 1 
        if self.left:
            layer = max(layer, self.left.max_layer() + 1)
        if self.right:
            layer = max(layer, self.right.max_layer() + 1)
        return layer

    @classmethod
    def build_minimum_searching_tree(cls, arr: list):
        if len(arr) == 0:
            return None
        mid = int(len(arr) / 2)
        root = cls(arr[mid])
        if len(arr) == 1:
            return root
        root.set_left(cls.build_minimum_searching_tree(arr[0:mid]))
        root.set_right(cls.build_minimum_searching_tree(arr[mid+1:]))
        return root


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

    print(root)
