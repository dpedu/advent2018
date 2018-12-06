#!/usr/bin/env python3


def getdist(pa, pb):
    return abs(pa[0] - pb[0]) + abs(pa[1] - pb[1])


def fullrange(s, e):
    return range(s, e + 1)


def get_closest(point, allpoints):
    """
    Returns the index of the point from allpoints closest to the passed point.
    Returns None if two points are equidistant.
    """
    best_index = None
    best_distance = 999999999
    is_dupe = False

    for index, p in enumerate(allpoints):
        # if p == point:
        #     continue
        dist = getdist(point, p)
        if dist <= best_distance:
            if dist == best_distance:
                is_dupe = True
            else:
                is_dupe = False
            best_distance = dist
            best_index = index

    if is_dupe:
        return None

    return best_index


def main():
    coords = []

    with open("input.txt") as f:
        for line in f.readlines():
            a, b = line.split(", ")
            coords.append((int(a), int(b)))

    # bounding box is be +x+y, -x,-y corners
    xcoords = [i[0] for i in coords]
    ycoords = [i[1] for i in coords]
    bufsize = 1
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

    # point ids (their index in the coords list) mapped to their size count
    fields = {x: 0 for x in range(0, len(coords))}
    infinte_fields = set()
    for y in fullrange(bbox[1][1], bbox[0][1]):
        for x in fullrange(bbox[1][0], bbox[0][0]):
            closest = get_closest((x, y), coords)
            if closest is not None:
                fields[closest] += 1

                # if touching an edge of the bounding box
                if x == bbox[1][0] or x == bbox[0][0] or y == bbox[1][1] or y == bbox[0][1]:
                    infinte_fields.update([closest])

    biggest_fieldid = None
    biggest_field_size = 0

    for pointid, size in fields.items():
        if pointid not in infinte_fields:
            if size > biggest_field_size:
                biggest_field_size = size
                biggest_fieldid = pointid

    print("biggest field id:", biggest_fieldid)
    print("biggest field size:", biggest_field_size)


if __name__ == '__main__':
    main()
