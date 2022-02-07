# We can use array or hash to store the index of not empty string to jump direct to next word not empty. But it is still 0(n).
# It's sorted array so we have can use binary search but we have to skip empty string efficiently.
def spare_seach(arr: list[int], word: str):
    high = len(arr) - 1
    low = 0
    while high >= low:
        mid = (high + low) // 2
        curr = mid
        distance = 1
        while curr > low and high > curr and arr[curr] == "":
            curr = mid + distance
            if distance > 0:
                distance *= -1
            else:
                distance *= -1
                distance += 1
        if arr[curr] == "":
            return -1
        elif arr[curr] == word:
            return curr
        elif arr[curr] > word:
            low = curr + 1
        elif arr[curr] < word:
            high = curr - 1
    return -1


def test():
    assert 4, spare_seach(["at", "", "", "", "ball", "",
                          "", "car", "", "", "dad", "", ""], "ball")
