'''
Special binary strings are binary strings with the following two properties:

The number of 0's is equal to the number of 1's.
Every prefix of the binary string has at least as many 1's as 0's.
You are given a special binary string s.

A move consists of choosing two consecutive, non-empty, special substrings of s, and swapping them. Two strings are consecutive if the last character of the first string is exactly one index before the first character of the second string.

Return the lexicographically largest resulting string possible after applying the mentioned operations on the string.

 

Example 1:

Input: s = "11011000"
Output: "11100100"
Explanation: The strings "10" [occuring at s[1]] and "1100" [at s[3]] are swapped.
This is the lexicographically largest string possible after some number of swaps.
Example 2:

Input: s = "10"
Output: "10"
 

Constraints:

1 <= s.length <= 50
s[i] is either '0' or '1'.
s is a special binary string.
'''

'''
Thoughts: 
. we are already given a special string which means there will always be some answer
. one edge case which can do right away is if the the first n/2 chars are 1 and the next are all 0's then that itself is the best valid string
. smallest valid string would be 10 and any other valid string would be multiple of 2
. can only swap consecutive valid parenthesis substrings
    . another rabbit hole was converting it into a parenthesis question
. to know if they are valid, the counts should be same and the stack approach should work 
. if you have a sequence of valid substrings of length say :
    - 2 4 8 => can become 8 4 2 in place
    - if there are valid substrings seperated by non valid substrings it cant be swapped and will stay right there
        . e.g. .. 2 4 .. 4 => .. 4 2 .. 4
    - I went down this rabbit hole and got stuck because if we merge intervals sometimes that interval itself might not be the best lexographic special string
. Need to solve it recursively:
    - just keep accumulating the longest valid chain and then recursively make that valid
        . core insight is that if the string is not already the largest (i.e. n1s followed by n0s) then we can just say it is 
        . 1 + makeLargestSpecial(inner_string) + 0 => i.e we skip the first and last characters and only do the middle chunk
            - because we can be sure that the first and last chars are always going to be 1 & 0 !!
            - any strings like 1 10 1100 0 -> would basically be solved as 1 + makeValid(101100) + 0
                - that inner chunk is easy because that is just 2 simple largest chains which would become 1100 10 => 1 1100 10 0
    - once you collect all valid chains in a list -> sort them lexographically and join
        . went down another rabbit hole here because I sorted by length! and not be lexographic order
        . e.g. 101010 vs 110100 vs 111000 vs 101100 all of them would have the same priority as they have the same length but we need to sort them lexographically!
'''

class Solution:
    def makeLargestSpecial(self, s: str) -> str:
        def is_largest_possible(str):
            n = len(s)
            return str[:n//2] == "1"*(n//2) and str[n//2:] == "0"*(n//2)

        # get the chains
        balance = 0

        valid_consecutive_chains = []
        chain = ""
        for c in s:
            chain += c
            balance += 1 if c == '1' else -1

            if balance == 0:
                if not is_largest_possible(chain):
                    # make it the largest it can be
                    chain = "1" + self.makeLargestSpecial(chain[1:-1]) + "0"

                # after making it the largest append
                valid_consecutive_chains.append(chain)
                chain = ""

        # now that each chain is the largest, sort them in lexographic order
        valid_consecutive_chains.sort(reverse=True)

        # concatenate everything after sorting
        return "".join(valid_consecutive_chains)

if __name__ == "__main__":
    sol = Solution()

    s = "1101001110001101010110010010"
    expected = "1110010101010011100011010010"
    ans = sol.makeLargestSpecial(s)
    assert ans == expected, f"{s=} {expected=} {ans=}"

    s = "11011000"
    expected = "11100100"
    ans = sol.makeLargestSpecial(s)
    assert ans == expected, f"{s=} {expected=} {ans=}"

    s = "101101011000"
    expected = "111001010010"
    ans = sol.makeLargestSpecial(s)
    assert ans == expected, f"{s=} {expected=} {ans=}"

    s = "101100101100"
    expected = "110011001010"
    ans = sol.makeLargestSpecial(s)
    assert ans == expected, f"{s=} {expected=} {ans=}"

    s = "11011000"
    expected = "11100100"
    ans = sol.makeLargestSpecial(s)
    assert ans == expected, f"{s=} {expected=} {ans=}"

    s = "10110010"
    expected = "11001010"
    ans = sol.makeLargestSpecial(s)
    assert ans == expected, f"{s=} {expected=} {ans=}"

    s = "10111000"
    expected = "11100010"
    ans = sol.makeLargestSpecial(s)
    assert ans == expected, f"{s=} {expected=} {ans=}"

    s = "11110000"
    expected = "11110000"
    ans = sol.makeLargestSpecial(s)
    assert ans == expected, f"{s=} {expected=} {ans=}"