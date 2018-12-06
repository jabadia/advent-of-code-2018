from collections import namedtuple, Counter, defaultdict

TestCase = namedtuple('TestCase', 'case expected')

INPUT = """
66, 204
55, 226
231, 196
69, 211
69, 335
133, 146
321, 136
220, 229
148, 138
42, 319
304, 181
101, 329
72, 244
242, 117
83, 237
169, 225
311, 212
348, 330
233, 268
99, 301
142, 293
239, 288
200, 216
44, 215
353, 289
54, 73
73, 317
55, 216
305, 134
343, 233
227, 75
139, 285
264, 179
349, 263
48, 116
223, 60
247, 148
320, 232
60, 230
292, 78
247, 342
59, 326
333, 210
186, 291
218, 146
205, 246
124, 204
76, 121
333, 137
117, 68
"""


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase("""
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9
""", 17),
]


def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def solve(input):
    points = [tuple(map(int, line.split(','))) for line in input.strip().split('\n')]
    minx = min(x for x, y in points)
    miny = min(y for x, y in points)
    maxx = max(x for x, y in points)
    maxy = max(y for x, y in points)
    border_ids = [id for id, (x, y) in enumerate(points) if x == minx or x == maxx or y == miny or y == maxy]

    nearest = {}
    dist_to_nearest = defaultdict(lambda: 1000000)
    for id, p in enumerate(points):
        print(id, id / len(points))
        for x in range(minx, maxx + 1):
            for y in range(miny, maxy + 1):
                d1 = dist((x, y), p)
                d2 = dist_to_nearest[(x, y)]
                if d1 < d2:
                    nearest[(x, y)] = id
                    dist_to_nearest[(x, y)] = d1
                elif d1 == d2:
                    nearest[(x, y)] = -1

    most_common, count = Counter(filter(
        lambda v: v not in border_ids,
        nearest.values())
    ).most_common(1)[0]
    return count


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case)
        check_case(case, result)

    print(solve(INPUT))
