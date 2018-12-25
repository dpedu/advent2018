#!/usr/bin/env python3


"""
The immune system and the infection each have an army made up of several groups;
Each group consists of one or more identical units.
The armies repeatedly fight until only one army has units remaining.

Units within a group all have the same hit points, attack damage, attack type, initiative, and sometimes weaknesses or immunities.
    (higher initiative units attack first and win ties)

Each group also has an effective power: the number of units in that group multiplied by their attack damage.

Each fight consists of two phases: target selection and attacking.

Target selection:
    In decreasing order of effective power,
        in a tie, the group with the higher initiative chooses first.
    The attacking group chooses to target the group in the enemy army to which it would deal the most damage
        (after accounting for weaknesses and immunities,
            but not accounting for whether the defending group has enough units to actually receive all of that damage).
    If an attacking group is considering two defending groups to which it would deal equal damage,
        it chooses to target the defending group with the largest effective power;
        if there is still a tie, it chooses the defending group with the highest initiative.
    If it cannot deal any defending groups damage, it does not choose a target.
    Defending groups can only be chosen as a target by one attacking group.

Attacking phase:
    each group deals damage to the target it selected, if any. Groups attack in decreasing order of initiative,
        regardless of whether they are part of the infection or the immune system.
    By default, an attacking group would deal damage equal to its effective power to the defending group.
        Immune means no damage
        Weak means 2x damage
    The defending group only loses whole units from damage;
        damage is always dealt in such a way that it kills the most units possible,
        Any remaining damage to a unit that does not immediately kill it is ignored

    After the fight is over, if both armies still contain units, a new fight begins;
        combat only ends once one army has lost all of its units.
"""


from pprint import pprint
import pdb
import re


RE_ARMY = re.compile(r'([0-9]+) units each with ([0-9]+) hit points (\(([^\)]+)\) )?with an attack that does ([0-9]+) ([a-z]+) damage at initiative ([0-9]+)')
RE_MODIFIER = re.compile(r'(weak|immune) to ([a-z, ]+)')


class Army(object):
    def __init__(self, tag, team, units, hp, weaknesses, immunes, damage, damage_type, initiative):
        # Group number for debugging purposes
        self.tag = tag
        # Team string name
        self.team = team
        # Number of units
        self.units = units
        # Health per unit
        self.hp = hp
        # set() of weaknesses (string names)
        self.weak = weaknesses
        # set() of immunities (string names)
        self.immune = immunes
        # attack power
        self.damage = damage
        # attack type (string name)
        self.damtype = damage_type
        # initiative level
        self.initiative = initiative

    @property
    def effpower(self):
        return self.units * self.damage

    def __repr__(self):
        mods = []
        modstr = ""
        if self.immune:
            mods.append("immunte:{}".format('|'.join(self.immune)))
        if self.weak:
            mods.append("weak:{}".format('|'.join(self.weak)))
        if mods:
            modstr = " {}".format(' '.join(mods))
        return "<Army tag:{} team:'{}' eff:{} units:{} hp:{} damage:{} damtype:{} init:{}{}>" \
            .format(self.tag, self.team, self.effpower, self.units, self.hp, self.damage, self.damtype, self.initiative, modstr)

    def attack(self, target, simulate=False):
        """
        Perform a battle
        :param target: army that self will attack
        :param simulate: if true, don't modify the target army.
        :return: maximum damage dealt if simulating
                 if not simulating, True if the target army was wiped out. False otherwise
        """

        """
        Attacking phase:
        each group deals damage to the target it selected, if any. Groups attack in decreasing order of initiative,
            regardless of whether they are part of the infection or the immune system.
        By default, an attacking group would deal damage equal to its effective power to the defending group.
            Immune means no damage
            Weak means 2x damage
        The defending group only loses whole units from damage;
            damage is always dealt in such a way that it kills the most units possible,
            Any remaining damage to a unit that does not immediately kill it is ignored

        After the fight is over, if both armies still contain units, a new fight begins;
            combat only ends once one army has lost all of its units.
        """

        # Determine weakness/immunity damage multiplier
        if self.damtype in target.immune:
            multiplier = 0
        elif self.damtype in target.weak:
            multiplier = 2
        else:
            multiplier = 1

        damage = multiplier * self.effpower

        # if multiplier == 0:
        #     return False, 0, 0

        dead = damage // target.hp
        killed = min(target.units, dead)

        if simulate:
            return damage

        target.units -= killed

        return target.units == 0, damage, killed


