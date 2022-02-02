from collections import defaultdict


def way(n: int):
    coins = [25, 10, 5, 1]
    return permutation(n, coins)

# 35
# 25 10  5  1
# 1   1  0  0 -> 10: 10 ,5, 1 的組合
# 0   3  1  0 -> 35: 10, 5, 1


def permutation(n, coins, coin_offset=0, mem=None):
    if mem == None:
        mem = [[None] * (len(coins)+1) for _ in range(n+1)]
    else:
        ways = mem[n][coin_offset]
        if ways != None:
            return ways
    if n < 0:
        return 0
    if coin_offset >= len(coins):
        if n == 0:
            return 1
        else:
            return 0
    if coin_offset == len(coins) - 1 or n == 0:
        return 1
    count, max_coin, max_coin_idx = 0, 0, 0
    # 找出最大的
    for idx, coin in enumerate(coins[coin_offset:]):
        count = n // coin
        if count:
            max_coin = coin
            max_coin_idx = idx
            break
    sum = 0
    # 如果最大的有 n 個，最大的選法是 0～n 個，
    for i in range(count + 1):
        sum += permutation(n - i * max_coin, coins,
                           coin_offset + max_coin_idx + 1, mem)
    mem[n][coin_offset] = sum
    return sum

# coin M sum N
# count 最差是 N
# O(M * N)


def way_dp(n: int):
    coins = [1, 5, 10, 25]
    dp = [[0] * len(coins) for _ in range(n + 1)]
    # state[n][coins begin from this index can be choose]
    for i in range(n+1):
        dp[i][0] = 1

    for i in range(len(coins)):
        dp[0][i] = 1

    for amount in range(1, n+1):
        for offset in range(1, len(coins)):
            coin = coins[offset]
            count = amount // coin
            for i in range(count+1):
                dp[amount][offset] += dp[amount - i * coin][offset - 1]

    return dp[n][len(coins) - 1]


def test():
    for f in [way, way_dp]:
        assert 1 == f(4)
        assert 2 == f(5)
        assert 2 == f(6)
        assert 4 == f(10)
        assert 4 == f(11)
        assert 13 == f(25)
        assert 13 == f(26)
        assert 49 == f(51)
        assert 49 == f(50)
