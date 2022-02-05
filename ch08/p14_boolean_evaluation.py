# not extraneous: (1) same as ((1))
# 對於這種題型來說遞迴的方式不太一樣
# 1 ^ 0 | 0 | 1
# 1 ^ (...) + (1 ^ 0) | (...) + (1^0|0) ^ (...)
from typing import DefaultDict


DEBUG = False


def count_evaluate_dp(eq: str, result: bool) -> int:
    # state[offset][True/False] = ways
    state = DefaultDict(lambda: DefaultDict(lambda: [0, 0]))
    for i in range(0, len(eq), 2):
        state[eq[i]][i][int(eq[i])] = 1
    for l in range(3, len(eq)+1, 2):
        for i in range(0, len(eq) - l+1, 2):
            tmp_eq = eq[i:i+l]
            for op_idx in range(1, len(tmp_eq), 2):
                op = tmp_eq[op_idx]
                left = tmp_eq[:op_idx]
                right = tmp_eq[op_idx+1:]
                left_ways = state[left][i]
                right_ways = state[right][i+op_idx+1]
                for left_value, left_way_count in enumerate(left_ways):
                    for right_value, right_way_count in enumerate(right_ways):
                        match op:
                            case "^":
                                state[tmp_eq][i][int(bool(left_value) ^ bool(
                                    right_value))] += left_way_count * right_way_count
                            case "|":
                                state[tmp_eq][i][int(bool(left_value) | bool(
                                    right_value))] += left_way_count * right_way_count
                            case "&":
                                state[tmp_eq][i][int(bool(left_value) & bool(
                                    right_value))] += left_way_count * right_way_count
                            case _:
                                raise RuntimeError(
                                    f"{tmp_eq}: from:{i} length:{l} op_idx: {op_idx}")
    way = 0
    for ways in state[eq].values():
        way += ways[result]
    return way


def count_evaluate(eq: str, result: bool, deep=0) -> int:
    if len(eq) == 1:
        if bool(int(eq)) == result:
            return 1
        return 0
    prefix = "| " * deep
    if DEBUG:
        print(prefix, "".ljust(3, ">"), ":", eq, "=", result)
    ways = 0
    for op_idx in range(1, len(eq), 2):
        left = eq[:op_idx]
        op = eq[op_idx]
        right = eq[op_idx+1:]
        for left_value in [True, False]:
            right_values = get_right_value(left_value, result, op)
            if len(right_values) == 0:
                continue
            left_way = count_evaluate(left, left_value, deep+1)
            for other_part_result in right_values:
                right_ways = count_evaluate(right, other_part_result, deep+1)
                ways += left_way * right_ways
    if DEBUG:
        print(prefix, str(ways).ljust(3, "<"),  eq, "=", result)
    return ways


def get_right_value(left: bool, result: bool, op: str) -> list[bool]:
    assert op in ["|", "&", "^"]
    match op:
        case "^":
            if result:
                return [not left]
            else:
                return [left]
        case "&":
            if result:
                if left:
                    return [True]
                return []
            else:
                if left:
                    return [False]
                else:
                    return [True, False]
        case "|":
            if not result:
                if left:
                    return []
                else:
                    return [False]
            else:
                if left:
                    return [True, False]
                else:
                    return [True]
    return []


def test_count_evaluate():
    for f in [count_evaluate_dp,  count_evaluate]:
        assert 10 == f("0&0&0&1^1|0", True)
        assert 2 == f("1^0|0|1", False)
        assert 547 == f("1^1^0^0&0|1&1&1^1", True)