def parsearmies(fname):
    armies = []
    with open(fname) as f:
        teamname = None
        groupnum = 1
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            if ":" in line:  # Found a new army like "Infection:"
                teamname = line[0:-1]
                groupnum = 1
            else:  # an army line to parse
                units, hp, _, modifiers, atkpwr, atktype, initia = RE_ARMY.search(line).groups()
                mods = {"weak": set(),
                        "immune": set()}
                if modifiers:
                    for prop in RE_MODIFIER.findall(modifiers):
                        mods[prop[0]].update(prop[1].split(', '))
                armies.append(Army(groupnum, teamname, int(units), int(hp), mods["weak"], mods["immune"],
                                   int(atkpwr), atktype, int(initia)))
                groupnum +=1
    return armies


def assignbattles(armies):
    """
    Target selection:
    In decreasing order of effective power,
        in a tie, the group with the higher initiative chooses first.
    The attacking group chooses to target the group in the enemy army to which it would deal the most damage
        (after accounting for weaknesses and immunities,
            but not accounting for whether the defending group has enough units to actually receive all of that damage).
    If an attacking group is considering two defending groups to which it would deal equal damage,
        it chooses to target the defending group with the largest effective power;
        if there is still a tie, it chooses the defending group with the highest initiative.
    If it cannot deal any defending groups damage, it does not choose a target.
    Defending groups can only be chosen as a target by one attacking group.
    """

    battles = []  # list of tuples (attacker, defender)
    # armies in this list need to be assigned a target
    assign = sorted(armies,
                    key=lambda a: a.effpower * 100000000 + a.initiative,  # strongest armies pick a target first
                    reverse=True)

    # print("Assign order")
    # for ass in assign:
    #     print("- {} group {} (eff {})".format(ass.team, ass.tag, ass.effpower))
    # print()

    targets = set(assign)  # these armies can still be attacked
    while assign:
        army = assign.pop(0)  # we're finding a target for this army
        best = None    # best target
        best_dmg = -1  # damage inflicted to best target
        best_eff = -1
        best_init = -1
        considered = False
        for target in targets:
            if army.team == target.team or army == target:  # don't attack same team
                continue
            considered = True
            dmg = army.attack(target, simulate=True)
            # print("{} {} -> {} {}   damage: {} (target eff={}, init={})".format(army.team, army.tag, target.team, target.tag, dmg, target.effpower, target.initiative))
            if  (dmg > best_dmg) or \
                (dmg == best_dmg and target.effpower > best_eff) or \
                (dmg == best_dmg and target.effpower == best_eff and target.initiative > best_init):
                    best = target
                    best_dmg = dmg
                    best_init = target.initiative
                    best_eff = target.effpower

        if not considered:  # no targets available
            continue

        if best_dmg == 0:
            continue

        targets.remove(best)
        battles.append((army, best))
        # print("\nBest target for ({} group {} (effpwr {}) :: dmg={})\n\t{} is \n\t{}\n\n".format(army.team, army.tag, army.effpower, best_dmg, army, best))

    return sorted(battles, key=lambda b: b[0].initiative, reverse=True)


def main():
    armies = parsearmies("input.txt")

    while True:  # each loop is one round of fighting
        # print("\n========== Round ==========")
        battles = assignbattles(armies)

        if not battles:  # one side has been wiped out
            break

        # print()

        for attacker, defender in battles:
            if attacker.units > 0:
                wiped, dmg, killed = attacker.attack(defender)
                # print("{} group {} (i{}) attacks {} group {}, dealing {}, killing {}".format(attacker.team, attacker.tag, attacker.initiative, defender.team, defender.tag, dmg, killed))
                if wiped:
                    # print("{} group {} is wiped out! ({})".format(defender.team, defender.tag, defender.units))
                    armies.remove(defender)

                    if len(battles) == 1:
                        break

        # pdb.set_trace()
        # input()

    # print()
    # print()
    # pprint(armies)
    print(sum([i.units for i in armies]))


if __name__ == '__main__':
    main()
