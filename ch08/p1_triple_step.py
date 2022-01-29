import unittest

def ways_of_climb_stair(n: int):
    if n == 1:
        return 1
    elif n == 2:
        return 2 # 1 + 1 / 2
    elif n == 3:
        return 4# 1 + 1 + 1 / 1 + 2 / 2 + 1 / 3
    elif n == 0:
        return 0

    return ways_of_climb_stair(n - 1) + ways_of_climb_stair(n - 2) + ways_of_climb_stair(n - 3) 

def ways_of_climb_stair_memory(n: int, m: dict[int,int]|None=None):
    if m is None:
        m = dict()
        m[0] = 0
        m[1] = 1
        m[2] = 2 
        m[3] = 4

    if m.get(n) is None :
        m[n] = ways_of_climb_stair_memory(n-1, m) + ways_of_climb_stair_memory(n-2, m) + ways_of_climb_stair_memory(n-3, m)
        return m[n]
    else:
        return m[n]

def ways_of_climb_stair_dp(n: int):
    dp = [0] * (n + 1)
    dp[1], dp[2], dp[3] = 1, 2, 4 
    for i in range(4, n+1):
        dp[i] = dp[i-1] + dp[i-2] + dp[i-3]
    return dp[n]

def answer(n):
    if n < 0:
        return 0
    elif n == 0:
        return 1
    return answer(n - 1) + answer(n-2) + answer(n-3)

class TestClimbStair(unittest.TestCase):
    def test(self):
        self.assertEqual(answer(10), ways_of_climb_stair(10))
        self.assertEqual(answer(10), ways_of_climb_stair_memory(10))
        self.assertEqual(answer(10), ways_of_climb_stair_dp(10))

if __name__ == '__main__':
    unittest.main()
