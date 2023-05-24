def sortStack(stack):
    if len(stack) == 0:
        return []

    top = stack.pop()

    #sort the rest
    stack = sortStack(stack)

    return insertAtCorrectPlace(top, stack)



def insertAtCorrectPlace(val, stack):
    if len(stack) == 0:
        stack.append(val)
        return stack

    if val > stack[-1]:
        stack.append(val)
        return stack

    top = stack.pop()
    insertAtCorrectPlace(val, stack)
    stack.append(top)

    return stack

if __name__ == '__main__':
    stack = [-5, 2, 1, 4, 0, 3, -1]
    # stack = [0, 2, 1]
    print(sortStack(stack))
