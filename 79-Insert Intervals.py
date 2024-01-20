from bisect import *
from typing import *

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

        # print(f"intervals after sorting {intervals}")

        # merge in a reductive manner
        merger = [intervals[0]]
        i = 1
        while i < len(intervals):
            merger = self.tryMerging(intervals[i], merger)
            i += 1

        # print(f"final merger is {merger}")
        return merger

    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        # option 1. use python's inbuilt binarySearch
        # insort(intervals, newInterval, key=lambda interval: interval[0])

        # option 2. my own binary search
        intervals = self.binarySearcher(intervals, newInterval)
        return self.merge(intervals)

    def binarySearcher(self, intervals, newInterval):
        startTimes = list(map(lambda interval: interval[0], intervals))
        start, end = newInterval

        first = 0
        last = len(startTimes) - 1

        # print(f"startTimes {startTimes}")

        while first <= last:
            mid = (first + last) // 2
            # print(f"first: {first} | last: {last} | mid: {mid}")
            if start >= startTimes[mid]:
                # print(" -> changing first")
                first = mid + 1  # or mid+1?
            elif start < startTimes[mid]:
                # print(" -> changing last")
                last = mid - 1

        # print(f"after loop first {first} & last {last}")
        # place to insert
        i = last + 1
        # print(f"i is {i}")
        intervals.insert(i, newInterval)
        # print(f"after insert {intervals}")
        return intervals

