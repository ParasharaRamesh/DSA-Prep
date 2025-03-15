'''
We are given two non-empty arrays of positive integers: the first is going to represent the heights of students wearing red shirts and the second is going to represent the heights of students wearing blue shirts.
The two arrays will always have the same length.
We are asked to write a function that is going to find out if we can take a photo of these students that satisfies the following constraints:

All the students that are wearing red shirts must be in the same row;
All of the students that are wearing blue shirts must be in the same row;
The photo must have exactly two rows and the two rows must have the same number of students in them.
Every student in the front row must be shorter than the student directly behind them in the back row.
The function is going to arrange the students and return true if we can take a photo that follows these constraints; otherwise return false.


'''

def classPhotos(redShirtHeights, blueShirtHeights):
    redShirtHeights.sort(reverse = True)
    blueShirtHeights.sort(reverse = True)

    isRedInBackRow = redShirtHeights[0] > blueShirtHeights[0]
    isEqual = redShirtHeights[0] == blueShirtHeights[0]

    if isEqual:
        return False


    for red, blue in zip(redShirtHeights[1:], blueShirtHeights[1:]):
        if red == blue:
            return False
        if isRedInBackRow and blue > red:
            return False
        elif not isRedInBackRow and red > blue:
            return False

    return True


if __name__ == "__main__":
    print(classPhotos([6, 9, 2, 4, 5],[5, 8, 1, 3, 4]))