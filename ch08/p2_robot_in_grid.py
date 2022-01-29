from typing import  Tuple
import unittest

def find_path(maze: list[list[bool]]) -> list[Tuple[int,int]] | None:
    path = []
    has_path(maze, len(maze) - 1, len(maze[0]) - 1, path)
    return path


def has_path(maze, r, c, path, visit=None) -> bool:
    if visit == None:
        visit = set() 
    if (r, c) in visit:
        return False
    else:
        visit.add((r, c))
    if (not maze[r][c]) or r < 0 or c < 0:
        return False
    if (r == 0 and c == 0) or has_path(maze, r - 1, c, path, visit) or has_path(maze, r, c - 1, path, visit):
        path.append((r,c))
        return True
    return False

# 轉換成 dp , 狀態 s(r, c) = 到 r , c 的其中一個 path
def find_path_dp(maze: list[list[bool]]) -> list[Tuple[int, int]]:
    r_count = len(maze)
    c_count = len(maze[0]) 
    state = [[None] * c_count for _ in range(r_count)] 
    state[0][0] = [(0, 0)]
    for r in range(r_count):
        for c in range(c_count):
            if not maze[r][c]:
                continue
            if r - 1 >= 0 and state[r - 1][c] != None:
                path = state[r - 1][c].copy()
                path.append((r, c))
                state[r][c] = path
            elif c - 1 >= 0 and state[r][c - 1] != None: 
                path = state[r][c-1].copy() 
                path.append((r, c))
                state[r][c] = path
    return state[r_count-1][c_count-1]

class TestFindPath(unittest.TestCase):
    def test(self):
        r, c = 5, 5
        maze = [ [ True ] * c  for _ in range(r) ]
        maze[0][1] = False
        maze[1][1] = False
        print(find_path(maze))
        print(find_path_dp(maze))

if __name__ == '__main__':
    unittest.main()
