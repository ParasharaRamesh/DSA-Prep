'''
Segment Trees are for range query problems in logarithmic time. By range it refers to the subarray.

left child = 2i + 1
right child = 2i + 2
parent = (i-1)//2

'''


class SegmentTree:
    def __init__(self, arr):
        self.arr = arr

        # apparently need 4n space
        self.tree = [float("inf")] * len(self.arr) * 4

        if len(arr) > 0:
            self.build(0, len(self.arr) - 1)
            print("Initialized segment tree")
        else:
            print("array is empty")

    def range_func(self, val1, val2):
        return min(val1, val2)

    def build(self, l, r, tree_index=0):
        '''
            l , r represent the indexes of the array
            tree_index always starts at 0 for root
        '''
        if l == r:
            self.tree[tree_index] = self.arr[l]
        else:
            mid = l + (r - l) // 2

            # build the left part
            left_index = 2 * tree_index + 1
            self.build(l, mid, left_index)

            # build the right part
            right_index = 2 * tree_index + 2
            self.build(mid + 1, r, right_index)

            # now combine the results
            self.tree[tree_index] = self.range_func(self.tree[left_index], self.tree[right_index])

    def query(self, l, r, tree_index=0, start=None, end=None):
        '''
        Tree_index = start with root so it will be 0,
        l,r = the range of the query passed ( will be passed down entirely)
        start, end will be the range of that tree node

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
            return self.tree[tree_index]

        # partial case (refer both paths)
        mid = start + (end - start) // 2

        # check left node
        left_tree_index = 2 * tree_index + 1
        left_query = self.query(l, r, left_tree_index, start, mid)

        # check right node
        right_tree_index = 2 * tree_index + 2
        right_query = self.query(l, r, right_tree_index, mid + 1, end)

        # combine the results
        return self.range_func(left_query, right_query)

    def update(self, arr_index, new_val, tree_index=0, start=None, end=None):
        '''
        arr_index = index of the array element to be updated
        new_val = value to be updated
        tree_index = always starts with 0 ( because it is the root)
        start, end = the range that particular tree index represnts

        find the leaf , update it and also ensure that its parent paths are also appropriately updated
        '''

        if start == None and end == None:
            start = 0
            end = len(self.arr) - 1

        # no need to go down this path
        if arr_index < start or arr_index > end:
            return

        # if you have reached the exact node needed to be modified
        if arr_index == start == end:
            self.tree[tree_index] = new_val
            return

        mid = start + (end - start) // 2
        left_tree_index = 2 * tree_index + 1
        right_tree_index = 2 * tree_index + 2

        if start <= arr_index and arr_index <= mid:
            # update and search in the left one
            self.update(arr_index, new_val, left_tree_index, start, mid)
        elif mid < arr_index and arr_index <= end:
            # update and search in the right one
            self.update(arr_index, new_val, right_tree_index, mid + 1, end)

        # now update the current node
        self.tree[tree_index] = self.range_func(self.tree[left_tree_index], self.tree[right_tree_index])


if __name__ == '__main__':
    arr = [0, 1, 2, 3, 4]
    tree = SegmentTree(arr)
    print("Finished tree building")

    # queries
    print(tree.query(1, 1))
    print(tree.query(1, 2))
    print(tree.query(1, 3))
    print(tree.query(2, 4))

    # updates
    print(tree.update(3, -1))
    print(tree.query(1, 4))
    print(tree.query(2, 3))
