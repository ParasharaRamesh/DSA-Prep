'''

You are given an integer array people where people[i] is the weight of the ith person, and an infinite number of boats where each boat can carry a maximum weight of limit. Each boat carries at most two people at the same time, provided the sum of the weight of those people is at most limit.

Return the minimum number of boats to carry every given person.

Example 1:

Input: people = [5,1,4,2], limit = 6

Output: 2
Explanation:
First boat [5,1].
Second boat [4,2].

Example 2:

Input: people = [1,3,2,3,2], limit = 3

Output: 4
Explanation:
First boat [3].
Second boat [3].
Third boat [1,2].
Fourth boat [2].

Constraints:

1 <= people.length <= 50,000
1 <= people[i] <= limit <= 30,000

'''

'''
. Has to be < O(N^2) in time complexity because of constraint
. Can try to be greedy and pick the highest and lowest person and pair them together
. since each boat can only accomodate two people doesnt matter if we pick the two most heavy people since the boat size is only accomodative of 2 people. Can as well just go with high and low
. Just keep pairing the high and low weight person together else you just make the high weight person have his own boat
. In the end if one person is left then ensure that person has his own boat
'''

from typing import List


class Solution:
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        people.sort()
        boats = 0

        l, r = 0, len(people) - 1

        while l < r:
            if people[l] + people[r] <= limit:
                boats += 1
                l += 1
                r -= 1
            else:
                # only the people[r] can go in the boat alone
                boats += 1
                r -= 1

        if l == r:
            # last person left
            boats += 1

        return boats