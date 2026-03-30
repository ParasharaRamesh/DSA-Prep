'''
Leetcode 2840.

You are given two strings s1 and s2, both of length n, consisting of lowercase English letters.

You can apply the following operation on any of the two strings any number of times:

Choose any two indices i and j such that i < j and the difference j - i is even, then swap the two characters at those indices in the string.
Return true if you can make the strings s1 and s2 equal, and false otherwise.

 

Example 1:

Input: s1 = "abcdba", s2 = "cabdab"
Output: true
Explanation: We can apply the following operations on s1:
- Choose the indices i = 0, j = 2. The resulting string is s1 = "cbadba".
- Choose the indices i = 2, j = 4. The resulting string is s1 = "cbbdaa".
- Choose the indices i = 1, j = 5. The resulting string is s1 = "cabdab" = s2.
Example 2:

Input: s1 = "abe", s2 = "bea"
Output: false
Explanation: It is not possible to make the two strings equal.
 

Constraints:

n == s1.length == s2.length
1 <= n <= 105
s1 and s2 consist only of lowercase English letters.
'''

'''
Thoughts:

need a linear, or nlogn kind of solution 
    - just check the parities and if the frequencies are same then its possible
    - trivial case of frequencies not matching -> false
bfs -> X
    - there should be a lot of ways to choose 2 indices such that diff is even nc2/2? 
    - add all of those as edges while tracking what was already seen is going to be factorial complexity
    - we can reduce it by doing an A* kind of search where we only keep track of violations as potential edges?
        . or make num violations as the edge weight => dikstra?
    - we can further reduce by leaving aside pointless edges e.g. swapping a with a again?

Just check the char frequencies at the different index parities:
    - whatever char is even can only be swapped with other positions in an even parity and likewise with odd
    - just need to check if the same char + same frequencies exist at both odd and even parities
'''
from collections import defaultdict

class Solution:
    def checkStrings(self, s1: str, s2: str) -> bool:
        s1_even = defaultdict(int)
        s1_odd = defaultdict(int)

        s2_even = defaultdict(int)
        s2_odd = defaultdict(int)

        for i, (c1, c2) in enumerate(zip(s1, s2)):
            if i % 2 == 0:
                s1_even[c1] += 1
                s2_even[c2] += 1
            else:
                s1_odd[c1] += 1
                s2_odd[c2] += 1

        if not self.is_equal(s1_even, s2_even):
            return False
        
        return self.is_equal(s1_odd, s2_odd)

    def is_equal(self, counts1, counts2):
        if len(counts1) != len(counts2):
            return False

        # check keys
        keys1 = set(counts1.keys())
        keys2 = set(counts2.keys())

        if keys1 != keys2:
            return False

        # check values
        for k in keys1:
            c1 = counts1[k]
            c2 = counts2[k]

            if c1 != c2:
                return False

        return True
