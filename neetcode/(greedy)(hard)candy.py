'''
There are n children standing in a line. Each child is assigned a rating value given in the integer array ratings.

You are giving candies to these children subjected to the following requirements:

Each child must have at least one candy.
Children with a higher rating get more candies than their neighbors.
Return the minimum number of candies you need to have to distribute the candies to the children.

Example 1:

Input: ratings = [4,3,5]

Output: 5
Explanation: You can allocate to the first, second and third child with 2, 1, 2 candies respectively.

Example 2:

Input: ratings = [2,3,3]

Output: 4
Explanation: You can allocate to the first, second and third child with 1, 2, 1 candies respectively.
The third child gets 1 candy because it satisfies the above two conditions.

Constraints:

1 <= ratings.length <= 20,000
0 <= ratings[i] <= 20,000
'''

from typing import List

class Solution:
    '''
    We can handle left and right neighbors separately. First, scan left to right to ensure each child with a higher rating than their left neighbor gets more candy. Then, scan right to left to handle the right neighbor constraint. When adjusting for right neighbors, we take the maximum of the current value and what the right constraint requires, preserving the left constraint satisfaction.

    Algorithm
        Initialize an array where each child starts with 1 candy.
        First pass (left to right): if a child's rating is higher than their left neighbor's, set their candy count to one more than the left neighbor.
        Second pass (right to left): if a child's rating is higher than their right neighbor's, set their candy count to the maximum of its current value and one more than the right neighbor.
        Return the sum of all candies.
    '''
    def candy_greedy_2_pass(self, ratings: List[int]) -> int:
        """
        `n` is number of children. The algorithm works in O(n) with two linear scans.
        """
        n = len(ratings)
        """
        Start with 1 candy for everyone to satisfy the minimum requirement:
        each child must get at least one candy.
        Example: n=4 -> [1,1,1,1] before enforcing relative-rating constraints.
        """
        arr = [1] * n

        """
        First pass (left -> right):
        Enforce only the left-neighbor rule:
        if ratings[i] > ratings[i-1], then arr[i] must be arr[i-1] + 1.
        Example: ratings [1,2,3] updates arr to [1,2,3].
        """
        for i in range(1, n):
            """
            When current rating is higher than left rating, current child must have
            strictly more candies than left child.
            """
            if ratings[i - 1] < ratings[i]:
                """
                Minimal valid increment is exactly +1 over left child, which keeps
                total candies minimal while satisfying the strict inequality.
                Example: left candies=2 -> current becomes 3.
                """
                arr[i] = arr[i - 1] + 1

        """
        Second pass (right -> left):
        Enforce right-neighbor rule without breaking what first pass already fixed.
        Example purpose: ratings [3,2,1] cannot be solved by left->right alone.
        """
        for i in range(n - 2, -1, -1):
            """
            If current rating is higher than right rating, current child must have
            more candies than the right child.
            """
            if ratings[i] > ratings[i + 1]:
                """
                We take max(existing, right+1):
                - right+1 satisfies right-side constraint now
                - existing may already be larger due to left-side constraints
                Taking max preserves both constraints simultaneously.
                Example: ratings [1,3,2]
                after first pass arr=[1,2,1], at i=1 right+1=2, max(2,2)=2.
                """
                arr[i] = max(arr[i], arr[i + 1] + 1)

        """
        Sum of per-child candies gives the minimum total after both constraints
        are enforced globally.
        Example: ratings [1,0,2] -> arr [2,1,2] -> total 5.
        """
        return sum(arr)

    # ---------------------1 pass greedy solution I came up with ---------------------------------------------
    def get_dir(self, ratings, i):
        """
        If we are at the last child, there is no "next" child to compare against,
        so direction is undefined for this step.
        Example: ratings = [4, 2, 5], i = 2 (last index) -> no pair (2, 3) exists.
        """
        if i == len(ratings) - 1:
            return None

        dir = 0

        """
        Compare current child with next child:
        - Upward direction means next rating is larger, so candies should rise.
          Example: [1, 3] -> second child needs more candies than first.
        - Downward direction means next rating is smaller, so candies should fall.
          Example: [5, 2] -> first child needs more candies than second.
        """
        if ratings[i] < ratings[i + 1]:
            dir = 1
        elif ratings[i] > ratings[i + 1]:
            dir = -1

        return dir

    def up_streak(self, ratings, i):
        streak = 1
        n = len(ratings)

        """
        Count how long the strictly increasing run is from index i.
        Example: [1, 2, 4, 3] starting at i=0 gives streak=3 (1<2<4).
        """
        while i < n - 1 and ratings[i] < ratings[i+1]:
            i += 1
            streak += 1

        return streak, i  

    def down_streak(self, ratings, i):
        streak = 1
        n = len(ratings)

        """
        Count how long the strictly decreasing run is from index i.
        Example: [5, 4, 1, 2] starting at i=0 gives streak=3 (5>4>1).
        """
        while i < n - 1 and ratings[i] > ratings[i+1]:
            i += 1
            streak += 1

        return streak, i  
    
    def same_streak(self, ratings, i):
        streak = 1
        n = len(ratings)

        """
        Count plateau length where adjacent ratings are equal.
        Example: [3, 3, 3, 2] starting at i=0 gives streak=3.
        """
        while i < n - 1 and ratings[i] == ratings[i+1]:
            i += 1
            streak += 1

        return streak, i

    def candy(self, ratings: List[int]) -> int:
        n = len(ratings)
        print(f"{n=} {ratings=}")

        """
        Base case: one child must receive exactly one candy.
        Example: [7] -> answer is 1.
        """
        if n == 1:
            return 1
        
        total = 0
        i = 0
        prev = 0

        """
        We process contiguous segments (uphill / downhill / flat) one by one.
        `prev` tracks the candy value at the segment boundary's last child so we can
        remove overlap when the next segment also includes that same boundary child.
        """
        while True:
            dir = self.get_dir(ratings, i)

            if dir == None:
                # reached ending
                break

            if dir == 1:
                streak, i = self.up_streak(ratings, i)

                """
                For an uphill streak of length k, minimal candies are 1..k, whose sum is
                k*(k+1)/2. This enforces strictly increasing candies with minimum total.
                Example: ratings pattern 1<2<3 (k=3) -> candies 1,2,3 -> sum 6.
                """
                # add the sum of numbers from 1,2 ... streak count and remove the previous value as the new streak starts from 1
                total += streak * (streak + 1) // 2
                """
                Remove `prev` because the first child of this segment was already counted
                as the last child of the previous segment.
                Example: previous segment ended with candy 2, current formula starts again
                from 1 at the same index; subtract old contribution to avoid double count.
                """
                total -= prev

                """
                End of an increasing run gets the largest candy value, equal to streak.
                We store it so the next segment can reconcile peak overlap correctly.
                """
                prev = streak # last value is the streak

            elif dir == -1:
                streak, i = self.down_streak(ratings, i)

                """
                A downhill streak also contributes triangular count k*(k+1)/2 when viewed
                from left to right as k,k-1,...,1.
                Example: 5>4>3 (k=3) -> candies 3,2,1 -> sum 6.
                """
                # same logic as the ascending case
                total += streak * (streak + 1) // 2
                """
                Remove previously counted boundary child for the same overlap reason as
                the uphill case.
                """
                total -= prev
                
                """
                The triangular downhill sum assumes the left boundary (peak) is exactly k.
                But an earlier uphill might have already assigned a larger peak via `prev`.
                So:
                - subtract assumed peak `k`
                - add back max(k, prev) to keep both neighbor constraints valid
                Example: ... up gave peak=5, then down length k=3.
                Raw down part assumes peak 3 (3,2,1), but we must keep peak 5 (5,2,1).
                """
                # starting of the downhill could be higher -> so just replace peak
                # e.g. we might have a streak of 3 => 3 2 1. But the starting point could have already been a 5. In which case we need it to be 5 2 1 eventually. Therefore we just remove the 3 and add the 5
                total -= streak
                total += max(streak, prev)

                
                """
                End of any decreasing run always has candy 1 (strictly descending to the
                minimum valid candy), so this becomes the new boundary value.
                """
                prev = 1 # last value in dec sequence is 1

            else:
                streak, i = self.same_streak(ratings, i)

                """
                In an equal-rating run of length k, each extra child beyond the first can
                safely receive 1 candy because there is no strict inequality requirement.
                So we add k-1 new ones here.
                Example: [3,3,3] contributes 1,1,1; if first already covered, add 2.
                """
                # ignoring the first one everything else is just 1
                total += streak - 1

                """
                If this is effectively the first processed segment (`prev == 0`), the
                plateau's first child has not yet been counted, so add its 1 candy now.
                Example: ratings starts with [2,2,...] -> first child still needs candy.
                """
                # in case the very first streak is the one where everything is same we also need to add 1
                if prev == 0:
                    total += 1

                """
                Flat segments end with candy 1 at the boundary child for subsequent
                overlap handling.
                """
                prev = 1 # the ending in the sequence is going to be a 1

        return total