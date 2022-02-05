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
    boxes = sorted(boxes, key=attrgetter('w', 'd', 'h'), reverse=True)
    max_height_till_idx = [0] * len(boxes)
    max_height_till_idx[0] = boxes[0].h
    for idx in range(1, len(boxes)):
        max_height_till_idx[idx] = max_height_till_idx[idx-1] + boxes[idx].h

    dp = [[False] * (max_height_till_idx[-1] + 1) for _ in range(len(boxes))]
    for idx, box in enumerate(boxes):
        dp[idx][box.h] = True

    for idx in range(1, len(boxes)):
        box = boxes[idx]
        for last_boxes_idx_of_stack in range(idx):
            for height in range(max_height_till_idx[idx]+1):
                if dp[last_boxes_idx_of_stack][height] and boxes[last_boxes_idx_of_stack] > box:
                    dp[idx][height+box.h] = True
    max_height = 0
    for row in dp:
        for height, existed in enumerate(row):
            if existed and height > max_height:
                max_height = height
    return max_height


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
    boxes = [Box(6, 4, 4), Box(8, 6, 2), Box(5, 3, 3),
             Box(7, 8, 3), Box(4, 2, 2), Box(9, 7, 3)]
    assert 13 == max_hight_of_stack(boxes)
    boxes = [Box(30,14,70), Box(8,30,45), Box(0,34,29), Box(30,30,91), Box(53,95,78), Box(84,68,0), Box(48,81,28), Box(92,17,8), Box(95,1,2), Box(67,72,47), Box(93,7,69), Box(30,98,37), Box(92,89,7), Box(29,37,87), Box(43,93,34), Box(57,10,41), Box(77,5,22), Box(8,34,54), Box(63,45,63), Box(29,27,85), Box(72,11,76), Box(1,95,27), Box(8,47,51), Box(39,39,2), Box(59,68,83), Box(79,45,81), Box(19,52,58), Box(75,32,93), Box(22,1,1), Box(24,76,90), Box(37,26,1), Box(84,44,82), Box(78,55,90), Box(49,60,4), Box(47,60,15), Box(37,1,37), Box(90,7,7), Box(69,29,44), Box(91,2,40), Box(5,15,59), Box(13,52,35), Box(98,93,38), Box(76,70,25), Box(23,18,32), Box(60,11,2), Box(26,80,16), Box(0,7,91), Box(87,1,85), Box(95,52,13), Box(58,40,31), Box(82,24,27), Box(27,94,11), Box(66,43,51), Box(67,96,28), Box(99,40,35), Box(48,0,32), Box(78,65,28), Box(88,26,29), Box(26,90,24), Box(34,40,21), Box(75,30,81), Box(65,16,76), Box(63,45,91), Box(63,1,6), Box(84,39,91), Box(64,25,50), Box(35,49,13), Box(4,36,46), Box(12,66,64), Box(66,82,76), Box(83,24,43), Box(44,55,6), Box(69,49,52), Box(93,35,36), Box(52,51,29), Box(49,0,33), Box(81,5,95), Box(40,7,58), Box(1,87,44), Box(41,59,53), Box(37,26,10), Box(92,90,52), Box(85,86,26), Box(95,45,55), Box(41,19,63), Box(50,39,59), Box(65,22,77), Box(14,98,21), Box(52,45,84), Box(93,96,35), Box(64,90,79), Box(15,1,9), Box(18,3,45), Box(78,24,22), Box(0,1,86), Box(60,44,2), Box(88,35,66), Box(42,93,8), Box(79,59,88), Box(87,10,44), Box(61,22,14), Box(4,14,39), Box(29,15,90), Box(35,79,39), Box(52,73,83), Box(61,2,94), Box(45,90,46), Box(86,10,9), Box(46,13,99), Box(45,16,37), Box(17,56,42), Box(64,76,5), Box(93,80,67), Box(83,1,1), Box(11,55,80), Box(61,82,65), Box(5,21,40), Box(8,77,66), Box(98,23,76), Box(82,30,6), Box(89,53,15), Box(24,87,54), Box(29,93,98), Box(76,19,68), Box(59,17,60), Box(6,57,24), Box(85,94,97), Box(27,26,54), Box(24,56,85), Box(81,20,21), Box(47,64,95), Box(80,29,80), Box(21,55,88), Box(52,80,85), Box(82,87,61), Box(32,85,32), Box(74,55,88), Box(31,56,8), Box(2,20,72), Box(37,97,22), Box(40,48,74), Box(10,78,85), Box(70,46,77), Box(95,29,80), Box(85,65,21), Box(91,84,94), Box(65,80,55), Box(95,13,67), Box(79,4,56), Box(30,11,38), Box(98,31,33), Box(94,12,95), Box(32,66,29), Box(94,81,31), Box(4,43,92), Box(35,60,88), Box(11,73,50), Box(47,7,79), Box(77,79,47), Box(16,19,94), Box(53,88,10), Box(49,72,72), Box(76,52,88), Box(81,17,32), Box(11,64,97), Box(10,73,78), Box(84,33,43), Box(2,5,39), Box(83,96,0), Box(4,28,47), Box(26,82,82), Box(20,76,98), Box(5,2,21), Box(67,23,51), Box(64,95,11), Box(92,23,4), Box(83,48,78), Box(70,8,89), Box(24,29,99), Box(35,10,1), Box(74,71,34), Box(75,90,76), Box(35,75,78), Box(6,38,74), Box(83,95,37), Box(90,14,48), Box(14,39,62), Box(6,9,47), Box(76,49,79), Box(48,48,57), Box(91,27,70), Box(49,0,36), Box(5,80,46), Box(53,34,18), Box(63,19,56), Box(86,9,77), Box(11,61,64), Box(80,2,70), Box(4,52,4), Box(31,31,68)] 
    assert 527 == max_hight_of_stack(boxes)
