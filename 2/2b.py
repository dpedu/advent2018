#!/usr/bin/env python3


from itertools import combinations


def main():
    with open("boxes.txt") as f:
        boxids = [l.strip() for l in f.readlines()]

    for a, b in combinations(boxids, 2):
        diffs = 0
        for i, c in enumerate(a):
            if b[i] != c:
                diffs += 1
        if diffs == 1:
            common = []
            for i, c in enumerate(a):
                if b[i] == c:
                    common.append(c)
            print(''.join(common))
            return


if __name__ == '__main__':
    main()
