'''
A binary string is monotone increasing if it consists of some number of 0's (possibly none), followed by some number of 1's (also possibly none).

You are given a binary string s. You can flip s[i] changing it from 0 to 1 or from 1 to 0.

Return the minimum number of flips to make s monotone increasing.

 

Example 1:

Input: s = "00110"
Output: 1
Explanation: We flip the last digit to get 00111.
Example 2:

Input: s = "010110"
Output: 2
Explanation: We flip to get 011111, or alternatively 000111.
Example 3:

Input: s = "00011000"
Output: 2
Explanation: We flip to get 00000000.
 

Constraints:

1 <= s.length <= 105
s[i] is either '0' or '1'.


Thoughts:

. to make it monotone increasing there is a clear point where the array becomes all 0s on the LHS and all 1s on the RHS
. There are 2 solutions, greedy or dp based

1. DP solution:
. main realization is that its a function which depends on current index 'i' and a flag stating whether everything before it is a 0 or everything before it is a one
. if everything before it is a 0 and the current char is a 0 you can chose to leave it as is or flip it
. in case not everything before it is a 0 ( meaning it is a 1 just before ) you have no choice but to flip everything to a 1
. the time/space complexity is no of bools * size = 2n

2. Greedy solution:

. basically we need to do it in a single pass as we go from left -> right we keep track of the no of flips required
. if at an index i, we know the no of flips needed to make the previous segment increasing then we can do the following:
    - if the curr char is a '1' we dont know yet on what the number of flips needed are
    - if it is a '0' however, we know that we can either flip this one or flip all of the ones seen so far to make it monotone increasing.  
    - keep track of the minimum all throughout

'''

class Solution:
    def minFlipsMonoIncr(self, s: str) -> int:
        res = 0
        cnt_one = 0

        for c in s:
            if c == "1":
                cnt_one += 1
            else:
                # either you can flip this to increase no of flips or you can just flip all of the 1s before to a zero 
                res = min(res + 1, cnt_one)

        return res

    def minFlipsMonoIncr_dp(self, s: str) -> int:
        cache = dict()

        def flips(i, is_prev_all_zero):
            key = (i, is_prev_all_zero)

            if key in cache:
                return cache[key]

            if i == len(s):
                cache[key] = 0
                return 0

            res = float("inf")

            # means everything before is all 1s
            if not is_prev_all_zero:
                if s[i] == "0":
                    # because we need to flip it
                    res = min(res, 1 + flips(i+1, False))
                else:
                    res = min(res, flips(i+1, False))
            else:
                if s[i] == "0":
                    leave = flips(i+1, True)
                    flip = 1 + flips(i+1, False)
                    res = min(res, leave, flip)
                else:
                    leave = flips(i+1, False) # leave it as 1
                    flip = 1 + flips(i+1, True) # flip to 0
                    res = min(res, leave, flip)

            cache[key] = res
            return res

        return flips(0, True)