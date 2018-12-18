#!/usr/bin/env python3


from enum import Enum
from collections import defaultdict


class Tile(Enum):
    EMPTY = 0
    YARD = 1
    TREE = 2


def char2tile(char):
    return {".": Tile.EMPTY,
            "#": Tile.YARD,
            "|": Tile.TREE}[char]


def tile2char(tile):
    return {Tile.EMPTY: ".",
            Tile.YARD: "#",
            Tile.TREE: "|"}[tile]


def loadmap(fname):
    field = {}
    width = 0
    height = 0
    with open(fname) as f:
        for y, line in enumerate(f.readlines()):
            height = y
            for x, char in enumerate(line.strip()):
                field[(x, y)] = char2tile(char)
                width = y
    return field, width + 1, height + 1


def printmap(field, width, height):
    for y in range(0, height):
        for x in range(0, width):
            print(tile2char(field[(x, y)]), end="")
        print()


def iterneighbors(field, cx, cy):
    for y in range(cy - 1, cy + 2):
        for x in range(cx - 1, cx + 2):
            if x != cx or y != cy:
                try:
                    yield field[(x, y)]
                except KeyError:
                    pass


def tick(field, width, height):
    """
    Empty => Trees     >=3 adj with trees
    Trees => Yard      >=3 adj with yards
    Yard  => Yard      >0 adj with yard AND >0 adj with trees
    Yard  => Empty     If above rule fails
    """
    newfield = {}
    for y in range(0, height):
        for x in range(0, width):
            counts = defaultdict(int)
            for tile in iterneighbors(field, x, y):
                counts[tile] += 1
            tile = field[(x, y)]
            if tile == Tile.EMPTY:
                if counts[Tile.TREE] >= 3:
                    tile = Tile.TREE
            elif tile == Tile.TREE:
                if counts[Tile.YARD] >= 3:
                    tile = Tile.YARD
            elif tile == Tile.YARD:
                if counts[Tile.YARD] == 0 or counts[Tile.TREE] == 0:
                    tile = Tile.EMPTY
            newfield[(x, y)] = tile
    return newfield


def counttypes(field):
    counts = defaultdict(int)
    for _, v in field.items():
        counts[v] += 1
    return counts


def main():
    field, width, height = loadmap("input.txt")
    printmap(field, width, height)

    generation = 0
    while True:
        # input()
        generation += 1
        field = tick(field, width, height)
        print("Generation", generation)
        printmap(field, width, height)
        print()
        if generation >= 10:
            break

    counts = counttypes(field)
    print(counts[Tile.TREE] * counts[Tile.YARD])


if __name__ == '__main__':
    main()
