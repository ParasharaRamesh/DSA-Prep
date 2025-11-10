'''
Segment Trees are for range query problems in logarithmic time. By range it refers to the subarray.

left child = 2i + 1
right child = 2i + 2
parent = (i-1)//2

'''
class SegmentTree:
    def __init__(self, arr):
        self.arr = arr

        # in case of Range Min it is if, in case of Range sum it can be 0
        # self.SPECIAL = float("inf")
        self.SPECIAL = 0

        # apparently need 4n space
        self.tree = [self.SPECIAL] * len(self.arr) * 4
        self.lazy = [self.SPECIAL] * len(self.arr) * 4

        if len(arr) > 0:
            self.build(0, len(self.arr) - 1)
            print("Initialized segment tree")
        else:
            print("array is empty")

    def range_func(self, val1, val2):
        # return min(val1, val2)
        return sum([val1, val2])

    def build(self, start, end, tree_index=0):
        '''
            start, end represent the indexes of the array
            tree_index always starts at 0 for root
        '''
        if start == end:
            self.tree[tree_index] = self.arr[start]
        else:
            mid = start + (end - start) // 2

            # build the left part
            left_index = 2 * tree_index + 1
            self.build(start, mid, left_index)

            # build the right part
            right_index = 2 * tree_index + 2
            self.build(mid + 1, end, right_index)

            # now combine the results
            self.tree[tree_index] = self.range_func(self.tree[left_index], self.tree[right_index])

    def query(self, l, r, tree_index=0, start=None, end=None):
        '''
        Tree_index = start with root so it will be 0,
        l,r = the range of the query passed ( will be passed down entirely)
        start, end will be the range of that tree node

        Three cases wrt a node's start,end when compared with the given range:
        1. No overlap with range: return some invalid token [l r Start End] or [Start End l r]
        2. Complete overlap with range (l, r): i.e.  [l  Start  End  r]: return as is
        3. Partial overlap with range: (l,r) is a subset of the node's (start, end) => [l <= Start <= r <= End] or [Start <= l <= End <= r]  or [Start, l, r, End]
        '''

        if start == None and end == None:
            start = 0
            end = len(self.arr) - 1

        # no overlap case
        if (r < start) or (l > end):
            return self.SPECIAL

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

    def range_update(self, l, r, val, tree_index=0, start=None, end=None):
        '''
        We are assuming that all nodes in this range of l-> r are all going to be incremented by val from their original values.
            * Idea is to maintain a parallel tree called lazy_tree which holds the updates needed for that node (along with their children)
            * For every node we visit, if at all it happened to have a lazy update value in that node; update it first and ask its children to get updated later on
            * same 3 cases here also, wrt a node's start,end
                a. if there is no overlap of the node in the range l,r : no need to update anything just return
                b. if there is a complete overlap of that node's start,end inside the l,r : update that node directly
                    - now this is interesting because this node might be responsible for a whole range of nodes under it (so instead of going all the way to each of the leave's and updating them we do the following)
                    - for this node's start -> end it is responsible for (end - start +1) #no of nodes
                    - since each of those node's will be updated, we can make a guesstimate of how this node will be updated (e.g. in case of range sum, all of the nodes will be added by "val" so the total new update
                        will be current value + (no of nodes under it) * val
                    - once this is done, we still need to update the leaves, but since we are lazy we can do it later, so just mark the lazy update value for its children ( and all of its children under it ) to be done by "val"
                    - this way when it is visited later on it will get updated correctly
                c. if there is partial overlap: just do it for the left and right one and then update the current node (baesd on those two values)

        If we really care for making sure that this lazy thing works even during querying. The lazy update can happen during one of the queries also so that way things are always in an upto date state
        '''
        pass

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
    # print(tree.update(3, -1))
    #
    # # testing the query again
    # print(tree.query(1, 4))
    # print(tree.query(2, 3))
