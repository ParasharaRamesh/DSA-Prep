'''
Given an array of intervals intervals where intervals[i] = [start_i, end_i], return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.

Note: Intervals are non-overlapping even if they have a common point. For example, [1, 3] and [2, 4] are overlapping, but [1, 2] and [2, 3] are non-overlapping.

Example 1:

Input: intervals = [[1,2],[2,4],[1,4]]

Output: 1
Explanation: After [1,4] is removed, the rest of the intervals are non-overlapping.

Example 2:

Input: intervals = [[1,2],[2,4]]

Output: 0
Constraints:

1 <= intervals.length <= 1000
intervals[i].length == 2
-50000 <= starti < endi <= 50000

Insights:
* sort
* keep track of only the recent most interval
* when checking curr interval with recent interval, check if they are overlapping:
    - if so count ++
    - keep the interval which has a lower finish, and throw away the other interval which finishes later. This ensures that we dont count more overlaps in the future.

'''

from typing import List
from collections import OrderedDict


class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        count_overlaps = 0

        intervals.sort(key=lambda interval: interval[0])

        prev_interval = intervals[0]
        for interval in intervals[1:]:
            # overlapping case
            if prev_interval[1] > interval[0]:
                count_overlaps += 1

                #keep the one which finishes first so that there is less chance of overlapping with future intervals
                if prev_interval[1] >= interval[1]:
                    # essentially change pre interval
                    prev_interval = interval
                # in the else case we continue to retain prev_interval as that finished earlier
            else:
                prev_interval = interval

        return count_overlaps


if __name__ == '__main__':
    s = Solution()
    intervals = s.eraseOverlapIntervals([[1, 100], [11, 22], [1, 11], [2, 12]])
    assert intervals == 2, f"expected 2 was {intervals} instead"  # 2

    overlap_intervals = s.eraseOverlapIntervals([[1, 2], [2, 3], [3, 4], [1, 3]])
    assert overlap_intervals == 1, f"expected 1 was {overlap_intervals} instead"  # 1

    erase_overlap_intervals = s.eraseOverlapIntervals([[1, 2], [1, 2], [1, 2]])
    assert erase_overlap_intervals == 2, f"expected 2 was {erase_overlap_intervals} instead"  # 2

    i = s.eraseOverlapIntervals([[1, 2], [2, 4], [1, 4]])
    assert i == 1, f"expected 1 was {i} instead"

    intervals1 = s.eraseOverlapIntervals([[1, 2], [2, 4]])
    assert intervals1 == 0, f"expected 0 was {intervals1} instead"
