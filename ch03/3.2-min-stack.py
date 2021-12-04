from stack import Stack

"""
一定要是 O(1) 所以只用一個值在 pop 的時候，如果將最小 pop 掉了，要找出最小會超過 O(1)，所以我們要記錄所有的最小值的 history
1. 用另一個 stack 來記錄最小的 history
2. 在 node 中記錄上一個最小值，在 pop 時用這個最小值更新 MinStack 的最小值

1 較優，不破壞原本的 Stack 符合開閉原則，而且如果 stack 很長，用到的空間較少
"""

class MinStack(Stack):
    def __init__(self) -> None:
        super().__init__()
        self.__min_history = Stack()

    def push(self, value):
        super().push(value)
        if self.__min_history.peek() == None or self.__min_history.peek() >= value: # >=，否則如果有兩個一樣小的在 pop 的時候會把最小的 pop 掉，就會連續跳兩個
            self.__min_history.push(value)

    def pop(self):
        result = super().pop()
        if result == self.__min_history.peek():
            self.__min_history.pop()
        return result

    def min(self):
        return self.__min_history.peek()


if __name__ == '__main__':
    stack = MinStack()
    stack.push(5)
    assert stack.min() == 5
    stack.push(6)
    assert stack.min() == 5
    stack.push(3)
    assert stack.min() == 3
    stack.push(7)
    assert stack.min() == 3
    stack.pop()
    assert stack.min() == 3
    stack.pop()
    assert stack.min() == 5
