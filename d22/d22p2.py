from collections import namedtuple, deque
import heapq

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
""", 45),
]

ROCKY = 0  # climb or torch
WET = 1  # climb or neither
NARROW = 2  # torch or neither

TORCH = 'torch'
CLIMBING = 'climbing'
NEITHER = 'neither'

NEIGHBOURS = [(1, 0), (-1, 0), (0, -1), (0, 1)]


def advance(pos, delta):
    return (pos[0] + delta[0], pos[1] + delta[1])


def solve(input):
    for line in input.strip().split('\n'):
        if 'depth' in line:
            depth = int(line[6:])
        elif 'target' in line:
            maxx, maxy = [int(n) for n in line[7:].split(',')]

    target = (maxy, maxx)
    maxy *= 2
    maxx *= 2

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

    # map
    map = [[level % 3 for level in row] for row in erosion_level]
    map[target[0]][target[1]] = ROCKY

    cell = {
        ROCKY: '.',
        NARROW: '|',
        WET: '=',
    }
    # for row in map:
    #     print(''.join([cell[c] for c in row]))
    # bfs
    queue, visited = [(0, (0, 0), TORCH, [(0, 0, TORCH, cell[map[0][0]])])], set()
    while queue:
        time, pos, equipment, path = heapq.heappop(queue)
        if pos == target:
            return time + (7 if equipment != TORCH else 0)
        if (pos, equipment) in visited:
            continue
        visited.add((pos, equipment))
        py, px = pos
        current_type = map[py][px]
        for neighbour in [advance(pos, delta) for delta in NEIGHBOURS]:
            ny, nx = neighbour
            if nx < 0 or ny < 0 or nx >= maxx + 1 or ny >= maxy + 1:
                continue
            neighbour_type = map[ny][nx]
            next_equipment = equipment
            if neighbour_type != current_type:
                if neighbour_type == ROCKY:
                    if equipment == NEITHER:
                        next_equipment = TORCH if current_type == NARROW else CLIMBING
                elif neighbour_type == WET:
                    if equipment == TORCH:
                        next_equipment = NEITHER if current_type == NARROW else CLIMBING
                elif neighbour_type == NARROW:
                    if equipment == CLIMBING:
                        next_equipment = NEITHER if current_type == WET else TORCH
            heapq.heappush(queue, (
                time + 1 + (7 if next_equipment != equipment else 0),
                neighbour,
                next_equipment,
                path + [(ny, nx, next_equipment, cell[map[ny][nx]])]))


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        check_case(case, result)

    print(solve(INPUT))
