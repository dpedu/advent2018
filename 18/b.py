#!/usr/bin/env python3


from collections import defaultdict
from a import Tile, loadmap, iterneighbors, counttypes


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


def main():
    field, width, height = loadmap("input.txt")

    # Generations to run:                                             1000000000
    # I (manually) noticed it cycles after every X generations:       28
    # 1000000000 % 28 =                                               20

    generation = 0

    # Run the first 500 generations
    while generation <= 500:
        field = tick(field, width, height)
        generation += 1

    # Run until our generation minus 20 is a multiple of 28
    while (generation - 20) % 28 != 0:
        field = tick(field, width, height)
        generation += 1

    counts = counttypes(field)
    total = counts[Tile.TREE] * counts[Tile.YARD]
    print("Generation", generation, "Total", total)


if __name__ == '__main__':
    main()
