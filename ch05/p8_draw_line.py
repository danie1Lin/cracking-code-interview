from typing import Tuple
import unittest


def draw_line(screen: [int], width: int, x1: int, x2: int, y: int):
    for x in range(x1, x2+1):
        pos = convert(x, y, width)
        screen[pos[0]] |= 1 << (8 - pos[1] - 1)
    for idx, i in enumerate(screen):
        if (idx * 8) % width == 0:
            print()
        v = bin(i).replace("0b", "").rjust(8, "0")
        print(f"{v:>8}", end="")

def convert(x: int, y: int, width: int) -> Tuple[int, int]:
    bit = y * width + x
    offset = bit % 8
    idx = int(bit / 8)
    return idx, offset


class TestDrawLine(unittest.TestCase):
    def test(self):
        draw_line([0]* 32, 16, 4, 15, 0)

if __name__ == '__main__':
    unittest.main()
