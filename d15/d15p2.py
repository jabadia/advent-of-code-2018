from collections import namedtuple, deque
import heapq

TestCase = namedtuple('TestCase', 'case expected')

INPUT = """
################################
########################.....###
########################.....###
########################.....###
######################.##.G..###
###################...G..G....##
###################...G......###
#################......#.....###
##################.#..#....G..##
#################..G..........##
###############...G..G.....E...#
###########...G........#.......#
###########..G#####..........###
###########..#######..G....E.###
######..###.#########.#.....####
######.####.#########.###...####
###...G####.#########.###..#####
###..#....#.#########G###...####
######....G.#########.......####
#######......#######...........#
#.#####G......#####...........##
#.######....E...............#.##
#.####.........................#
#.##G#...#...E..E..............#
#..............................#
#..#G.....G........E.......E..##
#..##.##...#...G..........###.##
#.#####...##..............###.E#
######...#.....#....#.#.#####..#
#####....G.####.E..E#..#########
#######.#######....###.#########
################################
"""


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase("""
#######   
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#   
#######
""", 4988),
    TestCase("""
#######   
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#   
#######   
""", 31284),
    TestCase("""
#######   
#E.G#.#
#.#G..#
#G.#.G#   
#G..#.#
#...E.#
#######
""", 3478),
    TestCase("""
#######   
#.E...#   
#.#..G#
#.###.#   
#E#G#G#   
#...#G#
#######   
""", 6474),
    TestCase("""
#########   
#G......#
#.E.#...#
#..##..G#
#...##..#   
#...#...#
#.G...G.#   
#.....G.#   
#########   
""", 1140),
]

ELF = 'E'
GOBLIN = 'G'


class Unit:
    def __init__(self, kind, pos, attack, hit_points):
        self.kind = kind
        self.pos = pos
        self.attack = attack
        self.hit_points = hit_points

    def __repr__(self) -> str:
        return "%s %s %d %d" % (self.kind, self.pos, self.attack, self.hit_points)


def advance(pos, delta):
    return pos[0] + delta[0], pos[1] + delta[1]


NEIGHBOURS = [(-1, 0), (0, -1), (0, 1), (1, 0)]


def find_open_neighbours(pos, walls, units):
    open_neighbours = set(
        neighbour
        for neighbour in [advance(pos, delta) for delta in NEIGHBOURS]
        if neighbour not in walls and neighbour not in units
    )
    return open_neighbours


def find_nearest_target(pos, target_ranges, walls, units):
    distance = {}
    prev_pos = {}
    queue = deque([pos])
    visited = set()
    distance[pos] = 0
    closest = None
    while queue:
        cell = queue.popleft()
        visited.add(cell)
        if cell in target_ranges:
            closest = cell
            break
        if cell in walls:
            continue
        for cell2 in [advance(cell, delta) for delta in NEIGHBOURS]:
            if cell2 not in visited and cell2 not in walls and cell2 not in units:
                visited.add(cell2)
                queue.append(cell2)
                distance[cell2] = distance[cell] + 1
                prev_pos[cell2] = cell

    if not closest or closest == pos:
        return None, None

    next_step = closest
    while prev_pos[next_step] != pos:
        next_step = prev_pos[next_step]

    return closest, next_step


def print_board(rounds, walls, units):
    maxy = max(y for y, x in walls)
    maxx = max(x for y, x in walls)
    print('--- %s ---' % (rounds,))
    for y in range(0, maxy + 1):
        for x in range(0, maxx + 1):
            pos = (y, x)
            if pos in walls:
                print('#', end='')
            elif pos in units:
                print(units[pos].kind, end='')
            else:
                print('.', end='')
        print()


def solve1(input, attack_points):
    walls = set()
    units = {}
    for y, line in enumerate(input.strip().split('\n')):
        for x, c in enumerate(line):
            pos = (y, x)
            if c == '#':
                walls.add(pos)
            elif c in 'EG':
                units[pos] = Unit(c, pos, attack_points if c == ELF else 3, 200)

    rounds = 0
    while True:
        # round begins
        # print_board(rounds, walls, units)
        # remaining_elfs = len([u for u in units.values() if u.kind == ELF])
        # print(rounds, remaining_elfs)
        round_units = sorted(units)
        for pos in round_units:
            # turn begins
            unit = units.get(pos, None)
            if not unit:
                continue

            # identify targets
            target_kind = GOBLIN if unit.kind == ELF else ELF
            targets = [target for target in units.values() if target.kind == target_kind]

            if not targets:
                return unit.kind, rounds * sum(unit.hit_points for unit in units.values())

            # open squares
            open_squares = set()
            for target in targets:
                squares_in_range = [advance(target.pos, delta) for delta in
                                    NEIGHBOURS]  # find_open_neighbours(target.pos, walls, units)
                open_squares.update(squares_in_range)

            nearest_target, next_pos = find_nearest_target(unit.pos, open_squares, walls, units)

            # move
            if next_pos:
                # print("%s %s -> %s" % (units[pos], pos, next_pos))
                del units[pos]
                units[next_pos] = unit
                unit.pos = next_pos
            else:
                # print("%s %s doesn't move" % (units[pos], pos))
                pass

            # attack
            _, _, most_vulnerable_target = min(
                ((units[pos].hit_points, pos, units[pos])
                 for pos in [advance(unit.pos, delta) for delta in NEIGHBOURS]
                 if pos in units and units[pos].kind == target_kind),
                default=(0, (0, 0), None)
            )
            if most_vulnerable_target:
                # print("%s attacks %s" % (unit, most_vulnerable_target))
                most_vulnerable_target.hit_points -= unit.attack
                if most_vulnerable_target.hit_points <= 0:
                    if units[most_vulnerable_target.pos].kind == ELF:
                        return GOBLIN, 0
                    del units[most_vulnerable_target.pos]

        rounds += 1


def solve(INPUT):
    attack_points = 4
    while True:
        winner, outcome = solve1(INPUT, attack_points)
        if winner == ELF:
            return outcome
        attack_points += 1


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        check_case(case, result)

    print(solve(INPUT))
