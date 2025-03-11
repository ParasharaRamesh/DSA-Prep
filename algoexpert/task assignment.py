def taskAssignment(k, tasks):
    results = []
    taskIndices = [(task, i) for i, task in enumerate(tasks)]
    taskIndices.sort(key=lambda x: x[0])

    for i in range(k):
        item = [taskIndices[i][1], taskIndices[2*k - 1 - i][1]]
        results.append(item)

    return results


if __name__ == '__main__':
    k = 3
    tasks = [1, 3, 5, 3, 1, 4]
    print(taskAssignment(k, tasks))
