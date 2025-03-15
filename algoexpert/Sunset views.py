from collections import deque

'''
Given an array of buildings facing a particular direction (east of west). 
A building is said to see the sunset only iff all the buildings that follow it in that direction are strictly smaller than itself.
 So find out the indices of the buildings which can see the sunset

'''

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