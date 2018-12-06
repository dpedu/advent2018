#!/usr/bin/env python3


from a import getdist, fullrange


def point_vaild(point, allpoints, units):
    """
    Returns True if the point is no more than units away from all points in allpoints (as in the sum of all dists)
    """

    for p in allpoints:
        units -= getdist(point, p)
        if units <= 0:
            return False
    return True


def main():
    coords = []
    maxdist = 10000

    with open("input.txt") as f:
        for line in f.readlines():
            a, b = line.split(", ")
            coords.append((int(a), int(b)))

    # bounding box is be +x+y, -x,-y corners
    # TBD this probably breaks with abusive input
    xcoords = [i[0] for i in coords]
    ycoords = [i[1] for i in coords]
    bufsize = 0
    bbox = (
        (
            max(xcoords) + bufsize,
            max(ycoords) + bufsize
        ),
        (
            min(xcoords) - bufsize,
            min(ycoords) - bufsize
        )
    )

    print("bbox:", bbox)

    valids = 0
    for y in fullrange(bbox[1][1], bbox[0][1]):
        for x in fullrange(bbox[1][0], bbox[0][0]):
            if point_vaild((x, y), coords, maxdist):
                valids += 1

    print(valids)


if __name__ == '__main__':
    main()
