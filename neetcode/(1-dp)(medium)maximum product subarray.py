'''
Given an integer array nums, find a subarray that has the largest product within the array and return it.

A subarray is a contiguous non-empty sequence of elements within an array.

You can assume the output will fit into a 32-bit integer.

Example 1:

Input: nums = [1,2,-3,4]

Output: 4
Example 2:

Input: nums = [-2,-1]

Output: 2
Constraints:

1 <= nums.length <= 1000
-10 <= nums[i] <= 10

'''
from functools import reduce
from typing import List
from collections import deque, Counter, defaultdict


class Solution:
    '''
    1. kadane's method:

    . the standard kadane's method wont work because with negative numbers the sign can get flipped instantly making whatever was large -> small ( in negative direction) and vice versa
    . that's why it is better to keep track of both maximum and minimum and if at all a negative number comes we swap it so that we are still continuing to keep track of things.
    . perhaps sliding window is more intuitive
    '''

    def maxProduct_kadane(self, nums: List[int]) -> int:
        maxProd = nums[0]
        minProd = nums[0]
        result = nums[0]

        for num in nums[1:]:
            if num < 0:
                maxProd, minProd = minProd, maxProd  # Swap if negative

            maxProd = max(num, num * maxProd)
            minProd = min(num, num * minProd)

            # technically dont need to compare with minProd
            result = max(result, maxProd, minProd)

        return result

    '''
    2. NC Kadane's method:
    
    - similarly keep track of min and max
    - at each point a number a negative num multiplied with min could result in max value and a positive number multiplied with max could also give the max value
    '''

    def maxProduct(self, nums: List[int]) -> int:
        res = nums[0]
        curr_max, curr_min = 1, 1

        for num in nums:
            # holding the values
            num_curr_max = num * curr_max
            num_curr_min = num * curr_min

            # num as is || num with current max || if num is negative then times curr_min assuming that is also negative
            curr_max = max(num, num_curr_max, num_curr_min)
            curr_min = min(num, num_curr_max, num_curr_min)
            res = max(res, curr_max, curr_min)

        return res

    ''' 
    3. Prefix and suffix method:
    
    - for this problem the best solution is definitely going to be linked with one of the ends
    - therefore build from both sides and see which is better every step of the way
    '''

    def maxProduct_prefix_suffix(self, nums: List[int]) -> int:
        res = nums[0]

        # build prefix
        prefix = 1
        for num in nums:
            prefix *= num
            res = max(res, prefix)

            if prefix == 0:
                # reset
                prefix = 1

        # build suffix
        suf = 1
        for num in reversed(nums):
            suf *= num
            res = max(res, suf)

            if suf == 0:
                # reset
                suf = 1

        return res

    '''
    4. Similar to prefix and suffix method:
    
    - first split the array into subarrays which dont contain a zero
    - for each subarray find out the number of negative signs
    - find the total product
    - go from l->r an r->l and keep removing until the first negative number is removed. (in case there are odd number of negative signs)
    - this is so that there is no cuts and the contiguity of the product sub array is maintained
    - find out the number
    '''

    def maxProduct_neg_num_signs(self, nums: List[int]) -> int:
        # find all 0's
        indices = defaultdict(list)
        for i, num in enumerate(nums):
            indices[num].append(i)

        # find out all the max
        if 0 in indices and len(indices[0]) > 0:
            res = 0

            start = 0
            for index in indices[0]:
                sub_nums = nums[start: index]
                start = index + 1
                res = max(res, self.nonzero_maxproduct(sub_nums))

            # last one
            res = max(res, self.nonzero_maxproduct(nums[start:]))
            return res
        else:
            return self.nonzero_maxproduct(nums)

    def nonzero_maxproduct(self, nums):
        if len(nums) == 0:
            return 0

        if len(nums) == 1:
            return nums[0]

        res = nums[0]

        neg = 0
        prod = 1
        for num in nums:
            if num < 0:
                neg += 1
            prod *= num

        # even no of zeroes
        if neg % 2 == 0:
            return prod

        # if odd number of negative things, go from each side
        # l->r
        curr = prod
        l = 0
        while l < len(nums) and nums[l] > 0:
            curr //= nums[l]
            l += 1
        res = max(res, curr // nums[l])

        # r->l
        curr = prod
        r = len(nums) - 1
        while r >= 0 and nums[r] > 0:
            curr //= nums[r]
            r -= 1
        res = max(res, curr // nums[r])

        return res


if __name__ == '__main__':
    s = Solution()

    expected = 0
    ans = s.maxProduct([-2, 0, -1])
    assert expected == ans, f"expected {expected}, got {ans}"

    expected = 2
    ans = s.maxProduct([-2, -1])
    assert expected == ans, f"expected {expected}, got {ans}"

    expected = 24
    ans = s.maxProduct([1, -2, -3, 4])
    assert expected == ans, f"expected {expected}, got {ans}"

    expected = 24
    ans = s.maxProduct([1, -2, 3, -4])
    assert expected == ans, f"expected {expected}, got {ans}"

    expected = 48
    ans = s.maxProduct([2, -2, 3, -4])
    assert expected == ans, f"expected {expected}, got {ans}"

    expected = 4
    ans = s.maxProduct([1, 2, -3, 4])
    assert expected == ans, f"expected {expected}, got {ans}"
