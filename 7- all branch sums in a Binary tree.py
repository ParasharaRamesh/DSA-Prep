class BinaryTree:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def branchSums(root):
    allPaths = []

    # pathsStack is (curr, path to curr)
    pathsStack = [(root, [root.value])]
    while len(pathsStack) != 0:
        currNode, currPath = pathsStack.pop()
        if currNode.right:
            pathsStack.append((currNode.right, currPath + [currNode.right.value]))
        if currNode.left:
            pathsStack.append((currNode.left, currPath + [currNode.left.value]))
        if not currNode.right and not currNode.left:
            #leaf
            allPaths.append(currPath)

    return list(map(lambda path: sum(path), allPaths))


if __name__ == "__main__":
    pass