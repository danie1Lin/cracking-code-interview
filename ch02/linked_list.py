class LinkedNode:
    def __init__(self, value, n=None) -> None:
        self.value = value
        self.next = n

    def __eq__(self, __o: object) -> bool:
        if __o == None:
            return False
        return self.value == __o.value

    def total_eq(self, node)-> bool:
        node_equal = self == node
        next_equal = False
        if self.next and node.next:
            next_equal = self.next.total_eq(node.next) 
        elif not self.next and not node.next:
            next_equal = True
        return next_equal and node_equal

    def __repr__(self):
        s = f"list: {self.value}"
        c = self.next
        while c:
            s += f" -> {c.value}"
            c = c.next
        return s
