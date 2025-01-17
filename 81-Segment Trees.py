'''
Segment Trees are for range query problems in logarithmic time. By range it refers to the subarray.
'''


class SegmentTreeNode:
    def __init__(self, start, end, val=float("inf"), left=None, right=None, parent=None):
        self.start = start
        self.end = end
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent


class SegmentTree:
    def __init__(self, arr):
        self.arr = arr

        # storing it as adjacency tree with extra vars is easier than array [(l,r) => SegmentTreeNode object]
        self.tree = dict()

        # self.tree = [] # apparently size of 4n always suffices , but using dictionary is better

    def aggregate(self, val1, val2):
        '''
            this can change based on the problem but setting to min for now
        '''
        return min(val1, val2)

    def build(self, arr):
        '''
            build from the leaves as the leaves will be the individual elements and coming to the root will be the whole array.
            in case we are building it as an array the root will cover the entire array from (0,n-1) and its left and right indices will be 2i + 1 & 2i + 2.
        '''
        start = 0
        end = len(arr) - 1
        mid = start + (end - start) // 2

        # create root for the whole range
        root = SegmentTreeNode(start, end)

        if start == end:
            # base case (leaf)
            root.val = arr[mid]
        else:
            # left node (start -> mid)
            left_val = self.build(arr[start: mid + 1])
            left = SegmentTreeNode(start, mid, left_val, None, None, root)

            # right node (mid + 1 -> end)
            right_val = self.build(arr[mid + 1: end])
            right = SegmentTreeNode(mid + 1, end, right_val, None, None, root)

            # change the properties of the root
            root.left = left
            root.right = right
            root.val = self.aggregate(left_val, right_val)

        # save in segment tree
        self.tree[(start, end)] = root
        return root.val

    def query(self, l, r, start=None, end=None):
        '''
        Three cases wrt a node:
        1. No overlap with range: return some invalid token [l r start end] or [start end l r]
        2. Complete overlap with range (l, r): i.e.  [l  start  end  r]: return as is
        3. Partial overlap with range: (l,r) is a subset of the node's (start, end) => [l <= start <=r <= end] or [start <= l <= end <= r] => check both and return
        '''
        if start == None and end == None:
            start = 0
            end = len(self.arr) - 1

        # no overlap case
        if (r < start) or (l > end):
            return float("inf")

        # complete overlap case
        if (l <= start) and (end <= r):
            return self.tree[(start, end)]

        # partial case (refer both paths)
        mid = start + (end - start) // 2
        left_query = self.query(l, r, start, mid)
        right_query = self.query(l, r, mid + 1, end)
        return self.aggregate(left_query, right_query)

    def update(self, i, updated_value, start=None, end=None):
        '''
        find the leaf, from there repopulate the parents
        '''
        if start == None and end == None:
            start = 0
            end = len(self.arr) - 1

        # directly updated that node
        self.tree[(i, i)].val = updated_value

        # now update the entire hierarchy
        curr = self.tree[(i, i)]

        while curr.parent != None:
            #curr would have been left or right
            curr.parent.val = self.aggregate(curr.parent.left.val, curr.parent.right.val)

            curr = curr.parent

if __name__ == '__main__':
    pass
