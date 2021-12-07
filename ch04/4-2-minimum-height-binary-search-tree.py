from .tree import *
import unittest


# 建立最小高度 -> 平衡的樹 -> 可以從中位數當跟節點



def BuildMinimumTree(arr: []) -> Optional[BinaryTreeNode]:
    if len(arr) == 0:
        return None
    mid = int(len(arr) / 2)
    root = BinaryTreeNode(arr[mid])
    if len(arr) == 1:
        return root
    root.left = BuildMinimumTree(arr[0:mid])
    root.right = BuildMinimumTree(arr[mid+1:])
    """
    python 的 range index 超過不會怎麼樣, 其他語言要注意一下
    >>> [0,1,2][4:]
    []
    """
    return root

class TestBuildMinimumTree(unittest.TestCase):
    TestCases = [
        list(range(10)),
        list(range(16)),
        list(range(17)),
    ]
    def test_build_minimum_tree(self):
        for case in self.TestCases:
            for i in BuildMinimumTree(case).in_order():
                print(f'{i} ', end='')
            print()


if __name__ == '__main__':
    unittest.main()
