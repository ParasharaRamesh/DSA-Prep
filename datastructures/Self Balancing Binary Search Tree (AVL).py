'''
1. What is balance factor?:
- @ any node = height(node.left) - height(node.right)
- bf = 0 => both subtrees are balanced
- bf = 1 => balanced, but left side has one more
- bf = -1 => balanced, but right side has one more
- if the bf is not {-1,0,1} then it is imbalanced

2. What are the different types of imbalances?

. There are mainly 4 imbalances (LL, RR, LR, RL)

3. For each type of imbalance we just rotate and rebalance it

For more theory refer to my notion notes
'''
from typing import Optional


class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class AVLTree:
    def __init__(self):
        self.root = None  # Start with an empty tree

    def get_height(self, node: TreeNode) -> int:
        if node is None:
            return 0
        return 1 + max(self.get_height(node.left), self.get_height(node.right))
    def get_balance_factor(self, node: TreeNode) -> int:
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    # In case of LL imbalance (left heavy, bf > 1) => we do a right rotate from the node's left as pivot
    def right_rotate(self, unbalanced_node: TreeNode) -> Optional[TreeNode]:
        # unbalanced node's right subtree stays the same all throughout!

        left_child = unbalanced_node.left
        left_right_subtree = left_child.right

        # Perform rotation
        left_child.right = unbalanced_node
        unbalanced_node.left = left_right_subtree

        # Return new root after rotation
        return left_child

    # In case of RR imbalance (right heavy, bf < -1) => we do a left rotate from the node's right as pivot
    def left_rotate(self, unbalanced_node: TreeNode) -> Optional[TreeNode]:
        #unbalanced node's left subtree stays as is

        right_child = unbalanced_node.right
        right_left_subtree = right_child.left

        # Perform rotation
        right_child.left = unbalanced_node
        unbalanced_node.right = right_left_subtree

        # Return the new root after rotation
        return right_child

    # In case of LR imbalance => tackle it in reverse order => handle the R imbalance of the left child first to make it into -> LL case and then do right rotation to fix that
    def left_right_rotate(self, unbalanced_node: TreeNode) -> Optional[TreeNode]:
        #handle in reverse order
        unbalanced_node.left = self.left_rotate(unbalanced_node.left)

        # after this it has become the LL case so do right rotate
        return self.right_rotate(unbalanced_node)

    # in case of RL imbalance => handle the L imbalance of the right child first to make it into -> RR case and then do left rotation to fix that
    def right_left_rotate(self, unbalanced_node: TreeNode) -> Optional[TreeNode]:
        # handle in reverse order
        unbalanced_node.right = self.right_rotate(unbalanced_node.right)

        #now the same case as RR imbalance
        return self.left_rotate(unbalanced_node)

    # will take care of any imbalance (anywhere)
    def balanceBST(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None

        root.left = self.balanceBST(root.left)
        root.right = self.balanceBST(root.right)

        # check balance factors
        root_bf = self.get_balance_factor(root)

        if abs(root_bf) <= 1:
            return root
        if root_bf > 1:
            # Node is left-heavy.
            left = root.left
            if self.get_height(left.left) >= self.get_height(left.right):
                # LL Case: Left child is left-heavy or balanced
                root = self.right_rotate(root)
            else:
                # LR Case: Left child is right-heavy
                root = self.left_right_rotate(root)
        elif root_bf < 1:
            # Node is right-heavy.
            right = root.right
            if self.get_height(right.right) >= self.get_height(right.left):
                # RR Case: Right child is right-heavy or balanced
                root = self.left_rotate(root)
            else:
                # RL Case: Right child is left-heavy
                root = self.right_left_rotate(root)

        return self.balanceBST(root)

    # insert it in the correct place first, and then find out the imbalance if any and the rotate and balance it
    def insert(self, val: int):
        #helper function to recursively find the place to insert and then rotate it appropriately
        def helper(node: Optional[TreeNode], val: int) -> TreeNode:
            # Base case: insert new node, since we have reached the point where it needs to be added
            if not node:
                return TreeNode(val)

            # BST insertion (duplicates go to right), assume that it has been insrted somewhere
            if val < node.val:
                node.left = helper(node.left, val)
            else:
                node.right = helper(node.right, val)

            # not using the rebalance function here, since we are doing this bottom up
            balance = self.get_balance_factor(node)

            # LL Case: Left heavy on the left side
            if balance > 1 and self.get_balance_factor(node.left) > 1:
                return self.right_rotate(node)

            # LR Case: right heavy on the right side
            if balance > 1 and self.get_balance_factor(node.left) < -1:
                return self.left_right_rotate(node)

            # RR Case: Right heavy on the right side
            if balance < -1 and self.get_balance_factor(node.right) < -1:
                return self.left_rotate(node)

            # RL Case: left heavy on the right side
            if balance < -1 and self.get_balance_factor(node.right) > 1:
                return self.right_left_rotate(node)

            # If no balancing needed, return the node
            return node

        self.root = helper(self.root, val)

    def delete(self, val: int):
        def helper(node: Optional[TreeNode], val: int) -> TreeNode:
            if not node:
                return None

            # Step 1: BST deletion logic, assume that we get already go and get it deleted
            if val < node.val:
                node.left = helper(node.left, val)
            elif val > node.val:
                node.right = helper(node.right, val)
            else:
                # This is the node to be deleted
                if not node.left and not node.right:
                    return None  # No children
                elif not node.left:
                    return node.right  # Only right child
                elif not node.right:
                    return node.left  # Only left child
                else:
                    # Node has two children: replace with in-order successor (min in right)
                    successor = node.right
                    while successor.left:
                        successor = successor.left
                    node.val = successor.val  # Replace value
                    node.right = helper(node.right, successor.val)  # Delete the successor

            # Step 2: Balance the current node
            balance = self.get_balance_factor(node)

            # LL Case
            if balance > 1 and self.get_balance_factor(node.left) >= 0:
                return self.right_rotate(node)

            # LR Case
            if balance > 1 and self.get_balance_factor(node.left) < 0:
                return self.left_right_rotate(node)

            # RR Case
            if balance < -1 and self.get_balance_factor(node.right) <= 0:
                return self.left_rotate(node)

            # RL Case
            if balance < -1 and self.get_balance_factor(node.right) > 0:
                return self.right_left_rotate(node)

            return node

        self.root = helper(self.root, val)