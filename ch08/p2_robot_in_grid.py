from typing import Any, Tuple
from dataclasses import dataclass
import unittest

def find_path(maze: list[list[bool]]) -> list[Tuple[int,int]] | None:
    path = []
    has_path(maze, len(maze) - 1, len(maze[0]) - 1, path)
    return path


def has_path(maze, r, c, path) -> bool:
    if (not maze[r][c]) or r < 0 or c < 0:
        return False
    if (r == 0 and c == 0) or has_path(maze, r - 1, c, path) or has_path(maze, r, c - 1, path):
        path.append((r,c))
        return True
    return False


class TestFindPath(unittest.TestCase):
    def test(self):
        r, c = 5, 5
        maze = [ [ True ] * c  for _ in range(r) ]
        maze[0][1] = False
        maze[1][1] = False
        print(find_path(maze))

if __name__ == '__main__':
    unittest.main()
