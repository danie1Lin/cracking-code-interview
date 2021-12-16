from collections import defaultdict
from typing import Optional
import unittest
from .tree import BinaryTreeNode

# I misunderstand the problem totally
# def sum_path_v1(root: Optional[BinaryTreeNode], start: int, end: int) -> int:
    # if not root:
        # raise ValueError
    # node = root.find(start)
    # return sum_from_v1(node, end)
    
# def sum_from_v1(node: Optional[BinaryTreeNode], end: int) -> int:
    # if not node:
        # raise ValueError
    # total = node.value
    # if end == node.value:
        # return total
    # left, right = False, False
    # if node.left:
        # try:
            # total += sum_from_v1(node.left, end)
            # left = True
        # except ValueError:
            # pass
    # if node.right:
        # try:
            # total += sum_from_v1(node.right, end)
            # right = True
        # except ValueError:
            # pass
    # if left or right:
        # return total
    # else:
        # raise ValueError


# class TestPathWithSum(unittest.TestCase):
    # def test_sum_path(self):
        # tree = BinaryTreeNode.build_minimum_searching_tree(range(15))
        # print(tree)
        # self.assertIs(sum_path_v1(tree, 3, 2), sum([3, 1, 2]))
        # self.assertIs(sum_path_v1(tree, 7, 10), sum([7, 11, 9, 10]))
        # with self.assertRaises(ValueError):
            # sum_path_v1(tree, 9, 14)

def path_count(tree: Optional[BinaryTreeNode], target) -> int:
    if not tree:
        return 0
    # sub question:
    # start from the root
    # not start the root
    count = 0
    # 開始
    count += paths_start_from(tree, target)
    # 從下一個開始
    count += path_count(tree.left, target)
    count += path_count(tree.right, target)
    return count

def paths_start_from(node, target) -> int:
    if not node:
        return 0
    count = 0
    if node.value == target:
       count += 1 
    if node.left:
        count += paths_start_from(node.left, target - node.value)
    if node.right:
        count += paths_start_from(node.right, target - node.value)
    return count

def path_count_opt(tree: Optional[BinaryTreeNode], target: int, running_sum=0, cache=None) -> int:
    # cache 記錄了 累積加總 VS 總路經數 
    if cache is None:
        cache = defaultdict(lambda: 0)
    if not tree:
        return 0
    running_sum += tree.value
    # running_sum -> 從 root 到目前的加總
    # running_sum - running_sum_from_start = target
    running_sum_from_start = running_sum - target
    total_path_count = cache[running_sum_from_start]
    # 如果剛好從 root 到這個點
    if running_sum == target:
        total_path_count += 1
    cache[running_sum] += 1 # 這個總和的可能路徑多了一個可能
    total_path_count += path_count_opt(tree.left, target, running_sum, cache)
    total_path_count += path_count_opt(tree.right, target, running_sum, cache)
    cache[running_sum] -= 1 # 從其他支線是不可能到這裏的要拿掉
    return total_path_count


    
class TestPathWithSum(unittest.TestCase):
    def test_sum_path(self):
        tree = BinaryTreeNode(
                2, 
                BinaryTreeNode(4, BinaryTreeNode(-1, BinaryTreeNode(2), BinaryTreeNode(3, BinaryTreeNode(0))), BinaryTreeNode(5, BinaryTreeNode(-4, BinaryTreeNode(0, BinaryTreeNode(0)), BinaryTreeNode(0)), BinaryTreeNode(10))),
                BinaryTreeNode(6, BinaryTreeNode(7), BinaryTreeNode(-3)),
        )
        print(tree)
        self.assertIs(path_count(tree, 5), 8)
        self.assertIs(path_count_opt(tree, 5), 8)


if __name__ == '__main__':
    unittest.main()
