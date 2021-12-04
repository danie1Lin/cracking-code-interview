import pprint
import json
from itertools import chain
from stack import Stack
# first level: the queue will not grow or shrink
# second level: the stack will grow when not enough
# third level: see array as ring buffer

# other thought
# 1. How to relocation the stack
# 2. 看到動態調整可以聯想到 ring buffer 不過 queue 會比 stack 更適合

"""
start 會是該 stack 的第 0 個元素
end 會是最後一個元素的 ’後一個‘
好處:
end - start 就會是長度
list[start: end] 就是 start 到 end - 1 的元素


ring 的位置計算
可以用 ‘%’ 來完成大多數麻煩的判斷
abs_idx %= total 就可以避免 out of range
(total + end - start) % total 就可以避免 end 繞道 start 前面變成負的
"""
def len_of_ring(start: int, end: int, total: int) -> int:
    """
    if is_cross_head_and_tail(start, end, total):
        return total - start + end
    return end - start
    用下面的寫法就很快
    """
    return (total + end - start) % total # 先將 end 加上 total 後，這樣不管 end 是不是在 start 前面都可以算


# def is_cross_head_and_tail(start: int, end: int, total: int) -> bool:
    # return end < start < total 

def to_abs_idx_of_ring(start: int, total: int, rel_idx: int) -> int:
    """
    
    原本這樣寫，不過其實用 mod 不管 rel_idx 多大都可以
    version 1
    abs_idx = rel_idx + start
    if abs_idx >= total:
        abs_idx -= total
    return abs_idx
    """
    """
    version 2:

    (start + rel_idx) % total
    有些無法對應負數，ex abs_idx = -11 total = 10
    python -11 % 10 會是 9 
    但是 java/Golang/rust/js -11 % 10 會是 -1
    就必須換成這樣：

    abs_idx = start + rel_idx 
    return ( abs_idx % total + total) % total
    """
    return (start + rel_idx) % total



class StackNoSpace(Exception):
    pass

class SliceStack:
    def __init__(self, arr: list, start, end) -> None:
        self.slice = arr
        self.start_idx = start
        self.end_idx = end
        self.next_idx = self.start_idx
        self.next_stack = None

    def cap(self):
        return len_of_ring(self.start_idx, self.end_idx, len(self.slice))

    def len(self):
        return len_of_ring(self.start_idx, self.next_idx, len(self.slice))

    def get(self, rel_idx):
        return self.slice[to_abs_idx_of_ring(self.start_idx, len(self.slice), rel_idx)]

    def set(self, rel_idx, value):
        self.slice[to_abs_idx_of_ring(self.start_idx, len(self.slice), rel_idx)] = value
    
    def push(self, value):
        if self.len() >= self.cap():
            raise StackNoSpace
        self.slice[self.next_idx] = value
        self.next_idx += 1
        self.next_idx %= len(self.slice)

    def space_left(self) -> int:
        return max(len_of_ring(self.next_idx, self.end_idx, len(self.slice)), 0)

    def pop(self):
        if self.next_idx == self.start_idx:
            raise IndexError
        v = self.slice[self.next_idx - 1]
        self.next_idx -= 1
        """
        雖然可以寫
        self.next_idx -= 1
        v = self.slice[self.next_idx]
        但是流程上先取之前的值再做後面的操作比較易懂
        """
        return v

    def shift_to(self, start, end):
        if self.len() > len_of_ring(start, end, len(self.slice)):
            raise StackNoSpace

        # the start is change should shift
        shift = start - self.start_idx
        if shift > 0:
            for i in range(self.len()-1, -1, -1): # ex len 3 -> 2, 1, 0 遞減
                self.set(shift + i, self.get(i))
        elif shift < 0:
            # raise ValueError("shift can not be negative")
            for i in range(0, self.len()):
                self.set(shift + i, self.get(i))

        self.next_idx += shift 
        self.start_idx = start
        self.end_idx = end

    def shift_rel(self, start, end):
        start = self.start_idx + start
        if start > len(self.slice) - 1:
            start = start - len(self.slice) - 1

        end = self.end_idx + end
        if end > len(self.slice) - 1:
            end = end - len(self.slice) - 1

        self.shift_to(start, end)

    def to_list(self):
        res = []
        for i in range(self.len()):
            res.append(self.get(i))
        return res



