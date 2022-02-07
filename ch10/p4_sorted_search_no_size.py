# can not use len() to get size
# of course, we can use elementAt(i) to get size, but it will be O(n).
# But I think that making this quesiton meaningless. So we have to solve better than O(n)

# we can search at 2^n element once bigger than value we want we can use binary search again.

def element_at(arr, i):
    if i >= len(arr):
        return -1
    return arr[i]


def search(arr: list[int], v: int) -> int:
    low, high = 0, 1
    curr_v = element_at(arr, high)
    if curr_v == -1:
        if element_at(arr, low) == v:
            return 0
        return -1

    while curr_v < v and curr_v > 0:
        curr_v = element_at(arr, high)
        low = high
        high *= 2

    while high >= low:
        mid = (high+low) // 2
        curr_v = element_at(arr, mid)
        if curr_v == -1:
            high = mid - 1
        elif curr_v == v:
            return mid
        elif curr_v > v:
            high = mid - 1
        else:
            low = mid + 1
    return -1


def test():
    assert 2 == search([0, 1, 3, 4, 5, 6, 7], 3)
    assert 0 == search([0, 1, 3, 4, 5, 6, 7], 0)
    assert -1 == search([0, 1, 3, 4, 5, 6, 7], 10)
    assert -1 == search([0], 2)
