import math

class BST:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def checkNodeValidity(tree, lower, upper):
    if not tree:
        return True

    if tree.value < lower or tree.value >= upper:
        return False

    isLeftValid = checkNodeValidity(tree.left, lower, tree.value)
    isRightValid = checkNodeValidity(tree.right, tree.value, upper)

    return isLeftValid and isRightValid


def validateBst(tree):
    lower = -math.inf
    upper = math.inf
    return checkNodeValidity(tree, lower, upper)
