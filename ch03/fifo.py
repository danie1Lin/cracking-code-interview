import stack

class Fifo(stack.Stack):
    def __init__(self) -> None:
        self.last = None
        super().__init__()

    def add(self, value):
        node = stack.Node(value)
        if self.last == None:
            self.last = node 
        else:
            self.last.next = node 
            self.last = node

        if self.top == None:
            self.top = self.last

    def remove(self):
        node = self.top
        if node == None:
            return None
        self.top = node.next
        return node.data

if __name__ == "__main__":
    q = Fifo()
    q.add(1)
    assert 1 == q.peek()
    q.add(2)
    assert 1 == q.peek()

    assert 1 == q.remove()
    assert 2 == q.remove()
    assert None == q.remove()
