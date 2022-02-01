from typing import Deque, Tuple


def paint_fill(canvas: list[list[int]], color: int, r: int, c: int):
    origin = canvas[r][c]
    visited = set()
    queue = Deque()
    queue.append((r, c))
    while queue:
        r, c = queue.pop()
        visited.add((r, c))
        canvas[r][c] = color
        for next_r in range(max(0, r - 1), min(len(canvas)-1, r+1) + 1):
            for next_c in range(max(0, c - 1), min(len(canvas[next_r])-1, c+1) + 1):
                if canvas[next_r][next_c] == origin and (next_r, next_c) not in visited:
                    queue.append((next_r, next_c))


def test_paint_fill():
    canvas = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 0, 1, 1],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 1]
    ]

    paint_fill(canvas, 2, 0, 0)

    expect = [
        [2, 2, 2, 2, 2],
        [2, 1, 1, 1, 2],
        [2, 1, 0, 1, 1],
        [2, 1, 1, 1, 2],
        [2, 2, 2, 2, 1]
    ]

    assert expect == canvas
