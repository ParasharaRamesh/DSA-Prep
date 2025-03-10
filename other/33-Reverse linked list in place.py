class LinkedList:
    def __init__(self, value):
        self.value = value
        self.next = None


def reverseLinkedList(head: LinkedList):
    last = findLastNode(head)
    reverse(head)
    #new tail
    head.next = None
    return last


def findLastNode(head):
    curr = head
    while curr.next:
        curr = curr.next
    return curr


def reverse(head):
    if not head or not head.next:
        return

    next = head.next
    reverse(head.next)
    next.next = head



if __name__ == '__main__':
    one = LinkedList(1)
    two = LinkedList(2)
    three = LinkedList(3)
    four = LinkedList(4)

    one.next = two
    two.next = three
    three.next = four

    reverseLinkedList(one)
