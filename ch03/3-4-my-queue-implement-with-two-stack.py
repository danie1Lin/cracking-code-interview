from ch03.stack import Stack

class MyQueue:
    def __init__(self) -> None:
        self.list =  Stack()
        self.tmp_list = Stack()

    def add(self, value):
        self.list.push(value)

    def remove(self):
        return self.remove_many(1)[0]

    def remove_many(self, count):
        while not self.list.is_empty():
            self.tmp_list.push(self.list.pop())
        res = []
        for i in range(count):
            res.append(self.tmp_list.pop())
        while not self.tmp_list.is_empty():
            self.list.push(self.tmp_list.pop())
        return res





if __name__ == '__main__':
    q = MyQueue()
    q.add(1)
    q.add(2)
    q.add(3)
    assert q.remove() == 1
    assert q.remove() == 2
    assert q.remove() == 3 
    q.add(1)
    q.add(2)
    q.add(3)
    assert q.remove_many(3) == [1,2,3]

