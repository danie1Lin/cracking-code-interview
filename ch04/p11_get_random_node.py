from typing import DefaultDict
import unittest
from .tree import BinaryTreeNode
import random
class NodeWithAmount(BinaryTreeNode):
    def amount(self):
        amount = 1
        if self.left:
            amount += self.left.amount()
        if self.right:
            amount += self.right.amount()
        return amount

    def get_random_node(self):
        count = [1] 
        if self.left:
            count.append(self.left.amount())
        else:
            count.append(0)
        if self.right:
            count.append(self.right.amount())
        else:
            count.append(0)
        total = sum(count)
        rand = random.randint(1, total)
        if rand == count[0]:
            return self
        elif 1 < rand <= count[0] + count[1]:
            return self.left.get_random_node() 
        else:
            return self.right.get_random_node()


class TestNodeWithAmount(unittest.TestCase):
    def test_amount(self):
        tree = NodeWithAmount.build_minimum_searching_tree(range(15))
        self.assertIs(tree.amount(), 15)
        self.assertIs(tree.left.amount(), 7)

    def test_get_random(self):
        tree = NodeWithAmount.build_minimum_searching_tree(range(100))
        data = DefaultDict(lambda: 0)
        for i in range(100000):
            node = tree.get_random_node()
            data[node.value] += 1
        
        import matplotlib.pyplot as plt
        names = list(data.keys())
        values = list(data.values())

        fig, axs = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
        axs[0].bar(names, values)
        axs[1].scatter(names, values)
        axs[2].plot(names, values)
        fig.suptitle('Categorical Plotting')
        plt.show()


if __name__ == '__main__':
    unittest.main()
        


