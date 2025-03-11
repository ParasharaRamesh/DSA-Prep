def mergeOverlappingIntervals(intervals):
    # sort with first index
    intervals.sort(key=lambda x: x[0])

    i = 0

    # merge adjacent ones
    while i < len(intervals) - 1:
        if intervals[i][1] >= intervals[i + 1][0] and intervals[i][1] <= intervals[i + 1][1]:
            # modify currentInterval
            intervals[i][1] = intervals[i + 1][1]

            # modify intervals , include ith and leave the next one as its merged!
            intervals = intervals[:i + 1] + intervals[i + 2:]

            # index should reamin the same to merge with next potential interval!
            continue
        elif intervals[i][1] >= intervals[i + 1][0] and intervals[i][1] >= intervals[i + 1][1]:
            # no need to modify currentInterval! include ith and leave the next one as its merged!
            intervals = intervals[:i + 1] + intervals[i + 2:]

            # index should reamin the same to merge with next potential interval!
            continue

        i += 1

    return intervals


if __name__ == '__main__':
    # intervals = [
    #     [1, 2],
    #     [3, 5],
    #     [4, 7],
    #     [6, 8],
    #     [9, 10]
    # ]

    intervals = [
        [1, 22],
        [-20, 30]
    ]

    print(mergeOverlappingIntervals(intervals))
