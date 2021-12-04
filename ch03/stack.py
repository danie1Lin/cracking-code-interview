class Stack:
    def __init__(self):
        self.top = None

    def __len__(self):
        if self.top is None:
            return 0
        c = self.top
        count = 1
        while c.next != None:
            c = c.next
            count += 1
        return count

    def is_empty(self):
        if self.top == None:
            return True
        return False

    def peek(self):
        if self.top is None:
            return None
        return self.top.data

    def push(self, value):
        new_node = Node(value)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        node = self.top
        if node is None:
            return None
        self.top = self.top.next
        return node.data


class Node:
    def __init__(self, value) -> None:
        self.data = value
        self.next = None


if __name__ == "__main__":
    q = Stack()
    assert(None == q.peek())
    assert(True == q.is_empty())
    q.push(1)
    q.push(2)
    assert(2 == q.peek())
    assert(2 == q.pop())
    assert(1 == q.peek())
    assert(False == q.is_empty())
