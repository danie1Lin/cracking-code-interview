from typing import Any, Sequence, TypeVar, Generic, Type
from itertools import accumulate

TNode = TypeVar('TNode', bound="GraphNode")
TValue = TypeVar('TValue')

class GraphNode(Generic[TNode, TValue]):
    children: Sequence[TNode]
    parent: TNode
    value: Any
    def __init__(self, value, parent = None) -> None:
        self.value = value
        self.children = []
        self.parent = parent

    def post_order(self):
        for child in self.children:
            yield from child.post_order()
        yield self.value

    def pre_order(self):
        yield self.value
        for child in self.children:
            yield from child.pre_order()

class Graph(Generic[TNode]):
    nodes: Sequence[TNode]
    def __init__(self):
        self.nodes = []

    def post_order(self):
        for node in self.nodes:
            yield from node.post_order() # 將工作交給另一個 iterator

    def pre_order(self):
        for node in self.nodes:
            yield from node.pre_order()


if __name__ == '__main__':
    nodes = []
    for i in range(16):
        nodes.append(GraphNode(i))
    
    nodes[0].children = nodes[1:3]
    nodes[3].children = nodes[4:9]
    nodes[9].children = nodes[10:16]

    g = Graph()
    # FIXME: graph setup wrong, graph.nodes should have all nodes
    g.nodes = list(map(nodes.__getitem__, [0, 3, 9])) # 外層要用 list 包起來

    for n in g.pre_order():
        print(n)

    for n in g.post_order():
        print(n)
