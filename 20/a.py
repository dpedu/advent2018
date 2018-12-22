#!/usr/bin/env python3


from collections import defaultdict


def cmp2dir(char):
    # Return (X,Y) translations corresponding to compass directions
    return {"N": (0, -1),
            "E": (1, 0),
            "S": (0, 1),
            "W": (-1, 0)}[char]


def addpts(a, b):
    return (a[0] + b[0], a[1] + b[1])


def parseregex(regex):
    ptr = 0

    def parseblock():
        nonlocal ptr
        # recurses the () sections of a regex
        # we want to return the length of the longest sub path
        children = []
        curchild = []
        while True:
            if ptr == len(regex):
                children.append(curchild)
                return max(children)
            char = regex[ptr]
            ptr += 1
            if char == "(":
                curchild.append(parseblock())
            elif char == "|":
                children.append(curchild)
                curchild = []
            elif char == ")":
                children.append(curchild)
                curchild = []
                return children
            else:  # Some NESW direction
                curchild.append(char)

    return parseblock()


def parselinks(res):

    links = defaultdict(set)  # mapping of roomA -> (roomB, ...) AND roomB -> (roomA, ...)

    def parseres(sub, coords):
        nonlocal links
        for unit in sub:
            if isinstance(unit, str):
                # Step into another room
                # Add link from previous room to this room
                newroom = addpts(coords, cmp2dir(unit))
                links[newroom].update([coords])
                links[coords].update([newroom])
                coords = newroom
            else:
                parseres(unit, coords)

    parseres(res, (0, 0))
    return links


def main():
    with open("input.txt") as f:
        regex = f.read().strip()[1:-1]

    # Parse a regex like 'NE(S|WW)' into a structure like [N, E, [[S], [W, W]]]
    res = parseregex(regex)
    # Parse the above output into coordinate links
    # E.g. the initial N creates a link between 0,0 and 0,-1 and vice-versa
    links = parselinks(res)

    # Explore the links until all rooms have been visited
    frontier = [(0, 0)]
    room_distance = dict()
    dist = 0
    while frontier:
        new_frontier = []
        for room in frontier:
            if room in room_distance:  # already found room
                continue
            room_distance[room] = dist
            new_frontier.extend(links[room])
        frontier = new_frontier
        dist += 1

    print(max(room_distance.values()))
    print(len([i for i in filter(lambda x: x>=1000, room_distance.values())]))


if __name__ == '__main__':
    main()
