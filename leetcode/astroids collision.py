def canCollide(x, y):
    return x > 0 and y < 0


def simulateCollisions(survivors):
    if len(survivors) == 1:
        return survivors

    if survivors[-1] > 0:
        # no need to check anything
        return survivors

    while len(survivors) >= 2 and canCollide(survivors[-2], survivors[-1]):
        penultimate = survivors[-2]
        top = survivors[-1]
        if abs(penultimate) == abs(top):
            survivors.pop()
            survivors.pop()
        elif abs(penultimate) < abs(top):
            survivors.pop(-2)
        else:
            survivors.pop()

    return survivors


def collidingAsteroids(asteroids):
    survivors = []
    for asteroid in asteroids:
        survivors.append(asteroid)
        survivors = simulateCollisions(survivors)
    return survivors


if __name__ == '__main__':
    asteroids = [-3, 5, 6, -8, 9, -9, 10]
    print(collidingAsteroids(asteroids))
