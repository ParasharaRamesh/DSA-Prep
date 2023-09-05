def optimalFreelancing(jobs):
    if len(jobs) == 0:
        return 0

    bestPayments = [0] * 7

    # sort by payment first
    jobs.sort(key=lambda job: job["payment"], reverse=True)

    # greedily fill the values as late as possible
    for job in jobs:
        deadline, payment = job["deadline"], job["payment"]
        slotIndex = min(deadline - 1, len(bestPayments) - 1)

        #while there is no slot keep going down one by one and slot it there
        while bestPayments[slotIndex] > 0 and slotIndex > 0:
            slotIndex -= 1

        #only if it is free we can even put it in
        if slotIndex >= 0 and bestPayments[slotIndex] == 0:
            bestPayments[slotIndex] = payment

    return sum(bestPayments)


if __name__ == '__main__':
    jobs = [
        {
            "deadline": 2,
            "payment": 1
        },
        {
            "deadline": 1,
            "payment": 4
        },
        {
            "deadline": 3,
            "payment": 2
        },
        {
            "deadline": 1,
            "payment": 3
        },
        {
            "deadline": 4,
            "payment": 3
        },
        {
            "deadline": 4,
            "payment": 2
        },
        {
            "deadline": 4,
            "payment": 1
        },
        {
            "deadline": 5,
            "payment": 4
        },
        {
            "deadline": 8,
            "payment": 1
        }
    ]
    print(optimalFreelancing(jobs))
