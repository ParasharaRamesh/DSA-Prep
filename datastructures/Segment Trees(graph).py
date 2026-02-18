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
    
    # alternative way to query which is easier to understand 
    def query_with_node(self, l, r, node=None):
        '''Query by walking the tree: pass root, then node.left / node.right. No dict lookup, no mid.'''
        if node is None:
            # technically we can even store only the root in the constructor if needed
            node = self.tree[(0, len(self.arr) - 1)]  # root
        start, end = node.start, node.end

        # no overlap
        if r < start or l > end:
            return float("inf")

        # complete overlap: we're at a real node, just use node.val
        if l <= start and end <= r:
            return node.val

        # partial: recurse on children (tree structure does the "split" for us)
        left_val = self.query_with_node(l, r, node.left)
        right_val = self.query_with_node(l, r, node.right)
        return self.range_func(left_val, right_val)

    def update(self, i, updated_value):
        '''
        find the leaf, from there repopulate the parents using parent pointers directly
        '''
        # directly updated that node
        self.tree[(i, i)].val = updated_value

        # now update the entire hierarchy
        curr = self.tree[(i, i)]

        while curr.parent != None:
            # curr would have been left or right
            curr.parent.val = self.range_func(curr.parent.left.val, curr.parent.right.val)

            curr = curr.parent

    def update_with_node(self, arr_index, new_val, node=None):
        '''
        Traverse down from root to leaf, update leaf, then refresh each node on the path
        using left/right children (no parent pointers). Same idea as the array version.

        This does not use the parent pointers directly, instead it uses the tree structure to find the node and update the path on the way back.
        '''
        if node is None:
            node = self.tree[(0, len(self.arr) - 1)]  # root
        start, end = node.start, node.end

        # not in range
        if arr_index < start or arr_index > end:
            return

        # found that leaf node where the start and end is actually the same as the array index
        if start == end:
            # leaf: update and return (path will be updated on unwind)
            node.val = new_val
            return

        mid = start + (end - start) // 2
        if arr_index <= mid:
            # update the left child since the array index to update is in the left subtree
            self.update_with_node(arr_index, new_val, node.left)
        else:
            # update the right child since the array index to update is in the right subtree
            self.update_with_node(arr_index, new_val, node.right)

        # on the way back: current node's value from its children
        node.val = self.range_func(node.left.val, node.right.val)

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
