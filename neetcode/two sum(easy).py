from collections import defaultdict
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        reverse_map = defaultdict(list)
        for i, num in enumerate(nums):
            reverse_map[num].append(i)

        for i, num in enumerate(nums):
            other = target - num
            if other in reverse_map:
                other_inds = reverse_map[other]
                for other_ind in other_inds:
                    if other_ind != i:
                        return [i, other_ind]
        return []

    def twoSum_2pointer_sort(self, nums: List[int], target: int) -> List[int]:
        A = []
        for i, num in enumerate(nums):
            A.append([num, i])

        A.sort()
        i, j = 0, len(nums) - 1
        while i < j:
            cur = A[i][0] + A[j][0]
            if cur == target:
                return [min(A[i][1], A[j][1]),
                        max(A[i][1], A[j][1])]
            elif cur < target:
                i += 1
            else:
                j -= 1
        return []