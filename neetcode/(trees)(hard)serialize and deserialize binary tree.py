'''
Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.

Clarification: The input/output format is the same as how LeetCode serializes a binary tree. You do not necessarily need to follow this format, so please be creative and come up with different approaches yourself.



Example 1:


Input: root = [1,2,3,null,null,4,5]
Output: [1,2,3,null,null,4,5]
Example 2:

Input: root = []
Output: []


Constraints:

The number of nodes in the tree is in the range [0, 104].
-1000 <= Node.val <= 1000
'''


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


# this approach gave MLE after 52/54, going to try a different approach :(!
class Codec_memory_limit_exceeded:
    '''
    # thought this could help in defining the size of the array as 4n, similar to segment tree
    def count(self, root):
        if not root:
            return 0

        return 1 + self.count(root.left) + self.count(root.right)
    '''

    def serialize(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """
        # n = self.count(root)
        # res = [None]*8*n

        res = []

        def add_to_res(i, val):
            # if that index exists add it, if not add None's in the end to match it
            if len(res) == 0:
                res.append(val)
            elif i < len(res):
                res[i] = val
            else:
                j = len(res) - 1

                while j < i:
                    res.append(None)
                    j += 1

                res[i] = val

        def helper(root, i):
            if root:
                # res[i] = root.val
                add_to_res(i, root.val)
                helper(root.left, 2*i+1)
                helper(root.right, 2*i+2)
            else:
                # res[i] = None
                add_to_res(i, None)

        # serialize it
        helper(root, 0)

        #remove all the Nones in the end
        while res and res[-1] == None:
            res.pop()

        res = list(map(lambda x: str(x), res))
        return ",".join(res)

    def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """
        if data == "":
            return None

        arr = data.split(",")
        n = len(arr)

        def helper(i):
            if i < n:
                if arr[i] != "None":
                    val = int(arr[i])
                    root = TreeNode(val)
                else:
                    return None

                left = helper(2*i + 1)
                right = helper(2*i + 2)

                root.left = left
                root.right = right

                return root

            return None

        return helper(0)

# using preorder traversal
class Codec:
    def serialize(self, root):
        res = []

        def dfs(node):
            if not node:
                res.append("N")
                return
            res.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(res)

    def deserialize(self, data):
        """Decodes your encoded data to tree.
        :type data: str
        :rtype: TreeNode
        """

        def dfs(l):
            """ a recursive helper function for deserialization."""
            if l[0] == 'N':
                l.pop(0)
                return None

            root = TreeNode(l[0])
            l.pop(0)

            root.left = dfs(l)
            root.right = dfs(l)

            return root

        data_list = data.split(',')
        root = dfs(data_list)
        return root

if __name__ == '__main__':
    c = Codec()

    one = TreeNode(1)
    two = TreeNode(2)
    three = TreeNode(3)
    four = TreeNode(4)
    five = TreeNode(5)

    one.left = two
    one.right = three
    three.left = four
    three.right = five

    serialized = c.serialize(one)
    deserialized = c.deserialize(serialized)
    print(deserialized)