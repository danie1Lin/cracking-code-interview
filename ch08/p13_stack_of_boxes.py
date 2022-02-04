from dataclasses import dataclass
from functools import reduce
from operator import attrgetter
import pytest


@dataclass
class Box:
    w: int
    h: int
    d: int

    def __gt__(self, other):
        return self.__class__ == other.__class__ and self.w > other.w and self.h > other.h and self.d > other.d

# s(n) =
# s(n-1) + n
# 找到比 n 大的
# if 找到可以放的位置
# if 找不到: 抽換掉不合規的箱子
# 與 n 做交換看有沒有比原本高


def max_hight_of_stack(boxes: list[Box]) -> int:
    boxes = sorted(boxes, key=attrgetter('h', 'w', 'd'), reverse=True)
    print(boxes)
    # box should larger than below
    return reduce(lambda acc, x: acc + boxes[x].h,
                  max_hight_permutation(boxes, len(boxes) - 1), 0)


def max_hight_permutation(boxes: list[Box], can_picked_before: int) -> list[int]:
    if can_picked_before == 0:
        return [can_picked_before]
    picked = max_hight_permutation(boxes, can_picked_before - 1)
    box = boxes[can_picked_before]
    bigger_idx_in_stack = -1
    for idx, picked_idx in enumerate(reversed(picked)):
        if boxes[picked_idx] > box:
            bigger_idx_in_stack = idx
    if bigger_idx_in_stack == -1:
        return picked

    h = reduce(lambda acc, x: acc +
               boxes[x].h, picked[bigger_idx_in_stack+1:], 0)
    if box.h > h:
        picked = picked[:bigger_idx_in_stack] + [can_picked_before]
    return picked


def test():
    boxes = [Box(3, 3, 3), Box(4, 4, 4), Box(2, 8, 1)]
    assert 8 == max_hight_of_stack(boxes)
    boxes = [Box(3, 3, 3), Box(4, 4, 4), Box(1, 3, 1), Box(2, 5, 2)]
    assert 8 == max_hight_of_stack(boxes)
