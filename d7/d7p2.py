import heapq
from collections import namedtuple, defaultdict
import re

TestCase = namedtuple('TestCase', 'case expected')

INPUT = """
Step J must be finished before step E can begin.
Step X must be finished before step G can begin.
Step D must be finished before step A can begin.
Step K must be finished before step M can begin.
Step P must be finished before step Z can begin.
Step F must be finished before step O can begin.
Step B must be finished before step I can begin.
Step U must be finished before step W can begin.
Step A must be finished before step R can begin.
Step E must be finished before step R can begin.
Step H must be finished before step C can begin.
Step O must be finished before step S can begin.
Step Q must be finished before step Y can begin.
Step V must be finished before step W can begin.
Step T must be finished before step N can begin.
Step S must be finished before step I can begin.
Step Y must be finished before step W can begin.
Step Z must be finished before step C can begin.
Step M must be finished before step L can begin.
Step L must be finished before step W can begin.
Step N must be finished before step I can begin.
Step I must be finished before step G can begin.
Step C must be finished before step G can begin.
Step G must be finished before step R can begin.
Step R must be finished before step W can begin.
Step Z must be finished before step R can begin.
Step Z must be finished before step N can begin.
Step G must be finished before step W can begin.
Step L must be finished before step G can begin.
Step Y must be finished before step R can begin.
Step P must be finished before step I can begin.
Step C must be finished before step W can begin.
Step T must be finished before step G can begin.
Step T must be finished before step R can begin.
Step V must be finished before step Z can begin.
Step L must be finished before step C can begin.
Step K must be finished before step I can begin.
Step J must be finished before step I can begin.
Step Q must be finished before step C can begin.
Step F must be finished before step A can begin.
Step H must be finished before step Y can begin.
Step M must be finished before step N can begin.
Step P must be finished before step H can begin.
Step M must be finished before step C can begin.
Step V must be finished before step Y can begin.
Step O must be finished before step V can begin.
Step O must be finished before step Q can begin.
Step A must be finished before step G can begin.
Step T must be finished before step Z can begin.
Step K must be finished before step R can begin.
Step H must be finished before step O can begin.
Step O must be finished before step Y can begin.
Step O must be finished before step C can begin.
Step K must be finished before step P can begin.
Step P must be finished before step F can begin.
Step E must be finished before step M can begin.
Step M must be finished before step I can begin.
Step T must be finished before step W can begin.
Step P must be finished before step L can begin.
Step A must be finished before step O can begin.
Step X must be finished before step V can begin.
Step S must be finished before step G can begin.
Step A must be finished before step Y can begin.
Step J must be finished before step R can begin.
Step K must be finished before step F can begin.
Step J must be finished before step A can begin.
Step P must be finished before step C can begin.
Step E must be finished before step N can begin.
Step F must be finished before step Y can begin.
Step J must be finished before step D can begin.
Step H must be finished before step Z can begin.
Step U must be finished before step H can begin.
Step J must be finished before step T can begin.
Step V must be finished before step G can begin.
Step Z must be finished before step I can begin.
Step H must be finished before step W can begin.
Step B must be finished before step R can begin.
Step F must be finished before step B can begin.
Step X must be finished before step C can begin.
Step L must be finished before step R can begin.
Step F must be finished before step U can begin.
Step D must be finished before step N can begin.
Step P must be finished before step O can begin.
Step B must be finished before step O can begin.
Step F must be finished before step C can begin.
Step H must be finished before step L can begin.
Step O must be finished before step N can begin.
Step J must be finished before step Y can begin.
Step H must be finished before step N can begin.
Step O must be finished before step L can begin.
Step I must be finished before step W can begin.
Step J must be finished before step H can begin.
Step D must be finished before step Z can begin.
Step F must be finished before step W can begin.
Step X must be finished before step W can begin.
Step Y must be finished before step M can begin.
Step T must be finished before step M can begin.
Step U must be finished before step G can begin.
Step L must be finished before step I can begin.
Step N must be finished before step W can begin.
Step E must be finished before step C can begin.
"""


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase("""
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
""", 15),
]

RE_PARSE = re.compile('Step (\w) must be finished before step (\w) can begin\.')


def solve(input, delay, worker_count):
    graph, dependencies = defaultdict(set), defaultdict(set)
    for line in input.strip().split('\n'):
        source, target = RE_PARSE.match(line).groups()
        graph[source].add(target)
        dependencies[target].add(source)

    def duration(task):
        return ord(task) - ord('A') + 1 + delay

    workers = []
    tasks = []
    time = 0
    for task in sorted(set(graph) - set(dependencies)):  # nodes without dependencies
        heapq.heappush(tasks, task)

    while workers or tasks:
        # print(time, workers, tasks)
        while len(workers) < worker_count and tasks:
            task = heapq.heappop(tasks)
            heapq.heappush(workers, (duration(task) + time, task))
        if workers:
            finish_time, task = heapq.heappop(workers)
            time = finish_time
            for target in graph[task]:
                dependencies[target].remove(task)
                if len(dependencies[target]) == 0:
                    heapq.heappush(tasks, target)

    return time


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case, 0, 2)
        check_case(case, result)

    print(solve(INPUT, 60, 5))
