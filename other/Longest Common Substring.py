from collections import defaultdict


class Solution:
    # using extra space and indices to start traversing
    def longestCommonSubstr_bruteforce(self, s1: str, s2: str) -> int:
        ''' for every char in s1, find all occurances it occurs in s2 and try from there and see '''
        longest = 0

        # find all occurances of chars in s2
        s2_chars = defaultdict(list)

        for i, c in enumerate(s2):
            s2_chars[c].append(i)

        # iterate through all chars in s1
        for _i, c in enumerate(s1):
            if c not in s2_chars:
                continue

            # for each such occurence walk through together and find out the best
            s2_c_is = s2_chars[c]
            for _j in s2_c_is:
                curr = 0
                i = _i
                j = _j

                while i < len(s1) and j < len(s2) and s1[i] == s2[j]:
                    curr += 1
                    i += 1
                    j += 1

                longest = max(longest, curr)

        return longest

    def longestCommonSubstr_memoize(self, s1: str, s2: str) -> int:
        n, m = len(s1), len(s2)
        cache = {}  # (i, j) -> best LCSuf length anywhere in s1[i:], s2[j:]
        longest = 0

        def dfs(i: int, j: int) -> int:
            nonlocal longest

            if (i, j) in cache:
                return cache[(i, j)]

            # Base case
            if i >= n or j >= m:
                cache[(i, j)] = 0
                return cache[(i, j)]

            # 1) If chars match, consider extending here
            cache[(i, j)] = 0
            if s1[i] == s2[j]:
                cache[(i, j)] = 1 + dfs(i + 1, j + 1)
                longest = max(longest, cache[(i, j)])

            # explore other paths
            dfs(i + 1, j)
            dfs(i, j + 1)

            # but from this path only return this
            return cache[(i, j)]

        dfs(0, 0)
        return longest

    def longestCommonSubstr_tabulation(self, s1: str, s2: str) -> int:
        n, m = len(s1), len(s2)
        cache = defaultdict(int)  # (i, j) -> best LCSuf length anywhere in s1[i:], s2[j:]

        # NOTE: base cases of (i >= n or j >= m) are 0 by default

        # reverse topological state visit ( anyways going through all states , so no need to worry about the other two paths dfs(i+1,j) and dfs(i,j+1)
        for i in range(n - 1, -1, -1):
            for j in range(m - 1, -1, -1):
                if s1[i] == s2[j]:
                    cache[(i, j)] = 1 + cache[(i + 1, j + 1)]

        # amongst the ones which do have something, return max, if nothing exists return 0
        return max(cache.values()) if len(cache) else 0

