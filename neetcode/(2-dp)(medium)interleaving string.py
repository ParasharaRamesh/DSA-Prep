'''
You are given three strings s1, s2, and s3. Return true if s3 is formed by interleaving s1 and s2 together or false otherwise.

Interleaving two strings s and t is done by dividing s and t into n and m substrings respectively, where the following conditions are met

|n - m| <= 1, i.e. the difference between the number of substrings of s and t is at most 1.
s = s1 + s2 + ... + sn
t = t1 + t2 + ... + tm
Interleaving s and t is s1 + t1 + s2 + t2 + ... or t1 + s1 + t2 + s2 + ...
You may assume that s1, s2 and s3 consist of lowercase English letters.

Example 1:



Input: s1 = "aaaa", s2 = "bbbb", s3 = "aabbbbaa"

Output: true
Explanation: We can split s1 into ["aa", "aa"], s2 can remain as "bbbb" and s3 is formed by interleaving ["aa", "aa"] and "bbbb".

Example 2:

Input: s1 = "", s2 = "", s3 = ""

Output: true
Example 3:

Input: s1 = "abc", s2 = "xyz", s3 = "abxzcy"

Output: false
Explanation: We can't split s3 into ["ab", "xz", "cy"] as the order of characters is not maintained.

Constraints:

0 <= s1.length, s2.length <= 50
0 <= s3.length <= 100
'''
from collections import defaultdict


