# 1. use set to store and decide if the element should be picked.
# It will have 2 * n subset

import unittest


def find_all_subset(array: list[int]) -> list[set[int]]:
    source_set = set(array)
    subsets = list[set[int]]()
    subsets.append(set())
    for i in source_set:
        append_subset = list[set[int]]()
        for subset in subsets:
            new_set = subset.copy()
            new_set.add(i)
            append_subset.append(new_set)
        subsets.extend(append_subset)
    return subsets

class TestFindAllSubset(unittest.TestCase):
    def test(self):
        expect_set = [set([1,2,3]), set([1,2]), set([1,3]), set([2,3]), set([1]), set([2]), set([3]), set()]
        result = find_all_subset([1,2,3])
        self.assertEqual(len(expect_set), len(result))
        for s in result:
            self.assertIn(s, expect_set)

if __name__ == '__main__':
    unittest.main()

