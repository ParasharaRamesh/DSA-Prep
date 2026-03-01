'''
Given a list of accounts where each element accounts[i] is a list of strings, where the first element accounts[i][0] is a name, and the rest of the elements are emails representing emails of the account.

Now, we would like to merge these accounts. Two accounts definitely belong to the same person if there is some common email to both accounts. Note that even if two accounts have the same name, they may belong to different people as people could have the same name. A person can have any number of accounts initially, but all of their accounts definitely have the same name.

After merging the accounts, return the accounts in the following format: the first element of each account is the name, and the rest of the elements are emails in sorted order. The accounts themselves can be returned in any order.

Example 1:

Input: accounts = [
    ["neet","neet@gmail.com","neet_dsa@gmail.com"],
    ["alice","alice@gmail.com"],
    ["neet","bob@gmail.com","neet@gmail.com"],
    ["neet","neetcode@gmail.com"]
]

Output: [["neet","bob@gmail.com","neet@gmail.com","neet_dsa@gmail.com"],["alice","alice@gmail.com"],["neet","neetcode@gmail.com"]]
Example 2:

Input: accounts = [
    ["James","james@mail.com"],
    ["James","james@mail.co"]
]

Output: [["James","james@mail.com"],["James","james@mail.co"]]
Constraints:

1 <= accounts.length <= 1000
2 <= accounts[i].length <= 10
1 <= accounts[i][j].length <= 30
accounts[i][0] consists of English letters.
accounts[i][j] (for j > 0) is a valid email.

'''

from typing import List
from collections import *

class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        email_to_name = dict()
        uf = UnionFind()

        for items in accounts:
            name = items[0]
            emails = items[1:]

            for email in emails:
                email_to_name[email] = name
                uf.create(email)

        for items in accounts:
            emails = items[1:]

            for i in range(len(emails) - 1):
                print(f"union {emails[i]} <-> {emails[i+1]}")
                uf.union(emails[i], emails[i+1])

        components = uf.get_connected_components()
        
        res = []
        for connected in components:
            name = email_to_name[connected[0]]
            connected.appendleft(name)

            res.append(list(connected))

        return res


class UnionFind():
    """
    Similar to UF by rank, instead of keeping track of the rank you can keep track of the size of components inside one connected component
    """
    def __init__(self):
        self.parent = {}
        self.size = {}

    def create(self, value):
        """Create a standalone set and initialize rank to 0."""
        if value not in self.parent:
            self.parent[value] = None
            self.size[value] = 1 # there is one node in its own connected component so far

    def find(self, value):
        """
        Find the root representative without path compression.
        * Traverse up the tree until we reach the topmost node (None)
        * Return the parent/root. Which is that node which has a parent pointer as None (almost like linked list traversal)
        """
        if value not in self.parent:
            return None
        curr = value
        while self.parent[curr] is not None:
            curr = self.parent[curr]
        return curr

    def union(self, a, b):
        """Merge by size: attach smaller-size tree under larger-size tree."""
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a is None or root_b is None or root_a == root_b:
            return

        size_a = self.size.get(root_a, 0)
        size_b = self.size.get(root_b, 0)

        if size_a <= size_b:
            # make a's parent as b because a is smaller
            self.parent[root_a] = root_b
            self.size[root_b] += self.size[root_a]
        elif size_a > size_b:
            self.parent[root_b] = root_a
            self.size[root_a] += self.size[root_b]

    def get_connected_components(self) :
        components = defaultdict(set)

        print(self.parent)
        for node in self.parent:
            parent = self.find(node)
            components[parent].add(node)

        all_components = components.values()
        return list(map(lambda connected: deque(sorted(connected)), all_components))
