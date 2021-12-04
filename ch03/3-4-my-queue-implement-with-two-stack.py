from ch03.stack import Stack

class MyQueue:
    def __init__(self) -> None:
        self.list =  Stack()
        self.tmp_list = Stack()

    def add(self, value):
        self.list.push(value)

    def remove(self):
        while not self.list.is_empty():
            self.tmp_list.push(self.list.pop())
        res = self.tmp_list.pop()
        while not self.tmp_list.is_empty():
            self.list.push(self.tmp_list.pop())
        return res

class MyQueueV2:
    """
    v2 改進版
    如果連續 remove 不會倒過去再倒回來
    """
    def __init__(self) -> None:
        self.list =  Stack()
        self.tmp_list = Stack()

    def add(self, value):
        self.list.push(value)

    def remove(self):
        """
        倒過去就不需要再倒回來了，因為原本的 list push也沒有影響
        """
        if self.tmp_list.is_empty():
            while not self.list.is_empty():
                self.tmp_list.push(self.list.pop())
        return self.tmp_list.pop()

if __name__ == '__main__':
    q1 = MyQueue()
    def test(q):
        q.add(1)
        q.add(2)
        q.add(3)
        assert q.remove() == 1
        assert q.remove() == 2
        q.add(4)
        assert q.remove() == 3 
        q.add(5)
        q.add(6)
        assert q.remove() == 4


    test(q1)
    test(MyQueueV2())
