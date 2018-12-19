from collections import namedtuple

TestCase = namedtuple('TestCase', 'case minutes expected')

INPUT = """
...|||......|||........#..|...|.......#||.||.#|.#|
..##.|.||...||.|.#....||..|......|.#..#||.|#..|##.
.|...|....|.|.##...|#...|...#...#.#|.#............
|#.||.|..#.#..|...#..#..|.|..#...#..#...|##....|##
.|.........#.|.#.........|..#....|..##..##........
.#|##.||.........||||#..#|#|.||...|..|...#.||...#.
...|....#...|....|#.#.#..#..#.#....#|..|#...|.|...
.|....#|.|.#|###.|..|..|.#|.###|.##..|.#....|.||..
|..|#.|..#.#...#|#....#...|..|......#|.#.|||..|#.#
....##||..#....|.|...|###.#.|.|#.|..##.....||...|.
....#.#|..#|##..#........#.#....|......###|#|##.|#
|..##.###.#.###.......|..|#|.|..|#.#....#|..|#..#|
....##.#..###.......|.|.|..#..##....#|..|...#.|...
..##...|..#.|....#.#.|###..|....|||.|.|.|....|#.#.
|..|#|....#|.#..#|.#..|.#..|#.|.|..|##|||.#.##.|..
.....#.|#|.|.#......#.#..#.#|...#.|.#|........#...
|.#.#.#..|.|.#.|||..|..|##|.##...#.|...##|...#....
..|.#..#....|..|.|.#.|#..|##.....|.....|....##..||
.|.#.#.#...||.|#...|........|..|#....#.|#..#|.|.|.
#..#.#............#.#.|.|#.||..|#....#.|.#|.##....
|.....|#..#|.|...|.#||.#||.......#.||..|.||.####..
#..#......#||.#..##...#.####..#|.#.|...|#.##|.#..|
...|..#|.||.|###...##.......|....#.|.||.|#|#..#..#
...#.#|...#|||...#|..||.#....|.|..#..|...#|.#...|.
.#|..#.|||.|##|.|#.#....|..|.|.##.#.#|#..#.#|..||#
.#.|#.#..####...|.#|#..#.|...#|#.|.##.|...##..#.||
...#..#|..##|.|#||...##||..|...##...|...|#.||..#.#
|#.....|..#..#..|.|#|...|..#.#|...#............###
||.|.|##.#|...|....#..|.|.|.#|...........|.....#|#
|..#..#..#......|....|.|......|##|.#....##.|##.|||
###.||.|.|.|..#..||....|...|..|....#..#|..|.||..|#
....#.#|||..|#|.......#|....#........####|....##.|
........|..|...#..|....#...|#.#..##|..|.#..#|.###.
.#.##.#...##|.|#.#.|.....#...#..#|.#|#|.|......#|.
.|.....###.||...#|.#.|||#|..#.|.|.#.#.##.##.|.|.|.
#.#|.||..|.#...##..||.##....#..........#...##.|...
.#....|..##..|.#.##|........#..#......#.....#|..##
.|#.#...|.|||....||...#|.|.#......#..###..|.#|.|.|
##..#.|#.|.....||..##.||#|.#|#|#....#..|...|......
..|......#.|.|.#..|........|.###||###....|.#.....|
|..|#|..|...#...##|#|#.#|#|......||###...|.#||....
.........|.##|...#.#...##....|.....#...|#..|..#..#
...#.#........#.|#..#..#|##|.....#.#.|#||...|#.|..
...##..#|..........|.....|....|#.|..#...#|...#|.#.
.|..#|..|.|.|||....|.#....|..||..#...|..#..|..##|.
....|.|...#...#..#.|.....#....|...#.|..........|..
...#|#.||.#..|#.|.###|#|.#.......#...##.##|.|....|
....##||.#...#..#...##|...||#.#..#|#......##||.|..
..#.....##.......|##.|..||#......|..|||.#.......#.
.....|#||#..|.#|..|..|....|........|.....##.#.#.|.
"""


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase("""
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
""", 10, 1147),
]


def pos(y, x, stride):
    return (y + 1) * stride + x + 1


OPEN = '.'
TREES = '|'
LUMBERYARD = '#'


def get_neighbours(world, y, x):
    return [
        world[yy][xx]
        for yy in range(max(y - 1, 0), min(y + 2, len(world)))
        for xx in range(max(x - 1, 0), min(x + 2, len(world)))
        if yy != y or xx != x
    ]


def solve(input, minutes):
    world = []
    for line in input.strip().split('\n'):
        world.append(line)

    history = {}

    while minutes:
        next_world = []
        for y, row in enumerate(world):
            next_row = []
            for x, c in enumerate(row):
                neighbours = get_neighbours(world, y, x)

                if c == OPEN:
                    # An open acre will become filled with trees if three or more adjacent acres contained trees.
                    # Otherwise, nothing happens.
                    next_row.append(TREES if neighbours.count(TREES) >= 3 else OPEN)
                elif c == TREES:
                    # An acre filled with trees will become a lumberyard if three or more adjacent acres were
                    # lumberyards.
                    # Otherwise, nothing happens.
                    next_row.append(LUMBERYARD if neighbours.count(LUMBERYARD) >= 3 else TREES)
                else:
                    # An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other
                    # lumberyard and at least one acre containing trees.
                    # Otherwise, it becomes open.
                    assert c == LUMBERYARD
                    next_row.append(LUMBERYARD if neighbours.count(LUMBERYARD) >= 1 and neighbours.count(TREES) >= 1 else OPEN)
            assert len(next_row) == len(row)
            next_world.append(next_row)
        assert len(next_world) == len(world)
        world = next_world
        minutes -= 1

        if minutes % 100 == 0:
            flat_world = [a for row in world for a in row]
            print(minutes, flat_world.count(TREES) * flat_world.count(LUMBERYARD))

        if minutes % 1000 == 0:
            print()
            for row in world:
                print(''.join(row))

    flat_world = [a for row in world for a in row]
    return flat_world.count(TREES) * flat_world.count(LUMBERYARD)


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case, case.minutes)
        check_case(case, result)

    print(solve(INPUT, 10))
