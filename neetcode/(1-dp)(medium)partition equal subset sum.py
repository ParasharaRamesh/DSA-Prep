'''
You are given an array of positive integers nums.

Return true if you can partition the array into two subsets, subset1 and subset2 where sum(subset1) == sum(subset2). Otherwise, return false.

Example 1:

Input: nums = [1,2,3,4]

Output: true
Explanation: The array can be partitioned as [1, 4] and [2, 3].

Example 2:

Input: nums = [1,2,3,4,5]

Output: false
Constraints:

1 <= nums.length <= 100
1 <= nums[i] <= 50

'''
from collections import UserDict
from typing import List


class Solution:
    # memoization
    def canPartition_memo(self, nums: List[int]) -> bool:
        cache = {}

        def helper(i, target):
            key = (i, target)

            if key in cache:
                return cache[key]

            if i == len(nums):
                cache[key] = False
                return False

            if target < 0:
                cache[key] = False
                return False

            if target == 0:
                cache[key] = True
                return True

            cache[key] = helper(i + 1, target - nums[i]) or helper(i + 1, target)
            return cache[key]

        total = sum(nums)
        if total % 2:
            return False

        return helper(0, total // 2)

    # bottom up
    #this one actually gives TLE for some reason probably because of the fact that I am using userdict which is slower
    def canPartition_bottomup_with_userdict(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2:
            return False

        target = total // 2
        n = len(nums)
        cache = Cache(n)

        # Reverse topological order: i = n-1 → 0, target = 0 → total//2
        for i in range(n - 1, -1, -1):
            for t in range(0, target + 1):
                key = (i, t)
                cache[key] = cache[(i + 1, t - nums[i])] or cache[(i + 1, t)]

        return cache[(0, target)]

    # filling up the truthy base cases first and then the false ones ( i.e. reverse order of base cases is also important )
    def canPartition_bottomup_raw_from_constraints(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2 != 0:
            return False

        target = total // 2
        n = len(nums)
        cache = {}

        # 1) Truthy base: for all i,   (i, 0) → True . Note even when i == n it is True (in the topdown one it was not because we were doing early stopping, but that is the consequence when doing it in reverse manner)
        for i in range(n + 1):
            cache[(i, 0)] = True

        # 2) “End-of-list” falsy base: for t=1…target, (n, t) → False
        for t in range(1, target + 1):
            cache[(n, t)] = False

        # 3) Falsy base cases for all i, negative targets → False
        #    (worst-case negative offset is -101 baesd on the constraints)
        for i in range(n + 1):
            for t in range(-101, 0):
                cache[(i, t)] = False

        # 3) Now the main reverse-topo DP, exactly your one-liner:
        for i in range(n - 1, -1, -1):
            for t in range(0, target + 1):
                cache[(i, t)] = cache[(i + 1, t - nums[i])] or cache[(i + 1, t)]

        return cache[(0, target)]

    def canPartition_bottomup_but_cachemisses_resolved_with_get(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2 != 0:
            return False

        target = total // 2
        n = len(nums)
        cache = {}

        # 1) Truthy base: for all i, (i, 0) → True
        for i in range(n + 1):
            cache[(i, 0)] = True

        # 2) End-of-list falsy: for t = 1 to target, (n, t) → False
        for t in range(1, target + 1):
            cache[(n, t)] = False

        # 3) Main reverse-topo DP
        for i in range(n - 1, -1, -1):
            for t in range(0, target + 1):
                cache[(i, t)] = cache.get((i + 1, t - nums[i]), False) or cache[(i + 1, t)]

        return cache[(0, target)]

    def canPartition_cache_misses_handled_by_userdict_for_not_obvious_basecase(self, nums: List[int]) -> bool:
        total = sum(nums)
        if total % 2 != 0:
            return False

        target = total // 2
        n = len(nums)
        cache = Cache2(n)

        # 1) Truthy base: for all i, (i, 0) → True
        for i in range(n + 1):
            cache[(i, 0)] = True

        # 2) End-of-list falsy: for t = 1 to target, (n, t) → False
        for t in range(1, target + 1):
            cache[(n, t)] = False

        # 3) Main reverse-topo DP
        for i in range(n - 1, -1, -1):
            for t in range(0, target + 1):
                cache[(i, t)] = cache[(i + 1, t - nums[i])] or cache[(i + 1, t)]

        return cache[(0, target)]

class Cache(UserDict):
    def __init__(self, n):
        super().__init__()
        self.n = n

    def __missing__(self, key):
        i, target = key

        # i.e. just reverse the order of the conditions in the original one
        #truthy ones first
        if target == 0:
            self[key] = True
            return True

        # falsy ones later
        if i == self.n or target < 0:
            self[key] = False
            return False

        raise KeyError(f"Invalid access: {key}")

class Cache2(UserDict):
    def __init__(self, n):
        super().__init__()
        self.n = n

    def __missing__(self, key):
        i, t = key
        if t < 0:
            self[key] = False
            return False
        raise KeyError


if __name__ == '__main__':
    s = Solution()

    nums = [2, 3, 5]
    expected = True
    ans = s.canPartition(nums)
    assert ans == expected, f"expected:{expected}, got:{ans}"

    nums = [1, 5, 11, 5]
    expected = True
    ans = s.canPartition(nums)
    assert ans == expected, f"expected:{expected}, got:{ans}"

    nums = [1, 5, 5, 11]
    expected = True
    ans = s.canPartition(nums)
    assert ans == expected, f"expected:{expected}, got:{ans}"


