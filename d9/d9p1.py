from collections import namedtuple, defaultdict

TestCase = namedtuple('TestCase', 'players marbles expected')

INPUT = (428, 70825)


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %d %d" % (test_case.players, test_case.marbles,))
    else:
        print("FAIL %d %d, expected %s, got %s" % (test_case.players, test_case.marbles, test_case.expected, actual))


TEST_CASES = [
    TestCase(9, 25, 32),
    TestCase(10, 1618, 8317),
    TestCase(13, 7999, 146373),
    TestCase(17, 1104, 2764),
    TestCase(21, 6111, 54718),
    TestCase(30, 5807, 37305),
]


def solve(players, marbles):
    circle = [0]
    current_pos = 0
    current_player = 1
    current_marble = 1
    scores = defaultdict(int)
    while current_marble <= marbles:
        # print("[%d] %d - %s" % (current_player, current_pos, circle))
        if current_marble % 23 == 0:
            current_pos = (current_pos - 7) % len(circle)
            scores[current_player] += current_marble + circle[current_pos]
            circle = circle[:current_pos] + circle[current_pos + 1:]
        else:
            current_pos = (current_pos + 2) % len(circle)
            circle = circle[:current_pos] + [current_marble] + circle[current_pos:]
        current_marble += 1
        current_player = (current_player + 1) % players

    return max(scores.values())


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.players, case.marbles)
        check_case(case, result)

    players, marbles = INPUT
    print(solve(players, marbles))
