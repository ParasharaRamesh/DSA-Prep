from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __str__(self):
        curr = self
        result = ""
        while curr:
            result += f"{curr.val} -> "
            curr = curr.next
        return result

class Solution:
    '''
    K < length of list
    whatever is left out we shouldn't reverse it!
    '''
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if head:
            curr = head
            nextGroupHead, kNodesExist = self.findKsNextNodeFrom(curr, k)
            currGroupHead, currGroupTail = None, None

            if kNodesExist:
                #if a group of k can be formed reverse it!
                currGroupHead = self.reverseUptoNodeAndReturnNewHead(curr, nextGroupHead)
                currGroupTail = self.findLastNode(currGroupHead)
                currGroupTail.next = self.reverseKGroup(nextGroupHead, k)
                return currGroupHead

            # left out ones should not be reversed!
            return head

        return None

    def findKsNextNodeFrom(self, curr, k):
        count = 1
        while curr and count <= k:
            curr = curr.next
            count += 1
        return curr, count - 1 == k

    def reverseUptoNodeAndReturnNewHead(self, head, stop):
        last = self.findLastNodeBeforeNode(head, stop)
        self.reverseInPlace(head, last)
        #new tail therefore set it to empty
        head.next = None
        #return new head
        return last

    def findLastNodeBeforeNode(self, head, stop):
        curr = head
        while curr.next != stop:
            curr = curr.next
        return curr

    def findLastNode(self, head):
        curr = head
        while curr.next:
            curr = curr.next
        return curr

    def reverseInPlace(self, head, last):
        if not head or not head.next or head == last:
            return

        next = head.next
        self.reverseInPlace(head.next, last)
        next.next = head


if __name__ == '__main__':
    one = ListNode(1)
    two = ListNode(2)
    three = ListNode(3)
    four = ListNode(4)
    five = ListNode(5)

    one.next = two
    two.next = three
    three.next = four
    four.next = five

    s = Solution()
    k = 2
    head = one
    new = s.reverseKGroup(head, k)
    print(new)
