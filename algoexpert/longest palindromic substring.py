# refer to manachers algorithm for O(n) approach

# recursive approach but time limit exceeded!
def longestCommonSubstring(word1, word2, allCommonSubstrings):
    m = len(word1)
    n = len(word2)

    if m == 0 or n == 0:
        return max(allCommonSubstrings, key=lambda x: len(x))

    # characters match
    if word1[0] == word2[0]:
        match = allCommonSubstrings[:]
        match[-1] += word1[0]
        return longestCommonSubstring(word1[1:], word2[1:], match)
    else:
        possibilities = [
            longestCommonSubstring(word1[1:], word2, allCommonSubstrings[:] + [""]),
            longestCommonSubstring(word1, word2[1:], allCommonSubstrings[:] + [""])
        ]
        return max(possibilities, key=lambda x: len(x))


def longestPalindromicSubstring2(word):
    reverse = word[::-1]
    return longestCommonSubstring(word, reverse, [""])


# dp aproach would be to build up recursions of different lengths, i.e. different batch sizes

# sliding window approach of different batches
def isPalindrome(string):
    i = 0
    j = len(string) - 1

    while i <= j:
        if string[i] != string[j]:
            return False

        i += 1
        j -= 1

    return True


def longestPalindromicSubstring(string):
    m = len(string)
    # checking only sizes till 2
    for windowSize in range(m, 0, -1):
        i = 0
        while i <= m - windowSize:
            slice = string[i: i + windowSize]
            if isPalindrome(slice):
                return slice
            else:
                i += 1


# middle out approach
class Solution:
    def bestPalindromeWithStartingIndices(self, l, r, s):
        m = len(s)
        palindrome = ""
        while l >= 0 and r < m:
            #no match
            if s[l] != s[r]:
                break

            #if they match
            if l == r:
                #odd case
                palindrome = s[l]
            else:
                #even case
                palindrome = s[l] + palindrome + s[r]

            #move it
            l -= 1
            r += 1
        return palindrome

    def longestPalindrome(self, s):
        # consider each char as the centre and check outwards
        best = ""

        for i in range(len(s)):
            #odd length palindrome case with center at i
            odd = self.bestPalindromeWithStartingIndices(i, i, s)
            #even length palindrome case with center at i, i+1
            even = self.bestPalindromeWithStartingIndices(i, i + 1, s)
            best = max([best, odd, even], key=lambda x: len(x))

        return best

if __name__ == '__main__':
    word = "abaxyzzyxf"  # xyzzyxgv
    print(Solution().longestPalindrome(word))
