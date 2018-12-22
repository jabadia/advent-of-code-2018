from collections import namedtuple

TestCase = namedtuple('TestCase', 'case expected')

INPUT = """
depth: 5355
target: 14,796
"""


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase("""
depth: 510
target: 10, 10
""", 114),
]


def solve(input):
    for line in input.strip().split('\n'):
        if 'depth' in line:
            depth = int(line[6:])
        elif 'target' in line:
            maxx, maxy = [int(n) for n in line[7:].split(',')]

    geologic_index = [[0] * (maxx + 1) for y in range(0, maxy + 1)]
    erosion_level = [[0] * (maxx + 1) for y in range(0, maxy + 1)]

    # mouth
    geologic_index[0][0] = 0

    # first row
    for x in range(1, maxx + 1):
        geologic_index[0][x] = x * 16807
        erosion_level[0][x] = (geologic_index[0][x] + depth) % 20183

    # first column
    for y in range(1, maxy + 1):
        geologic_index[y][0] = y * 48271
        erosion_level[y][0] = (geologic_index[y][0] + depth) % 20183

    # rest
    for i in range(1, max(maxx, maxy)):
        for y in range(i, maxy + 1):
            for x in range(i, maxx + 1):
                geologic_index[y][x] = erosion_level[y - 1][x] * erosion_level[y][x - 1]
                erosion_level[y][x] = (geologic_index[y][x] + depth) % 20183

    return sum(sum(level % 3 for level in row) for row in erosion_level) - erosion_level[maxy][maxx] % 3


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        check_case(case, result)

    print(solve(INPUT))
