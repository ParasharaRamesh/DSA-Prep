'''
You are given an array of non-overlapping intervals intervals where intervals[i] = [start_i, end_i] represents the start and the end time of the ith interval. intervals is initially sorted in ascending order by start_i.

You are given another interval newInterval = [start, end].

Insert newInterval into intervals such that intervals is still sorted in ascending order by start_i and also intervals still does not have any overlapping intervals. You may merge the overlapping intervals if needed.

Return intervals after adding newInterval.

Note: Intervals are non-overlapping if they have no common point. For example, [1,2] and [3,4] are non-overlapping, but [1,2] and [2,3] are overlapping.

Example 1:

Input: intervals = [[1,3],[4,6]], newInterval = [2,5]

Output: [[1,6]]
Example 2:

Input: intervals = [[1,2],[3,5],[9,10]], newInterval = [6,7]

Output: [[1,2],[3,5],[6,7],[9,10]]
Constraints:

0 <= intervals.length <= 1000
newInterval.length == intervals[i].length == 2
0 <= start <= end <= 1000

'''

from bisect import *


class Solution:
    def canMerge(self, interval_a, interval_b):
        intervals = list(sorted([interval_a, interval_b], key=lambda interval: interval[0]))
        print(f"inside can merge intervals is {intervals}")
        a_s, a_e = intervals[0]
        b_s, b_e = intervals[1]

        return a_e >= b_s

    def mergeTwo(self, lastInterval, currInterval):
        return [min(lastInterval[0], currInterval[0]), max(lastInterval[1], currInterval[1])]

    def merge(self, intervals, i, j, newInterval):
        start = max(0, i - 1)
        end = min(j + 1, len(intervals))

        res = []

        print(f"start: {start}, end: {end}")

        for k in range(start, end):
            if k == start:
                if self.canMerge(intervals[k], newInterval):
                    res.append(self.mergeTwo(intervals[k], newInterval))
                else:
                    res.append(intervals[k])
                    res.append(newInterval)
                    res.sort(key=lambda k: k[0])
                print(f"init case res is {res}")
                continue

            curr_interval = intervals[k]

            if self.canMerge(res[-1], curr_interval):
                print(f"can merge {res[-1]} & {curr_interval}")
                last_interval = res[-1]
                res.pop()
                res.append(self.mergeTwo(last_interval, curr_interval))
            else:
                print(f"cannot merge {res[-1]} & {curr_interval}")
                res.append(curr_interval)
            print(f"res is {res} after k: {k}")

        return res

    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        if len(intervals) == 0:
            return [newInterval]

        start, end = newInterval
        i = bisect_left(intervals, start, key=lambda interval: interval[0])
        j = bisect_left(intervals, end, key=lambda interval: interval[1])

        l_u = intervals[:i - 1] if 0 <= i - 1 < len(intervals) else []
        r_u = intervals[j + 1:] if 0 <= j + 1 < len(intervals) else []
        print(f'i : {i}, j: {j}, left untouched: {l_u}, right untouched: {r_u}')

        return l_u + self.merge(intervals, i, j, newInterval) + r_u