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

    def __str__(self):
        return f"Node(start={self.start}, end={self.end}, val={self.val}, parent={self.parent}, left={self.left}, right={self.right})"

class SegmentTree:
    def __init__(self, arr):
        self.arr = arr

        # storing it as adjacency tree with extra vars is easier than array [(l,r) => SegmentTreeNode object]
        self.tree = dict()

        if len(arr) > 0:
            self.build(0, len(self.arr) - 1)
            print("Initialized segment tree")
        else:
            print("array is empty")

    def range_func(self, val1, val2):
        return min(val1, val2)

    def build(self, start, end):
        '''
            build from the leaves as the leaves will be the individual elements and coming to the root will be the whole array.
            in case we are building it as an array the root will cover the entire array from (0,n-1) and its left and right indices will be 2i + 1 & 2i + 2.
        '''
        if start == end:
            # base case (leaf)
            leaf = SegmentTreeNode(start, end, val=self.arr[start])
            self.tree[(start, end)] = leaf
            return leaf

        # create node
        node = SegmentTreeNode(start, end)

        mid = start + (end - start) // 2

        # left node (start -> mid)
        left_node = self.build(start, mid)
        left_node.parent = node

        # right node (mid + 1 -> end)
        right_node = self.build(mid + 1, end)
        right_node.parent = node

        # change the properties of the root
        node.left = left_node
        node.right = right_node
        node.val = self.range_func(left_node.val, right_node.val)

        # save in tree
        self.tree[(start, end)] = node
        return node

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
            return self.tree[(start, end)].val

        # partial case (refer both paths)
        mid = start + (end - start) // 2
        left_query = self.query(l, r, start, mid)
        right_query = self.query(l, r, mid + 1, end)
        return self.range_func(left_query, right_query)

    def update(self, i, updated_value):
        '''
        find the leaf, from there repopulate the parents
        '''
        # directly updated that node
        self.tree[(i, i)].val = updated_value

        # now update the entire hierarchy
        curr = self.tree[(i, i)]

        while curr.parent != None:
            # curr would have been left or right
            curr.parent.val = self.range_func(curr.parent.left.val, curr.parent.right.val)

            curr = curr.parent


if __name__ == '__main__':
    arr = [0, 1, 2, 3, 4]
    tree = SegmentTree(arr)
    print("Finished tree building")

    #queries
    # print(tree.query(1, 1))
    # print(tree.query(1, 2))
    # print(tree.query(1, 3))

    #updates
    print(tree.update(3, -1))
    print(tree.query(1, 4))
