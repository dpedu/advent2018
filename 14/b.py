#!/usr/bin/env python3


def main():
    elves = [0, 1]
    scores = [3, 7]
    endseq = [5, 0, 3, 7, 6, 1]  # puzzle input
    sqlen = len(endseq)

    while True:
        comb = str(sum([scores[i] for i in elves]))
        for digit in comb:
            newscore = int(digit)
            scores.append(newscore)
            if scores[-sqlen:] == endseq:
                print(len(scores) - len(endseq))
                return
        scorelen = len(scores)
        for i, elf in enumerate(elves):
            elves[i] = (elf + 1 + scores[elf]) % scorelen


if __name__ == '__main__':
    main()

