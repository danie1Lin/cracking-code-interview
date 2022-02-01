from collections import defaultdict
import math

import pytest


def permutations_without_dup(s: str) -> list[str]:
    if len(s) == 1:
        return [s]
    sub_permutations = permutations_without_dup(s[1:])
    result = []
    for sub_permutation in sub_permutations:
        for i in range(len(sub_permutation) + 1):
            result.append(sub_permutation[:i] + s[0] + sub_permutation[i:])
    return result


def test_permutations_without_dup():
    s = "abcde"
    permutations = permutations_without_dup(s)
    counts = defaultdict(lambda: 0)
    for permutation in permutations:
        counts[permutation] += 1
        assert len(permutation) == len(s)

    for permutation, count in counts.items():
        if count != 1:
            pytest.fail(f"{permutation} shows {count} times")

    assert len(permutations) == math.factorial(len(s))

    print(permutations)
