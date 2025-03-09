'''
Top K Frequent Elements
Solved
Given an integer array nums and an integer k, return the k most frequent elements within the array.

The test cases are generated such that the answer is always unique.

You may return the output in any order.

Example 1:

Input: nums = [1,2,2,3,3,3], k = 2

Output: [2,3]
'''

from collections import Counter
from typing import List


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        counts = list(Counter(nums).items())
        print(f"counts are {counts}")
        counts.sort(key=lambda kv: kv[1],reverse=True)
        print(f"ordered is {counts}")
        result = []
        for i in range(k):
            result.append(counts[i][0])
        return result
