#!/usr/bin/env python3


import sys
from collections import defaultdict


class Point(object):
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def tick(self):
        self.x += self.vx
        self.y += self.vy

    def __repr__(self):
        return "<Point ({},{}) v=({}, {})>".format(self.x, self.y, self.vx, self.vy)


def drawpoints(points):
    # sort points into rows
    minY = sys.maxsize
    maxY = -minY - 1

    for p in points:
        if p.y < minY:
            minY = p.y
        if p.y > maxY:
            maxY = p.y

    rangeY = (minY - maxY + 1)

    if abs(rangeY) != 8:
        return False

    minX = min([i.x for i in points])
    maxX = max([i.x for i in points])

    rows = defaultdict(list)
    for point in points:
        rows[point.y].append(point)

    rows_sorted = sorted(rows.items(), key=lambda x: x[1][0].y)

    for rowY, rowpoints in rows_sorted:
        rowX = sorted(rowpoints, key=lambda x: x.x)
        for i in range(minX, maxX + 1):
            if rowX and rowX[0].x == i:
                print("#", end="")
                while rowX and rowX[0].x == i:
                    rowX.pop(0)
            else:
                print(".", end="")
        print()

    return True


def main():
    points = []
    with open("input.txt") as f:
        for line in f.readlines():
            line = line[10:]
            posX, rest = line.split(",", 1)
            posX = int(posX)
            posY, rest = rest.split(">", 1)
            posY = int(posY)
            rest = rest[11:]
            vX, rest = rest.split(",", 1)
            vX = int(vX)
            vY, rest = rest.split(">", 1)
            vY = int(vY)
            points.append(Point(posX, posY, vX, vY))

    generations = 0
    while True:
        generations += 1

        for point in points:
            point.tick()

        if drawpoints(points):
            print(generations)
            break


if __name__ == '__main__':
    main()
