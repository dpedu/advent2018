#!/usr/bin/env python3


from sys import exit
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
        if self.damtype in target.immune:
            multiplier = 0
        elif self.damtype in target.weak:
            multiplier = 2
        else:
            multiplier = 1

        damage = multiplier * self.effpower

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
    battles = []  # list of tuples (attacker, defender)
    # armies in this list need to be assigned a target
    assign = sorted(armies,
                    key=lambda a: a.effpower * 100000000 + a.initiative,  # strongest armies pick a target first
                    reverse=True)

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

    return sorted(battles, key=lambda b: b[0].initiative, reverse=True)


def runsim(armies):
    while True:  # each loop is one round of fighting
        battles = assignbattles(armies)

        if not battles:  # one side has been wiped out
            break

        had_casualties = False
        for attacker, defender in battles:
            if attacker.units > 0:
                wiped, dmg, killed = attacker.attack(defender)
                had_casualties = had_casualties or killed > 0
                if wiped:
                    armies.remove(defender)

                    if len(battles) == 1:
                        break

        if not had_casualties:
            return

    if armies[0].team == "Immune System":
        print(sum([i.units for i in armies]))
        exit(0)


def main():
    boost = 80  # semi-arbitrary starting point to save time. Tweak if it doesn't fit your input
    while True:
        armies = parsearmies("input.txt")
        for unit in armies:
            if unit.team == "Immune System":
                unit.damage += boost
        print(boost)
        runsim(armies)
        boost += 1



if __name__ == '__main__':
    main()
