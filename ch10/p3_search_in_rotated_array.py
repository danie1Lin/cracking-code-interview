from typing import Deque

# We must perform better than O(n) or this question is meaningless.


def to_abs_idx(a: int, head: int, length: int):
    abs_idx = (a + head) % length
    """
    跟下面的邏輯一樣
    abs_idx = a + head
    if abs_idx > length - 1:
        abs_idx -= length
    """
    return abs_idx


def search_in_rotated_array(arr: list[int], v: int) -> int:
    # find the index of the smallest element. we have to make it to O(log(n)) to beat 0(n)
    # 15, 16, 19, 20, 25, 1, 3, 4, 5, 7, 10, 14
    # |> high & > low     |    < low & < high  |
    high = len(arr) - 1
    low = 0
    head = 0
    while high >= low:
        head = (high + low) // 2
        if arr[head] < arr[low]:
            high = head - 1
        else:
            low = head + 1
    rel_max = len(arr) - 1
    rel_min = 0
    while rel_max >= rel_min:
        rel_current = (rel_max + rel_min) // 2
        curr_v = arr[to_abs_idx(rel_current, head, len(arr))]
        if v > curr_v:
            rel_min = rel_current + 1
        elif v < curr_v:
            rel_max = rel_current - 1
        else:
            return to_abs_idx(rel_current, head, len(arr))
    return -1


def test():
    test_cases = [
        dict(arr=[1, 3, 7, 8, 9, 10], n=1),
        dict(arr=[1, 2, 3], n=1),
        dict(arr=[1, 2], n=1),
        dict(arr=[1, 3, 4, 5, 7, 10, 14, 15, 16, 19, 20, 25], n=4)
    ]
    for search in [search_in_rotated_array]:
        for case in test_cases:
            n = case['n']
            arr = case['arr']
            arr = arr[len(arr) - n:] + arr[:len(arr) - n]
            find = arr[min(n+1, len(arr) - 1)]
            expected = arr.index(find)
            assert expected == search(arr, find)
            assert -1 == search(arr, 100)
