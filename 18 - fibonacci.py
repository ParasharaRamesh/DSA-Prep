from functools import lru_cache


@lru_cache(maxsize=None)
def getNthFib(num):
    if num == 1:
        return 0

    # check if num between 1, 0
    # it will return num
    elif num == 2:
        return 1

    # return the fibonacci of num - 1 & num - 2
    return getNthFib(num - 1) + getNthFib(num - 2)

if __name__ == '__main__':
    print(getNthFib(1))
    print(getNthFib(2))
    print(getNthFib(3))
    print(getNthFib(4))
    print(getNthFib(5))
    print(getNthFib(6))