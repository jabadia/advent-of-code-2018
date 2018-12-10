from collections import namedtuple, deque

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
    TestCase(428, 70825, 398502),  # part 1
]


def solve(players, marbles):
    circle = deque([0])
    current_player = 1
    current_marble = 1
    scores = [0] * players
    while current_marble <= marbles:
        if current_marble % 23 == 0:
            circle.rotate(-7)
            scores[current_player] += current_marble + circle.pop()
        else:
            circle.rotate(2)
            circle.append(current_marble)
        current_marble += 1
        current_player = (current_player + 1) % players

    return max(scores)


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.players, case.marbles)
        check_case(case, result)

    players, marbles = INPUT
    print(solve(players, marbles * 100))
