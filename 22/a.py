#!/usr/bin/env python3


from enum import Enum


X = 0
Y = 1
GI = 0
EL = 1
TYPE = 2


class Tile(Enum):
    ROCKY = 0
    WET = 1
    NARROW = 2


def main():
    with open("input.txt") as f:
        depth = int(f.readline().split(" ")[1])
        target = tuple([int(i) for i in f.readline().split(" ")[1].split(",")])
    # print(depth)
    # print(target)

    # depth = 510
    # target = (10, 10)

    target2 = (target[X] + 1, target[Y] + 1)

    """
    Type is based on erosion level (EL)
    EL based on geologic index (GI)
    GI based on rules

    00 01 03 06 10 15
    02 04 07 11 16 21
    05 08 12 17 22 26
    09 13 18 23 27 30
    14 19 24 28 31 33
    20 25 29 32 34 35


    """
    world = {}  # mapping of (x,y) to (GI, EL)

    def calcGi(coord):
        nonlocal world
        if coord == (0, 0):
            return 0  # gi hard coded to 0
        elif coord == target:
            return 0  # gi hard coded to 0
        elif coord[Y] == 0:
            return coord[X] * 16807  # X coordinate times 16807.
        elif coord[X] == 0:
            return coord[Y] * 48271  # Y coordinate times 48271.
        else:
            # result of multiplying the erosion levels of the regions at X-1,Y and X,Y-1.
            return world[(coord[X] - 1, coord[Y])][EL] * world[(coord[X], coord[Y] - 1)][EL]

    # https://stackoverflow.com/a/20422854
    for k in range(0, target2[X] + target2[Y] - 1):
        for y in range(0, k + 1):
            x = k - y
            if x < target2[X] and y < target2[Y]:
                gi = calcGi((x, y))
                el = (gi + depth) % 20183
                world[(x,y)] = (gi, el, Tile(el % 3))
                # print((x,y))

    # print(world)

    total = 0

    for y in range(0, target[Y] + 1):
        for x in range(0, target[X] + 1):
            total += world[(x,y)][TYPE].value

    print(total)

    # populate world with risk values



if __name__ == '__main__':
    main()
