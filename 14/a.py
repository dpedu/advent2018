#!/usr/bin/env python3


def main():
    elves = [0, 1]
    scores = [3, 7]
    after = 503761  # puzzle input

    while True:
        comb = str(sum([scores[i] for i in elves]))
        for digit in comb:
            newscore = int(digit)
            scores.append(newscore)
            slen = len(scores)
            if slen > after:
                print(newscore, end="")
            if slen > after + 9:
                print()
                return

        for i, elf in enumerate(elves):
            elves[i] = (elf + 1 + scores[elf]) % slen


if __name__ == '__main__':
    main()

