from collections import namedtuple

import re

TestCase = namedtuple('TestCase', 'case expected')

INPUT = """
Immune System:
3916 units each with 3260 hit points with an attack that does 8 radiation damage at initiative 16
4737 units each with 2664 hit points (immune to radiation, cold, bludgeoning) with an attack that does 5 slashing damage at initiative 13
272 units each with 10137 hit points with an attack that does 331 slashing damage at initiative 10
92 units each with 2085 hit points (immune to fire) with an attack that does 223 bludgeoning damage at initiative 1
126 units each with 11001 hit points (immune to bludgeoning; weak to cold, fire) with an attack that does 717 bludgeoning damage at initiative 8
378 units each with 4669 hit points (immune to cold, slashing) with an attack that does 117 fire damage at initiative 17
4408 units each with 11172 hit points (immune to slashing; weak to bludgeoning) with an attack that does 21 bludgeoning damage at initiative 5
905 units each with 11617 hit points (weak to fire) with an attack that does 100 fire damage at initiative 20
3574 units each with 12385 hit points (weak to bludgeoning; immune to radiation) with an attack that does 27 radiation damage at initiative 19
8186 units each with 3139 hit points (immune to bludgeoning, fire) with an attack that does 3 bludgeoning damage at initiative 9

Infection:
273 units each with 26361 hit points (weak to slashing; immune to radiation) with an attack that does 172 radiation damage at initiative 18
536 units each with 44206 hit points (weak to fire, cold) with an attack that does 130 bludgeoning damage at initiative 12
1005 units each with 12555 hit points (immune to fire, radiation, bludgeoning) with an attack that does 24 radiation damage at initiative 6
2381 units each with 29521 hit points (immune to bludgeoning, radiation) with an attack that does 23 slashing damage at initiative 4
5162 units each with 54111 hit points (weak to radiation) with an attack that does 19 fire damage at initiative 2
469 units each with 45035 hit points (weak to fire, slashing) with an attack that does 163 radiation damage at initiative 15
281 units each with 23265 hit points (weak to slashing; immune to bludgeoning) with an attack that does 135 radiation damage at initiative 11
4350 units each with 46138 hit points (weak to fire) with an attack that does 18 bludgeoning damage at initiative 14
3139 units each with 48062 hit points (immune to bludgeoning, slashing, fire; weak to cold) with an attack that does 28 bludgeoning damage at initiative 3
9326 units each with 41181 hit points (weak to fire, bludgeoning) with an attack that does 8 cold damage at initiative 7
"""


def check_case(test_case, actual):
    if test_case.expected == actual:
        print("OK %s" % (test_case.case,))
    else:
        print("FAIL %s, expected %s, got %s" % (test_case.case, test_case.expected, actual))

IMMUNE_ARMY = 'inmune'
INFECTION_ARMY = 'infection'



TEST_CASES = [
    TestCase("""
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
""", (INFECTION_ARMY, 5216)),
]


class Group:
    RE_GROUP = re.compile(
        '(\d+) units each with (\d+) hit points( \((.+)\))? with an attack that does (\d+) (\w+) damage at initiative (\d+)')

    def __init__(self, line, army, index, boost):
        groups = self.RE_GROUP.match(line).groups()
        self.index = index
        self.army = army
        self.units = int(groups[0])
        self.hit_points = int(groups[1])
        self.weak_to = []
        self.immune_to = []
        if groups[3]:
            for part in groups[3].split('; '):
                if part.startswith('weak to'):
                    self.weak_to = part[8:].split(', ')
                elif part.startswith('immune to'):
                    self.immune_to = part[10:].split(', ')
                else:
                    assert False, 'bad part ' + part
        self.attack_points = int(groups[4]) + (boost if army == IMMUNE_ARMY else 0)
        self.attack_type = groups[5]
        self.initiative = int(groups[6])

    def attack(self, defender):
        inflicted_damage = damage(self, defender)
        units_to_kill = inflicted_damage // defender.hit_points
        # print("%s attacks to %s killing %d units" % (self, defender, min(defender.units, units_to_kill)))
        defender.units = max(0, defender.units - units_to_kill)

    @property
    def effective_power(self):
        return self.units * self.attack_points

    def long_repr(self):
        return "[%s %d] %d units each with %d hit points (%s) with an attack that does %d %s damage at initiative %d" % (
            self.army,
            self.index,
            self.units,
            self.hit_points,
            '; '.join(filter(None, [
                ('immune to ' + ', '.join(self.immune_to)) if self.immune_to else None,
                ('weak to ' + ', '.join(self.weak_to)) if self.weak_to else None,
            ])),
            self.attack_points,
            self.attack_type,
            self.initiative,
        )

    def __repr__(self) -> str:
        return "[%s %d] %d units ep: %d" % (self.army, self.index, self.units, self.units * self.attack_points)


def damage(attacker, defender):
    inflicted_damage = attacker.effective_power
    if attacker.attack_type in defender.immune_to:
        inflicted_damage = 0
    elif attacker.attack_type in defender.weak_to:
        inflicted_damage *= 2
    return inflicted_damage


def solve(input, boost):
    army = None
    groups = []
    for line in input.strip().split('\n'):
        if line == 'Immune System:':
            army = IMMUNE_ARMY
        elif line == 'Infection:':
            army = INFECTION_ARMY
        elif line == '' or not line:
            continue
        else:
            group = Group(line, army, 1 + len([g for g in groups if g.army == army]), boost)
            groups.append(group)

    # print('\n'.join([g.long_repr() for g in groups]))

    while True:
        # target selection
        groups = sorted(groups, key=lambda group: (group.effective_power, group.initiative), reverse=True)
        # print(groups)
        selected_targets = {}
        for i, group in enumerate(groups):
            enemy_army = IMMUNE_ARMY if group.army == INFECTION_ARMY else INFECTION_ARMY
            inflicted_damage, _, _, target = max(
                ((damage(group, enemy), enemy.effective_power, enemy.initiative, enemy)
                 for enemy in groups if enemy.army == enemy_army and enemy not in selected_targets.values()),
                default=(None, None, None, None)
            )
            if inflicted_damage:
                selected_targets[group] = target

        # attack
        for attacker in sorted(groups, key=lambda group: group.initiative, reverse=True):
            defender = selected_targets.get(attacker, None)
            if defender:
                attacker.attack(defender)

        # end of round
        groups = [g for g in groups if g.units > 0]

        alive_infection = len([g for g in groups if g.army == INFECTION_ARMY])
        print(alive_infection, len(groups), sum(g.units for g in groups if g.army == INFECTION_ARMY),
              sum(g.units for g in groups if g.army == IMMUNE_ARMY))
        if alive_infection == 0 or alive_infection == len(groups):
            return IMMUNE_ARMY if alive_infection == 0 else INFECTION_ARMY, sum(g.units for g in groups)


if __name__ == '__main__':
    for case in TEST_CASES:
        result = solve(case.case, 0)
        check_case(case, result)

    # for lower boost levels between 120 and 130 it hangs forever... why? Will investigate
    for boost in range(131, 100000):
        winner, units = solve(INPUT, boost)
        print(boost, winner, units)
        if winner == IMMUNE_ARMY:
            print('winner:', units)
            break
