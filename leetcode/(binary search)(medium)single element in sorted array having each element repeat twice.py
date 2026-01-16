''' 
You are given a sorted array consisting of only integers where every element appears exactly twice, except for one element which appears exactly once.

Return the single element that appears only once.

Your solution must run in O(log n) time and O(1) space.

 
Example 1:

Input: nums = [1,1,2,3,3,4,4,8,8]
Output: 2
Example 2:

Input: nums = [3,3,7,7,10,11,11]
Output: 10
 

Constraints:

1 <= nums.length <= 105
0 <= nums[i] <= 105
'''
class Solution:
    # xor trick to remove duplicates
    def singleNonDuplicate_linear(self, nums: List[int]) -> int:
        res = 0
        for n in nums:
            res ^= n

        return res

    # binary search
    def singleNonDuplicate(self, nums: List[int]) -> int:
        '''
        . binary search needed
        . if nums[m] != (nums[l], nums[r]) then nums[m] is the answer
        . whichever side is the match; if the other side excluding m is of even length then can be ignored otherwise we should consider it
        '''
        l = 0
        r = len(nums) - 1

        while 0 <= l <= r < len(nums): 
            m = (l + r) // 2

            #bounday cases also considered
            is_left_same = False if m == 0 else nums[m-1] == nums[m]
            is_right_same = False if m == len(nums) - 1 else nums[m] == nums[m + 1]

            # easiest case we have found the unique element
            if not is_left_same and not is_right_same:
                return nums[m]
              
            '''
              . check the right side from [m:] and if that length is even then it means that the unique element is not there meaning we can move the right pointer by 2 because the leftside m-1 and m are the same
              . if the other side is odd then we can move to that side
            '''
            if is_left_same and not is_right_same:
                # on the right side, check the length : if even r = m - 2  else l = m + 1
                right_len = r - m

                if right_len % 2 == 0:
                    r = m - 2
                else: 
                    l = m + 1
            # exact mirror analogous case
            elif not is_left_same and is_right_same:
                # on the left side, check the length : if even l = m + 2  else r = m - 1
                left_len = m - l

                if left_len % 2 == 0:
                    l = m + 2
                else:
                    r = m - 1
                  
        # will never reach here anyway
        return None
