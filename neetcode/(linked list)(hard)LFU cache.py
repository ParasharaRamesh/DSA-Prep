from collections import defaultdict

'''
Main idea is that for each usage count we maintain a doubly linked list so that we know the order i.e. the LRU
we also maintain lfuCnt -> which doubly linked list do we need to look at
valMap -> actual key value dict
countMap -> usage count of each key
'''

class ListNode:

    def __init__(self, val, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next

class LinkedList:

    def __init__(self):
        self.left = ListNode(0)
        self.right = ListNode(0, self.left)
        self.left.next = self.right
        self.map = {}

    def length(self):
        return len(self.map)

    def pushRight(self, val):
        node = ListNode(val, self.right.prev, self.right)
        self.map[val] = node
        self.right.prev = node
        node.prev.next = node

    def pop(self, val):
        if val in self.map:
            node = self.map[val]
            next, prev = node.next, node.prev
            next.prev = prev
            prev.next = next
            self.map.pop(val, None)

    def popLeft(self):
        res = self.left.next.val
        self.pop(self.left.next.val)
        return res

    def update(self, val):
        self.pop(val)
        self.pushRight(val)

class LFUCache:

    def __init__(self, capacity: int):
        self.cap = capacity
        self.lfuCnt = 0
        self.valMap = {} # Map key -> val
        self.countMap = defaultdict(int) # Map key -> count
        # Map count of key -> linkedlist
        self.listMap = defaultdict(LinkedList)

    def counter(self, key):
        cnt = self.countMap[key]
        self.countMap[key] += 1
        self.listMap[cnt].pop(key)
        self.listMap[cnt + 1].pushRight(key)

        if cnt == self.lfuCnt and self.listMap[cnt].length() == 0:
            self.lfuCnt += 1


    def get(self, key: int) -> int:
        if key not in self.valMap:
            return -1
        self.counter(key)
        return self.valMap[key]

    def put(self, key: int, value: int) -> None:
        if self.cap == 0:
            return

        if key not in self.valMap and len(self.valMap) == self.cap:
            res = self.listMap[self.lfuCnt].popLeft()
            self.valMap.pop(res)
            self.countMap.pop(res)

        self.valMap[key] = value
        self.counter(key)
        self.lfuCnt = min(self.lfuCnt, self.countMap[key])