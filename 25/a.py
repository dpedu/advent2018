#!/usr/bin/env python3


from pprint import pprint


class Point(object):
    def __init__(self, x, y, z, t):
        self.x = x
        self.y = y
        self.z = z
        self.t = t

    def __sub__(self, other):
        return sum([abs(getattr(self, prop) - getattr(other, prop)) for prop in ["x", "y", "z", "t"]])

    def __repr__(self):
        return "<Point {},{},{},{}>".format(self.x, self.y, self.z, self.t)


def main():
    points = []
    with open("input.txt") as f:
        for line in f.readlines():
            if line:
                points.append(Point(*[int(i) for i in line.split(",")]))

    consts = []

    # assign near points
    while points:
        assigned_one = False

        for seeker in points[:]:
            assigned = False
            for const in consts:
                for point in const:
                    if point - seeker <= 3:
                        const.append(seeker)
                        points.remove(seeker)
                        assigned = True
                        assigned_one = True
                        break
                if assigned:
                    break

        if not assigned_one:
            # if we don't assign a point after looping through them all, create a new constellation
            consts.append([points.pop()])

        print("Constellations:", len(consts), "Points:", len(points))

    pprint(consts)

    print("Constellations:", len(consts), "Points:", len(points))


if __name__ == '__main__':
    main()
