"""
Min Stack (#155) - Medium
Pattern: Stack
"""


class MinStack:
    def __init__(self):
        self.stack = []

    def push(self, val: int) -> None:
        if not self.stack:
            cur_min = val
        else:
            cur_min = min(val, self.stack[-1][1])
        self.stack.append([val, cur_min])

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]


# Tests
ms = MinStack()
ms.push(-2)
ms.push(0)
ms.push(-3)
print(ms.getMin())  # -3
ms.pop()
print(ms.top())  # 0
print(ms.getMin())  # -2
