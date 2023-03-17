
# This is an input class. Do not edit.
class LinkedList:
    def __init__(self, value):
        self.value = value
        self.next = None


def removeDuplicatesFromLinkedList(linkedList: LinkedList):
    curr = linkedList
    ahead = linkedList.next if linkedList and linkedList.next else None

    while ahead != None:
        if curr.value == ahead.value:
            curr.next = ahead.next
            ahead = ahead.next
        else:
            curr = curr.next
            ahead = ahead.next

    return linkedList


if __name__ == "__main__":
    pass

