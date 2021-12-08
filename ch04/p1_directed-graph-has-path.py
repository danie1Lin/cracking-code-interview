from collections import deque
from .graph import *
from ch03.stack import Stack
import unittest

# ask:
# 1. will the graph have loop? ~first assume not~ usually yes
# 2. Is the node unique?

def has_path_v1(graph, a, b) -> bool:
    points = [a, b]
    path = []
    start = False
    root = None
    for n in g.nodes:
        root = n
        for target in points:
            if target == n:
                path.append(target)
                points.remove(target)
                break
    return False


class TestHasPathV1(unittest.TestCase):
    """
    use Graph class to represent graph in python is not quite convenient
    we can try use map[node][node] to represent
    """
    def xtest_has_path_v1(self):
        """
        this graph is not setup right
        Graph nodes should have all nodes, you can found the neighbors only access first layer
        """
        node1 = GraphNode(0)
        node1.children = [GraphNode(x) for x in range(1, 11)]
        node1.children[3].children = [GraphNode(x) for x in range(11, 21)] 
        node1.children[3].children[3].children = [GraphNode(x) for x in range(21, 31)] 

        node2 = GraphNode(200)
        node2.children = [GraphNode(x) for x in range(201, 211)]
        node2.children[3].children = [GraphNode(x) for x in range(211, 221)] 
        node2.children[3].children[3].children = [GraphNode(x, ) for x in range(221, 231)] 


        assert not has_path_v1(g, 221, 231)
        assert not has_path_v1(g, 11, 231)
        assert has_path_v1(g, 200, 231)


# DFS
def has_path(graph, start, end, visited = None) -> bool:
    if not visited: visited = set()
    if start in visited:
        return False
    visited.add(start)
    for node in graph[start]:
        if node == end or has_path(graph, node, end, visited):
            return True
    return False


# BFS
def has_path_bfs(graph, start, end) -> bool:
    q = deque(start)
    visited = set()
    while not len(q) == 0:
        node = q.popleft()
        if node in visited:
            continue
        visited.add(node)
        if node == end:
            return True
        for child in graph[node]:
            q.append(child)
    return False

class TestHasPath(unittest.TestCase):
    # test case from: https://github.com/careercup/CtCI-6th-Edition-Python/blob/master/chapter_04/p01_route_between_nodes.py
    graph = {
        "A": ["B", "C"],
        "B": ["D"],
        "C": ["D", "E"],
        "D": ["B", "C"],
        "E": ["C", "F"],
        "F": ["E", "O", "I", "G"],
        "G": ["F", "H"],
        "H": ["G"],
        "I": ["F", "J"],
        "O": ["F"],
        "J": ["K", "L", "I"],
        "K": ["J"],
        "L": ["J"],
        "P": ["Q", "R"],
        "Q": ["P", "R"],
        "R": ["P", "Q"],
    }

    tests = [
        ("A", "L", True),
        ("A", "B", True),
        ("H", "K", True),
        ("L", "D", True),
        ("P", "Q", True),
        ("Q", "P", True),
        ("Q", "G", False),
        ("R", "A", False),
        ("P", "B", False),
    ]

    def test_has_path(self):
        for test in self.tests:
            assert test[2] == has_path(self.graph, test[0], test[1]), f'{test}'

    def test_has_path_bfs(self):
        for test in self.tests:
            assert test[2] == has_path_bfs(self.graph, test[0], test[1]), f'{test}'



if __name__ == '__main__':
    unittest.main()
