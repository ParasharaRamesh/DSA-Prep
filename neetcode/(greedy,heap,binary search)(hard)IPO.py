'''
Suppose LeetCode will start its IPO soon. In order to sell a good price of its shares to Venture Capital, LeetCode would like to work on some projects to increase its capital before the IPO. Since it has limited resources, it can only finish at most k distinct projects before the IPO. Help LeetCode design the best way to maximize its total capital after finishing at most k distinct projects.

You are given n projects where the ith project has a pure profit profits[i] and a minimum capital of capital[i] is needed to start it.

Initially, you have w capital. When you finish a project, you will obtain its pure profit and the profit will be added to your total capital.

Pick a list of at most k distinct projects from given projects to maximize your final capital, and return the final maximized capital.

The answer is guaranteed to fit in a 32-bit signed integer.

 

Example 1:

Input: k = 2, w = 0, profits = [1,2,3], capital = [0,1,1]
Output: 4
Explanation: Since your initial capital is 0, you can only start the project indexed 0.
After finishing it you will obtain profit 1 and your capital becomes 1.
With capital 1, you can either start the project indexed 1 or the project indexed 2.
Since you can choose at most 2 projects, you need to finish the project indexed 2 to get the maximum capital.
Therefore, output the final maximized capital, which is 0 + 1 + 3 = 4.
Example 2:

Input: k = 3, w = 0, profits = [1,2,3], capital = [0,1,2]
Output: 6
 

Constraints:

1 <= k <= 10^5
0 <= w <= 10^9
n == profits.length
n == capital.length
1 <= n <= 10^5
0 <= profits[i] <= 10^4
0 <= capital[i] <= 10^9
'''

'''
Thoughts:

. greedy problem
. outer loop where the operation runs only k times
    - trivial case where if k == len(profits) then we can return w + sum(profits)
    - can keep modifying w until we get the final answer
. can maintain max_heap => (profit, cap) (profit_to_cap_maxheap)
    . can also keep a sorted list of unique caps so that we can do binary search for the values of caps which are valid when popping from profit_to_cap_maxheap
    . using that we can pop from profit_to_cap_maxheap into temp buffer until we get a valid cap -> re push the buffer for future operations
'''
from typing import List
from heapq import *
from bisect import bisect_left

class Solution:
    def findMaximizedCapital(self, k: int, w: int, profits: List[int], capital: List[int]) -> int:
        # accumulated capital starts with w
        acc_cap = w

        # create the maxheaps
        profit_cap_max_heap = []

        for c, p in zip(capital, profits):
            heappush(profit_cap_max_heap, (-p, c))
            
        # all unique capital
        sorted_caps = list(sorted(set(capital)))

        # greedy simulation
        for _ in range(k):
            # using acc_cap get cap index from sorted_cap below which we can get the profit
            i = bisect_left(sorted_caps, acc_cap)

            if i == len(sorted_caps):
                valid_cap = sorted_caps[i - 1]
            elif sorted_caps[i] == acc_cap:
                valid_cap = sorted_caps[i]
            elif i == 0:
                # can exit early since all caps are higher than it 
                break
            else:
                valid_cap = sorted_caps[i - 1]
            
            # get the max profit when the cap is <= valid_cap -> keep popping until > valid_cap
            buffer = []
            while profit_cap_max_heap and profit_cap_max_heap[0][1] > valid_cap:
                item = heappop(profit_cap_max_heap)
                buffer.append(item)

            # break early if there is no way to improve -> as there is no c <= valid_cap
            if not profit_cap_max_heap:
                break

            # add to the acc cap
            p, c = heappop(profit_cap_max_heap)
            acc_cap -= p #because p is negative

            # repopulate
            for item in buffer:
                heappush(profit_cap_max_heap, item)

        return acc_cap

if __name__ == "__main__":
    s = Solution()
    
    # test case 1
    k = 2
    w = 0
    profits = [1,2,3]
    capital = [0,1,1]
    ans = s.findMaximizedCapital(k, w, profits, capital)
    expected = 4
    assert ans == expected, f"{expected=} {ans=}"

    # test case 2
    k = 3
    w = 0
    profits = [1,2,3]
    capital = [0,1,2]
    ans = s.findMaximizedCapital(k, w, profits, capital)
    expected = 6
    assert ans == expected, f"{expected=} {ans=}"

    # test case 3
    k = 3
    w = 0
    profits = [1,4,2,3]
    capital = [0,3,1,1]
    ans = s.findMaximizedCapital(k, w, profits, capital)
    expected = 8
    assert ans == expected, f"{expected=} {ans=}"

    # test case 4
    k = 4
    w = 2
    profits = [2,3,1,5,3]
    capital = [4,4,2,3,3]
    ans = s.findMaximizedCapital(k, w, profits, capital)
    expected = 14
    assert ans == expected, f"{expected=} {ans=}"
