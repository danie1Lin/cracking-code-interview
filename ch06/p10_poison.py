import unittest
import copy


class TestStrip:
    used: bool
    result: bool
    def __init__(self) -> None:
        self.used = False
        self.result = False

    def set(self, result):
        if self.used:
            raise ValueError('already used')
        self.result = result
        self.used = True

    def __repr__(self) -> str:
        return f'[used: {self.used}, result: {self.result}]'

# if we do not use test strip repeatedly
# but the question does not point out, so it is not the optimal solution.
class PoisonTestIn7days:
    def __init__(self, soda_num, test_strip_num, poison_idx) -> None:
        self.sodas = [False] * soda_num
        self.test_strips = [copy.copy(TestStrip()) for i in range(test_strip_num)]
        self.sodas[poison_idx] = True

    def test(self):
        for i in range(len(self.test_strips)):
            set_amount = 2 ** i
            arr = []
            for set_idx, set_start_idx in enumerate(range(0, len(self.sodas), 2**i)):
                if set_idx % 2 == 0:
                    continue
                arr.extend(range(set_start_idx, min(set_start_idx + set_amount, len(self.sodas))))
            self.test_strips[i].set(self.test_mix(arr))

    def test_mix(self, arr):
        for i in arr:
            if self.sodas[i] == True:
                return True
        return False

    def get_result(self):
        result = 0
        for idx, strip in enumerate(self.test_strips):
            if strip.result:
                result += 2 ** idx 
        return result

class TestPoisonTest(unittest.TestCase):
    test_cases = [
        8,
        315
    ]    
    def test_17days(self):
        for test_case in self.test_cases:
            self.poison_test = PoisonTestIn7days(1000, 10, test_case)
            self.expect = test_case
            self.poison_test.test()
            self.assertEqual(self.expect, self.poison_test.get_result(), f'{self.poison_test.test_strips}')

if __name__ == '__main__':
    unittest.main()
