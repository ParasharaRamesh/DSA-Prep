'''
1888. Minimum Number of Flips to Make the Binary String Alternating

You are given a binary string s. You are allowed to perform two types of operations on the string in any sequence:

Type-1: Remove the character at the start of the string s and append it to the end of the string.
Type-2: Pick any character in s and flip its value, i.e., if its value is '0' it becomes '1' and vice-versa.
Return the minimum number of type-2 operations you need to perform such that s becomes alternating.

The string is called alternating if no two adjacent characters are equal.

For example, the strings "010" and "1010" are alternating, while the string "0100" is not.
 

Example 1:

Input: s = "111000"
Output: 2
Explanation: Use the first operation two times to make s = "100011".
Then, use the second operation on the third and sixth elements to make s = "101010".
Example 2:

Input: s = "010"
Output: 0
Explanation: The string is already alternating.
Example 3:

Input: s = "1110"
Output: 1
Explanation: Use the second operation on the second element to make s = "1010".
 

Constraints:

1 <= s.length <= 105
s[i] is either '0' or '1'.
'''

'''
.for string of len n -> n-1 left rotations to give (n-1) * n -> unique strings . Find minimum across that
. does type 1 even matter? YES
. given a string maintain count of 1,0 in odd position and count 1,0 in even position.
    -> ans = min(convert all 0 -> 1 in odd + convert all 1 -> 0 in even, convert all 1->0 in odd + convert all 0-> 1 in odd)
. for the base configuration you can easily maintain two counters for odd and even
    -> for every left shift its just a matter of reorganizing the counters in an efficient way?
    -> otherwise if we try to recount and then take a decision -> N^2 -> TLE
. total no of 1s and total no of 0s dont change
. if len is odd-> after one type 1 op parity of that char doesnt change but if len is even -> it switches
    - need to give away one to the other parity from first position then swap the rest 
. this way each counter slide is o(1) op

'''
from collections import defaultdict

class Solution:
    def minFlips(self, s: str) -> int:
        n = len(s)

        even = defaultdict(int)
        odd = defaultdict(int)

        # init even and odd 
        for i, c in enumerate(s):
            if i % 2:
                odd[c] += 1
            else:
                even[c] += 1

        # check for the string as is
        res = self.get_min_flips(even, odd)

        # early exit
        if res == 0:
            return res

        # do n - 1 type 1 ops -> all unique strings
        for i in range(n-1):
            even, odd = self.get_left_shifted_counts(even, odd, s, i)
            shifted_min = self.get_min_flips(even, odd)
            res = min(res, shifted_min)  
            
        return res

    def get_min_flips(self, even, odd):
        e0, e1 = even["0"], even["1"]
        o0, o1 = odd["0"], odd["1"]
        return min(e0 + o1, o0 + e1)

    def get_left_shifted_counts(self, even, odd, s, i):
        n = len(s)
        new_even = defaultdict(int)
        new_odd = defaultdict(int)

        even[s[i]] -= 1

        if n % 2:
            # if odd
            new_even[s[i]] += 1
        else:
            new_odd[s[i]] += 1

        e1, e0 = even["1"], even["0"]
        o1, o0 = odd["1"], odd["0"]

        new_even["1"] += o1
        new_even["0"] += o0

        new_odd["1"] += e1
        new_odd["0"] += e0

        return new_even, new_odd
