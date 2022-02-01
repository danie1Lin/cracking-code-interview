from collections import defaultdict
from typing import Dict

import pytest
import math

# pick one to be prefix is more simpler than pick position to insert
def permutations_with_dup_prefix_version(s: str):
    counts = defaultdict(lambda: 0)
    for c in s:
        counts[c] += 1
    return permutation_form_counts(counts)

def permutation_form_counts(counts: Dict[str, int]) -> list[str]:
    all_zero = True
    for count in counts.values():
        if count != 0:
            all_zero = False
    if all_zero:
        return [""]
    result = []
    for char, count in counts.items():
        if count == 0:
            continue
        counts[char] -= 1
        sub_results = permutation_form_counts(counts)
        counts[char] += 1
        for sub_result in sub_results:
            result.append(char + sub_result)
    return result

def permutations_with_dup(s: str) -> list[str]:
    counts = defaultdict(lambda: 0)
    for c in s:
        counts[c] += 1
    result = []
    char = s[0]
    count = counts[char]
    if len(counts) == 1:
        return [s]
    sub_str = s.replace(char, "")
    permutations = permutations_with_dup(sub_str)
    for perm in permutations:
        max_insertable_postion = len(perm)
        for positions in choose_position(count, max_insertable_postion):
            new_perm = perm
            for position in positions:
                new_perm = new_perm[:position] + char + new_perm[position:]
            result.append(new_perm)
    return result



def choose_position(n: int, maximum:int) -> list[list[int]]:
    if n == 1:
        return [[x] for x in range(maximum+1)] 
    if maximum == 0:
        return [[0] * n]
    result = []
    for local_max in reversed(range(maximum + 1)):
        n_sets = choose_position(n - 1, local_max)
        for n_set in n_sets:
            n_set.insert(0, local_max)
            result.append(n_set)
    return result

def check_permutations_with_dup(s: str, f):
    permutations = f(s)
    counts = defaultdict(lambda: 0)
    for permutation in permutations:
        counts[permutation] += 1
        assert len(permutation) == len(s)

    for permutation, count in counts.items():
        if count != 1:
            pytest.fail(f"{permutation} shows {count} times")

    counts = defaultdict(lambda: 0)
    for c in s:
        counts[c] += 1
    permutations_count =math.factorial(len(s)) 
    for count in counts.values():
        permutations_count /= math.factorial(count)
    assert len(permutations) == permutations_count 

def test():
    cases = ["abcded", "aaaaa", "abcdee", "aabcde", "aabbccd"]
    for case in cases:
        check_permutations_with_dup(case, permutations_with_dup)
        check_permutations_with_dup(case, permutations_with_dup_prefix_version)
