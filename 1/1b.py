#!/usr/bin/env python3


def main():
    total = 0
    seen = {}
    with open("input.txt") as f:
        numbers = [int(i) for i in f.readlines()]
    while True:
        for number in numbers:
            total += number
            if total in seen:
                print(total)
                return
            seen[total] = None


if __name__ == '__main__':
    main()
