class BinaryTree:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def binaryTreeDiameter(tree):
    '''
    #Edges not nodes

    a. root + maxDepth on left + maxDepth on right
    b. diamater(left)
    c. diameter(right)
    '''
    if not tree or (not tree.left and not tree.right):
        #empty tree or a single node both cases diameter is 0
        return 0

    linkThroughRoot = 0

    if tree.left:
        linkThroughRoot += maxDepth(tree.left) + 1

    if tree.right:
        linkThroughRoot += maxDepth(tree.right) + 1

    return max(
        linkThroughRoot,
        binaryTreeDiameter(tree.left),
        binaryTreeDiameter(tree.right)
    )

def maxDepth(tree):
    if not tree or (not tree.left and not tree.right):
        # empty tree or a single node both cases depth is 0
        return 0

    leftDepth = 0
    rightDepth = 0

    if tree.left:
        leftDepth = maxDepth(tree.left) + 1

    if tree.right:
        rightDepth = maxDepth(tree.right) + 1

    return max(leftDepth, rightDepth)

if __name__ == '__main__':
    pass
