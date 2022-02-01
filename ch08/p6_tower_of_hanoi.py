from functools import reduce
from time import sleep, time
from typing import Deque
import pytest

class Hanoi:
    def __init__(self, n: int) -> None:
        self._max = n
        self.towers = [Deque() for _ in range(3)]
        for i in range(n, 0, -1):
            self.towers[0].append(i)

    def __str__(self) -> str:
        length_unit = 4 
        tower_width = length_unit * (self._max) + 1 + 8
        interval = 1
        pillar_height = self._max + 1 
        lines = [""] * pillar_height
        left_edge = "_|"
        right_edge = "|_"
        for tower_idx, tower in enumerate(self.towers):
            offset = tower_idx * tower_width
            for layer in range(pillar_height - 1, -1, -1):
                l = 0
                if layer < len(tower):
                    l = tower[layer]
                if l == 0:
                    lines[layer] += "|".center(tower_width) 
                else:
                    disk_width = l * (length_unit) + 1
                    lines[layer] += (left_edge + str(l).center(disk_width, "_") + right_edge).center(tower_width)
                    if layer + 1 < pillar_height:
                        upper_line = lines[layer + 1] 
                        for i in range(offset, offset + len(upper_line)):
                            padding_len = (tower_width - disk_width) // 2
                            if i >= offset + padding_len and i < offset + tower_width - padding_len and upper_line[i] == " ":
                                upper_line = upper_line[:i] + "_" + upper_line[i+1:]
                        lines[layer + 1] = upper_line
        boundary = "".center(tower_width * 3, "=")
        lines.insert(0, boundary)
        lines.append(boundary)
        return "\n".join(reversed(lines))
    def move(self, source: int, dist: int):
        disk = self.towers[source].pop()
        if len(self.towers[dist]) == 0:
            self.towers[dist].append(disk)
        else:
            dist_top = self.towers[dist].pop()
            if disk > dist_top:
                raise RuntimeError(f"can not move: disk {disk} is bigger the top of {dist_top}")
            self.towers[dist].append(dist_top)
            self.towers[dist].append(disk)

    def top(self, idx: int):
        if len(self.towers[idx]) == 0:
            return None
        top = self.towers[idx].pop()
        self.towers[idx].append(top)
        return top

    def count(self, idx):
        return len(self.towers[idx])

    def num_bigger_than(self, idx: int, n: int):
        tmp = Deque()
        x = self.towers[idx].pop()
        tmp.append(x)
        num = 0
        while x > n:
            num += 1
            x = self.towers[idx].pop()
            tmp.append(x)

        while len(tmp) > 0:
            self.towers.append(tmp.pop())

        return num



def solve(hanoi: Hanoi):
    move(hanoi, 0, 2, 1, hanoi.count(0))

def move(hanoi: Hanoi, source: int, dist: int, other: int, num: int):
    if num == 0:
        return
    elif num == 1:
        hanoi.move(source, dist)
    else:
        # 1. move all the pieces from last to middle
        # 2. move the top of first to last
        # 3. move all the pieces to last
        move(hanoi, source, other, dist, num - 1)
        move(hanoi, source, dist, other, 1)
        move(hanoi, other, dist, source, num - 1)
    sleep(0.3)
    print("\033[2J")
    print(hanoi)

def test_hanoi_view():
    game = Hanoi(6)
    game.move(0, 2)
    game.move(0, 1)
    print(game)

def test_hanoi_invalid_move():
    game = Hanoi(6)
    game.move(0, 2)
    with pytest.raises(RuntimeError, match=r'can not move:.*') as context:
        game.move(0, 2)

def test_solve_hanoi():
    game = Hanoi(6)
    solve(game)

if __name__ == '__main__':
    game = Hanoi(6)
    solve(game)
