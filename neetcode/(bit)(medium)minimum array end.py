'''
You are given two integers n and x. You have to construct an array of positive integers nums of size n where for every 0 <= i < n - 1, nums[i + 1] is greater than nums[i], and the result of the bitwise AND operation between all elements of nums is x.

Return the minimum possible value of nums[n - 1].

Example 1:

Input: n = 3, x = 2

Output: 6
Explanation: nums can be [2,3,6].

Example 2:

Input: n = 5, x = 3

Output: 19
Explanation: nums can be [3,7,11,15,19].

Constraints:

1 <= n, x <= 100,000,000

Insights:

* Basically we need to find the binary representation of n-1 and inject that binary representation into the binary     
representation of x such that we inject it.
* The way we inject it is as follows:

e.g. number 00100101 notice there are 5 zeros. If we want to inject 110 then we essentially have to inject 00110 into the location of the zeros
which becomes 00111101
'''

class Solution:
    def minEnd(self, n: int, x: int) -> int:
        if n == 1:
            return x

        # Find the number of zeros in x and its location as index
        bin_x = bin(x)[2:]
        zero_cnt = bin_x.count("0")
        zero_indices = []

        for i, c in enumerate(bin_x):
            if c == "0":
                zero_indices.append(i)

        # find out how much extra space is needed in binary rep of n to accomodate based on bit length of n - 1
        k = n-1
        extra_space = k.bit_length() - zero_cnt

        # change the bin_x to add extra space as a prefix
        if extra_space > 0:
            bin_x = "0"*extra_space + bin_x 
            zero_indices = [ind + extra_space for ind in zero_indices]
            zero_indices = [i for i in range(extra_space)] + zero_indices # to make sure that the extra space is at the beginning
            
        bin_x = [c for c in bin_x]
    
        # use the binary rep of the n - 1 and update it 
        last_bin_rep = bin(n-1)[2:] # to remove the starting 0b
        
        # update bin_x
        for val, zero_ind in zip(reversed(last_bin_rep), reversed(zero_indices)):
            bin_x[zero_ind] = val

        bin_x = "".join(bin_x)

        # reconvert it back 
        res = int(bin_x, 2)
        return res

if __name__ == "__main__":
    s = Solution()

    tests = [
        (97, 100000, 100320),
        (3, 2, 6),
        (5, 3, 19)
    ]

    for n, x, expected in tests:
        actual = s.minEnd(n, x)
        assert actual == expected, f"expected {expected} but got {actual}"