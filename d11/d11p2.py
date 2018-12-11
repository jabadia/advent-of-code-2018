from collections import namedtuple, defaultdict

TestCase = namedtuple('TestCase', 'case expected')

INPUT = 3031


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase(18, (90, 269, 16)),
    TestCase(42, (232, 251, 12)),
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


def solve(input): # grid is a dict ( (x,y) -> level )
    serial = input
    grid = defaultdict(int)
    for x in range(1, DIM + 1):
        for y in range(1, DIM + 1):
            grid[(x, y)] = power_level(x, y, serial)

    def square_level(grid, x, y, size, prev_level):
        return prev_level[(x, y)] + \
               sum(grid[(xx, y + size - 1)] for xx in range(x, x + size)) + \
               sum(grid[(x + size - 1, yy)] for yy in range(y, y + size - 1))

    max_level = -999
    max_cell = None
    levels_for_prev_size = grid.copy()
    levels_for_size = defaultdict(int)
    for size in range(2, 31):
        print(size, max_cell, max_level)
        for x in range(1, DIM - size + 1):
            for y in range(1, DIM - size + 1):
                level = square_level(grid, x, y, size, levels_for_prev_size)
                levels_for_size[(x, y)] = level
                if level > max_level:
                    max_cell = (x, y, size)
                    max_level = level
        levels_for_prev_size = levels_for_size
        levels_for_size = defaultdict(int)
    return max_cell


def solve1(input):  # grid is a list
    serial = input
    grid = [-999] * DIM * DIM
    for x in range(0, DIM):
        for y in range(0, DIM):
            grid[x * DIM + y] = power_level(x + 1, y + 1, serial)

    def square_level(grid, x, y, size, prev_level):
        return prev_level[x * DIM + y] + \
               sum(grid[xx * DIM + (y + size - 1)] for xx in range(x, x + size)) + \
               sum(grid[(x + size - 1) * DIM + yy] for yy in range(y, y + size - 1))

    max_level = -999
    max_cell = None
    levels_for_prev_size = grid[:]
    levels_for_size = [-999] * DIM * DIM
    for size in range(2, 30):
        print(size)
        for x in range(0, DIM - size):
            for y in range(0, DIM - size):
                level = square_level(grid, x, y, size, levels_for_prev_size)
                levels_for_size[x * DIM + y] = level
                if level > max_level:
                    max_cell = (x + 1, y + 1, size)
                    max_level = level
        levels_for_prev_size = levels_for_size
        levels_for_size = [-999] * DIM * DIM
    return max_cell


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        check_case(case, result)

    print(solve(INPUT))
