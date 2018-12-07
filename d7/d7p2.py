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
    sources = set()
    targets = set()
    prerequisites = defaultdict(set)
    for line in input.strip().split('\n'):
        source, target = RE_PARSE.match(line).groups()
        sources.add(source)
        targets.add(target)
        prerequisites[target].add(source)

    def duration(task):
        return ord(task) - ord('A') + 1 + delay

    queue = [(task, duration(task)) for task in sorted(sources - targets)]
    available_workers = worker_count
    workers = []
    path = []
    time = 0
    while queue or workers:
        for worker_task, worker_finish_time in workers:
            if worker_finish_time == time:  # task completed
                path.append(worker_task)
                available_workers += 1
                for target in prerequisites:
                    if worker_task in prerequisites[target]:
                            prerequisites[target].remove(worker_task )
                            if len(prerequisites[target]) == 0:
                                queue.append((target, duration(target)))
        workers = [worker for worker in workers if worker[1] != time]
        while available_workers and queue:
            task, task_duration = queue.pop(0)
            available_workers -= 1
            workers.append((task, task_duration + time))
        queue.sort()
        print(time, workers, path)
        time += 1

    return time-1


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case, 0, 2)
        check_case(case, result)

    print(solve(INPUT, 60, 5))
