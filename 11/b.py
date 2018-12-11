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


def getregionbestsizevalue(x, y, sizemax):
    """
    Calculate each square size in passes as illustrated below
    1 2 3 4
    2 2 3 4
    3 3 3 4
    4 4 4 4
    """
    # size with the highest total
    bestsize = None
    # score of the best size
    bestsizevalue = -999999
    # maximum square we can fit
    size = min(sizemax + 1 - x, sizemax + 1 - y)
    # running total for this coordinate
    total = 0
    for sz in range(0, size):
        # the column/row we're currently iterating
        xcol = x + sz
        yrow = y + sz
        # iteration counters
        yit = yrow - 1
        xit = xcol
        while yit >= y:
            total += getcelvalue(xcol, yit)
            yit -= 1
        while xit >= x:
            total += getcelvalue(xit, yrow)
            xit -= 1

        if total > bestsizevalue:
            bestsizevalue = total
            bestsize = sz

    return (x, y, bestsize + 1, bestsizevalue)


from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import cpu_count


def main():
    bestcoords = None
    bestvalue = 0
    compl = 0
    todo = 300 * 300

    with ProcessPoolExecutor(max_workers=cpu_count()) as pool:
        futures = []
        for x in range(1, 300):
            for y in range(1, 300):
                futures.append(pool.submit(getregionbestsizevalue, x, y, 300, ))

        for f in as_completed(futures):
            rx, ry, size, value = f.result()
            if value > bestvalue:
                bestvalue = value
                bestcoords = (rx, ry, size)
                print("new best:", bestcoords, "@", bestvalue)
            compl += 1
            if compl % 100 == 0:
                print(compl, "({}%)".format(int(compl / todo * 100)))

    print("Value:", bestvalue)
    print("Solution:", ",".join([str(i) for i in bestcoords]))


if __name__ == '__main__':
    main()
