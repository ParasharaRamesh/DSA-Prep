'''
You are given a string s consisting of lowercase english letters.

We want to split the string into as many substrings as possible, while ensuring that each letter appears in at most one substring.

Return a list of integers representing the size of these substrings in the order they appear in the string.

Example 1:

Input: s = "xyxxyzbzbbisl"

Output: [5, 5, 1, 1, 1]
Explanation: The string can be split into ["xyxxy", "zbzbb", "i", "s", "l"].

Example 2:

Input: s = "abcabc"

Output: [6]
Constraints:

1 <= s.length <= 100
'''

from typing import List


class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        groups = []

        char_to_last_ind = dict()
        for i, char in enumerate(s):
            char_to_last_ind[char] = i

        # grow as much as possible
        n = len(s)
        l, r = 0, 0

        while l <= r < n:
            group_count = 0

            while l <= r < n:
                curr_char_last_ind = char_to_last_ind[s[l]]

                if l == curr_char_last_ind:
                    # only char
                    l += 1
                    group_count += 1
                else:
                    # it is there somewhere further down the line
                    l += 1
                    r = max(r, curr_char_last_ind)
                    group_count += 1

            groups.append(group_count)
            r = l # start from the next place

        return groups


if __name__ == '__main__':
    sol = Solution()

    s = "abbec"
    expected = [1, 2, 1, 1]
    ans = sol.partitionLabels(s)
    assert expected == ans, f"{expected = }, {ans = }"

    s = "eccbbbbdec"
    expected = [10]
    ans = sol.partitionLabels(s)
    assert expected == ans, f"{expected = }, {ans = }"

    s = "abcabc"
    expected = [6]
    ans = sol.partitionLabels(s)
    assert expected == ans, f"{expected = }, {ans = }"

    s = "xyxxyzbzbbisl"
    expected = [5, 5, 1, 1, 1]
    ans = sol.partitionLabels(s)
    assert expected == ans, f"{expected = }, {ans = }"

    s = "ababcbacadefegdehijhklij"
    expected = [9, 7, 8]
    ans = sol.partitionLabels(s)
    assert expected == ans, f"{expected = }, {ans = }"
