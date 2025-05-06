'''
You are given an integer array hand where hand[i] is the value written on the ith card and an integer groupSize.

You want to rearrange the cards into groups so that each group is of size groupSize, and card values are consecutively increasing by 1.

Return true if it's possible to rearrange the cards in this way, otherwise, return false.

Example 1:

Input: hand = [1,2,4,2,3,5,3,4], groupSize = 4

Output: true
Explanation: The cards can be rearranged as [1,2,3,4] and [2,3,4,5].

Example 2:

Input: hand = [1,2,3,3,4,5,6,7], groupSize = 4

Output: false
Explanation: The closest we can get is [1,2,3,4] and [3,5,6,7], but the cards in the second group are not consecutive.

Constraints:

1 <= hand.length <= 1000
0 <= hand[i] <= 1000
1 <= groupSize <= hand.length

'''

from collections import Counter
from typing import List


class Solution:
    def isNStraightHand(self, hands: List[int], groupSize: int) -> bool:
        counts = Counter(hands)
        sorted_keys = list(sorted(counts.keys()))

        if len(hands) % groupSize != 0:
            return False

        group = []

        while len(counts) > 0:
            for hand in sorted_keys:
                print(f"counts are {counts}, group is {group}")
                if hand in counts:
                    if len(group) == 0:
                        group.append(hand)
                        counts[hand] -= 1
                    elif len(group) == groupSize:
                        print(f"group is cleared")
                        group.clear()
                        break
                    else:
                        if group[-1] + 1 == hand:
                            group.append(hand)
                            counts[hand] -= 1
                        else:
                            print(f"false :(")
                            return False

                    # remove hand
                    if counts[hand] == 0:
                        print(f"{hand} removed from counts")
                        del counts[hand]

        print(f"return true")
        return True