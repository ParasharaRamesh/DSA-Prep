from typing import List


class Solution:
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

    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
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

