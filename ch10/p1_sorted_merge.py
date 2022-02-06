# We have to merge B into A
# Can we use another buffer to copy A? You can ask interviewer. But I assume not. I will solve it with in-place merge


def sorted_merge_in_place(a: list[int], b: list[int], a_length: int):
    # check the length
    if len(a) < len(b) + a_length:
        raise ValueError("array a must have enough buffer")
    # for not overwrite the element in a before we loop to it, we can loop from back
    p_a = a_length - 1
    p_b = len(b) - 1
    p_store = a_length + len(b) - 1
    while p_b >= 0:
        if p_a >= 0 and a[p_a] > b[p_b]:
            a[p_store] = a[p_a]
            p_a -= 1
        else:
            a[p_store] = b[p_b]
            p_b -= 1
        p_store -= 1


def test_sorted_merge():
    test_cases = [
        dict(a=[0, 4, 6, 7, 8], b=[3, 5, 9, 10],
             ans=[0, 3, 4, 5, 6, 7, 8, 9, 10]),
        dict(a=[1, 2, 3], b=[], ans=[1, 2, 3]),
        dict(a=[1, 2, 3], b=[4, 5, 6, 7], ans=[1, 2, 3, 4, 5, 6, 7]),
        dict(a=[1, 2, 3], b=[0], ans=[0, 1, 2, 3]),
        dict(a=[0], b=[1, 2, 3], ans=[0, 1, 2, 3]),
    ]
    for test_case in test_cases:
        a = test_case['a']
        b = test_case['b']
        a_len = len(a)
        a += [-1] * len(b)
        sorted_merge_in_place(a, b, a_len)
        assert a == test_case['ans']
