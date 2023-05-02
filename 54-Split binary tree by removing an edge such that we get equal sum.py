class BinaryTree:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right



#cache everything as we go
def sum(node):
    sumCache = dict()

    def summation(node):
        if node == None:
            return 0

        left = str(node.left.value) if node.left else "*"
        right = str(node.right.value) if node.right else "*"
        nodeId = f"{node.value}|{left}|{right}|{str(id(node))}"
        if nodeId in sumCache:
            return sumCache[nodeId]

        sumCache[nodeId] = node.value + sum(node.left) + sum(node.right)

        return sumCache[nodeId]

    return summation(node)

def splitBinaryTree(tree):
    total = sum(tree)

    if total % 2 == 1:
        return 0

    #its possible to split it
    half = total // 2

    #now have to traverse each node and try out sum
    q = []

    if tree.left:
        q.append(tree.left)

    if tree.right:
        q.append(tree.right)

    while q:
        node = q.pop()
        nodeSum = sum(node)

        if nodeSum == half:
            return nodeSum
        else:
            if node.left:
                q.append(node.left)

            if node.right:
                q.append(node.right)

    #not possible at all!
    return 0


if __name__ == '__main__':
    one = BinaryTree(1)
    three = BinaryTree(3)
    negTwo = BinaryTree(-2)
    six = BinaryTree(6)
    negFive = BinaryTree(-5)
    five = BinaryTree(5)
    two = BinaryTree(2)
    otherTwo = BinaryTree(2)

    one.left = three
    one.right = negTwo

    three.left = six
    three.right = negFive
    six.left = two

    negTwo.left = five
    negTwo.right = otherTwo

    print(splitBinaryTree(one))