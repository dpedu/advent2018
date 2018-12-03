#!/usr/bin/env python3


WIDTH = 1000
HEIGHT = 1000


def finddims():
    # find how big the canvas is from our input
    maxX = 0
    maxY = 0
    for x, y, w, h in iterclaims():
        xsize = x + w
        if xsize > maxX:
            maxX = xsize
        ysize = y + h
        if ysize > maxY:
            maxY = ysize
    print(maxX, maxY)  # 999, 999


def iterclaims():
    with open("input.txt") as f:
        for line in f.readlines():
            idx, _, coords, size = line.split()
            coords = coords.rstrip(":")
            x, y = coords.split(",")
            w, h = size.split("x")
            idx = idx.lstrip("#")
            yield (int(idx), int(x), int(y), int(w), int(h))


def buildarena(xs=WIDTH, ys=HEIGHT):
    arena = []
    for row in range(0, xs):
        arena.append([0 for _ in range(0, ys)])
    return arena


def muxclaims(claims, arena):
    for _, x, y, w, h in claims:
        for xp in range(x, x + w):
            for yp in range(y, y + h):
                arena[xp][yp] += 1


def buildworld():
    arena = buildarena()
    claims = iterclaims()
    muxclaims(claims, arena)
    return arena


def main():
    world = buildworld()
    overclaims = 0
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            if world[x][y] > 1:
                overclaims += 1

    print(overclaims)


if __name__ == '__main__':
    # finddims()
    main()
