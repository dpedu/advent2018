#!/usr/bin/env python3


from a import iterclaims, buildworld


def main():
    world = buildworld()
    for idx, x, y, w, h in iterclaims():
        it = True
        for xp in range(x, x + w):
            for yp in range(y, y + h):
                if world[xp][yp] != 1:
                    it = False
                    break
            else:
                continue
            break
        if it:
            print(idx, x, y, w, h)
            break


if __name__ == '__main__':
    main()
