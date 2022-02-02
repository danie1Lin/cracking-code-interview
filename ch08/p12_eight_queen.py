# print all ways of eight queen not in same row, column, diagonal
# we have 8 * 8, and we have to place 8 queens, so we have to place one queen at each row and column
# the question left is how we prevent place in diagonal

# you can ask question like: Is different orientation considered as different? If do not we have to consider another way

from typing import NewType
import copy
import math
TBoard = NewType('TBoard', list[list[int]])


def eight_queens() -> list[TBoard]:
    permutations = permutation(0)
    for i in range(len(permutations)):
        for r in range(8):
            for c in range(8):
                if permutations[i][r][c] == -1:
                    permutations[i][r][c] = 0
    return permutations


def permutation(offset_r: int) -> list[TBoard]:
    row, col = 8, 8
    if offset_r == row:
        return [[[0] * row for _ in range(col)]]

    permutations = permutation(offset_r + 1)
    result = []
    for board_permutation in permutations:
        for c in range(col):
            if board_permutation[offset_r][c] == -1:
                continue
            board = copy.deepcopy(board_permutation)
            result.append(board)
            board[offset_r][c] = 1
            # optimize: we do not need to check the row had been place before
            for tmp_r in range(offset_r):
                board[tmp_r][c] = -1
            for tmp_c in range(8):
                dis = c - tmp_c
                if dis == 0:
                    continue
                board[offset_r][tmp_c] = -1
                if row > offset_r + dis and offset_r + dis >= 0:
                    board[offset_r+dis][tmp_c] = -1
                if row > offset_r - dis and offset_r - dis >= 0:
                    board[offset_r-dis][tmp_c] = -1
    return result


def filter(permutations: list[TBoard]) -> list[TBoard]:
    result = []
    while permutations:
        p = permutations.pop()
        for i in range(3):
            for i in range(len(permutations)):
                if board_equal(permutations[i], transform90(p)):
                    permutations.pop(i)
                    break
        result.append(p)
    return result


def transform90(board: TBoard) -> TBoard:
    n = board[::-1]
    res = []
    for line in zip(*n):
        res.append(line)
    return res


def board_equal(a: TBoard, b: TBoard):
    if len(a) != len(b):
        return False

    for r in range(len(a)):
        if len(a[r]) != len(b[r]):
            return False
        for c in range(len(a)):
            if a[r][c] != b[r][c]:
                return False
    return True


def test():
    row, col = 8, 8
    permutations = eight_queens()
    assert 92 == len(permutations)
    uniq_permutations = set()
    for permutation in permutations:
        uniq_permutations.add(str(permutation))
        queen_count = 0
        print("")
        print("=" * 24)
        for r in range(8):
            print("")
            for c in range(8):
                print(str(permutation[r][c]).center(4), end="")
                if permutation[r][c] == 1:
                    queen_count += 1
                    for tmp_r in range(8):
                        if tmp_r == r:
                            continue
                        assert permutation[tmp_r][c] != 1
                    for tmp_c in range(8):
                        if tmp_c == c:
                            continue
                        assert permutation[r][tmp_c] != 1
                        dis = c - tmp_c
                        if row > r + dis and r + dis >= 0:
                            assert permutation[r+dis][tmp_c] != 1
                        if row > r - dis and r - dis >= 0:
                            assert permutation[r-dis][tmp_c] != 1
        assert queen_count == 8
    assert 92 == len(uniq_permutations)
    print(f"total: {len(permutations)}")
