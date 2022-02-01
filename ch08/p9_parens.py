from typing import Deque, NamedTuple
import pytest


# use recursion like this is not working efficiently.
# 2 => ()(), (())
# 3 => (())(), ()(()), ((())), (()()) = 2 check every place to insert: ^(^(^)) ^(^)(^)
# And It also will get duplicated permutation
# So we have to split `(` `)` into`(` and`)`.
# We can record the `(` and `)` number we can use.
# if we already use one `(` we can add `)` or another `(` but, in later, we have to add two `)`
def parens(n: int) -> list[str]:
    deep = 0
    q = Deque()
    q.append((n, 0, ""))
    result = []
    while q:
        paren_num, deep, permutation = q.pop()
        if deep == 0 and paren_num == 0:
            result.append(permutation)
        else:
            if deep > 0:
                q.append((paren_num, deep - 1, permutation + ")"))
            if paren_num > 0:
                q.append((paren_num - 1, deep + 1, permutation + "("))
    return result


class ParansTestCase(NamedTuple):
    given: int
    expected: list[str]


@pytest.fixture
def cases():
    return [
        ParansTestCase(3, ["()()()", "(())()", "()(())", "(()())", "((()))"]),
        ParansTestCase(2, ["(())", "()()"])
    ]


def test_parens(cases):
    for case in cases:
        result = parens(case.given)
        print(result)
        assert len(result) == len(case.expected)
        for expected_possible in case.expected:
            assert expected_possible in result
