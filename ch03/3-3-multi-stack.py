from .stack import Stack

class MultiStackWithLimit():
    stacks: list[Stack]
    limit: int

    def __init__(self, limit) -> None:
        self.stacks = [Stack()]
        self.limit = limit

    def push(self, value):
        if len(self.last_stack()) >= self.limit:
            self.stacks.append(Stack())
        self.last_stack().push(value)

    def peek(self):
        self.clean_empty()
        return self.last_stack().peek()

    """
    V1
    假設我們的 popAt 是單純的將其中一個 stack pop
    def popAt(self, stackNum):
        return self.stacks[stackNum].pop()

    """

    def popAt(self, stackNum):
        self.clean_empty()
        res = self.stacks[stackNum].pop()
        # XXX: 有沒有更好的寫法
        for next_stack_idx in range(stackNum + 1, self.last_stack_num() + 1):
            next_stack = self.stacks[next_stack_idx]
            current_stack = self.stacks[next_stack_idx - 1]
            last_value_of_next_stack = None
            if next_stack.top.next != None:
                last = next_stack.top
                c = last.next
                while c and c.next:
                    last = c
                    c = c.next
                last.next = None
                last_value_of_next_stack = c.data
            else:
                last_value_of_next_stack = next_stack.top.data
                next_stack.top = None
            if last_value_of_next_stack:
                current_stack.push(last_value_of_next_stack)
        return res

    def pop(self):
        self.clean_empty()
        return self.last_stack().pop()


    def clean_empty(self):
        while self.last_stack().is_empty() and self.last_stack_num() != 0:
            del(self.stacks[self.last_stack_num()])

    def last_stack(self):
        return self.stacks[self.last_stack_num()]

    def last_stack_num(self):
        return len(self.stacks) - 1


if __name__ == '__main__':
    stack = MultiStackWithLimit(2)
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert len(stack.stacks) == 2
    assert stack.pop() == 3
    assert stack.peek() == 2
    assert stack.pop() == 2
    assert stack.pop() == 1
    stack.push(1)
    stack.push(2)
    stack.push(3)
    stack.push(4)
    assert stack.popAt(0) == 2
    # 如果 popAt 要把後面的 stack 移過來用
    assert stack.popAt(0) == 3
    assert stack.pop() == 4
