'''
Given an array of integers arr, find the sum of min(b), where b ranges over every (contiguous) subarray of arr. Since the answer may be large, return the answer modulo 109 + 7.



Example 1:

Input: arr = [3,1,2,4]
Output: 17
Explanation:
Subarrays are [3], [1], [2], [4], [3,1], [1,2], [2,4], [3,1,2], [1,2,4], [3,1,2,4].
Minimums are 3, 1, 2, 4, 1, 1, 2, 1, 1, 1.
Sum is 17.
Example 2:

Input: arr = [11,81,94,43,3]
Output: 444

'''

class SegmentTree:
    def __init__(self, arr):
        self.arr = arr
        self.n = len(arr)
        self.tree = [float("inf")] * 4 * self.n
        self.build(0, 0, self.n - 1)
        print("constructed segment tree")

    def build(self, tree_ind, start, end):
        if start == end:
            self.tree[tree_ind] = self.arr[start]
            return self.tree[tree_ind]

        mid = start + (end - start) // 2

        # left
        left_min = self.build(2 * tree_ind + 1, start, mid)

        # right
        right_min = self.build(2 * tree_ind + 2, mid + 1, end)

        # combine
        self.tree[tree_ind] = min(left_min, right_min)
        return self.tree[tree_ind]

    def query(self, l, r, tree_ind=0, start=None, end=None):
        if start == None and end == None:
            start = 0
            end = self.n - 1

        # no overlap (l r start end) or ( start end l r)
        if r < start or end < l:
            return float("inf")

        # complete overlap l start end r
        if l <= start and start <= end and end <= r:
            return self.tree[tree_ind]

        # partial overlap
        mid = start + (end - start) // 2
        left_min = self.query(l, r, 2 * tree_ind + 1, start, mid)
        right_min = self.query(l, r, 2 * tree_ind + 2, mid + 1, end)
        return min(left_min, right_min)


class Solution:
    def sumSubarrayMinsWithSegmentTrees(self, arr): # O(N2 Logn) -> TLE
        st = SegmentTree(arr)
        total = 0

        for i in range(len(arr)):
            for j in range(i, len(arr)):
                query = st.query(i, j)
                total += query
                print(f"sum from {i} to {j} is {query}. Total is now {total}")

        return total % (10**9 + 7)

    def sumSubarrayMins(self, arr):
        total = 0
        n = len(arr)
        stack = []

        for i, ele in enumerate(arr):
            while stack and stack[-1][1] > ele:
                '''
                this is the best this element can do in terms of being the minimum
                '''
                j, curr_min = stack.pop()
                num_left = j - stack[-1][0] if stack else j
                num_right = (i + 1) - j
                total += num_left * num_right * curr_min

            stack.append((i+ 1, ele))

        #now count all of the stacks go through this
        while stack:
            #1 based indexing
            curr_i, curr_min = stack.pop()
            num_right = (n - curr_i + 1) #num of right subarrays including this
            num_left = curr_i # num of left subarrays including this
            if stack:
                num_left = (curr_i - stack[-1][0])
            total += num_left * num_right *  curr_min

        return total % (10**9 + 7)


if __name__ == '__main__':
    solution = Solution()
    arr = [3, 1, 2, 4]
    print(solution.sumSubarrayMins(arr))  # 17

    arr = [11, 81, 94, 43, 3]
    print(solution.sumSubarrayMins(arr))  # 444
