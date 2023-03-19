from collections import Counter


def generateDocument(characters, document):
    charCount = Counter(characters)
    docCount = Counter(document)
    for key in docCount:
        if not (key in charCount and docCount[key] <= charCount[key]):
            return False

    return True


if __name__ == "__main__":
    print(generateDocument("Bste!hetsi ogEAxpelrt x ","AlgoExpert is the Best!"))