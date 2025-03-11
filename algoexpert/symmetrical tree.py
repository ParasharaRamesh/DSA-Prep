class BinaryTree:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def symmetricalTree(tree):
    if not tree:
        return False
    return checkMirror(tree.left, tree.right)


def checkMirror(node1, node2):
    # both empty
    if not node1 and not node2:
        return True

    # one of it is empty
    if (not node1 and node2) or (node1 and not node2):
        return False

    # if the values don't match no point checking
    if node1.value != node2.value:
        return False

    return checkMirror(node1.left, node2.right) and checkMirror(node1.right, node2.left)
