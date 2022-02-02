from collections import defaultdict


def way(n: int):
    coins = [25, 10, 5, 1]
    return gen(n, coins)


def greedy_counts(n: int, coins: list[int]):
    counts = defaultdict(lambda: 0)
    for coin in coins:
        counts[coin] += n // coin
        n %= coin
    assert n == 0
    return counts

# 35
# 25 10  5  1
# 1   1  0  0 -> 10: 10 ,5, 1 的組合
# 0   3  1  0 -> 35: 10, 5, 1


def gen(n, coins):
    if len(coins) == 1 or n == 0:
        return 1
    if n < 0 or len(coins) == 0:
        return 0
    counts = greedy_counts(n, coins)
    coin, count = 0, 0
    for idx, i in enumerate(coins):
        if counts[i] != 0:
            coin = i
            break
    count = counts[coin]
    sum = 0
    for i in range(count + 1):
        sum += gen(n - i * coin, coins[idx + 1:])
    return sum


def test():
    assert 1 == way(4)
    assert 2 == way(5)
    assert 2 == way(6)
    assert 4 == way(10)
    assert 4 == way(11)
    assert 13 == way(25)
    assert 13 == way(26)