class Solution:
    # my original solution (inefficient af)
    def isInterleave_original(self, s1: str, s2: str, s3: str) -> bool:

        cache = dict()

        # left over s1, s2 and i which matches with s3, turn is either 1 or 2
        def helper(s1, s2, i, turn, n, m):
            key = (s1, s2, i, turn, n, m)
            if key in cache:
                return cache[(s1, s2, i, turn, n, m)]

            # base
            if s1 == "" and s2 == "":
                cache[key] = (abs(n - m) <= 1)
                return cache[key]

            # invalid cases
            if len(s1) == 0 and len(s2) > 0 and turn == 1:
                cache[key] = False
                return False

            if len(s1) > 0 and len(s2) == 0 and turn == 2:
                cache[key] = False
                return False

            # do something based on turn
            j = 0
            if turn == 1:
                # invalid cannot be formed
                if s1[0] != s3[i]:
                    cache[key] = False
                    return False

                all_poss = False
                while j < len(s1):
                    if s1[j] == s3[i + j]:
                        all_poss = all_poss or helper(s1[j + 1:], s2, i + j + 1, 2, n + 1, m)
                        j += 1
                    else:
                        break

                cache[key] = all_poss
                return all_poss
            elif turn == 2:
                if s2[0] != s3[i]:
                    cache[key] = False
                    return False

                all_poss = False
                while j < len(s2):
                    if s2[j] == s3[i + j]:
                        all_poss = all_poss or helper(s1, s2[j + 1:], i + j + 1, 1, n, m + 1)
                        j += 1
                    else:
                        break

                cache[key] = all_poss
                return all_poss

        n, m = 0, 0
        return (len(s3) == len(s1) + len(s2)) and (helper(s1, s2, 0, 1, n, m) or helper(s1, s2, 0, 2, n, m))

    # better top down solution (O(N3) space and time complexity)
    def isInterleave_memo(self, s1: str, s2: str, s3: str) -> bool:
        m = len(s1)
        n = len(s2)
        o = len(s3)

        # trivial case
        if m + n != o:
            return False

        cache = dict()

        def helper(i, j, k):
            key = (i, j, k)

            if key in cache:
                return cache[key]

            # base cases
            # k exhausted but i or j still has something left
            if k >= o and (i < m or j < n):
                cache[key] = False
                return cache[key]

            # i and j exhausted but k has something left
            if i >= m and j >= n and k < o:
                cache[key] = False
                return cache[key]

            # only when everything is exhausted is it true
            if i == m and j == n and k == o:
                cache[key] = True
                return cache[key]

            # actual recurrence
            # if all are equal, can proceed from either place
            if (i < m and j < n and k < o) and (s1[i] == s2[j] == s3[k]):
                cache[key] = helper(i + 1, j, k + 1) or helper(i, j + 1, k + 1)
                return cache[key]

            # only s1 matches
            if (i < m and k < o) and (s1[i] == s3[k]):
                cache[key] = helper(i + 1, j, k + 1)
                return cache[key]

            # only s2 matches
            if (j < n and k < o) and (s2[j] == s3[k]):
                cache[key] = helper(i, j + 1, k + 1)
                return cache[key]

            # nothing matches
            cache[key] = False
            return cache[key]

        return helper(0, 0, 0)

    # bottom up approach ((O(N3) space and time complexity))
    def isInterleave_tabu(self, s1: str, s2: str, s3: str) -> bool:
        m = len(s1)
        n = len(s2)
        o = len(s3)

        # trivial case
        if m + n != o:
            return False

        # Initialize cache with default value False
        cache = defaultdict(bool)

        # Base case: when all strings are exhausted
        cache[(m, n, o)] = True

        # Fill the dp table in reverse order (bottom-up)
        for i in range(m, -1, -1):
            for j in range(n, -1, -1):
                for k in range(o, -1, -1):
                    # Skip the base case we already set
                    if i == m and j == n and k == o:
                        continue

                    # Skip invalid state combinations ( still works without this , if we want to purely convert from the top down code)
                    # if i + j != k:
                    #     continue

                    # if all are equal, can proceed from either place
                    if (i < m and j < n and k < o) and (s1[i] == s2[j] == s3[k]):
                        cache[(i, j, k)] = cache[(i + 1, j, k + 1)] or cache[(i, j + 1, k + 1)]

                    # only s1 matches
                    elif (i < m and k < o) and (s1[i] == s3[k]):
                        cache[(i, j, k)] = cache[(i + 1, j, k + 1)]

                    # only s2 matches
                    elif (j < n and k < o) and (s2[j] == s3[k]):
                        cache[(i, j, k)] = cache[(i, j + 1, k + 1)]

                    # else case is automatically handled by defaultdict(bool) which returns False

        return cache[(0, 0, 0)]


    # OPTIMAL DP: Top down
    def isInterleave_memo2(self, s1: str, s2: str, s3: str) -> bool:
        m, n, o = len(s1), len(s2), len(s3)

        # trivial case
        if m + n != o:
            return False

        # Use dict instead of defaultdict for explicit caching
        cache = {}

        # only 2 states is needed because anyways k is always going to be i + j
        def helper(i, j):
            # Calculate k based on i and j
            k = i + j

            # Check if already computed
            if (i, j) in cache:
                return cache[(i, j)]

            # Base case: reached the end of both strings successfully
            if i == m and j == n:
                return True

            result = False

            # Try taking a character from s1 if possible
            if i < m and s1[i] == s3[k]:
                result = helper(i + 1, j)

            # If we haven't found a valid interleaving yet, try s2
            if not result and j < n and s2[j] == s3[k]:
                result = helper(i, j + 1)

            # Cache and return the result
            cache[(i, j)] = result
            return result

        return helper(0, 0)

    # OPTIMAL: Bottom up DP with 2 states
    def isInterleave_tabu_2(self, s1: str, s2: str, s3: str) -> bool:
        m, n, o = len(s1), len(s2), len(s3)

        # trivial case
        if m + n != o:
            return False

        # Use dict instead of defaultdict for explicit caching
        cache = defaultdict(bool)

        cache[(m, n)] = True

        for i in range(m, -1, -1):
            for j in range(n, -1, -1):
                if i == m and j == n:
                    # skip as already present
                    continue

                # Calculate k based on i and j
                k = i + j

                result = False

                # Try taking a character from s1 if possible
                if i < m and s1[i] == s3[k]:
                    result = cache[(i + 1, j)]

                # If we haven't found a valid interleaving yet, try s2
                if not result and j < n and s2[j] == s3[k]:
                    result = cache[(i, j + 1)]

                # Cache and return the result
                cache[(i, j)] = result

        return cache[(0, 0)]