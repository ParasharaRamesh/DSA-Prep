class BST:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

currClosest = None

def findClosestValueInBst(tree, target):
    global currClosest

    if currClosest == None:
        #init
        currClosest = tree.value
    elif abs(tree.value - target) <= abs(currClosest - target):
        currClosest = tree.value

    if tree.value == target:
        #closest by 0
        currClosest = tree.value
        return currClosest

    if tree.left and tree.value > target:
        return findClosestValueInBst(tree.left, target)

    if tree.right and tree.value < target:
        return findClosestValueInBst(tree.right, target)

    return tree.value if abs(tree.value - target) <= abs(currClosest - target) else currClosest

if __name__ == "__main__":
    pass