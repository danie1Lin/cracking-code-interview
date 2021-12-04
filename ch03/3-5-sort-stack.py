from ch03.stack import Stack

"""
覺得這個題目描述的不是很明確
將 stack 排序是單一次操作還是 pop / push 操作後都可以維持排序
從 p287 頁看起來是單一次把 stack 做 inplace 排序
所以在做排序的題目可以問
1. 是否要 inplace
2. 時間 空間 數據結構類型 限制
"""

def sort_stack(stack: Stack):
    tmp = Stack()
    tmp.push(stack.pop())
    while not stack.is_empty():
        cursor = stack.pop()
        while not tmp.is_empty() and tmp.peek() > cursor:
            """
            如果是 peek 的結果是比較大，先暫存到原本的 stack
            """
            stack.push(tmp.pop())
        # 直到找到比較小的位置把原本要放的資料放到 tmp
        # 因為 tmp 都是照排序的反序暫存到 stack 會一直順順的推回所有的東西直到沒有排序
        # 時間複雜度是 O(n^2) 空間是 O(n)
        tmp.push(cursor)
    """
    最後要讓 tmp 是最上面是最大的
    倒回去原本的 stack 才會變成最上面最小
    """
    while not tmp.is_empty():
        stack.push(tmp.pop())


if __name__ == '__main__':
    s = Stack()
    s.push(3)
    s.push(2)
    s.push(5)
    s.push(6)
    s.push(7)
    s.push(10)
    s.push(9)
    s.push(8)
    s.push(1)
    s.push(4)
    
    sort_stack(s)
    for i in range(1, 11):
        assert i == s.pop()
