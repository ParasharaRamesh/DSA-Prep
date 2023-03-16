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