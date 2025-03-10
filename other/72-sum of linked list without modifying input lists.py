# This is an input class. Do not edit.
class LinkedList:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        rep = ""
        while self:
            rep += f"{self.value}:->"
            self = self.next
        rep += "X"
        # print(rep)
        return rep

def goThroughTheRest(head, curr, one_before_curr, carry):
    while head:
        sum = head.value + carry
        units = sum % 10
        carry = sum // 10
        curr.value = units

        head = head.next
        curr.next = LinkedList(None)
        one_before_curr = curr
        curr = curr.next

    return head, curr, one_before_curr, carry


def sumOfLinkedLists(linkedListOne, linkedListTwo):
    # first make a blank linked list
    curr = LinkedList(None)
    one_before_curr = curr
    head = curr

    carry = 0
    one = linkedListOne
    two = linkedListTwo

    while one and two:
        sum = one.value + two.value + carry
        units = sum % 10
        carry = sum // 10

        curr.value = units
        curr.next = LinkedList(None)
        one_before_curr = curr
        curr = curr.next

        one = one.next
        two = two.next

    # if one is finished earlier
    oneIsOver = (one == None)
    twoIsOver = (two == None)

    if oneIsOver and not twoIsOver:
        two, curr, one_before_curr, carry = goThroughTheRest(two, curr, one_before_curr, carry)
    elif not oneIsOver and twoIsOver:
        one, curr, one_before_curr, carry = goThroughTheRest(one, curr, one_before_curr, carry)

    # if both are finished
    if not one and not two and carry > 0:
        curr.value = carry
    elif not one and not two and carry == 0:
        # cut the last one
        one_before_curr.next = None

    return head


if __name__ == '__main__':
    '''
    #1. Both finish together
    
    # one is 321
    one_1 = LinkedList(1)
    one_2 = LinkedList(2)
    one_3 = LinkedList(3)

    one_1.next = one_2
    one_2.next = one_3

    # two is 947
    two_1 = LinkedList(7)
    two_2 = LinkedList(4)
    two_3 = LinkedList(5)

    two_1.next = two_2
    two_2.next = two_3
    # sum should be 868
    '''

    '''
    #2. Both finish together with carry inbtn
    # one is 321
    one_1 = LinkedList(1)
    one_2 = LinkedList(2)
    one_3 = LinkedList(3)

    one_1.next = one_2
    one_2.next = one_3

    # two is 479
    two_1 = LinkedList(9)
    two_2 = LinkedList(7)
    two_3 = LinkedList(4)

    two_1.next = two_2
    two_2.next = two_3
    # sum should be 800
    '''

    '''
    #3. Both finish together with carry in end
    # one is 321
    one_1 = LinkedList(1)
    one_2 = LinkedList(2)
    one_3 = LinkedList(3)

    one_1.next = one_2
    one_2.next = one_3

    # two is 979
    two_1 = LinkedList(9)
    two_2 = LinkedList(7)
    two_3 = LinkedList(9)

    two_1.next = two_2
    two_2.next = two_3
    # sum should be 1300
    '''

    # '''
    #4. Two finishes first, and one needs to continue
    # one is 1742
    one_1 = LinkedList(2)
    one_2 = LinkedList(4)
    one_3 = LinkedList(7)
    one_4 = LinkedList(1)

    one_1.next = one_2
    one_2.next = one_3
    one_3.next = one_4

    # two is 549
    two_1 = LinkedList(9)
    two_2 = LinkedList(4)
    two_3 = LinkedList(5)

    two_1.next = two_2
    two_2.next = two_3
    #sum should be 2291
    # '''

    '''
    # 5. One finishes first and two needs to continue
    # one is 549
    one_1 = LinkedList(9)
    one_2 = LinkedList(4)
    one_3 = LinkedList(5)

    one_1.next = one_2
    one_2.next = one_3

    # two is 1742
    two_1 = LinkedList(2)
    two_2 = LinkedList(4)
    two_3 = LinkedList(7)
    two_4 = LinkedList(1)

    two_1.next = two_2
    two_2.next = two_3
    two_3.next = two_4

    #sum should be 2291
    '''

    ans = sumOfLinkedLists(one_1, two_1)
    print(ans)
