def minimumWaitingTime(queries):
    queries.sort()
    cumm = [0]
    for x in queries[:-1]:
        cumm.append(cumm[-1] + x)

    return sum(cumm)
