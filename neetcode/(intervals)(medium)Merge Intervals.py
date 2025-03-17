from typing import List
from functools import reduce

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        def try_merging(merged_intervals, interval):
            if not merged_intervals or merged_intervals[-1][1] < interval[0]:
                merged_intervals.append(interval)
            else:
                merged_intervals[-1][1] = max(merged_intervals[-1][1], interval[1])
            return merged_intervals


        intervals.sort(key=lambda interval: interval[0])
        return list(reduce(try_merging, intervals, []))

    def tryMerging(self, interval, merger):
        start, end = interval
        isIntervalMergable = merger[-1][0] <= start and start <= merger[-1][1]
        if isIntervalMergable:
            newIntervalEnd = max(end, merger[-1][1])
            newIntervalStart = min(start, merger[-1][0])
            merger.pop()
            merger.append([newIntervalStart, newIntervalEnd])
        else:
            merger.append(interval)
        # print(f"state of merger after {merger}")
        return merger

    def merge_manual(self, intervals: List[List[int]]) -> List[List[int]]:
        # edge case taken care of
        if len(intervals) == 1:
            return intervals

        # sort the array in ascending starting time first
        intervals.sort(key=lambda interval: interval[0])

        # print(f"intervals after sorting {intervals}")

        # merge in a reductive manner
        merger = [intervals[0]]
        i = 1
        while i < len(intervals):
            merger = self.tryMerging(intervals[i], merger)
            i += 1

        # print(f"final merger is {merger}")
        return merger

