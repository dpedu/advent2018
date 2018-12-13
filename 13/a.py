#!/usr/bin/env python3


from enum import Enum


class Track(Enum):
    BLANK = 0
    CORNER1 = 1
    CORNER2 = 2
    STRAIGHT = 3
    INTERSECTION = 4
    CART = 5


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


VERTICAL = set([Direction.UP, Direction.DOWN])


def dir2offset(direction):
    return {Direction.UP: (0, -1),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0),
            Direction.RIGHT: (1, 0)}[direction]


def applydir(coords, direction):
    offset = dir2offset(direction)
    return (coords[0] + offset[0],
            coords[1] + offset[1])


def char2track(char):
    if char in set("^v<>"):
        return Track.CART
    elif char in set("|-"):
        return Track.STRAIGHT
    elif char == "/":
        return Track.CORNER1
    elif char == "\\":
        return Track.CORNER2
    elif char == "+":
        return Track.INTERSECTION
    elif char == " ":
        return Track.BLANK
    else:
        raise Exception("Invalid char:", repr(char))


def cart2dir(char):
    if char == "^":
        return Direction.UP
    elif char == ">":
        return Direction.RIGHT
    elif char == "v":
        return Direction.DOWN
    elif char == "<":
        return Direction.LEFT
    else:
        raise Exception("Invalid cart direction:", repr(char))


def dir2char(direction):
    return {Direction.UP: "^",
            Direction.RIGHT: ">",
            Direction.DOWN: "v",
            Direction.LEFT: "<"}[direction]


def track2char(track):
    return {Track.STRAIGHT: "+",
            Track.CORNER1: "/",
            Track.CORNER2: "\\",
            Track.INTERSECTION: "@",
            Track.BLANK: " "}[track]


class Cart(object):
    def __init__(self, coord, direction):
        self.coord = coord
        self.direction = direction
        self.turn = 0

    def __repr__(self):
        return "<Cart coord=({}) ({})>".format(self.coord, id(self))


def printboard(board, carts):
    dimX = 0
    dimY = 0
    for x, y in board.keys():
        dimX = max(dimX, x)
        dimY = max(dimY, y)

    cartskeyed = {cart.coord: cart for cart in carts}

    for y in range(0, dimY + 1):
        for x in range(0, dimX + 1):
            if (x, y) in cartskeyed:
                print(dir2char(cartskeyed[(x, y)].direction), end="")
            else:
                print(track2char(board[(x, y)]), end="")
            pass
        print()
    print()


def advancecart(cart, carts, board):
    # find the coordinate the cart will advance to
    newcoord = applydir(cart.coord, cart.direction)

    # check if the new square is already occupied
    for c in carts:
        if newcoord == c.coord:
            return True, c  # A collision happened!

    # advance the cart in the direction of travel
    cart.coord = newcoord

    # deal with implications of the new square it landed on
    newsquare = board[cart.coord]

    if newsquare == Track.STRAIGHT:
        pass  # Do nothing
    elif newsquare == Track.CORNER1:  # /
        # class Direction(Enum):
        #     UP = 0    -> 1
        #     RIGHT = 1 -> 2
        #     DOWN = 2  -> 3
        #     LEFT = 3  -> 0
        cart.direction = Direction((cart.direction.value + (1 if cart.direction in VERTICAL else -1)) % 4)
    elif newsquare == Track.CORNER2:  # \
        # class Direction(Enum):
        #     UP = 0    -> 3
        #     RIGHT = 1 -> 0
        #     DOWN = 2  -> 1
        #     LEFT = 3  -> 2
        cart.direction = Direction((cart.direction.value + (-1 if cart.direction in VERTICAL else 1)) % 4)
    elif newsquare == Track.CART:
        raise Exception("wtf")
    elif newsquare == Track.INTERSECTION:
        # class Direction(Enum):
        #     UP = 0
        #     RIGHT = 1
        #     DOWN = 2
        #     LEFT = 3
        # left, straight, right
        # turn = 0, subtract
        # turn = 1, do nothing
        # turn = 2, add
        diff = {0: -1, 1: 0, 2: 1}[cart.turn]
        cart.direction = Direction((cart.direction.value + diff) % 4)
        cart.turn = (cart.turn + 1) % 3
    elif newsquare == Track.BLANK:
        raise Exception("wtf")
    else:
        raise Exception("wtf!")

    return False, None  # No collision


def loadboard(fname):
    board = {}
    carts = []
    with open(fname) as f:
        y = 0
        for line in f.readlines():
            for x, char in enumerate(line.rstrip("\n")):
                c = char2track(char)
                if c == Track.CART:
                    carts.append(Cart((x, y), cart2dir(char)))
                    c = Track.STRAIGHT
                board[(x, y)] = c
            y += 1
    # printboard(board, carts)
    return board, carts


def main():
    board, carts = loadboard("input.txt")

    while True:
        # Put carts in processing order
        carts.sort(key=lambda cart: cart.coord)
        for cart in carts:
            collision, crashee = advancecart(cart, carts, board)
            if collision:
                print("Collision at", crashee.coord)
                return
        # printboard(board, carts)


if __name__ == '__main__':
    main()
