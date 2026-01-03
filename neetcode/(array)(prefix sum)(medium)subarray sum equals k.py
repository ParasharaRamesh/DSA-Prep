'''
Given an array of integers nums and an integer k, return the total number of subarrays whose sum equals to k.

A subarray is a contiguous non-empty sequence of elements within an array.

 

Example 1:

Input: nums = [1,1,1], k = 2
Output: 2
Example 2:

Input: nums = [1,2,3], k = 3
Output: 2
 

Constraints:

1 <= nums.length <= 2 * 104
-1000 <= nums[i] <= 1000
-107 <= k <= 107

Thoughts:
1. My solution involved computing the prefix sum array and then using a hash map to store the indices of the prefix sum array. Then for every prefix sum, I would add to the result smartly based on whether the prefix sum was equal to k, and whether ps + k also existed in the same hashmap. Few minor edge cases where if the k value itself was 0, then we could just pick two indices from the same list to form a subarray with sum as 0. This solution worked but was inefficient.
2. Neetcode solution:
    . idea is that as we build the prefix sum array at position i, we can check if the difference between the prefix sum and k has occurred before.
    . if it has, then we can add the number of times it has occurred to the result.
    . The only tricky part is the initial value of the prefix sum to count map, which is 0: 1 which corresponds to saying that there is 1 empty subarray at index -1 which is 0. Doing this kind of sentinel trick makes it easier to calculate things and keeps the code clean.
    . This way the first time we come up with the subarray sum as k, its equivalent to saying we removed the empty subarray in the beginning to get this one!
'''

from typing import List
from collections import defaultdict
from bisect import * 
from math import *

class Solution:
    '''
    inspired by neetcode solution, can build it in a single pass:
    . idea is that as we build the prefix sum array at position i, we can check if the difference between the prefix sum and k has occurred before.
    . if it has, then we can add the number of times it has occurred to the result.
    . The only tricky part is the initial value of the prefix sum to count map, which is 0: 1 which corresponds to saying that there is 1 empty subarray at index -1 which is 0. Doing this kind of sentinel trick makes it easier to calculate things and keeps the code clean.
    . This way the first time we come up with the subarray sum as k, its equivalent to saying we removed the empty subarray in the beginning to get this one!
    '''
    def subarraySum(self, nums: List[int], k: int) -> int:
        ps_to_count = {0: 1}
        prefix_sum = 0
        res = 0
        for num in nums:
            prefix_sum += num
            diff = prefix_sum - k
            res += ps_to_count.get(diff, 0)
            ps_to_count[prefix_sum] = ps_to_count.get(prefix_sum, 0) + 1

        return res

    # it worked but was inefficient
    def subarraySum_mysolution(self, nums: List[int], k: int) -> int:
        # get prefix sum array
        prefix = []
        count = 0
        for num in nums:
            count += num
            prefix.append(count)
            
        # have a hash map of sum -> list of indices (preferably sorted)
        ps_to_inds = defaultdict(list)
        for i, ps in enumerate(prefix):
            ps_to_inds[ps].append(i)
        ordered_ps = list(sorted(ps_to_inds.keys()))
        

        # iterate over every key and see if it could have been used in the array 
        res = 0
        for ps in ordered_ps:
            # the ps itself could be k in which case just add it
            if ps == k:
                res += len(ps_to_inds[ps])

            if ps + k in ps_to_inds:
                curr_inds = ps_to_inds[ps]

                if ps + k == ps: #i.e k is 0
                    # this means we can just pick two indices from this list to form a subarray with sum as 0
                    res += comb(len(curr_inds), 2) if len(curr_inds) >= 2 else 0
                else:
                    # look for ps + k 
                    other_inds = ps_to_inds[ps + k]

                    # for every curr_ind find the number of other_inds greater and add it
                    for ci in curr_inds:
                        # do binary search to efficiently find the number of other_inds greater than ci
                        ind = bisect_left(other_inds, ci)
                        if ind < len(other_inds):
                            num_other = len(other_inds) - ind
                            # print(f"addding {num_other=} to {res=} for {ci=}")
                            res += num_other

        return res