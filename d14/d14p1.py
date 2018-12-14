from collections import namedtuple

TestCase = namedtuple('TestCase', 'case expected')

INPUT = 260321


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase(5, '0124515891'),
    TestCase(9, '5158916779'),
    TestCase(18, '9251071085'),
    TestCase(2018, '5941429882'),
]


def solve(input):
    scoreboard = '37'
    elf1, elf2 = 0, 1
    while len(scoreboard) < input + 10:
        scoreboard += str(int(scoreboard[elf1]) + int(scoreboard[elf2]))
        # print(scoreboard)
        elf1 = (elf1 + int(scoreboard[elf1]) + 1) % len(scoreboard)
        elf2 = (elf2 + int(scoreboard[elf2]) + 1) % len(scoreboard)
        assert elf1 != elf2
    return scoreboard[input:input + 10]


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        check_case(case, result)

    print(solve(INPUT))
