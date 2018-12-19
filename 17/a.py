#!/usr/bin/env python3


import re
from enum import Enum


RE_LINE = re.compile(r'(y|x)=([0-9]+), (x|y)=([0-9]+)\.\.([0-9]+)')


class Tile(Enum):
    WALL = 0
    FALL = 1
    SPREAD = 2
    STILL = 3


class Dir(Enum):  # Direction
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


def addpts(a, b):
    return (a[0] + b[0], a[1] + b[1])


def loadworld(fname):
    world = {}
    minX = 9999999999999
    minY = 9999999999999
    maxX = 0
    maxY = 0
    with open(fname) as f:
        for line in f.readlines():
            axis, coord, axis2, range1, range2 = RE_LINE.search(line).groups()
            coord = int(coord)
            range2 = int(range2)
            range1 = int(range1)
            if axis == "x":
                for y in range(range1, range2 + 1):
                    world[(coord, y)] = Tile.WALL
                maxX = max(maxX, coord)
                minX = min(minX, coord)
                maxY = max(maxY, range2)
                minY = min(minY, range1)
            else:
                for x in range(range1, range2 + 1):
                    world[(x, coord)] = Tile.WALL
                maxX = max(maxX, range2)
                minX = min(minX, range1)
                maxY = max(maxY, coord)
                minY = min(minY, coord)
    return world, minX, maxX, minY, maxY


def printworld(world, minX, maxX, minY, maxY, fall, still):
    padding = 5
    for y in range(minY - padding, maxY + 1 + padding):
        for x in range(minX - padding, maxX + 1 + padding):
            coord = (x, y)
            if coord in fall:
                print("|", end="")
            elif coord in still:
                print("~", end="")
            elif coord in world:
                print("#", end="")
            else:
                print(".", end="")
        print()


def main():
    world, minX, maxX, minY, maxY = loadworld("input.txt")
    minY = 0
    # world[(500, 0)] = Tile.WALL

    # Tiles in the falling state
    fall = set([(500, 0)])
    # Tiles that have landed somewhere and can flow left/right
    still = set()

    printworld(world, minX, maxX, minY, maxY, fall, still)

    while True:
        # input()

        """
        Particle Rules
        - Any type above AIR spawns a "fall" below it
        - Any type above WALL turns into STILL
        - Any type next to an open space and above a wall spawns one next door
        """
        updated = False

        for coord in list(fall):
            below = addpts(coord, Dir.DOWN.value)
            if below[1] > maxY:
                continue
            if below in fall:
                continue
            elif below not in world:
                world[below] = Tile.FALL
                fall.update([below])
                updated = True
                # print("u1")
            elif world[below] in (Tile.WALL, Tile.STILL):
                # fall.remove(coord)
                # spread.update([coord])

                # Search left and right, spreading the water (in fall state) as we go
                # If we find contiguous floor until we hit a wall on both sides, the water is changed to still
                # Otherwise, it stays flowing
                capped = True
                added = set([coord])

                # search left
                sleft = addpts(coord, Dir.LEFT.value)
                while True:
                    if sleft in world and world[sleft] == Tile.WALL:
                        break  # left wall found
                    added.update([sleft])
                    support = addpts(sleft, Dir.DOWN.value)
                    if support not in world or world[support] not in (Tile.WALL, Tile.STILL):
                        capped = False
                        break
                    sleft = addpts(sleft, Dir.LEFT.value)

                # search right
                sright = addpts(coord, Dir.RIGHT.value)
                while True:
                    if sright in world and world[sright] == Tile.WALL:
                        break  # left wall found
                    added.update([sright])
                    support = addpts(sright, Dir.DOWN.value)
                    if support not in world or world[support] not in (Tile.WALL, Tile.STILL):
                        capped = False
                        break
                    sright = addpts(sright, Dir.RIGHT.value)

                # If the region is sealed off (e.g. no water can flow out, fill it wit still water)
                if capped:
                    for c in added:
                        if c not in world:
                            updated = True
                        world[c] = Tile.STILL
                        try:
                            fall.remove(c)
                        except KeyError:
                            pass
                    still.update(added)
                else:
                    for c in added:
                        if c not in world:
                            updated = True
                        world[c] = Tile.FALL
                    fall.update(added)

        maxwater = 0
        for w in fall:
            maxwater = max(maxwater, w[1])
        print("MaxY:", maxY, "MaxWater:", maxwater, "Fallers:", len(fall))

        if not updated:
            printworld(world, minX, maxX, minY, maxY, fall, still)
            print("Fall   =", len(fall))  # This seems to include off-map fallers (from the spring), but i don't care.
            print("Still  =", len(still))
            fall -= still
            still -= fall
            total = len(still)
            for point in fall:
                if point[1] >= minY and point[1] <= maxY:
                    total += 1
            print(total)
            return


if __name__ == '__main__':
    main()

