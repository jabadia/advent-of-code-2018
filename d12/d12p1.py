from collections import namedtuple, defaultdict

TestCase = namedtuple('TestCase', 'case expected')

INPUT = """
initial state: #....##.#.#.####..#.######..##.#.########..#...##...##...##.#.#...######.###....#...##..#.#....##.##

.#.## => #
.#.#. => #
#.#.# => .
.#### => .
.#... => .
#..## => .
..#.# => #
#.#.. => .
##### => .
....# => .
...## => .
..##. => .
##.#. => #
##..# => .
##... => #
..### => #
.##.. => #
###.. => .
#..#. => .
##.## => .
..#.. => #
.##.# => #
####. => #
#.### => .
#...# => #
###.# => #
...#. => #
.###. => .
.#..# => #
..... => .
#.... => .
#.##. => #
"""


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase("""
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
""", 325),
]


def solve(input):
    state = set()
    rules = set()
    for line in input.strip().split('\n'):
        if line.strip() == '':
            continue
        elif 'initial state' in line:
            initial_state = line.replace('initial state: ', '')
            state = {i for i, s in enumerate(initial_state) if s == '#'}
        else:
            assert '=>' in line
            pattern, result = line.split(' => ')
            if result == '#':
                rules.add(pattern)

    generations = 20
    while generations:
        if generations % 10000 == 0:
            print(generations)
        next_state = set()
        for i in range(min(state) - 2, max(state) + 3):
            pattern = ''.join('#' if j in state else '.' for j in range(i-2, i+3))
            if pattern in rules:
                next_state.add(i)
        state = next_state
        generations -= 1

    return sum(state)


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        check_case(case, result)

    print(solve(INPUT))
