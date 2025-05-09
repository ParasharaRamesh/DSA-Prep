'''
You are given a 2D array of integers triplets, where triplets[i] = [ai, bi, ci] represents the ith triplet. You are also given an array of integers target = [x, y, z] which is the triplet we want to obtain.

To obtain target, you may apply the following operation on triplets zero or more times:

Choose two different triplets triplets[i] and triplets[j] and update triplets[j] to become [max(ai, aj), max(bi, bj), max(ci, cj)].
* E.g. if triplets[i] = [1, 3, 1] and triplets[j] = [2, 1, 2], triplets[j] will be updated to [max(1, 2), max(3, 1), max(1, 2)] = [2, 3, 2].

Return true if it is possible to obtain target as an element of triplets, or false otherwise.

Example 1:

Input: triplets = [[1,2,3],[7,1,1]], target = [7,2,3]

Output: true
Explanation:
Choose the first and second triplets, update the second triplet to be [max(1, 7), max(2, 1), max(3, 1)] = [7, 2, 3].

Example 2:

Input: triplets = [[2,5,6],[1,4,4],[5,7,5]], target = [5,4,6]

Output: false
Constraints:

1 <= triplets.length <= 1000
1 <= ai, bi, ci, x, y, z <= 100

'''

from typing import List

'''
. trivial case 1: if target[i] not found in any triplet[j][i] -> return false
. trivial case 2: as we iterate in case we find the triplet which exactly same as target then return and finish
. keep temp
. if not, for each triplet :
    - check temp == triplet
    - choose to not use it at all:
        . if each is > target[i] -> can never contribute when taken max (other one will spoil the party)
    - choose to use it:
        . in case anything matches and others are lesser than equal to target
        . keep doing the max operation with the current best and check if that is equal to target whenever there is some match
'''
class Solution:
    def mergeTriplets(self, triplets: List[List[int]], target: List[int]) -> bool:

        # trvivial cases
        a_present = False
        b_present = False
        c_present = False

        for triplet in triplets:
            a, b, c = triplet

            # exact match
            if triplet == target:
                return True

            # partial matches
            if a == target[0]:
                a_present = True

            if b == target[1]:
                b_present = True

            if c == target[2]:
                c_present = True

        # trvial case no 2:
        if not (a_present and b_present and c_present):
            return False

        best = None
        tx, ty, tz = target

        for triplet in triplets:
            x, y, z = triplet

            # ignore it
            if x > tx or y > ty or z > tz:
                continue

            # choose it
            x_equal = x == tx
            y_equal = y == ty
            z_equal = z == tz
            atleast_one = x_equal or y_equal or z_equal
            all_le = (x <= tx) and (y <= ty) and (z <= tz)

            if atleast_one and all_le:
                best = [max(best[0], triplet[0]), max(best[1], triplet[1]), max(best[2], triplet[2])] if best else triplet

                if best == target:
                    return True

        # default
        return False


if __name__ == '__main__':
    s = Solution()

    triplets = [[2, 5, 3], [1, 8, 4], [1, 7, 5]]
    target = [2, 7, 5]
    expected = True
    res = s.mergeTriplets(triplets, target)
    assert expected == res, f"{expected = }, {res = }"

    triplets = [[1, 2, 3], [7, 1, 1]]
    target = [7, 2, 3]
    expected = True
    res = s.mergeTriplets(triplets, target)
    assert expected == res, f"{expected = }, {res = }"

    triplets = [[2, 5, 3], [2, 3, 4], [1, 2, 5], [5, 2, 3]]
    target = [5, 5, 5]
    expected = True
    res = s.mergeTriplets(triplets, target)
    assert expected == res, f"{expected = }, {res = }"

    triplets = [[2, 5, 6], [1, 4, 4], [5, 7, 5]]
    target = [5, 4, 6]
    expected = False
    res = s.mergeTriplets(triplets, target)
    assert expected == res, f"{expected = }, {res = }"

    triplets = [[3, 4, 5], [4, 5, 6]]
    target = [3, 2, 5]
    expected = False
    res = s.mergeTriplets(triplets, target)
    assert expected == res, f"{expected = }, {res = }"
