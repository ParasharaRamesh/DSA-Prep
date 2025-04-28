'''
Leetcode. 5

. Brute force solution is cubic
. Expanding from centers is quadratic
. Manachers algorithm is linear

Refer to this video for explanation => https://www.youtube.com/watch?v=nbTSfrEfo6M

Main ideas of this algorithm:

1. use extra space to store the lengths which will help going from quadratic to linear
2. add # in between each character so that any string ( even, odd ) lengths becomes of odd length ( i.e. total length will now become 2*N + 1 where N is length of original string)
    - this way effectively we are considering all of the inbetween positions between 2 characters also which will help in finding even length palindromes!
3. lets say we already knew the palindromic substring length centered at position c which has a left boundary L and a right boundary R.
    - usually [L -> c-1] (left half) and [c+1 -> R] (right half) are symmetric so any smaller palindromic substrings within the left half will be mirrored to the right half
    - for a position i > c if we want to know what its value is there are mainly 2 cases:
        a. either you can look at the value from the mirrored point on the left half which is @ 2c - i
        b. but since that mirrored value could have a longer substring strectching beyond the left boundary of L, then the value is just R - i
        c. we take the lower bound between these two to ensure a fair starting point to expand from
. now that we have found the lower bound, we dont need to re-compare all of the values and can directly start expanding from the fringe elements
. in case the palindrome length @ i has exceeded right boundary, then update the center and the new right boundary, if not let it stay as what it was already

In this code the right boundary is called radius since that alone is enough and we dont really need to keep track of the left boundary.
'''


class Solution:
    def add_hashes(self, s):
        res = "#"
        for c in s:
            res += f"{c}#"
        return res

    def longestPalindrome(self, s: str) -> str:
        # edge cases
        if len(s) <= 1:
            return s

        # values to keep updating as and when we find something better
        longest_palindrome = s[0]
        longest_palindrome_length = 1

        # make any string into an odd length string so that manachers algorithm can work
        s = self.add_hashes(s)
        n = len(s)

        # aux datastructure to avoid repeated calculations
        palindrome_radius = [0] * n
        center = 0
        radius = 0

        # go over each character, compare with mirrored index and find lower bound , grow from lower bound and update the values
        for i in range(n):
            # is this current index i within the radius from the current center
            if center - radius < i < center + radius:
                # mirrored index(i)
                mirror = 2 * center - i

                palindrome_radius[i] = min(
                    palindrome_radius[mirror],
                    # in case the left half contains palindromes which do not extend beyond the left boundary @ c - (r-c)
                    radius - i
                    # in case the left half contains palindromes which are actually exceeding the left boundary, the mirror palindrome value will be a lot higher and we need a value smaller than that. Therefore we need to restrict ourselves within the left-right boundaries.
                )

            # NOTE: in case, the index i was not inside the current radius from the center, then the palindrome_radius is basically 0, which means you just try to compute that from the center moving outwards char by char from 0.
            # try to grow and find the correct value for palindrome_radius[i], because now we know a lower bound and can compare from the fringe
            while (
                i - (palindrome_radius[i] + 1) >= 0 and  # as long as left edge of palindrome radius of i is within bounds
                i + (palindrome_radius[i] + 1) < n and  # as long as right edge of palindrome radius of i is within bounds
                s[i - (palindrome_radius[i] + 1)] == s[i + (palindrome_radius[i] + 1)]
            ):  # as long as the fringe elements after growing are equal
                palindrome_radius[i] += 1  # keep adding to the palindrome length

            # move the center to the next location. if the final palindrome @ i exceeds the right boundary, then i is the new center and the right most position is also updated
            if i + palindrome_radius[i] > radius:
                center = i
                radius = i + palindrome_radius[i]

            # update the best value so far
            if palindrome_radius[i] > longest_palindrome_length:
                longest_palindrome_length = palindrome_radius[i]
                longest_palindrome = s[i - palindrome_radius[i]: i + palindrome_radius[i]].replace("#", "")

        return longest_palindrome

if __name__ == '__main__':
    s = Solution()
    print(s.longestPalindrome("babad"))
    print(s.longestPalindrome("cbbd"))
    print(s.longestPalindrome("abdabba"))
