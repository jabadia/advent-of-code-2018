from collections import namedtuple

TestCase = namedtuple('TestCase', 'case expected')

INPUT = '260321'


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase('01245', 5),
    TestCase('51589', 9),
    TestCase('92510', 18),
    TestCase('59414', 2018),
]


def solve(input):
    scoreboard = '37'
    elf1, elf2 = 0, 1
    while input not in scoreboard[-10:]:
        scoreboard += str(int(scoreboard[elf1]) + int(scoreboard[elf2]))
        elf1 = (elf1 + int(scoreboard[elf1]) + 1) % len(scoreboard)
        elf2 = (elf2 + int(scoreboard[elf2]) + 1) % len(scoreboard)
    return len(scoreboard) - 10 + scoreboard[-10:].index(input)


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        check_case(case, result)

    print(solve(INPUT))
