class LinkedList:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __str__(self):
        return self.value


def findLoop(head):
    slow, fast = head, head

    #fast and slow trick
    while True:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            break


    #found the meeting point
    slow = head

    #init slow to head and move both one by one!
    while slow != fast:
        slow = slow.next
        fast = fast.next

    return slow


if __name__ == '__main__':
    zero = LinkedList(0)
    one = LinkedList(1)
    two = LinkedList(2)
    three = LinkedList(3)
    four = LinkedList(4)
    five = LinkedList(5)
    six = LinkedList(6)
    seven = LinkedList(7)
    eight = LinkedList(8)
    nine = LinkedList(9)

    nine.next = four

    zero.next = one
    one.next = two
    two.next = three
    three.next = four
    four.next = five
    five.next = six
    six.next = seven
    seven.next = eight
    eight.next = nine

    print(findLoop(zero))
