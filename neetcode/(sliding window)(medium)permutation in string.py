from collections import Counter, defaultdict


class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False
        m, n = len(s1), len(s2)
        target = Counter(s1)
        window = defaultdict(int)

        # Build the first window [0, m - 1]
        for i in range(m):
            window[s2[i]] += 1

        start, end = 0, m - 1
        while end < n:
            if window == target:
                return True
            # Slide: drop left, advance, add right
            window[s2[start]] -= 1
            if window[s2[start]] == 0:
                del window[s2[start]]
            start += 1
            end += 1
            if end < n:
                window[s2[end]] += 1
        return False
