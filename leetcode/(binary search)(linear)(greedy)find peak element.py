'''
A peak element is an element that is strictly greater than its neighbors.

Given a 0-indexed integer array nums, find a peak element, and return its index. If the array contains multiple peaks, return the index to any of the peaks.

You may imagine that nums[-1] = nums[n] = -∞. In other words, an element is always considered to be strictly greater than a neighbor that is outside the array.

You must write an algorithm that runs in O(log n) time.

 

Example 1:

Input: nums = [1,2,3,1]
Output: 2
Explanation: 3 is a peak element and your function should return the index number 2.
Example 2:

Input: nums = [1,2,1,3,5,6,4]
Output: 5
Explanation: Your function can return either index number 1 where the peak element is 2, or index number 5 where the peak element is 6.
 

Constraints:

1 <= nums.length <= 1000
-231 <= nums[i] <= 231 - 1
nums[i] != nums[i + 1] for all valid i.
'''

'''
We know that for all i, nums[i] != nums[i+1] and nums[-1] == nums[n] == -INF. From these conditions, we can prove that there must exist such an i that is peak, nums[i] > nums[i-1] and nums[i] > nums[i+1]:
Suppose there is no i such that nums[i] > nums[i-1] and nums[i] > nums[i+1], then there are two cases:

if nums[i] > nums[i-1], it implies nums[i] < nums[i+1] for all i. however, this contradicts nums[n] == -INF
if nums[i] > nums[i+1], it implies nums[i] < nums[i-1] for all i which contradicts nums[-1] == -INF
QED
Now we know that there must exist a peak i, we can derive the algorithm

if nums[m] < nums[m+1], then we know the right half is also an array where for all i, nums[i] != nums[i+1] and nums[-1] == nums[n] == -INF (or to be more precise any x such that x < nums[i_0] && x < nums[i_n-1] and we know there must exist a peak
if nums[m] > nums[m+1], same logic applies for the left half
'''
class Solution:
    #binary search -> we just need local maxima so just go towards the side which is bigger
    def findPeakElement(self, nums: List[int]) -> int:
        l = 0
        r = len(nums) - 1

        while l <= r:
            m = (l + r) // 2
            curr = nums[m]
            prev = nums[m-1] if m - 1 >= 0 else float("-inf")
            after = nums[m+1] if m + 1 < len(nums) else float("-inf")

            if prev < curr and curr > after:
                return m

            if prev > curr and prev > after:
                r = m - 1
            elif after > curr and after > prev:
                l = m + 1
            else:
                l = m + 1

        return -1
        
    def findPeakElement_linear(self, nums: List[int]) -> int:
        for i in range(len(nums)):
            curr = nums[i]
            prev = nums[i-1] if i - 1 >= 0 else float("-inf") 
            after = nums[i+1] if i + 1 < len(nums) else float("-inf")

            if prev < curr and curr > after:
                return i
