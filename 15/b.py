#!/usr/bin/env python3


from a import Tile, loadmap, getneighbors, findpath


def char2tile(char):
    return {"#": Tile.WALL,
            ".": Tile.OPEN}[char]


def tile2char(tile):
    return {Tile.WALL: "#",
            Tile.OPEN: "."}[tile]


def main():
    minpower = 24  # found with some guesswork, change to suit your needs
    while True:
        print("Trying", minpower)
        result = rungame(minpower)
        if result:
            return
        minpower += 1


def rungame(powerlevel):
    field, units, width, height = loadmap("input.txt")
    for u in units:
        if u.cls == "E":
            u.power = powerlevel

    rounds = 0
    while True:
        # print("BEGIN ROUND", rounds)
        # input()

        # Put units into the order they'll be updated
        units.sort(key=lambda u: u.pos[0] + u.pos[1] * 1000)
        units_toupdate = units[:]

        # Process units in order
        while units_toupdate:
            current_unit = units_toupdate.pop(0)

            # Find desirable destinations - squares that border an enemy
            enemies = [u for u in units if u.cls != current_unit.cls]
            dests = set()
            for enemy in enemies:
                dests.update(getneighbors(field, enemy.pos))
            occupied = {u.pos for u in units if u != current_unit}  # Omit occupied dests
            dests -= occupied

            if current_unit.pos not in dests:
                # No targets in range, unit must move

                costs = []  # list of (dest, pathlength, firstmove)
                for dest in dests:
                    unitscoords = {u.pos: u for u in units}
                    path = findpath(field, current_unit.pos, dest, unitscoords)
                    if not path:
                        continue
                    costs.append((dest, len(path), path[-1]))

                if costs:  # A path to a dest exists

                    costs.sort(key=lambda i: i[1])
                    closest_cost = costs[0][1]

                    next_moves = []

                    for cost in costs:
                        if cost[1] == closest_cost:
                            next_moves.append(cost)

                    next_moves.sort(key=lambda i: i[0][0] + i[0][1] * 1000)
                    current_unit.pos = next_moves[0][2]

            if current_unit.pos in dests:
                unitscoords = {u.pos: u for u in units}
                targets = []  # Units we can hit from where we are
                for pos in getneighbors(field, current_unit.pos):
                    if pos in unitscoords and unitscoords[pos].cls != current_unit.cls:
                        targets.append(unitscoords[pos])

                targets.sort(key=lambda t: t.hp)  # We want to hit the lowest hp'd units
                lowhp = targets[0].hp

                candidates = []
                for target in targets:
                    if target.hp == lowhp:
                        candidates.append(target)
                    else:
                        break
                targets = candidates

                # reading order for targets
                targets.sort(key=lambda i: i.pos[0] + i.pos[1] * 1000)
                target = targets[0]

                target.hp -= current_unit.power

                if target.hp <= 0:
                    if target.cls == "E":
                        return False

                    units.remove(target)
                    if target in units_toupdate:
                        units_toupdate.remove(target)

                    if len(enemies) == 1:
                        print("End of combat")
                        print()
                        hpsum = sum([u.hp for u in units])
                        print("Rounds:", rounds)
                        print("HP sum:", hpsum)
                        print("Answer:", hpsum * rounds)
                        return True

        rounds += 1


if __name__ == '__main__':
    main()
