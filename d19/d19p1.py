from collections import namedtuple

import re

TestCase = namedtuple('TestCase', 'case expected')

INPUT = """
#ip 4
addi 4 16 4
seti 1 1 1
seti 1 7 3
mulr 1 3 2
eqrr 2 5 2
addr 2 4 4
addi 4 1 4
addr 1 0 0
addi 3 1 3
gtrr 3 5 2
addr 4 2 4
seti 2 3 4
addi 1 1 1
gtrr 1 5 2
addr 2 4 4
seti 1 6 4
mulr 4 4 4
addi 5 2 5
mulr 5 5 5
mulr 4 5 5
muli 5 11 5
addi 2 1 2
mulr 2 4 2
addi 2 6 2
addr 5 2 5
addr 4 0 4
seti 0 0 4
setr 4 5 2
mulr 2 4 2
addr 4 2 2
mulr 4 2 2
muli 2 14 2
mulr 2 4 2
addr 5 2 5
seti 0 5 0
seti 0 2 4
"""


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))


TEST_CASES = [
    TestCase("""
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
""", 7),
]


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
        getattr(self, opcode)(A, B, C)

    def addr(self, A, B, C):
        print("%s = %s %s %s" % (self.registers[C], self.registers[A], '+', self.registers[B]))

    def addi(self, A, B, C):
        print("%s = %s %s %s" % (self.registers[C], self.registers[A], '+', B))

    def mulr(self, A, B, C):
        print("%s = %s %s %s" % (self.registers[C], self.registers[A], '*', self.registers[B]))

    def muli(self, A, B, C):
        print("%s = %s %s %s" % (self.registers[C], self.registers[A], '*', B))

    def banr(self, A, B, C):
        print("%s = %s %s %s" % (self.registers[C], self.registers[A], '&', self.registers[B]))

    def bani(self, A, B, C):
        print("%s = %s %s %s" % (self.registers[C], self.registers[A], '&', B))

    def borr(self, A, B, C):
        print("%s = %s %s %s" % (self.registers[C], self.registers[A], '|', self.registers[B]))

    def bori(self, A, B, C):
        print("%s = %s %s %s" % (self.registers[C], self.registers[A], '|', B))

    def setr(self, A, B, C):
        print("%s = %s" % (self.registers[C], self.registers[A]))

    def seti(self, A, B, C):
        print("%s = %s" % (self.registers[C], A))

    def gtir(self, A, B, C):
        print("%s = %s %s %s" % (self.registers[C], A, '>', self.registers[B]))

    def gtri(self, A, B, C):
        print("%s = %s %s %s" % (self.registers[C], self.registers[A], '>', B))

    def gtrr(self, A, B, C):
        print("%s = %s %s %s" % (self.registers[C], self.registers[A], '>', self.registers[B]))

    def eqir(self, A, B, C):
        print("%s = %s %s %s" % (self.registers[C], A, '==', self.registers[B]))

    def eqri(self, A, B, C):
        print("%s = %s %s %s" % (self.registers[C], self.registers[A], '==', B))

    def eqrr(self, A, B, C):
        print("%s = %s %s %s" % (self.registers[C], self.registers[A], '==', self.registers[B]))


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

    cpu = CpuDebugger(ip=ip)
    for i, (opcode, A, B, C) in enumerate(program):
        print('%3d   ' % (i,), end='')
        cpu.execute(opcode, A, B, C)

    cpu = Cpu()
    while cpu.registers[ip] < len(program):
        opcode, A, B, C = program[cpu.registers[ip]]
        cpu.execute(opcode, A, B, C)
        cpu.registers[ip] = cpu.registers[ip] + 1
        print(dict(zip(['a', 'b', 'c', 'd', 'ip', 'f'], cpu.registers)))
        pass
        # print(cpu.registers)

    return cpu.registers[0]


if __name__ == '__main__':
    # for case in TEST_CASES:
    #     result = solve(case.case)
    #     check_case(case, result)

    print(solve(INPUT))
