from typing import Optional
import unittest
from .tree import BinaryTreeNode
from itertools import chain
import copy
# idea:
# the same layer node maybe unordered.
def bst_sequence(root: Optional[BinaryTreeNode]) -> list[list[int]]:
    if not root:
        return []
    left_seqs = bst_sequence(root.left) or [[]]
    right_seqs = bst_sequence(root.right) or [[]] # 如果沒有，下面的 for 就不會跑了
    # 只要 left 維持順序 right 維持順序就好
    result = []
    for a in left_seqs:
        for b in right_seqs:
             result.extend(merge(a, b, []))
    print(result)
    if not result:
        result = [[]]
    for s in result:
        s.insert(0, root.value)
    return result


def merge(a: list[int], b: list[int], prefix: list[int]):
    if len(a) == 0 and len(b) == 0:
        return [prefix]
    combs = []
    if len(a) > 0:
        p = prefix.copy()
        p.append(a[0])
        combs.extend(merge(a[1:], b, p))

    if len(b) > 0:
        p = prefix.copy()
        p.append(b[0])
        combs.extend(merge(a, b[1:], p))
    return combs
    


class TestBstSequence(unittest.TestCase):
    test_cases = [ 
            {
                'list': list(range(1, 4)),
                'expect': [[2,1,3], [2,3,1]] 
            },
            {
                'list': list(range(1, 8)),
                'expect': [
                    [4, 2, 6, 1, 3, 5, 7],
                    [4, 2, 1, 6, 3, 5, 7],
                    [4, 2, 1, 3, 6, 5, 7],
                    [4, 6, 2, 1, 3, 5, 7],
                    [4, 6, 2, 1, 5, 3, 7],
                    [4, 6, 2, 5, 1, 3, 7],
                    [4, 6, 5, 2, 1, 3, 7],
                    [4, 6, 5, 2, 1, 7, 3],
                    [4, 6, 5, 2, 7, 1, 3],
                    [4, 6, 5, 7, 2, 1, 3],
                ], 
            },
            {
                'list': list(range(1, 7)),
                'expect': [
                    [4, 2, 6, 1, 3, 5],
                    [4, 6, 2, 1, 3, 5],
                ], 
            },
        ]
    def test_merge(self):
        expect = [
                [1,2,3,4],
                [1,3,2,4],
                [1,3,4,2],
                [3,1,2,4],
                [3,1,4,2],
                [3,4,1,2],
                ]

        result = merge([1,2], [3,4], [])
        for i in expect:
            self.assertIn(i, result)
    def test_bst_sequence(self):
        for test_case in self.test_cases:
            tree = BinaryTreeNode.build_minimum_searching_tree(test_case.get('list'))
            possible_seq = bst_sequence(tree)
            [self.assertIn(comb, possible_seq) for comb in test_case.get('expect')]

if __name__ == '__main__':
    unittest.main()

