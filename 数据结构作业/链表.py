class Node:
    def __init__(self, data: int | str | float):
        self.data = data
        self.next : Node | None = None
    def __repr__(self) -> str:
        return f"Node({self.data!r})"

class LinkedList:
    def __init__(self):
        self.head : Node | None = None
    
    def append(self, data: int | str | float):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node
    
    def __repr__(self) -> str:
        nodes = []
        current = self.head
        while current:
            nodes.append(repr(current))
            current = current.next
        return " -> ".join(nodes)
    def delete(self,index: int):
        current = self.head
        if index == 0:
            if self.head:
                self.head = self.head.next
                return
            else:
                self.head = None
                return
        current = self.head
        while True:
            if index == 0:
                if not current.next:
                    return None
                else:
                    last.next = current.next
                    return 
            index -= 1
            if not current.next:
                return None
            last=current
            current = current.next

# 方式1：直接创建节点并连接
node_1 = Node(10)
node_2 = Node(20) 
node_3 = Node(30)
node_1.next = node_2
node_2.next = node_3

# 创建一个链表，将head指向第一个节点
list_1 = LinkedList()
list_1.head = node_1
print(f"链表1: {list_1}")  

list_1.append(40)
print(f"链表1: {list_1}")

list_1.delete(1)
print(f"链表1: {list_1}")
