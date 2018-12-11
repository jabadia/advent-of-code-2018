from collections import namedtuple

TestCase = namedtuple('TestCase', 'case expected')

INPUT = 3031


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase(18, (33, 45)),
    TestCase(42, (21, 61)),
]


def power_level(x, y, serial):
    rack_id = x + 10
    power_level = ((rack_id * y) + serial) * rack_id
    # hundreds = int(str(power_level)[-3])
    hundreds = (power_level // 100) % 10
    return hundreds - 5


assert power_level(3, 5, 8) == 4
assert power_level(122, 79, 57) == -5
assert power_level(217, 196, 39) == 0
assert power_level(101, 153, 71) == 4

DIM = 300


def square_level(grid, x, y):
    return (
            grid[x * DIM + y] + grid[(x + 1) * DIM + y] + grid[(x + 2) * DIM + y] +
            grid[x * DIM + y + 1] + grid[(x + 1) * DIM + y + 1] + grid[(x + 2) * DIM + y + 1] +
            grid[x * DIM + y + 2] + grid[(x + 1) * DIM + y + 2] + grid[(x + 2) * DIM + y + 2]
    )


def solve(input):
    serial = input
    grid = [-999] * DIM * DIM
    for x in range(0, DIM):
        for y in range(0, DIM):
            grid[x * DIM + y] = power_level(x + 1, y + 1, serial)

    max_level = -999
    max_cell = None
    for x in range(0, DIM - 3):
        for y in range(0, DIM - 3):
            level = square_level(grid, x, y)
            if level > max_level:
                max_cell = (x + 1, y + 1)
                max_level = level
    return max_cell


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        check_case(case, result)

    print(solve(INPUT))
