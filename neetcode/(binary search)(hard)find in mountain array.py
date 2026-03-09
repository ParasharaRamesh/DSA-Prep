'''
(This problem is an interactive problem.)

You may recall that an array arr is a mountain array if and only if:

arr.length >= 3
There exists some i with 0 < i < arr.length - 1 such that:
arr[0] < arr[1] < ... < arr[i - 1] < arr[i]
arr[i] > arr[i + 1] > ... > arr[arr.length - 1]
Given a mountain array mountainArr, return the minimum index such that mountainArr.get(index) == target. If such an index does not exist, return -1.

You cannot access the mountain array directly. You may only access the array using a MountainArray interface:

MountainArray.get(k) returns the element of the array at index k (0-indexed).
MountainArray.length() returns the length of the array.
Submissions making more than 100 calls to MountainArray.get will be judged Wrong Answer. Also, any solutions that attempt to circumvent the judge will result in disqualification.



Example 1:

Input: mountainArr = [1,2,3,4,5,3,1], target = 3
Output: 2
Explanation: 3 exists in the array, at index=2 and index=5. Return the minimum index, which is 2.
Example 2:

Input: mountainArr = [0,1,2,4,2,1], target = 3
Output: -1
Explanation: 3 does not exist in the array, so we return -1.


Constraints:

3 <= mountainArr.length() <= 104
0 <= target <= 109
0 <= mountainArr.get(index) <= 109
'''

# """
# This is MountainArray's API interface.
# You should not implement it, or speculate about its implementation
# """
#class MountainArray:
#    def get(self, index: int) -> int:
#    def length(self) -> int:

class Solution:
    def findInMountainArray(self, target: int, mountainArr: 'MountainArray') -> int:
        self.mountainArr = mountainArr
        self.n = mountainArr.length()
        self.cache = dict()
        self.cache[-1] = float("-inf")
        self.cache[self.n] = float("inf")

        max_ind = self.get_max_ind()
        
        ind = self.search(0, max_ind, target, reverse=False)

        if ind != -1:
            return ind

        return self.search(max_ind + 1, self.n - 1, target, reverse=True)

    def get(self, i):
        if i in self.cache:
            return self.cache[i]
        
        self.cache[i] = self.mountainArr.get(i)
        return self.cache[i]

    def get_max_ind(self):
        l = 0
        r = self.n - 1

        while l <= r:
            m = (l + r)//2

            prev = self.get(m-1)
            curr = self.get(m)
            after = self.get(m+1)

            if prev < curr and curr > after:
                return m

            if prev < curr < after:
                l = m + 1
            else:
                r = m - 1

        return l
    
    def search(self, l, r, target, reverse):
        while l <= r:
            m = (l + r)//2
            val = self.get(m)

            if val == target:
                return m

            if val < target:
                if not reverse:
                    l = m + 1
                else:
                    r = m - 1
            else:
                if not reverse:
                    r = m - 1
                else:
                    l = m + 1

        return -1
        
