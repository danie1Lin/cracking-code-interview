import unittest
from ch02.linked_list import LinkedNode


# only access to that node
def delete_middle(target: LinkedNode):
    if not target.next:
        return False
    # 因為沒有給前面的節點所以唯一的辦法是複製下一個的值過來，然後刪掉下一個
    target.value = target.next.value
    target.next = target.next.next
    
    

class TestDeleteMiddle(unittest.TestCase):
    def test(self):
        root = LinkedNode('a', LinkedNode('b', LinkedNode('c', LinkedNode('d', LinkedNode('e', LinkedNode('f'))))))
        delete_node = root.next.next
        delete_middle(delete_node)
        self.assertTrue(root.total_eq(LinkedNode('a', LinkedNode('b',  LinkedNode('d', LinkedNode('e', LinkedNode('f')))))
)) 

if __name__ == '__main__':
    unittest.main()
