#!/usr/bin/env python3


from collections import defaultdict


def main():
    twofers = 0
    threefers = 0
    with open("boxes.txt") as f:
        for line in f.readlines():
            letters = defaultdict(int)
            for letter in line.strip():
                letters[letter] += 1
            is_twofer = False
            is_threefer = False
            for k, v in letters.items():
                if v == 2:
                    is_twofer = True
                if v == 3:
                    is_threefer = True
            if is_twofer:
                twofers += 1
            if is_threefer:
                threefers += 1

    print(twofers * threefers)


if __name__ == '__main__':
    main()
