#!/usr/bin/env python3


import re
import pdb


RE_LINE = re.compile(r'pos=<(-?[0-9]+),(-?[0-9]+),(-?[0-9]+)>, r=([0-9]+)')


class Bot(object):
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def __repr__(self):
        return "<Bot ({},{},{}) r={}>".format(self.x, self.y, self.z, self.r)


def getdist(bot1, x, y, z):
    return abs(bot1.x - x) + abs(bot1.y - y) + abs(bot1.z - z)


def main():
    bots = []
    with open("input.txt") as f:
        for line in f.readlines():
            bot = Bot(*[int(i) for i in RE_LINE.search(line).groups()])
            bots.append(bot)


    xs = [bot.x for bot in bots]
    ys = [bot.y for bot in bots]
    zs = [bot.z for bot in bots]

    dist = 1
    while dist < max(xs) - min(xs):
        dist *= 2

    while True:
        target_count = 0
        best = None
        best_val = None
        for x in range(min(xs), max(xs) + 1, dist):
            for y in range(min(ys), max(ys) + 1, dist):
                for z in range(min(zs), max(zs) + 1, dist):

                    count = 0

                    for bot in bots:
                        calc = getdist(bot, x, y, z)
                        if (calc - bot.r) / dist <= 0:
                            count += 1
                    if count > target_count:
                        target_count = count
                        best_val = abs(x) + abs(y) + abs(z)
                        best = (x, y, z)
                    elif count == target_count:
                        if not best_val or abs(x) + abs(y) + abs(z) < best_val:
                            best_val = abs(x) + abs(y) + abs(z)
                            best = (x, y, z)

        if dist == 1:
            print(best_val)
            return
        else:
            xs = [best[0] - dist, best[0] + dist]
            ys = [best[1] - dist, best[1] + dist]
            zs = [best[2] - dist, best[2] + dist]
            dist //= 2




if __name__ == '__main__':
    main()
