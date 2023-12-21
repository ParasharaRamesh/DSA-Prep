# This is an input class. Do not edit.
class BinaryTree:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def mergeBinaryTrees(tree1, tree2):
    if not tree1:
        return tree2

    if not tree2:
        return tree1

    if not tree1 and not tree2:
        return None

    mergedValue = tree1.value + tree2.value
    merged = BinaryTree(mergedValue)

    #now go left in both tree1 and tree2
    merged.left = mergeBinaryTrees(tree1.left, tree2.left)

    #now go right in both tree1 and tree2
    merged.right = mergeBinaryTrees(tree1.right, tree2.right)

    return merged


if __name__ == '__main__':
    pass
    # result = mergeBinaryTrees(tree1, tree2)