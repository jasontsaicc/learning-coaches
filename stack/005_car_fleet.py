from typing import List


class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        # Plan:
        # 1. pair each car as (position, speed), sort by position DESC (closest to target first)
        # 2. walk front -> back, push a car's time-to-target onto stack when it can't
        #    catch the fleet ahead (its time > stack top)
        # 3. return len(stack) = number of fleets
        #
        # time-to-target for a car = (target - position) / speed
        # your code here
        stack = []
        cars = []
        # [(10,2), (8,4), (5,1), (3,3), (0,1)]
        for i in range(len(position)):
            cars.append((position[i], speed[i]))
        cars.sort(reverse=True)
        for p, s in cars:
            time = (target - p) / s
            if not stack or time > stack[-1]:
                stack.append(time)

        return len(stack)


# --- tests ---
if __name__ == "__main__":
    s = Solution()

    assert s.carFleet(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]) == 3
    assert s.carFleet(10, [3], [3]) == 1  # single car
    assert s.carFleet(10, [0, 4], [2, 1]) == 1  # fast behind catches slow ahead
    assert s.carFleet(10, [4, 0], [1, 2]) == 1  # same two cars, input order swapped
    assert s.carFleet(100, [0, 2, 4], [4, 2, 1]) == 1  # all merge into one
    assert s.carFleet(10, [6, 8], [3, 2]) == 2  # ahead car faster -> never caught
    print("all passed")
