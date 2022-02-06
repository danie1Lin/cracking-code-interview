# apple tea coffee eat => apple coffee eat tea
# anagrams is different from palindrome
# anagrams two word is same in alphabet amount
def sort_by_anagrams(words: list[str]):
    words.sort(key=by_anagrams)


def by_anagrams(s: str):
    return sorted(s)


def test():
    cases = [dict(given=['apple', 'tea', 'coffee', 'eat', 'fefeco', 'paple'],
                  expected=['apple', 'paple', 'tea', 'eat', 'coffee', 'fefeco'])]
    for case in cases:
        words = case['given'].copy()
        sort_by_anagrams(words)
        assert words == case['expected']
