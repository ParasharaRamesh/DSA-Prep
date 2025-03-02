'''
Leetcode.6: Medium


The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this: (you may want to display this pattern in a fixed font for better legibility)

P   A   H   N
A P L S I I G
Y   I   R
And then read line by line: "PAHNAPLSIIGYIR"

Write the code that will take a string and make this conversion given a number of rows:

string convert(string s, int numRows);


Example 1:

Input: s = "PAYPALISHIRING", numRows = 3
Output: "PAHNAPLSIIGYIR"
Example 2:

Input: s = "PAYPALISHIRING", numRows = 4
Output: "PINALSIGYAHRPI"
Explanation:
P     I    N
A   L S  I G
Y A   H R
P     I
Example 3:

Input: s = "A", numRows = 1
Output: "A"


Constraints:

1 <= s.length <= 1000
s consists of English letters (lower-case and upper-case), ',' and '.'.
1 <= numRows <= 1000
'''

'''
Approach: Just simulate
'''
class Solution:
    def convert(self, s: str, numRows: int) -> str:
        res = [[] for i in range(numRows)]

        c = 0 # ch index
        r = -1 # row index
        forward = True

        while c < len(s):
            ch = s[c]

            if forward:
                if r + 1 < numRows:
                    r += 1
                    res[r].append(ch)
                else:
                    r -= 1
                    res[r].append(ch)
                    forward = False
            else:
                if r > 0:
                    r -= 1
                    res[r].append(ch)
                else:
                    r += 1
                    res[r].append(ch)
                    forward = True

            c += 1

        return "".join(["".join(row) for row in res])



if __name__ == '__main__':
    s = Solution()

    res = s.convert("PAYPALISHIRING", 3)
    ans = "PAHNAPLSIIGYIR"
    print(res, ans, res == ans)

    res = s.convert("PAYPALISHIRING", 4)
    ans = "PINALSIGYAHRPI"
    print(res, ans, res == ans)