class MultiStack:
    def __init__(self, array: list, queue_count) -> None:
        self.data = array
        self.total = len(array)
        self.queue_count = queue_count
        average_cap = int(self.total / self.queue_count)
        self.stacks = []
        for i in range(self.queue_count):
            start = i * average_cap
            if i == self.queue_count - 1:
                end = 0 # 本來是寫 end = total 但是在環中 total 的位置跟 0 一樣
            else:
                end = (i+1) * average_cap
            self.stacks.append(SliceStack(self.data, start, end))

    def push(self, stack_num, value):
        current_stack = self.stacks[stack_num]
        try:
            current_stack.push(value)
        except StackNoSpace:
            space = self.space_left()
            if space < 1:
                raise
            shift_space = int(space / self.queue_count) # 這個平均分配的策略也許可以優化
            if shift_space < 1:
                shift_space = space
            tmp = Stack()
            shift = shift_space
            """
            或是
            for i in chain(range(stack_num + 1, self.queue_count), range(0, stack_num)):
            """
            for idx in range(stack_num + 1, stack_num + 1 + self.queue_count):
                idx %= self.queue_count
                stack = self.stacks[idx]
                available_decrease = min(stack.space_left(), shift)
                """
                1. 押入 stack , 之後從後面開始 shift 才不會把資料蓋掉
                2. 使用相對來操作會易讀許多

                這邊有個巧思是因為上一個往後移多少，下一個 start 就要往後移多少
                所以 start 的位置直接帶入 shift
                但是光是平移不夠還要要把這些空間讓出來，所以是後移 shift - available_decrease = end

                available_decrease 應該還有其他的策略，比如說用平均可用空間
                """
                tmp.push((stack, shift, shift - available_decrease))
                shift -= available_decrease
                if shift <= 0:
                    break

            # no space if run through all stack, there is still shift can not be digest 
            if shift > 0: 
                raise StackNoSpace
            while tmp.top != None:
                s = tmp.pop()
                s[0].shift_rel(s[1], s[2])
            current_stack.shift_rel(0, shift_space)
            current_stack.push(value)

    def pop(self, stack_num):
        return self.stacks[stack_num].pop()

    def space_left(self):
        return sum([x.space_left() for x in self.stacks])

    def inspect(self):
        pprint.pprint([(x.to_list(), x.start_idx, x.end_idx, x.next_idx) for x in self.stacks])

if __name__ == '__main__':
    li = [0] * 10
    stacks = MultiStack(li, 3)
    assert 10 == sum([x.cap() for x in stacks.stacks])

    ss = [x for x in stacks.stacks]
    stacks.push(0, 100)
    stacks.push(1, 101)
    stacks.push(2, 102)
    assert 10 == sum([x.cap() for x in stacks.stacks])
    assert stacks.pop(0) == 100
    assert stacks.pop(1) == 101
    assert stacks.pop(2) == 102

    stacks.push(0, 100)
    stacks.push(1, 101)
    stacks.push(2, 102)
    stacks.push(2, 103)
    stacks.push(2, 104)
    stacks.push(2, 105)
    stacks.push(2, 106)
    stacks.inspect()
    assert 106 == stacks.pop(2)
    assert 100 == stacks.pop(0)
    for i in range(5):
        stacks.push(0, 200 + i)
        stacks.inspect()


    stacks = MultiStack([0] * 99, 3)
    for i in range(34):
        stacks.push(2, i)
        stacks.push(0, i)
        
    stacks.inspect()

