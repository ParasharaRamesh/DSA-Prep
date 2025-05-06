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
        # make a dict of char -> list of indicies
        char_to_inds = {char: [] for char in set(s)}

        for i, char in enumerate(s):
            char_to_inds[char].append(i)

        '''
        for each char:
            0. its always better to be a single char group or group with min chars
            a. find the furthest away it is , and include that ( set the end pointer to that )
            b. for the next char after that see if it is already in current group charset if yes include (till next index ) if no then its a new group
        '''
        start = 0
        end = 0
        groups = []
        current_groupset = None

        # print(f"char_to_inds is {char_to_inds}")

        while end < len(s):
            curr_char = s[end]
            curr_char_inds = char_to_inds[curr_char]

            # print(f"begin | start: {start}, end: {end}, curr_char: {curr_char}, curr_char_inds: {curr_char_inds}")
            # this in itself is a group
            if len(curr_char_inds) == 1:
                groups.append(end - start + 1)

                # print(f"curr_char_is just one | group is {s[start: end+1]}")

                start = end + 1
                end = start
                # print(f"curr_char_is just one | new start: {start} and new end: {end}")
            else:
                end = curr_char_inds[-1]

                current_groupset = set(s[start:end + 1])
                # print(f"else | current_groupset is {current_groupset}, start: {start}, end: {end}")

                # pick the max
                while True:
                    max_inds = [(char_to_inds[group_char][-1], group_char) for group_char in current_groupset]
                    end, last_char = max(max_inds, key=lambda x: x[0])
                    # print("-" * 50)
                    # print(f"new end with greedy biggest {end} and last char is {last_char}")

                    new_group = set(s[start: end + 1])

                    if new_group != current_groupset:
                        current_groupset = new_group
                        # print(f"setting new current_groupset to {current_groupset}")
                    else:
                        # print("group done!")
                        break

                # set this as the next group
                groups.append(end - start + 1)
                # print(f"new group is {s[start:end+1]} and groups is {groups}")

                start = end + 1
                end = start
                # print("-" * 50)
                # print()

        return groups