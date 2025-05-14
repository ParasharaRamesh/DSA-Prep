'''

'''

from typing import List
from collections import defaultdict


class Solution:
    # using sliding window
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        if k == 0:
            # there can never be distinct i,j for which this is true
            return False

        window = set()
        n = len(nums)

        # fill the first window
        i = 0
        while i < n and i < k + 1:
            if nums[i] in window:
                return True
            window.add(nums[i])
            i += 1

        l, r = 0, k

        # keep sliding
        while r < n:
            # shrink l
            window.discard(nums[l])
            l += 1

            # check
            if r + 1 < n and nums[r + 1] in window:
                return True

            # grow r
            if r + 1 < n:
                window.add(nums[r + 1])

            r += 1

        return False

    # using dictionary
    def containsNearbyDuplicate_dict(self, nums: List[int], k: int) -> bool:
        unique_nums = defaultdict(list)

        for i, num in enumerate(nums):
            unique_nums[num].append(i)

        for num in unique_nums:
            indices = unique_nums[num]
            if len(indices) > 1:
                i = 0
                while i < len(indices) - 1:
                    if abs(indices[i] - indices[i + 1]) <= k:
                        return True
                    i += 1

        return False


if __name__ == '__main__':
    s = Solution()

    nums = [1, 0, 1, 1]
    k = 1
    expected = True
    ans = s.containsNearbyDuplicate(nums, k)
    assert expected == ans, f"{expected = }, {ans = }"

    nums = [1, 2, 3, 1, 2, 3]
    k = 2
    expected = False
    ans = s.containsNearbyDuplicate(nums, k)
    assert expected == ans, f"{expected = }, {ans = }"

    nums = [2, 1, 2]
    k = 1
    expected = False
    ans = s.containsNearbyDuplicate(nums, k)
    assert expected == ans, f"{expected = }, {ans = }"

    nums = [1, 2, 3, 1]
    k = 3
    expected = True
    ans = s.containsNearbyDuplicate(nums, k)
    assert expected == ans, f"{expected = }, {ans = }"
