class BinaryTree:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def invertBinaryTree(tree):
    if not tree:
        return None

    if not tree.left and not tree.right:
        return tree

    left = tree.left
    right = tree.right

    # swap it now
    tree.left = right
    tree.right = left

    # recurse
    invertBinaryTree(tree.left)
    invertBinaryTree(tree.right)

    # done mirroring all the way down
    return tree



