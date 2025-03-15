'''
given n cities where i -> i+1 has a distance[i] and to travel it you need to have fuel[i] * miles per gallon at that city > distance[i]

going in clockwise direction is there a point where we go all the way around and reach this city back?
'''


def simulateAndFindNext(deficits):
    total = 0
    for i, d in enumerate(deficits):
        total += d
        if total < 0:
            return (i + 1) % len(deficits), False
    return 0, True


def validStartingCity(distances, fuel, mpg):
    n = len(distances)
    deficits = [(f * mpg) - d for f, d in zip(fuel, distances)]

    # simulate with these deficits
    i = 0
    while i < n:
        skip, possible = simulateAndFindNext(deficits[i:] + deficits[:i])
        if possible:
            return i
        else:
            i = (i + skip) % n


if __name__ == '__main__':
    distances = [5, 25, 15, 10, 15]
    fuel = [1, 2, 1, 0, 3]
    mpg = 10
    print(validStartingCity(distances, fuel, mpg))
