from collections import deque

def sunsetViews(buildings, direction):
    if len(buildings) == 0:
        return []

    buildingsWithIndex = []
    for i, building in enumerate(buildings):
        buildingsWithIndex.append((i, building))

    stack = deque([])

    if direction == "EAST":
        buildingsWithIndex.reverse()
        for i, building in buildingsWithIndex:
            if len(stack) == 0:
                stack.appendleft(i)
                continue

            if building > buildings[stack[0]]:
                stack.appendleft(i)

    elif direction == "WEST":
        for i, building in buildingsWithIndex:
            if len(stack) == 0:
                stack.append(i)
                continue

            if building > buildings[stack[-1]]:
                stack.append(i)

    return list(stack)


if __name__ == '__main__':
    buildings = [3, 5, 4, 4, 3, 1, 3, 2]
    directions = "EAST" #should be [1,3,6,7]
    # directions = "WEST" #should be [0,1]

    print(sunsetViews(buildings, directions))