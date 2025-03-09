class MinMaxStack:
    def __init__(self):
        # (ele, min, max)
        self.stack = []

    def peek(self):
        if self.stack:
            return self.stack[-1][0]
        return None

    def pop(self):
        if self.stack:
            ele, _, _ = self.stack.pop()
            return ele
        return None

    def push(self, number):
        if not self.stack:
            self.stack.append([number, number, number])
        else:
            _, existingMin, existingMax = self.stack[-1]
            self.stack.append([number, min(existingMin, number), max(existingMax, number)])

    def getMin(self):
        if self.stack:
            _, min, _ = self.stack[-1]
            return min
        return None

    def getMax(self):
        if self.stack:
            _, _, max = self.stack[-1]
            return max
        return None