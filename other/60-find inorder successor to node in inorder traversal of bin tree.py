class BinaryTree:
    def __init__(self, value, left=None, right=None, parent=None):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent

# find inorder successor to node if parent pointers are also there, if last then return None
def findSuccessor(tree, node):
    # if node has a right subtree, then find its left most node
    if node.right:
        curr = node.right
        while curr:
            if not curr.left:
                # if left doesnt exist stop there!
                break
            curr = curr.left

        # this is the next one
        return curr

    # else , keep going up until a point where the curr is in the left side of the parent
    curr = node
    while curr:
        if curr.parent and curr.parent.left == curr:
            # is curr in the left sub tree?
            return curr.parent
        curr = curr.parent

    # if you reach last then None is the return answer
    return None