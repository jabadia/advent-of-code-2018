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
    state = {}
    rules = set()
    for line in input.strip().split('\n'):
        if line.strip() == '':
            continue
        elif 'initial state' in line:
            initial_state = line.replace('initial state: ', '')
            for i, s in enumerate(initial_state):
                state[i] = s
        else:
            assert '=>' in line
            pattern, result = line.split(' => ')
            if result == '#':
                rules.add(pattern)

    generation = 0
    visited_states = [state]
    while generation < 20 or state != visited_states[generation-20]:
        print(generation, min(state.keys()), max(state.keys()),
              ''.join('#' if k in state else '.' for k in range(min(state.keys()), max(state.keys())+1))
              )
        next_state = {}
        for i in range(min(state.keys())-2, max(state.keys())+3):
            pattern = state.get(i-2, '.') + state.get(i-1, '.') + state.get(i, '.') + state.get(i+1, '.') + state.get(i+2, '.')
            if pattern in rules:
                next_state[i] = '#'
        state = {k-min(next_state.keys()): '#' for k in next_state}
        generation += 1
        visited_states.append(state)

    end_state = state

    result = 0
    for i in range(min(end_state.keys()), max(end_state.keys()) + 1):
        if end_state.get(i, '.') == '#':
            result += i + 50000000000 - 17

    return result

# 750000000697

if __name__ == '__main__':
    # for case in TEST_CASES:
    #     result = solve(case.case)
    #     check_case(case, result)

    print(solve(INPUT))
