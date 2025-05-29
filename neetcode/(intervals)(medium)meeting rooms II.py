'''
Given an array of meeting time interval objects consisting of start and end times [[start_1,end_1],[start_2,end_2],...] (start_i < end_i), find the minimum number of days required to schedule all meetings without any conflicts.

Example 1:

Input: intervals = [(0,40),(5,10),(15,20)]

Output: 2
Explanation:
day1: (0,40)
day2: (5,10),(15,20)

Example 2:

Input: intervals = [(4,9)]

Output: 1
Note:

(0,8),(8,10) is not considered a conflict at 8

Constraints:

0 <= intervals.length <= 500
0 <= intervals[i].start < intervals[i].end <= 1,000,000

Thoughts:

* strictly lesser + not neccesarily sorted
* (0,8) - (8,10) not a conflict
* if any is overlapping schedule to next day, but what about minimum?
* similar logic to min non overlapping? just keep track of the longer one in another. (Turns out this lead me astray, just greedily process whatever you can in each day and throw any overlapping ones to the next day)
* pop once processed.
* day++ when intervals is empty/processed


'''

from typing import List
from collections import deque, defaultdict


class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"({self.start},{self.end})"

class Solution:
    def minMeetingRooms(self, intervals: List[Interval]) -> int:
        intervals.sort(key=lambda x: x.start)
        intervals = deque(intervals)

        days = 0
        next_day = []

        # keep popping and empty it, increment day when intervals is empty
        while len(intervals) > 0 or len(next_day) > 0:
            # process this day
            curr_day_prev_interval = None

            while len(intervals) > 0:
                interval = intervals.popleft()

                if not curr_day_prev_interval:
                    curr_day_prev_interval = interval
                    continue

                #overlapping case: which ever finishes earlier, keep that as the prev one and put the other one for next day
                if curr_day_prev_interval.end > interval.start:
                    # throw the new one for next day and keep prev_interval as same
                    next_day.append(interval)
                else:
                    #non overlapping, just assign it to the next one
                    curr_day_prev_interval = interval

            # assigning next day as curr day
            if not intervals:
                days += 1
                intervals = deque(next_day)
                next_day.clear()

        return days

    # optimal way to do it, sort both by start and end times, and increment count when meeting is on and decrement count when a meeting is over, can technically use a minheap instead of the sorted end array also
    def minMeetingRooms_sorting_two_pointers(self, intervals: List[Interval]) -> int:
        start = sorted([i.start for i in intervals])
        end = sorted([i.end for i in intervals])

        res = count = 0
        s = e = 0
        while s < len(intervals):
            if start[s] < end[e]:
                s += 1
                count += 1
            else:
                e += 1
                count -= 1
            res = max(res, count)
        return res

    # Scan line variant
    def minMeetingRooms_sweep_line(self, intervals: List[Interval]) -> int:
        mp = defaultdict(int)
        for i in intervals:
            mp[i.start] += 1
            mp[i.end] -= 1
        prev = 0
        res = 0
        for i in sorted(mp.keys()):
            prev += mp[i]
            res = max(res, prev)
        return res

if __name__ == '__main__':
    s = Solution()

    intervals = [Interval(0,40),Interval(5,10),Interval(15,20)]
    # days = s.minMeetingRooms(intervals)
    # days = s.minMeetingRooms_sorting_two_pointers(intervals)
    days = s.minMeetingRooms_sweep_line(intervals)
    expected = 2
    assert days == expected, f"expected {expected}, got {days}"

    intervals = [Interval(2,15),Interval(36,45),Interval(9,29),Interval(16,23),Interval(4,9)]
    days = s.minMeetingRooms(intervals)
    expected = 2
    assert days == expected, f"expected {expected}, got {days}"


    intervals = [Interval(4,9)]
    days = s.minMeetingRooms(intervals)
    expected = 1
    assert days == expected, f"expected {expected}, got {days}"