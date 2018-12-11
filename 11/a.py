#!/usr/bin/env python3


SERIAL = 6878


def getcelvalue(x, y):
    """
    Find the fuel cell's rack ID, which is its X coordinate plus 10.
    Begin with a power level of the rack ID times the Y coordinate.
    Increase the power level by the value of the grid serial number (your puzzle input).
    Set the power level to itself multiplied by the rack ID.
    Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers with no hundreds digit become 0).
    Subtract 5 from the power level.
    """
    rackid = x + 10
    pwr = rackid * y
    pwr += SERIAL
    pwr *= rackid
    pwr = int(pwr / 100) % 10
    return pwr - 5


def getregionvalue(x, y, size):
    total = 0
    for xi in range(x, x + size):
        for yi in range(y, y + size):
            total += getcelvalue(xi, yi)
    return total


def main():
    bestcoords = None
    bestvalue = 0
    for x in range(1, 299):
        for y in range(1, 299):
            value = getregionvalue(x, y)
            if value > bestvalue:
                bestcoords = (x, y, )
                bestvalue = value

    print(bestcoords, bestvalue)


if __name__ == '__main__':
    main()
