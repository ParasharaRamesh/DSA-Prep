
from collections import Counter, defaultdict


class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False

        m = len(s1)
        n = len(s2)

        s1_counts = Counter(s1)
        s2_counts = defaultdict(int)

        start = 0
        end = m - 1

        # build the window of comparision first
        for i in range(start, end + 1):
            s2_counts[s2[i]] += 1

        while end < n:
            if s1_counts == s2_counts:
                return True
            else:
                s2_counts[s2[start]] -= 1
                if s2_counts[s2[start]] == 0:
                    s2_counts.pop(s2[start])

                start += 1

                end += 1
                if end < n:
                    s2_counts[s2[end]] += 1

        return False
