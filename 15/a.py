#!/usr/bin/env python3


from enum import Enum
from collections import deque


class Tile(Enum):
    WALL = 0
    OPEN = 1


def char2tile(char):
    return {"#": Tile.WALL,
            ".": Tile.OPEN}[char]


def tile2char(tile):
    return {Tile.WALL: "#",
            Tile.OPEN: "."}[tile]


class Unit(object):
    def __init__(self, coord, cls, powerlevel=3):
        self.pos = coord
        self.cls = cls  # G or E
        self.hp = 200
        self.power = powerlevel

    def __repr__(self):
        return "<{} @ {}, hp={}>".format(self.cls, self.pos, self.hp)


def printfield(field, units, width, height, markers=None):
    """
    Print out the map. Optionally, add markers using a list of (x,y) tuples
    :param field: dict of (x,y)->Tile
    :param units: list of Unit objects
    :param width: width of the map
    :param height: height of the map
    :param markers: list of (x,y) coordinates making up the path
    """
    unitskeyed = {unit.pos: unit for unit in units}

    for y in range(0, height):
        inrow = []
        for x in range(0, width):
            c = (x, y)
            if c in unitskeyed:
                u = unitskeyed[c]
                print(u.cls, end="")
                inrow.append("{}({})".format(u.cls, u.hp))
            elif markers and c in markers:
                print("o", end="")
            else:
                print(tile2char(field[c]), end="")
        if inrow:
            print("   ", ", ".join(inrow))
        else:
            print()
    print()


def findpath(field, start, end, unitscoords):
    """
    Given the field and start/end (x,y) tuples, return a list of (x,y) coordinate tuples representing a path back from
    end to the start. Units are counted as blocked squares
    :param field: dict of (x,y)->Tile
    :param start: (x,y) coordinate tuple
    :param end: (x,y) coordinate tuple
    :param unitscoords: list of (x,y) unit coordinate tuples
    """
    frontier = deque([start])
    came_from = {}
    came_from[start] = None
    while True:
        try:
            current = frontier.pop()
        except IndexError:  # Runs out of spaces to move
            return None

        if current == end:
            break
        for move in getneighbors(field, current):
            if move in unitscoords:
                continue
            if move not in came_from:
                frontier.appendleft(move)
                came_from[move] = current
    else:
        return None  # No path available

    # use the data in came_from to build a path
    path = []
    position = end
    while position != start:
        path.append(position)
        position = came_from[position]
    return path


TRNSLATIONS = (0, -1), (-1, 0), (1, 0), (0, 1),


def getneighbors(field, start):
    """
    Return a list of (x,y) tuples of squares that are valid moves from the start square
    """
    valid = []
    for t in TRNSLATIONS:
        new = cmbcoords(start, t)
        if field[new] == Tile.OPEN:
            valid.append(new)
    return valid


def cmbcoords(c1, c2):
    """
    Combine coordinates such that (1,2) + (3,4) = (4,6)
    """
    return (c1[0] + c2[0], c1[1] + c2[1])


def loadmap(fpath):
    field = {}
    units = []
    width = 0
    height = 0
    with open(fpath) as f:
        for y, line in enumerate(f.readlines()):
            height = y + 1
            for x, char in enumerate(line.strip()):
                width = max(width, x + 1)
                if char in set(["E", "G"]):
                    field[(x, y)] = Tile.OPEN
                    units.append(Unit((x, y), char))
                else:
                    field[(x, y)] = char2tile(char)
    return field, units, width, height


def main():
    field, units, width, height = loadmap("input.txt")
    printfield(field, units, width, height)

    rounds = 0
    while True:
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

            unitscoords = {u.pos: u for u in units}

            if current_unit.pos not in dests:
                # No targets in range, unit must move

                costs = []  # list of (dest, pathlength, firstmove)
                for dest in dests:
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
                    newpos = next_moves[0][2]
                    del unitscoords[current_unit.pos]
                    unitscoords[newpos] = current_unit
                    current_unit.pos = newpos

            if current_unit.pos in dests:
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
                        return

        printfield(field, units, width, height)
        rounds += 1


if __name__ == '__main__':
    main()
