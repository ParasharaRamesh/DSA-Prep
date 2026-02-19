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
import heapq


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

    def eraseOverlapIntervalsActivitySelection(self, intervals: List[List[int]]) -> int:
        """
        A Scan Line approach using 'Activity Selection' logic.
        
        Concept: Moving along the end points (completion times). 
        By sorting by end times, we greedily pick the interval that finishes 
        earliest, which leaves the maximum possible space for future intervals.
        """
        if not intervals:
            return 0
            
        # Sort by end time
        intervals.sort(key=lambda x: x[1])
        
        non_overlapping_count = 0
        last_end_time = float('-inf')
        
        for start, end in intervals:
            # If current interval starts after or at the last one's end time
            if start >= last_end_time:
                non_overlapping_count += 1
                last_end_time = end
        
        # Minimum removals = Total - Maximum non-overlapping
        return len(intervals) - non_overlapping_count

    def eraseOverlapIntervalsEventBased(self, intervals: List[List[int]]) -> int:
        """
        A Point-based Scan Line approach (Sweep Line).
        
        Concept: Treat starts and ends as separate events. When an overlap occurs, 
        use a Max-Heap to greedily remove the interval that ends the latest 
        (the one most likely to cause future overlaps).
        """
        if not intervals:
            return 0
            
        # 1. Create events: (time, type, interval_index)
        # type -1 for END, 1 for START (ENDs before STARTs at same time to handle boundaries)
        events = []
        for i, (s, e) in enumerate(intervals):
            events.append((s, 1, i))
            events.append((e, -1, i))
        
        # 2. Sort event points
        events.sort()
        
        active_count = 0
        removals = 0
        removed = [False] * len(intervals)
        max_heap = [] # Stores (-end_time, index) to simulate max-heap
        
        # 3. Scan the events
        for time, kind, idx in events:
            if kind == 1: # START
                active_count += 1
                heapq.heappush(max_heap, (-intervals[idx][1], idx))
                
                # If an overlap is detected, we must remove one
                if active_count > 1:
                    # Remove the most "costly" interval (the one ending latest)
                    _, latest_idx = heapq.heappop(max_heap)
                    removed[latest_idx] = True
                    active_count -= 1
                    removals += 1
            else: # END
                # Only decrement if the interval wasn't already removed
                if not removed[idx]:
                    active_count -= 1
                    
        return removals


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
