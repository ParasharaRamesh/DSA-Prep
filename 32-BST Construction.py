class BST:
    leftDirection = "LEFT"
    rightDirection = "RIGHT"

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    # main
    def insert(self, value):
        if value < self.value:
            if self.left:
                self.left.insert(value)
            else:
                self.left = BST(value)
        else:
            if self.right:
                self.right.insert(value)
            else:
                self.right = BST(value)

        return self

    def contains(self, value):
        if not self:
            return False

        if value == self.value:
            return True
        elif value > self.value and self.right:
            return self.right.contains(value)
        elif self.left:
            return self.left.contains(value)

        return False

    def remove(self, value):
        # replace root with left ka rightmost or right ka leftmost
        path = []
        if self.contains(value):
            self.removeUtil(value, path)
        return self

    # helper
    def removeUtil(self, value, path):
        if value == self.value:
            # get replacement element
            if self.right:
                path.append([self, BST.rightDirection])
                self.value = self.right.getAndRemoveLeftMostElement(path)
            elif self.left:
                path.append([self, BST.leftDirection])
                self.value = self.left.getAndRemoveRightMostElement(path)
            elif len(path) > 0:
                # non root case as if it is root we can just skip it
                parent, direction = path[-1]
                if direction == BST.rightDirection:
                    parent.right = None
                elif direction == BST.leftDirection:
                    parent.left = None
        elif value > self.value:
            path.append([self, BST.rightDirection])
            self.right.removeUtil(value, path)
        else:
            path.append([self, BST.leftDirection])
            self.left.removeUtil(value, path)

    def getAndRemoveLeftMostElement(self, path):
        if self.left:
            #go as much left as possible
            path.append([self, BST.leftDirection])
            return self.left.getAndRemoveLeftMostElement(path)
        else:
            #at this point there may be a right child, but we have to remove this node only
            value = self.value

            #connect parent to self's right this will remove the node automatically
            parent,direction = path[-1]

            if direction == BST.leftDirection:
                parent.left = self.right
            else:
                parent.right = self.right

            return value


    def getAndRemoveRightMostElement(self, path):
        if self.right:
            path.append([self, BST.rightDirection])
            return self.right.getAndRemoveRightMostElement(path)
        else:
            # at this point there may be a left child, but we have to remove this node only
            value = self.value

            # connect parent to self's left this will remove the node automatically
            parent, direction = path[-1]

            if direction == BST.leftDirection:
                parent.left = self.left
            else:
                parent.right = self.left

            return value