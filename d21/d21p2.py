from collections import namedtuple

import re

TestCase = namedtuple('TestCase', 'case expected')

INPUT = """
#ip 1
seti 123 0 4
bani 4 456 4
eqri 4 72 4
addr 4 1 1
seti 0 0 1
seti 0 0 4
bori 4 65536 5
seti 10704114 0 4
bani 5 255 2
addr 4 2 4
bani 4 16777215 4
muli 4 65899 4
bani 4 16777215 4
gtir 256 5 2
addr 2 1 1
addi 1 1 1
seti 27 2 1
seti 0 4 2
addi 2 1 3
muli 3 256 3
gtrr 3 5 3
addr 3 1 1
addi 1 1 1
seti 25 5 1
addi 2 1 2
seti 17 5 1
setr 2 6 5
seti 7 8 1
eqrr 4 0 2
addr 2 1 1
seti 5 3 1
"""


class Cpu:
    registers = [0] * 6

    def execute(self, opcode, A, B, C):
        getattr(self, opcode)(A, B, C)

    def addr(self, A, B, C):
        self.registers[C] = self.registers[A] + self.registers[B]

    def addi(self, A, B, C):
        self.registers[C] = self.registers[A] + B

    def mulr(self, A, B, C):
        self.registers[C] = self.registers[A] * self.registers[B]

    def muli(self, A, B, C):
        self.registers[C] = self.registers[A] * B

    def banr(self, A, B, C):
        self.registers[C] = self.registers[A] & self.registers[B]

    def bani(self, A, B, C):
        self.registers[C] = self.registers[A] & B

    def borr(self, A, B, C):
        self.registers[C] = self.registers[A] | self.registers[B]

    def bori(self, A, B, C):
        self.registers[C] = self.registers[A] | B

    def setr(self, A, B, C):
        self.registers[C] = self.registers[A]

    def seti(self, A, B, C):
        self.registers[C] = A

    def gtir(self, A, B, C):
        self.registers[C] = 1 if A > self.registers[B] else 0

    def gtri(self, A, B, C):
        self.registers[C] = 1 if self.registers[A] > B else 0

    def gtrr(self, A, B, C):
        self.registers[C] = 1 if self.registers[A] > self.registers[B] else 0

    def eqir(self, A, B, C):
        self.registers[C] = 1 if A == self.registers[B] else 0

    def eqri(self, A, B, C):
        self.registers[C] = 1 if self.registers[A] == B else 0

    def eqrr(self, A, B, C):
        self.registers[C] = 1 if self.registers[A] == self.registers[B] else 0


class CpuDebugger:
    registers = list('abcdef')

    def __init__(self, ip):
        self.registers[ip] = 'ip'

    def execute(self, opcode, A, B, C):
        return getattr(self, opcode)(A, B, C)

    def addr(self, A, B, C):
        return "%s = %s %s %s" % (self.registers[C], self.registers[A], '+', self.registers[B])

    def addi(self, A, B, C):
        return "%s = %s %s %s" % (self.registers[C], self.registers[A], '+', B)

    def mulr(self, A, B, C):
        return "%s = %s %s %s" % (self.registers[C], self.registers[A], '*', self.registers[B])

    def muli(self, A, B, C):
        return "%s = %s %s %s" % (self.registers[C], self.registers[A], '*', B)

    def banr(self, A, B, C):
        return "%s = %s %s %s" % (self.registers[C], self.registers[A], '&', self.registers[B])

    def bani(self, A, B, C):
        return "%s = %s %s %s" % (self.registers[C], self.registers[A], '&', B)

    def borr(self, A, B, C):
        return "%s = %s %s %s" % (self.registers[C], self.registers[A], '|', self.registers[B])

    def bori(self, A, B, C):
        return "%s = %s %s %s" % (self.registers[C], self.registers[A], '|', B)

    def setr(self, A, B, C):
        return "%s = %s" % (self.registers[C], self.registers[A])

    def seti(self, A, B, C):
        return "%s = %s" % (self.registers[C], A)

    def gtir(self, A, B, C):
        return "%s = %s %s %s" % (self.registers[C], A, '>', self.registers[B])

    def gtri(self, A, B, C):
        return "%s = %s %s %s" % (self.registers[C], self.registers[A], '>', B)

    def gtrr(self, A, B, C):
        return "%s = %s %s %s" % (self.registers[C], self.registers[A], '>', self.registers[B])

    def eqir(self, A, B, C):
        return "%s = %s %s %s" % (self.registers[C], A, '==', self.registers[B])

    def eqri(self, A, B, C):
        return "%s = %s %s %s" % (self.registers[C], self.registers[A], '==', B)

    def eqrr(self, A, B, C):
        return "%s = %s %s %s" % (self.registers[C], self.registers[A], '==', self.registers[B])


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase('x', -1),
]

RE_PARSE = re.compile('(\w+) (\d+) (\d+) (\d+)')
RE_NUMBER = re.compile('(\d+)')


def solve(input):
    program = []
    ip = None
    for line in input.strip().split('\n'):
        if '#' in line:
            ip = int(RE_NUMBER.findall(line)[0])
        else:
            opcode, A, B, C = RE_PARSE.match(line).groups()
            program.append((opcode, int(A), int(B), int(C)))

    cpu_debugger = CpuDebugger(ip=ip)
    # for i, (opcode, A, B, C) in enumerate(program):
    #     print('%3d   ' % (i,), end='')
    #     cpu.execute(opcode, A, B, C)

    cpu = Cpu()
    count = 0
    seen = set()
    prev = None
    while True:
        opcode, A, B, C = program[cpu.registers[ip]]
        # print(count, cpu.registers[ip], cpu_debugger.execute(opcode, A, B, C), cpu.registers)
        cpu.execute(opcode, A, B, C)
        cpu.registers[ip] = cpu.registers[ip] + 1
        if cpu.registers[ip] == 28:
            e = cpu.registers[4]
            print(e)
            if e in seen:
                return prev
            seen.add(e)
            prev = e

        count += 1


if __name__ == '__main__':
    # for case in TEST_CASES:
    #     result = solve(case.case)
    #     check_case(case, result)

    print(solve(INPUT))
