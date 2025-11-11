class BST:

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
        if value < self.value:
            if self.left:
                self.left = self.left.remove(value)
        elif value > self.value:
            if self.right:
                self.right = self.right.remove(value)
        else:
            # Found the node to delete
            if not self.left and not self.right:
                return None
            elif self.right:
                # Replace with in-order successor (min of right subtree)
                self.value = self._successor()
                self.right = self.right.remove(self.value)
            else:
                # No right child, replace with in-order predecessor (max of left)
                self.value = self._predecessor()
                self.left = self.left.remove(self.value)
        return self

    # One step right, then all the way left
    def _successor(self) -> int:
        node = self.right
        while node.left:
            node = node.left
        return node.value

    # One step left, then all the way right
    def _predecessor(self) -> int:
        node = self.left
        while node.right:
            node = node.right
        return node.value