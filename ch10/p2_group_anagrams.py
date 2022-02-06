# apple tea coffee eat => apple coffee eat tea
# anagrams is different from palindrome
# anagrams two word is same in alphabet amount
from typing import DefaultDict


def sort_by_anagrams(words: list[str]):
    words.sort(key=by_anagrams_with_map)


# O(nlog(n))
def by_anagrams_by_sort_str(s: str):
    return sorted(s.lower())

# if given word in ascii set in limited length we can use this way. If not, will overflow, and we have to use a map to store the words counts
# we use char value to represent the word, same amount in every alphabet will get same number
# the key function has O(n) time complexity
# apple = v(a) + v(p) * 2 + v(l) + v(e)


def by_anagrams(s: str):
    v = 0
    for c in s.lower():
        v += ord(c)
    return v


def by_anagrams_with_map(s: str):
    counts = DefaultDict(lambda: 0)
    for c in s.lower():
        counts[c] += 1
    return counts


def test():
    cases = [dict(given=['apple', 'tea', 'coffee', 'eat', 'fefeco', 'paple'],
                  expected=['tea', 'eat', 'apple', 'paple', 'coffee', 'fefeco'])]
    for case in cases:
        words = case['given'].copy()
        sort_by_anagrams(words)
        assert words == case['expected']
